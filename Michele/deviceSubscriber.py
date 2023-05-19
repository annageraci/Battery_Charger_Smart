import paho.mqtt.client as PahoMQTT
import json
from thingSpeakAdapter import send_data_to_thingspeak_channel


class DeviceSubscriber:
    def __init__(self, clientID, broker, port, device):  # passare dati necessari a mqtt
        self.device = device
        #self.device.register_thingspeak()
        #mqtt.subscribe(device.mqttURL, callback = callback())

        self.clientID = clientID
        self._paho_mqtt = PahoMQTT.Client(clientID, True) #True è la duration: si riconnette automaticamente se non legge il messaggio
        self.topic = device.topic
        self.messageBroker = broker
        self.value = device.value
        self.port = port
        self._paho_mqtt.subscribe(self.topic, 2)
        self._paho_mqtt.on_connect = self.myOnConnect
        self._paho_mqtt.on_message = self.myOnMessageReceived


    def start(self):
        # manage connection to broker
        self._paho_mqtt.connect(self.messageBroker, self.port)
        self._paho_mqtt.loop_start()
        # subscribe for a topic
        self._paho_mqtt.subscribe(self.topic, 2)

    def stop(self):
        # da fare prima di disconnettersi
        self._paho_mqtt.unsubscribe(self.topic)
        self._paho_mqtt.loop_stop()
        self._paho_mqtt.disconnect()

    def myOnConnect(self, paho_mqtt, userdata, flags, rc):
        print("DataAnalysis as SUBSCRIBER connected to %s at the topic %s with result code: %d" % (self.messageBroker, self.topic,rc))  # rc = Return Code. Se rc = 0 no errori

    def myOnMessageReceived(self, paho_mqtt, userdata, msg):
        # A new message is received
        print(msg)
        received_msg = json.loads(msg)["e"][0]["v"]

        self.device.value = received_msg
        send_data_to_thingspeak_channel(self.device)
        return



