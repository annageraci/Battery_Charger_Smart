import math
from Sensor import Sensor
from Simulators import PresenceSimulator
import time
import datetime as dt
import paho.mqtt.client as pahoMQTT

class PresenceSensor(Sensor):
    def __init__(self, ID, name = "", simulated = True, currTemp = None):
        self.unit = ""
        self.quantity = "presence"
        Sensor.__init__(self, ID, name, simulated, currTemp)
        if self.simulated:
            self.start_simulator()
        
        else:
            # instructions related to RPi
            pass

        self.dict = {"bn": self.ID, "e": [{"n": self.quantity, "u": self.unit, "t": self.time_last_update, "v": self.value}]}

    def start_simulator(self):
        self.simulator = PresenceSimulator()
        self.value = self.simulator.generateNewVal()

            
    # def sensor_update(self):
    #     prevVal = self.prevValue
    #     prevTime = self.time_last_update
    #     self.prevValue = self.value
    #     if self.simulated:
    #         self.value = self.simulator.generateNewVal(dt.datetime.now(), prevVal)
    #     else:
    #         pass

    #     self.time_last_update = time.time()
    #     self.dict["e"][0]["t"] = self.time_last_update
    #     self.dict["e"][0]["v"] = self.value
    #     return self.dict
        

    def errorCheck(self):
        try:
            if math.abs(self.value - self.prevValue) > 5:
                self.error = True
                self.errorCode = 1
        except:
            pass

        if time.time() - self.time_last_update > 120:
            self.error = True
            self.errorCode = 2

        
        if self.error:
            if self.errorCode == 1:
                print("Value error: incoherent temperature values (previous: " + str(self.value) +"°C, current: " + str(self.prevValue) + "°C)")
            elif self.errorCode == 2:
                print("Error: the sensor has generated no data for 120 seconds. Disconnecting.")

        return self.errorCode