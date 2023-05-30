from catalogAdapter import CatalogAdapter
<<<<<<< HEAD
from deviceSubscriber   import DeviceSubscriber
import time
import json

catalog = CatalogAdapter("http://172.25.224.1:8080") # Catalog Server avviato da Anna (pc-lavoro)
=======
from deviceSubscriber  import DeviceSubscriber
import time
import json

catalog = CatalogAdapter("http://172.25.224.1:8080") #avviato da Carlo (hot-spot)
>>>>>>> 6d9f3d1beed4933f11b8b16b5082e38f0aedff36
deviceList = catalog.get_devices()

Settings=json.load(open("../settings.json"))

broker=Settings['broker']['IPAddress']
clientSubID = "dataAnalysisAsSubscriber"
<<<<<<< HEAD
port = 1883
=======
port =['broker']['port']
>>>>>>> 6d9f3d1beed4933f11b8b16b5082e38f0aedff36
    

subscriber = DeviceSubscriber(clientSubID, broker, port, deviceList)
subscriber.start()
<<<<<<< HEAD
time.sleep(5) #in modo tale da permettere al publisher di pubblicare. DA CONTROLLARE

while True:
    continue
=======
#CONTROLLARE SE THINGSPEAK VUOLE VALORI INTERI OPPURE STRINGHE
#subscriber.stop()
#subscribedDevices.append(subscriber)
time.sleep(5) #in modo tale da permettere al publisher di pubblicare
while True:
    continue



# implementare:
# - (Da fare passo passo mentre completi i punti successivi) classe Device in modo da avere al suo interno delle
#       strutture dati che possano contenere i dati utili dei devices;
# - classe catalogAdapter che crei una lista di oggetti Device e la ritorni al chiamante
# - classe DeviceSubscriber che faccia la subscribe ai topic mqtt di ogni device e le registri su thinkspeak
# - funzioni del modulo thingSpeakAdapter per fare le chiamate a thingspeak attraverso request per creare channel, field
#       e caricare dati (??)
>>>>>>> 6d9f3d1beed4933f11b8b16b5082e38f0aedff36
