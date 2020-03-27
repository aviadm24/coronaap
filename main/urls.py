from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('create_sheet', views.create_sheet, name='create_sheet')
]
