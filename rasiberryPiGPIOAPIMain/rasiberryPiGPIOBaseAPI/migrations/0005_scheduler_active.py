# Generated by Django 3.0.4 on 2020-04-24 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rasiberryPiGPIOBaseAPI', '0004_auto_20200424_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduler',
            name='active',
            field=models.IntegerField(default=1),
        ),
    ]