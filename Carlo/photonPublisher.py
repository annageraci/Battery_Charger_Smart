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
    deviceID = "113"
    userAssociationID = "1"
    baseTopic += userAssociationID + "/sensor"
    deviceName = "PhotonSimulator1"
    catalogURL = settingsDict["Catalog_url_Carlo"]
    sensor = PhotonSensor(deviceID, deviceName, userAssociationID, baseTopic, True)
    topic = sensor.getMQTTtopic()

    broker = settingsDict["broker"]["IPAddress"]
    port = settingsDict["broker"]["port"]
    publisher = SimSensorPublisher("csim48rPisensor" + deviceID, deviceID, deviceName, userAssociationID, broker, port, topic, catalogURL)
    publisher.startOperation()

    while True:
        print(topic)
        publisher.rPi_publish(topic, sensor.sensor_update(), 2)
        publisher.sendLastUpdateToCatalog()
        time.sleep(5)