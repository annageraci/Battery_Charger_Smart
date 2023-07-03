from Michele.catalogAdapter import CatalogAdapter
from deviceSubscriber   import DeviceSubscriber
import time
import json


catalog = CatalogAdapter("http://192.168.72.220:8080") # Catalog Server avviato da WiFiCarlo
deviceList = catalog.get_devices()
lenDevList = len(deviceList)
Settings = json.load(open("settings.json"))
broker = Settings['broker']['IPAddress']
port = Settings['broker']['port']
clientSubID = "dataAnalysisAsSubscriber"

subscriber = DeviceSubscriber(clientSubID, broker, port, deviceList)
subscriber.start()
while True:
    #updateDeviceList(lenDevList) ## FUNZIONE DA FARE
    continue
