import requests
from device import Device


class CatalogAdapter:

    def __init__(self, catalog_server):  # To pass the serverIP of the catalog
        self.catalogServer = catalog_server

    def get_devices(self): # used to select only the useful information
        json_devices = requests.get(self.catalogServer+"/AllDevices").json()
        deviceList = []
        deviceAllowList = ["Temperature_Sensor", "Photon_Sensor", "Battery_Detector", "MeasureType"]
        for item in json_devices:
            if item["deviceName"] not in deviceAllowList:
                continue
            deviceID = item['DeviceID']
            userAssociatedID = item['UserAssociationID']
            topic = item["ServiceDetails"]["topic"]
            measureType = item["MeasureType"]
            deviceListForUser = Device(deviceID, userAssociatedID, topic, measureType)
            deviceList.append(deviceListForUser)
        return deviceList
