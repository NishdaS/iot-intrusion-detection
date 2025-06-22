""" This script will act as the MQTT client that subscribes to 
the topic where the network traffic data is published. 
It will receive and display the data, and potentially perform some analysis."""
import paho.mqtt.client as mqtt
import json

# Callback function for when a message is received
def on_message(client, userdata, message):
    # Decode the message payload
    payload = message.payload.decode('utf-8')
    print(f"Raw message received: {payload} on topic: {message.topic}")  # Add this line for debugging
    try:
        traffic_data = json.loads(payload)  # Convert the JSON string to a dictionary
        print(f"Received message: {traffic_data} on topic: {message.topic}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e} for payload: {payload}")  # Print the error and payload


# MQTT Client class
class TrafficSubscriber:
    def __init__(self, client_id, broker, username, password):
        self.client = mqtt.Client(client_id)
        self.client.username_pw_set(username, password)
        self.client.connect(broker)

        # Set the message callback function
        self.client.on_message = on_message
    
    def subscribe_topics(self):
        # Subscribe to the private topic
        self.client.subscribe(f"{username}/network_traffic")
        # Subscribe to the public topic
        self.client.subscribe("public/#")  # Subscribe to all sub-topics of public
        self.client.loop_start()  # Start the MQTT client loop

if __name__ == "__main__":
    username = "<104791010>"
    broker = "rule28.i4t.swin.edu.au"
    password = username  # Same as username

    subscriber = TrafficSubscriber("traffic_subscriber", broker, username, password)
    subscriber.subscribe_topics()

    # Keep the script running to listen for messages
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Exiting...")
