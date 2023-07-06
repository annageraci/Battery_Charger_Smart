import cherrypy
import requests
from device import Device

class CatalogAdapter:

    def __init__(self, catalog_server):  # To pass the serverIP of the catalog
        self.catalogServer = catalog_server

    def get_devices(self): # used to select only the useful information
        json_devices = requests.get(self.catalogServer+"/AllDevices").json()
        json_users = requests.get(self.catalogServer+"/AllUsers").json()
        deviceList = []
        deviceAllowList = ["TemperatureB", "Voltage", "Percentage"]
        userVector = []
        for user in json_users:
             userVector.append({"ThingSpeakChannel": user["ThingSpeakKey"]["APIKeyWrite"], "userID": user["UserID"]})
        for item in json_devices:
            if item["MeasureType"] not in deviceAllowList:
                continue
            deviceID = item["DeviceID"]
            userAssociatedID = item["UserAssociationID"]
            topic = item["ServiceDetails"]["topic"]
            measureType = item["MeasureType"]
            for user in userVector:
                if user["userID"] == userAssociatedID:
                    channel = user["ThingSpeakChannel"]
                    deviceListForUser = Device(deviceID, userAssociatedID, topic, measureType, channel)
                    deviceList.append(deviceListForUser)
        return deviceList


