"""
Hands-on 4: Subscriber Wildcard untuk Banyak Perangkat
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Memakai wildcard topik kampus/lab1/+/telemetry untuk membaca
banyak ruangan/perangkat sekaligus.
"""

import argparse
from datetime import datetime
import json
from pathlib import Path
import sys
import time

import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "kampus/lab1/+/telemetry"
CLIENT_ID = "subscriber-all-lab1"
LOG_PATH = Path("outputs/logs/subscriber_all_rooms.log")


def create_mqtt_client(client_id):
  return mqtt.Client(client_id=client_id)


def main():
  parser = argparse.ArgumentParser(
      description="MQTT Wildcard Subscriber (Hands-on 4)"
  )
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

  state = {"received": 0, "topics": set()}

  def on_connect(client, userdata, flags, reason_code, properties=None):
    print("[INFO] Terhubung ke broker.")
    client.subscribe(args.topic, qos=1)
    print(f"[INFO] Subscribe wildcard ke: {args.topic}")

  def on_message(client, userdata, msg):
    state["received"] += 1
    state["topics"].add(msg.topic)
    try:
      payload = msg.payload.decode()
      data = json.loads(payload)
      print(f"[{msg.topic}] {data}")
      LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
      with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(
            f"{datetime.now().isoformat()} - [{msg.topic}] {json.dumps(data)}\n"
        )
    except Exception as exc:
      print(f"[ERROR] Gagal memproses pesan: {exc}")

    if args.max_messages > 0 and state["received"] >= args.max_messages:
      client.disconnect()

  client = create_mqtt_client(CLIENT_ID)
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

  print(f"[INFO] Total pesan diterima: {state['received']}")
  print(f"[INFO] Topik yang terbaca  : {sorted(state['topics'])}")


if __name__ == "__main__":
  main()
