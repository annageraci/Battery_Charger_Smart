import requests

def send_data_to_thingspeak_channel(device): # To send measurements to Thingspeak
        requests.post("https://api.thingspeak.com/update.json", json={"api_key": device.channel, device.field: device.value})
        print("Information of the UserID %s about %s = %s was send. Channel: %s" % (device.userAssociationID, device.measureType, device.value, device.channel))
