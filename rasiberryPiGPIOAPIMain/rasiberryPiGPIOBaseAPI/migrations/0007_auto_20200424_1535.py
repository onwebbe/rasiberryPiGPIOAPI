# Generated by Django 3.0.4 on 2020-04-24 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rasiberryPiGPIOBaseAPI', '0006_scheduler_pideviceid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scheduler',
            name='piDeviceId',
        ),
        migrations.AddField(
            model_name='scheduler',
            name='piDeviceID',
            field=models.IntegerField(default=-1),
        ),
    ]
