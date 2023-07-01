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
    catalogURL = settingsDict["Catalog_url_Carlo"]
    # sensor = PresenceSensor(deviceID, deviceName, userAssociationID, baseTopic, True,meanDuration=15,meanWait=0)
    broker = settingsDict["broker"]["IPAddress"]
    port = settingsDict["broker"]["port"]
    # publisher = SensorPublisher("csim48rPisensor" + deviceID, deviceID, deviceName, userAssociationID, broker, port, topic, catalogURL)
    # publisher.startOperation()
    sensors = []
    publishers = []
    users = [1,2,4]

    for i in range(len(users)):
        userAssociationID = str(users[i])
        baseTopic = settingsDict["baseTopic"] + userAssociationID + "/sensor"
        deviceID = str(104+10*users[i])
        deviceName = "PresenceSimulator"+str(users[i])
        sensors.append(PresenceSensor(deviceID, deviceName, userAssociationID, baseTopic, True,meanDuration=15,meanWait=0))
        topic = sensors[i].getMQTTtopic()
        publishers.append(SensorPublisher("csim48rPisensor" + deviceID, deviceID, deviceName, userAssociationID, sensors[i].getMeasureType(), broker, port, topic, catalogURL))
        publishers[i].startOperation()
    while True:
        for i in range(len(users)):
            publishers[i].rPi_publish(sensors[i].sensor_update(), 2)
            publishers[i].sendLastUpdateToCatalog(sensors[i].getValue())
        time.sleep(5)