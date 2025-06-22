import paho.mqtt.client as mqtt
import time
import random
import json

# Function to simulate network traffic data
def simulate_network_traffic():
    return {
        "source_ip": f"192.168.1.{random.randint(1, 254)}",
        "destination_ip": f"192.168.1.{random.randint(1, 254)}",
        "protocol": random.choice(["TCP", "UDP"]),
        "data_size": random.randint(64, 1500)  # Simulating packet size
    }

# Callback function for when a message is received
def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    traffic_data = json.loads(payload)
    print(f"Received message: {traffic_data} on topic: {message.topic}")

# MQTT Client class
class NetworkTrafficMonitor:
    def __init__(self, client_id, broker, username, password):
        self.client = mqtt.Client(client_id)
        self.client.username_pw_set(username, password)
        self.client.connect(broker)

        # Set the message callback function
        self.client.on_message = on_message
        
        # Subscribe to the public topic
        self.client.subscribe("public/#")  # Subscribe to all sub-topics of public

    def publish_network_traffic(self):
        while True:
            traffic_data = simulate_network_traffic()
            self.client.publish(f"{username}/network_traffic", json.dumps(traffic_data))
            print(f"Published network traffic: {traffic_data}")  # This should be correct
            time.sleep(5)  # Publish every 5 seconds

            
            # Process MQTT loop to handle incoming messages
            self.client.loop()  # Keep the client loop running

if __name__ == "__main__":
    username = "<104791010>"
    broker = "rule28.i4t.swin.edu.au"
    password = username  # Same as username

    monitor = NetworkTrafficMonitor("network_traffic_monitor", broker, username, password)
    monitor.publish_network_traffic()
