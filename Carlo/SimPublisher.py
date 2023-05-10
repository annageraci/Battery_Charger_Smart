import paho.mqtt.client as pahoMQTT
import cherrypy
import requests
import json
import time
from Sensors import *
from rPiCatalogUpdater import CatalogUpdater

class SimSensorPublisher():
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
        self.catalogUpdater = CatalogUpdater(catalogURI, self.deviceID, self.deviceName)

    def startOperation(self):
        self.client.connect(self.broker, self.port)
        self.catalogUpdater.joinCatalog()
        self.client.loop_start()
    

    def rPi_onConnect(self, paho_mqtt, userdata, flags, rc):
        print("Connected to broker " + self.broker + " on port " + str(self.port) + " with result code " + str(rc))

    def rPi_publish(self, topic, json_payload, QoS=2):
        self.client.publish(topic, json.dumps(json_payload), QoS)
        print(json_payload)
        self.lastUpdate = time.time()
        self.catalogUpdater.setUpdateTime(self.lastUpdate)

    def getLastUpdate(self):
        return self.lastUpdate
    
    def sendLastUpdateToCatalog(self):
        self.catalogUpdater.generateMessage()
        self.catalogUpdater.sendMessage()

    

if __name__ == "__main__":
    topic = "Battery/IoT/project/UserID/1/sensor"
    deviceID = "101"
    userAssociationID = "1"
    deviceName = "HumiditySimulator1"
    catalogURL = "https://192.168.72.16:8080"
    sensor = PhotonSensor(deviceID, deviceName, userAssociationID, topic, True)
    

    broker = "mqtt.eclipseprojects.io" # to be updated with the relative reference
    port = 1883 # same
    publisher = SimSensorPublisher("csim48rPisensor" + str(1), deviceID, deviceName, broker, port, topic, catalogURL)
    publisher.startOperation()

    while True:
        publisher.rPi_publish(topic, sensor.sensor_update(), 2)
        publisher.sendLastUpdateToCatalog()
        time.sleep(5)



    



