"""
Hands-on 4: Subscribe Data MQTT dengan Python (Subscriber Room Telemetry)
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Subscriber sederhana: terhubung ke broker, berlangganan satu topik,
menampilkan payload, dan mengubah payload JSON menjadi objek Python.
"""

import argparse
from datetime import datetime
import json
from pathlib import Path
import sys

import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "kampus/lab1/room01/telemetry"
CLIENT_ID = "subscriber-room01"
LOG_PATH = Path("outputs/logs/subscriber_room01.log")


def create_mqtt_client(client_id):
  return mqtt.Client(client_id=client_id)


def log_line(text):
  LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
  with open(LOG_PATH, "a", encoding="utf-8") as f:
    f.write(f"{datetime.now().isoformat()} - {text}\n")


def build_arg_parser():
  parser = argparse.ArgumentParser(
      description="MQTT Room Telemetry Subscriber (Hands-on 4)"
  )
  parser.add_argument("--broker", default=BROKER_HOST, help="MQTT Broker Host")
  parser.add_argument(
      "--port", type=int, default=BROKER_PORT, help="MQTT Broker Port"
  )
  parser.add_argument("--topic", default=TOPIC, help="MQTT Topic")
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
  return parser


def main():
  args = build_arg_parser().parse_args()
  state = {"received": 0}

  def on_connect(client, userdata, flags, reason_code, properties=None):
    print("[INFO] Terhubung ke broker MQTT.")
    client.subscribe(args.topic, qos=1)
    print(f"[INFO] Subscribe ke topik: {args.topic}")
    log_line(f"Subscribe ke topik: {args.topic}")

  def on_message(client, userdata, msg):
    state["received"] += 1
    print("\n=== Pesan baru diterima ===")
    print(f"Topik   : {msg.topic}")
    print(f"QoS     : {msg.qos}")
    print(f"Payload : {msg.payload.decode()}")

    try:
      data = json.loads(msg.payload.decode())
      print("[SUKSES] Payload JSON valid.")
      print(f"Device ID     : {data.get('device_id')}")
      print(f"Temperature C : {data.get('temperature_c')}")
      print(f"Humidity %    : {data.get('humidity_pct')}")
      print(f"CO2 ppm       : {data.get('co2_ppm')}")
      print(f"Power watt    : {data.get('power_watt')}")
      print(f"Timestamp     : {data.get('timestamp')}")
      log_line(f"Pesan valid dari {msg.topic}: {json.dumps(data)}")
    except json.JSONDecodeError:
      print("[ERROR] Payload bukan JSON yang valid.")
      log_line(f"Payload tidak valid dari {msg.topic}")

    if args.max_messages > 0 and state["received"] >= args.max_messages:
      print(
          f"\n[SELESAI] Menerima {state['received']} pesan, subscriber berhenti."
      )
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
    if args.timeout > 0:
      client.loop_start()
      import time

      deadline = time.time() + args.timeout
      while time.time() < deadline:
        if (
            args.max_messages > 0
            and state["received"] >= args.max_messages
        ):
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


if __name__ == "__main__":
  main()
