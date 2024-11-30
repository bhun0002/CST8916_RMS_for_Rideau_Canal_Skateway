# Import necessary libraries
import time  # For generating timestamps and adding delays between messages
import random  # For simulating random telemetry data
from azure.iot.device import IoTHubDeviceClient, Message  # Azure IoT Hub client and Message classes

# Define the connection string for the IoT Hub
# Replace the actual connection string with your device's connection string
CONNECTION_STRING = "HostName=RideauCanalSkatewayIoT.azure-devices.net;DeviceId=dows-lake-sensor;SharedAccessKey=2FdwxQdkqj08SIPE4bEwXpjT8fCw/4dl3UvnIz2fqFg="  # Dow's Lake Query String

# Function to simulate telemetry data
def get_telemetry():

    return {
        "iceThickness": random.uniform(20.0, 40.0),
        "surfaceTemperature": random.uniform(-5.0, 2.0),
        "snowAccumulation": random.uniform(0.0, 20.0),
        "externalTemperature": random.uniform(-10.0, 5.0),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")  # Generate the timestamp in ISO 8601 format
    }

# Main function to set up and manage telemetry transmission
def main():
    """
    Establish a connection to Azure IoT Hub, send telemetry data at regular intervals,
    and handle graceful termination on user interruption.
    """
    # Create a client to connect to Azure IoT Hub using the device's connection string
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    print("Sending telemetry to IoT Hub...")
    try:
        # Continuously send telemetry data to the IoT Hub
        while True:
            # Generate a telemetry message
            telemetry = get_telemetry()  # Call the function to simulate sensor data
            message = Message(str(telemetry))  # Wrap the telemetry data in a Message object

            # Send the message to the IoT Hub
            client.send_message(message)
            print(f"Sent message: {message}")  # Log the sent message to the console

            # Wait for 10 seconds before sending the next message
            time.sleep(10)
    except KeyboardInterrupt:
        # Graceful exit on Ctrl+C
        print("Stopped sending messages.")
    finally:
        # Ensure the client disconnects from the IoT Hub
        client.disconnect()

# Entry point of the script
if __name__ == "__main__":
    main()
