from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('update_sheets', views.update_sheets, name='update_sheets'),
    path('aviad_sheets', views.aviad_sheets, name='aviad_sheets'),
    path('create_sheet', views.create_sheet, name='create_sheet'),
    path('send_sms', views.send_sms, name='send_sms'),
    path('cancel_sms', views.cancel_sms, name='cancel_sms')
]
