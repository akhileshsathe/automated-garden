"""
URL configuration for automatedGarden project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
#from .views import create_plant,tank_depth,watering_method,index,dashboard,soilgraph,waterlevel,humiditygraph,temperaturegraph,switch_lights_view
from .views import *
app_name = 'plants'
urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('create/', create_plant, name='create'),
     path('tankDepth/', tank_depth, name='depth'),
     path('wateringMethod/', watering_method, name='method'),
     path('dashboard/', dashboard, name='dashboard'),
     path('soilgraph/', soilgraph, name='soilgraph'),
     path('waterlevel/', waterlevel, name='waterlevel'),
     path('waterlevel2/', waterlevel2, name='waterlevel2'),

     path('humiditygraph/', humiditygraph, name='humiditygraph'),
     path('temperaturegraph/', temperaturegraph, name='temperaturegraph'),
     path('switchPump/', switch_pump, name='switch_pump'),
     path('switchLight/', switch_light, name='switch_light'),

     path('settings/', settings, name='settings'),


     




]



