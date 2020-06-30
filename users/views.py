"Contains the views for the users app."
from django.shortcuts import render, redirect
from .permission_validation import PermissionValidation

def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {"name": "form_user", "label": "Pagina del formulario de usuario"},
        {"name": "listing_user", "label": "Pagina del listado de usuarios"}
    ]
    return actions

def form_user(request, user_id=0):
    "Returns the rendered template for the given user."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('form_user')
    if validation['status']:
        if user_id == 0:
            action = "Crear"
        else:
            action = "Actualizar"

        return render(
            request,
            'users/form.html',
            {
                'id':user_id,
                'action':action,
                'username': permission_obj.user.name
            }
        )
    return PermissionValidation.error_response_view(validation, request)

def listing_user(request):
    "Returns the rendered template for user listing."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('form_user')
    if validation['status']:
        return render(
            request,
            'users/listing.html',
            {
                'username': permission_obj.user.name
            }
        )
    return PermissionValidation.error_response_view(validation, request)

def view_my_profile(request):
    """Return rendered template for own user info"""
    permission_obj = PermissionValidation(request)
    if permission_obj.login_session is not None:
        user_id = permission_obj.user.id
        return render(
            request,
            'users/my_profile.html',
            {
                'username': permission_obj.user.name,
            }
        )
    return redirect('login')
