import paho.mqtt.client as mqtt
from pykafka import KafkaClient
import time

# MQTT broker details
broker_address = "localhost"
broker_port = 1883
topic = "trucks\data"
client = 0

class MQTT:
    def __init__(self):
        global client
        # Create an MQTT client instance
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,)
        #username = "your_username"
        #password = "your_password"
        # Set username and password for authentication (if required)
        #client.username_pw_set(username, password)
        
        # Connect to the broker
        client.connect(broker_address, broker_port)

    def Publish(self, data):
        # Convert JSON data to string
        #json_data = json.dumps(data)

        # Publish JSON data to the specified topic
        client.publish(topic, data)

    def Disconnect(self):
        # Disconnect from the broker
        client.disconnect()