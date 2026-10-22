"""
Hands-on 30 (Bab 12): Simulator Sensor Ruangan -> MQTT
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Mengirim telemetry (suhu, kelembaban, CO2, daya) ke topik iotlab/room01/telemetry.
Gunakan --count 0 untuk mode terus-menerus seperti di buku.
"""

import argparse
import json
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "iotlab/room01/telemetry"


def main():
  parser = argparse.ArgumentParser(description="Simulator sensor ruangan -> MQTT")
  parser.add_argument("--count", type=int, default=20,
                      help="Jumlah pesan (0 = terus-menerus, default 20)")
  parser.add_argument("--interval", type=float, default=1.0,
                      help="Jeda antar-pesan dalam detik (default 1.0)")
  parser.add_argument("--host", default=BROKER_HOST)
  parser.add_argument("--port", type=int, default=BROKER_PORT)
  args = parser.parse_args()

  rng = random.Random()

  client = mqtt.Client(client_id="publisher-room-sim")
  client.connect(args.host, args.port, keepalive=60)
  client.loop_start()

  sent = 0
  while args.count == 0 or sent < args.count:
    payload = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "device_id": "room01",
        "temperature_c": round(rng.uniform(24.0, 33.5), 2),
        "humidity_pct": round(rng.uniform(40.0, 70.0), 2),
        "co2_ppm": rng.randint(450, 1500),
        "power_watt": round(rng.uniform(90.0, 300.0), 2),
    }
    payload_json = json.dumps(payload)
    result = client.publish(TOPIC, payload_json, qos=1)
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
      print("Published:", payload_json)
    else:
      print("[ERROR] Publish gagal.")
    sent += 1
    time.sleep(args.interval)

  client.loop_stop()
  client.disconnect()
  print(f"[SUKSES] {sent} pesan terkirim ke {TOPIC}.")


if __name__ == "__main__":
  main()
