# Rideau Canal Skateway Monitoring Solution

## Scenario Description
The Rideau Canal Skateway, a world-renowned historic attraction in
Ottawa, requires continuous monitoring to ensure the safety of skaters.
Factors like ice thickness, surface temperature, snow accumulation, and
external temperature significantly affect the safety and usability of
the canal. This project addresses the challenge of real-time monitoring
by implementing a system to:

1.  Simulate IoT sensors at key locations along the canal.

2.  Process incoming sensor data in real time to detect unsafe
    conditions.

3.  Store the processed data in Azure Blob Storage for future analysis.

This solution enables proactive safety measures and operational
insights, helping the National Capital Commission (NCC) maintain the
Skateway efficiently.

## System Architecture

The system consists of three main components:

1.  **IoT Sensors**: Simulate real-time data from three locations along
    the Rideau Canal: Dow\'s Lake, Fifth Avenue, and NAC.

2.  **Azure IoT Hub**: Serves as the ingestion point for sensor data.

3.  **Azure Stream Analytics**: Processes the incoming data to calculate
    metrics like average ice thickness and maximum snow accumulation
    over 5-minute windows.

4.  **Azure Blob Storage**: Stores processed data in organized JSON/CSV
    formats for further analysis.

**Data Flow Diagram**

![System Architecture Diagram](screenshots/system_architecture.jpg)



## IoT Sensor Simulation**

-   **How It Works**:

    -   A Python script simulates IoT sensors at three locations (Dow\'s
        Lake, Fifth Avenue, and NAC) along the Rideau Canal.

    -   Every 10 seconds, each sensor sends a JSON payload to Azure IoT
        Hub containing:

        -   iceThickness: Random value between 20--35 cm.

        -   surfaceTemperature: Random value between -10--0 °C.

        -   snowAccumulation: Random value between 5--15 cm.

        -   externalTemperature: Random value between -15--5 °C.

        -   timestamp: Current UTC time in ISO 8601 format.

-   **JSON Payload Structure**:

```json
{
  "location": "Dow's Lake",
  "iceThickness": 27,
  "surfaceTemperature": -1,
  "snowAccumulation": 8,
  "externalTemperature": -4,
  "timestamp": "2024-11-23T12:00:00Z"
}
```
## Azure IoT Hub Configuration

### 1. Create an IoT Hub
1. In the Azure Portal, search for **IoT Hub** and click **Create**.
2. Provide a name for your IoT Hub and select a resource group.
3. Choose the **Free Tier** (if available) for testing purposes and create the IoT Hub.
### 2. Register a Device
1. In the IoT Hub, go to the **Devices** section and click **Add Device**.
2. Provide a Device ID (e.g., `Sensor1`) and click **Save**.
3. After the device is created, click on it to view the connection string. Copy the connection string for use in the Python script that going to simulate the sensor.
### 3. Install Required Libraries

Install the `azure-iot-device` library to simulate sensor data. Run the following command:

```bash
pip install azure-iot-device
```
### 4. Run the Python Script to Simulate Sensor Data
Use the following Python script to simulate telemetry data and send it to the IoT Hub. Replace the `CONNECTION_STRING` with the device connection string you copied earlier.

```python
import time
import random
from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "Your IoT Hub device connection string here"

def get_telemetry():
    return {
        "temperature": random.uniform(20.0, 40.0),
        "humidity": random.uniform(30.0, 70.0)
    }

def main():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    print("Sending telemetry to IoT Hub...")
    try:
        while True:
            telemetry = get_telemetry()
            message = Message(str(telemetry))
            client.send_message(message)
            print(f"Sent message: {message}")
            time.sleep(10)
    except KeyboardInterrupt:
        print("Stopped sending messages.")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
```

**Explanation:**
This Python script simulates an IoT device sending telemetry data to an Azure IoT Hub. 
It uses a connection string to authenticate and connects to the IoT Hub via the `IoTHubDeviceClient`. 
The script generates random temperature and humidity data through the `get_telemetry` function and continuously sends this data as messages to the IoT Hub every 10 seconds. 
It handles keyboard interrupts (e.g., Ctrl+C) to stop the loop gracefully and disconnects the client.

### 5. Run the Script
Execute the script to start sending telemetry data to your IoT Hub.
