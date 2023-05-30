import paho.mqtt.client as PahoMQTT
import json
from thingSpeakAdapter import send_data_to_thingspeak_channel


class DeviceSubscriber:
    def __init__(self, clientID, broker, port, deviceList):  # passare dati necessari a mqtt
        self.deviceList = deviceList
        #self.device.register_thingspeak()
        #mqtt.subscribe(device.mqttURL, callback = callback())

        self.clientID = clientID
        self._paho_mqtt = PahoMQTT.Client(clientID, True) #True è la duration: si riconnette automaticamente se non legge il messaggio
        self.messageBroker = broker
        self.port = port
        self._paho_mqtt.on_connect = self.myOnConnect
        self._paho_mqtt.on_message = self.myOnMessageReceived


    def start(self):
        # manage connection to broker
        self._paho_mqtt.connect(self.messageBroker, self.port)
        self._paho_mqtt.loop_start()
        # subscribe for a topic
        for item in self.deviceList:
            self._paho_mqtt.subscribe(item.topic, 2)
            print(f'Subscribed to the topic: {item.topic}')

    def stop(self):
        # da fare prima di disconnettersi
        self._paho_mqtt.unsubscribe(self.topic)
        self._paho_mqtt.loop_stop()
        self._paho_mqtt.disconnect()

    def myOnConnect(self, paho_mqtt, userdata, flags, rc):
        pass
        #print("DataAnalysis as SUBSCRIBER connected to %s at the topic %s with result code: %d" % (self.messageBroker, self.topic,rc))  # rc = Return Code. Se rc = 0 no errori

    def myOnMessageReceived(self, paho_mqtt, userdata, msg):
        # A new message is received
        for device in self.deviceList: 
            if msg.topic==device.topic:
                print(msg.payload)
                print(msg.topic)
                received_msg = json.loads(msg.payload)
                device.value = received_msg["e"][0]["v"]
                send_data_to_thingspeak_channel(device)
        



