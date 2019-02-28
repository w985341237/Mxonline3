from django.urls import path,re_path
from django.views.generic import TemplateView
from organization.views import OrgView,OrgHomeView,AddAskView,OrgTeacherView,OrgCourseView,OrgDescView,AddFavView,TeacherListView,TeacherDetailView

app_name = 'organization'

urlpatterns = [
    # 课程机构列表
    path('list/',OrgView.as_view(),name='org_list'),
    # 讲师列表
    path('teacher/list/',TeacherListView.as_view(),name='teacher_list'),
    # 机构主页
    path('org_home/<int:org_id>/',OrgHomeView.as_view(),name='org_home'),
    # 机构讲师
    path('org_teacher/<int:org_id>/',OrgTeacherView.as_view(),name='org_teacher'),
    # 机构课程
    path('course/<int:org_id>/',OrgCourseView.as_view(),name='org_course'),
    # 机构介绍
    path('desc/<int:org_id>/',OrgDescView.as_view(),name='org_desc'),
    # 我要学习
    path('add_ask/',AddAskView.as_view(),name='add_ask'),
    # 讲师详情
    path('teacher/detail/<int:teacher_id>/',TeacherDetailView.as_view(),name='teacher_detail'),
    # 收藏
    path('add_fav/',AddFavView.as_view(),name='add_fav')
]