# Generated by Django 3.0.4 on 2020-04-19 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rasiberryPiGPIOEquiptAPI', '0002_devicedata_devicedatahistory_deviceinfo_devicepin_pideviceinfo_pidevicepin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pidevicepin',
            old_name='deviceID',
            new_name='piDeviceID',
        ),
    ]
