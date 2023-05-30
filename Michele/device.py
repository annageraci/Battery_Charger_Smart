# import thingSpeakAdapter
import json

class Device:
    def __init__(self, deviceID, userAssociationID, topic, measureType): #bisogna aggiungere il value
<<<<<<< HEAD
=======
        #self.thingspeak_coordinates = {}
>>>>>>> 6d9f3d1beed4933f11b8b16b5082e38f0aedff36
        self.topic = topic
        self.userAssociationID = userAssociationID
        self.deviceID = deviceID
        self.value = -1
        self.channel = -1
        self.field = -1

        if userAssociationID == "1":
<<<<<<< HEAD
            self.channel = "EUWUGU3WMLEZ6U88" # User1
=======
            self.channel = "EUWUGU3WMLEZ6U88" #User1
>>>>>>> 6d9f3d1beed4933f11b8b16b5082e38f0aedff36
            #self.channel =  "GE6I54M68UHJM19B" ESEMPIO
        elif userAssociationID == "2":
            self.channel = "YBW43BVJKR1G742E"
        elif userAssociationID == "4":
            self.channel = "TILVO0S7Z1LN2FPN"

        if measureType == "Temperature":
            self.field = "field1"
        elif measureType == "Photoni":
            self.field = "field2"
<<<<<<< HEAD
        elif measureType == "Percentage": # Percentage of Battery
            self.field = "field3"

        self.check_errors = self.checkErrors # to check if an user do not have a ThingSpeak channel
=======
        elif measureType == "Percentage": #livello batteria
            self.field = "field3"

        self.check_errors = self.checkErrors

        # self.devicesForUser = {
        #     "UserID": self.userAssociationID,
        #     "DeviceID": self.deviceID,
        #     "Topic": self.topic,
        #     "ChannelID": self.channel,
        #     "Field": self.field,
        #     "Value": self.value
        # }
>>>>>>> 6d9f3d1beed4933f11b8b16b5082e38f0aedff36

    def checkErrors(self):
        if self.channel == -1:
            print("UserID: %s does not have a ThingSpeak channel" %(self.userAssociationID))
        elif self.field == -1:
            print("Problems with energy attributes of the UserID: %s" % (self.userAssociationID))

<<<<<<< HEAD
=======
    def register_thingspeak(self):
        #self.thingspeak_coordinates = thingSpeakAdapter.register(self.deviceID, ...)
        pass
>>>>>>> 6d9f3d1beed4933f11b8b16b5082e38f0aedff36

