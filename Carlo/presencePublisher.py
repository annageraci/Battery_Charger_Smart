import time
from Sensors import *
from Publishers import SensorPublisher
import json

if __name__ == "__main__":
    settings_file_path = 'settings.json'

    settingsFile = open(settings_file_path)
    settingsDict = json.load(settingsFile)
    settingsFile.close()
    baseTopic = settingsDict["baseTopic"]
    deviceID = "114"
    userAssociationID = "1"
    baseTopic += userAssociationID + "/sensor"
    deviceName = "PresenceSimulator1"
    catalogURL = settingsDict["Catalog_url_Carlo"]
    sensor = PresenceSensor(deviceID, deviceName, userAssociationID, baseTopic, True,meanDuration=15,meanWait=0)
    topic = sensor.getMQTTtopic()

    broker = settingsDict["broker"]["IPAddress"]
    port = settingsDict["broker"]["port"]
    publisher = SensorPublisher("csim48rPisensor" + deviceID, deviceID, deviceName, userAssociationID, sensor.getMeasureType(), broker, port, topic, catalogURL)
    publisher.startOperation()

    while True:
        publisher.rPi_publish(topic, sensor.sensor_update(), 2)
        publisher.sendLastUpdateToCatalog(sensor.getValue())
        time.sleep(5)