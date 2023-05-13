from catalogAdapter import CatalogAdapter
from deviceSubscriber import DeviceSubscriber
import time
from thingSpeakAdapter import send_data_to_thingspeak_channel

catalog = CatalogAdapter("http://192.168.72.16:8080")
deviceList = catalog.get_devices()


clientSubID = "dataAnalysisAsSubscriber"
clientPubID = "dataAnalysisAsPublisher"
broker = "mqtt.eclipseprojects.io"
port = 1883
for i in deviceList:
    subscriber = DeviceSubscriber(clientSubID, broker, port, device=i)
    subscriber.start()
    #CONTROLLARE SE THINGSPEAK VUOLE VALORI INTERI OPPURE STRINGHE
    #subscriber.stop()
    #subscribedDevices.append(subscriber)
    time.sleep(5) #in modo tale da permettere al publisher di pubblicare
    toThingSpeak = send_data_to_thingspeak_channel(deviceList)
    break


# implementare:
# - (Da fare passo passo mentre completi i punti successivi) classe Device in modo da avere al suo interno delle
#       strutture dati che possano contenere i dati utili dei devices;
# - classe catalogAdapter che crei una lista di oggetti Device e la ritorni al chiamante
# - classe DeviceSubscriber che faccia la subscribe ai topic mqtt di ogni device e le registri su thinkspeak
# - funzioni del modulo thingSpeakAdapter per fare le chiamate a thingspeak attraverso request per creare channel, field
#       e caricare dati (??)
