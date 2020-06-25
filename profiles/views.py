from django.shortcuts import render
from users.permission_validation import PermissionValidation
from .models import Action, App

# Create your views here.
def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {"name": "listing_profile", "label": "Pagina de listado del modulo de perfiles"},
        {"name": "form_profile", "label": "Pagina de formulario del modulo de perfiles"}
    ]
    return actions

def form_profile(request, profile_id=0):
    "Returns the rendered template for the given profile."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('form_profile')
    if validation['status']:
        if profile_id == 0:
            action = "Crear"
        else:
            action = "Actualizar"

        result = actions_by_app()
        return render(
            request,
            'profiles/form.html',
            {
                'id':profile_id,
                'action':action,
                'result': result,
                'username': permission_obj.user.name
            }
        )
    return PermissionValidation.error_response_view(validation, request)

def actions_by_app():
    """Return a list which contains each app with its info and actios"""
    result = []
    apps = App.objects.all()
    for app in apps:
        id_app = app.id
        actions = Action.objects.filter(app=id_app)
        actionslist = []
        for action in actions:
            actionslist.append({'id': action.id, 'name':action.name, 'label': action.label})
        result.append({'id': app.id, 'label': app.label, 'actions': actionslist})
    return result

def listing_profile(request):
    "Returns the rendered template for profile listing."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('listing_profile')
    if validation['status']:
        return render(
            request,
            'profiles/listing.html',
            {
                'username': permission_obj.user.name
            }
        )
    return PermissionValidation.error_response_view(validation, request)
