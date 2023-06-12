from datetime import datetime
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

bucket = "RemoteBucket2"
org = "sensorweb"
token = "YD02N-6cCD1XbHyU38urcCRdD4Jvnzie0itFvF9KMjUHc-ZpV2BPtM7qWM6n-MdgUGsHnEs_-GdZhZB37RnW8Q=="
# Store the URL of your InfluxDB instance
url="http://localhost:8086"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

# Write script
write_api = client.write_api(write_options=SYNCHRONOUS)

p = influxdb_client.Point("my_measurement").tag("location", "MQTT").field("temperature", 29.3).field("humidity", 999.3).time("2023-06-12 21:57:00.001643")
write_api.write(bucket=bucket, org=org, record=p)