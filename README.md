"# Battery_Charger_Smart" 

DOCKER instruction: 
To run the scripts inside Docker containers:
1) uncomment the line of code correspondent to the access to the file setting.json: settings=json.load(open('/app/settings/settings.json'))
2) build the image as usual
3) when running the image:
   a) from Docker Desktop: it is necessary to declare the Battery_Charger_Smart folder path as 'host path', and '/app/settings' as 'container path'
   b) from command line: docker run -v [path of Battery_Charger_Smart]:/app/settings imageName

To access to the catalog, if the CatalogServer is run in a Docker container: 
1) run the image of the Catalog_Server with the command line: sudo docker run --name [name to identifie the container] -d -p 8080:80 nameImage !container, is an instance of the image in execution!
2) The other application could access to the catalog server and so to the Catalog, only through the IP where the container is running and the port 8080. To know the IP address use: docker inspect [container id or name].
3) Verify that it is the one reported in the configuration file, setting.json, as value of the key 'DockerIP'; if not update the file.
4) uncomment the line that set the URL of get, put, or post request, with the correct IP.
5) build the image as usual.
6) when running the image:
   a) from Docker Desktop: it is necessary to declare the Battery_Charger_Smart folder path as 'host path', and '/app/settings' as 'container path'
   b) from command line: docker run -v [path of Battery_Charger_Smart]:/app/settings imageName

Each folder corresponds to an application, and contain a DockerFile


