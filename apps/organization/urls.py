from django.urls import path,re_path
from django.views.generic import TemplateView
from organization.views import OrgView,OrgHomeView,AddAskView

app_name = 'organization'

urlpatterns = [
    # 课程机构列表
    path('list/',OrgView.as_view(),name='org_list'),
    path('teacher_list/',TemplateView.as_view(template_name='teacher_list.html'),name='teacher_list'),
    re_path('org_home/(?P<org_id>\d+)/',TemplateView.as_view(template_name='org_home.html'),name='org_home'),
    path('add_ask',AddAskView.as_view(),name='add_ask')
]