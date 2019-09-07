import RPi.GPIO as GPIO
import time

light = 2
motor = 3

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(motor, GPIO.OUT)
GPIO.setup(light, GPIO.OUT)


def motorOn():
    GPIO.output(motor, True)

def motorOff():
    GPIO.output(motor, False)

def lightOn():
    GPIO.output(light, True)

def lightOff():
    GPIO.output(light, False)
