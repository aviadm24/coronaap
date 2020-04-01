from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('update_sheets', views.update_sheets, name='update_sheets'),
    path('check_update', views.check_update, name='check_update'),
    path('aviad_sheets', views.aviad_sheets, name='aviad_sheets'),
    path('create_sheet', views.create_sheet, name='create_sheet')
]
