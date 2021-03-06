"""Mxonline3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
import xadmin
from django.views.generic import TemplateView
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetPwdView, ModifyPwdView, IndexView, LogoutView
from .settings import MEDIA_ROOT  # ,STATIC_ROOT
from django.views.static import serve  # 上传媒体加载包


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    # TemplateView.as_view会将template转换为view
    # 首页
    path('', IndexView.as_view(), name="index"),
    # 登录
    path('login/', LoginView.as_view(), name='login'),
    # 登出
    path('logout/',LogoutView.as_view(), name='logout'),
    # 注册
    path('register/', RegisterView.as_view(), name='register'),
    # 忘记密码
    path('forget_pwd/',ForgetPwdView.as_view(),name='forget_pwd'),
    # 修改密码
    path('modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd'),
    # 用户相关
    path('users/', include('users.urls')),
    # 课程相关
    path('course/', include('course.urls')),
    # 机构相关
    path('org/', include('organization.urls', namespace='org')),
    # 验证码
    path('captcha/', include('captcha.urls')),
    # 富文本编辑器
    path('ueditor/',include('DjangoUeditor.urls')),
    # 激活用户url，利用正则表达式提取激活码
    re_path(
        'active/(?P<active_code>.*)/',
        ActiveUserView.as_view(),
        name='user_active'),
    # 处理图片显示的url,使用Django自带的serve
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    # 重置密码
    re_path(
        'reset/(?P<active_code>.*)/',
        ResetPwdView.as_view(),
        name='reset_pwd'),
    # 配置静态文件上传的访问处理url
    # re_path('static/(?P<path>.*)', serve, {"document_root": STATIC_ROOT})
]

# 全局404页面配置
handler404 = 'users.views.page_not_found'
# 全局500页面配置
handler500 = 'users.views.page_error'
