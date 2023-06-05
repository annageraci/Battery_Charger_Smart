import paho.mqtt.client as PahoMQTT
import json
from MyMQTT import *
import time
import cherrypy
import requests

class Controller:
    def __init__(self,clientID,broker, base_topic, topic_Btemp, topic_battery, topic_presence, topic_alert,topic_daily, base_url, DockerIP):
        self.clientID=clientID
        self.broker=broker
        self.base_url=base_url
        self.DockerIP=DockerIP
        self.base_topic=base_topic
        self.topic_Btemp=topic_Btemp
        self.topic_battery=topic_battery
        self.topic_presence=topic_presence
        self.topic_alert=topic_alert
        self.topic_daily=topic_daily
        # the notifier is the Sensor itself
        url=self.base_url+'/catalog'
        #url=self.DockerIP+'/catalog'
        response=requests.get(url)
        self.Catalog=response.json()
        self.NumberofUser=len(self.Catalog['UserList'])
        self.client=MyMQTT(self.clientID,self.broker,1883,self)
        self.__message = {
            'bn': 'State_Control',
            'text':'', 
            't':''
        }
        self.output=[-1]*self.NumberofUser

        # initialize the value of the measurement pick from the sensor
        self.Btemp=[-1]*self.NumberofUser
        self.battery_percentage=[-1]*self.NumberofUser
        self.digital_button=[-1]*self.NumberofUser
        self.photon=[-1]*self.NumberofUser
        self.actuator_command=[-1]*self.NumberofUser
        self.daily=[-1]*self.NumberofUser
        self.flag=[2]*self.NumberofUser

        # initialize the topic of the message send by the sensor        
        self.topic_Btemp_completed=[]
        self.topic_alert_completed=[]
        self.topic_presence_completed=[]
        self.topic_battery_completed=[]
        self.topic_daily_completed=[]
        self.topic_flag=[]

    def StartOperation(self):
        self.client.start() #connect to the broker and start the loop
        time.sleep(6) # asyncronous so we want exaclty ordered
        for i in range(len(self.Catalog['UserList'])):
            UserID=int(self.Catalog['UserList'][i]['UserID'])
            self.topic_Btemp_completed.insert(i,self.base_topic +str(UserID)+ self.topic_Btemp)       
            self.client.mySubscribe(self.topic_Btemp_completed[i])
            self.topic_alert_completed.insert(i,self.base_topic +str(UserID)+ self.topic_alert) 
            self.client.mySubscribe(self.topic_alert_completed[i])
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
            if topic==self.topic_Btemp_completed[i]:
                payload=json.loads(msg)
                self.Btemp[i]=payload['e'][0]['v']
                print(f'the value of the temperature sensor of the UserID {UserID} is {self.Btemp[i]}')
            elif topic==self.topic_battery_completed[i]:
                payload=json.loads(msg)
                self.battery_percentage[i]=payload['e'][0]['v']
                print(f'the value of the percentage of the battery of the UserID {UserID} is {self.battery_percentage[i]}')
            elif topic==self.topic_presence_completed[i]:
                payload=json.loads(msg)
                self.digital_button[i]=payload['e'][0]['v']
                print(f'the value of the presence of the vehicle of the UserID {UserID} is {self.digital_button[i]}')
            elif topic==self.topic_daily_completed[i]:
                payload=json.loads(msg)
                self.daily[i]=payload['e'][0]['v']
                print(f'the value of the battery percentage usage today by the userID {UserID} will be {self.daily[i]}')
            elif topic==self.topic_flag[i]:
                payload=json.loads(msg)
                self.flag[i]=payload['e'][0]['v']
                print(f'the value of the flag of the userID {UserID} is changed: Flag = {self.flag[i]}')
    
    def control_strategy(self):
        for i in range(self.NumberofUser):
            UserID=self.Catalog['UserList'][i]['UserID']
            
            alert=0
            # temperature of the battery too high 
            if self.Btemp[i]>50:
                #set the actuator OFF manually
                topic=self.base_topic+UserID+'/manualFlag'
                print(f'Published to {topic}')
                message={"bn": 'manualFlag', "e": [{"n": 'Flag', "u": 'boolean', "t": [], "v": []}]}
                message['e'][0]['v'] = 0
                message['e'][0]['t'] = str(time.time())
                self.client.myPublish(topic, message)
                alert=1
                # send alertSMS
                self.output[i]='The temperature of the battery is too high, cannot recharge the battery, leave the vehicle to a specialist'
            else: 
                #restore the actuator controller strategy only the first time
                if alert==1: 
                    topic=self.base_topic+UserID+'/manualFlag'
                    print(f'Published to {topic}')
                    message={"bn": 'manualFlag', "e": [{"n": 'Flag', "u": 'boolean', "t": [], "v": []}]}
                    message['e'][0]['v'] = 0
                    message['e'][0]['t'] = str(time.time())
                    self.client.myPublish(topic, message)
                    alert=0
                self.output[i]='No temperature battery issue'
            topic=self.base_topic+UserID+self.topic_alert
            print(f'Published to {topic}')
            message=self.__message
            message['text'] = self.output[i]
            message['t'] = str(time.time())
            self.client.myPublish(topic, message)
            #print(self.output[i])

            if self.digital_button[i]==0:
                self.output[i]='The vehicle is not present in the garage'
            elif self.digital_button[i]==-1: 
                self.output[i]='Presence sensor not work'
            else: 
                self.output[i]='No issue from presence sensor'
            topic=self.base_topic+UserID+self.topic_alert
            print(f'Published to {topic}')
            message=self.__message
            message['text'] = self.output[i]
            message['t'] = str(time.time())
            self.client.myPublish(topic, message)
            #print(self.output[i])

            if self.battery_percentage[i]<15 and self.battery_percentage[i]!=-1:
                self.output[i]=f'The percentage of battery is too low (<15%): {self.battery_percentage[i]} %'
            elif self.battery_percentage[i]==-1:
                self.output[i]=f'Battery percentage is not detected!!'
            else: 
                self.output[i]=f'Battery percentage is not too low: {self.battery_percentage[i]}'
            topic=self.base_topic+UserID+self.topic_alert   
            print(f'Published to {topic}')
            message=self.__message
            message['text'] = self.output[i]
            message['t'] = str(time.time())
            self.client.myPublish(topic, message)
            #print(self.output[i])

                


if __name__=="__main__":
    Settings=json.load(open("../settings.json"))
    base_url=Settings['Catalog_url_Carlo']
    Docker_url=Settings['DockerIP']
    broker=Settings['broker']['IPAddress']
    port=Settings['broker']['port']
    base_topic=Settings['baseTopic']
    topic_Btemp='/sensor/Btemperature'
    topic_battery='/sensor/battery'
    topic_presence='/sensor/presence'
    topic_photon='/sensor/photon'
    topic_daily='/sensor/daily'
    topic_alert='/statecontrol/AlertSMS'
    Contr=Controller('Geraci1901321',broker,base_topic,topic_Btemp, topic_battery, topic_presence, topic_alert, topic_daily, base_url,Docker_url)
    Contr.StartOperation()
    # infinite loop to keep the script running 
    while True:
        time.sleep(30)
        Contr.control_strategy()
