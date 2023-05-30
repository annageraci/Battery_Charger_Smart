# import thingSpeakAdapter
import json

class Device:
    def __init__(self, deviceID, userAssociationID, topic, measureType): #bisogna aggiungere il value
        self.topic = topic
        self.userAssociationID = userAssociationID
        self.deviceID = deviceID
        self.value = -1
        self.channel = -1
        self.field = -1

        if userAssociationID == "1":
            self.channel = "EUWUGU3WMLEZ6U88" # User1
            #self.channel =  "GE6I54M68UHJM19B" ESEMPIO
        elif userAssociationID == "2":
            self.channel = "YBW43BVJKR1G742E"
        elif userAssociationID == "4":
            self.channel = "TILVO0S7Z1LN2FPN"

        if measureType == "Temperature":
            self.field = "field1"
        elif measureType == "Photoni":
            self.field = "field2"
        elif measureType == "Percentage": # Percentage of Battery
            self.field = "field3"

        self.check_errors = self.checkErrors # to check if an user do not have a ThingSpeak channel

    def checkErrors(self):
        if self.channel == -1:
            print("UserID: %s does not have a ThingSpeak channel" %(self.userAssociationID))
        elif self.field == -1:
            print("Problems with energy attributes of the UserID: %s" % (self.userAssociationID))


