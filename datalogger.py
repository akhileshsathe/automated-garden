from time import time,sleep
from datetime import  datetime
from zoneinfo import ZoneInfo
import os
import django
import serial
import Adafruit_DHT
import RPi.GPIO as GPIO
import board
import neopixel
import threading
india_timezone = ZoneInfo("Asia/Kolkata")
def thishour():
    return datetime.now(india_timezone).hour
print(f"Script Local Time: {thishour()}")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'automatedGarden.settings')
django.setup()
from django.db.models import Max
from automatedGarden.models import Plant,Tank,WateringMethod,HumidityData,TemperatureData,LightState
from automatedGarden.models import SoilMoistureData,PumpState,LightState
trig_pin = 14
echo_pin = 15
LDR_pin=17
relay_pin = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(LDR_pin, GPIO.IN)
GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)
GPIO.setup(relay_pin, GPIO.OUT)
workingArray=[0,0,0,1]
log=open("Logs.txt","a")
tankDepth = Tank.objects.first().value
water_requirements = {
    "herb": {
        'seedling': 50,
        'vegetative_growth': 100,
        'flowering': 120,
        'fruiting': 150,
        'dormant': 50,
    },
    "shrub": {
        'seedling': 100,
        'vegetative_growth': 150,
        'flowering': 180,
        'fruiting': 200,
        'dormant': 50,
    },
    "perennial": {
        'seedling': 80,
        'vegetative_growth': 120,
        'flowering': 150,
        'fruiting': 180,
        'dormant': 50,
    },
    "annual": {
        'seedling': 70,
        'vegetative_growth': 110,
        'flowering': 140,
        'fruiting': 160,
        'dormant': 50,
    },
    "succulent": {
        'seedling': 30,
        'vegetative_growth': 50,
        'flowering': 60,
        'fruiting': 70,
        'dormant': 20,
    },
    "cactus": {
        'seedling': 20,
        'vegetative_growth': 40,
        'flowering': 50,
        'fruiting': 60,
        'dormant': 10,
    },
    "water_plant": {
        'seedling': 150,
        'vegetative_growth': 200,
        'flowering': 250,
        'fruiting': 300,
        'dormant': 100,
    },
}

#0=soil
#1=dht
#2=relay
#3=ultrasonic

def getSoilMoistureSerial():
    try:
        port = serial.Serial('/dev/ttyUSB0', baudrate=9600)
        data = port.readline().decode().strip()
        workingArray[0]=1
        # print(data)
        return data
    except Exception as e:
        workingArray[0]=0
        print("Some problem with soil moisture sensor\nWriting to log file")
        log.write("_"*10)
        log.write(str(e))
        log.write("_"*10)
        return -1000


def dht():
    sensor = Adafruit_DHT.DHT11
    pin = 4
    try:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        workingArray[0]=1
        return [humidity,temperature]
    except Exception as e:
        workingArray[1]=0
        print("Some problem with DHT sensor\nWriting to log file")
        log.write("_"*10)
        log.write(str(e))
        log.write("_"*10)
        return [-1000,-1000]

def pumpOn():
    GPIO.output(relay_pin, GPIO.LOW)

def pumpOff():
    GPIO.output(relay_pin, GPIO.HIGH)

def pump():
    try:
        GPIO.output(relay_pin, GPIO.LOW)
        sleep(0.01)
        GPIO.output(relay_pin, GPIO.HIGH)
        workingArray[2]=1
        while True:
            if PumpState.objects.first().is_on:
                with lock:
                    GPIO.output(relay_pin, GPIO.LOW)
                    sleep(1)
                    GPIO.output(relay_pin, GPIO.HIGH)

    except Exception as e:
        workingArray[2]=0
        print("Some problem with Pump relay\nWriting to log file")
        log.write("_"*10)
        log.write(str(e))
        log.write("_"*10)
    finally:
        print("Finally turning off the pump!")
        GPIO.output(relay_pin, GPIO.HIGH)

def light():
    try:
        print("Lights starting")
        pixels = neopixel.NeoPixel(board.D21, 11)
        l=len(pixels)
        def startup():
            for i in range(l):
                pixels[i] = (255, 0, 0)
                sleep(0.01)
            sleep(0.01)

            for i in range(l):
                pixels[i] = (0, 255, 0)
                sleep(0.01)
            sleep(0.01)

            for i in range(l):
                pixels[i] = (0, 0, 255)
                sleep(0.01)
            sleep(0.01)
        count=0
        while not count==2:
            startup() 
            sleep(0.3)      
            count+=1
        for i in range(l-1,-1,-1):
            pixels[i] = (0, 0, 0)
            sleep(0.01)
        workingArray[3]=1
        while True:

            if LightState.objects.first().is_on:
                print("Lights on",flush=True)
                for i in range(l):
                    pixels[i] = (255, 255, 255)
                    sleep(0.01)
            else:
                # print("Lights off",flush=True)
                for i in range(l-1,-1,-1):
                    pixels[i] = (0, 0, 0)
                    sleep(0.01)
                
            sleep(1)
    except Exception as e:
        workingArray[3]=0
        print("Some problem with lights\nWriting to log file")
        log.write("_"*10)
        log.write(str(e))
        log.write("_"*10)
        for i in range(l):
            pixels[i] = (0, 0, 0)

        
    finally:
        print("Turning lights off finally",flush=True)
        for i in range(l):
            pixels[i] = (0, 0, 0)
        

def datalogger():

    while True:
        moisture_level = getSoilMoistureSerial()
        DHT=dht()
        # print("Moisture:",moisture_level)
        # print(moisture_level,DHT[0])
        if not moisture_level==-1000:
            mdata = SoilMoistureData(value=moisture_level)
        mdata.save()
        if not DHT[0]==-1000:
            tdata = TemperatureData(value=DHT[1])
            tdata.save()
            hdata = HumidityData(value=DHT[0])
            hdata.save()
        global SOIL_MOISTURE_LEVEL
        global HUMIDITY_LEVEL
        global TEMPERATURE_LEVEL

        SOIL_MOISTURE_LEVEL=moisture_level
        HUMIDITY_LEVEL=DHT[0]
        TEMPERATURE_LEVEL=DHT[1]
        sleep(10) 
def read_depth():
    trig_pin = 14
    echo_pin = 15
    # Set up GPIO mode and pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(trig_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)

    
            # Send a short pulse to the Trig pin
    GPIO.output(trig_pin, GPIO.HIGH)
    sleep(0.00001)
    GPIO.output(trig_pin, GPIO.LOW)
        # Measure the duration of the Echo pin high pulse
    while GPIO.input(echo_pin) == 0:
        pulse_start = time()
    while GPIO.input(echo_pin) == 1:
        pulse_end = time()
        # Calculate the distance based on the pulse duration
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound in cm/s
    distance = round(distance, 2)
    return distance
def autoGarden():

    print("Waitinng 1 min for sensor checks to finish")
    sleep(5)
    print("Starting AutoGarden")

    watered=False
    lwCount=0

    while True:
        start=time()
        
        if not PumpState.objects.first().is_on:
            sleep(1)
            
            percentage = int(read_depth() / tankDepth * 100)
            if percentage >= 101:percentage = 100
            remaining = 100 - percentage
            global wMethod

            if remaining<=20.0 :
                global wMethod
                wMethod="LOW Water"
                if lwCount<1:
                    print("\twater level:LOW!!. Notifying the user")
                lwCount+=1
            else:
                lwCount=0
                wMethod=WateringMethod.objects.latest('id').method
                print(wMethod)
                # print("Watering Method:",wMethod)
                plant=Plant.objects.first()
                # dbSoilMoisture=SoilMoistureData.objects[-1].value
                last_added_value = SoilMoistureData.objects.aggregate(Max('time')).get('time__max')
                dbSoilMoisture = SoilMoistureData.objects.filter(time=last_added_value).first().value
                # .latest("value").
                # print(dbSoilMoisture)
                if wMethod == "regular":
                    mPercent=(dbSoilMoisture/1024)*100

                    # print(dbSoilMoisture,mPercent)
                    if mPercent >= 60.0:
                        with lock:
                            pumpOn()
                            sleep(3)
                            pumpOff()         
                    else:
                        print("Pumpoff regular")
                if wMethod == "optimal":
                    if not watered and 0<= thishour() <= 6:
                        with lock:
                            try:

                                pumpOn()
                                waterDuration=water_requirements[plant.plant_type][plant.growth_phase]
                                print(f"Plant type:{plant.plant_type} Growth Phase:{plant.growth_phase}")
                                print("\toptimally watering  for \n\tduration:",waterDuration," "*20)
                                for i in range(waterDuration):
                                    print(f"Pump will be turned off in:{waterDuration-i}seconds",end="\r")
                                    sleep(1)
                                # sleep(waterDuration)
                                watered=True
                                pumpOff()
                            except Exception as e:
                                pumpOff()
                                GPIO.cleanup()


                    elif not watered:
                        print("time:",thishour(), "not between 2-6AM"+" "*20)
                        pumpOff()
                else:
                    print("unkown watering method")

        else:
                print("\n\t control bypassed by user!\n\t\tThe system will resume control once use"+" "*20)
                sleep(10)
        if time()-start>=12 * 60 * 60:watered=False
        global optimallyWatered
        optimallyWatered=False
        if watered and wMethod=="optimal":optimallyWatered=True
        print(f"Soil Moisture: {SOIL_MOISTURE_LEVEL} Humidity: {HUMIDITY_LEVEL}% Temperature: {TEMPERATURE_LEVEL}℃  wMethod:{wMethod} Optimally Watered:{optimallyWatered}"," "*10,end="\r")
        # print(f"END Local Time: {thishour()}",end="\r")

try:
    lock = threading.Lock()
    thread1 = threading.Thread(target=light)
    thread2 = threading.Thread(target=pump)
    thread3 = threading.Thread(target=datalogger)
    thread4 = threading.Thread(target=autoGarden)



    # Start the threads
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    # Wait for the threads to finish
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()

except KeyboardInterrupt:
    print("Exiting...")
    os._exit(1)
except Exception as e:
    pass
    # print(e)
    
finally:
    pumpOff()
    GPIO.cleanup()
    log.close()
    

