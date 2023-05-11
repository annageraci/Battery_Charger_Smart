import requests

def send_data_to_thingspeak_channel(deviceList):
    for i in deviceList:
        requests.post("https://api.thingspeak.com/update.json", json={"api_key": i.channel, i.field: i.value})
        print("Information of the UserID %s about DeviceID %s was send" % (i.userAssociationID, i.deviceID))
        break
