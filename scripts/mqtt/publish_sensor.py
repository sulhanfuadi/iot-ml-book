"""
Hands-on 3: Mengirim Data Sensor ke MQTT (Publisher Room Telemetry)
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)
"""

import argparse
from datetime import datetime
import json
from pathlib import Path
import random
import sys
import time
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "kampus/lab1/room01/telemetry"
CLIENT_ID = "publisher-room01"


def create_mqtt_client(client_id):
  return mqtt.Client(client_id=client_id)


def generate_sensor_data(device_id="room01"):
  temperature = round(random.uniform(24.0, 30.0), 2)
  humidity = round(random.uniform(45.0, 65.0), 2)
  co2 = random.randint(450, 900)
  power = round(random.uniform(100.0, 160.0), 2)

  payload = {
      "device_id": device_id,
      "temperature_c": temperature,
      "humidity_pct": humidity,
      "co2_ppm": co2,
      "power_watt": power,
      "timestamp": datetime.now().isoformat(timespec="seconds"),
  }
  return payload


def main():
  parser = argparse.ArgumentParser(
      description="MQTT Sensor Telemetry Publisher"
  )
  parser.add_argument(
      "--broker", default=BROKER_HOST, help="MQTT Broker Host (default: localhost)"
  )
  parser.add_argument(
      "--port",
      type=int,
      default=BROKER_PORT,
      help="MQTT Broker Port (default: 1883)",
  )
  parser.add_argument(
      "--topic",
      default=TOPIC,
      help="MQTT Topic (default: kampus/lab1/room01/telemetry)",
  )
  parser.add_argument(
      "--count",
      type=int,
      default=0,
      help="Jumlah pesan yang dikirim (0 = tak terbatas)",
  )
  parser.add_argument(
      "--interval",
      type=float,
      default=5.0,
      help="Interval pengiriman dalam detik (default: 5.0)",
  )
  args = parser.parse_args()

  client = create_mqtt_client(CLIENT_ID)

  try:
    client.connect(args.broker, args.port, keepalive=60)
    print(f"[INFO] Terhubung ke broker MQTT di {args.broker}:{args.port}")
  except Exception as e:
    print(
        f"[ERROR] Gagal terhubung ke broker {args.broker}:{args.port} -> {e}"
    )
    sys.exit(1)

  sent_count = 0
  log_path = Path("outputs/logs/publisher_room01.log")
  log_path.parent.mkdir(parents=True, exist_ok=True)

  try:
    while True:
      payload = generate_sensor_data()
      payload_json = json.dumps(payload)
      result = client.publish(args.topic, payload_json, qos=1)
      status = result.rc

      if status == 0:
        log_line = f"Berhasil publish ke {args.topic}: {payload_json}"
        print(f"[PUBLISH] {log_line}")
        with open(log_path, "a", encoding="utf-8") as f:
          f.write(f"{datetime.now().isoformat()} - {log_line}\n")
      else:
        print(f"[GAGAL] Kode status publish: {status}")

      sent_count += 1
      if args.count > 0 and sent_count >= args.count:
        print(
            f"[SELESAI] Telah mengirim {sent_count} pesan uji ke {args.topic}."
        )
        break

      time.sleep(args.interval)
  except KeyboardInterrupt:
    print("\n[INFO] Publisher dihentikan oleh pengguna.")
  finally:
    client.disconnect()


if __name__ == "__main__":
  main()
