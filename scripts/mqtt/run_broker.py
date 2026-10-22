"""
Hands-on 4: Broker MQTT lokal untuk pengembangan (helper).
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Di lingkungan produksi/lab, buku memakai Mosquitto (`mosquitto -v`).
Skrip ini memakai Mosquitto bila terpasang (PATH, atau lokasi Homebrew/apt),
sehingga perilaku sama dengan buku. Bila Mosquitto tidak ada, skrip jatuh ke
broker lokal berbasis Python (amqtt) agar seluruh alur publish/subscribe
tetap bisa dijalankan tanpa instalasi sistem tambahan.

Paksa amqtt dengan variabel lingkungan: IOT_BROKER=amqtt
"""

import asyncio
import logging
import os
import shutil
import sys
import tempfile

BROKER_HOST = "127.0.0.1"
BROKER_PORT = 1883

BROKER_CONFIG = {
  "listeners": {
    "default": {
      "type": "tcp",
      "bind": f"{BROKER_HOST}:{BROKER_PORT}",
    }
  },
  "sys_interval": 0,
  "auth": {
    "allow-anonymous": True,
    "plugins": ["auth_anonymous"],
  },
  "topic-check": {
    "enabled": False,
    "plugins": [],
  },
}


def find_mosquitto():
  if os.environ.get("IOT_BROKER", "").lower() == "amqtt":
    return None
  candidates = [shutil.which("mosquitto"),
                "/opt/homebrew/sbin/mosquitto", "/usr/local/sbin/mosquitto",
                "/opt/homebrew/bin/mosquitto", "/usr/sbin/mosquitto"]
  for path in candidates:
    if path and os.path.exists(path):
      return path
  return None


def run_mosquitto(path):
  conf = os.path.join(tempfile.gettempdir(), "iot_ml_book_mosquitto.conf")
  with open(conf, "w") as f:
    f.write(f"listener {BROKER_PORT} {BROKER_HOST}\nallow_anonymous true\n")
  print(f"[INFO] Broker MQTT Mosquitto aktif di {BROKER_HOST}:{BROKER_PORT}", flush=True)
  print("[INFO] Tekan Ctrl+C untuk menghentikan broker.", flush=True)
  os.execv(path, [path, "-c", conf])


async def start_broker():
  from amqtt.broker import Broker
  broker = Broker(BROKER_CONFIG)
  await broker.start()
  print(f"[INFO] Broker MQTT lokal aktif di {BROKER_HOST}:{BROKER_PORT}")
  print("[INFO] Tekan Ctrl+C untuk menghentikan broker.")
  try:
    while True:
      await asyncio.sleep(1)
  except asyncio.CancelledError:
    pass
  finally:
    await broker.shutdown()
    print("[INFO] Broker MQTT dihentikan.")


def main():
  mosquitto = find_mosquitto()
  if mosquitto:
    run_mosquitto(mosquitto)
  print("[INFO] Mosquitto tidak ditemukan, memakai broker amqtt (Python).")
  logging.basicConfig(level=logging.WARNING)
  try:
    asyncio.run(start_broker())
  except KeyboardInterrupt:
    print("\n[INFO] Broker dihentikan oleh pengguna.")
    sys.exit(0)


if __name__ == "__main__":
  main()
