from django.urls import path
from django.views.generic import TemplateView

app_name = 'course'

urlpatterns = [
    path('list/',TemplateView.as_view(template_name='course_list.html'),name='list'),
    path('detail/<int:course_id>/',TemplateView.as_view(template_name='course_detail.html'),name='course_detail')
]