import paho.mqtt.client as mqtt

# MQTT broker information
broker = "localhost"
port = 1883
topic = "SensorData"

# Create MQTT client
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(topic)

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    #print(f"Received message: {message}")

def main():
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker, port, 60)
    client.loop_start()

    while True:
        message = input("Enter a message: ")
        client.publish(topic, message)

if __name__ == '__main__':
    main()
