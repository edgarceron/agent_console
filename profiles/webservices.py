"""Contains the webservices for the profiles app"""
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import ProfileSerializer, ProfilePermissionsSerializer
from .models import Profile, ProfilePermissions
from users.permission_validation import PermissionValidation

def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {"name": "add_profile", "label": "Webservice crear perfil"},
        {"name": "replace_profile", "label": "Webservice actualizar perfil"},
        {"name": "get_profile", "label": "Webservice obtener datos perfil"},
        {"name": "delete_profile", "label": "Webservice borrar perfil"},
        {"name": "picker_search_profile", "label": "Webservice picker de perfiles"},
        {"name": "list_profile", "label": "Webservice del listado de perfiles"},
        {"name": "toggle_profile", "label": "Webservice para cambiar estado del perfil"},
    ]
    return actions
   
@api_view(['POST'])
def add_profile(request):
    """Tries to create an profile and returns the result"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('add_profile')
    if validation['status']:
        json_actions = request.data['actions']
        profile_serializer = ProfileSerializer(data=request.data)
        actions = json.loads(json_actions)

        if profile_serializer.is_valid():
            profile_serializer.save()
            profile_id = profile_serializer.data['id']
            for x in range(0, len(actions)):
                actions[x]['profile'] = profile_id
                permission_serializer = ProfilePermissionsSerializer(data=actions[x])
                if permission_serializer.is_valid():
                    permission_serializer.save()

            return Response(
                {"success":True},
                status=status.HTTP_201_CREATED, content_type='application/json')

        data = error_data(profile_serializer)
        return Response(data, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['PUT'])
def replace_profile(request, profile_id):
    "Tries to update an user and returns the result"
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('replace_profile')
    if validation['status']:
        profile_obj = Profile.objects.get(id=profile_id)
        profile_serializer = ProfileSerializer(profile_obj, data=request.data)
        json_actions = request.data['actions']
        actions = json.loads(json_actions)

        if profile_serializer.is_valid():
            profile_serializer.save()
            profile_id = profile_serializer.data['id']
            for element in range(0, len(actions)):
                action_id = actions[element]['action']
                try:
                    permission_obj = ProfilePermissions.objects.get(
                        profile=profile_id, action=action_id)
                    actions[element]['profile'] = profile_id
                    permission_serializer = ProfilePermissionsSerializer(
                        permission_obj, data=actions[element])
                except:
                    actions[element]['profile'] = profile_id
                    permission_serializer = ProfilePermissionsSerializer(data=actions[element])
                
                if permission_serializer.is_valid():
                    permission_serializer.save()
                else:
                    print(permission_serializer.errors)
            return Response(
                {"success":True},
                status=status.HTTP_200_OK,
                content_type='application/json'
            )

        data = error_data(profile_serializer)
        return Response(data, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['POST'])
def get_profile(request, profile_id):
    "Return a JSON response with profile data for the given id"
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('get_profile')
    if validation['status']:
        profile_obj = Profile.objects.get(id=profile_id)
        profile_serializer = ProfileSerializer(profile_obj)
        permission_list = ProfilePermissions.objects.filter(profile=profile_obj.id)
        permissions_serializer = ProfilePermissionsSerializer(permission_list, many=True)

        data = {
            "success":True,
            "data": profile_serializer.data,
            "actions": permissions_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['DELETE'])
def delete_profile(request, profile_id):
    """Tries to delete an profile and returns the result."""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('delete_profile')
    if validation['status']:
        profile_obj = Profile.objects.get(id=profile_id)
        profile_obj.delete()
        data = {
            "success": True,
            "message": "Perfil elminado exitosamente"
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['POST'])
def toggle_profile(request, profile_id):
    """Toogles the active state for a given profile"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('toggle_profile')
    if validation['status']:
        profile_obj = Profile.objects.get(id=profile_id)
        previous = profile_obj.active

        if previous:
            message = "Perfil desactivado con exito"
        else:
            message = "Perfil activado con exito"

        profile_obj.active = not profile_obj.active
        profile_obj.save()
        data = {
            "success": True,
            "message": message
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['POST'])
def picker_search_profile(request):
    "Returns a JSON response with user data for a selectpicker."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('picker_search_profile')
    if validation['status']:
        value = request.data['value']
        queryset = Profile.profile_picker_filter(value)
        serializer = ProfileSerializer(queryset, many=True)
        result = serializer.data

        data = {
            "success": True,
            "result": result
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['POST'])
def list_profile(request):
    """ Returns a JSON response containing registered users"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('list_profile')
    if validation['status']:
        sent_data = request.data
        draw = int(sent_data['draw'])
        start = int(sent_data['start'])
        length = int(sent_data['length'])
        search = sent_data['search[value]']

        records_total = Profile.objects.count()

        if search != '':
            queryset = Profile.profiles_listing_filter(search, start, length)
            records_filtered = Profile.profiles_listing_filter(search, start, length, True)
        else:
            queryset = Profile.objects.all()[start:start + length]
            records_filtered = records_total


        result = ProfileSerializer(queryset, many=True)
        data = {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': result.data
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    return PermissionValidation.error_response_webservice(validation, request)

def error_data(serializer):
    """Return a common JSON error result"""
    error_details = []
    for key in serializer.errors.keys():
        error_details.append({"field": key, "message": serializer.errors[key][0]})

    data = {
        "Error": {
            "success": False,
            "status": 400,
            "message": "Los datos enviados no son validos",
            "details": error_details
        }
    }
    return data
    