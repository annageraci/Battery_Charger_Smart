import time
from Sensors import *
from rPiCatalogUpdater import CatalogUpdater
from SimPublisher import SimSensorPublisher

if __name__ == "__main__":
    topic = "Battery/IoT/project/UserID/1/sensor"
    deviceID = "111"
    userAssociationID = "1"
    deviceName = "TemperatureSimulator1"
    catalogURL = "http://192.168.72.16:8080"
    sensor = BatteryChargeSensor(deviceID, deviceName, userAssociationID, topic, True)
    

    broker = "mqtt.eclipseprojects.io" # to be updated with the relative reference
    port = 1883 # same
    publisher = SimSensorPublisher("csim48rPisensor" + str(1), deviceID, deviceName, broker, port, topic, catalogURL)
    publisher.startOperation()

    while True:
        publisher.rPi_publish(topic, sensor.sensor_update(), 2)
        publisher.sendLastUpdateToCatalog()
        time.sleep(5)