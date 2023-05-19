import paho.mqtt.client as PahoMQTT
import json
from MyMQTT import *
import time
import cherrypy
import requests

class Controller:
    def __init__(self,clientID,broker, base_topic, topic_temp, topic_battery, topic_presence, topic_photon,topic_daily, base_url, DockerIP):
        self.clientID=clientID
        self.broker=broker
        self.base_url=base_url
        self.DockerIP=DockerIP
        self.base_topic=base_topic
        self.topic_temp=topic_temp
        self.topic_battery=topic_battery
        self.topic_presence=topic_presence
        self.topic_photon=topic_photon
        self.topic_daily=topic_daily
        # the notifier is the Sensor itself
        url=self.base_url+'/catalog'
        #url=self.DockerIP+'/catalog'
        response=requests.get(url)
        self.Catalog=response.json()
        self.NumberofUser=len(self.Catalog['UserList'])
        self.client=MyMQTT(self.clientID,self.broker,1883,self)
        
        # initialize the value of the measurement pick from the sensor
        self.temperature=[-1]*self.NumberofUser
        self.battery_percentage=[-1]*self.NumberofUser
        self.digital_button=[-1]*self.NumberofUser
        self.photon=[-1]*self.NumberofUser
        self.actuator_command=[-1]*self.NumberofUser
        self.daily=[-1]*self.NumberofUser
        self.flag=[2]*self.NumberofUser

        # initialize the topic of the message send by the sensor        
        self.topic_temp_completed=[]
        self.topic_photon_completed=[]
        self.topic_presence_completed=[]
        self.topic_battery_completed=[]
        self.topic_daily_completed=[]
        self.topic_flag=[]

    def StartOperation(self):
        self.client.start() #connect to the broker and start the loop
        time.sleep(6) # asyncronous so we want exaclty ordered
        for i in range(len(self.Catalog['UserList'])):
            print('INITIALIZING')
            UserID=int(self.Catalog['UserList'][i]['UserID'])
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
            self.topic_flag.insert(i,self.base_topic+str(UserID)+'/manualFlag')
            self.client.mySubscribe(self.topic_flag[i])

    def notify(self,topic,msg):
        for i in range(len(self.Catalog['UserList'])):
            UserID=int(self.Catalog['UserList'][i]['UserID'])
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
            elif topic==self.topic_flag[i]:
                payload=json.loads(msg)
                self.flag[i]=payload['e'][0]['v']
                print(f'the value of the flag of the userID {UserID} is changed: Flag = {self.flag[i]}')
    
    def control_strategy(self):
        soglia_photon=500 # eV energy of the photon 
        for i in range(self.NumberofUser):
            UserID=self.Catalog['UserList'][i]['UserID']
            if self.flag[i]==2:
                # 1° step car in garage?
                if (self.digital_button[i]==0):
                    print('The vehicle is not present in the garage')
                    self.actuator_command[i]=0
                else:
                    if (self.digital_button[i]==-1):
                        print('The sensor of presence does not work')
                    # 2* step ha i pannelli fotovoltaici? c'è il sole?
                    if self.photon[i]<=soglia_photon and self.photon[i]!=-1:
                        # self.photon=-1 means no solar pannel 
                        print(f'Solar panel produce enough energy, energy: {self.photon[i]}')
                        self.actuator_command[i]=1
                    else:
                        # 3° step check aria condizionata o riscaldamento (temperatura) 
                        daily_appointment=int(self.daily[i]) #%battery usage in this day
                        print(daily_appointment)
                        print(self.battery_percentage[i])
                        soglia_Htemperature=20 # more than 20° aria condizionata
                        soglia_Ltemperature=10 # less than 10° aria calda
                        if ((self.temperature[i]>soglia_Htemperature or self.temperature[i]<soglia_Ltemperature) and self.temperature[i]!=-1):
                            print(f'Could be necessary switch on the conditioning, temp: {self.temperature[i]}')
                            daily_appointment=daily_appointment+0.2*daily_appointment #maggiorazione del 20%
                        # 4° step % batteria è sufficiente
                        if (daily_appointment>100):
                            print('probably you have to charge the car during the usage in another charge station')
                        if (self.battery_percentage[i]-15>daily_appointment and int(daily_appointment)!=-1):
                            print(f'percentage of battery sufficient, more than {daily_appointment}')
                            self.actuator_command[i]=0
                        elif (self.battery_percentage[i]-15<daily_appointment and int(daily_appointment)!=-1):
                            print(f'percentage of battery insufficient, less than {daily_appointment}')
                            self.actuator_command[i]=1
                    if (self.actuator_command[i]==-1):
                        print('All the previous check down')
                        self.actuator_command[i]=0            
                topic=self.base_topic+UserID+'/actuator'
                print(f'{topic} Published {self.actuator_command[i]} from control strategies \n')
                msg= {
                        'bn': 'actuator',
                        'e':
                        [
                    {'n': 'actuator', 'v': self.actuator_command[i], 't': time.time(), 'u': '%'},
                    ]
                    }   
                self.client.myPublish(topic, msg)
                dict_to_post={"UserID": UserID,"value": int(self.actuator_command[i])}
                response = requests.put(self.base_url+'/Actuator', json.dumps(dict_to_post))
                #print(dict_to_post)
                self.actuator_command[i]=-1
                self.temperature[i]=-1
                self.battery_percentage[i]=-1
                self.digital_button[i]=-1
                self.photon[i]=-1
                self.actuator_command[i]=-1
                self.daily[i]=-1
            elif self.flag[i]==1:
                topic=self.base_topic+UserID+'/actuator'
                msg= {
                        'bn': 'actuator',
                        'e':
                        [
                    {'n': 'actuator', 'v': 1, 't': time.time(), 'u': '%'},
                    ]
                    }   
                self.client.myPublish(topic, msg)
                print(f'{topic} Published {msg["e"][0]["v"]} from manual activation \n')
                dict_to_post={"UserID": UserID,"value": msg["e"][0]["v"]}
                #print(dict_to_post)
                response = requests.put(self.base_url+'/Actuator', json.dumps(dict_to_post))
            elif self.flag[i]==0:
                topic=self.base_topic+UserID+'/actuator'
                msg= {
                        'bn': 'actuator',
                        'e':
                        [
                    {'n': 'actuator', 'v': 0, 't': time.time(), 'u': '%'},
                    ]
                    }   
                self.client.myPublish(topic, msg)
                print(f'{topic} Published {msg["e"][0]["v"]} from manual activation \n')
                dict_to_post={"UserID": UserID,"value": msg["e"][0]["v"]}
                #print(dict_to_post)
                response = requests.put(self.base_url+'/Actuator', json.dumps(dict_to_post))

                


if __name__=="__main__":
    Settings=json.load(open("../settings.json"))
    base_url=Settings['Catalog_url_Carlo']
    Docker_url=Settings['DockerIP']
    broker=Settings['broker']['IPAddress']
    port=Settings['broker']['port']
    base_topic=Settings['baseTopic']
    topic_temp='/sensor/temperature'
    topic_battery='/sensor/battery'
    topic_presence='/sensor/presence'
    topic_photon='/sensor/photon'
    topic_daily='/sensor/daily'
    Contr=Controller('Geraci12232211321',broker,base_topic,topic_temp, topic_battery, topic_presence, topic_photon, topic_daily, base_url,Docker_url)
    Contr.StartOperation()
    # infinite loop to keep the script running 
    while True:
        time.sleep(30)
        Contr.control_strategy()
