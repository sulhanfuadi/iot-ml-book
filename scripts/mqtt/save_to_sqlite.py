"""
Hands-on 5: Simpan Data MQTT ke SQLite
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Setiap pesan telemetri disimpan ke tabel room_telemetry pada
data/raw/iot_sensor.db. SQLite tidak memerlukan server database terpisah.
"""

import argparse
import json
from pathlib import Path
import sqlite3
import sys
import time

import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "kampus/lab1/room01/telemetry"

DB_PATH = Path("data/raw/iot_sensor.db")


def create_mqtt_client(client_id):
  try:
    return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
  except AttributeError:
    return mqtt.Client(client_id=client_id)


def init_db():
  DB_PATH.parent.mkdir(parents=True, exist_ok=True)
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS room_telemetry (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      device_id TEXT,
      temperature_c REAL,
      humidity_pct REAL,
      co2_ppm INTEGER,
      power_watt REAL,
      timestamp TEXT
    )
  """)
  conn.commit()
  return conn, cursor


def main():
  parser = argparse.ArgumentParser(description="MQTT ke SQLite (Hands-on 5)")
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

  conn, cursor = init_db()
  state = {"received": 0}

  def on_connect(client, userdata, flags, reason_code, properties=None):
    print("[INFO] Terhubung ke broker.")
    client.subscribe(args.topic, qos=1)
    print(f"[INFO] Subscribe ke topik: {args.topic}")

  def on_message(client, userdata, msg):
    state["received"] += 1
    try:
      data = json.loads(msg.payload.decode())
      cursor.execute("""
        INSERT INTO room_telemetry (
          device_id, temperature_c, humidity_pct, co2_ppm,
          power_watt, timestamp
        ) VALUES (?, ?, ?, ?, ?, ?)
      """, (
          data.get("device_id"),
          data.get("temperature_c"),
          data.get("humidity_pct"),
          data.get("co2_ppm"),
          data.get("power_watt"),
          data.get("timestamp"),
      ))
      conn.commit()
      print(f"[SUKSES] Data disimpan ke SQLite: {data}")
    except Exception as exc:
      print(f"[ERROR] Gagal menyimpan ke SQLite: {exc}")

    if args.max_messages > 0 and state["received"] >= args.max_messages:
      client.disconnect()

  client = create_mqtt_client("subscriber-save-sqlite")
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
  finally:
    conn.close()

  print(f"[INFO] Total {state['received']} pesan disimpan ke {DB_PATH}")


if __name__ == "__main__":
  main()
