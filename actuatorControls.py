import RPi.GPIO as GPIO
import time

light = 3

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(light, GPIO.OUT)

def lightOn():
    GPIO.output(light, True)

def lightOff():
    GPIO.output(light, False)
