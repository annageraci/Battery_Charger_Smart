import json
import time
import paho.mqtt.client as PahoMQTT

class DeviceSubscriber:
    def __init__(self, clientID, broker, port, topic, value):  # passare dati necessari a mqtt
        #self.device.register_thingspeak()
        #mqtt.subscribe(device.mqttURL, callback = callback())

        self.clientID = clientID
        self._paho_mqtt = PahoMQTT.Client(clientID, True)
        self.topic = topic
        self.value = value
        self.messageBroker = broker
        self.port = port
        self._paho_mqtt.on_connect = self.myOnConnect
        self._paho_mqtt.on_message = self.myOnMessageReceived

    # definire callback()

    # def callback():
        # ...
        # thingspeak.send_data_to_thingspeak_channel(self.device.thingspeak_coordinates, data)
        # ...

    def mock_input(self):  # call callback function with fake data
        pass

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
        print("DataAnalysis as SUBSCRIBER connected to %s with result code: %d" % (self.messageBroker, rc))  # rc = Return Code. Se rc = 0 no errori

    def myOnMessageReceived(self, paho_mqtt, userdata, msg):
        # A new message is received
        received_msg = json.loads(msg.payload)
        print(received_msg)
        self.value = received_msg
        return

if __name__ == "__main__":
    clientID = "Sub-sss"
    topic = "Battery/IoT/project/UserID/1/sensor/temperature"
    port = 1883
    value = -1
    broker = "mqtt.eclipseprojects.io"
    subscriber = DeviceSubscriber(clientID, broker, port, topic, value)
    subscriber.start()

    a = 0
    while (a < 300):
        a += 1
        time.sleep(1)

    subscriber.stop()