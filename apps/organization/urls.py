from django.urls import path
from django.views.generic import TemplateView
from organization.views import OrgView,OrgHomeView,AddAskView

app_name = 'organization'

urlpatterns = [
    # 课程机构列表
    path('list/',OrgView.as_view(),name='org_list'),
    path('teacher_list/',TemplateView.as_view(template_name='teacher_list.html'),name='teacher_list'),
    path('org_home/(?P<org_id>\d+)/',TemplateView.as_view(template_name='org_home.html'),name='org_home'),
    path('add_ask',TemplateView.as_view(template_name='add_ask.html'),name='add_ask')
]