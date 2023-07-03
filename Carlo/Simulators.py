from numpy import random
import datetime as dt
import math
import numpy as np

class OutsideTemperatureSimulator():

    def __init__(self, dawnTime=6*3600+47*60, duskTime=20*3600+13*60, minTemp=8, maxTemp=23):
        self.longitude = 7 + 40/60 + 32.52/3600
        self.timeShift = 3600*(1 + (15-self.longitude)/15)
        self.dawnTime = dawnTime
        self.duskTime = duskTime
        self.minTemp = minTemp
        self.maxTemp = maxTemp
        self.realNoon = 12*3600 + self.timeShift
        self.ncTimes = [dawnTime+300, self.realNoon*0.6+self.duskTime*0.4]
        self.m = [(minTemp-maxTemp)/(86400+self.ncTimes[0]-self.ncTimes[1]), (maxTemp-minTemp)/(self.ncTimes[1]-self.ncTimes[0])]

    def generateNewVal(self, currTime, prevTemp):
        nowsec = currTime.hour * 3600 + currTime.minute * 60 + currTime.second
        midTemp = self.mid_temp(nowsec)
        errSim = random.binomial(1, 0.001)
        if prevTemp == None:
            newTemp = midTemp + 0.2*random.randn()
        else:
            newTemp = ((midTemp+prevTemp)/2.0) + 0.2*random.randn() + errSim*20

        return newTemp


    def mid_temp(self, t):
        """ ncTimes = [0, dawnTime-1800, dawnTime+300, dawnTime+1800, realNoon-3600, realNoon*1.4+duskTime*0.4, duskTime+1800, 86400]
        ncTemps = [0,0,minTemp,0,0,maxTemp,0,0]
        n = [0,0,0,0,0,0,0]
        m = [0,0,0,0,0,0,0]
        q = 0 """
        

        print("Current time: " + dt.datetime.now().strftime("%H:%M:%S"))
        # print ("Current t: " + str(t))

        if t < self.ncTimes[0]:
            temp = self.minTemp + self.m[0] * (t-self.ncTimes[0])
        elif t < self.ncTimes[1]:
            temp = self.minTemp + self.m[1] * (t-self.ncTimes[0])
        else:
            temp = self.maxTemp + self.m[0] * (t-self.ncTimes[1])

        return temp
    
class BatteryTemperatureSimulator():
    def __init__(self, running = True, initVal = None, minOutTemp=8, maxOutTemp=23):
        self.running = running
        self.outsideSimulator = OutsideTemperatureSimulator(minTemp=minOutTemp, maxTemp=maxOutTemp)
        if initVal != None:
            self.value = initVal
        elif running:
            self.value = 35 + 3 * random.randn()
        else:
            self.value = self.outsideSimulator.generateNewVal(dt.datetime.now(), None)
        

    def generateNewVal(self, currTime, prevVal = None):
        if prevVal == None:
            prevVal = self.value
        if self.running:
            mul = random.randn()
            self.value += mul*np.where(mul * (prevVal-25) > 0 and prevVal < 55, 0.1, 1)
        else:
            self.value = self.outsideSimulator.generateNewVal(currTime, prevVal)
        return self.value

    def setRunningState(self, newState):
        self.running = newState
    
class BinarySimulator():
    def __init__(self, meanDuration = 8, meanWait = 15):
        self.meanDuration = meanDuration #in number of events
        self.meanWait = meanWait
        self.value = random.binomial(1, meanDuration/(meanDuration+meanWait))
        self.prevVal = self.value
        if self.value:
            self.currStay = math.floor(max([0, self.meanDuration * (1 + random.randn()/8)]))
        else:
            self.currStay = math.floor(max([0, self.meanWait * (1 + random.randn()/8)]))
        self.presentSince = math.floor(random.rand()*self.currStay)
        print (f"Previous value: {self.prevVal}\nExpected stay: {self.currStay-self.presentSince}")
        
    
    def generateNewVal(self):
        self.presentSince += 1
        self.prevVal = self.value
        if self.meanWait == 0:
            newVal = 1
        elif self.meanDuration == 0:
            newVal = 0
        elif self.presentSince > self.currStay:
            self.presentSince = 0
            if self.value:
                self.currStay = max([1, self.meanWait * (1 + random.randn()/8)])
            else:
                self.currStay = max([1, self.meanDuration * (1 + random.randn()/8)])
            newVal = 1-self.prevVal
        else:
            newVal = self.prevVal
        self.value = newVal
        
        return newVal
    
class BatterySimulator():
    def __init__(self, initVal = None, charging = False, chargingSpeed = 0.05, dischargingSpeed = 0.1):
        if initVal != None:
            self.value = initVal
        else:
            self.value = random.uniform(0.0, 100.0)
        self.chargingSpeed = chargingSpeed
        self.dischargingSpeed = dischargingSpeed
        self.charging = charging

    def generateNewVal(self):
        if self.charging:
            self.value = min(self.value + max(self.chargingSpeed*(1 + random.randn()/5), 0), 100)
        else:
            self.value = max(self.value - max(self.dischargingSpeed*(1 + random.randn()/5), 0), 0)
        return self.value
    
    def setChargingState(self, newChargingState):
        self.charging = newChargingState

    def setChargingSpeed(self, newChargingSpeed):
        self.chargingSpeed = newChargingSpeed

    def setDischargingSpeed(self, newDischargingSpeed):
        self.dischargingSpeed = newDischargingSpeed

    def getValue(self):
        return self.value
    
class HumiditySimulator():
    def __init__(self, initVal = None, changingSpeed = 1.0):
        self.changingSpeed = changingSpeed
        if initVal != None:
            self.value = initVal
        else:
            self.value = min(max(0.0, 45.0 + 10*random.randn()), 100.0)
    
    def generateNewVal(self):
        self.value = min(max(0.0, self.value + self.changingSpeed*random.randn()/5, 0), 100.0)
        return self.value
    
    def getValue(self):
        return self.value
    
    def setChangingSpeed(self, newSpeed):
        self.changingSpeed = newSpeed


class PhotonSimulator():
    def __init__(self, initVal = None, initState = 0, trend = 0, dawnTime=6*3600+47*60, duskTime=20*3600+13*60, illumValue = 900, darkValue = 100):
        """ Trend:
        0 = (almost) constant lighting
        1 = exponential growth toward 5 V
        -1 = exponential decrease toward 0 V
        2 = linear growth
        -2 = linear decrease
        3 = \"natural\" behavior"""
        
        self.trend = trend
        self.initVal = initVal
        self.longitude = 7 + 40/60 + 32.52/3600
        self.timeShift = 3600*(1 + (15-self.longitude)/15)
        self.dawnTime = dawnTime
        self.duskTime = duskTime
        self.illumValue = illumValue
        self.darkValue = darkValue
        self.cloudyFactor = 300
        if initState != None:
            self.weatherState = initState # 0:clear 1:cloudy
        else:
            self.weatherState = random.binomial(1, 0.3)
        self.cloudCovering = self.weatherState*min((0.5+random.rand()), 0)
        self.duration = 3600*min(0.5, random.exponential(2))
        self.presentSince = math.floor(random.rand()*self.duration)
        self.realNoon = 12*3600 + self.timeShift
        self.lamp = 0
        if self.initVal != None:
            self.value = self.initVal

    
    def generateNewVal(self, currTime = None):
        if self.trend == 0:
            newVal = min(5, max(0, (self.initVal + random.randn()*5.0/1023)))
        elif self.trend == 1:
            newVal = self.value + (5-self.value)/2
        elif self.trend == -1:
            newVal = self.value/2
        elif abs(self.trend) == 2:
            newVal = max(0, min(5, self.value + self.trend*0.002) + random.randn()*5.0/1023)
        else:
            self.presentSince += 1
            if self.presentSince > self.duration:
                self.presentSince = 0
                self.duration = 3600*min(0.5, random.exponential(2))
                self.weatherState = random.binomial(1, 0.3) # Probability of cloudy weather is 0.3
            if currTime == None:
                currTime = dt.datetime.now()
            currSec = currTime.hour * 3600 + currTime.minute * 60 + currTime.second
            if currSec > self.duskTime + 3600 or currSec < self.dawnTime - 3600: # night time
                newVal = self.darkValue*(1+self.lamp) * 5.0/1023
            else: # daytime, dawn and dusk
                newBaseVal = np.where(currSec < self.realNoon,
                                    self.darkValue+(self.illumValue-self.darkValue)/(self.realNoon-self.dawnTime+3600)*(currSec-self.dawnTime+3600),
                                    self.darkValue+(self.illumValue-self.darkValue)/(self.duskTime+3600-self.realNoon)*(self.duskTime+3600-currSec)
                                    )
                newBaseVal -= self.weatherState*self.cloudyFactor*self.cloudCovering
                newVal = max(newBaseVal + random.randn(), self.darkValue)*(1+self.lamp) * 5.0 / 1023
        
        self.value = newVal
        return self.value
    
class ThreeWaySimulator():
    def __init__(self, mean0duration, mean1duration, mean2duration):
        self.durations = [float(mean0duration), float(mean1duration), float(mean2duration)]
        self.probs = [i/(mean0duration+mean1duration+mean2duration) for i in self.durations]
        self.value = int(np.where(random.multinomial(1, self.probs))[0][0])
        self.prevVal = self.value
        self.currStay = math.floor(max([0, self.durations[self.value] * (1 + random.randn()/8)]))
        self.presentSince = math.floor(random.rand()*self.currStay)
        print (f"Previous value: {self.prevVal}\nExpected stay: {self.currStay-self.presentSince}")

    def generateNewVal(self):
        self.presentSince += 1
        self.prevVal = self.value
        if self.presentSince > self.currStay:
            self.presentSince = 0
            while self.value == self.prevVal:
                self.value = int(np.where(random.multinomial(1, self.probs))[0][0])
            self.currStay = max([1, self.durations[self.value] * (1 + random.randn()/8)])
        return self.value