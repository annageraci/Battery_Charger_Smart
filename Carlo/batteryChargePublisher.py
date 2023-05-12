import time
from Sensors import *
from SimPublisher import SimSensorPublisher
import json

if __name__ == "__main__":
    settings_file_path = 'settings.json'

    settingsFile = open(settings_file_path)
    settingsDict = json.load(settingsFile)
    settingsFile.close()
    baseTopic = settingsDict["baseTopic"]
    deviceID = "111"
    userAssociationID = "1"
    baseTopic += userAssociationID + "/sensor"
    deviceName = "BatteryChargeSimulator1"
    catalogURL = "http://192.168.72.16:8080"
    sensor = BatteryChargeSensor(deviceID, deviceName, userAssociationID, baseTopic, True)
    topic = sensor.getMQTTtopic()

    broker = "mqtt.eclipseprojects.io" # to be updated with the relative reference
    port = 1883 # same
    publisher = SimSensorPublisher("csim48rPisensor" + deviceID, deviceID, deviceName, userAssociationID, broker, port, topic, catalogURL)
    publisher.startOperation()

    while True:
        publisher.rPi_publish(topic, sensor.sensor_update(), 2)
        publisher.sendLastUpdateToCatalog()
        time.sleep(5)