import requests

<<<<<<< HEAD
def send_data_to_thingspeak_channel(device): # To send measurements to Thingspeak
=======
def send_data_to_thingspeak_channel(device):
>>>>>>> 6d9f3d1beed4933f11b8b16b5082e38f0aedff36
        requests.post("https://api.thingspeak.com/update.json", json={"api_key": device.channel, device.field: device.value})
        print("Information of the UserID %s about DeviceID %s was send" % (device.userAssociationID, device.deviceID))
