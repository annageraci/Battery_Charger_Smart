import pyfirmata
import paho.mqtt.client as pahoMQTT
import requests
import time

class ArduinoPiConnector():
    def __init__(self, deviceID, deviceName = "", baseTopic = "", userID = "1", serialID = "/dev/ttyACM0", relayPin = 10):
        self.deviceID = deviceID
        self.deviceName = deviceName
        self.MQTTtopic = baseTopic
        self.userID = userID
        self.serialID = serialID
        self.board = pyfirmata.Arduino(serialID)
        self.relayPin = 10
        self.currentState = self.board.digital[self.relayPin].read() # boolean
        self.timeLastUpdate = time.time()
        

    def updateCurrentState(self, newState):
        oldState = self.currentState
        self.currentState = newState
        if oldState != newState:
            self.board.digital[self.relayPin].write(int(newState))

