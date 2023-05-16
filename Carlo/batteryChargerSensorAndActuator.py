from ArduinoPiConnector import ArduinoPiConnector
import paho.mqtt.client as pahoMQTT
import json
import time
from OnConnectionCatalogUpdater import CatalogUpdater
from ActuatorSubscriber import ActuatorSubscriber
from Sensors import BatteryChargeSensor
from SimPublisher import SimSensorPublisher

if __name__ == "__main__":
    settings_file_path = 'settings.json'

    settingsFile = open(settings_file_path)
    settingsDict = json.load(settingsFile)
    settingsFile.close()
    baseTopic = settingsDict["baseTopic"]
    publisherID = "111"
    userAssociationID = "1"
    baseTopic += userAssociationID
    sensorName = "BatteryChargeSimulator1"
    sensor = BatteryChargeSensor(publisherID, sensorName, userAssociationID, baseTopic+"/sensor", True)
    sensorTopic = sensor.getMQTTtopic()
    subscriberID = "101"
    userAssociationID = "1"
    deviceName = "Actuator1"
    catalogURL = settingsDict["Catalog_url_Carlo"]
    broker = settingsDict["broker"]["IPAddress"]
    port = settingsDict["broker"]["port"]
    

    subscriber = ActuatorSubscriber("csim48rPiActuator" + subscriberID + "sub", subscriberID, deviceName, userAssociationID, broker, port, baseTopic, catalogURL)
    subscriber.startOperation()

    publisher = SimSensorPublisher("csim48rPisensor" + publisherID, publisherID, deviceName, userAssociationID, broker, port, sensorTopic, catalogURL)
    publisher.startOperation()

    actuatorTopic = subscriber.getMQTTtopic()
    subscriber.actuator_subscribe(actuatorTopic, 2)

    errorCode = 0
    while not errorCode:
        time.sleep(1)
        sensor.setBatteryParams((subscriber.getCurrentState(),None,None))
        publisher.rPi_publish(sensorTopic, sensor.sensor_update(), 2)
        publisher.sendLastUpdateToCatalog()
        errorCode = subscriber.arduinoConnector.errorCheck()
