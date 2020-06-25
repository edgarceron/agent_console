"""Contains the webservices for the maingui app"""
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import DatosPersonalesSerializer
from .models import DatosPersonales
from agent_console.models import CurrentCallEntry

# Create your views here.
def get_actions():
    actions = [
       #{"name": "index", "label": "Pagina principal del modulo de usuario"},
    ]
    return actions

@api_view(['POST'])
def add_datos(request):
    """Tries to create an data and returns the result"""
    datos_serializer = DatosPersonalesSerializer(data=request.data)

    if datos_serializer.is_valid():
        datos_serializer.save()
        return Response(
            {"success":True},
            status=status.HTTP_201_CREATED, content_type='application/json')

    data = error_data(datos_serializer)
    return Response(data, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

@api_view(['PUT'])
def replace_datos(request, datos_id):
    "Tries to update an datos and returns the result"
    #TODO verificar usuario y permisos
    datos_obj = DatosPersonales.objects.get(id=datos_id)
    datos_serializer = DatosPersonalesSerializer(datos_obj, data=request.data)

    if datos_serializer.is_valid():
        datos_serializer.save()
        return Response(
            {"success":True},
            status=status.HTTP_200_OK,
            content_type='application/json'
        )

    data = error_data(datos_serializer)
    return Response(data, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')

@api_view(['POST'])
def get_datos(request, datos_id):
    """Return a JSON response with datos data for the given id"""
    #TODO verificar usuario y permisos
    datos_obj = DatosPersonales.objects.get(id=datos_id)
    datos_serializer = DatosPersonalesSerializer(datos_obj)

    data = {
        "success":True,
        "data": datos_serializer.data
    }
 
    return Response(
        data,
        status=status.HTTP_200_OK,
        content_type='application/json'
    )

@api_view(['POST'])
def get_cedula(request):
    cedula = request.data['cedula']
    try:
        datos_obj = DatosPersonales.objects.get(identificacion=cedula)
        datos_serializer = DatosPersonalesSerializer(datos_obj)
        data = datos_serializer.data
    except:
        data = None

    data = {
        "success":True,
        "data": data
    }
 
    return Response(
        data,
        status=status.HTTP_200_OK,
        content_type='application/json'
    )
    

@api_view(['POST'])
def get_llamadas(request):
    tel = None
    try:
        llamada = CurrentCallEntry.objects.get(id_agent=9)
        tel = llamada.callerid
        datos_obj = DatosPersonales.objects.get(telefono=tel)
        datos_serializer = DatosPersonalesSerializer(datos_obj)
        data = datos_serializer.data
    except:
        data = None
        

    data = {
        "success":True,
        "data": data,
        "phone": tel
    }
 
    return Response(
        data,
        status=status.HTTP_200_OK,
        content_type='application/json'
    )
    
def error_data(datos_serializer):
    """Return a common JSON error result"""
    error_details = []
    for key in datos_serializer.errors.keys():
        error_details.append({"field": key, "message": datos_serializer.errors[key][0]})

    data = {
        "Error": {
            "success": False,
            "status": 400,
            "message": "Los datos enviados no son validos",
            "details": error_details
        }
    }
    return data
