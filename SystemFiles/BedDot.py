## This file will be hosted on the Bed Dot
## First Iteration will recieve MQTT Data, Write it to Influx
## This file is a combination of MQTTTest/reciever.py and InfluxTest/SinglePoint.py

import paho.mqtt.client as mqtt
import asyncio
import datetime
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import numpy as np
import socket

# MQTT broker information
broker = "192.168.12.32"
port = 1883
topic = "ESP"

# Create MQTT client
client = mqtt.Client()

# Influx init
bucket = "RemoteBucket8"
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
UDPport = 8887  # Port to listen on


# Queue
queue = []

# This gets called whenever we connect to the MQTT broker server
def mqtt_on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code "+str(rc))
    client.subscribe("ESP")

# This gets called whenever get get an MQTT message
def mqtt_on_message(client, userdata, msg):
    message = msg.payload.decode()
    print("I am in the on message function and the message is:", message)
    queue.append(message)

    
async def UDPSearch():
    print("Entered the DUP Search Function")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, UDPport))
    print("Looking for messages on UDP port 8888")
    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode()
        queue.append(message)
        
        await asyncio.sleep(.1) 
        # print(f"Received message: {message} from {addr[0]}:{addr[1]}")

    sock.close();
    
def writeResponse(message):
    f.write(message+ "\n")     
 
# If queue is not empty, pop front and insert it     
async def DeQueue():
    print("Entered the De Queue Function")
    while True:
        # print("The length of the queue is:", len(queue))
        if(len(queue) >= 1):
            data = queue.pop(0)
            print("I am in the deque stage and I am popping off: ", data)
            source = FindSource(data)
            print(source)
            if(source == "ESP"):
                print("Sending data to ESP sender")
                InfluxESP(data)
            else:
                # print("Sending data to UDP sender")
                InfluxUDP(data)
        await asyncio.sleep(.01)

async def main():
    mqtt_client=mqtt.Client()
    mqtt_client.on_connect=mqtt_on_connect
    mqtt_client.on_message=mqtt_on_message
    mqtt_client.connect("192.168.12.32",port=1883,keepalive=60)

    mqtt_client.loop_start()

    # In this case, loop forever.  q.get() will block if queue is empty.
    while True:
        await DeQueue()
        await UDPSearch()
    

# Function to write data to influx from ESP
# Data in the form: {"source" "epoch time" "tempature data" "humidity data"} ie. {ESP 2309402.230 23 49}
def InfluxESP(inputString):
    print("entered the influxESP script")
    source, ept, tempature, humidity = ParseStringESP(inputString)
    utc = epoch_to_utc(ept)
    p = influxdb_client.Point("ChickenLab").tag("Source", source).field("temperature", float(tempature)).field("humidity", float(humidity))
    write_api.write(bucket=bucket, org=org, record=p)
    print("Data Packet sent to: ", source)

# Function to parse the data from the ESP
def ParseStringESP(inputString):
    source, ept, tempature, humidity = inputString.split(" ")
    return source, ept, tempature, humidity

#Function to convert Epoch time to UTC Time
def epoch_to_utc(epoch_time):
    utc_time = datetime.datetime.utcfromtimestamp(float(epoch_time))
    return utc_time

# Function find the source
def FindSource(inputString):
    print("I am in the find source passage and the inputString is: ", inputString)
    splitString = inputString.split(" ", 2)
    print("I am in the find source passage and the source is: ", splitString[0])
    if(splitString[0]!= "ESP"):
        source = "UDP"
        return source
    
    source = splitString[0]
    return source

# Function to write data to influx from UDP
def InfluxUDP(inputString):
    # print("welcome to the UDP Sender")
    # print("this is the input string:", inputString)
    source = FindSource(inputString)
    dataArray = ParseStringUDP(inputString)
    for i in range(len(dataArray)-1):
        p = influxdb_client.Point("ChickenLab").tag("Source", source).field("Seismic", float(dataArray[i][1])) # Index could be wrong here
        # print("printing the data as: data, time: ",(dataArray[i][1]), epoch_to_utc(dataArray[i][0]))
        write_api.write(bucket=bucket, org=org, record=p)
    #print("Data Packet sent to: ", source)

    
def ParseStringUDP(inputString):
    dataArray = np.empty((24, 2))
    
    dataPoints = inputString.split(",",2)
    print("I am in the ParseStringUDP, and the input string is", inputString)
    print("The length of dataPoints is:", len(dataPoints))
    pointsString = dataPoints[2].replace(",", "") 
    epochTime = float(dataPoints[1])
    
    pointsString = pointsString.strip(" ")
    pointsString = pointsString.strip("}")
    stringArray = pointsString.split(" ")
    
    for i in range(len(dataArray)-1):
        dataArray[i][1] = stringArray[i]
        dataArray[i][0] = epochTime
        epochTime+=.01  
    
    return dataArray
    
if __name__ == '__main__':
    asyncio.run(main())
    

