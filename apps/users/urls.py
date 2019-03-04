from django.urls import path
from django.views.generic import TemplateView
from users.views import UserInfoView, MyCourseView, MyFavOrgView, MyFavCourseView, MyFavTeacherView, MyMessageView, UploadImageView, UpdatePwdView, SendMailCodeView, UpdateEmailView

# 添加命名空间
app_name = 'users'

urlpatterns = [
    # 个人资料
    path('info/', UserInfoView.as_view(), name='user_info'),
    # 我的课程
    path('mycourse/', MyCourseView.as_view(), name='mycourse'),
    # 机构收藏
    path('myfav_org/', MyFavOrgView.as_view(), name='myfav_org'),
    # 课程收藏
    path('myfav_course/', MyFavCourseView.as_view(), name='myfav_course'),
    # 讲师收藏
    path('myfav_teacher/', MyFavTeacherView.as_view(), name='myfav_teacher'),
    # 我的消息
    path('my_message/', MyMessageView.as_view(), name='my_message'),
    # 修改头像
    path('image/upload/', UploadImageView.as_view(), name='image_upload'),
    # 修改密码
    path('update/pwd/', UpdatePwdView.as_view(), name='update_pwd'),
    # 修改邮箱发送验证码
    path('sendemail_code/', SendMailCodeView.as_view(), name='sendemail_code'),
    # 修改邮箱
    path('update_email/', UpdateEmailView.as_view(), name='update_email')
]
