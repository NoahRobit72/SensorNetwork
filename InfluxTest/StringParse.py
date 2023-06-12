## this script will parse an input and save the values of the string as elements in an array
# Influx imports
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# InFlux Info
token = os.environ.get("INFLUXDB_TOKEN")
org = "sensorweb"
url = "http://localhost:8086"
write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
bucket="RemoteBucket1"

write_api = write_client.write_api(write_options=SYNCHRONOUS)


def parseString(inputString):
    dataArray = []
    dataPoints = inputString.split(",",2)
    pointsString = dataPoints[2].replace(",", "") 
    pointsString = pointsString.strip(" ")
    stringArray = pointsString.split(" ")
     
    print(len(stringArray))
    print(stringArray)
    
    for a in stringArray:
        sendDataPoint(a)
    
    return dataArray

# Function to send a datapoint to the influx database
def sendDataPoint(message):
    SmValue = int(message)

    point = (
        Point("census")
        .tag("location", "Sensor1")
        .field("Tempature", SmValue)
    )
    write_api.write(bucket=bucket, org=org, record=point)
    



parseString("'SHZ', 1507760140.530, 614, 916, 1095, 1156, 839, 923, 861, 856, 861, 789, 568, 823, 965, 788, 835, 991, 1028, 1225, 1142, 828, 682, 635, 771, 978, 834, 1167, 1116, 888, 627, 564, 944, 994, 780, 652, 811, 915, 832, 1134, 1020, 594, 756, 782, 748, 810, 864, 936, 977, 1014, 676, 502")