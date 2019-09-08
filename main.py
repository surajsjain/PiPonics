import RPi.GPIO as GPIO
import time
import requests

from sensorReadings import *
from actuatorControls import *

# print(str(getWaterLevel()))
# print(str(getSoilMoisture()))
# print(str(getTemp()))
# print(str(getHum()))
#
# lightOn()
# motorOn()
# time.sleep(10)
# lightOff()
# motorOff()

## With Networking

motorOff('initial')
lightOff()

motor = False
light = False

def checkActuateConditions():
    url = 'https://speeve-ponics.herokuapp.com/conditions/actuate/1'
    r = requests.get(url)
    data = r.json()

    if((data['water'] == False) and (motor == True)):
        motorOff()
        motor = False

    if((data['water'] == True) and (motor == False)):
        motorOn()
        motor = True

    if((data['light'] == False) and (light == True)):
        lightOff()
        light = False

    if((data['light'] == True) and (light == False)):
        lightOn()
        light = True

def updateInFocus():
    pass

def updateData(): ## Onli on thr 15th min
    pass

def actoControls():
    pass



## Call all the functions in order in a while loop
