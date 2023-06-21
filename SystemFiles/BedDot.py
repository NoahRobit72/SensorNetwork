## This file will be hosted on the Bed Dot
## First Iteration will recieve MQTT Data, Write it to Influx
## This file is a combination of MQTTTest/reciever.py and InfluxTest/SinglePoint.py

import paho.mqtt.client as mqtt
import datetime
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import numpy as np
import socket
import sys

# MQTT broker information
broker = ""
port = 1883
topic = "SensorData"

# Create MQTT client
client = mqtt.Client()


# Influx init
bucket = "RemoteBucket9"
org = "sensorweb"
token = "YD02N-6cCD1XbHyU38urcCRdD4Jvnzie0itFvF9KMjUHc-ZpV2BPtM7qWM6n-MdgUGsHnEs_-GdZhZB37RnW8Q=="
url="http://localhost:8086"

clientDB = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)
write_api = clientDB.write_api(write_options=SYNCHRONOUS)

# UDP init
host = "0.0.0.0"  # Listen on all available network interfaces
UDPport = 8888  # Port to listen on

#Mqtt
broker = "localhost"
port = 1883
topic = "SensorData"

client = mqtt.Client()
client.connect(broker, port, 60)


def UDPSearch():
    print("Entered the DUP Search Function")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, UDPport))
    print("Looking for messages on UDP port 8888")
    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode()
        InfluxUDP(message)
        #print(f"Received message: {message} from {addr[0]}:{addr[1]}")
    sock.close();

def SerialSearch():
    print("Searching for Serial")

def main():
    if (sys.argv[1] == "RShake"):
        UDPSearch()
    else:
        SerialSearch()
        

# Function to write data to influx from UDP
def InfluxUDP(inputString):
    # print("welcome to the UDP Sender")
    # print("this is the input string:", inputString)
    source = "UDP"
    dataArray = ParseStringUDP(inputString)
    for i in range(len(dataArray)-1):
        p = influxdb_client.Point("ChickenLab").tag("Source", source).field("Seismic", float(dataArray[i][1])) # Index could be wrong here
        # print("printing the data as: data: ",(dataArray[i][1]))
        write_api.write(bucket=bucket, org=org, record=p)
    print("Data Packet sent from: ", source)

    
def ParseStringUDP(inputString):
    dataArray = np.empty((24, 2))
    
    dataPoints = inputString.split(",",2)
    pointsString = dataPoints[2].replace(",", "") 
    
    epochTime = float(dataPoints[1])
    
    MQTTString = "UDP " + str(epochTime)  + pointsString # probally not the greatest place to send this but thats a later problem...
    client.publish(topic, MQTTString) # also not a great place but fuck it
    
    pointsString = pointsString.strip(" ")
    pointsString = pointsString.strip("}")
    stringArray = pointsString.split(" ")
    
    for i in range(len(dataArray)-1):
        dataArray[i][1] = stringArray[i]
        dataArray[i][0] = epochTime
        epochTime+=.01  
    
    return dataArray
    
if __name__ == '__main__':
    main()
    

