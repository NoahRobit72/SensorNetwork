This is a pair of scripts to test MQTT and influx DB 

THe python1.py script will be hosted on the raspberry pi and will collect sensor data (via serial port, MQTT, or UPT). It will then send the data via MQTT to the cloud.

The python2.py script will be hosted in the cloud and will recieve the data from the python1.py script. This script will then write the data to the local influx db that is hosted on sensorweb.us