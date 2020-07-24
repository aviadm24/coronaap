from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "exceldb"

urlpatterns = [
    path('', views.index, name='index'),
    # path('yonatan/', TemplateView.as_view(template_name="main/map.html"))
]
