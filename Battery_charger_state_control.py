import paho.mqtt.client as PahoMQTT
import json
from MyMQTT import *
import time
import cherrypy
import requests

class Controller:
    def __init__(self,clientID,broker, base_topic, topic_temp, topic_battery, topic_presence, topic_photon,topic_daily, Catalog):
        self.clientID=clientID
        self.broker=broker
        self.base_topic=base_topic
        self.topic_temp=topic_temp
        self.topic_battery=topic_battery
        self.topic_presence=topic_presence
        self.topic_photon=topic_photon
        self.topic_daily=topic_daily
        # the notifier is the Sensor itself
        self.Catalog=Catalog,
        self.CatalogUser_json= Catalog['UserList']
        self.NumberofUser=len(self.CatalogUser_json)
        print(f'the number of the user is {self.NumberofUser}')
        self.client=MyMQTT(self.clientID,self.broker,1883,self)
        
        # initialize the value of the measurement pick from the sensor
        self.temperature=[-1]*self.NumberofUser
        self.battery_percentage=[-1]*self.NumberofUser
        self.digital_button=[-1]*self.NumberofUser
        self.photon=[-1]*self.NumberofUser
        self.actuator_command=[-1]*self.NumberofUser
        self.daily=[-1]*self.NumberofUser

        # initialize the topic of the message send by the sensor        
        self.topic_temp_completed=[]
        self.topic_photon_completed=[]
        self.topic_presence_completed=[]
        self.topic_battery_completed=[]
        self.topic_daily_completed=[]

    def StartOperation(self):
        self.client.start() #connect to the broker and start the loop
        time.sleep(6) # asyncronous so we want exaclty ordered
        for i in range(self.NumberofUser):
            UserID=int(self.CatalogUser_json[i]['UserID'])
            self.topic_temp_completed.insert(i,self.base_topic +str(UserID)+ self.topic_temp)       
            self.client.mySubscribe(self.topic_temp_completed[i])
            self.topic_photon_completed.insert(i,self.base_topic +str(UserID)+ self.topic_photon) 
            self.client.mySubscribe(self.topic_photon_completed[i])
            self.topic_presence_completed.insert(i,self.base_topic +str(UserID)+ self.topic_presence) 
            self.client.mySubscribe(self.topic_presence_completed[i])
            self.topic_battery_completed.insert(i,self.base_topic +str(UserID)+ self.topic_battery) 
            self.client.mySubscribe(self.topic_battery_completed[i])
            self.topic_daily_completed.insert(i,self.base_topic +str(UserID)+ self.topic_daily)
            self.client.mySubscribe(self.topic_daily_completed[i])

    def notify(self,topic,msg):
        for i in range(self.NumberofUser):
            UserID=int(self.CatalogUser_json[i]['UserID'])
            if topic==self.topic_temp_completed[i]:
                payload=json.loads(msg)
                self.temperature[i]=payload['e'][0]['v']
                print(f'the value of the temperature sensor of the UserID {UserID} is {self.temperature[i]}')
            elif topic==self.topic_battery_completed[i]:
                payload=json.loads(msg)
                self.battery_percentage[i]=payload['e'][0]['v']
                print(f'the value of the percentage of the battery of the UserID {UserID} is {self.battery_percentage[i]}')
            elif topic==self.topic_presence_completed[i]:
                payload=json.loads(msg)
                self.digital_button[i]=payload['e'][0]['v']
                print(f'the value of the presence of the vehicle of the UserID {UserID} is {self.digital_button[i]}')
            elif topic==self.topic_photon_completed[i]:
                payload=json.loads(msg)
                self.photon[i]=payload['e'][0]['v']
                print(f'the value of the energy of the photon of the UserID {UserID} is {self.photon[i]}')
            elif topic==self.topic_daily_completed[i]:
                payload=json.loads(msg)
                self.daily[i]=payload['e'][0]['v']
                print(f'the value of the battery percentage usage today by the userID {UserID} will be {self.daily[i]}')
    
    def control_strategy(self):
        soglia_photon=1.1 # eV energy of the photon 
        for i in range(self.NumberofUser):
            UserID=self.CatalogUser_json[i]['UserID']
            # 1° step car in garage?
            if (self.digital_button[i]==0):
                print('The vehicle is not present in the garage')
                self.actuator_command.insert(i,0)
            else:
                # 2* step ha i pannelli fotovoltaici? c'è il sole?
                if self.photon[i]>=soglia_photon and self.photon[i]!=-1:
                    # self.photon=-1 means no solar pannel 
                    print(f'Solar panel produce enough energy, energy: {self.photon[i]}')
                    self.actuator_command.insert(i,1)
                else:
                    # 3° step check aria condizionata o riscaldamento (temperatura) 
                    daily_appointment=int(self.daily[i]) #%battery usage in this day
                    soglia_Htemperature=20 # more than 20° aria condizionata
                    soglia_Ltemperature=10 # less than 10° aria calda
                    if ((self.temperature[i]>soglia_Htemperature or self.temperature[i]<soglia_Ltemperature) and self.temperature[i]!=-1):
                        print(f'Could be necessary switch on the conditioning, temp: {self.temperature[i]}')
                        daily_appointment=daily_appointment+0.2*daily_appointment #maggiorazione del 20%
                    # 4° step % batteria è sufficiente
                    if (daily_appointment>100):
                        print('probably you have to charge the car during the usage in another charge station')
                    if (self.battery_percentage[i]>daily_appointment and int(daily_appointment)!=-1):
                        print(f'percentage of battery sufficient, more than {daily_appointment}')
                        self.actuator_command.insert(i,0)
                    elif (daily_appointment!=-1):
                        print(f'percentage of battery insufficient, less than {daily_appointment}')
                        self.actuator_command.insert(i,1)
                if (self.actuator_command[i]==-1):
                    print('last_chance')
                    self.actuator_command.insert(i,0)            
            topic=self.base_topic+UserID+'/actuator'
            print(f'{topic} Published {self.actuator_command[i]}')
            self.client.myPublish(topic, self.actuator_command[i])
            dict_to_post={"UserID": UserID,"value": int(self.actuator_command[i])}
            urlToPut=self.Catalog['DockerIP']+'/Actuator'
            response = requests.put(urlToPut, json.dumps(dict_to_post))
            print(dict_to_post)

if __name__=="__main__":
    Catalog=json.load(open('Catalog.json'))
    broker=Catalog['broker']['IPAddress']
    port=Catalog['broker']['port']
    base_topic=Catalog['baseTopic']
    topic_temp='/sensor/temperature'
    topic_battery='/sensor/battery'
    topic_presence='/sensor/presence'
    topic_photon='/sensor/photon'
    topic_daily='/sensor/daily'
    Contr=Controller('Geraci12232211321',broker,base_topic,topic_temp, topic_battery, topic_presence, topic_photon, topic_daily,Catalog)
    Contr.StartOperation()
    # infinite loop to keep the script running 
    while True:
        time.sleep(30)
        Contr.control_strategy()
