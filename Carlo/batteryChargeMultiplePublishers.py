import time
import os
from Sensors import *
from Publishers import SensorPublisher
from ActuatorSubscriber import ActuatorExtSubscriber
import json

if __name__ == "__main__":
    currDir = os.path.dirname(os.path.abspath(__file__))
    settings_file_path = os.path.join(currDir,'..','settings.json')

    settingsFile = open(settings_file_path)
    settingsDict = json.load(settingsFile)
    settingsFile.close()
    baseTopic = settingsDict["baseTopic"]
    deviceID = "111"
    userAssociationID = "1"
    baseTopic += userAssociationID + "/sensor"
    deviceName = "BatteryChargeSimulator1"
    catalogURL = settingsDict["Catalog_url_Carlo"]
    broker = settingsDict["broker"]["IPAddress"]
    port = settingsDict["broker"]["port"]
    sensors = []
    publishers = []
    users = [1, 2, 4]
    actuatorSubscribers = []
    battery_start_values = [30, 80, 40] 
    actuatorDeviceIDs = ["5", "9", "17"]
    charging_states = [False, False, False]


    for i in range(len(users)-1):

        userAssociationID = str(users[i+1])
        baseTopic = settingsDict["baseTopic"] + userAssociationID + "/sensor"
        baseActTopic = settingsDict["baseTopic"] + userAssociationID
        deviceID = str(101+10*users[i+1])
        deviceName = "BatteryChargeSimulator"+str(users[i+1])
        sensors.append(BatteryChargeSensor(deviceID, deviceName, userAssociationID, baseTopic, True, battery_start_values[i]))
        actuatorSubscribers.append(ActuatorExtSubscriber("csim48Actuator"+actuatorDeviceIDs[i]+"sub", actuatorDeviceIDs[i], userAssociationID, broker, port, baseActTopic))
        if i+1 != 2:
            sensors[i].setBatteryParams((True, None, None))
            charging_states[i+1] = True
        else:
            sensors[i].setBatteryParams((False, None, 0.0005))
        topic = sensors[i].getMQTTtopic()
        publishers.append(SensorPublisher("csim48rPisensor" + deviceID, deviceID, deviceName, userAssociationID, sensors[i].getMeasureType(), broker, port, topic, catalogURL))
        publishers[i].startOperation()
    while True:
        for i in range(len(users)-1):
            publishers[i].rPi_publish(sensors[i].sensor_update(), 2)
            publishers[i].sendLastUpdateToCatalog(sensors[i].getValue())
            if actuatorSubscribers[i].getCurrentState() != sensors[i].getBatteryParams()[0]:
                sensors[i].setBatteryParams((actuatorSubscribers[i].getCurrentState(), None, None))
        time.sleep(5)