import json
import time
from ActuatorSubscriber import ActuatorSubscriber
from Sensors import BatteryChargeSensor
from Publishers import SensorPublisher

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
    sensor = BatteryChargeSensor(publisherID, sensorName, userAssociationID, baseTopic+"/sensor", True, 30)
    sensorTopic = sensor.getMQTTtopic()
    subscriberID = "5"
    userAssociationID = "1"
    deviceName = "Actuator1"
    catalogURL = settingsDict["Catalog_url_Carlo"]
    print (catalogURL)
    broker = settingsDict["broker"]["IPAddress"]
    port = settingsDict["broker"]["port"]
    

    subscriber = ActuatorSubscriber("csim48rPiActuator" + subscriberID + "sub", subscriberID, deviceName, userAssociationID, sensor.getMeasureType(), broker, port, baseTopic, catalogURL)
    subscriber.startOperation()

    publisher = SensorPublisher("csim48rPisensor" + publisherID, publisherID, deviceName, userAssociationID, sensor.getMeasureType(), broker, port, sensorTopic, catalogURL)
    publisher.startOperation()

    actuatorTopic = subscriber.getMQTTtopic()
    subscriber.actuator_subscribe(actuatorTopic, 2)

    errorCode = 0
    while True:
        time.sleep(5)
        sensor.setBatteryParams((subscriber.getCurrentState(),None,0.0005))
        if not errorCode:
            publisher.rPi_publish(sensor.sensor_update(), 2)
            publisher.sendLastUpdateToCatalog()
            errorCode = subscriber.arduinoConnector.errorCheck()
