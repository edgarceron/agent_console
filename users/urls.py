"""Urls for users app"""
from django.urls import path
from . import views
from . import webservices

urlpatterns = [
    path('create', views.form_user, name='create_user'),
    path('listing', views.listing_user, name='listing_user'),
    path('update/<int:user_id>', views.form_user, name='update_user'),
    path('add', webservices.add_user, name='add_user'),
    path('replace/<int:user_id>', webservices.replace_user, name='replace_user'),
    path('picker_search', webservices.picker_search_user, name='picker_search_user'),
    path('data_list', webservices.list_user, name='data_list_user'),
    path('get/<int:user_id>', webservices.get_user, name='get_user'),
    path('delete/<int:user_id>', webservices.delete_user, name='delete_user'),
    path('toggle/<int:user_id>', webservices.toggle_user, name='toggle_user'),
    path('login', webservices.login, name='login_user'),
    path('logout', webservices.logout, name='logout')
]
