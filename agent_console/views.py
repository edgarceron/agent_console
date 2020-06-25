""" Contains the view for the agent consoole module"""
from django.shortcuts import render
from users.permission_validation import PermissionValidation
from .models import UserAgent, AgentConsoleOptions
def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {"name": "form_user_agent", "label": "Formulario para usuario con agente"},
        {"name": "agent_console", "label": "Vista de la consola principal del agente"},
    ]
    return actions

def form_user_agent(request, user_id=0):
    "Returns the rendered template for the given user."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('form_user_agent')
    if validation['status']:
        if user_id == 0:
            action = "Crear"
        else:
            action = "Actualizar"

        return render(
            request,
            'agent_console/form.html',
            {
                'id':user_id,
                'action':action,
                'username': permission_obj.user.name
            }
        )
    return PermissionValidation.error_response_view(validation, request)

def agent_console(request):
    "Returns the rendered template for the given user."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('agent_console')
    if validation['status']:
        id_user = permission_obj.user.id
        try:
            user_agent = UserAgent.objects.get(user=id_user)
            id_agent = user_agent.agent
        except UserAgent.DoesNotExist:
            id_agent = "null"

        data = {
            'id_agent': id_agent,
            'username': permission_obj.user.name
        }
        return render(
            request,
            'agent_console/agent_console.html',
            data
        )
    return PermissionValidation.error_response_view(validation, request)

def options_form(request):
    "Returns the rendered template for the given user."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('agent_console')
    if validation['status']:
        data = {
            "success": "True",
            'username': permission_obj.user.name
        }

        return render(
            request,
            'agent_console/options_form.html',
            data
        )
    return PermissionValidation.error_response_view(validation, request)

# Create your views here.
