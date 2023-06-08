How to use MQTT to communicate between two devices.

1. First download mosquitto

pip install paho-mqtt

2. Go find the configuration file

The default setting for mosquitto is to have the broker on localhost. 

We need to find the configuration file called: "mosquitto.conf"

3. Once you find it, open it in vim and add the lines below:

allow_anonymous true
listener 1883 192.168.12.32

if you want to change the ip address to your adress change "192.168.12.32" -> your IP address

4. Run the reciever.py by typing:

python3 reciever.py

5. Run the sender.py by typing:

python3 reciever.py

6. All done


