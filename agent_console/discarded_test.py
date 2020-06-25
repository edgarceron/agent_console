from datetime import datetime
import time
import pytz
from django.test import SimpleTestCase
from django.db import connections
from _thread import start_new_thread
from agent_console.socket_call_entry.socket_server import AgentConsoleSocketServer
from agent_console.socket_call_entry.socket_client import AgentConsoleSocketClient
from agent_console.models import *
# Create your tests here.
class AgentConsoleServerTest(SimpleTestCase):
    databases = {'default', 'call_center'}

    def setUp(self):
        super().setUp()
        conn = connections['call_center']
        with conn.schema_editor() as schema_editor:
            schema_editor.create_model(Agent)
            schema_editor.create_model(Break)
            schema_editor.create_model(Contact)
            schema_editor.create_model(Form)
            schema_editor.create_model(CampaignExternalUrl)
            schema_editor.create_model(CampaignEntry)
            schema_editor.create_model(Audit)
            schema_editor.create_model(QueueCallEntry)
            schema_editor.create_model(CallEntry)
            schema_editor.create_model(CurrentCallEntry)

            if Agent._meta.db_table not in conn.introspection.table_names():
                raise ValueError(
                    "Table `{table_name}` is missing in test database.".format(
                        table_name=Agent._meta.db_table))

    def tearDown(self):
        super().tearDown()
        conn = connections['call_center']
        with conn.schema_editor() as schema_editor:
            schema_editor.delete_model(CurrentCallEntry)
            schema_editor.delete_model(CallEntry)
            schema_editor.delete_model(CampaignEntry)
            schema_editor.delete_model(Audit)
            #Do not have foreing key
            schema_editor.delete_model(QueueCallEntry)
            schema_editor.delete_model(Agent)
            schema_editor.delete_model(Break)
            schema_editor.delete_model(Contact)
            schema_editor.delete_model(Form)
            schema_editor.delete_model(CampaignExternalUrl)

    def test_agent_exist(self):
        """Testing agent_exist method"""
        agent = Agent(
            type='Agent',
            number='110',
            name='Mauro',
            password='Mauro',
            estatus='A',
            eccp_password='aaaa'
        )

        agent.save()

        result = AgentConsoleSocketServer.agent_exist(agent.id)

        self.assertEqual(result, True)

    def test_is_loged(self):
        """Testing is_loged method"""
        agent = Agent(
            type='Agent',
            number='110',
            name='Mauro',
            password='Mauro',
            estatus='A',
            eccp_password='aaaa'
        )
        agent.save()

        timezone = pytz.timezone("America/Bogota")
        date_aware = timezone.localize(datetime.now())

        audit_log = Audit(
            id_agent=agent,
            datetime_init=date_aware
        )

        audit_log.save()

        result = AgentConsoleSocketServer.is_loged(agent.id)
        self.assertEqual(result, True)

        date_aware = timezone.localize(datetime.now())
        audit_log.datetime_end = date_aware
        audit_log.save()

        result = AgentConsoleSocketServer.is_loged(agent.id)
        self.assertEqual(result, False)

        date_aware = timezone.localize(datetime.now())
        audit_log2 = Audit(
            id_agent=agent,
            datetime_init=date_aware
        )

        audit_log2.save()
        result = AgentConsoleSocketServer.is_loged(agent.id)
        self.assertEqual(result, True)

    def test_agent_current_call(self):
        """ Testing agent_current_call method"""
        agent = Agent(
            type='Agent',
            number='110',
            name='Mauro',
            password='Mauro',
            estatus='A',
            eccp_password='aaaa'
        )
        agent.save()

        timezone = pytz.timezone("America/Bogota")
        date_aware = timezone.localize(datetime.now())

        queue = QueueCallEntry(
            queue="101",
            estatus="A"
        )
        queue.save()

        call = CallEntry(
            id_agent=agent,
            id_queue_call_entry=queue,
            callerid="3176483290",
            uniqueid="salsa"
        )
        call.save()

        current = CurrentCallEntry(
            id_agent=agent,
            id_queue_call_entry=queue,
            id_call_entry=call,
            callerid="3176483290",
            datetime_init=date_aware,
            uniqueid="salsa"
        )
        current.save()

        result = AgentConsoleSocketServer.agent_current_call(agent.id)
        self.assertEqual(result, current)

    def test_server(self):

        agent = Agent(
            type='Agent',
            number='110',
            name='Mauro',
            password='Mauro',
            estatus='A',
            eccp_password='aaaa'
        )
        agent.save()

        server = AgentConsoleSocketServer(True)
        client_a = AgentConsoleSocketClient(True)
        client_b = AgentConsoleSocketClient(True)

        start_new_thread(server.start_server, ())
        print("Waiting 5 seconds")
        time.sleep(2)

        start_new_thread(client_a.start_client, ())
        time.sleep(1)
        client_a.set_message({'id':'103'})
        time.sleep(1)
        start_new_thread(client_b.start_client, ())
        time.sleep(1)
        client_b.set_message({'id':agent.id})
        time.sleep(1)

        timezone = pytz.timezone("America/Bogota")
        date_aware = timezone.localize(datetime.now())
        audit_log = Audit(
            id_agent=agent,
            datetime_init=date_aware
        )
        audit_log.save()

        time.sleep(3)

        print("Stoping server")
        server.stop_server()

        events = ServerLog.objects.filter(agent=agent.id)
        self.assertEqual(len(events), 3)



