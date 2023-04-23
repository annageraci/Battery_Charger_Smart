import datetime as dt
import numpy as np
import math

class DawnDuskTime():
    def __init__(self, lat, long, date=dt.date.today()):
        self.year = date.year
        self.month = date.month
        self.day = date.day
        self.astroYear = self.year + int(self.month == 12 and self.day >= 22)
        self.leapYear = int((self.year % 4 == 0) and not(self.year % 400 == 0))
        self.leapAstroYear = int((self.astroYear % 4 == 0) and not(self.astroYear % 400 == 0))
        self.yearDuration = 365 + self.leapYear
        self.dayOfYear = self.dateToDay()
        self.astroDay = (self.dayOfYear+10) % self.yearDuration
        self.axisTilt = 23.0+27/60
        self.apparentAxisTilt = self.evalAxisTilt()
        print(self.apparentAxisTilt)
        self.long = long
        self.lat = lat
        #print (date)
        #print (self.year, self.leapYear, self.astroYear, self.leapAstroYear)
        #print (self.dayOfYear, self.astroDay)
        self.dawnTime, self.duskTime = self.evalTimes()

    def getDawnTimeSec(self):
        return int(self.dawnTime*3600)
    
    def getDuskTimeSec(self):
        return int(self.duskTime*3600)


    def dateToDay(self):
        monthOneHot = np.zeros((1,12))
        monthOneHot[0, self.month-1] = 1
        gapDays = np.array([-self.leapYear, 1-self.leapYear, -1, 0, 0, 1, 1, 2, 3, 3, 4, 4]).T + self.leapYear
        #print(int(np.dot(monthOneHot, gapDays)))
        return int(np.dot(monthOneHot, gapDays) + 30*(self.month-1) + self.day)
    
    def evalAxisTilt(self):
        springEquinoxDay = 89 + self.leapAstroYear # March 20
        summerSolsticeDay = 182 + self.leapAstroYear # June 21
        autumnEquinoxDay = 276 + self.leapAstroYear # September 23
        winterSolsticeDay = 365 + self.leapAstroYear # December 21

        if self.astroDay <= springEquinoxDay:
            return -self.axisTilt*(1.0-float(self.astroDay)/springEquinoxDay)
        elif self.astroDay <= summerSolsticeDay:
            return self.axisTilt*(self.astroDay-springEquinoxDay)/(summerSolsticeDay-springEquinoxDay)
        elif self.astroDay <= autumnEquinoxDay:
            return self.axisTilt*(1.0-float(self.astroDay-summerSolsticeDay)/(autumnEquinoxDay-summerSolsticeDay))
        else:
            return -self.axisTilt*(self.astroDay-autumnEquinoxDay)/(winterSolsticeDay-autumnEquinoxDay)
        

    def evalTimes(self):
        middayTime = 12.0 + ((15-self.long)%15.0)/15
        acosArg = -math.tan(self.apparentAxisTilt*math.pi/180)*math.tan(self.lat*math.pi/180)
        if acosArg > 1:
            deltaPhi = 0
        elif acosArg < -1:
            deltaPhi = 180
        else:
            deltaPhi = math.acos(acosArg)*180/math.pi
        deltaHours = deltaPhi/15
        print(deltaHours)
        return (middayTime-deltaHours, middayTime+deltaHours)
    
    