"""Urls for agent_console app"""
from django.urls import path
from . import views
from . import webservices

urlpatterns = [
    path('create', views.form_user_agent, name='create_user_agent'),
    path('update/<int:user_id>', views.form_user_agent, name='update_user_agent'),
    path('set_user_agent', webservices.set_user_agent, name='set_user_agent'),
    path('get_agent/<int:user_id>', webservices.get_agent, name='get_agent'),
    path('picker_search_agent', webservices.picker_search_agent, name='picker_search_agent'),
    path('agent_console', views.agent_console, name='agent_console'),
    path('agent_state', webservices.agent_state, name='agent_state'),
    path('get_crm_url', webservices.get_crm_url, name='get_crm_url'),
    path('options_form', views.options_form, name='options_form_agent_console'),
    path(
        'replace_options_agent_console',
        webservices.replace_options_agent_console,
        name='replace_options_agent_console'),
    path(
        'get_options_agent_console',
        webservices.get_options_agent_console,
        name='get_options_agent_console'),
    path('auto_generate_users', webservices.auto_generate_users, name='auto_generate_users'),

]
