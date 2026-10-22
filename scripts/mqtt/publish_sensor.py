import json
import random
import time
from datetime import datetime
import paho.mqtt.client as mqtt
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "kampus/lab1/room01/telemetry"
CLIENT_ID = "publisher-room01"
client = mqtt.Client(client_id=CLIENT_ID)
def connect():
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
def generate_sensor_data():
    temperature = round(random.uniform(24.0, 30.0), 2)
    humidity = round(random.uniform(45.0, 65.0), 2)
    co2 = random.randint(450, 900)
    power = round(random.uniform(100.0, 160.0), 2)
    payload = {
        "device_id": "room01",
        "temperature_c": temperature,
        "humidity_pct": humidity,
        "co2_ppm": co2,
        "power_watt": power,
        "timestamp": datetime.now().isoformat(timespec="seconds")
    }
    return payload
def main():
    connect()
    print("Terhubung ke broker MQTT.")
    while True:
        payload = generate_sensor_data()
        payload_json = json.dumps(payload)
        result = client.publish(TOPIC, payload_json, qos=1)
        status = result.rc
        if status == 0:
            print(f"Berhasil publish ke {TOPIC}: {payload_json}")
        else:
            print(f"Gagal publish, kode status: {status}")
        time.sleep(5)
if __name__ == "__main__":
    main()
