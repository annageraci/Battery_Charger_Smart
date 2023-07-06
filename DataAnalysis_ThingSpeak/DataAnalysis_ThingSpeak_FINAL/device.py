# import thingSpeakAdapter
import json

class Device:
    def __init__(self, deviceID, userAssociationID, topic, measureType, channel): #bisogna aggiungere il value
        self.topic = topic
        self.userAssociationID = userAssociationID
        self.deviceID = deviceID
        self.measureType = measureType
        self.value = -1
        self.channel = channel
        self.field = -1

        if self.measureType == "TemperatureB": # Battery temperature
            self.field = "field1"
        elif self.measureType == "Voltage": # Photon Voltage
            self.field = "field2"
        elif self.measureType == "Percentage": # Percentage of Battery
            self.field = "field3"

        self.check_errors = self.checkErrors # to check if an user do not have a ThingSpeak channel

    def checkErrors(self):
        if self.channel == -1:
            print("UserID: %s does not have a ThingSpeak channel" %(self.userAssociationID))
        elif self.field == -1:
            print("Problems with energy attributes for the UserID: %s" % (self.userAssociationID))