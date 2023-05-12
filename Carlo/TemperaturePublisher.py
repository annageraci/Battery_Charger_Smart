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
    deviceID = "110"
    userAssociationID = "1"
    baseTopic += userAssociationID + "/sensor"
    deviceName = "TemperatureSimulator1"
    catalogURL = settingsDict["Catalog_url_Anna"]
    sensor = TemperatureSensor(deviceID, deviceName, userAssociationID, baseTopic, True)
    topic = sensor.getMQTTtopic()

    broker = settingsDict["broker"]["IPAddress"] # to be updated with the relative reference
    port = settingsDict["broker"]["port"] # same
    publisher = SimSensorPublisher("csim48rPisensor" + deviceID, deviceID, deviceName, userAssociationID, broker, port, topic, catalogURL)
    publisher.startOperation()

    while True:
        publisher.rPi_publish(topic, sensor.sensor_update(), 2)
        publisher.sendLastUpdateToCatalog()
        time.sleep(5)