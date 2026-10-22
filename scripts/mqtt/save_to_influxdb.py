import json
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "kampus/lab1/room01/telemetry"
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "GANTI_DENGAN_TOKEN_ANDA"
INFLUX_ORG = "iotlab"
INFLUX_BUCKET = "sensor_data"
influx_client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG
)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)
def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Terhubung ke broker MQTT.")
    client.subscribe(TOPIC, qos=1)
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        point = (
            Point("room_telemetry")
            .tag("device_id", data.get("device_id", "unknown"))
            .field("temperature_c", float(data.get("temperature_c", 0)))
            .field("humidity_pct", float(data.get("humidity_pct", 0)))
            .field("co2_ppm", int(data.get("co2_ppm", 0)))
            .field("power_watt", float(data.get("power_watt", 0)))
            .time(data.get("timestamp"), WritePrecision.S)
        )
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        print(f"Data disimpan ke InfluxDB: {data}")
    except Exception as exc:
        print(f"Gagal menyimpan ke InfluxDB: {exc}")
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER_HOST, BROKER_PORT, 60)
try:
    client.loop_forever()
finally:
    influx_client.close()
