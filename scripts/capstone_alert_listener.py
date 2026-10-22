"""
Hands-on 39 (Bab 15): Notifikasi Sederhana - Listener Alert Capstone
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Subscribe ke topik capstone/iotnode01/alert dan tampilkan notifikasi di terminal,
serta simpan ke outputs/reports/capstone_notifications.csv. Inilah titik ekstensi
menuju Telegram/email/WA di masa depan.
"""

import argparse
import json
import time
from pathlib import Path

import pandas as pd
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC_ALERT = "capstone/iotnode01/alert"
CSV_PATH = Path("outputs/reports/capstone_notifications.csv")

notifications = []


def main():
  parser = argparse.ArgumentParser(description="Listener notifikasi alert capstone")
  parser.add_argument("--max-messages", type=int, default=5)
  parser.add_argument("--timeout", type=int, default=60)
  args = parser.parse_args()

  CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
  state = {"count": 0}

  def on_connect(client, userdata, flags, reason_code, properties=None):
    client.subscribe(TOPIC_ALERT, qos=1)
    print(f"[INFO] Menunggu alert di topik: {TOPIC_ALERT}")

  def on_message(client, userdata, msg):
    try:
      payload = json.loads(msg.payload.decode("utf-8"))
      print("\n=== NOTIFIKASI ALERT ===")
      print(f"Waktu   : {payload.get('timestamp')}")
      print(f"Device  : {payload.get('device_id')}")
      print(f"Alasan  : {payload.get('reason', payload.get('alert_reason', '-'))}")
      print(f"Daya    : {payload.get('power_watt')} W")
      print(f"Arus    : {payload.get('current_amp')} A")
      notifications.append(payload)
      state["count"] += 1
      if args.max_messages and state["count"] >= args.max_messages:
        client.disconnect()
    except Exception as exc:
      print("[ERROR] Payload alert tidak valid:", exc)

  client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                       client_id="capstone-alert-listener")
  client.on_connect = on_connect
  client.on_message = on_message
  client.connect(BROKER, PORT, 60)
  client.loop_start()

  start = time.time()
  while time.time() - start < args.timeout:
    if args.max_messages and state["count"] >= args.max_messages:
      break
    time.sleep(0.2)

  client.loop_stop()
  client.disconnect()

  if notifications:
    pd.DataFrame(notifications).to_csv(CSV_PATH, index=False)
    print(f"\n[SUKSES] {len(notifications)} notifikasi disimpan ke {CSV_PATH}")
  else:
    print("\n[INFO] Tidak ada alert diterima dalam batas waktu.")


if __name__ == "__main__":
  main()
