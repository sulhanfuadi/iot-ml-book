import json
import paho.mqtt.client as mqtt
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "iotlab/room01/telemetry"
def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Terhubung ke broker.")
    client.subscribe(TOPIC, qos=1)
    print(f"Subscribe ke: {TOPIC}")
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print(
            f"[{payload['timestamp']}] "
            f"T={payload['temperature_c']}C, "
            f"H={payload['humidity_pct']}%, "
            f"CO2={payload['co2_ppm']}, "
            f"P={payload['power_watt']}W, "
            f"label={payload['status_label']}, "
            f"anomaly={payload['is_anomaly']}"
        )
    except Exception as exc:
        print(f"Gagal parse payload: {exc}")
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
client.loop_forever()
