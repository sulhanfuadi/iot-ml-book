"""
Hands-on 3: Variasi Realistis - Publisher untuk Sensor Greenhouse (Pertanian Presisi)
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
TOPIC = "kampus/greenhouse/zone1/telemetry"
CLIENT_ID = "publisher-greenhouse-zone1"


def create_mqtt_client(client_id):
  return mqtt.Client(client_id=client_id)


def generate_greenhouse_data():
  return {
      "device_id": "greenhouse-zone1",
      "air_temp_c": round(random.uniform(25.0, 35.0), 2),
      "soil_moisture_pct": round(random.uniform(30.0, 80.0), 2),
      "light_lux": random.randint(8000, 30000),
      "timestamp": datetime.now().isoformat(timespec="seconds"),
  }


def main():
  parser = argparse.ArgumentParser(
      description="Greenhouse MQTT Telemetry Publisher"
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
      "--topic", default=TOPIC, help="MQTT Topic (default: greenhouse zone1)"
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
      default=10.0,
      help="Interval dalam detik (default: 10.0)",
  )
  args = parser.parse_args()

  client = create_mqtt_client(CLIENT_ID)

  try:
    client.connect(args.broker, args.port, keepalive=60)
    print(
        f"[INFO] Terhubung ke broker MQTT greenhouse di {args.broker}:{args.port}"
    )
  except Exception as e:
    print(
        f"[ERROR] Gagal terhubung ke broker {args.broker}:{args.port} -> {e}"
    )
    sys.exit(1)

  sent_count = 0
  log_path = Path("outputs/logs/publisher_greenhouse.log")
  log_path.parent.mkdir(parents=True, exist_ok=True)

  try:
    while True:
      payload = generate_greenhouse_data()
      payload_json = json.dumps(payload)
      result = client.publish(args.topic, payload_json, qos=1)

      if result.rc == 0:
        log_line = f"[GREENHOUSE] {payload_json}"
        print(log_line)
        with open(log_path, "a", encoding="utf-8") as f:
          f.write(f"{datetime.now().isoformat()} - {log_line}\n")
      else:
        print(f"[GAGAL] Kode status publish: {result.rc}")

      sent_count += 1
      if args.count > 0 and sent_count >= args.count:
        print(
            f"[SELESAI] Telah mengirim {sent_count} pesan uji ke {args.topic}."
        )
        break

      time.sleep(args.interval)
  except KeyboardInterrupt:
    print("\n[INFO] Publisher greenhouse dihentikan oleh pengguna.")
  finally:
    client.disconnect()


if __name__ == "__main__":
  main()
