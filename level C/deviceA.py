""" HD LEVEL - 104791010 FATHIMA NISHDA MOHOMED SEMSAR """

# This script simulates a network device (DeviceA) that connects to an MQTT broker
# and continuously publishes random network traffic data to two topics:
# 1. A private topic, which is specific to the device/user.
# 2. A public topic that other devices can access.
# It also subscribes to a control topic and wildcard topic to receive and process commands.
# The script leverages MQTT for message publishing and receiving, and it formats the data as JSON.
# Messages are sent every 5 seconds, and each message includes a timestamp.
# The script runs in an infinite loop, simulating continuous network traffic.

import paho.mqtt.client as mqtt # the MQTT library to allow communication with the MQTT broker
import time # to control the interval between published messages
import random # to generate random data for network traffic
import json # to format the data into JSON before publishing
from datetime import datetime  # Added to timestamp the messages

# Defining the DeviceA class -  represents a network device
class DeviceA:
    
    # Initializing the device with the client ID, broker address, username, and password
    def __init__(self, client_id, broker, username, password):
        # Initialize the MQTT client for Device A
        print("Initializing Device A...")
        
        # Create a new MQTT client instance with a unique client_id
        self.client = mqtt.Client(client_id)
        
        # Setting the username and password for connecting to the broker (authentication)
        self.client.username_pw_set(username, password)
        
        # Attempt to connect to the MQTT broker
        try:
            self.client.connect(broker, 1883)
            print(f"Connected to MQTT broker at {broker} on port 1883") # If success
        except Exception as e:
            print(f"Failed to connect to MQTT broker: {e}")
            exit(1)  # Exit if connection fails
        
        # Set a callback for when a message is received
        # This means whenever a subscribed topic receives a message, the on_message function will be triggered
        self.client.on_message = self.on_message
        
        # Call the function to subscribe to topics
        self.subscribe_topics()

    # Function to subscribe to specific topics
    def subscribe_topics(self):
        # Subscribe to the "public/device_control" topic to receive commands
        self.client.subscribe("public/device_control")
        self.client.subscribe("public/#")  # to all public topics
        
        # Start the MQTT client loop to continuously check for incoming messages
        self.client.loop_start()

    # Callback function to handle incoming messages
    def on_message(self, client, userdata, message):
        # Decode the message payload from bytes to a string (UTF-8 format)
        payload = message.payload.decode('utf-8')
        
        # Print out the received message and the topic it was sent to, including a timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Print out the received message and the topic it was sent to
        print(f"[{timestamp}] Device A received command: '{payload}' on topic: {message.topic}")
        print() # Additional Linebreak

    # Function to simulate network traffic data
    def generate_traffic_data(self):
        # Return a dictionary simulating random network traffic details (source/destination IP, protocol, data size)
        return {
            "source_ip": f"192.168.1.{random.randint(1, 254)}",  # Random source IP address
            "destination_ip": f"192.168.1.{random.randint(1, 254)}",  # Random destination IP address
            "protocol": random.choice(["TCP", "UDP"]),  # Randomly choose between TCP or UDP protocols
            "data_size": random.randint(64, 1500)  # Simulating a random packet size between 64 and 1500 bytes
        }

    # Function to publish simulated network traffic data to MQTT topics
    def publish_traffic_patterns(self):
        # Continuous loop to repeatedly publish data every 5 seconds
        while True:
            # Generate random traffic data using the generate_traffic_data function
            traffic_data = self.generate_traffic_data()

            # Convert the data to JSON format
            traffic_data_json = json.dumps(traffic_data)

            # Get the current timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Publish the generated traffic data to the private topic (username-specific)
            self.client.publish(f"{username}/traffic_patterns", json.dumps(traffic_data))  # Convert data to JSON
            print(f"[{timestamp}] Device A published to private topic '{username}/traffic_patterns': {traffic_data}")
            print() # Additional Linebreak

            # Publish the same data to the public topic where other devices can access it
            self.client.publish("public/traffic_patterns", json.dumps(traffic_data))  # Convert data to JSON
            print(f"[{timestamp}] Device A published to public topic 'public/traffic_patterns': {traffic_data}")
            print() # Additional Linebreak

            # Wait for 5 seconds before publishing the next set of data
            time.sleep(5)
            

# Main block to execute the code
if __name__ == "__main__":
    # Defining the username (student ID) and broker address (server hosting the MQTT service)
    username = "<104791010>"  
    broker = "rule28.i4t.swin.edu.au"  # MQTT broker address
    
    # The password is the same as the username 
    password = username
    
    # Creating an instance of DeviceA with the client ID "device_a", broker address, and credentials
    device_a = DeviceA("device_a", broker, username, password)
    
    # Start publishing network traffic data
    try:
        device_a.publish_traffic_patterns()
    except KeyboardInterrupt:
        print("[INFO] Exiting Device A...")
        device_a.client.loop_stop()  # Stop the MQTT loop gracefully
        print("[INFO] Device A has shut down.")
    
    