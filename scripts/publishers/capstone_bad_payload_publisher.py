"""
Hands-on 40 (Bab 15): Uji Payload Rusak
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Mengirim 3 payload buruk: field hilang, tipe data salah, nilai ekstrem.
Subscriber harus menolak/menangani tanpa crash.
"""

import json
import time
from datetime import datetime

import paho.mqtt.client as mqtt

BROKER = "localhost"
TOPIC = "capstone/iotnode01/telemetry"


def main():
  client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="capstone-bad-publisher")
  client.connect(BROKER, 1883, 60)
  client.loop_start()

  samples = [
      # field wajib hilang
      {"timestamp": datetime.now().isoformat(timespec="seconds"),
       "device_id": "iotnode01"},
      # tipe data salah
      {"timestamp": "bad_time", "device_id": "iotnode01",
       "temperature_c": "abc", "humidity_pct": 50, "power_watt": 100,
       "current_amp": 5},
      # nilai ekstrem di luar rentang wajar
      {"timestamp": datetime.now().isoformat(timespec="seconds"),
       "device_id": "iotnode01", "temperature_c": -99, "humidity_pct": 999,
       "power_watt": 10000, "current_amp": -3},
  ]

  for payload in samples:
    client.publish(TOPIC, json.dumps(payload), qos=1)
    print("Published bad payload:", payload)
    time.sleep(1)

  client.loop_stop()
  client.disconnect()
  print("[SUKSES] 3 payload rusak terkirim.")


if __name__ == "__main__":
  main()
