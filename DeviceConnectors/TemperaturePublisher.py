import time
import os
from Sensors import *
from Publishers import SensorPublisher
import json

if __name__ == "__main__":
    currDir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(currDir,'..','settings.json')
    # to run with Docker:
    # settings_file_path = '/app/settings/settings.json'

    settingsFile = open(settings_file_path)
    settingsDict = json.load(settingsFile)
    settingsFile.close()
    baseTopic = settingsDict["baseTopic"]
    deviceID = "110"
    userAssociationID = "1"
    baseTopic += userAssociationID + "/sensor"
    deviceName = "TemperatureSimulator1"
    catalogURL = settingsDict["Catalog_url_Carlo"]
    sensor = TemperatureSensor(deviceID, deviceName, userAssociationID, baseTopic, True)
    topic = sensor.getMQTTtopic()

    broker = settingsDict["broker"]["IPAddress"] # to be updated with the relative reference
    port = settingsDict["broker"]["port"] # same
    publisher = SensorPublisher("csim48rPisensor" + deviceID, deviceID, deviceName, userAssociationID, broker, port, topic, catalogURL)
    publisher.startOperation()

    while True:
        publisher.rPi_publish(topic, sensor.sensor_update(), 2)
        publisher.sendLastUpdateToCatalog(sensor.getValue())
        time.sleep(5)