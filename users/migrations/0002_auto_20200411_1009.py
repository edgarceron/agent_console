# Generated by Django 3.0.4 on 2020-04-11 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='needPassword',
            new_name='need_password',
        ),
    ]
