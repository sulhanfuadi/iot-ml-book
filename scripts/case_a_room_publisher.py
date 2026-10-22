"""
Hands-on 35 (Studi Kasus A): Simulator Publisher Ruangan
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Kirim telemetry (suhu, kelembaban, CO2) ke topik casea/room01/telemetry.
"""

import argparse
import json
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt

BROKER = "localhost"
TOPIC = "casea/room01/telemetry"


def main():
  parser = argparse.ArgumentParser(description="Publisher studi kasus A")
  parser.add_argument("--count", type=int, default=20, help="Jumlah pesan (0 = terus-menerus)")
  parser.add_argument("--interval", type=float, default=1.0)
  args = parser.parse_args()

  rng = random.Random()
  client = mqtt.Client(client_id="casea-room-pub")
  client.connect(BROKER, 1883, 60)
  client.loop_start()

  sent = 0
  while args.count == 0 or sent < args.count:
    payload = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "device_id": "room01",
        "temperature_c": round(rng.uniform(23.0, 33.0), 2),
        "humidity_pct": round(rng.uniform(40.0, 72.0), 2),
        "co2_ppm": rng.randint(450, 1500),
    }
    client.publish(TOPIC, json.dumps(payload), qos=1)
    print("Published:", payload)
    sent += 1
    time.sleep(args.interval)

  client.loop_stop()
  client.disconnect()
  print(f"[SUKSES] {sent} pesan terkirim.")


if __name__ == "__main__":
  main()
