from datetime import datetime
import time
import pytz
from django.test import SimpleTestCase
from django.db import connections
from _thread import start_new_thread
from agent_console.console_functions.generate_users import GenerateUsers
from agent_console.models import *

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

    def test_auto_generate_users(self):
        agent = Agent(
            type='Agent',
            number='110',
            name='Mauro',
            password='Mauro',
            estatus='A',
            eccp_password='aaaa'
        )
        agent.save()

        agent = Agent(
            type='Agent',
            number='111',
            name='Karlos',
            password='Mauro',
            estatus='A',
            eccp_password='aaaa'
        )
        agent.save()

        GenerateUsers.bulk_create_users()

        count = User.objects.count()
        self.assertEqual(count, 2)

        user_agent = UserAgent.objects.get(agent=agent.id)
        user = user_agent.user
        expected = agent.number + "@call.center"
        self.assertEqual(user.username, expected)
