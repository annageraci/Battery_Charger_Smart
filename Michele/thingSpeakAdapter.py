import requests

def send_data_to_thingspeak_channel(device):
        requests.post("https://api.thingspeak.com/update.json", json={"api_key": device.channel, device.field: device.value})
        print("Information of the UserID %s about DeviceID %s was send" % (device.userAssociationID, device.deviceID))
