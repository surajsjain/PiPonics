import RPi.GPIO as GPIO
import time
import requests
from datetime import datetime

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

plantID = 1

motor = False
light = False
st = False
manual = False

punchTime = {
    'actionTaken' : False,
    'minute' : 0
}

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

    manual = data['manual']

def updateInFocus():
    # pass
    temperature = getTemp()
    humidity = getHum()
    soilMoisture = getSoilMoisture()

    if(soilMoisture == True):
        sm = 100
    else:
        sm = 0

    data = {
        "temperature": temperature,
        "humidity": humidity,
        "soilMoisture": soilMoisture,
        "diseased": false
    }

    url = 'https://speeve-ponics.herokuapp.com/conditions/infocus/'+str(plantID)

    r = requests.post(url, data)


def updateData(): ## Onli on thr 15th min
    dt = datetime.now()
    m = dt.minute

    if((m%15) == 0):
        temperature = getTemp()
        humidity =getHum()
        soilMoisture = getSoilMoisture()

        data = {
            "timestamp": dt,
            "plant": 1,
            "temperature": temperature,
            "humidity": humidity,
            "soilMoisture": soilMoisture,
            "diseased": false
        }

        url = 'https://speeve-ponics.herokuapp.com/conditions/plant'

        r = requests.post(url, data)


def actoControls():
    sm = getSoilMoisture()

    dt = datetime.now()
    m = dt.minute

    if(((m%30) == 0) and (motor == False)):
        motorOn()
        motor = True

    if(((m == 35) or (m == 05)) and (motor == True)):
        motorOff()
        motor = False


    if((sm == False) and (motor == False)):
        motorOn()
        motor = True
        punchTime['actionTaken'] = True
        punchTime['minute'] = m

    if((punchTime['actionTaken'] == True)):
         # and (m >= punchTime['minute']))
         if((punchTime['minute'] >= 55) and ((m >= 0 ) and (m < 55))):
             motorOff()
             motor = False
             punchTime['actionTaken'] = False
             punchTime['minute'] = m

         elif(m >= (punchTime['minute'] + 5)):
             motorOff()
             motor = False
             punchTime['actionTaken'] = False
             punchTime['minute'] = m


while(True):
    checkActuateConditions()
    updateInFocus()
    updateData()
    if(manual == False):
        actoControls()


## Call all the functions in order in a while loop
