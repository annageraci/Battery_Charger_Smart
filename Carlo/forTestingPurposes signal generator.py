# from RPi import GPIO
# import paho.mqtt.client as pahoMQTT
import time
import datetime as dt
import json
import cherrypy
from TemperatureSensor import TemperatureSensor
from PresenceSensor import PresenceSensor
from numpy import random
import math

# GPIO.setmode(GPIO.BCM)

ber_p = 0.001

# reference day = april 14, 2022 in Turin

longitude = 7 + 40/60 + 32.52/3600
realTimeShift = 3600*(1 + (15-longitude)/15)
dawnTime = 6*3600+47*60
duskTime = 20*3600+13*60
minTemp = 8
maxTemp = 23
            


temperatureSensor = TemperatureSensor("10")
presenceSensor = PresenceSensor("11")

longitude = 7 + 40/60 + 32.52/3600
realTimeShift = 3600*(1 + (15-longitude)/15)
dawnTime = 6*3600+47*60
duskTime = 20*3600+13*60
minTemp = 8
maxTemp = 23

timeStep = 2
count = 0

print(longitude, realTimeShift, dawnTime, duskTime, minTemp, maxTemp)

print("Temperature sensor connected at instant " + str(temperatureSensor.time_connected))
print("Presence sensor connected at instant " + str(presenceSensor.time_connected))
time.sleep(timeStep)

while True and not (temperatureSensor.error+presenceSensor.error):
    if count < 50:
        temperatureSensor.sensor_update()
        presenceSensor.sensor_update()
        #print("Time: " + str(temperatureSensor.time_last_update))
        #print("Temperature: " + str(temperatureSensor.value) + "°C")
        print("Presence: " + str(presenceSensor.value))
    temperatureSensor.errorCheck()
    presenceSensor.errorCheck()
    count +=1





    time.sleep(timeStep)
