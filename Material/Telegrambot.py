import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import time
import paho.mqtt.client as PahoMQTT
import json
from MyMQTT import *
import time
import cherrypy
import requests


class SwitchBot:
    def __init__(self, token, broker, port, topic):
        # Local token
        self.tokenBot = token
        # Catalog token
        # self.tokenBot=requests.get("http://catalogIP/telegram_token").json()["telegramToken"]
        self.bot = telepot.Bot(self.tokenBot)
        self.client = MyMQTT("telegramBot21389", broker, port, self)
        self.client.start()
        self.BaseTopic = topic
        self.__message = {'bn': "telegramBot",
                          'e':
                          [
                              {'n': 'switch', 'v': '', 't': '', 'u': 'bool'},
                          ]
                          }
        self.__messageAgenda = {
                        "UserID": "",
                        "Day": "",
                        "Date":
                        {
                        "Type": "",
                        "StartTimeSlot": [],
                        "NumberOfTotalKilometers": []
                        }
                        }
        MessageLoop(self.bot, {'chat': self.on_chat_message,
                               'callback_query': self.on_callback_query}).run_as_thread()
        
        urlToContact='http://127.0.0.1:8080/AllUsers'
        response= requests.get(urlToContact)
        self.ListOfAllUser_json = response.json()
        self.topic_presence=[]
        self.UserID=-1
        self.output=[]
        self.Flag=0
        self.output=[]
        self.topic_StateControl=[]
        self.AlertOutput=[]

    def StartOperation(self):
        self.client.start() #connect to the broker and start the loop
        time.sleep(6) # asyncronous so we want exaclty ordered
        self.topic_presence=self.BaseTopic +str(self.UserID)+ '/sensor/presence'
        if self.AlertOutput==-1:

            # Da completare con il topic del tipo di allerta pubblicato dallo State Control
            self.client.mySubscribe(self.topic_statecontrol)
            
        elif self.output==-1:
            self.client.mySubscribe(self.topic_presence)
    
    def notify(self,topic,msg):
        
        if topic==self.topic_presence:
            payload=json.loads(msg)
            self.output=payload['e'][0]['value']
            #how to do when the message is received
            print(f'the value of the presence of the vehicle of the UserID {self.UserID} is {self.output}')

    def on_chat_message(self, msg):
        content_type, chat_type, chat_ID = telepot.glance(msg)
        message = msg['text']
        ChatID=msg['chat']['id']
        for currentUser in self.ListOfAllUser_json:
            if currentUser['ChatID']==str(ChatID):
                self.UserID=currentUser['UserID']
                if message == "/switch":
                    buttons = [[InlineKeyboardButton(text=f'start charge🔋', callback_data=f'on'), 
                            InlineKeyboardButton(text=f'stop charge🪫', callback_data=f'off'), 
                            InlineKeyboardButton(text=f'nothing', callback_data=f'nothing')]]
                    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
                    self.bot.sendMessage(chat_ID, text='What do you want to do?', reply_markup=keyboard)
                elif message=="/IsPresence":
                    self.output=-1
                    sb.StartOperation()
                    self.bot.sendMessage(chat_ID, text='Wait the value from the sensor!')
                    time.sleep(15)
                    if self.output==1:
                        self.bot.sendMessage(chat_ID, text='The vehicle is in postation!')
                        self.client.stop()
                    elif self.output==0:
                        self.bot.sendMessage(chat_ID, text='The vehicle is not in postation!')
                        self.client.stop()
                    else:
                        self.bot.sendMessage(chat_ID, text='The sensor is not work in this moment, Try again later!')
                        self.client.stop()
                        self.output=[]
                elif message=='/AgendaMonday':
                    buttons = [[InlineKeyboardButton(text=f'20 km\n', callback_data=f'0'), 
                            InlineKeyboardButton(text=f'40 km\n', callback_data=f'1'), 
                            InlineKeyboardButton(text=f'60 km\n', callback_data=f'2'),
                            InlineKeyboardButton(text=f'80 km\n', callback_data=f'3')]]
                    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
                    self.bot.sendMessage(chat_ID, text='How Many kilometers?', reply_markup=keyboard)
                elif message=='/AgendaThursday':
                    buttons = [[InlineKeyboardButton(text=f'20 km\n', callback_data=f'4'), 
                            InlineKeyboardButton(text=f'40 km\n', callback_data=f'5'), 
                            InlineKeyboardButton(text=f'60 km\n', callback_data=f'6'),
                            InlineKeyboardButton(text=f'80 km\n', callback_data=f'7')]]
                    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
                    self.bot.sendMessage(chat_ID, text='How Many kilometers?', reply_markup=keyboard)
                elif message=='/AgendaWednesday':
                    buttons = [[InlineKeyboardButton(text=f'20 km\n', callback_data=f'8'), 
                            InlineKeyboardButton(text=f'40 km\n', callback_data=f'9'), 
                            InlineKeyboardButton(text=f'60 km\n', callback_data=f'10'),
                            InlineKeyboardButton(text=f'80 km\n', callback_data=f'11')]]
                    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
                    self.bot.sendMessage(chat_ID, text='How Many kilometers?', reply_markup=keyboard)
                elif message=='/AgendaTuesday':
                    buttons = [[InlineKeyboardButton(text=f'20 km\n', callback_data=f'12'), 
                            InlineKeyboardButton(text=f'40 km\n', callback_data=f'13'), 
                            InlineKeyboardButton(text=f'60 km\n', callback_data=f'14'),
                            InlineKeyboardButton(text=f'80 km\n', callback_data=f'15')]]
                    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
                    self.bot.sendMessage(chat_ID, text='How Many kilometers?', reply_markup=keyboard)
                elif message=='/AgendaFriday':
                    buttons = [[InlineKeyboardButton(text=f'20 km\n', callback_data=f'16'), 
                            InlineKeyboardButton(text=f'40 km\n', callback_data=f'17'), 
                            InlineKeyboardButton(text=f'60 km\n', callback_data=f'18'),
                            InlineKeyboardButton(text=f'80 km\n', callback_data=f'19')]]
                    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
                    self.bot.sendMessage(chat_ID, text='How Many kilometers?', reply_markup=keyboard)
                elif message=='/AgendaSaturday':
                    buttons = [[InlineKeyboardButton(text=f'20 km\n', callback_data=f'20'), 
                            InlineKeyboardButton(text=f'40 km\n', callback_data=f'21'), 
                            InlineKeyboardButton(text=f'60 km\n', callback_data=f'22'),
                            InlineKeyboardButton(text=f'80 km\n', callback_data=f'23')]]
                    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
                    self.bot.sendMessage(chat_ID, text='How Many kilometers?', reply_markup=keyboard)
                elif message=='/AgendaSunday':
                    buttons = [[InlineKeyboardButton(text=f'20 km\n', callback_data=f'24'), 
                            InlineKeyboardButton(text=f'40 km\n', callback_data=f'25'), 
                            InlineKeyboardButton(text=f'60 km\n', callback_data=f'26'),
                            InlineKeyboardButton(text=f'80 km\n', callback_data=f'27')]]
                    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
                    self.bot.sendMessage(chat_ID, text='How Many kilometers?', reply_markup=keyboard)

                # Da completare con lo sviluppo di ThingSpeakAdaptor
                # elif message=='/Statistics':

                # Da completare con lo sviluppo di State Control
                elif message=='/AlertSMS':
                    self.AlertOutput=-1
                    time.sleep(15)
                    if self.AlertOutput==1:
                        # update con il giusto alert che darà 
                        self.bot.sendMessage(chat_ID, text='Type of Alert: ')
                        self.client.stop()
                    elif self.AlertOutput==0:
                        # Da continuare con il giusto Alert
                        self.bot.sendMessage(chat_ID, text='Type of Alert: ')
                        self.client.stop()
                    else:
                        self.bot.sendMessage(chat_ID, text='In this moment the service is not work')
                        self.client.stop()

                else:
                    self.bot.sendMessage(chat_ID, text="Command not supported")
        if self.UserID==-1:
            self.bot.sendMessage(chat_ID, text="You do not have User associated with this Telegram profile")

    def on_callback_query(self,msg):
        query_ID , chat_ID , query_data = telepot.glance(msg,flavor='callback_query')
        if (query_data=='on' or query_data=='off' or query_data=='nothing'):
            self.topic_actuator=self.BaseTopic+str(self.UserID)+'/actuator'
            self.topic_flag=self.BaseTopic+str(self.UserID)+'/manualFlag'
            if query_data=='on':
                output=1
                payload = self.__message.copy()
                payload['e'][0]['v'] = output
                payload['e'][0]['t'] = time.time()
                self.client.myPublish(self.topic_actuator, payload)
                self.client.myPublish(self.topic_flag, payload)
            elif query_data=='off':
                output=0
                payload = self.__message.copy()
                payload['e'][0]['v'] = output
                payload['e'][0]['t'] = time.time()
                self.client.myPublish(self.topic_actuator, payload)
                self.client.myPublish(self.topic_flag, payload)
            elif query_data=='nothing':
                output=2
                payload = self.__message.copy()
                payload['e'][0]['v'] = output
                payload['e'][0]['t'] = time.time()
                self.client.myPublish(self.topic_actuator, payload)
                self.client.myPublish(self.topic_flag, payload)
            print('Published to the topic '+self.topic_actuator+':'+str(payload['e'][0]['v']))
            print('Published to the topic '+self.topic_flag+':'+str(payload['e'][0]['v']))
            self.bot.sendMessage(chat_ID, text=f"Charger switched {query_data}")
            #self.UserID=-1
        else: 
            if (query_data=='0' or query_data=='1' or query_data=='2' or query_data=='3'):
                day='Monday'
            elif (query_data=='4' or query_data=='5' or query_data=='6' or query_data=='7'):
                day='Thursday'
            elif (query_data=='8' or query_data=='9' or query_data=='10' or query_data=='11'):
                day='Wednesday'
            elif (query_data=='12' or query_data=='13' or query_data=='14' or query_data=='15'):
                day='Tuesday'
            elif (query_data=='16' or query_data=='17' or query_data=='18' or query_data=='19'):
                day='Friday'
            elif (query_data=='20' or query_data=='21' or query_data=='22' or query_data=='23'):
                day='Saturday'
            elif (query_data=='24' or query_data=='25' or query_data=='26' or query_data=='27'):
                day='Sunday'   
            payload=self.__messageAgenda.copy()
            payload['UserID']=str(self.UserID)
            payload['Day']=day
            if (query_data=='0' or query_data=='4' or query_data=='8' or query_data=='12' or query_data=='16' or query_data=='20' or query_data=='24'):
                payload['Date']['NumberOfTotalKilometers']=20
            elif (query_data=='1' or query_data=='5' or query_data=='9' or query_data=='13' or query_data=='17' or query_data=='21' or query_data=='25'):
                payload['Date']['NumberOfTotalKilometers']=40
            elif (query_data=='2' or query_data=='6' or query_data=='10' or query_data=='14' or query_data=='18' or query_data=='22' or query_data=='26'):
                payload['Date']['NumberOfTotalKilometers']=60
            elif (query_data=='3' or query_data=='7' or query_data=='11' or query_data=='15' or query_data=='19' or query_data=='23' or query_data=='27'):
                payload['Date']['NumberOfTotalKilometers']=80
            response = requests.put('http://127.0.0.1:8080/Agenda', json.dumps(payload))
            self.bot.sendMessage(chat_ID, text=f"Successfully added to the agenda of the User {self.UserID}, in day {day}, {payload['Date']['NumberOfTotalKilometers']} km")
            self.UserID=-1


if __name__ == "__main__":
    conf = json.load(open("settings.json"))
    token = conf["TelegramToken"]
    broker = conf["broker"]['IPAddress']
    port = conf["broker"]['port']
    topic_base = conf["baseTopic"]
    sb=SwitchBot(token,broker,port,topic_base)

    while True:
        time.sleep(3)