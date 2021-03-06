# encoding = utf-8

import django
import os
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import ModelBackend
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
# 并集运算
from django.db.models import Q

from .models import UserProfile, EmailVerifyRecord, Banner
from course.models import Course
from organization.models import CourseOrg, Teacher
from operation.models import UserCourse, UserFavorite, UserMessage

# 基于类实现需要继承的View
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm, ActiveForm, ForgetForm, ModifyPwdForm, UserInfoForm, ImageUploadForm, UpdateEmailForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from pure_pagination import Paginator, PageNotAnInteger, EmptyPage

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
    def get(self, request):
        # render就是渲染html返回用户
        # render三变量：request 模板名称 一个字典鞋面传给前端的值
        redirect_url = request.GET.get('next', '')
        return render(request, 'login.html', {"redirect_url": redirect_url})

    def post(self, request):
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
                if user.is_active:
                    # login_in 两参数：request,user
                    # 实际是对request写了一部分东西进去，然后在render的时候
                    # request是要render回去的，这些信息也就随着返回浏览器。完成登录
                    login(request, user)
                    # 跳转到首页 user request会被带回到首页
                    # 增加重定向回原网页
                    redirect_url = request.POST.get('next', '')
                    if redirect_url:
                        return HttpResponseRedirect(redirect_url)
                    return HttpResponseRedirect(reverse('index'))
                # 用户未激活登录
                else:
                    return render(request, 'login.html', {'msg': '用户未激活！'})
            # 仅当用户真的密码出错时，返回错误信息
            return render(request, 'login.html', {'msg': '用户名或密码错误！'})
        # 验证不成功返回登录页面
        return render(request, 'login.html', {'login_form': login_form})

# 用户登出


class LogoutView(View):
    def get(self, request):
        # 采用django自带的函数完成登出功能
        logout(request)
        # 不采用之前的render，而是采用重定向返回到首页
        return HttpResponseRedirect(reverse('index'))


# 注册视图


class RegisterView(View):
    def get(self, request):
        # 添加验证码
        register_form = RegisterForm()
        return render(request, 'register.html', {
                      'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            e_mail = request.POST.get('email', '')
            # 验证邮箱是否被注册
            if UserProfile.objects.filter(email=e_mail):
                return render(request, 'register.html', {
                              'register_form': register_form, 'msg': '该邮箱已经被注册过了'})
            else:
                pass_word = request.POST.get('password', '')

                # 发送注册激活邮件
                send_register_email(e_mail, 'register')

                user_profile = UserProfile()
                user_profile.username = e_mail
                user_profile.email = e_mail

                # 默认激活状态
                user_profile.is_active = False

                # make_password(pass_word)会对密码加密进行保存
                user_profile.password = make_password(pass_word)
                user_profile.save()

                # 写入欢迎注册的信息
                user_message = UserMessage()
                user_message.user = user_profile.id
                user_message.message = '欢迎注册王宁的慕课小站！'
                user_message.save()

                return render(request, 'login.html', {
                              'login_form': register_form})
        else:
            return render(request, 'register.html', {
                          'register_form': register_form, 'msg': '邮箱或密码格式错误'})


# 激活用户的视图

class ActiveUserView(View):
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        # 激活form负责给激活跳转进来的人加验证码
        active_form = ActiveForm(request.GET)
        # 如果不为空也就是有用户
        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 查找到邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                # 激活成功，跳转到登录页面
                return render(request, 'login.html',)
        # 自己随便输的验证码
        return render(request, 'register.html', {
                      'msg': '您的激活链接无效', 'active_form': active_form})


# 忘记密码视图

class ForgetPwdView(View):
    def get(self, request):
        active_form = ActiveForm()
        return render(request, 'forget_pwd.html', {'active_form': active_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            e_mail = request.POST.get('email', '')
            # 发送找回密码的邮件
            send_register_email(e_mail, 'forget')
            # 发送成功，返回登录页，并提示消息
            return render(request, 'login.html', {'msg': u'找回密码邮件发送成功，请注意查收'})
        else:
            return render(request, 'forget_pwd.html', {
                          'forget_form': forget_form})


# 重置密码视图

class ResetPwdView(View):
    def get(self, request, active_code):
        # 用于检查邮箱是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        active_form = ActiveForm()
        if all_record:
            for recode in all_record:
                email = recode.email
                return render(request, 'password_reset.html',
                              {'active_code': active_code})
        # 自己瞎输入的验证码
        return render(request, 'forget_pwd.html', {
                      'msg': u'您的重置密码链接无效，请重新请求', 'active_form': active_form})


# 修改密码视图

class ModifyPwdView(View):
    def post(self, request,):
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            active_code = request.POST.get('active_code', '')
            # email = request.POST.get('email','')
            # 如果两次密码不一致，返回错误信息这块暂时未能实现
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {
                              'msg': '密码不一致', 'active_code': active_code})
            # 如果密码一致，找到激活码对应的邮箱
            all_record = EmailVerifyRecord.objects.filter(code=active_code)
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                # 加密成密文
                user.password = make_password(pwd2)
                # 保存
                user.save()
            return render(request, 'login.html', {'msg': '密码修改成功，请重新登录'})
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {
                          'email': email, 'modify_form': modifypwd_form})


# 首页视图

class IndexView(View):
    def get(self, request):
        # 取出轮播图只显示5个，并按照顺序排列
        all_banner = Banner.objects.all().order_by('index')[:5]
        # 取出轮播课程，取出3个
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        # 取出非轮播课程，显示6个
        courses = Course.objects.filter(is_banner=False)[:6]
        # 取出15个课程机构
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
                      'all_banner': all_banner, 'banner_courses': banner_courses, 'courses': courses, 'course_orgs': course_orgs})


# 个人中心修改信息

class UserInfoView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        return render(request, 'usercenter_info.html', {})

    def post(self, request):
        info_form = UserInfoForm(request.POST, instance=request.user)
        if info_form.is_valid():
            info_form.save()
            return HttpResponse('{"status":"success"}',
                                content_type='application/json')
        else:
            return HttpResponse(
                '{"status":"failure","msg":"个人信息填写错误"}', content_type='application/json')


# 我的课程
class MyCourseView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter_mycourse.html',
                      {'user_courses': user_courses})


# 机构收藏

class MyFavOrgView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(pk=org_id)
            org_list.append(org)
        return render(request, 'usercenter_myfav_org.html',
                      {'org_list': org_list})

# 课程收藏


class MyFavCourseView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(
            user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(pk=course_id)
            course_list.append(course)
        return render(request, 'usercenter_myfav_course.html',
                      {'course_list': course_list})

# 讲师收藏


class MyFavTeacherView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(
            user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(pk=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter_myfav_teacher.html',
                      {'teacher_list': teacher_list})


# 个人消息

class MyMessageView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        all_messages = UserMessage.objects.filter(user=request.user.id)

        # 进入当前页面，代表消息已读，清空未读消息
        all_unread_messages = UserMessage.objects.filter(
            user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, 10, request=request)
        messages = p.page(page)

        return render(request, 'usercenter_message.html',
                      {'messages': messages})


# 个人中心修改头像
class UploadImageView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def post(self, request):
        image_form = ImageUploadForm(
            request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status::"success"}',
                                content_type="application/json")
        return HttpResponse('{"status":"fail"}',
                            content_type="application/json")

# 个人中心修改密码


class UpdatePwdView(View):

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse(
                    '{"status":"fail","msg":"两次输入的密码不一致！', content_type="application/json")
            user = request.user
            user.password = make_password(pwd1)
            user.save()

            return HttpResponse('{"status::"success","msg":"修改成功"}',
                                content_type="application/json")
        else:
            return HttpResponse(
                '{"status":"fail","msg":"密码填写错误！', content_type="application/json")


# 个人中心修改邮箱发送验证码
class SendMailCodeView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse(
                '{"status":"fail","msg":"该邮箱已经被注册"}', content_type='application/json')
        else:
            send_register_email(email, send_type='update_email')
            return HttpResponse(
                '{"status":"success","msg":"邮件已发送"}', content_type='application/json')


# 个人中心修改邮箱
class UpdateEmailView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'

    def post(self, request):
        email = request.POST.get('email', '')
        email_code = request.POST.get('code', '')

        # 验证输入的验证码与发送的验证是否一致
        existed_records = EmailVerifyRecord.objects.filter(
            send_type='update_email', email=email, code=email_code)
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}',
                                content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码错误"}',
                                content_type='application/json')


# 404页面对应的处理函数
def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response("404.html", {

    })
    # 设置request的状态码
    response.status_code = 404
    return response


# 500页面对应的处理函数
def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response("500.html", {

    })
    # 设置request的状态码
    response.status_code = 500
    return response
