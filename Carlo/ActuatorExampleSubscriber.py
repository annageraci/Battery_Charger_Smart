from ArduinoPiConnector import ArduinoPiConnector
import paho.mqtt.client as pahoMQTT
import json
import time

class ActuatorSubscriber():
    def __init__(self, clientID, deviceID, deviceName, broker, port, topic, notifier=None):
        self.client = pahoMQTT.Client(clientID, True)
        self.deviceID = deviceID
        self.deviceName = deviceName
        # self.userID = userID
        self.broker = broker
        self.port = port
        self.notifier = notifier
        self.client.on_connect = self.actuator_onConnect
        self.client.on_message = self.actuator_onMsgRec
        self.topic = topic
        self.arduinoConnector = ArduinoPiConnector(self.deviceID, self.deviceName, self.topic, "1", "/dev/ttyACM0")
        self.lastUpdate = time.time()

    def startOperation(self):
        self.arduinoConnector.startInput()
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
        self.lastUpdate = self.msg['e'][0]["t"]
        self.arduinoConnector.updateCurrentState(newValue)
        print (f"Output state updated to \"{newValue}\" at time {self.lastUpdate}")
    
    def getLastUpdate(self):
        return self.lastUpdate

    

if __name__ == "__main__":
    topic = "Battery/IoT/project/UserID/1/actuator"
    deviceID = "101"
    userAssociationID = "1"
    deviceName = "BatterySimulator1"
    catalogURL = "http://192.168.72.16:8080"
    

    broker = "mqtt.eclipseprojects.io" # to be updated with the relative reference
    port = 1883 # same
    subscriber = ActuatorSubscriber("csim48rPiActuator" + str(1) + "sub", deviceID, deviceName, broker, port, topic)
    subscriber.startOperation()

    subscriber.actuator_subscribe(topic, 2)

    errorCode = 0
    while not errorCode:
        time.sleep(3)
        errorCode = subscriber.arduinoConnector.errorCheck()
