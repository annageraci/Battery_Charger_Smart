from ArduinoPiConnectorForRpi import ArduinoPiConnector
import paho.mqtt.client as pahoMQTT
import json
import time
from OnConnectionCatalogUpdater import CatalogUpdater

class ActuatorSubscriber():
    def __init__(self, clientID, deviceID, deviceName, userID, measureType, broker, port, baseTopic, catalogURL, notifier=None):
        self.client = pahoMQTT.Client(clientID, True)
        self.deviceID = deviceID
        self.deviceName = deviceName
        self.userID = userID
        self.measureType = measureType
        self.broker = broker
        self.port = port
        self.notifier = notifier
        self.client.on_connect = self.actuator_onConnect
        self.client.on_message = self.actuator_onMsgRec
        self.MQTTtopic = baseTopic+"/actuator"
        print ("Actuator subscribe topic: ", self.MQTTtopic)
        self.catalogURL = catalogURL
        self.arduinoConnector = ArduinoPiConnector(self.deviceID, self.deviceName, self.MQTTtopic, "1", "/dev/ttyACM0")
        self.catalogUpdater = CatalogUpdater(self.catalogURL, self.deviceID, self.MQTTtopic, self.deviceName, self.userID, self.measureType)
        self.lastUpdate = time.time()
        self.currentState = self.arduinoConnector.getCurrentState()

    def startOperation(self):
        self.arduinoConnector.startOperation()
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
        if self.msg['bn'] == self.deviceID:
            newValue = self.msg['e'][0]['v']
            self.lastUpdate = self.msg['e'][0]['t']
            self.arduinoConnector.updateCurrentState(newValue)
            self.currentState = self.arduinoConnector.getCurrentState()
            print (f"Output state updated to \"{newValue}\" at time {self.lastUpdate}")
            self.catalogUpdater.generateMessage(self.currentState)
            self.catalogUpdater.sendMessage()
            return newValue
    
    def getLastUpdate(self):
        return self.lastUpdate
    
    def getMQTTtopic(self):
        return self.MQTTtopic
    
    def getCurrentState(self):
        return self.currentState
    
class ActuatorExtSubscriber():
    def __init__(self, clientID, deviceID, userID, broker, port, baseTopic, initState = None, notifier=None):
        self.client = pahoMQTT.Client(clientID, True)
        self.deviceID = deviceID
        self.userID = userID
        self.broker = broker
        self.port = port
        self.notifier = notifier
        self.client.on_connect = self.actuator_onConnect
        self.client.on_message = self.actuator_onMsgRec
        self.MQTTtopic = baseTopic+"/actuator"
        print ("Actuator subscribe topic: ", self.MQTTtopic)
        self.lastUpdate = time.time()
        self.currentState = initState

    def startOperation(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def actuator_onConnect(self, paho_mqtt, userdata, flags, rc):
        print("Connected to broker " + self.broker + " on port " + str(self.port) + " with result code " + str(rc))

    def actuator_subscribe(self, topic, QoS=2):
        self.client.subscribe(topic, QoS)
        self.lastUpdate = time.time()

    def actuator_onMsgRec(self, client, userdata, msg):
        self.msg = json.loads(msg.payload)
        if self.msg['bn'] == self.deviceID:
            newValue = self.msg['e'][0]['v']
            self.lastUpdate = self.msg['e'][0]['t']
            print (f"Output state updated to \"{newValue}\" at time {self.lastUpdate}")
            self.currentState = bool(newValue)
            return newValue
    
    def getLastUpdate(self):
        return self.lastUpdate
    
    def getMQTTtopic(self):
        return self.MQTTtopic
    
    def getCurrentState(self):
        return self.currentState

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
    subscriber = ActuatorSubscriber("csim48rPiActuator" + deviceID + "sub", deviceID, deviceName, "Percentage", broker, port, baseTopic)
    subscriber.startOperation()

    topic = subscriber.getMQTTtopic()
    subscriber.actuator_subscribe(topic, 2)

    errorCode = 0
    while not errorCode:
        time.sleep(3)
        errorCode = subscriber.arduinoConnector.errorCheck()
