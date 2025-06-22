""" HD LEVEL - 104791010 FATHIMA NISHDA MOHOMED SEMSAR """
"""
This script implements an Intrusion Detection System (IDS) that listens for network traffic data
and evaluates it for suspicious patterns or high data sizes. It publish alerts or commands 
based on detected threats, such as high data sizes or connections from known malicious IP addresses.
"""

import paho.mqtt.client as mqtt # the MQTT library to allow communication with the MQTT broker
import json  # to format the data into JSON before publishing

# Defining suspicious patterns and thresholds
SUSPICIOUS_IPS = {"192.168.1.10", "192.168.1.20"}  # Examples of known malicious IPs
HIGH_DATA_SIZE_THRESHOLD = 1000  #Packet size threshold for alerts

# Callback function for when a message is received
def on_message(client, userdata, message):

    """
    Callback function that gets executed when a message is received on the subscribed topic.
    It checks incoming traffic data for suspicious patterns or high data sizes and takes action accordingly.
    """
     
    payload = message.payload.decode('utf-8')  # Decode the incoming message payload
    print(f"Received message: {payload} on topic: {message.topic}")  # Log the received message and topic
    print() #additional line break

    # Generating command based on traffic data
    try:
        traffic_data = json.loads(payload)
        # Check if the data size exceeds the defined threshold
        if traffic_data['data_size'] > 1000:
            # Create a command to enable logging for large packets
            command = {
                "action": "enable_logging", 
                "details": f"Alert: Large packet detected from IP {traffic_data['source_ip']} with size {traffic_data['data_size']} bytes."
            }
            client.publish(f"{username}/device_control", json.dumps(command))  # Publish the command to the device control topic
            print(f"Command sent to enable logging: {command}")
            print()
            
        # Check if the source IP is in the list of suspicious IPs
        elif traffic_data['source_ip'] in SUSPICIOUS_IPS:
            # Create an alert command for suspicious IPs
            command = {
                "action": "alert",
                "details": f"Alert: Suspicious IP detected: {traffic_data['source_ip']}."
            }
            client.publish(f"{username}/device_control", json.dumps(command))  # Publish the alert command
            print(f"Alert sent for suspicious IP: {command}") 
            print()

    except json.JSONDecodeError as e:
        # Handle JSON parsing errors
        print(f"Error decoding JSON: {e} for payload: {payload}")  # Log any JSON decode errors

# MQTT Client class for the IDS
class IntrusionDetectionSystem:
    def __init__(self, client_id, broker, username, password):
        self.client = mqtt.Client(client_id)
        # Setting the username and password for MQTT broker authentication
        self.client.username_pw_set(username, password)
        self.client.connect(broker)
        self.client.on_message = on_message

    def subscribe_to_traffic_patterns(self):
        # Subscribe to the network traffic topic
        self.client.subscribe(f"{username}/traffic_patterns")
        self.client.loop_start()

if __name__ == "__main__":
    # Start MQTT client and UI
    # Defining the username (student ID) and broker address (server hosting the MQTT service)
    username = "<104791010>"  
    broker = "rule28.i4t.swin.edu.au"  # MQTT broker address
    # The password is the same as the username 
    password = username

    # Create an instance of the IntrusionDetectionSystem
    ids = IntrusionDetectionSystem("ids", broker, username, password)
    ids.subscribe_to_traffic_patterns()  # Subscribe to the traffic patterns topic

    try:
        print("Intrusion Detection System is running. Press Ctrl+C to exit.")  # Inform user that the IDS is running
        print()
        while True:
            pass  # Keep the script running to continuously listen for messages
    except KeyboardInterrupt:
        print("Exiting Intrusion Detection System...")  # Print exit message on keyboard interrupt