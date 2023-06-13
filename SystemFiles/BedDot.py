## This file will be hosted on the Bed Dot
## First Iteration will recieve MQTT Data, Write it to Influx
## This file is a combination of MQTTTest/reciever.py and InfluxTest/SinglePoint.py

import paho.mqtt.client as mqtt

import datetime
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import numpy as np
import socket



# MQTT broker information
broker = "192.168.12.32" # ip adress of the computer running the broker software
port = 1883
topic = "ESP"

# Influx init
bucket = "RemoteBucket4"
org = "sensorweb"
token = "YD02N-6cCD1XbHyU38urcCRdD4Jvnzie0itFvF9KMjUHc-ZpV2BPtM7qWM6n-MdgUGsHnEs_-GdZhZB37RnW8Q=="
url="http://localhost:8086"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)
write_api = client.write_api(write_options=SYNCHRONOUS)

# UDP init
host = "0.0.0.0"  # Listen on all available network interfaces
UDPport = 8888  # Port to listen on

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host, UDPport))


# Create MQTT client
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(topic)

# on the collection of a message
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    InfluxESP(message)
    
def UDPSearch():
    print("looking for messages on UDP port 8888")
    data, addr = sock.recvfrom(1024)
    message = data.decode()
    print(f"Received message: {message} from {addr[0]}:{addr[1]}")
    sock.close();



def main():
    client.on_connect = on_connect
    client.on_message = on_message
    
    UDPSearch();

    client.connect(broker, port, 60)
    client.loop_forever()

# should probally put this somewhere
    

# Function to write data to influx from ESP
# Data in the form: {"source" "epoch time" "tempature data" "humidity data"} ie. {ESP 2309402.230 23 49}
def InfluxESP(inputString):
    source, ept, tempature, humidity = ParseStringESP(inputString)
    utc = epoch_to_utc(ept)
    
    p = influxdb_client.Point("ChickenLab").tag("Source", source).field("temperature", float(tempature)).field("humidity", float(humidity)).time(utc)
    write_api.write(bucket=bucket, org=org, record=p)

# Function to parse the data from the ESP
def ParseStringESP(inputString):
    source, ept, tempature, humidity = inputString.split(" ")
    return source, ept, tempature, humidity

#Function to convert Epoch time to UTC Time
def epoch_to_utc(epoch_time):
    utc_time = datetime.datetime.utcfromtimestamp(int(epoch_time))
    return utc_time

# Function find the source
def FindSource(inputString):
    source = inputString.split(" ", 2)
    return source[0]

# Function to write data to influx from UDP
def InfluxUDP():
    print("hello")
    
def ParseStringUDP(inputString):
    dataArray = np.empty((50, 2))
    count = 0    
    dataPoints = inputString.split(",",2)
    pointsString = dataPoints[2].replace(",", "") 
    epochTime = float(dataPoints[1])
    pointsString = pointsString.strip(" ")
    stringArray = pointsString.split(" ")
        
    for a in stringArray:
        dataArray[count][1] = a
        dataArray[count][0] = epochTime
        epochTime+=.005
        count+=1  
    return dataArray


# # Function to write data to influx from serial
# def InfluxSerial():
#     print("hello")
    
if __name__ == '__main__':
    main()
