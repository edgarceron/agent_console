"""Urls for users app"""
from django.urls import path
from . import views
from . import webservices

urlpatterns = [
    path('create', views.form_profile, name='form_profile'),
    path('listing_profile', views.listing_profile, name='listing_profile'),
    path('update/<int:profile_id>', views.form_profile, name='update_profile'),
    path('add', webservices.add_profile, name='add_profile'),
    path('replace/<int:profile_id>', webservices.replace_profile, name='replace_profile'),
    path('picker_search', webservices.picker_search_profile, name='picker_search_profile'),
    path('data_list', webservices.list_profile, name='data_list_profile'),
    path('get/<int:profile_id>', webservices.get_profile, name='get_profile'),
    path('delete/<int:profile_id>', webservices.delete_profile, name='delete_profile'),
    path('toggle/<int:profile_id>', webservices.toggle_profile, name='toggle_profile'),
]