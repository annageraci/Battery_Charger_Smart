import pyfirmata
import time

class ArduinoPiConnector():
    def __init__(self, deviceID, deviceName = "", baseTopic = "", userID = "1", serialID = "/dev/ttyACM0", relayPin = 8, feedbackPin = 10):
        self.deviceID = deviceID
        self.deviceName = deviceName
        self.MQTTtopic = baseTopic
        self.userID = userID
        self.serialID = serialID
        self.board = pyfirmata.Arduino(serialID)
        self.arduinoInputIterator = pyfirmata.util.Iterator(self.board)
        self.relayPin = self.board.digital[relayPin]
        self.feedbackPin = self.board.digital[feedbackPin]
        self.currentState = False # boolean
        self.timeLastUpdate = time.time()
        self.errorCode = 0
        self.error = 0

    def startOperation(self):
        self.arduinoInputIterator.start()
        self.feedbackPin.mode = pyfirmata.INPUT
        self.relayPin.mode = pyfirmata.OUTPUT
        self.relayPin.write(1) # Low level trigger -> Start from "OFF"

        

    def updateCurrentState(self, newState):
        oldState = self.currentState
        self.currentState = newState
        self.timeLastUpdate = time.time()
        if oldState != self.currentState:
            self.relayPin.write(not self.currentState)
    
    def getCurrentState(self):
        return self.currentState

    def errorCheck(self):
        self.errorCode = 0
        if self.feedbackPin.read() == self.currentState:
            self.error = True
            self.errorCode = 1
            print("Error: relay state inconsistent with theoretical value.")
        elif time.time() - self.timeLastUpdate > 120:
            self.error = True
            self.errorCode = 2
            print("Error: the actuator has not been updated for 120 seconds.")
        return self.errorCode

