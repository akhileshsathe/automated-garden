# Generated by Django 4.2.2 on 2023-06-20 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automatedGarden', '0003_tank_alter_plant_growth_phase_alter_plant_placement_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WateringMethod',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('method', models.CharField(default='regular', max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='tank',
            name='value',
            field=models.FloatField(default=0),
        ),
    ]
