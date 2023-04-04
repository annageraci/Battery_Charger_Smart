import json 
import cherrypy
import time

class Catalog(object):
    exposed=True

    def GET(self, *uri, **params):
	
        if uri[0]=="MessageBroker":
            device=json.load(open('Catalog.json'))
            Broker=device["broker"]
            return json.dumps(Broker,indent=2)
        
        elif uri[0]=="TelegramToken":
            device=json.load(open('Catalog.json'))
            token=device["TelegramToken"]
            return json.dumps(token,indent=2)
        
        elif uri[0]=="catalog":
            catalog=json.load(open('Catalog.json'))
            return json.dumps(catalog, indent=2)        

        elif uri[0]=='AllDevices':
            catalog=json.load(open('Catalog.json'))
            devices=catalog["DeviceList"]
            return json.dumps(devices, indent=2)

        elif uri[0]=='DeviceID':
            ID=uri[1]
            Catalog=json.load(open('Catalog.json'))
            ListOfDevice=Catalog['DeviceList']
            output=''
            for i in range(len(ListOfDevice)):
                if  ListOfDevice[i]['DeviceID']==ID:
                    output=ListOfDevice[i]
            return json.dumps(output, indent=2)

        elif uri[0]=='AllUsers':
            catalog=json.load(open('Catalog.json'))
            users=catalog["UserList"]
            return json.dumps(users, indent=2)

        elif uri[0]=='UserID':
            ID=uri[1]
            Catalog=json.load(open('Catalog.json'))
            ListOfUsers=Catalog['UserList']
            output=''
            for i in range(len(ListOfUsers)):
                if  ListOfUsers[i]['UserID']==ID:
                    output=ListOfUsers[i]
                    if uri[2]=='Agenda':
                        Agenda=ListOfUsers[i]['Agenda']
                        output={
                            "Agenda": Agenda
                        }
            return json.dumps(output, indent=2)
        else: 
            output='Add a valid uri parameters according to your request'
            return json.dumps(output,indent=2)

    def POST(self, *uri):
        if uri[0]=='Device':
            bodyAsString=cherrypy.request.body.read() 
            bodyAsDictionary=json.loads(bodyAsString)
            Catalog=json.load(open('Catalog.json'))
            ListOfDevice=Catalog['DeviceList']
            for i in range(len(ListOfDevice)):
                if ListOfDevice[i]['DeviceID']==bodyAsDictionary['DeviceID']:
                    return 'this device is already present in the list \n'
            # else is new so we can update the device list
            Catalog['DeviceList'].insert(len(Catalog['DeviceList']), bodyAsDictionary)
            json.dump(Catalog,open('Catalog.json','w'), indent=2)
            #json.dump(Catalog,open('setting.json','w'), indent=2)
            return json.dumps(Catalog)
        
        if uri[0]=='User':
            bodyAsString=cherrypy.request.body.read() 
            bodyAsDictionary=json.loads(bodyAsString)
            Catalog=json.load(open('Catalog.json'))
            ListOfUser=Catalog['UserList']
            for i in range(len(ListOfUser)):
                if ListOfUser[i]['UserID']==bodyAsDictionary['UserID']:
                    return 'this device is already present in the list \n'
            # else is new so we can update the device list
            Catalog['UserList'].insert(len(Catalog['UserList']), bodyAsDictionary)
            json.dump(Catalog,open('Catalog.json','w'), indent=2)
            #json.dump(Catalog,open('setting.json','w'), indent=2)
            return json.dumps(Catalog)

        
    def PUT(self,*uri):
        if uri[0]=='Device':
            # body {
            #   "DeviceID":13
            #   "time":time.time()
            # }
            bodyAsString=cherrypy.request.body.read() 
            bodyAsDictionary=json.loads(bodyAsString)
            Catalog=json.load(open('Catalog.json'))
            ListOfDevice=Catalog['DeviceList']
            for i in range(len(ListOfDevice)):
                if ListOfDevice[i]['DeviceID']==bodyAsDictionary['DeviceID']:
                    #Catalog['DeviceList'][i]['lastUpDate']=bodyAsDictionary["time"]
                    Catalog['DeviceList'][i]['lastUpDate']=int(time.time())
                    json.dump(Catalog,open('Catalog.json','w'), indent=2)
                    return json.dumps(Catalog)
        
        if uri[0]=='User':
            # body {
            #    "UserID":"1",
            #    "CapacityBattery": 50,
            #    "Consuption_km/kwh": 6,
            #    "ConnectedDevices": 
            #    {
            #        "measure": "Temperature",
            #        "DeviceName": "Temperature_sensor",
            #        "DeviceID": "1"
            #    }
            # }
            bodyAsString=cherrypy.request.body.read() 
            bodyAsDictionary=json.loads(bodyAsString)
            Catalog=json.load(open('Catalog.json'))
            ListOfUser=Catalog['UserList']
            for i in range(len(ListOfUser)):
                if ListOfUser[i]['UserID']==bodyAsDictionary['UserID']:
                    Catalog['UserList'][i]['CapacityBattery']=bodyAsDictionary['CapacityBattery']
                    Catalog['UserList'][i]["Consuption_km/kwh"]=bodyAsDictionary["Consuption_km/kwh"]
                    for currentDevice in Catalog['UserList'][i]["ConnectedDevices"]:
                        if currentDevice['DeviceID']==bodyAsDictionary['ConnectedDevices']['DeviceID']:
                            return 'Device already present in the list'
                    Catalog['UserList'][i]["ConnectedDevices"].append(bodyAsDictionary['ConnectedDevices'])
                    json.dump(Catalog,open('Catalog.json','w'),indent=2)
                    #json.dump(Catalog,open('setting.json','w'), indent=2)
                    return json.dumps(Catalog)
                
        if uri[0]=='Actuator':
            # body {"UserID": "1/2/4" 
            #        "value": "on/off"
            #       }
            bodyAsString=cherrypy.request.body.read()
            bodyAsDictionary=json.loads(bodyAsString)
            value=bodyAsDictionary['value']
            Catalog=json.load(open('Catalog.json'))
            ListOfUser=Catalog['UserList']
            for currentUser in ListOfUser:
                for currentDevice in currentUser['ConnectedDevices']:
                    if (currentDevice['DeviceName']=='Actuator' and int(currentUser['UserID'])==int(bodyAsDictionary['UserID'])):
                        DeviceID=currentDevice["DeviceID"]
            for i in range(len(Catalog['DeviceList'])):
                if Catalog['DeviceList'][i]['DeviceID']==DeviceID:
                    Catalog['DeviceList'][i]['status']=value
            json.dump(Catalog,open('Catalog.json','w'), indent=2)
            return json.dumps(Catalog)
        
        if uri[0]=='Agenda':
            #{
            #   "UserID": "1",
            #   "Day": "Monday",
            #   "Date":
            #    {
            #        "Type": "work",
            #        "StartTimeSlot": 8,
            #        "NumberOfTotalKilometers": 50
            #      }
            #}
            bodyAsString=cherrypy.request.body.read() 
            bodyAsDictionary=json.loads(bodyAsString)
            Catalog=json.load(open('Catalog.json'))
            ListOfUser=Catalog['UserList']
            for i in range(len(ListOfUser)):
                for currentUser in ListOfUser:
                    if currentUser['UserID']==bodyAsDictionary['UserID']:
                        day=bodyAsDictionary['Day']
                        if "Monday"==bodyAsDictionary['Day']:
                            currentUser['Agenda']['Monday'].append(bodyAsDictionary['Date'])
                        elif "Tuesday"==bodyAsDictionary['Day']:
                            currentUser['Agenda']['Tuesday'].append(bodyAsDictionary['Date'])
                        elif "Wednesday"==bodyAsDictionary['Day']:
                            currentUser['Agenda']['Wednesday'].append(bodyAsDictionary['Date'])
                        elif "Thursday"==bodyAsDictionary['Day']:
                            currentUser['Agenda']['Thurday'].append(bodyAsDictionary['Date'])
                        elif "Friday"==bodyAsDictionary['Day']:
                            currentUser['Agenda']['Friday'].append(bodyAsDictionary['Date'])
                        elif "Saturday"==bodyAsDictionary['Day']:
                            currentUser['Agenda']['Saturday'].append(bodyAsDictionary['Date'])
                        elif "Sunday"==bodyAsDictionary['Day']:
                            currentUser['Agenda']['Sunday'].append(bodyAsDictionary['Date'])
                        else:
                            return 'Does not exist this day'
                #json.dump(Catalog,open('Catalog.json','w'),indent=2)
                json.dump(Catalog,open('setting.json','w'), indent=2)
                return json.dumps(Catalog)
    
if __name__=="__main__":
    conf={
        '/':{
            'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
            'tool.session.on':True
        }
    }
    WebService=Catalog()
    cherrypy.tree.mount(WebService,'/',conf)
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 80})
    cherrypy.engine.start()
    cherrypy.engine.block()
