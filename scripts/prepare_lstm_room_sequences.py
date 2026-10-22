from pathlib import Path
import numpy as np
import pandas as pd
INPUT_PATH = Path("data/synthetic/room_30days.csv")
OUTPUT_DIR = Path("data/processed/lstm_room")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(INPUT_PATH)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp").reset_index(drop=True)
series = df["temperature_c"].values.astype("float32")
window_size = 12    # 12 langkah = 2 jam jika interval 10 menit
X = []
y = []
for i in range(window_size, len(series)):
    X.append(series[i-window_size:i])
    y.append(series[i])
X = np.array(X)
y = np.array(y)
# reshape untuk LSTM: [samples, timesteps, features]
X = X.reshape((X.shape[0], X.shape[1], 1))
# split time-aware
n = len(X)
train_end = int(n * 0.70)
val_end = int(n * 0.85)
X_train, X_val, X_test = X[:train_end], X[train_end:val_end], X[val_end:]
y_train, y_val, y_test = y[:train_end], y[train_end:val_end], y[val_end:]
np.save(OUTPUT_DIR / "X_train.npy", X_train)
np.save(OUTPUT_DIR / "X_val.npy", X_val)
np.save(OUTPUT_DIR / "X_test.npy", X_test)
np.save(OUTPUT_DIR / "y_train.npy", y_train)
np.save(OUTPUT_DIR / "y_val.npy", y_val)
np.save(OUTPUT_DIR / "y_test.npy", y_test)
print("Sequence LSTM disimpan di:", OUTPUT_DIR)
print("Shape X_train:", X_train.shape)
