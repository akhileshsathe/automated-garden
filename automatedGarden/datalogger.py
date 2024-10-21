import time
import os
import django
import serial
def getSoilMoistureSerial():
    port = serial.Serial('/dev/ttyUSB0', baudrate=9600)
    data = port.readline().decode().strip()
    print(data)
    return data
# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'automatedGarden.settings')
django.setup()
from automatedGarden.models import SoilMoistureData
# Continuously read sensor data and write to Django SQLite database
while True:
    # Simulate reading sensor data
    moisture_level = getSoilMoistureSerial() # Replace with actual sensor reading code
    # Create a new instance of the SoilMoistureData model
    data = SoilMoistureData(value=moisture_level)
    data.save()
    # Wait for some time before the next reading
    time.sleep(10) 