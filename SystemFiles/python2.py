import paho.mqtt.client as mqtt

# Influx imports
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# MQTT broker information
broker = "192.168.12.32"
port = 1883
topic = "chat"

# InFlux Info
token = os.environ.get("INFLUXDB_TOKEN")
org = "sensorweb"
url = "http://localhost:8086"
write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
bucket="RemoteBucket1"

write_api = write_client.write_api(write_options=SYNCHRONOUS)



# Function to send a datapoint to the influx database
def sendDataPoint(message):
    SmValue = int(message)
    print("sending data to influx... with with value: " ,SmValue)

    point = (
        Point("census")
        .tag("location", "Sensor1")
        .field("Tempature", SmValue)
    )
    write_api.write(bucket=bucket, org=org, record=point)
    
        

    
# Create MQTT client
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(topic)

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    # print(f"Received message: {message}")
    sendDataPoint(message)

def main():
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker, port, 60)
    client.loop_forever()

if __name__ == '__main__':
    main()
