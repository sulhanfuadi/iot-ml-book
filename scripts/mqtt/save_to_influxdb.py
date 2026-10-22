"""
Hands-on 5: Simpan Data MQTT ke InfluxDB
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Skrip ini menyimpan telemetri ke InfluxDB (time-series database).
Prasyarat:
  1. Server InfluxDB berjalan (di buku: Docker `influxdb:2.7` di port 8086).
  2. Pustaka Python: pip install influxdb-client
  3. Token, organisasi, dan bucket yang valid.

Skrip tidak dijalankan pada pipeline notebook karena memerlukan server
InfluxDB eksternal; gunakan saat server tersedia.
"""

import argparse
import json
import sys

import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "kampus/lab1/room01/telemetry"

INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "GANTI_DENGAN_TOKEN_ANDA"
INFLUX_ORG = "iotlab"
INFLUX_BUCKET = "sensor_data"


def create_mqtt_client(client_id):
  return mqtt.Client(client_id=client_id)


def main():
  parser = argparse.ArgumentParser(
      description="MQTT ke InfluxDB (Hands-on 5)"
  )
  parser.add_argument("--broker", default=BROKER_HOST)
  parser.add_argument("--port", type=int, default=BROKER_PORT)
  parser.add_argument("--topic", default=TOPIC)
  parser.add_argument("--influx-url", default=INFLUX_URL)
  parser.add_argument("--influx-token", default=INFLUX_TOKEN)
  parser.add_argument("--influx-org", default=INFLUX_ORG)
  parser.add_argument("--influx-bucket", default=INFLUX_BUCKET)
  args = parser.parse_args()

  try:
    from influxdb_client import InfluxDBClient, Point
    from influxdb_client.client.write_api import SYNCHRONOUS
  except ImportError:
    print(
        "[ERROR] Pustaka influxdb-client belum terpasang. "
        "Jalankan: pip install influxdb-client"
    )
    sys.exit(1)

  influx = InfluxDBClient(
      url=args.influx_url, token=args.influx_token, org=args.influx_org
  )
  write_api = influx.write_api(write_options=SYNCHRONOUS)

  def on_connect(client, userdata, flags, reason_code, properties=None):
    print("[INFO] Terhubung ke broker.")
    client.subscribe(args.topic, qos=1)
    print(f"[INFO] Subscribe ke topik: {args.topic}")

  def on_message(client, userdata, msg):
    try:
      data = json.loads(msg.payload.decode())
      point = (
          Point("room_telemetry")
          .tag("device_id", data.get("device_id"))
          .field("temperature_c", float(data.get("temperature_c")))
          .field("humidity_pct", float(data.get("humidity_pct")))
          .field("co2_ppm", int(data.get("co2_ppm")))
          .field("power_watt", float(data.get("power_watt")))
          .time(data.get("timestamp"))
      )
      write_api.write(bucket=args.influx_bucket, record=point)
      print(f"[SUKSES] Data disimpan ke InfluxDB: {data}")
    except Exception as exc:
      print(f"[ERROR] Gagal menyimpan ke InfluxDB: {exc}")

  client = create_mqtt_client("subscriber-save-influxdb")
  client.on_connect = on_connect
  client.on_message = on_message

  try:
    client.connect(args.broker, args.port, keepalive=60)
  except Exception as e:
    print(f"[ERROR] Gagal terhubung ke broker {args.broker}:{args.port} -> {e}")
    sys.exit(1)

  try:
    client.loop_forever()
  except KeyboardInterrupt:
    print("\n[INFO] Subscriber dihentikan oleh pengguna.")
  finally:
    client.disconnect()
    influx.close()


if __name__ == "__main__":
  main()
