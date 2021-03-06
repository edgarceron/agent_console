# Generated by Django 3.0.4 on 2020-05-29 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile_active'),
        ('users', '0002_auto_20200411_1009'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=32, unique=True)),
                ('life', models.DateTimeField()),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='profiles.Profile')),
            ],
        ),
    ]
