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
from users.views import LoginView, RegisterView, ActiveUserView
from .settings import MEDIA_ROOT
from django.views.static import serve  # 上传媒体加载包

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    # TemplateView.as_view会将template转换为view
    path('', TemplateView.as_view(template_name='index.html'), name="index"),
    path('login/', LoginView.as_view(), name='login'),
    path(
        'logout/',
        TemplateView.as_view(
            template_name='logout.html'),
        name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path(
        'forget_pwd/',
        TemplateView.as_view(
            template_name='forget_pwd.html'),
        name='forget_pwd'),
    path('users/', include('users.urls')),
    path('course/', include('course.urls')),
    path('org/', include('organization.urls')),
    path('captcha/', include('captcha.urls')),
    # 激活用户url，利用正则表达式提取激活码
    re_path(
        'active/(?P<active_code>.*)/',
        ActiveUserView.as_view(),
        name='user_active'),
    # 处理图片显示的url,使用Django自带的serve
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
]
