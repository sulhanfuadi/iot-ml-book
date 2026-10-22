"""
Hands-on 13: Subscriber Verifikasi Payload MQTT
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Memverifikasi bahwa payload dari publisher CSV diterima utuh
di topik iotlab/room01/telemetry.
"""

import argparse
import json
import sys
import time

import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "iotlab/room01/telemetry"


def create_mqtt_client(client_id):
  return mqtt.Client(client_id=client_id)


def main():
  parser = argparse.ArgumentParser(description="Verifikasi payload MQTT (Hands-on 13)")
  parser.add_argument("--broker", default=BROKER_HOST)
  parser.add_argument("--port", type=int, default=BROKER_PORT)
  parser.add_argument("--topic", default=TOPIC)
  parser.add_argument("--max-messages", type=int, default=0)
  parser.add_argument("--timeout", type=float, default=0)
  args = parser.parse_args()

  state = {"received": 0}

  def on_connect(client, userdata, flags, reason_code, properties=None):
    print("[INFO] Terhubung ke broker.")
    client.subscribe(args.topic, qos=1)
    print(f"[INFO] Subscribe ke: {args.topic}")

  def on_message(client, userdata, msg):
    state["received"] += 1
    try:
      payload = json.loads(msg.payload.decode())
      print(
          f"[{payload['timestamp']}] "
          f"T={payload['temperature_c']}C, "
          f"H={payload['humidity_pct']}%, "
          f"CO2={payload['co2_ppm']}, "
          f"P={payload['power_watt']}W, "
          f"label={payload['status_label']}, "
          f"anomaly={payload['is_anomaly']}"
      )
    except Exception as exc:
      print(f"[ERROR] Gagal parse payload: {exc}")

    if args.max_messages > 0 and state["received"] >= args.max_messages:
      client.disconnect()

  client = create_mqtt_client("subscriber-verify-room01")
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
    print("\n[INFO] Subscriber dihentikan.")
    client.disconnect()

  print(f"[INFO] Total pesan terverifikasi: {state['received']}")


if __name__ == "__main__":
  main()
