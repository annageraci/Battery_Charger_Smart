To run the publishers' scripts inside Docker containers:
1) uncomment the line of code settings_file_path = '/app/settings/settings.json' (it should be line 11)
2) build the image as usual
3) when running the image:
   a) from Docker Desktop: it is necessary to declare the Battery_Charger_Smart folder path as 'host path', and '/app/settings' as 'container path'
   b) from command line: docker run -v [path of Battery_Charger_Smart]:/app/settings imageName