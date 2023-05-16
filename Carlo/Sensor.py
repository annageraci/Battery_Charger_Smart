import time
import datetime as dt
import math

class Sensor():
    def __init__(self, ID, name = "", userID = "1", baseTopic = "", simulated = True, currVal = None):
        self.ID = ID
        self.name = name
        self.userID = userID
        self.time_connected = time.time()
        self.time_last_update = self.time_connected
        self.error = False
        self.errorCode = 0
        self.prevValue = None
        self.simulated = simulated
        self.quantity = None
        self.unit = None
        self.value = currVal
        self.MQTTtopic = baseTopic

    def start_simulator(self):
        pass

    def getValue(self):
        return self.value

    def sensor_update(self):
        self.prevValue = self.value
        if self.simulated:
            self.value = self.simulator.generateNewVal()
        else:
            pass

        self.time_last_update = time.time()
        self.dict["e"][0]["t"] = self.time_last_update
        self.dict["e"][0]["v"] = self.value
        return self.dict
        

    def errorCheck(self):
        if time.time() - self.time_last_update > 120:
            self.error = True
            self.errorCode = 2

        if self.error:
            print("Error: the sensor has generated no data for 120 seconds. Disconnecting.")
        
        return self.errorCode
    
    def getMQTTtopic(self):
        return self.MQTTtopic