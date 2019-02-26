from django.urls import path
from django.views.generic import TemplateView
from course.views import CourseListView,CourseDetailView,CourseInfoView,CourseCommentView,AddCommentView,VideoPlayView


app_name = 'course'

urlpatterns = [
    path('list/',CourseListView.as_view(),name='list'),
    path('detail/<int:course_id>/',CourseDetailView.as_view(),name='course_detail'),
    path('info/<int:course_id>/',CourseInfoView.as_view(),name='course_info'),
    path('comments/<int:course_id>/',CourseCommentView.as_view(),name='course_comments'),
    path('add_comment/',AddCommentView.as_view(),name='add_comment'),
    path('video/<int:video_id>/',VideoPlayView.as_view(),name='video_play'),
]