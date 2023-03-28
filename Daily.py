import json
import random
import time
from datetime import datetime
from MyMQTT import MyMQTT
from simplePublisher import MyPublisher
import cherrypy
import requests

class BatteryDailyUsage(MyPublisher):

    def __init__(self,ClientID, broker, port, base_topic, topic_daily, Catalog):
        self.base_topic=base_topic
        self.topic_daily=topic_daily
        self.client = MyMQTT(ClientID, broker, port, None)
        self.__message = {
            'bn': 'Battery_daily_usage',
            'e':
            [
                {'n': 'Battery_percentage', 'value': '', 'timestamp': '', 'unit': '%'},
            ]
        }
        self.response_json_all_user = Catalog['UserList']
        self.NumberofUser=len(self.response_json_all_user)
        self.output=[0]*self.NumberofUser

    def start(self):
        self.client.start()

    def sendData(self):
        for i in range(self.NumberofUser):
            UserID=int(self.response_json_all_user[i]['UserID'])
            message = self.__message
            message['e'][0]['value'] = self.output[i]
            message['e'][0]['timestamp'] = str(time.time())
            self.topic=self.base_topic+str(UserID)+self.topic_daily
            print(self.topic+f' Published:  '+str(message['e'][0]['value']))
            self.client.myPublish(self.topic, message)

    def makerequest(self):
        for i in range(self.NumberofUser):
            UserID=int(self.response_json_all_user[i]['UserID'])
            url='http://127.0.0.1:8080/UserID/'+'/'+str(UserID)+'/Agenda'
            response= requests.get(url)
            response_json_Agenda = response.json()
            
            today_num=datetime.today().weekday()
            if today_num==0:
                today='Monday'
            if today_num==1:
                today='Tuesday'
            if today_num==2:
                today='Wednesday'
            if today_num==3:
                today='Thursday'
            if today_num==4:
                today='Friday'
            elif today_num==5:
                today='Saturday'
            elif today_num==6:
                today='Sunday'
            
            capacity=self.response_json_all_user[i]['CapacityBattery'] # capacità della batteria in KWh
            km_kWh=self.response_json_all_user[i]['Consuption_km/kwh'] # consumo in km/KWh
            max_autonomy=km_kWh*capacity
            Km=0
            for j in range(len(response_json_Agenda['Agenda'][today])):
                Km=Km+response_json_Agenda['Agenda'][today][j]['NumberOfTotalKilometers']
            if Km>max_autonomy:
                print('too much km')
                energy=capacity
                battery=100
                self.output=battery
            else:
                energy=Km/km_kWh #6 km 1 KWh 
                battery=100*energy/capacity
            self.output[i]=int(battery)

if __name__ == '__main__':
    while True:
        Catalog=json.load(open('Catalog.json'))
        URL=Catalog['Catalog_url']+'/catalog'
        response= requests.get(URL)
        Catalog_json = response.json()
        broker=Catalog_json['broker']['IPAddress']
        port=Catalog_json['broker']['port']
        base_topic=Catalog_json['baseTopic']
        topic_daily='/sensor/daily'
        daily=BatteryDailyUsage('Geraci15273627', broker, port, base_topic, topic_daily,Catalog_json)
        daily.makerequest()
        # time.sleep(5)
        daily.start()
        daily.sendData()
        time.sleep(10)
