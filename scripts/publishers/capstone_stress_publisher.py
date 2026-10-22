"""
Hands-on 40 (Bab 15): Uji Volume - Publisher Laju Tinggi
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

1000 pesan dengan jeda 0.05 detik dan injeksi anomali 12%.
"""

import argparse
import json
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "capstone/iotnode01/telemetry"


def main():
  parser = argparse.ArgumentParser(description="Stress publisher capstone")
  parser.add_argument("--count", type=int, default=1000)
  parser.add_argument("--interval", type=float, default=0.05)
  args = parser.parse_args()

  rng = random.Random()
  client = mqtt.Client(client_id="capstone-stress-publisher")
  client.connect(BROKER, PORT, 60)
  client.loop_start()

  for i in range(args.count):
    payload = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "device_id": "iotnode01",
        "temperature_c": round(rng.uniform(24.0, 34.0), 2),
        "humidity_pct": round(rng.uniform(40.0, 75.0), 2),
        "power_watt": round(rng.uniform(80.0, 260.0), 2),
        "current_amp": round(rng.uniform(3.5, 9.5), 2),
    }
    if rng.random() < 0.12:
      payload["power_watt"] += rng.uniform(100, 220)
      payload["current_amp"] += rng.uniform(2, 6)

    client.publish(TOPIC, json.dumps(payload), qos=0)
    if i % 100 == 0:
      print(f"Published {i} messages")
    time.sleep(args.interval)

  client.loop_stop()
  client.disconnect()
  print(f"[SUKSES] {args.count} pesan stress terkirim.")


if __name__ == "__main__":
  main()
