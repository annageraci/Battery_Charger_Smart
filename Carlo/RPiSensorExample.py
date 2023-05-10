import time
import datetime
import board
import adafruit_dht
import RPi.GPIO as gpio

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D4, use_pulseio=False)

filename = "temp_log.csv"

# Create header row in new CSV file
csv = open(filename, 'w')
csv.write("Timestamp,Temperature\n")
csv.close

for i in range(-1):
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )
       
        temp_c = str(temperature_c)
        entry = str(datetime.datetime.now())
        entry = entry + "," + temp_c + "\n"

        # Log (append) entry into file
        csv = open(filename, 'a')
        try:
            csv.write(entry)
        finally:
            csv.close()

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just             #        keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)

#print csv
csv = open(filename, 'r')
print(csv.read())
csv.close()

#cleanup gpio
gpio.cleanup()