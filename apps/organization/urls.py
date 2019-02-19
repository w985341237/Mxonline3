from django.urls import path,re_path
from django.views.generic import TemplateView
from organization.views import OrgView,OrgHomeView,AddAskView,OrgTeacherView,OrgCourseView,OrgDescView,AddFavView

app_name = 'organization'

urlpatterns = [
    # 课程机构列表
    path('list/',OrgView.as_view(),name='org_list'),
    path('teacher_list/',TemplateView.as_view(template_name='teacher_list.html'),name='teacher_list'),
    re_path('org_home/(?P<org_id>\d+)/',OrgHomeView.as_view(),name='org_home'),
    path('org_teacher/<int:org_id>/',OrgTeacherView.as_view(),name='org_teacher'),
    path('course/<int:org_id>/',OrgCourseView.as_view(),name='org_course'),
    path('desc/<int:org_id>/',OrgDescView.as_view(),name='org_desc'),
    path('add_ask/',AddAskView.as_view(),name='add_ask'),
    path('teacher/detail/<int:teacher_id>/',TemplateView.as_view(template_name='teacher_detail.html'),name='teacher_detail'),
    path('add_fav/',AddFavView.as_view(),name='add_fav')
]