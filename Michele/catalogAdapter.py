import requests
from device import Device


class CatalogAdapter:

    def __init__(self, catalog_server):  # passare IP server catalogo
        self.catalogServer = catalog_server

    def get_devices(self):  # eseguire chiamata con il modulo request per ottenere la lista dispositivi e restituirla
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
            deviceListForUser = Device(deviceID, userAssociatedID, topic, measureType) ##BISOGNA AGGIUNGERE I CHANNEL PER GLI ALTRU USERS PER THINGSPEAK e LE MISURE DAI TOPIC
            deviceList.append(deviceListForUser)
        return deviceList
        

