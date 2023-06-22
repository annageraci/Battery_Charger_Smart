import math
from Simulators import *
from Sensor import Sensor
import time
import datetime as dt

class TemperatureSensor(Sensor):
    def __init__(self, ID, name = "", userID = "1", baseTopic = "", simulated = True, location = 0, currTemp = None):
        Sensor.__init__(self, ID, name, userID, baseTopic, simulated, currTemp)
        self.unit = "Cel"
        self.location = location
        # 0: outside, 1: battery
        self.quantity = "temperature" + "B" * self.location
        self.measureType = "Temperature" + "B" * self.location

        if self.simulated:
            self.start_simulator()
            if currTemp != None:
                self.value = self.simulator.generateNewVal(dt.datetime.now(), self.prevValue) 
        
        else:
            # instructions related to RPi
            pass
        
        self.MQTTtopic += "/" + self.quantity
        self.dict = {"bn": self.ID, "e": [{"n": self.quantity, "u": self.unit, "t": self.time_last_update, "v": self.value}]}

    def start_simulator(self, dawnTime=6*3600+47*60, duskTime=20*3600+13*60, minTemp=8, maxTemp=23):
        if self.location == 0:
            self.simulator = OutsideTemperatureSimulator(dawnTime, duskTime, minTemp, maxTemp)
            self.value = self.simulator.generateNewVal(dt.datetime.now(), self.prevValue)
        else:
            self.simulator = BatteryTemperatureSimulator(True, initVal=self.value)

            
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


class PresenceSensor(Sensor):
    def __init__(self, ID, name = "", userID = "1", baseTopic="", simulated = True, URIarg = "Digital_Button", meanDuration=8, meanWait=15):
        Sensor.__init__(self, ID, name, userID, baseTopic, simulated)
        self.unit = ""
        self.quantity = "presence"
        self.measureType = "Boolean"
        if self.simulated:
            self.meanDuration = meanDuration
            self.meanWait = meanWait
            self.start_simulator()
        
        else:
            # instructions related to RPi
            pass
        
        self.MQTTtopic += "/" + self.quantity
        self.dict = {"bn": self.ID, "e": [{"n": self.quantity, "u": self.unit, "t": self.time_last_update, "v": self.value}]}

    def start_simulator(self):
        self.simulator = BinarySimulator(self.meanDuration, self.meanWait)
        self.value = self.simulator.generateNewVal()
    
    
class BatteryChargeSensor(Sensor):
    def __init__(self, ID, name="", userID = "1", baseTopic = "", simulated=True, currVal=None):
        Sensor.__init__(self, ID, name, userID, baseTopic, simulated, currVal)    
        self.unit = "%"
        self.quantity = "battery"
        self.measureType = "Percentage"
        if self.simulated:
            self.simulator = BatterySimulator(self.value)
        
        else:
            # instructions related to RPi
            pass
        
        self.MQTTtopic += "/" + self.quantity
        self.dict = {"bn": self.ID, "e": [{"n": self.quantity, "u": self.unit, "t": self.time_last_update, "v": self.value}]}

    # Sensor update and error check inherited from super class

    def getBatteryParams(self):
        return (self.simulator.charging, self.simulator.chargingSpeed, self.simulator.dischargingSpeed)

    def setBatteryParams(self, params):
        """
        params = (newChargingState, newChargingSpeed, newDischargingSpeed)\n
        Any of the fields can be set to None
        """
        if self.simulated:
            newChargingState, newChargingSpeed, newDischargingSpeed = params
            if newChargingState != None:
                self.simulator.setChargingState(newChargingState)
            if newChargingSpeed != None:
                self.simulator.setChargingSpeed(newChargingSpeed)
            if newDischargingSpeed != None:
                self.simulator.setDischargingSpeed(newDischargingSpeed)

class TempHumSensor(Sensor):
    def __init__(self, ID, name = "", userID = "1", baseTopic = "", simulated = True, currVals = None, humChangingSpeed = 1.0):
        Sensor.__init__(self, ID, name, userID, baseTopic, simulated, currVals)
        self.unit = ("Cel", "%")
        self.quantity = ("temperature", "humidity")
        self.measureType = "Temperature"
        currTemp, currHum = currVals
        self.value = [None,None]
        self.prevValue = [None, None]
        if self.simulated:
            self.tempSimulator = OutsideTemperatureSimulator()
            self.humSimulator = HumiditySimulator(currHum, humChangingSpeed)
            if currTemp != None:
                self.value[0] = currTemp
            if currHum != None:
                self.value[1] = currHum

        else:
            # instructions related to rPi
            pass

        self.MQTTtopic = "/temperature"
        self.dict = {"bn": self.ID,
                     "e": 
                        [{"n": self.quantity[0], "u": self.unit[0], "t": self.time_last_update, "v": self.value[0]},
                         {"n": self.quantity[1], "u": self.unit[1], "t": self.time_last_update, "v": self.value[1]}]
                    }
        

    def sensor_update(self):
        oldValue = self.value
        if self.simulated:
            self.value[0] = self.tempSimulator.generateNewVal(dt.dateTime.now(), self.prevValue[0])
            self.value[1] = self.humSimulator.generateNewVal()
        else:
            # instructions related to rPi
            pass
        self.prevValue = oldValue
        self.time_last_update = time.time()
        for i in range(2):
            self.dict["e"][i]["t"] = self.time_last_update
            self.dict["e"][i]["v"] = self.value[i]
            

    def setHumChangingSpeed(self, newSpeed):
        self.humSimulator.setChangingSpeed(newSpeed)


class PhotonSensor(Sensor):
    def __init__(self, ID, name = "", userID = "1", baseTopic = "", simulated = True, currLight = None):
        Sensor.__init__(self, ID, name, userID, baseTopic, simulated, currLight)
        self.unit = "V"
        self.quantity = "photon"
        self.measureType = "Voltage"
        if self.simulated:
            self.start_simulator()
        
        else:
            # instructions related to RPi
            pass

        self.MQTTtopic += "/" + self.quantity
        self.dict = {"bn": self.ID, "e": [{"n": self.quantity, "u": self.unit, "t": self.time_last_update, "v": self.value}]}

    def start_simulator(self, dawnTime=6*3600+47*60, duskTime=20*3600+13*60):
        self.simulator = PhotonSimulator(self.value, None, True, dawnTime, duskTime)
        self.value = self.simulator.generateNewVal(dt.datetime.now())

    def sensor_update(self):
        prevTime = self.time_last_update
        self.prevValue = self.value
        if self.simulated:
            self.value = self.simulator.generateNewVal(dt.datetime.now())
        else:
            pass

        self.time_last_update = time.time()
        self.dict["e"][0]["t"] = self.time_last_update
        self.dict["e"][0]["v"] = self.value
        return self.dict
    
    
class SwitchSensor(Sensor):
    def __init__(self, ID, name = "", userID = "1", baseTopic="", simulated = True, currVal = None):
        Sensor.__init__(self, ID, name, userID, baseTopic, simulated, currVal)
        self.unit = ""
        self.quantity = "switch"
        self.measureType = "Boolean"
        if self.simulated:
            self.start_simulator()
        
        else:
            # instructions related to RPi
            pass
        
        self.MQTTtopic += "/" + self.quantity
        self.dict = {"bn": self.ID, "e": [{"n": self.quantity, "u": self.unit, "t": self.time_last_update, "v": self.value}]}

    def start_simulator(self):
        self.simulator = BinarySimulator()
        self.value = self.simulator.generateNewVal()

        



