"""Urls for dashboard app"""
from django.urls import path
from . import views
from . import webservices

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard_dashboard'),
    path('create_datos', views.form, name='create_datos'),
    path('update_datos/<int:datos_id>', views.form, name='update_datos'),
    path('replace_datos/<int:datos_id>', webservices.replace_datos, name='replace_datos'),
    path('add_datos', webservices.add_datos, name='add_datos'),
    path('get_datos/<int:datos_id>', webservices.get_datos, name='get_datos'),
    path('get_llamadas', webservices.get_llamadas, name='get_llamadas'),
    path('get_cedula', webservices.get_cedula, name='get_cedula'),
]