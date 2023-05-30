import paho.mqtt.client as PahoMQTT
import json
from thingSpeakAdapter import send_data_to_thingspeak_channel


class DeviceSubscriber:
<<<<<<< HEAD
    def __init__(self, clientID, broker, port, deviceList):
        self.deviceList = deviceList
        self.clientID = clientID
        self._paho_mqtt = PahoMQTT.Client(clientID, True)
=======
    def __init__(self, clientID, broker, port, deviceList):  # passare dati necessari a mqtt
        self.deviceList = deviceList
        #self.device.register_thingspeak()
        #mqtt.subscribe(device.mqttURL, callback = callback())

        self.clientID = clientID
        self._paho_mqtt = PahoMQTT.Client(clientID, True) #True è la duration: si riconnette automaticamente se non legge il messaggio
>>>>>>> 6d9f3d1beed4933f11b8b16b5082e38f0aedff36
        self.messageBroker = broker
        self.port = port
        self._paho_mqtt.on_connect = self.myOnConnect
        self._paho_mqtt.on_message = self.myOnMessageReceived
<<<<<<< HEAD
        self.photonThreshold = 3.5
=======
>>>>>>> 6d9f3d1beed4933f11b8b16b5082e38f0aedff36


    def start(self):
        # manage connection to broker
        self._paho_mqtt.connect(self.messageBroker, self.port)
        self._paho_mqtt.loop_start()
<<<<<<< HEAD
        # subscribe to the different topics for the different devices
=======
        # subscribe for a topic
>>>>>>> 6d9f3d1beed4933f11b8b16b5082e38f0aedff36
        for item in self.deviceList:
            self._paho_mqtt.subscribe(item.topic, 2)
            print(f'Subscribed to the topic: {item.topic}')

    def stop(self):
<<<<<<< HEAD
=======
        # da fare prima di disconnettersi
>>>>>>> 6d9f3d1beed4933f11b8b16b5082e38f0aedff36
        self._paho_mqtt.unsubscribe(self.topic)
        self._paho_mqtt.loop_stop()
        self._paho_mqtt.disconnect()

    def myOnConnect(self, paho_mqtt, userdata, flags, rc):
        pass
<<<<<<< HEAD
=======
        #print("DataAnalysis as SUBSCRIBER connected to %s at the topic %s with result code: %d" % (self.messageBroker, self.topic,rc))  # rc = Return Code. Se rc = 0 no errori
>>>>>>> 6d9f3d1beed4933f11b8b16b5082e38f0aedff36

    def myOnMessageReceived(self, paho_mqtt, userdata, msg):
        # A new message is received
        for device in self.deviceList: 
            if msg.topic==device.topic:
<<<<<<< HEAD
                received_msg = json.loads(msg.payload)
                device.value = received_msg["e"][0]["v"] # to read data provided by the sensors
                if msg.topic == "Battery/IoT/project/UserID/+/sensor/photon" :
                    if device.value < self.photonThreshold:
                        device.value = 0    #it means that we are not using renewable energy
                    else: device.value = 1  #it means that we are using renewable energy
                send_data_to_thingspeak_channel(device)
=======
                print(msg.payload)
                print(msg.topic)
                received_msg = json.loads(msg.payload)
                device.value = received_msg["e"][0]["v"]
                send_data_to_thingspeak_channel(device)
        


>>>>>>> 6d9f3d1beed4933f11b8b16b5082e38f0aedff36

