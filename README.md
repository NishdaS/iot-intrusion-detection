

# IoT-Based Intrusion Detection System

This project implements an Internet of Things (IoT) infrastructure using the MQTT (Message Queuing Telemetry Transport) protocol to simulate device communication and detect potential security threats through a lightweight Intrusion Detection System (IDS). The system is built using Python and focuses on simulating traffic from IoT devices, generating normal and anomalous data, and detecting threats in real time.

## Project Overview

The system includes multiple Python-based IoT device simulations communicating over an MQTT broker hosted on Swinburne's infrastructure. It includes:
- Devices that publish sensor data
- Devices that subscribe to and process messages
- A hybrid device that publishes and subscribes
- A Python-based user interface to monitor devices and send commands
- A basic Intrusion Detection System (IDS) that flags anomalies in traffic
- A detailed cybersecurity report analysing MQTT vulnerabilities

## Key Features

- **MQTT-based Device Simulation**  
  Python scripts simulate multiple IoT devices (e.g., Device A, B, C) acting as MQTT clients.

- **Network Traffic Generation**  
  Devices publish sensor data and subscribe to control topics, creating diverse traffic (both normal and suspicious).

- **Intrusion Detection System (IDS)**  
  Monitors MQTT traffic in real-time to detect:
  - Unusual packet sizes
  - Suspicious patterns or IP addresses
  - Abnormal publish rates

- **Lightweight and Scalable**  
  Designed for efficiency, demonstrating how MQTT can scale in constrained environments.

## 🛠 Technologies Used

- **Programming Language**: Python
- **Protocol**: MQTT (using `paho-mqtt`)
- **Libraries**: `scapy`, `paho-mqtt`, `threading`, `random`, `time`
- **Command-Line Interface (CLI)** & Python-based UI

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YourUsername/iot-intrusion-detection.git
cd iot-intrusion-detection
```

### 2. Run the MQTT Broker

You can use a local broker (e.g., Mosquitto) or connect to a public test broker like:

```
test.mosquitto.org
```

### 3. Simulate Devices

```bash
python devices/DeviceA.py
python devices/DeviceB.py
...
```

### 4. Start Intrusion Detection

```bash
python ids/anomaly_detector.py
```

## Example Use Cases

* Academic demonstration of IoT security issues
* Real-time monitoring of sensor traffic
* Detection of unauthorized access or DDoS-like traffic anomalies

## Future Improvements

* Add machine learning-based detection models
* Web dashboard for monitoring device status and alerts
* Support for encrypted MQTT communication

## References

* Soni & Makwana (2017). MQTT in IoT
* Alazab, Wang, & Choo (2019). IoT security and anomaly detection
* MQTT (2024). Official Specification and Use Cases

---
## Author
* Fathima Nishda Mohomed Semsar
* School of Science, Computing and Emerging Technologies
