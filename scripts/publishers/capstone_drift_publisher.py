"""
Hands-on 40 (Bab 15): Uji Drift Buatan
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

500 pesan dengan suhu dan daya yang bergeser perlahan (drift).
"""

import argparse
import json
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt

BROKER = "localhost"
TOPIC = "capstone/iotnode01/telemetry"


def main():
  parser = argparse.ArgumentParser(description="Drift publisher capstone")
  parser.add_argument("--count", type=int, default=500)
  parser.add_argument("--interval", type=float, default=0.1)
  args = parser.parse_args()

  rng = random.Random()
  client = mqtt.Client(client_id="capstone-drift-publisher")
  client.connect(BROKER, 1883, 60)
  client.loop_start()

  base_temp = 26.0
  base_power = 130.0

  for i in range(args.count):
    # drift perlahan
    temp = base_temp + (i * 0.01) + rng.uniform(-0.5, 0.5)
    power = base_power + (i * 0.08) + rng.uniform(-10, 10)

    payload = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "device_id": "iotnode01",
        "temperature_c": round(temp, 2),
        "humidity_pct": round(rng.uniform(45.0, 65.0), 2),
        "power_watt": round(power, 2),
        "current_amp": round(rng.uniform(4.0, 7.5), 2),
    }
    client.publish(TOPIC, json.dumps(payload), qos=1)
    if i % 100 == 0:
      print(f"Published drift payload ke-{i}:", payload)
    time.sleep(args.interval)

  client.loop_stop()
  client.disconnect()
  print(f"[SUKSES] {args.count} pesan drift terkirim.")


if __name__ == "__main__":
  main()
