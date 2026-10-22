from pathlib import Path
import pandas as pd
DATA_PATH = Path("data/synthetic/room_classification_dataset.csv")
df = pd.read_csv(DATA_PATH)
print("Distribusi status_label:")
print(df["status_label"].value_counts())
print("\nDistribusi is_anomaly:")
print(df["is_anomaly"].value_counts())
