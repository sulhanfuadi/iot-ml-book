"""
Hands-on 38 (Bab 15): Capstone Publisher - Simulator Telemetry IoT Node
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Mengirim payload generik (suhu, kelembaban, daya, arus) ke
capstone/iotnode01/telemetry dengan injeksi anomali kecil sesekali (8%).
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
  parser = argparse.ArgumentParser(description="Capstone publisher")
  parser.add_argument("--count", type=int, default=20, help="Jumlah pesan (0 = terus-menerus)")
  parser.add_argument("--interval", type=float, default=1.0)
  parser.add_argument("--seed", type=int, default=None)
  args = parser.parse_args()

  rng = random.Random(args.seed)

  client = mqtt.Client(client_id="capstone-publisher")
  client.connect(BROKER, PORT, 60)
  client.loop_start()

  sent = 0
  while args.count == 0 or sent < args.count:
    payload = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "device_id": "iotnode01",
        "temperature_c": round(rng.uniform(24.0, 34.0), 2),
        "humidity_pct": round(rng.uniform(40.0, 75.0), 2),
        "power_watt": round(rng.uniform(80.0, 260.0), 2),
        "current_amp": round(rng.uniform(3.5, 9.5), 2),
    }

    # injeksi anomali kecil sesekali
    if rng.random() < 0.08:
      payload["power_watt"] += rng.uniform(80, 180)
      payload["current_amp"] += rng.uniform(2, 5)

    client.publish(TOPIC, json.dumps(payload), qos=1)
    print("Published:", payload)
    sent += 1
    time.sleep(args.interval)

  client.loop_stop()
  client.disconnect()
  print(f"[SUKSES] {sent} pesan terkirim.")


if __name__ == "__main__":
  main()
