"""Manage a tcp server for the call on each agen as a new connection"""
import socket
import json
import time
import selectors
from datetime import datetime
import pytz
from _thread import start_new_thread
from agent_console.models import Audit, Agent, CurrentCallEntry, CedulaLlamada, ServerLog

class AgentConsoleSocketServer():
    server = None
    sel = selectors.DefaultSelector()
    agents = {}
    connections = []
    previous_states = {}
    previous_calls = {}

    def __init__(self, verbosity=0):
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
        except:
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
            return query
        except CedulaLlamada.DoesNotExist:
            return None

    def get_answer(self, state, id_agent, current_call=None):
        """Returns the server answer given a state"""
        answer = {}
        if state == "1":
            answer['message'] = "El agente fue borrado del servidor de telefonía"
            answer['call'] = False
            answer['status'] = "No encontrado"

        elif state == "2":
            answer['message'] = "El agente no esta conectado, inicie sesión en su telefono"
            answer['call'] = False
            answer['status'] = "No conectado"

        elif state == "3":
            answer['message'] = "Esperando llamada"
            answer['call'] = False
            answer['status'] = "Conectado"

        elif state == "4":
            answer['message'] = "En llamada"
            answer['call'] = True
            answer['status'] = "Conectado"
            answer['phone'] = current_call.callerid
            answer['cedula'] = AgentConsoleSocketServer.get_cedula(current_call.uniqueid)

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
        answer = json.dumps(answer)
        return bytes(answer, 'utf-8')

    @staticmethod
    def check_state(id_agent):
        call_id=""
        if not AgentConsoleSocketServer.agent_exist(id_agent):
            state = "1"
        elif not AgentConsoleSocketServer.is_loged(id_agent):
            state = "2"
        else:
            current_call = AgentConsoleSocketServer.agent_current_call(id_agent)
            if current_call is None:
                state = "3"
            else:
                state = "4"
                call_id = current_call.uniqueid

        return state, call_id


    def manage_incoming_data(self, recv_data):
        id_agent = ""
        if recv_data:
            recv_data = recv_data.decode("utf-8")
            print('received {!r}'.format(recv_data))
            agent_info = json.loads(recv_data)
            id_agent = agent_info['id']
            if recv_data == "close":
                print("closing connection")
                self.sel.unregister(self.server)
                self.server.close()
        return id_agent

    def service_connection(self, key, mask):
        sock = key.fileobj
        state = ""

        if mask & selectors.EVENT_READ:
            recv_data = sock.recv(1024)  # Should be ready to read
            if recv_data:
                print("Se lee un mensaje")
                self.agents[sock.getpeername()] = self.manage_incoming_data(recv_data)

        if mask & selectors.EVENT_WRITE:
            if sock.getpeername() in self.agents:
                id_agent = self.agents[sock.getpeername()]
                if not id_agent in self.previous_states:
                    self.previous_states[id_agent] = ""

                if not id_agent in self.previous_calls:
                    self.previous_calls[id_agent] = ""

                state, current_call = self.check_state(id_agent)

                if state == "4":
                    if current_call != self.previous_calls[id_agent]:
                        self.previous_calls[id_agent] = current_call
                        answer = self.get_answer(state, id_agent, current_call)
                        print("Sever: Sending ", repr(answer), "to connection")
                        sock.send(answer)
                elif self.previous_states[id_agent] != state:
                    self.previous_states[id_agent] = state
                    answer = self.get_answer(state, id_agent)
                    print("Sever: Sending ", repr(answer), "to connection")
                    sock.send(answer)

    def accept_wrapper(self, sock):
        try:
            conn, addr = sock.accept()  # Should be ready to read
            print("accepted connection from", addr)
            conn.setblocking(False)
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
            self.sel.register(conn, events, data=None)
            self.connections.append(conn)

        except OSError:
            print("El socket esta cerrado accep_wrapper")
    
    # Create a TCP/IP socket
    def start_server(self):
        """ Starts the socket server """
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = ('localhost', 16899)
        print('starting up on {} port {}'.format(*server_address))
        self.server.bind(server_address)

        # Listen for incoming connections
        self.server.listen()
        self.server.setblocking(False)

        self.sel.register(self.server, selectors.EVENT_READ, data=None)

        try:
            while True:
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    if not key.fileobj in self.connections:
                        self.accept_wrapper(key.fileobj)
                    else:
                        self.service_connection(key, mask)
                time.sleep(1)
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting")
        except OSError as e:
            print("Ocurrio un error de OS:")
            print(e)

        finally:
            self.sel.close()

    def stop_server(self):
        """ Stops the socket server """
        self.server.close()
        print("Se detuvo el servidor exitosamente")
