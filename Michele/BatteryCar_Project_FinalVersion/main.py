from catalogAdapter import CatalogAdapter
from deviceSubscriber   import DeviceSubscriber
import json

def startDataAnalysis_Thingspeak():
    Settings = json.load(open("settings.json"))
    catalog = CatalogAdapter(Settings["Catalog_url_Carlo"])
    deviceList = catalog.get_devices()
    broker = Settings['broker']['IPAddress']
    port = Settings['broker']['port']
    clientSubID = "dataAnalysisAsSubscriber"

    subscriber = DeviceSubscriber(clientSubID, broker, port, deviceList)
    subscriber.start()

if __name__ == "__main__":
    counter = 0
    while True:
        if counter== 25000000 or counter==0:
            counter=0
            startDataAnalysis_Thingspeak()
        counter += 1
        continue
