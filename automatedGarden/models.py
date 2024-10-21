from django.db import models

class Plant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    type_choices = [
        ('','Select the type of plant'),
        ('herb', 'Herb'),
        ('shrub', 'Shrub'),
        ('perennial', 'Perennial'),
        ('annual', 'Annual'),
        ('succulent', 'Succulent'),
        ('cactus', 'Cactus'),
        ('water_plant', 'Water Plant'),
    ]
    plant_type = models.CharField(max_length=20, choices=type_choices,default='option1')
    growth_phase_choices = [
        ('','Select the growth phase the plant is currently in'),
        ('seedling', 'Seedling'),
        ('vegetative_growth', 'Vegetative Growth'),
        ('flowering', 'Flowering'),
        ('fruiting', 'Fruiting'),
        ('dormant', 'Dormant'),
    ]
    growth_phase = models.CharField(max_length=20, choices=growth_phase_choices,default='option1')
    water_requirement_choices = [
        ('','Select the level of water requirement'),
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    water_requirement = models.CharField(max_length=10, choices=water_requirement_choices)
    placement_choices = [
        ('','Select where the plant is placed'),
        ('indoors', 'Indoors'),
        ('outdoors', 'Outdoors'),
    ]
    placement = models.CharField(max_length=20, choices=placement_choices)

    def __str__(self):
        return self.name


class Tank(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.FloatField(default=0)

    def __str__(self):
        return f'Tank {self.id}'

class WateringMethod(models.Model):
    id = models.AutoField(primary_key=True)
    method = models.CharField(max_length=100)

    def __str__(self):
        return f'Watering Method {self.id}'


class SoilMoistureData(models.Model):
    value = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Soil Moisture Data: {self.value} at {self.time}"
class HumidityData(models.Model):
    value = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Humidity Data: {self.value} at {self.time}"
class TemperatureData(models.Model):
    value = models.FloatField()
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Temperature Data: {self.value} at {self.time}"
from django.db import models

class PumpState(models.Model):
    is_on = models.BooleanField(default=False)

    def __str__(self):
        return f"Pump State: {'On' if self.is_on else 'Off'}"

class LightState(models.Model):
    is_on = models.BooleanField(default=False)

    def __str__(self):
        return f"Light State: {'On' if self.is_on else 'Off'}"


