from pathlib import Path
import json
import time
import pandas as pd
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "iotlab/room01/telemetry"
CLIENT_ID = "csv-publisher-room01"
DATA_PATH = Path("data/synthetic/room_classification_dataset.csv")
PUBLISH_INTERVAL_SECONDS = 0.5  # percepat simulasi


def main():
    df = pd.read_csv(DATA_PATH)

    client = mqtt.Client(client_id=CLIENT_ID)
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

    print(f"Mengirim data dari {DATA_PATH} ke topic {TOPIC}")

    for _, row in df.iterrows():
        payload = {
            "timestamp": row["timestamp"],
            "device_id": row["device_id"],
            "temperature_c": float(row["temperature_c"]),
            "humidity_pct": float(row["humidity_pct"]),
            "co2_ppm": int(row["co2_ppm"]),
            "power_watt": float(row["power_watt"]),
            "status_label": row["status_label"],
            "is_anomaly": int(row["is_anomaly"])
        }

        payload_json = json.dumps(payload)
        result = client.publish(TOPIC, payload_json, qos=1)

        if result.rc == 0:
            print(f"Published: {payload_json}")
        else:
            print(f"Gagal publish: {payload_json}")

        time.sleep(PUBLISH_INTERVAL_SECONDS)

    client.disconnect()
    print("Selesai mengirim semua data.")


if __name__ == "__main__":
    main()
