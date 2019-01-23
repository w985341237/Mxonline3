from django.urls import path
from django.views.generic import TemplateView

app_name = 'org'

urlpatterns = [
    path('org_list/',TemplateView.as_view(template_name='org_list.html'),name='org_list'),
path('teacher_list/',TemplateView.as_view(template_name='teacher_list.html'),name='teacher_list'),
]