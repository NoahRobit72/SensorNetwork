import os,asyncio
import paho.mqtt.client as mqtt
from queue import Queue

# Sample async function to be used to processing inbound MQTT messages
async def function2():
    print("hi mom")
    await asyncio.sleep(1)
    
async def function1():
    print("hi dad")
    await asyncio.sleep(1)

# This gets called whenever we connect to the MQTT broker server
def mqtt_on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code "+str(rc))
    client.subscribe("ESP")

# This gets called whenever get get an MQTT message
def mqtt_on_message(client, userdata, msg):

    print(msg.topic+" " + msg.payload.decode())
    # data = json.loads(msg.payload.decode('utf-8'))
    # split_topic = msg.topic.split("/", 3)


async def main():
    mqtt_client=mqtt.Client()
    mqtt_client.on_connect=mqtt_on_connect
    mqtt_client.on_message=mqtt_on_message
    mqtt_client.connect("192.168.12.32",port=1883,keepalive=60)

    mqtt_client.loop_start()

    # In this case, loop forever.  q.get() will block if queue is empty.
    while True:
        await function1()
        await function2()


if __name__ == "__main__":
    # execute only if run as a script
    asyncio.run(main())