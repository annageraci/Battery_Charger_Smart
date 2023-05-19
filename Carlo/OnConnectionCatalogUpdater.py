import cherrypy
import time
import json
import requests

class CatalogUpdater():

    exposed = True

    def __init__(self, uri, MQTTtopic, deviceID, deviceName="", userID="1"):
        self.uri = uri
        self.deviceID = deviceID
        self.deviceName = deviceName
        self.userID = userID
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
            "MeasureType": "",
            "availableServices": "MQTT",
            "ServiceDetails": {
                "ServiceType": "MQTT",
                "topic": self.MQTTtopic
            },
            "status": "",
            "lastUpDate": self.updateTime
        }
        requests.post(self.uri+"/Device", json.dumps(self.deviceDict, indent=2))
        self.joined = True

    def setUpdateTime(self, newTime):
        self.updateTime = newTime

    def generateMessage(self, value):
        self.messageAsDict = {"DeviceID": self.deviceID, "time": self.updateTime, "value": value}
        self.messageAsStr = json.dumps(self.messageAsDict, indent=2)
        return self.messageAsStr

    def sendMessage(self, URIarg="Device"):
        requests.put(self.uri + "/" + URIarg, self.generateMessage())
    
    def checkCatalog(self):
        devices = requests.get(self.uri+"/AllDevices")
        return devices.json()

# For testing purposes only

if __name__ == '__main__':
    URL='http://localhost:8080'
    updater = CatalogUpdater(URL,"100", "Presence", "Battery/IoT/project/UserID/1/sensor/testing", "1")
    while True:
        updater.sendMessage()
        #requests.put(URL+"/Device",updater.generateMessage())
        updater.checkCatalog()
        time.sleep(10)
    
