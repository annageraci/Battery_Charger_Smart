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
        # The list of Device Deleted 
        self.RemainDevice=[]

    def makerequest(self):
        for currentDevice in self.response_json_alldevices:
            lastUpDate=int(currentDevice['lastUpDate'])
            dif=int(time.time()-lastUpDate)
            if dif<120:
                self.RemainDevice.append(currentDevice)
        print('the new device list is '+json.dumps(self.RemainDevice))

        # aggiornare il catalogo 
        response= requests.get(self.url+'/catalog')
        catalog = response.json()
        catalog['DeviceList']=self.RemainDevice
        json.dump(catalog, open('CatalogFake.json', 'w'), indent=2)
        # json.dump(catalog, open('Catalog.json', 'w'), indent=2)

if __name__ == '__main__':
    while True:
        Catalog=json.load(open('settings.json'))
        URL=Catalog['Catalog_url']
        #URL=Catalog['DockerIP']
        daily=CheckUpdate(URL)
        daily.makerequest()
        time.sleep(60)
