import paho.mqtt.client as pahoMQTT
import cherrypy
import requests
import json
import time
from Sensors import *
from rPiCatalogUpdater import CatalogUpdater
from numpy import random

class ActuatorPublisher():
    def __init__(self, clientID, deviceID, deviceName, broker, port, topic, catalogURI, notifier=None):
        self.client = pahoMQTT.Client(clientID, True)
        self.deviceID = deviceID
        self.deviceName = deviceName
        # self.userID = userID
        self.broker = broker
        self.port = port
        self.notifier = notifier
        self.client.on_connect = self.rPi_onConnect
        self.topic = topic

    def startOperation(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()
    

    def rPi_onConnect(self, paho_mqtt, userdata, flags, rc):
        print("Connected to broker " + self.broker + " on port " + str(self.port) + " with result code " + str(rc))

    def rPi_publish(self, topic, json_payload, QoS=2):
        self.client.publish(topic, json.dumps(json_payload), QoS)
        print(json_payload)
        self.lastUpdate = time.time()

    def getLastUpdate(self):
        return self.lastUpdate

    

if __name__ == "__main__":
    topic = "Battery/IoT/project/UserID/1/actuator"
    deviceID = "101"
    userAssociationID = "1"
    deviceName = "BatterySimulator1"
    catalogURL = "http://127.0.0.1:8080"
    msg= {
            'bn': 'actuator',
            'e':
            [
                {'n': 'actuator', 'v': 0, 't': time.time(), 'u': ''},
            ]
        }  
    

    broker = "mqtt.eclipseprojects.io" # to be updated with the relative reference
    port = 1883 # same
    publisher = ActuatorPublisher("csim48rPiActuator" + str(1) + "pub", deviceID, deviceName, broker, port, topic, catalogURL)
    publisher.startOperation()

    while True:
        msg['e'][0]['v'] = random.binomial(1, 0.5)
        msg['e'][0]['t'] = time.time()
        print(f"New actuator state  \"{msg['e'][0]['v']}\" published at time {msg['e'][0]['t']}")
        publisher.rPi_publish(topic, msg, 2)
        time.sleep(3)