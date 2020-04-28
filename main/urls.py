from django.urls import path
from django.views.generic import TemplateView
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('yonatan/', TemplateView.as_view(template_name="main/map.html")),
    path('incoming_sms', views.incoming_sms, name='incoming_sms'),
    path('send_sms', views.send_sms, name='send_sms'),
    path('cancel_sms', views.cancel_sms, name='cancel_sms'),
    path('gvura/', TemplateView.as_view(template_name="main/gvura.html")),
    path('semel/', TemplateView.as_view(template_name="main/semel.html")),
    path('shichrur1/', TemplateView.as_view(template_name="main/shichrur.html")),
    path('shichrur2/', TemplateView.as_view(template_name="main/shichrur2.html")),
    path('hapoelBeitShean/', TemplateView.as_view(template_name="main/hapoelBeitShean.html")),
    path('tarbut1/', TemplateView.as_view(template_name="main/tarbut.html")),
    path('tarbut2/', TemplateView.as_view(template_name="main/tarbut2.html")),
    path('pitaron/', TemplateView.as_view(template_name="main/pitaron.html")),
    path('nofey/', TemplateView.as_view(template_name="main/nofey.html")),
]
