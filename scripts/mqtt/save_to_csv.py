"""
Hands-on 5: Simpan Data MQTT ke CSV
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Setiap pesan telemetri yang diterima ditambahkan sebagai baris baru
ke data/raw/mqtt_room01.csv.
"""

import argparse
import csv
import json
from pathlib import Path
import sys
import time

import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "kampus/lab1/room01/telemetry"

OUTPUT_FILE = Path("data/raw/mqtt_room01.csv")
HEADER = [
  "device_id",
  "temperature_c",
  "humidity_pct",
  "co2_ppm",
  "power_watt",
  "timestamp",
]


def create_mqtt_client(client_id):
  try:
    return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
  except AttributeError:
    return mqtt.Client(client_id=client_id)


def ensure_header():
  OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
  if not OUTPUT_FILE.exists():
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
      writer = csv.writer(f)
      writer.writerow(HEADER)


def main():
  parser = argparse.ArgumentParser(description="MQTT ke CSV (Hands-on 5)")
  parser.add_argument("--broker", default=BROKER_HOST)
  parser.add_argument("--port", type=int, default=BROKER_PORT)
  parser.add_argument("--topic", default=TOPIC)
  parser.add_argument(
      "--max-messages",
      type=int,
      default=0,
      help="Berhenti setelah N pesan (0 = tak terbatas)",
  )
  parser.add_argument(
      "--timeout",
      type=float,
      default=0,
      help="Batas waktu subscribe dalam detik (0 = tak terbatas)",
  )
  args = parser.parse_args()

  ensure_header()
  state = {"received": 0}

  def on_connect(client, userdata, flags, reason_code, properties=None):
    print("[INFO] Terhubung ke broker.")
    client.subscribe(args.topic, qos=1)
    print(f"[INFO] Subscribe ke topik: {args.topic}")

  def on_message(client, userdata, msg):
    state["received"] += 1
    try:
      data = json.loads(msg.payload.decode())
      row = [
          data.get("device_id"),
          data.get("temperature_c"),
          data.get("humidity_pct"),
          data.get("co2_ppm"),
          data.get("power_watt"),
          data.get("timestamp"),
      ]
      with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(row)
      print(f"[SUKSES] Data disimpan ke CSV: {row}")
    except Exception as exc:
      print(f"[ERROR] Gagal menyimpan ke CSV: {exc}")

    if args.max_messages > 0 and state["received"] >= args.max_messages:
      client.disconnect()

  client = create_mqtt_client("subscriber-save-csv")
  client.on_connect = on_connect
  client.on_message = on_message

  try:
    client.connect(args.broker, args.port, keepalive=60)
  except Exception as e:
    print(f"[ERROR] Gagal terhubung ke broker {args.broker}:{args.port} -> {e}")
    sys.exit(1)

  try:
    if args.timeout > 0 or args.max_messages > 0:
      client.loop_start()
      deadline = time.time() + args.timeout if args.timeout > 0 else None
      while True:
        if args.max_messages > 0 and state["received"] >= args.max_messages:
          break
        if deadline is not None and time.time() >= deadline:
          break
        time.sleep(0.1)
      client.loop_stop()
      client.disconnect()
    else:
      client.loop_forever()
  except KeyboardInterrupt:
    print("\n[INFO] Subscriber dihentikan oleh pengguna.")
    client.disconnect()

  print(
      f"[INFO] Total {state['received']} pesan disimpan ke {OUTPUT_FILE}"
  )


if __name__ == "__main__":
  main()
