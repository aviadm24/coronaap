from django.urls import path
from django.views.generic import TemplateView
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('yonatan/', TemplateView.as_view(template_name="main/yom.html")),
    path('incoming_sms', views.incoming_sms, name='incoming_sms'),
    path('send_sms', views.send_sms, name='send_sms'),
    path('cancel_sms', views.cancel_sms, name='cancel_sms'),
    path('task1/', TemplateView.as_view(template_name="main/task1.html")),
    path('task2/', TemplateView.as_view(template_name="main/task2.html")),
    path('task3/', TemplateView.as_view(template_name="main/task3.html")),
    path('task4/', TemplateView.as_view(template_name="main/task4.html")),
    path('task5/', TemplateView.as_view(template_name="main/task5.html")),
    path('task6/', TemplateView.as_view(template_name="main/task6.html")),
    path('task7/', TemplateView.as_view(template_name="main/task7.html")),
]
