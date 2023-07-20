import json
import time
from datetime import datetime
from MyMQTT import *
from simplePublisher import MyPublisher
import requests

class StateControl(MyPublisher):

    def __init__(self,ClientID, broker, port, base_topic, topic_alert, BaseUrl, DockerIP, topic_Btemp, topic_battery,topic_presence):
        self.base_topic=base_topic
        self.topic_alert=topic_alert
        self.topic_Btemp=topic_Btemp
        self.topic_battery=topic_battery
        self.topic_presence=topic_presence
        self.client = MyMQTT(ClientID, broker, port,self)
        self.__message = {
            'bn': 'State_Control',
            'text':'', 
            't':''
        }
        self.BaseUrl=BaseUrl
        self.DockerIP=DockerIP

        # compute the number of the user
        #DOCKER 
        #url=self.DockerIP+'/AllUsers'
        
        url=self.BaseUrl+'/AllUsers'
        response= requests.get(url)
        self.response_json_all_user =response.json()
        self.NumberofUser=len(self.response_json_all_user)
        self.output=[0]*self.NumberofUser

        self.Btemp=[-1]*self.NumberofUser
        self.battery_percentage=[-1]*self.NumberofUser
        self.digital_button=[-1]*self.NumberofUser
        self.output=[-1]*self.NumberofUser

        self.topic_Btemp_completed=[]
        self.topic_presence_completed=[]
        self.topic_battery_completed=[]
        

    def start(self):
        self.client.start()
        time.sleep(6) # asyncronous so we want exaclty ordered
        for i in range(self.NumberofUser):
            UserID=int(self.response_json_all_user[i]['UserID'])
            self.topic_Btemp_completed.insert(i,self.base_topic +str(UserID)+ self.topic_Btemp) 
            self.client.mySubscribe(self.topic_Btemp_completed[i])
            self.topic_presence_completed.insert(i,self.base_topic +str(UserID)+ self.topic_presence) 
            self.client.mySubscribe(self.topic_presence_completed[i])
            self.topic_battery_completed.insert(i,self.base_topic +str(UserID)+ self.topic_battery) 
            self.client.mySubscribe(self.topic_battery_completed[i])

    def notify(self,topic,msg):
        for i in range(self.NumberofUser):
            UserID=int(self.response_json_all_user[i]['UserID'])
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
            
    def control_strategy(self):
        for i in range(self.NumberofUser):
            UserID=self.response_json_all_user[i]['UserID']
            
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
                    message['e'][0]['v'] = 2
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


if __name__ == '__main__':
    while True:
        settings=json.load(open('../settings.json'))

        # Comando per runnare Docker da prompt : docker run -v *absolute_path_of_setting.json_file":/app/Settings *nome_dell_image*
        # docker run -v C:/Users/an.geraci/Desktop/Battery_Charger_Smart:/app/Settings statecontrol
        #settings=json.load(open('/app/Settings/settings.json'))
        
        BaseUrl=settings['Catalog_url']
        DockerIP=settings['DockerIP']
        broker=settings['broker']['IPAddress']
        port=settings['broker']['port']
        base_topic=settings['baseTopic']
        topic_alert='/statecontrol/AlertSMS'
        topic_Btemp='/sensor/Btemperature' 
        topic_battery='/sensor/battery'
        topic_presence='/sensor/presence'
        state=StateControl('Geraci15273627', broker, port, base_topic, topic_alert,BaseUrl, DockerIP, topic_Btemp, topic_battery,topic_presence)
        state.start()
        while True:
            time.sleep(30)
            state.control_strategy()