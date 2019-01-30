# encoding = utf-8

import django
import os
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile,EmailVerifyRecord
# 并集运算
from django.db.models import Q

#基于类实现需要继承的View
from django.views.generic.base import View
from .forms import LoginForm,RegisterForm,ActiveForm
from utils.email_send import send_register_email

# Create your views here.
os.environ.setdefault('DJANGO_SETTING_MODULE', 'Mxonline3.settings')
django.setup()

# 实现用户名邮箱均可登录
# 继承ModelBackend类，因为它有方法authenticate,可点进源码查看


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询

            user = UserProfile.objects.get(
                Q(username=username) | Q(email=username))

            # django的后台中密码加密：所有不能有password=password
            # UserProfile继承的AbstractUser中有def
            # check_password(self,raw_password):

            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 用户登录视图

class LoginView(View):
    # 直接调用get方法免去判断
    def get(self,request):
        # render就是渲染html返回用户
        # render三变量：request 模板名称 一个字典鞋面传给前端的值
        return render(request, 'login.html', {})
    def post(self,request):
        # 类实例化需要一个字典参数dict:request.POST就是一个QueryDict所以直接传入
        # POST中的username password会对应到form中
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 取不到时为空，username,password为前端页面name值
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')

            # authenticate调用只需要传入用户名和密码。成功会返回user对象，失败返回null
            user = authenticate(username=user_name, password=pass_word)

            # 如果不是null，说明验证成功
            if user is not None:
                # login_in 两参数：request,user
                # 实际是对request写了一部分东西进去，然后在render的时候
                # request是要render回去的，这些信息也就随着返回浏览器。完成登录
                login(request, user)
                # 跳转到首页
                return render(request, 'index.html')
            # 仅当用户真的密码出错时，返回错误信息
            return render(request, 'login.html', {'msg': '用户名或密码错误！'})
        # 验证不成功返回登录页面
        return render(request,'login.html',{'login_form':login_form})


# 注册视图


class RegisterView(View):
    def get(self,request):
        # 添加验证码
        register_form = RegisterForm()
        return render(request,'register.html',{'register_form':register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            e_mail = request.POST.get('email','')
            pass_word = request.POST.get('password','')

            # 发送注册激活邮件
            send_register_email(e_mail,'register')

            user_profile = UserProfile()
            user_profile.username = e_mail
            user_profile.email = e_mail

            # 默认激活状态
            user_profile.is_active = False

            # make_password(pass_word)会对密码加密进行保存
            user_profile.password=make_password(pass_word)
            user_profile.save()
            pass
        return render(request,'register.html',{'register_form':register_form,'msg':'邮箱或密码格式错误'})


# 激活用户的视图

class ActiveUserView(View):
    def get(self,request,active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.fliter(code=active_code)
        # 激活form负责给激活跳转进来的人加验证码
        active_form = ActiveForm(request.GET)
        # 如果不为空也就是有用户
        if all_record:
            for record in all_record:
                #获取到对应的邮箱
                email = record.email
                # 查找到邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                # 激活成功，跳转到登录页面
                return render(request,'login.html',)
        # 自己随便输的验证码
        return render(request,'register.html',{'msg':'您的激活链接无效','active_form':active_form})
