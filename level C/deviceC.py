""" HD LEVEL - 104791010 FATHIMA NISHDA MOHOMED SEMSAR """

# This script simulates Device C, which acts as an MQTT client that:
# 1. Connects to a specified MQTT broker for communication.
# 2. Subscribes to a public topic (`public/traffic_patterns`) to receive network traffic data.
# 3. Listens for incoming messages and processes the received data:
#    - If the data indicates TCP traffic, it publishes a command to a control topic (`<username>/device_control`) based on the received information.
# 4. Logs all received messages and published commands to the console for monitoring purposes.

# The script runs indefinitely, continuously listening for messages until interrupted by the user (e.g., via a keyboard interrupt).


import paho.mqtt.client as mqtt # the MQTT library to allow communication with the MQTT broker
import json # to format the data into JSON before publishing

class DeviceC:
    def __init__(self, client_id, broker, username, password):
        
        # Initialize the MQTT client for Device C
        print("Initializing Device C...")

        # Create a new MQTT client instance with a unique client ID
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

    def on_message(self, client, userdata, message):
        # Decode the received message payload from bytes to string format
        payload = message.payload.decode('utf-8')
        print(f"Device C received message: '{payload}' on topic: '{message.topic}'")  # Log received message
        print()

        try:
            # Attempt to parse the received JSON data
            traffic_data = json.loads(payload)
            # Check if the traffic protocol is TCP
            if traffic_data['protocol'] == "TCP":
                print(f"Device C has detected TCP traffic: {traffic_data}")  # Log detection of TCP traffic
                print()

                # Publish a command based on the received data
                command = {"action": "process_tcp", "details": traffic_data}
                self.publish_command(command)  # Publish the generated command
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e} for payload: {payload}")
            print()

    def publish_command(self, command):
        # Define the topic for sending control commands
        command_topic = f"{username}/device_control"  
        # Publish the command as a JSON string to the control topic
        self.client.publish(command_topic, json.dumps(command))
        # If Device C detects TCP traffic, it generates a command and publishes it to the username/device_control topic.
        print(f"Device C published command: {json.dumps(command)} to topic: {command_topic}")
        print() 

    def subscribe_topics(self):
        # Subscribe to the public traffic patterns topic to receive data
        self.client.subscribe("public/traffic_patterns")
        print("Device C subscribed to topic: public/traffic_patterns")
        print()
        
        # Start the MQTT client loop to handle incoming messages
        self.client.loop_start()  
        print("Device C is now listening for messages...")
        print()

if __name__ == "__main__":
    # Defining the username (student ID) and broker address (server hosting the MQTT service)
    username = "<104791010>"  
    broker = "rule28.i4t.swin.edu.au"  # MQTT broker address
    # The password is the same as the username 
    password = username
    # Creating an instance of DeviceC with the client ID "device_c", broker address, and credentials
    device_c = DeviceC("device_c", broker, username, password)

    try:
        # Keep the script running indefinitely to listen for messages
        while True:
            pass  # Infinite loop to keep the program alive
    except KeyboardInterrupt:
        # Gracefully exit the script on keyboard interrupt
        print("Exiting Device C...")  # Log exit message
        device_c.client.loop_stop()    # Stop the MQTT loop gracefully
        print("Device C has been shut down.")  # Confirm shutdown