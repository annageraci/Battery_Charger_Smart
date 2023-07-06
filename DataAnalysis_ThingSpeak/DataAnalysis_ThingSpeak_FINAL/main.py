from catalogAdapter import CatalogAdapter
from deviceSubscriber import DeviceSubscriber
import json
import time

def startDataAnalysis_Thingspeak(Settings, deviceList, firstRun, changed):
    broker = Settings['broker']['IPAddress']
    port = Settings['broker']['port']
    clientSubID = "dataAnalysisAsSubscriber"
    subscriber = DeviceSubscriber(clientSubID, broker, port, deviceList)
    if firstRun:
        subscriber.start()
    elif changed:
        subscriber.stop()
        subscriber.start()



def comparisonLists(deviceList_init, deviceList_check, Settings, firstRun):
    if firstRun:
            changed = False
            startDataAnalysis_Thingspeak(Settings, deviceList_init, firstRun, changed)
            firstRun = False
    else:
        firstItem = True
        equalThingSpeak = False
        equalDeviceID = False
        for item_check in deviceList_check:
            changed = False
            isPresent = False
            for item in deviceList_init:
                if changed or isPresent:
                    break
                if item_check.channel == item.channel:
                    equalThingSpeak = True
                    if item_check.deviceID == item.deviceID:
                        equalDeviceID = True
                        isPresent = True
                    else:
                        equalDeviceID = False
                        isPresent = False
                else:
                    equalThingSpeak = False
                    isPresent = False
            if not equalDeviceID and not equalThingSpeak and firstItem:
                firstItem = False
                changed = True
                startDataAnalysis_Thingspeak(Settings, deviceList_check, firstRun, changed)
                print("DeviceList has changed due to the first item")

            elif not equalDeviceID and not equalThingSpeak and not isPresent:
                changed = True
                startDataAnalysis_Thingspeak(Settings, deviceList_check, firstRun, changed)
                print("DeviceList has changed")
            else:
                startDataAnalysis_Thingspeak(Settings, deviceList_check, firstRun, changed)
            




if __name__ == "__main__":
    firstRun = True
    changed  = False
    Settings = json.load(open("settings.json"))
    catalog = CatalogAdapter(Settings["Catalog_url_Carlo"])
    deviceList_init = catalog.get_devices()
    while True:
        if firstRun:
            startDataAnalysis_Thingspeak(Settings, deviceList_init, firstRun, changed)
            firstRun = False
        else:
            time.sleep(10)
            deviceList_check = catalog.get_devices()
            if len(deviceList_init) == len(deviceList_check):
                comparisonLists(deviceList_init, deviceList_check, Settings, firstRun)
                deviceList_init = list(deviceList_check)
            else:
                changed = True
                startDataAnalysis_Thingspeak(Settings, deviceList_check, firstRun, changed)
                deviceList_init = list(deviceList_check)
        continue
