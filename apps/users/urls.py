from django.urls import path
from django.views.generic import TemplateView
from users.views import UserInfoView,MyCourseView,MyFavOrgView,MyMessageView,UploadImageView,UpdatePwdView,SendMailCodeView,UpdateEmailView

# 添加命名空间
app_name='users'

urlpatterns = [
    path('my_message/',TemplateView.as_view(template_name='my_message.html'),name='my_message'),
    path('info/', UserInfoView.as_view(), name='user_info'),
    path('mycourse/',MyCourseView.as_view(),name='mycourse'),
    path('myfav_org/',MyFavOrgView.as_view(),name='myfav_org'),
    path('my_message/',MyMessageView.as_view(),name='my_message'),
    path('image/upload/',UploadImageView.as_view(),name='image_upload'),
    path('update/pwd/',UpdatePwdView.as_view(),name='update_pwd'),
    path('sendmail_code/',SendMailCodeView.as_view(),name='sendmail_code'),
    path('update_email/',UpdateEmailView.as_view(),name='update_email')
]