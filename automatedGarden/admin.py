
from django.contrib import admin
from .models import Plant,Tank,WateringMethod,SoilMoistureData,TemperatureData,HumidityData,PumpState,LightState

class PlantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'plant_type', 'growth_phase', 'water_requirement', 'placement')
admin.site.register(Plant)      
class TankAdmin(admin.ModelAdmin):
    list_display = ('id', 'value')
admin.site.register(Tank)
class WateringMethodAdmin(admin.ModelAdmin):
    list_display = ('id', 'method')
admin.site.register(WateringMethod)
class SoilMoistureDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'value')
admin.site.register(SoilMoistureData)
class TemperatureDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'value')
admin.site.register(TemperatureData)
class HumidityDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'value')
admin.site.register(HumidityData)
class PumpStateAdmin(admin.ModelAdmin):
    list_display = ('is_on')
admin.site.register(PumpState)
class LightStateAdmin(admin.ModelAdmin):
    list_display = ('is_on')
admin.site.register(LightState)