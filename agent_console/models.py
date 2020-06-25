from django.db import models
from django.db.models import Q
from users.models import User


#CALL CENTER
class Agent(models.Model):
    type = models.CharField(max_length=5)
    number = models.CharField(max_length=40)
    name = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    estatus = models.CharField(max_length=1, blank=True, null=True)
    eccp_password = models.CharField(max_length=128, blank=True, null=True)

    @staticmethod
    def agent_picker_filter(value):
        return list(Agent.objects.filter(
            Q(name__contains=value)
        )[:10])

    class Meta:
        managed = False
        db_table = 'agent'

class Audit(models.Model):
    id_agent = models.ForeignKey(Agent, models.DO_NOTHING, db_column='id_agent')
    id_break = models.ForeignKey('Break', models.DO_NOTHING, db_column='id_break', blank=True, null=True)
    datetime_init = models.DateTimeField()
    datetime_end = models.DateTimeField(blank=True, null=True)
    duration = models.TimeField(blank=True, null=True)
    ext_parked = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audit'

class Break(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=1)
    tipo = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'break'

class CallAttribute(models.Model):
    id_call = models.ForeignKey('Calls', models.DO_NOTHING, db_column='id_call')
    columna = models.CharField(max_length=30, blank=True, null=True)
    value = models.CharField(max_length=128)
    column_number = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'call_attribute'

class CallEntry(models.Model):
    id_agent = models.ForeignKey(Agent, models.DO_NOTHING, db_column='id_agent', blank=True, null=True)
    id_queue_call_entry = models.ForeignKey('QueueCallEntry', models.DO_NOTHING, db_column='id_queue_call_entry')
    id_contact = models.ForeignKey('Contact', models.DO_NOTHING, db_column='id_contact', blank=True, null=True)
    callerid = models.CharField(max_length=15)
    datetime_init = models.DateTimeField(blank=True, null=True)
    datetime_end = models.DateTimeField(blank=True, null=True)
    duration = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(max_length=32, blank=True, null=True)
    transfer = models.CharField(max_length=6, blank=True, null=True)
    datetime_entry_queue = models.DateTimeField(blank=True, null=True)
    duration_wait = models.IntegerField(blank=True, null=True)
    uniqueid = models.CharField(max_length=32, blank=True, null=True)
    id_campaign = models.ForeignKey('CampaignEntry', models.DO_NOTHING, db_column='id_campaign', blank=True, null=True)
    trunk = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'call_entry'

class CallProgressLog(models.Model):
    datetime_entry = models.DateTimeField()
    id_campaign_incoming = models.ForeignKey('CampaignEntry', models.DO_NOTHING, db_column='id_campaign_incoming', blank=True, null=True)
    id_call_incoming = models.ForeignKey(CallEntry, models.DO_NOTHING, db_column='id_call_incoming', blank=True, null=True)
    id_campaign_outgoing = models.ForeignKey('Campaign', models.DO_NOTHING, db_column='id_campaign_outgoing', blank=True, null=True)
    id_call_outgoing = models.ForeignKey('Calls', models.DO_NOTHING, db_column='id_call_outgoing', blank=True, null=True)
    new_status = models.CharField(max_length=32)
    retry = models.PositiveIntegerField(blank=True, null=True)
    uniqueid = models.CharField(max_length=32, blank=True, null=True)
    trunk = models.CharField(max_length=20, blank=True, null=True)
    id_agent = models.ForeignKey(Agent, models.DO_NOTHING, db_column='id_agent', blank=True, null=True)
    duration = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'call_progress_log'

class CallRecording(models.Model):
    datetime_entry = models.DateTimeField()
    id_call_incoming = models.ForeignKey(CallEntry, models.DO_NOTHING, db_column='id_call_incoming', blank=True, null=True)
    id_call_outgoing = models.ForeignKey('Calls', models.DO_NOTHING, db_column='id_call_outgoing', blank=True, null=True)
    uniqueid = models.CharField(max_length=32)
    channel = models.CharField(max_length=80)
    recordingfile = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'call_recording'

class Calls(models.Model):
    id_campaign = models.ForeignKey('Campaign', models.DO_NOTHING, db_column='id_campaign')
    phone = models.CharField(max_length=32)
    status = models.CharField(max_length=32, blank=True, null=True)
    uniqueid = models.CharField(max_length=32, blank=True, null=True)
    fecha_llamada = models.DateTimeField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    retries = models.PositiveIntegerField()
    duration = models.PositiveIntegerField(blank=True, null=True)
    id_agent = models.ForeignKey(Agent, models.DO_NOTHING, db_column='id_agent', blank=True, null=True)
    transfer = models.CharField(max_length=6, blank=True, null=True)
    datetime_entry_queue = models.DateTimeField(blank=True, null=True)
    duration_wait = models.IntegerField(blank=True, null=True)
    dnc = models.IntegerField()
    date_init = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    time_init = models.TimeField(blank=True, null=True)
    time_end = models.TimeField(blank=True, null=True)
    agent = models.CharField(max_length=32, blank=True, null=True)
    failure_cause = models.PositiveIntegerField(blank=True, null=True)
    failure_cause_txt = models.CharField(max_length=32, blank=True, null=True)
    datetime_originate = models.DateTimeField(blank=True, null=True)
    trunk = models.CharField(max_length=20, blank=True, null=True)
    scheduled = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'calls'

class Campaign(models.Model):
    name = models.CharField(max_length=64)
    datetime_init = models.DateField()
    datetime_end = models.DateField()
    daytime_init = models.TimeField()
    daytime_end = models.TimeField()
    retries = models.PositiveIntegerField()
    trunk = models.CharField(max_length=255, blank=True, null=True)
    context = models.CharField(max_length=32)
    queue = models.CharField(max_length=16)
    max_canales = models.PositiveIntegerField()
    num_completadas = models.PositiveIntegerField(blank=True, null=True)
    promedio = models.PositiveIntegerField(blank=True, null=True)
    desviacion = models.PositiveIntegerField(blank=True, null=True)
    script = models.TextField()
    estatus = models.CharField(max_length=1)
    id_url = models.ForeignKey('CampaignExternalUrl', models.DO_NOTHING, db_column='id_url', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'campaign'

class CampaignEntry(models.Model):
    name = models.CharField(max_length=64)
    id_queue_call_entry = models.ForeignKey('QueueCallEntry', models.DO_NOTHING, db_column='id_queue_call_entry')
    id_form = models.ForeignKey('Form', models.DO_NOTHING, db_column='id_form', blank=True, null=True)
    datetime_init = models.DateField()
    datetime_end = models.DateField()
    daytime_init = models.TimeField()
    daytime_end = models.TimeField()
    estatus = models.CharField(max_length=1)
    script = models.TextField()
    id_url = models.ForeignKey('CampaignExternalUrl', models.DO_NOTHING, db_column='id_url', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'campaign_entry'

class CampaignExternalUrl(models.Model):
    urltemplate = models.CharField(max_length=250)
    description = models.CharField(max_length=64)
    active = models.IntegerField()
    opentype = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = 'campaign_external_url'

class CampaignForm(models.Model):
    id_campaign = models.OneToOneField(Campaign, models.DO_NOTHING, db_column='id_campaign', primary_key=True)
    id_form = models.ForeignKey('Form', models.DO_NOTHING, db_column='id_form')

    class Meta:
        managed = False
        db_table = 'campaign_form'
        unique_together = (('id_campaign', 'id_form'),)

class CampaignFormEntry(models.Model):
    id_campaign = models.OneToOneField(CampaignEntry, models.DO_NOTHING, db_column='id_campaign', primary_key=True)
    id_form = models.ForeignKey('Form', models.DO_NOTHING, db_column='id_form')

    class Meta:
        managed = False
        db_table = 'campaign_form_entry'
        unique_together = (('id_campaign', 'id_form'),)

class Contact(models.Model):
    cedula_ruc = models.CharField(max_length=15)
    name = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)
    apellido = models.CharField(max_length=50)
    origen = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact'

class CurrentCallEntry(models.Model):
    id_agent = models.ForeignKey(Agent, models.DO_NOTHING, db_column='id_agent')
    id_queue_call_entry = models.ForeignKey('QueueCallEntry', models.DO_NOTHING, db_column='id_queue_call_entry')
    id_call_entry = models.ForeignKey(CallEntry, models.DO_NOTHING, db_column='id_call_entry')
    callerid = models.CharField(max_length=15)
    datetime_init = models.DateTimeField()
    uniqueid = models.CharField(max_length=32, blank=True, null=True)
    channelclient = models.CharField(db_column='ChannelClient', max_length=32, blank=True, null=True)  # Field name made lowercase.
    hold = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'current_call_entry'

class CurrentCalls(models.Model):
    id_call = models.ForeignKey(Calls, models.DO_NOTHING, db_column='id_call')
    fecha_inicio = models.DateTimeField()
    uniqueid = models.CharField(max_length=32, blank=True, null=True)
    queue = models.CharField(max_length=16)
    agentnum = models.CharField(max_length=16)
    event = models.CharField(max_length=32)
    channel = models.CharField(db_column='Channel', max_length=32)  # Field name made lowercase.
    channelclient = models.CharField(db_column='ChannelClient', max_length=32, blank=True, null=True)  # Field name made lowercase.
    hold = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'current_calls'

class DontCall(models.Model):
    caller_id = models.CharField(max_length=15)
    date_income = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dont_call'

class EccpAuthorizedClients(models.Model):
    username = models.CharField(max_length=64)
    md5_password = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'eccp_authorized_clients'

class Form(models.Model):
    nombre = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=150)
    estatus = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'form'

class FormDataRecolected(models.Model):
    id_calls = models.ForeignKey(Calls, models.DO_NOTHING, db_column='id_calls')
    id_form_field = models.ForeignKey('FormField', models.DO_NOTHING, db_column='id_form_field')
    value = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'form_data_recolected'

class FormDataRecolectedEntry(models.Model):
    id_call_entry = models.ForeignKey(CallEntry, models.DO_NOTHING, db_column='id_call_entry')
    id_form_field = models.ForeignKey('FormField', models.DO_NOTHING, db_column='id_form_field')
    value = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'form_data_recolected_entry'

class FormField(models.Model):
    id_form = models.ForeignKey(Form, models.DO_NOTHING, db_column='id_form')
    etiqueta = models.TextField()
    value = models.TextField()
    tipo = models.CharField(max_length=25)
    orden = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'form_field'

class QueueCallEntry(models.Model):
    queue = models.CharField(max_length=50, blank=True, null=True)
    date_init = models.DateField(blank=True, null=True)
    time_init = models.TimeField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    time_end = models.TimeField(blank=True, null=True)
    estatus = models.CharField(max_length=1)
    script = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'queue_call_entry'

class ValorConfig(models.Model):
    config_key = models.CharField(primary_key=True, max_length=32)
    config_value = models.CharField(max_length=128)
    config_blob = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'valor_config'

class CedulaLlamada(models.Model):
    uniqueid = models.CharField(max_length=32, blank=True, null=True)
    cedula = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cedula_llamada'

class UserAgent(models.Model):
    """Each user is related to one agent"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    agent = models.IntegerField(unique=True)

class ServerLog(models.Model):
    """Saves the events in the server log, test or debug only"""
    event = models.CharField(max_length=1)
    agent = models.CharField(max_length=10)
    description = models.CharField(max_length=200)
    datetime = models.DateTimeField()

class AgentConsoleOptions(models.Model):
    """Stores the values of the options for the agent console"""
    option = models.CharField(max_length=40)
    value = models.CharField(max_length=255, unique=True)
    help_text = models.CharField(max_length=255, null=True, blank=True)
