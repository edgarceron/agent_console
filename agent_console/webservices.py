""" Webservices for the agent_console app """
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from users.permission_validation import PermissionValidation
from .console_functions.agent_state import AgentState
from .console_functions.generate_users import GenerateUsers
from .serializers import UserAgentSerializer, AgentSerializer
from .models import UserAgent, Agent, AgentConsoleOptions


def get_actions():
    "Returns the list of actions to be registered for permissions module."
    actions = [
        {"name": "set_user_agent", "label": "Webservice enlazar usuario con agente de call center"},
        {"name": "picker_search_agent", "label": "Webservice para actualizar el picker de agentes"},
        {"name": "get_agent", "label": "Webservice para obteber los datos del agente"},
        {"name": "agent_state", "label": "Webservice para obteber el estado del agente"},
        {"name": "get_crm_url", "label": "Webservice para obteber la url de redirección al CRM"},
        {
            "name": "replace_options_agent_console",
            "label": "Webservice para guardar las opciones de la consola de agente"},
        {
            "name": "get_options_agent_console",
            "label": "Webservice para obtener las opciones de la consola de agente"},
        {
            "name": "auto_generate_users",
            "label": "Webservice para generar los usuario automaticamente"}
    ]
    return actions

@api_view(['POST'])
def set_user_agent(request):
    """Tries to create an user and returns the result"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('set_user_agent')
    if validation['status']:
        data = request.data
        user_id = data['user']
        agent_id = data['agent']

        try:
            query = UserAgent.objects.filter(user=user_id)
            if len(query) > 0:
                for obj in query:
                    model = obj
                    if agent_id == "":
                        model.delete()
                        return Response(
                            {"success":True, "message":"UserAgent deleted"},
                            status=status.HTTP_200_OK,
                            content_type='application/json')

                    serializer = UserAgentSerializer(instance=model, data=data)

            else:
                serializer = UserAgentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"success":True},
                    status=status.HTTP_201_CREATED,
                    content_type='application/json')
            data = error_data(serializer)
            return Response(
                data,
                status=status.HTTP_400_BAD_REQUEST,
                content_type='application/json')

        except Agent.DoesNotExist:
            data = {
                'success': False,
                'message': 'El agente se borro del servidor de telefonía, intente con otro agente'
            }
            return Response(data, status=status.HTTP_200_OK, content_type='application/json')

    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['POST'])
def picker_search_agent(request):
    "Returns a JSON response with user data for a selectpicker."
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('picker_search_agent')
    if validation['status']:
        value = request.data['value']
        queryset = Agent.agent_picker_filter(value)
        serializer = AgentSerializer(queryset, many=True)
        result = serializer.data

        data = {
            "success": True,
            "result": result
        }
        return Response(data, status=status.HTTP_200_OK, content_type='application/json')
    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['POST'])
def get_agent(request, user_id):
    "Return a JSON response with agent data for the given id"
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('get_agent')
    if validation['status']:
        try:
            user_agent_obj = UserAgent.objects.get(user=user_id)
            agent_id = user_agent_obj.agent
            agent_obj = Agent.objects.get(id=agent_id)
            agent_serializer = AgentSerializer(agent_obj)
            agent_data = agent_serializer.data.copy()

            data = {
                "success":True,
                "data":agent_data
            }
        except:
            data = {
                "success":False
            }
    
        return Response(
            data,
            status=status.HTTP_200_OK,
            content_type='application/json'
        )
    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['POST'])
def agent_state(request):
    """Gets the agent state"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('agent_state')
    if validation['status']:
        agent_state_obj = AgentState(False)
        data = request.data
        previous_state = data['previous_state']
        id_agent = data['id_agent']
        previous_call = data['previous_call']

        state, current_call = agent_state_obj.check_state(id_agent)
        if (state == 4 and current_call.uniqueid != previous_call) or state != previous_state:
            answer = agent_state_obj.get_answer(state, id_agent, current_call)
        else:
            answer = {'update': False}

        return Response(answer, status=status.HTTP_200_OK, content_type='application/json')

    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['POST'])
def get_crm_url(request):
    """Gets the agent state"""
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('get_crm_url')
    if validation['status']:
        try:
            option = AgentConsoleOptions.objects.get(option='CRM_URL')
            data = {
                'success': True,
                'url': option.value
            }
        except AgentConsoleOptions.DoesNotExist:
            data = {
                'success': False,
                'url': "No se ha especificado un valor para la url de redirección"
            }

        return Response(data, status=status.HTTP_200_OK, content_type='application/json')

    return PermissionValidation.error_response_webservice(validation, request)


@api_view(['PUT'])
def replace_options_agent_console(request):
    "Tries to update the agent console options"
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('replace_options_agent_console')
    if validation['status']:
        data = request.data.copy()
        url = data['CRM_URL']
        redirection_time = data['REDIRECT_TIME']
        try:
            option_url = AgentConsoleOptions.objects.get(option='CRM_URL')
        except AgentConsoleOptions.DoesNotExist:
            option_url = AgentConsoleOptions()
            option_url.option = 'CRM_URL'

        try:
            option_redirection = AgentConsoleOptions.objects.get(option='REDIRECT_TIME')
        except AgentConsoleOptions.DoesNotExist:
            option_redirection = AgentConsoleOptions()
            option_redirection.option = 'REDIRECT_TIME'

        option_url.value = url
        option_redirection.value = redirection_time

        option_url.save()
        option_redirection.save()

        return Response(
            {"success":True},
            status=status.HTTP_200_OK,
            content_type='application/json'
        )
    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['POST'])
def get_options_agent_console(request):
    "Return a JSON response with user data for the given id"
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('get_options_agent_console')
    if validation['status']:
        try:
            option_url = AgentConsoleOptions.objects.get(option='CRM_URL')
        except AgentConsoleOptions.DoesNotExist:
            option_url = AgentConsoleOptions()
            option_url.option = 'CRM_URL'

        try:
            option_redirection = AgentConsoleOptions.objects.get(option='REDIRECT_TIME')
        except AgentConsoleOptions.DoesNotExist:
            option_redirection = AgentConsoleOptions()
            option_redirection.option = 'REDIRECT_TIME'

        options = {
            option_url.option: option_url.value,
            option_redirection.option: option_redirection.value
        }

        data = {
            "success":True,
            "data":options
        }

        return Response(
            data,
            status=status.HTTP_200_OK,
            content_type='application/json'
        )
    return PermissionValidation.error_response_webservice(validation, request)

@api_view(['POST'])
def auto_generate_users(request):
    "Return a JSON response with user data for the given id"
    permission_obj = PermissionValidation(request)
    validation = permission_obj.validate('auto_generate_users')
    if validation['status']:
        try:
            GenerateUsers.bulk_create_users()
            return Response(
                {'success':True, 'message':'Usuarios Generados con exito'},
                status=status.HTTP_200_OK,
                content_type='application/json'
            )
        except:
            return Response(
                {'success':False, 'message':'Ocurrio un error al intentar generar los usuarios'},
                status=status.HTTP_200_OK,
                content_type='application/json'
            )

    return PermissionValidation.error_response_webservice(validation, request)

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
