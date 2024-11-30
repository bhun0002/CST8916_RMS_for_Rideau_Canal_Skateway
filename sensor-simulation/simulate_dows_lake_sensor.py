import time
import random
from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=RideauCanalSkatewayIoT.azure-devices.net;DeviceId=dows-lake-sensor;SharedAccessKey=2FdwxQdkqj08SIPE4bEwXpjT8fCw/4dl3UvnIz2fqFg=" # Dow's Lake Query String

def get_telemetry():
    return {
        "iceThickness": random.uniform(20.0, 40.0),
        "surfaceTemperature": random.uniform(-5.0, 2.0),
        "snowAccumulation": random.uniform(0.0, 20.0),
        "externalTemperature": random.uniform(-10.0, 5.0),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
    }

def main():
    # Create IoT Hub client for the sensor
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    print("Sending telemetry to IoT Hub...")
    try:
        while True:
            # Generate and send telemetry data
            telemetry = get_telemetry()
            message = Message(str(telemetry))
            client.send_message(message)
            print(f"Sent message: {message}")
            time.sleep(10)
    except KeyboardInterrupt:
        print("Stopped sending messages.")
    finally:
        # Disconnect the client
        client.disconnect()

if __name__ == "__main__":
    main()