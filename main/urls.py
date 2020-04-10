from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('incoming_sms', views.incoming_sms, name='incoming_sms'),
    path('send_sms', views.send_sms, name='send_sms'),
    path('cancel_sms', views.cancel_sms, name='cancel_sms')
]
