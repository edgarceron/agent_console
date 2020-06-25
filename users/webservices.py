"""Contains the webservices for the users app"""
import datetime
import pytz
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import UserSerializer, BasicUserSerializer
from .models import User, LoginSession
from .permission_validation import PermissionValidation


def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {"name": "add_user", "label": "Webservice crear usuario"},
        {"name": "replace_user", "label": "Webservice actualizar usuario"},
        {"name": "get_user", "label": "Webservice obtener datos usuario"},
        {"name": "delete_user", "label": "Webservice borrar usuario"},
        {"name": "picker_search_user", "label": "Webservice picker de usuarios"},
        {"name": "list_user", "label": "Webservice del listado de usuarios"},
        {"name": "toggle_user", "label": "Webservice para cambiar estado del usuario"},
    ]
    return actions

@api_view(['POST'])
def add_user(request):
    """Tries to create an user and returns the result"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('add_user')
    if validation['status']:
        data = request.data.copy()
        password = data['password']
        hasher = PBKDF2PasswordHasher()
        data['password'] = hasher.encode(password, "Wake Up, Girls!")
        user_serializer = UserSerializer(data=data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(
                {"success":True, "user_id":user_serializer.data['id']},
                status=status.HTTP_201_CREATED,
                content_type='application/json')

        data = error_data(user_serializer)
        return Response(data, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['PUT'])
def replace_user(request, user_id):
    "Tries to update an user and returns the result"
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('replace_user')
    if validation['status']:
        user_obj = User.objects.get(id=user_id)
        data = request.data.copy()
        password = data['password']
        if password == "":
            data['password'] = user_obj.password
        else:
            hasher = PBKDF2PasswordHasher()
            data['password'] = hasher.encode(password, "Wake Up, Girls!")
        
        user_serializer = UserSerializer(user_obj, data=data)

        if user_serializer.is_valid():
            user_serializer.save()
            return Response(
                {"success":True, "user_id":user_id},
                status=status.HTTP_200_OK,
                content_type='application/json'
            )

        data = error_data(user_serializer)
        return Response(data, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['POST'])
def get_user(request, user_id):
    "Return a JSON response with user data for the given id"
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('get_user')
    if validation['status']:
        user_obj = User.objects.get(id=user_id)
        user_serializer = UserSerializer(user_obj)
        user_data = user_serializer.data.copy()
        del user_data['password']

        data = {
            "success":True,
            "data":user_data
        }
    
        return Response(
            data,
            status=status.HTTP_200_OK,
            content_type='application/json'
        )
    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['DELETE'])
def delete_user(request, user_id):
    """Tries to delete an user and returns the result."""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('get_user')
    if validation['status']:
        user_obj = User.objects.get(id=user_id)
        user_obj.delete()
        data = {
            "success": True,
            "message": "Usuario elminado exitosamente"
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['POST'])
def toggle_user(request, user_id):
    """Toogles the active state for a given user"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('toggle_user')

    user_obj = User.objects.get(id=user_id)
    previous = user_obj.active
    if validation['status']:
        if previous:
            message = "Usuario desactivado con exito"
        else:
            message = "Usuario activado con exito"

        user_obj.active = not user_obj.active
        user_obj.save()
        data = {
            "success": True,
            "message": message
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['POST'])
def picker_search_user(request):
    "Returns a JSON response with user data for a selectpicker."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('picker_search_user')
    if validation['status']:
        value = request.data['value']
        queryset = User.usersPickerFilter(value)
        serializer = BasicUserSerializer(queryset, many=True)
        result = serializer.data

        data = {
            "success": True,
            "result": result
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['POST'])
def list_user(request):
    """ Returns a JSON response containing registered users"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('list_user')
    if validation['status']:
        sent_data = request.data
        draw = int(sent_data['draw'])
        start = int(sent_data['start'])
        length = int(sent_data['length'])
        search = sent_data['search[value]']

        records_total = User.objects.count()

        if search != '':
            queryset = User.users_listing_filter(search, start, length)
            records_filtered = User.users_listing_filter(search, start, length, True)
        else:
            queryset = User.objects.all()[start:start + length]
            records_filtered = records_total


        result = BasicUserSerializer(queryset, many=True)
        data = {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': result.data
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['POST'])
def login(request):
    """Logs in the user if given credentials are valid"""
    username = request.data['username']
    password = request.data['password']
    try:
        user = User.objects.get(username=username)
    except:
        user = None
    if user is not None:
        encoded = user.password
        hasher = PBKDF2PasswordHasher()
        login_valid = hasher.verify(password, encoded)

        if login_valid:
            key = username + str(datetime.datetime.now())
            key = hasher.encode(key, 'key', 10)
            life = datetime.datetime.now() + datetime.timedelta(hours=14)
            timezone = pytz.timezone("America/Bogota")
            life_aware = timezone.localize(life)
            loginsession = LoginSession(key=key, life=life_aware, user=user)
            loginsession.save()
            request.session['loginsession'] = key
            data = {
                'success': True,
                'key': key
            }
            return Response(data, status=status.HTTP_200_OK, content_type='application/json')
        
    data = {
        'success': False,
        'message':"Nombre de usuario o contraseña incorrectos"
    }
    return Response(data, status=status.HTTP_200_OK, content_type='application/json')

@api_view(['POST'])
def logout(request):
    """ Logs out the user from the system"""
    permission_obj = PermissionValidation(request)
    permission_obj.logout(request)
    data = {
        'success': True
    }
    return Response(data, status=status.HTTP_200_OK, content_type='application/json')

def error_data(user_serializer):
    """Return a common JSON error result"""
    error_details = []
    for key in user_serializer.errors.keys():
        error_details.append({"field": key, "message": user_serializer.errors[key][0]})

    data = {
        "Error": {
            "success": False,
            "status": 400,
            "message": "Los datos enviados no son validos",
            "details": error_details
        }
    }
    return data
    