import RPi.GPIO as GPIO
import time
import Adafruit_DHT

waterSensor = 4
soil = 27
dht = 17
sensor=Adafruit_DHT.DHT11


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(waterSensor, GPIO.OUT)
# GPIO.setup(soil, GPIO.OUT)

GPIO.output(waterSensor, GPIO.LOW)
# GPIO.output(soil, GPIO.LOW)

time.sleep(0.05)

GPIO.setup(waterSensor, GPIO.IN)
GPIO.setup(soil, GPIO.IN)


def getWaterLevel():
    condition = GPIO.input(waterSensor)

    if(condition == 1):
        return True

    else:
        return False

def getSoilMoisture():
    condition = GPIO.input(soil)

    if(condition == 0):
        return True

    else:
        return False

def getTemp():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, dht)
    return temperature

def getHum():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, dht)
    return humidity
