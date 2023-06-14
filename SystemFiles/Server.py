# MQTT Data format:
#
# ESP: ESP epoch     temp  humid
"""
ESP 1686580202.219 23 90
"""
#
# UDP: UDP epoch {25 data points}
"""
UDP 1686580202.219 -4436 5165 -8075 -35197 -15986 41045 65818 42310 21581 26642 38232 38036 45285 17019 -1216 14817 27802 24512 12286 22171 32239 20882 14934 17857 29023 
"""
#
# Serial:
# Serial
import paho.mqtt.client as mqtt
import asyncio
import datetime
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import numpy as np
import socket

import paho.mqtt.client as mqtt

# MQTT broker information
broker = "192.168.12.32"
port = 1883
topic = "SensorData"

# Create MQTT client
client = mqtt.Client()

# Influx init
bucket = "RemoteBucket10"
org = "sensorweb"
token = "YD02N-6cCD1XbHyU38urcCRdD4Jvnzie0itFvF9KMjUHc-ZpV2BPtM7qWM6n-MdgUGsHnEs_-GdZhZB37RnW8Q=="
url="http://localhost:8086"

clientDB = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)
write_api = clientDB.write_api(write_options=SYNCHRONOUS)

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(topic)

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Received message: {message}")
    ParseMessage(message)

def main():
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker, port, 60)
    client.loop_forever()
    
def ParseMessage(inputString):
    source = inputString.split(" ", 2)[0]
    if(source == "ESP"):
        InfluxESP(inputString)
    elif(source == "UDP"):
        InfluxUDP(inputString)
    else:
        print("hi")
        
        
# Writing Functions

# Data in the form: {"source" "epoch time" "tempature data" "humidity data"} ie. {ESP 2309402.230 23 49}
def InfluxESP(inputString):
    source, ept, tempature, humidity = ParseStringESP(inputString)
    p = influxdb_client.Point("ChickenLab").tag("Source", source).field("temperature", float(tempature)).field("humidity", float(humidity))
    write_api.write(bucket=bucket, org=org, record=p)
    print("Data Packet sent to: ", source)
    
def InfluxUDP(inputString):
    # print("welcome to the UDP Sender")
    # print("this is the input string:", inputString)
    source = "UDP"
    dataArray = ParseStringUDP(inputString)
    for i in range(len(dataArray)-1):
        p = influxdb_client.Point("ChickenLab").tag("Source", source).field("Seismic", float(dataArray[i][1])) # Index could be wrong here
        write_api.write(bucket=bucket, org=org, record=p)
    print("Data Packet sent to: ", source)




#Parsing Function:

# Function to parse the data from the ESP
def ParseStringESP(inputString):
    source, ept, tempature, humidity = inputString.split(" ")
    return source, ept, tempature, humidity


def ParseStringUDP(inputString):
    dataArray = np.empty((24, 2))
    parsedString = inputString.split()
    dataPoints = parsedString[1:26]
    
    for i in range(len(dataArray)-1):
        dataArray[i][1] = dataPoints[i]
        dataArray[i][0] = 0 # could put time here in the future    
    return dataArray


if __name__ == '__main__':
    main()




