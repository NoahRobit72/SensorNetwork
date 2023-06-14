import paho.mqtt.client as mqtt

broker = "192.168.12.32"
port = 1883
topic = "ESP"

client = mqtt.Client()
client.connect(broker, port, 60)


if __name__ == '__main__':
    message = input("Input a message: ")
    client.publish(topic, message)
