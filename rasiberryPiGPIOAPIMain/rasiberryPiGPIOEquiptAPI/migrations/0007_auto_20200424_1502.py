# Generated by Django 3.0.4 on 2020-04-24 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rasiberryPiGPIOEquiptAPI', '0006_auto_20200424_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceinfo',
            name='i2cAddress',
            field=models.IntegerField(default=None),
        ),
    ]
