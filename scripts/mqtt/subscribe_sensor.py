import json
import paho.mqtt.client as mqtt
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "kampus/lab1/room01/telemetry"
CLIENT_ID = "subscriber-room01"
def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Terhubung ke broker MQTT.")
    client.subscribe(TOPIC, qos=1)
    print(f"Subscribe ke topik: {TOPIC}")
def on_message(client, userdata, msg):
    print("\n=== Pesan baru diterima ===")
    print(f"Topik   : {msg.topic}")
    print(f"QoS     : {msg.qos}")
    print(f"Payload : {msg.payload.decode()}")
    try:
        data = json.loads(msg.payload.decode())
        print("Payload JSON valid.")
        print(f"Device ID     : {data.get('device_id')}")
        print(f"Temperature C : {data.get('temperature_c')}")
        print(f"Humidity %    : {data.get('humidity_pct')}")
        print(f"CO2 ppm       : {data.get('co2_ppm')}")
        print(f"Power watt    : {data.get('power_watt')}")
        print(f"Timestamp     : {data.get('timestamp')}")
    except json.JSONDecodeError:
        print("Payload bukan JSON yang valid.")
def main():
    client = mqtt.Client(client_id=CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_forever()
if __name__ == "__main__":
    main()
