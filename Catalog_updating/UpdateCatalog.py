import json
import random
import time
import cherrypy
import requests

class CheckUpdate():

    def __init__(self,url):
        self.url=url
        response= requests.get(self.url+'/AllDevices')
        self.response_json_alldevices = response.json()
        response_user=requests.get(self.url+"/AllUsers")
        self.response_json_allusers=response_user.json()



    def makerequest(self):
        for currentDevice in self.response_json_alldevices:
            lastUpDate=int(currentDevice['lastUpDate'])
            dif=int(time.time()-lastUpDate)
            if dif>120:
                self.response_json_alldevices.remove(currentDevice)
            else:
                for currentUser in self.response_json_allusers:
                    if currentDevice['UserAssociationID']==currentUser['UserID']:
                        for currentDeviceOfTheUser in currentUser['ConnectedDevices']:
                            if currentDevice['DeviceID']==currentDeviceOfTheUser['DeviceID']:
                                currentUser['ConnectedDevices'].remove(currentDeviceOfTheUser)


        print('the new device list is: '+json.dumps(self.response_json_alldevices))

        # aggiornare il catalogo 
        response= requests.get(self.url+'/catalog')
        catalog = response.json()
        catalog['DeviceList']=self.response_json_alldevices
        catalog['UserList']=self.response_json_allusers
        json.dump(catalog, open('../Catalog.json', 'w'), indent=2)

if __name__ == '__main__':
    while True:
        Catalog=json.load(open('../settings.json'))
        URL=Catalog['Catalog_url_Anna']
        URL='http://127.0.0.1:8080'
        #URL=Catalog['DockerIP']
        daily=CheckUpdate(URL)
        daily.makerequest()
        time.sleep(60)
