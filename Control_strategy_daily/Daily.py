import json
import time
from datetime import datetime
from MyMQTT import MyMQTT
from simplePublisher import MyPublisher
import cherrypy
import requests

class BatteryDailyUsage(MyPublisher):

    def __init__(self,ClientID, broker, port, base_topic, topic_daily, BaseUrl, DockerIP):
        self.base_topic=base_topic
        self.topic_daily=topic_daily
        self.client = MyMQTT(ClientID, broker, port, None)
        self.__message = {
            'bn': 'Battery_daily_usage',
            'e':
            [
                {'n': 'Battery_percentage', 'v': '', 't': '', 'unit': '%'},
            ]
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
        

    def start(self):
        self.client.start()

    def sendData(self):
        for i in range(self.NumberofUser):
            UserID=int(self.response_json_all_user[i]['UserID'])
            message = self.__message
            message['e'][0]['v'] = self.output[i]
            message['e'][0]['t'] = str(time.time())
            self.topic=self.base_topic+str(UserID)+self.topic_daily
            print(self.topic+f' Published:  '+str(message['e'][0]['v']))
            self.client.myPublish(self.topic, message)

    def makerequest(self):
        for i in range(self.NumberofUser):
            UserID=int(self.response_json_all_user[i]['UserID'])
            url=self.BaseUrl+'/UserID/'+'/'+str(UserID)+'/Agenda'
            # DOCKER container
            # url=self.DockerIP+'/UserID/'+'/'+str(UserID)+'/Agenda'
            response= requests.get(url)
            response_json_Agenda = response.json()
            
            today_num=datetime.today().weekday()
            week_day=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            today=week_day[today_num]
            

            capacity=self.response_json_all_user[i]['CapacityBattery'] # capacità della batteria in KWh   ## 15-20 kW/h
            km_kWh=self.response_json_all_user[i]['Consumption_km/kwh'] # consumo in km/KWh
            max_autonomy=km_kWh*capacity
            Km=0
            for j in range(len(response_json_Agenda['Agenda'][today])):
                Km=Km+response_json_Agenda['Agenda'][today][j]['NumberOfTotalKilometers']
            if Km>max_autonomy:
                # too km -> AlertSMS 
                topic=self.base_topic+str(UserID)+'/statecontrol/AlertSMS'  
                print(f'Published to {topic}')
                message={
                    'bn': 'State_Control',
                    'text':'', 
                    't':''
                }
                message['text'] = f'Today your Agenda is full, so could be necessary to charge the car in dedicated car station during your trip: \n Number of km necessary to your agenda: {Km} km \n Autonomy in km with the 100% of battery: {max_autonomy} km'
                message['t'] = str(time.time())
                self.client.myPublish(topic, message)
                energy=capacity
                battery=100
                time.sleep(15)
            else:
                energy=Km/km_kWh #6 km 1 KWh 
                battery=100*energy/capacity
            self.output[i]=int(battery)

if __name__ == '__main__':
    while True:
        settings=json.load(open('../settings.json'))

        # Comando per runnare Docker da prompt : docker run -v *absolute_path_of_setting.json_file":/app/Settings *nome_dell_image*
        # docker run -v C:/Users/an.geraci/Desktop/Battery_Charger_Smart:/app/Settings daily
        # settings=json.load(open('/app/Settings/settings.json'))

        BaseUrl=settings['Catalog_url_Anna']
        DockerIP=settings['DockerIP']
        broker=settings['broker']['IPAddress']
        port=settings['broker']['port']
        base_topic=settings['baseTopic']
        topic_daily='/sensor/daily'
        daily=BatteryDailyUsage('Geraci15273627', broker, port, base_topic, topic_daily,BaseUrl, DockerIP)
        while True:
            daily.makerequest()
            daily.start()
            daily.sendData()
            time.sleep(15)