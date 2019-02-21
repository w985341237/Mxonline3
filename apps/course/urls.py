from django.urls import path
from django.views.generic import TemplateView
from course.views import CourseListView,CourseDetailView


app_name = 'course'

urlpatterns = [
    path('list/',CourseListView.as_view(),name='list'),
    path('detail/<int:course_id>/',CourseDetailView.as_view(),name='course_detail')
]