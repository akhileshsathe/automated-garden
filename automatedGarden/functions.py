import RPi.GPIO as GPIO
import time
import Adafruit_DHT
# import board
# import neopixel
# import time
# pixels = neopixel.NeoPixel(board.D21, 21)

# def toggleLights(state):
#     if state:
#         for x in range(0, 20):pixels[x] = (255, 0, 0)
#     else: 
#         for x in range(0, 20):pixels[x] = (255, 0, 0)



# Set the GPIO pin numbers
def read_depth():
    trig_pin = 14
    echo_pin = 15
    percent=0
    # Set up GPIO mode and pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(trig_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)

    try:
            # Send a short pulse to the Trig pin
        GPIO.output(trig_pin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(trig_pin, GPIO.LOW)

            # Measure the duration of the Echo pin high pulse
        while GPIO.input(echo_pin) == 0:
            pulse_start = time.time()
        while GPIO.input(echo_pin) == 1:
            pulse_end = time.time()

            # Calculate the distance based on the pulse duration
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150  # Speed of sound in cm/s
        distance = round(distance, 2)
        # percent=int((distance/1203.0)*100)
            #print("Distance:", distance, "cm",percent,"%")
        return distance

    except KeyboardInterrupt:
        # Clean up GPIO settings
        GPIO.cleanup()
def dht():

# Set up the sensor type and GPIO pin
    sensor = Adafruit_DHT.DHT11
    pin = 4

    # Read the temperature and humidity from the sensor
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    return [humidity,temperature]