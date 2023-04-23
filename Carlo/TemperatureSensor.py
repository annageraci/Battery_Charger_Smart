import math
from Simulators import TemperatureSimulator
from Sensor import Sensor
import time
import datetime as dt
import paho.mqtt.client as pahoMQTT

class TemperatureSensor(Sensor):
    def __init__(self, ID, name = "", simulated = True, currTemp = None):
        Sensor.__init__(self, ID, name, simulated, currTemp)
        self.unit = "Cel"
        self.quantity = "temperature"
        if self.simulated:
            self.simulator = TemperatureSimulator()
            self.value = self.simulator.generateNewVal(dt.datetime.now(), self.prevValue) 
        
        else:
            # instructions related to RPi
            pass

        self.dict = {"bn": self.ID, "e": [{"n": "temperature", "u": "Cel", "t": self.time_last_update, "v": self.value}]}

    def start_simulator(self, dawnTime=6*3600+47*60, duskTime=20*3600+13*60, minTemp=8, maxTemp=23):
        self.simulator = TemperatureSimulator(dawnTime, duskTime, minTemp, maxTemp)
        self.value = self.simulator.generateNewVal(dt.datetime.now(), self.prevValue)

            
    def sensor_update(self):
        prevVal = self.prevValue
        prevTime = self.time_last_update
        self.prevValue = self.value
        if self.simulated:
            self.value = self.simulator.generateNewVal(dt.datetime.now(), prevVal)
        else:
            pass

        self.time_last_update = time.time()
        self.dict["e"][0]["t"] = self.time_last_update
        self.dict["e"][0]["v"] = self.value
        return self.dict
        

    def errorCheck(self):
        if time.time() - self.time_last_update > 120:
            self.error = True
            self.errorCode = 1

        try:
            if math.abs(self.value - self.prevValue) > 5:
                self.error = True
                self.errorCode = 2
        except:
            pass

        

        
        if self.error:
            if self.errorCode == 2:
                print("Value error: incoherent temperature values (previous: " + str(self.value) +"°C, current: " + str(self.prevValue) + "°C)")
            elif self.errorCode == 1:
                print("Error: the sensor has generated no data for 120 seconds. Disconnecting.")

        return self.errorCode