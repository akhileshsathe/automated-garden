# Generated by Django 4.2.2 on 2023-06-23 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automatedGarden', '0006_humiditydata_temperaturedata'),
    ]

    operations = [
        migrations.CreateModel(
            name='LightState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PumpState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField(default=False)),
            ],
        ),
    ]