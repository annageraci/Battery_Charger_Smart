import paho.mqtt.client as pahoMQTT
import json
import time
from OnConnectionCatalogUpdater import CatalogUpdater

class SensorPublisher():
    def __init__(self, clientID, deviceID, deviceName, userID, measureType, broker, port, topic, catalogURI, value = None, notifier=None):
        self.client = pahoMQTT.Client(clientID, True)
        self.deviceID = deviceID
        self.deviceName = deviceName
        self.userID = userID
        self.measureType = measureType
        self.broker = broker
        self.port = port
        self.notifier = notifier
        self.client.on_connect = self.rPi_onConnect
        self.topic = str(topic)
        self.value = value
        self.catalogUpdater = CatalogUpdater(catalogURI, self.topic, self.deviceID, self.deviceName, self.userID, self.measureType)

    def startOperation(self):
        self.catalogUpdater.joinCatalog()
        self.client.connect(self.broker, self.port)
        self.client.loop_start()
    
    def updateValue(self, newValue):
        self.value = newValue

    def rPi_onConnect(self, paho_mqtt, userdata, flags, rc):
        print("Connected to broker " + self.broker + " on port " + str(self.port) + " with result code " + str(rc))

    def rPi_publish(self, json_payload, QoS=2):
        self.client.publish(self.topic, json.dumps(json_payload), QoS)
        print(json_payload)
        print(self.topic)
        self.lastUpdate = time.time()
        self.catalogUpdater.setUpdateTime(self.lastUpdate)

    def getLastUpdate(self):
        return self.lastUpdate
    
    def sendLastUpdateToCatalog(self, value = None):
        if value == None:
            value = self.value
        self.catalogUpdater.generateMessage(value)
        self.catalogUpdater.sendMessage()


class ManualFlagPublisher():
    def __init__(self, clientID, userID, broker, port, topic, notifier=None):
        self.client = pahoMQTT.Client(clientID, True)
        self.userID = userID
        self.broker = broker
        self.port = port
        self.notifier = notifier
        self.client.on_connect = self.manualFlag_onConnect
        self.topic = topic

    def startOperation(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()
    
    def updateValue(self, newValue):
        self.value = newValue

    def manualFlag_onConnect(self, paho_mqtt, userdata, flags, rc):
        print("Connected to broker " + self.broker + " on port " + str(self.port) + " with result code " + str(rc))

    def mf_publish(self, topic, json_payload, QoS=2):
        self.client.publish(topic, json.dumps(json_payload), QoS)
        print(json_payload)
        print(topic)

    
# For testing only

if __name__ == "__main__":
    from Sensors import PhotonSensor
    topic = "Battery/IoT/project/UserID/1/sensor"
    deviceID = "101"
    userAssociationID = "1"
    deviceName = "PhotonSimulator1"
    catalogURL = "https://192.168.72.16:8080"
    sensor = PhotonSensor(deviceID, deviceName, userAssociationID, topic, True)
    

    broker = "mqtt.eclipseprojects.io" # to be updated with the relative reference
    port = 1883 # same
    publisher = SensorPublisher("csim48rPisensor" + str(1), deviceID, deviceName, broker, port, topic, catalogURL)
    publisher.startOperation()

    while True:
        publisher.rPi_publish(topic, sensor.sensor_update(), 2)
        publisher.sendLastUpdateToCatalog(sensor.getValue())
        time.sleep(5)
