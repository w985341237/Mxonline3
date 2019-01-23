from django.urls import path
from django.views.generic import TemplateView

# 添加命名空间
app_name='users'

urlpatterns = [
    path('my_message/',TemplateView.as_view(template_name='my_message.html'),name='my_message'),
    path('user_info/',TemplateView.as_view(template_name='user_info.html'),name='user_info'),
]