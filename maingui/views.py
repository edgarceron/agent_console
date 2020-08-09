""" Contains the views for the maingui module"""
import pytz
from datetime import datetime
from django.shortcuts import render, redirect
from users.permission_validation import PermissionValidation

def index(request):
    """ Returns the render for the index page"""
    permission_obj = PermissionValidation(request)
    if permission_obj.login_session is not None:
        return redirect('agent_console')
    return redirect('login')

def login(request):
    """ Returns the render for the login page"""
    permission_obj = PermissionValidation(request)
    timezone = pytz.timezone("America/Bogota")
    date_aware = timezone.localize(datetime.now())
    if permission_obj.login_session is None or permission_obj.login_session.life < date_aware:
        now = datetime.now()
        return render(
            request,
            'maingui/login.html',
            {
                'year': str(now.year)
            }
        )
    return redirect('index')
