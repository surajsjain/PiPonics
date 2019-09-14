import RPi.GPIO as GPIO
import time
from datetime import datetime
import requests

waterUrl = 'https://speeve-ponics.herokuapp.com/conditions/watering'

light = 2
motor = 3

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(motor, GPIO.OUT)
GPIO.setup(light, GPIO.OUT)


def motorOn():
    GPIO.output(motor, True)

    data = {
        "timestamp": datetime.now(),
        "plant": 1,
        "pond": 1,
        "motor": True
    }

    r = requests.post(waterUrl, data)

def motorOff(condition = ''):
    if condition is "initial":
        GPIO.output(motor, False)
    else:
        GPIO.output(motor, False)

        data = {
            "timestamp": datetime.now(),
            "plant": 1,
            "pond": 1,
            "motor": False
        }

        r = requests.post(waterUrl, data)

def lightOn():
    GPIO.output(light, True)

def lightOff():
    GPIO.output(light, False)
