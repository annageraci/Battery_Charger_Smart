from numpy import random
import datetime as dt
import math

class TemperatureSimulator():

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
    
class PresenceSimulator():
    def __init__(self, meanDuration = 8, meanWait = 15):
        self.meanDuration = meanDuration #in number of events
        self.meanWait = meanWait
        self.value = random.binomial(1, meanDuration/meanWait)
        if self.value:
            self.currStay = math.floor(max([0, self.meanDuration * (1 + random.randn()/8)]))
        else:
            self.currStay = math.floor(max([0, self.meanWait * (1 + random.randn()/8)]))
        self.presentSince = math.floor(random.rand()*self.currStay)
        print (f"Previous value: {self.prevVal}\nExpected stay: {self.currStay-self.presentSince}")
        
    
    def generateNewVal(self):
        self.presentSince += 1
        if self.presentSince > self.currStay:
            self.presentSince = 0
            if self.value:
                self.currStay = max([1, self.meanWait * (1 + random.randn()/8)])
            else:
                self.currStay = max([1, self.meanDuration * (1 + random.randn()/8)])
            newVal = 1-self.prevVal
        else:
            newVal = self.prevVal
        
        self.prevVal = newVal
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
    

