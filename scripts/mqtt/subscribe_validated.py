"""
Hands-on 4: Subscriber dengan Validasi Payload
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Validasi awal data IoT sebelum disimpan: memeriksa kelengkapan field
dan rentang nilai suhu, kelembaban, dan CO2.
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
CLIENT_ID = "subscriber-validated"
LOG_PATH = Path("outputs/logs/subscriber_validated.log")


def create_mqtt_client(client_id):
  return mqtt.Client(client_id=client_id)


def is_valid(data: dict) -> bool:
  temp = data.get("temperature_c")
  hum = data.get("humidity_pct")
  co2 = data.get("co2_ppm")

  if temp is None or hum is None or co2 is None:
    return False

  if not (0 <= temp <= 60):
    return False
  if not (0 <= hum <= 100):
    return False
  if not (300 <= co2 <= 5000):
    return False

  return True


def main():
  parser = argparse.ArgumentParser(
      description="MQTT Subscriber dengan Validasi Payload (Hands-on 4)"
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

  state = {"received": 0, "valid": 0, "invalid": 0}

  def on_connect(client, userdata, flags, reason_code, properties=None):
    print("[INFO] Terhubung ke broker.")
    client.subscribe(args.topic, qos=1)
    print(f"[INFO] Subscribe dengan validasi ke: {args.topic}")

  def on_message(client, userdata, msg):
    state["received"] += 1
    try:
      data = json.loads(msg.payload.decode())
      if is_valid(data):
        state["valid"] += 1
        print(f"[VALID] Data valid: {data}")
        status = "VALID"
      else:
        state["invalid"] += 1
        print(f"[PERINGATAN] Data tidak valid: {data}")
        status = "TIDAK_VALID"
      LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
      with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(
            f"{datetime.now().isoformat()} - {status} [{msg.topic}] "
            f"{json.dumps(data)}\n"
        )
    except Exception as exc:
      state["invalid"] += 1
      print(f"[ERROR] Error parsing payload: {exc}")

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

  print(
      f"[INFO] Ringkasan: {state['received']} pesan, "
      f"{state['valid']} valid, {state['invalid']} tidak valid."
  )


if __name__ == "__main__":
  main()
