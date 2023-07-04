import paho.mqtt.client as PahoMQTT
import json
from thingSpeakAdapter import send_data_to_thingspeak_channel


class DeviceSubscriber:
    def __init__(self, clientID, broker, port, deviceList):
        self.deviceList = deviceList
        self.clientID = clientID
        self._paho_mqtt = PahoMQTT.Client(clientID, True)
        self.messageBroker = broker
        self.port = port
        self._paho_mqtt.on_connect = self.myOnConnect
        self._paho_mqtt.on_message = self.myOnMessageReceived


    def start(self):
        # manage connection to broker
        self._paho_mqtt.connect(self.messageBroker, self.port)
        self._paho_mqtt.loop_start()
        # subscribe to the different topics for the different devices
        for item in self.deviceList:
            self._paho_mqtt.subscribe(item.topic, 2)
            print(f'Subscribed to the topic: {item.topic}')

    def stop(self):
        for device in self.deviceList:
            self._paho_mqtt.unsubscribe(device.topic)
            self._paho_mqtt.loop_stop()
            self._paho_mqtt.disconnect()
            print(f"Device ID {device.deviceID} unsubscribed")

    def myOnConnect(self, paho_mqtt, userdata, flags, rc):
        pass

    def myOnMessageReceived(self, paho_mqtt, userdata, msg):
        # A new message is received
        for device in self.deviceList: 
            if msg.topic==device.topic:
                received_msg = json.loads(msg.payload)
                device.value = received_msg["e"][0]["v"] # to read data provided by the sensors
                if device.channel == -1: #to check the presence of a thingSpeak channel for the User
                    continue
                send_data_to_thingspeak_channel(device)

