import time
import json
import requests

class CatalogUpdater():

    exposed = True

    def __init__(self, uri, MQTTtopic, deviceID, deviceName="", userID="1", measureType = ""):
        self.uri = uri
        self.deviceID = deviceID
        self.deviceName = deviceName
        self.userID = userID
        self.measureType = measureType
        self.updateTime = time.time()
        self.joined = False
        self.MQTTtopic = MQTTtopic

        currentDevices = self.checkCatalog()
        for item in currentDevices:
            if item["DeviceID"] == deviceID:
                self.joined = True 
        
        if not self.joined:
            self.joinCatalog()

    def joinCatalog(self):
        self.deviceDict = {
            "deviceName": self.deviceName,
            "DeviceID": self.deviceID,
            "UserAssociationID": self.userID,
            "MeasureType": self.measureType,
            "availableServices": "MQTT",
            "ServiceDetails": {
                "ServiceType": "MQTT",
                "topic": self.MQTTtopic
            },
            "status": "",
            "lastUpDate": self.updateTime
        }

        ok = 0
        while not ok:
            try:
                response = requests.post(self.uri+"/Device", json.dumps(self.deviceDict, indent=2))
                ok = response.ok
            except:
                print("Error: server unreachable.")
                time.sleep(3)
        self.joined = True

    def setUpdateTime(self, newTime):
        self.updateTime = newTime

    def generateMessage(self, value):
        self.messageAsDict = {"UserID": self.userID, "DeviceID": self.deviceID, "time": self.updateTime, "value": value}
        self.messageAsStr = json.dumps(self.messageAsDict, indent=2)
        return self.messageAsStr

    def sendMessage(self, URIarg="Device"):
        ok = 0
        while not ok:
            try:
                response = requests.put(self.uri + "/" + URIarg, self.messageAsStr)
                ok = response.ok
            except:
                print("Error: server unreachable.")

    def checkCatalog(self):
        ok = 0
        while not ok:
            ok = 1
            try:
                devices = requests.get(self.uri+"/AllDevices")
                # print(devices.content)
                return devices.json()
            except:
                print("Error: server unreachable")
                ok = 0
        
        

# For testing purposes only

if __name__ == '__main__':
    URL='http://localhost:8080'
    updater = CatalogUpdater(URL,"100", "Presence", "Battery/IoT/project/UserID/1/sensor/testing", "1")
    while True:
        updater.sendMessage()
        #requests.put(URL+"/Device",updater.generateMessage())
        updater.checkCatalog()
        time.sleep(10)
    
