import time
from Simulators import ThreeWaySimulator
from Publishers import *
import json

if __name__ == "__main__":
    settings_file_path = 'settings.json'

    settingsFile = open(settings_file_path)
    settingsDict = json.load(settingsFile)
    settingsFile.close()
    baseTopic = settingsDict["baseTopic"]
    
    userAssociationID = "1"
    topic = baseTopic + userAssociationID + "/manualFlag"
    deviceName = "SwitchSimulator1"
    simulator = ThreeWaySimulator(0, 15, 5)


    broker = settingsDict["broker"]["IPAddress"]
    port = settingsDict["broker"]["port"]
    publisher = ManualFlagPublisher("csim48rPiManualFlag", userAssociationID, broker, port, topic)
    publisher.startOperation()

    while True:
        payload = json.dumps({"bn": "manualFlag"+userAssociationID, "e": [{"n": "manualFlag", "u": "", "t": time.time(), "v": simulator.generateNewVal()}]})
        publisher.mf_publish(topic, payload, 2)
        time.sleep(5)