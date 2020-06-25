"""Manages the agent state logic """
import json
from datetime import datetime
import pytz
from agent_console.models import Audit, Agent, CurrentCallEntry, CedulaLlamada, ServerLog

class AgentState():
    """Class for agent state logic"""
    def __init__(self, verbosity=False):
        self.verbosity = verbosity

    @staticmethod
    def is_loged(id_agent):
        """ Checks if agent is loged to the call center module"""
        try:
            last_logon = Audit.objects.filter(
                id_agent=id_agent,
                id_break__isnull=True
            ).order_by('-datetime_init')[0]
            if last_logon.datetime_end == '' or last_logon.datetime_end is None:
                return True
            return False
        except IndexError:
            return False

    @staticmethod
    def agent_exist(id_agent):
        """Check if the agent still exist in the call_center db"""
        count = Agent.objects.filter(id=id_agent).count()
        if count == 1:
            return True
        return False

    @staticmethod
    def agent_current_call(id_agent):
        """Get the current call of the agent, None if there is no call"""
        try:
            query = CurrentCallEntry.objects.get(id_agent=id_agent)
            return query
        except CurrentCallEntry.DoesNotExist:
            return None

    @staticmethod
    def get_cedula(uniqueid):
        """Gets the document from the cedula_llamada table"""
        try:
            query = CedulaLlamada.objects.get(uniqueid=uniqueid)
            cedula = query.cedula
            return cedula
        except CedulaLlamada.DoesNotExist:
            return None

    def get_answer(self, state, id_agent, current_call=None):
        """Returns the server answer given a state"""
        answer = {}
        answer['previous'] = state
        if state == "1":
            answer['message'] = "El agente fue borrado del servidor de telefonía"
            answer['call'] = False
            answer['status'] = "No encontrado"

        elif state == "2":
            answer['message'] = "Por favor, inicie sesión en su telefono"
            answer['call'] = False
            answer['status'] = "No conectado"

        elif state == "3":
            answer['message'] = "Esperando llamada"
            answer['call'] = False
            answer['status'] = "Conectado"

        elif state == "4":
            agent = Agent.objects.get(id=id_agent)
            answer['message'] = "En llamada"
            answer['call'] = True
            answer['status'] = "Conectado"
            answer['phone'] = current_call.callerid
            answer['cedula'] = AgentState.get_cedula(current_call.uniqueid)
            answer['extension'] = agent.number
            answer['llamada_id'] = current_call.uniqueid

        if self.verbosity:
            timezone = pytz.timezone("America/Bogota")
            server_log = ServerLog(
                event=state,
                agent=id_agent,
                description=answer['message'],
                datetime=timezone.localize(datetime.now())
            )
            server_log.save()
            print("saved " + str(id_agent))
        answer['update'] = True
        return answer

    @staticmethod
    def check_state(id_agent):
        current_call=None
        if not AgentState.agent_exist(id_agent):
            state = "1"
        elif not AgentState.is_loged(id_agent):
            state = "2"
        else:
            current_call = AgentState.agent_current_call(id_agent)
            if current_call is None:
                state = "3"
            else:
                state = "4"

        return state, current_call

