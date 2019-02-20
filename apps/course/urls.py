from django.urls import path
from django.views.generic import TemplateView
from course.views import CourseListView


app_name = 'course'

urlpatterns = [
    path('list/',CourseListView.as_view(),name='list'),
    path('detail/<int:course_id>/',TemplateView.as_view(template_name='course_detail.html'),name='course_detail')
]