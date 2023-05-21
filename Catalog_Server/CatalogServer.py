import json 
import cherrypy
import time

class Catalog(object):
    exposed=True

    def GET(self, *uri, **params):
        if len(uri)>0:
            if uri[0]=="MessageBroker":
                device=json.load(open('../Catalog.json'))
                Broker=device["broker"]
                return json.dumps(Broker,indent=2)
            
            elif uri[0]=="TelegramToken":
                device=json.load(open('../Catalog.json'))
                token=device["TelegramToken"]
                return json.dumps(token,indent=2)
            
            elif uri[0]=="catalog":
                catalog=json.load(open('../Catalog.json'))
                return json.dumps(catalog, indent=2)        

            elif uri[0]=='AllDevices':
                catalog=json.load(open('../Catalog.json'))
                devices=catalog["DeviceList"]
                return json.dumps(devices, indent=2)

            elif uri[0]=='DeviceID':
                ID=uri[1]
                Catalog=json.load(open('../Catalog.json'))
                ListOfDevice=Catalog['DeviceList']
                output=''
                for i in range(len(ListOfDevice)):
                    if  ListOfDevice[i]['DeviceID']==ID:
                        output=ListOfDevice[i]
                return json.dumps(output, indent=2)

            elif uri[0]=='AllUsers':
                catalog=json.load(open('../Catalog.json'))
                users=catalog["UserList"]
                return json.dumps(users, indent=2)

            elif uri[0]=='UserID':
                ID=uri[1]
                Catalog=json.load(open('../Catalog.json'))
                ListOfUsers=Catalog['UserList']
                output=''
                for currentUser in ListOfUsers:
                    if  currentUser['UserID']==ID:
                        output=currentUser
                return json.dumps(output, indent=2)
            elif uri[0]=='Agenda':
                ID=uri[1]
                Catalog=json.load(open('../Catalog.json'))
                ListOfUsers=Catalog['UserList']
                output=''
                for currentUser in ListOfUsers:
                    if currentUser['UserID']==ID:
                        Agenda=currentUser['Agenda']
                        output={
                            'UserID':ID,
                            'Agenda':Agenda
                        }
                return json.dumps(output, indent=2)
            else: 
                output='Add a valid uri parameters according to your request'
                return json.dumps(output,indent=2)
        else: 
            return 'No information about your request in the uri'

    def POST(self, *uri):
        if uri[0]=='Device':
            bodyAsString=cherrypy.request.body.read() 
            bodyAsDictionary=json.loads(bodyAsString)
            Catalog=json.load(open('../Catalog.json'))
            ListOfDevice=Catalog['DeviceList']
            for i in range(len(ListOfDevice)):
                if ListOfDevice[i]['DeviceID']==bodyAsDictionary['DeviceID']:
                    return 'this device is already present in the list \n'
            # else is new so we can update the device list
            Catalog['DeviceList'].insert(len(Catalog['DeviceList']), bodyAsDictionary)
            json.dump(Catalog,open('../Catalog.json', 'w'), indent=2)
            return json.dumps(Catalog)
        
        if uri[0]=='User':
            bodyAsString=cherrypy.request.body.read() 
            bodyAsDictionary=json.loads(bodyAsString)
            Catalog=json.load(open('../Catalog.json'))
            ListOfUser=Catalog['UserList']
            for i in range(len(ListOfUser)):
                if ListOfUser[i]['UserID']==bodyAsDictionary['UserID']:
                    return 'this user is already present in the list \n'
            # else is new so we can update the user list
            Catalog['UserList'].insert(len(Catalog['UserList']), bodyAsDictionary)
            json.dump(Catalog,open('../Catalog.json', 'w'), indent=2)
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
            Catalog=json.load(open('../Catalog.json'))
            ListOfUser=Catalog['UserList']
            Week=['Monday','Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            for i in range(len(ListOfUser)):
                for currentUser in ListOfUser:
                    if currentUser['UserID']==bodyAsDictionary['UserID']:
                        for i in range(7):
                            if bodyAsDictionary['Day']==Week[i]:
                                day=Week[i]
                                currentUser['Agenda'][day].append(bodyAsDictionary['Date'])
                                json.dump(Catalog,open('../Catalog.json', 'w'),indent=2)
                                return json.dumps(Catalog)
                return 'Does not exist this day'
                
        
    def PUT(self,*uri):
        if uri[0]=='Device':
            # body {
            #   "DeviceID":13,
            #   "value":23,
            #   "time":time.time()
            # }
            bodyAsString=cherrypy.request.body.read() 
            bodyAsDictionary=json.loads(bodyAsString)
            Catalog=json.load(open('../Catalog.json'))
            ListOfDevice=Catalog['DeviceList']
            for i in range(len(ListOfDevice)):
                if ListOfDevice[i]['DeviceID']==bodyAsDictionary['DeviceID']:
                    Catalog['DeviceList'][i]['lastUpDate']=bodyAsDictionary["time"]
                    Catalog['DeviceList'][i]['value']=bodyAsDictionary['value']
                    json.dump(Catalog,open('../Catalog.json', 'w'), indent=2)
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
            Catalog=json.load(open('../Catalog.json'))
            ListOfUser=Catalog['UserList']
            for i in range(len(ListOfUser)):
                if ListOfUser[i]['UserID']==bodyAsDictionary['UserID']:
                    Catalog['UserList'][i]['CapacityBattery']=bodyAsDictionary['CapacityBattery']
                    Catalog['UserList'][i]["Consuption_km/kwh"]=bodyAsDictionary["Consuption_km/kwh"]
                    for currentDevice in Catalog['UserList'][i]["ConnectedDevices"]:
                        if currentDevice['DeviceID']==bodyAsDictionary['ConnectedDevices']['DeviceID']:
                            return 'The Device is already present in the list but the other parameter are updated' + json.dumps(Catalog)
                    Catalog['UserList'][i]["ConnectedDevices"].append(bodyAsDictionary['ConnectedDevices'])
                    json.dump(Catalog,open('../Catalog.json', 'w'),indent=2)
                    return json.dumps(Catalog)
                
        if uri[0]=='Actuator':
            # body {"UserID": "1/2/4" 
            #        "value": 0/1
            #       }
            bodyAsString=cherrypy.request.body.read()
            bodyAsDictionary=json.loads(bodyAsString)
            value=bodyAsDictionary['value']
            Catalog=json.load(open('../Catalog.json'))
            ListOfUser=Catalog['UserList']
            for currentUser in ListOfUser:
                for currentDevice in currentUser['ConnectedDevices']:
                    if (currentDevice['DeviceName']=='Actuator' and int(currentUser['UserID'])==int(bodyAsDictionary['UserID'])):
                        DeviceID=currentDevice["DeviceID"]
            for i in range(len(Catalog['DeviceList'])):
                if Catalog['DeviceList'][i]['DeviceID']==DeviceID:
                    if value==0:
                        Catalog['DeviceList'][i]['value']=0
                    elif value==1:
                        Catalog['DeviceList'][i]['value']=1
                    else:
                        return 'The value is not valid '+ json.dumps(Catalog)
            json.dump(Catalog,open('../Catalog.json', 'w'), indent=2)
            return json.dumps(Catalog)
        
        if uri[0]=='AgendaUpdate':
            #{
            #   "UserID": "1",
            #   "Day": "Monday",
            #   "Date":
            #    {
            #        "Type": "work",
            #        "StartTimeSlot": 8,
            #        "NumberOfTotalKilometers": 50
            #      }
            print('ok')
            bodyAsString=cherrypy.request.body.read() 
            bodyAsDictionary=json.loads(bodyAsString)
            Catalog=json.load(open('../Catalog.json'))
            ListOfUser=Catalog['UserList']
            Week=['Monday','Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            for i in range(len(ListOfUser)):
                for currentUser in ListOfUser:
                    if currentUser['UserID']==bodyAsDictionary['UserID']:
                        for i in range(7):
                            if Week[i]==bodyAsDictionary['Day']:
                                day=Week[i]
                                for appointment in currentUser['Agenda'][day]:
                                    if appointment['Type']==bodyAsDictionary['Date']['Type']:
                                        appointment['StartTimeSlot']=bodyAsDictionary['Date']['StartTimeSlot']
                                        appointment['NumberOfTotalKilometers']=bodyAsDictionary['Date']['NumberOfTotalKilometers']
                                        json.dump(Catalog,open('../Catalog.json', 'w'),indent=2)
                                        return json.dumps(Catalog)
                                 
                        return 'no corrispondence in your agenda'
                return 'no user associated'
                        
        if uri[0]=='AgendaRemove':
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
            Catalog=json.load(open('../Catalog.json'))
            ListOfUser=Catalog['UserList']
            ElemToRemove=bodyAsDictionary['Date']
            Week=['Monday','Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            for i in range(len(ListOfUser)):
                for currentUser in ListOfUser:
                    if currentUser['UserID']==bodyAsDictionary['UserID']:
                        for i in range(7):
                            if Week[i]==bodyAsDictionary['Day']:
                                day=Week[i]
                                for appointment in currentUser['Agenda'][day]:
                                    if ElemToRemove==appointment:
                                        currentUser['Agenda'][day].remove(appointment)
                                        json.dump(Catalog,open('../Catalog.json', 'w'),indent=2)
                                        return json.dumps(Catalog)
                        return 'Does not exist this appointment in your Agenda'
                        
if __name__=="__main__":
    conf={
        '/':{
            'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on':True
        }
    }
    WebService=Catalog()
    cherrypy.tree.mount(WebService,'/',conf)
    cherrypy.config.update({
    'server.socket_host' : '0.0.0.0',
    'server.socket_port' : 8080
    })
    cherrypy.engine.start()
    cherrypy.engine.block()
