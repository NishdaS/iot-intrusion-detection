""" HD LEVEL - 104791010 FATHIMA NISHDA MOHOMED SEMSAR """

#The client connects to an MQTT broker, authenticates using a username and password, 
#and handles real-time communication efficiently.

import paho.mqtt.client as mqtt  # the MQTT library to allow communication with the MQTT broker
import time  # to control the interval between published messages
import json  # to format the data into JSON before publishing
import tkinter as tk  # Importing Tkinter for GUI creation
from tkinter import scrolledtext  # Importing ScrolledText for message display

# Callback function for when a message is received from the subscriber
def on_message(client, userdata, message):
    payload = message.payload.decode('utf-8')
    # Insert the received message and its topic into the message area
    message_area.insert(tk.END, f"Received message: '{payload}' on topic: '{message.topic}'\n")
    message_area.see(tk.END)  # Automatically scroll to the bottom to show the latest message

# Add a list to hold published messages
published_messages = []

# MQTT Client class for the Client UI
class ClientUI:
    def __init__(self, client_id, broker, username, password):
        # Initialize the MQTT client with a unique client ID
        self.client = mqtt.Client(client_id)
        
        # Setting the username and password for MQTT broker authentication
        self.client.username_pw_set(username, password)
        self.client.connect(broker, 1883)

        self.client.on_message = on_message

    def subscribe_and_monitor(self):
        # Subscribe to private and public topics
        self.client.subscribe(f"{username}/traffic_patterns")  # Subscribe to the user's private traffic patterns
        self.client.subscribe("public/traffic_patterns")  # Subscribe to the public traffic patterns topic
        self.client.subscribe("public/#")  # Subscribe to all public topics
        self.client.loop_start()  # Start the MQTT client loop to handle incoming messages

    def publish_message(self, topic, message):
        # Publish a message to the specified topic in JSON format
        self.client.publish(topic, json.dumps(message))
        published_messages.append((topic, message))  # Store the message
        # Log the published message details
        if len(published_messages) > 10:  # Limit to last 10 messages
            published_messages.pop(0)
        message_area.insert(tk.END, f"Published message: {message} to topic: {topic}\n")
        message_area.see(tk.END)  # Scroll to the end

# Initializing the main window for the GUI
root = tk.Tk()
root.title("MQTT Client UI")  # Set the window title

# Creating UI components for topic input
topic_label = tk.Label(root, text="Topic")  # Label for topic input
topic_label.pack()
topic_entry = tk.Entry(root)  # Entry field for user to enter the topic
topic_entry.pack()

# Creating UI components for message input
message_label = tk.Label(root, text="Message")  # Label for message input
message_label.pack()
message_entry = tk.Entry(root)  # Entry field for user to enter the message
message_entry.pack()

# Creating a scrolled text area to display received messages and published messages
message_area = scrolledtext.ScrolledText(root, width=50, height=15)  # Scrolled text widget for displaying messages
message_area.pack(pady=5)

# Function to handle the publish button click
def on_publish():
    # Get the topic and message from the user input fields
    topic = topic_entry.get().strip()
    message_text = message_entry.get().strip()
    if not topic or not message_text:
        message_area.insert(tk.END, "Error: Topic and message cannot be empty.\n")
        message_area.see(tk.END)
        return  # Exit the function early if validation fails
    custom_message = {
        "msg": message_entry.get(),  # Get the custom message from the input field
        "timestamp": time.time()  # Add a timestamp for the published message
    }
    client_ui.publish_message(topic, custom_message)  # Call the publish method to send the message

# Creating a publish button and assign the on_publish function to it
publish_button = tk.Button(root, text="Publish", command=on_publish)
publish_button.pack(pady=5) #vertical padding

def on_subscribe():
    topic = subscribe_topic_entry.get().strip()
    if topic:
        client_ui.client.subscribe(topic)
        message_area.insert(tk.END, f"Subscribed to topic: '{topic}'\n")
        message_area.see(tk.END)

# Add UI components for subscribing
subscribe_topic_label = tk.Label(root, text="Subscribe to Topic")
subscribe_topic_label.pack()
subscribe_topic_entry = tk.Entry(root)
subscribe_topic_entry.pack()

#creating subscribe button
subscribe_button = tk.Button(root, text="Subscribe", command=on_subscribe)
subscribe_button.pack(pady=5) #vertical padding

# Start MQTT client and UI
# Defining the username (student ID) and broker address (server hosting the MQTT service)
username = "<104791010>"  
broker = "rule28.i4t.swin.edu.au"  # MQTT broker address
# The password is the same as the username 
password = username

# Creating an instance of the ClientUI class
client_ui = ClientUI("client_ui", broker, username, password)
client_ui.subscribe_and_monitor()  # Subscribe to topics and start monitoring

# Starting the GUI main loop
try:
    root.mainloop()  # Run the GUI loop until the window is closed
except KeyboardInterrupt:
    print("Exiting Client UI...")  # Print exit message on keyboard interrupt
