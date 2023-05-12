from ArduinoPiConnector import ArduinoPiConnector
import paho.mqtt.client as pahoMQTT
import json
import time
from OnConnectionCatalogUpdater import CatalogUpdater

class ActuatorSubscriber():
    def __init__(self, clientID, deviceID, deviceName, userID, broker, port, baseTopic, catalogURL, notifier=None):
        self.client = pahoMQTT.Client(clientID, True)
        self.deviceID = deviceID
        self.deviceName = deviceName
        self.userID = userID
        self.broker = broker
        self.port = port
        self.notifier = notifier
        self.client.on_connect = self.actuator_onConnect
        self.client.on_message = self.actuator_onMsgRec
        self.MQTTtopic = baseTopic+"/actuator"
        self.catalogURL = catalogURL
        self.arduinoConnector = ArduinoPiConnector(self.deviceID, self.deviceName, self.MQTTtopic, "1", "/dev/ttyACM0")
        self.catalogUpdater = CatalogUpdater(self.catalogURL, self.deviceID, self.MQTTtopic)
        self.lastUpdate = time.time()

    def startOperation(self):
        self.arduinoConnector.startInput()
        self.catalogUpdater.joinCatalog()
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def actuator_onConnect(self, paho_mqtt, userdata, flags, rc):
        print("Connected to broker " + self.broker + " on port " + str(self.port) + " with result code " + str(rc))

    def actuator_subscribe(self, topic, QoS=2):
        self.client.subscribe(topic, QoS)
        self.lastUpdate = time.time()

    def actuator_onMsgRec(self, client, userdata, msg):
        self.msg = json.loads(msg.payload)
        newValue = self.msg['e'][0]['v']
        self.lastUpdate = self.msg['e'][0]['t']
        self.arduinoConnector.updateCurrentState(newValue)
        print (f"Output state updated to \"{newValue}\" at time {self.lastUpdate}")
    
    def getLastUpdate(self):
        return self.lastUpdate
    
    def getMQTTtopic(self):
        return self.MQTTtopic
    

if __name__ == "__main__":
    settings_file_path = 'settings.json'

    settingsFile = open(settings_file_path)
    settingsDict = json.load(settingsFile)
    settingsFile.close()
    baseTopic = settingsDict["baseTopic"]

    deviceID = "101"
    userAssociationID = "1"
    baseTopic += userAssociationID
    deviceName = "Actuator1"
    catalogURL = settingsDict["Catalog_url_Anna"]
    

    broker = settingsDict["broker"]["IPAddress"]
    port = settingsDict["broker"]["port"]
    subscriber = ActuatorSubscriber("csim48rPiActuator" + deviceID + "sub", deviceID, deviceName, broker, port, baseTopic)
    subscriber.startOperation()

    topic = subscriber.getMQTTtopic()
    subscriber.actuator_subscribe(topic, 2)

    errorCode = 0
    while not errorCode:
        time.sleep(3)
        errorCode = subscriber.arduinoConnector.errorCheck()
