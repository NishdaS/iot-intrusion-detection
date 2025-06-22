""" HD LEVEL - 104791010 FATHIMA NISHDA MOHOMED SEMSAR """

# This script implements Device B, which connects to an MQTT broker 
# and subscribes to a private topic to receive network traffic data 
# published by Device A. It processes incoming messages
# The script uses MQTT for message subscription and handles messages 
# by printing the received data to the console. Device B runs 
# indefinitely, listening for messages until interrupted by the user.

import paho.mqtt.client as mqtt # the MQTT library to allow communication with the MQTT broker
import time # to control the interval between published messages
import json # to format the data into JSON before publishing

class DeviceB:
    def __init__(self, client_id, broker, username, password):
        # Initialize the MQTT client for Device B
        print("Initializing Device B...")

        # Create a new MQTT client instance with a unique client_id
        self.client = mqtt.Client(client_id)

        # Setting the username and password for MQTT broker authentication
        self.client.username_pw_set(username, password)
        self.client.connect(broker, 1883)

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

    #processes incoming messages from the username/traffic_patterns topic and prints them to the console.
    def on_message(self, client, userdata, message):
        # Decode the message payload from bytes to a string
        payload = message.payload.decode('utf-8')

        # Print the received message along with its topic
        print(f"[INFO] Device B received message: '{payload}' on topic: '{message.topic}'")
        print()

    def subscribe_topics(self):
        # Subscribe to the private topic specific to the user
        self.client.subscribe(f"{username}/traffic_patterns")  # private topic
        print(f"[INFO] Device B subscribed to topic: '{username}/traffic_patterns'")
        print()
        
        # Start the MQTT client loop to handle incoming messages
        self.client.loop_start()  
        print("[INFO] Device B is now listening for messages...")
        print()


if __name__ == "__main__":
    # Defining the username (student ID) and broker address (server hosting the MQTT service)
    username = "<104791010>"  
    broker = "rule28.i4t.swin.edu.au"  # MQTT broker address
    # The password is the same as the username 
    password = username
    # Creating an instance of DeviceB with the client ID "device_b", broker address, and credentials
    device_b = DeviceB("device_b", broker, username, password)

    try:
        # Keep the script running indefinitely to listen for messages
        while True:
            time.sleep(1)  # Prevent the script from exiting
    except KeyboardInterrupt:
        # Gracefully exit the script on keyboard interrupt
        print("[INFO] Exiting Device B...") # Log exit message
        device_b.client.loop_stop()  # Stop the MQTT loop gracefully
        print("[INFO] Device B has shut down.") # Confirm shutdown
 