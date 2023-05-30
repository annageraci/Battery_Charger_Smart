from catalogAdapter import CatalogAdapter
from deviceSubscriber   import DeviceSubscriber
import time
import json

catalog = CatalogAdapter("http://172.25.224.1:8080") # Catalog Server avviato da Anna (pc-lavoro)
deviceList = catalog.get_devices()

Settings=json.load(open("../settings.json"))

broker=Settings['broker']['IPAddress']
clientSubID = "dataAnalysisAsSubscriber"
port = 1883
    

subscriber = DeviceSubscriber(clientSubID, broker, port, deviceList)
subscriber.start()
time.sleep(5) #in modo tale da permettere al publisher di pubblicare. DA CONTROLLARE

while True:
    continue
