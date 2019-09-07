import RPi.GPIO as GPIO
import time

waterSensor = 4
soil = 21

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(waterSensor, GPIO.OUT)
GPIO.setup(soil, GPIO.OUT)

GPIO.output(waterSensor, GPIO.LOW)
GPIO.output(soil, GPIO.LOW)

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

    if(condition == 1):
        return True

    else:
        return False
