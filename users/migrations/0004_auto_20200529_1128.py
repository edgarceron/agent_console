# Generated by Django 3.0.4 on 2020-05-29 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_loginsession'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=255, verbose_name='Constraseña'),
        ),
    ]
