# Generated by Django 3.0.7 on 2020-06-21 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent_console', '0002_agentconsoleoptions_cedulallamada_serverlog_useragent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cedulallamada',
            options={'managed': False},
        ),
        migrations.RemoveField(
            model_name='useragent',
            name='fake',
        ),
    ]
