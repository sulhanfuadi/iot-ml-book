"""
Hands-on 4: Broker MQTT lokal untuk pengembangan (helper).
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Di lingkungan produksi/lab, buku memakai Mosquitto (`mosquitto -v`).
Skrip ini menyediakan broker lokal berbasis Python (amqtt) agar seluruh
alur publish/subscribe pada hands-on dapat dijalankan tanpa instalasi
sistem tambahan.
"""

import asyncio
import logging
import sys

from amqtt.broker import Broker

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


async def start_broker():
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
  logging.basicConfig(level=logging.WARNING)
  try:
    asyncio.run(start_broker())
  except KeyboardInterrupt:
    print("\n[INFO] Broker dihentikan oleh pengguna.")
    sys.exit(0)


if __name__ == "__main__":
  main()
