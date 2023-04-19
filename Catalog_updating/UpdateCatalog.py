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
        self.NumberofDevice=len(self.response_json_alldevices)
        self.devdel=[]

    def makerequest(self):
        for i in range(self.NumberofDevice):
            output=self.response_json_alldevices
            lastUpDate=int(self.response_json_alldevices[i]['lastUpDate'])
            dif=int(time.time()-lastUpDate)
            if dif>120:
                self.devdel.append(i)
        self.devdel.reverse()
        for i in range(len(self.devdel)):
            output.pop(self.devdel[i])
        print(output)

        # aggiornare il catalogo 
        response= requests.get(self.url+'/catalog')
        catalog = response.json()
        catalog['DeviceList']=output
        json.dump(catalog, open('setting.json', 'w'), indent=2)
        # json.dump(catalog, open('Catalog.json', 'w'), indent=2)

if __name__ == '__main__':
    while True:
        Catalog=json.load(open('settings.json'))
        #URL=Catalog['Catalog_url']
        URL=Catalog['DockerIP']
        daily=CheckUpdate(URL)
        daily.makerequest()
        time.sleep(60)
