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
    deviceID = "113"
    userAssociationID = "1"
    baseTopic += userAssociationID + "/sensor"
    deviceName = "PhotonSimulator1"
    catalogURL = settingsDict["Catalog_url_Carlo"]
    # sensor = PhotonSensor(deviceID, deviceName, userAssociationID, baseTopic, True)
    # topic = sensor.getMQTTtopic()
    broker = settingsDict["broker"]["IPAddress"]
    port = settingsDict["broker"]["port"]
    # publisher = SensorPublisher("csim48rPisensor" + deviceID, deviceID, deviceName, userAssociationID, broker, port, topic, catalogURL)
    # publisher.startOperation()
    sensors = []
    topics = []
    publishers = []
    users = [1,2,4]

    for i in range(len(users)):
        userAssociationID = str(users[i])
        baseTopic = settingsDict["baseTopic"] + userAssociationID + "/sensor"
        deviceID = str(103+10*users[i])
        deviceName = "PhotonSimulator"+str(users[i])
        if i == 0:
            baseValue = 3.8
        else:
            baseValue = 1.5
        sensors.append(PhotonSensor(deviceID, deviceName, userAssociationID, baseTopic, True, baseValue))
        topic = sensors[i].getMQTTtopic()
        publishers.append(SensorPublisher("csim48rPisensor" + deviceID, deviceID, deviceName, userAssociationID, sensors[i].getMeasureType(), broker, port, topic, catalogURL))
        publishers[i].startOperation()
    while True:
        for i in range(len(users)):
            publishers[i].rPi_publish(sensors[i].sensor_update(), 2)
            publishers[i].sendLastUpdateToCatalog(sensors[i].getValue())
        time.sleep(5)