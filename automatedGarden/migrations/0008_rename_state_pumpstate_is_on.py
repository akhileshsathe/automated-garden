# Generated by Django 4.2.2 on 2023-06-28 03:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('automatedGarden', '0007_lightstate_pumpstate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pumpstate',
            old_name='state',
            new_name='is_on',
        ),
    ]
