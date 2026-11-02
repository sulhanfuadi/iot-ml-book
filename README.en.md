# iot-ml-book

Practicum repository for Embedded Systems - Department of Informatics, Diponegoro University (2026).

[Bahasa Indonesia](README.md) | **[English]**

---

## Main Book & Reference Document

All hands-on implementations, code architecture, simulator scripts, and the analytics and machine learning models in this repository refer directly to the following book:

1. **Main Book:** [Onno W. Purbo, IoT Terintegrasi dengan Machine Learning Data Analytics, 2026 (PDF)](https://github.com/sulhanfuadi/iot-ml-book/blob/main/docs/Onno%20W.%20Purbo%2C%20IoT%20Terintegrasi%20dengan%20Machine%20Learning%20Data%20Analytics%2C%202026.pdf)
   - Author: Onno W. Purbo (ITTS / OnnoCenter, 2026)
   - Description: The primary reference source (536 pages) covering Hands-on 1 through Hands-on 40 (Practical IoT Analytics Foundations, Python Data Analytics, IoT Machine Learning, End-to-End Open Source Integration, and Practical Case Studies).

---

## Notebook Structure (Updated 2026-11-02)

All 43 notebooks are completed practical worksheets that have been run, not copies of the book:

- A short **Tujuan** (objectives) section at the start (the hands-on targets), followed by practice steps with **the book's original code as-is** together with **run results saved in the cell outputs** (text, tables, charts).
- **No copied book prose**: long explanations, guides, and work steps from the book are not duplicated into the notebooks; the book remains the primary reference.
- Book challenges/variations are solved in separate cells labeled **"Solusi Tantangan (Tambahan di Luar Buku)"** (challenge solutions, additions outside the book; Hands-on 2, 3, 5) and **"Solusi Variasi"** (variation solutions; Hands-on 13), with the challenge text included briefly. The Hands-on 25 regression variation lives in `scripts/compare_three_regressors.py`.
- The **Penutup** (closing) contains run results actually observed in the cell outputs.
- Verification: 43/43 notebooks re-executed from start to finish without errors (November 2, 2026), including Hands-on 30-31 with a local InfluxDB; code cells remain identical to the book.

---

## Setup on macOS (Apple Silicon / Intel)

All hands-on run locally without Docker and without Mosquitto; the MQTT broker is provided by a Python script (`scripts/mqtt/run_broker.py`, based on amqtt).

```bash
brew install python@3.11 git
git clone https://github.com/sulhanfuadi/iot-ml-book.git && cd iot-ml-book
python3.11 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m ipykernel install --user --name iot-ml-book
jupyter lab
```

Notes:
- Use Python 3.10-3.12. TensorFlow does not yet support Python 3.13 or newer.
- TensorFlow >=2.16 uses the native Apple Silicon wheel; `tensorflow-metal` is not needed. Only Hands-on 26-29 use TensorFlow/TFLite.
- Run notebooks from any folder; each notebook automatically switches to the repo root.
- Make sure port 1883 is free. If you use Homebrew Mosquitto (`brew install mosquitto && brew services start mosquitto`), do not run `run_broker.py` at the same time.
- InfluxDB/Grafana (optional, `--influx` flag): `brew install influxdb grafana` or Docker Desktop.
- Notebooks 00-02 use the kernel named `iot-ml-book` (the `ipykernel install` command above).
- Run one MQTT notebook at a time; notebooks start and stop the broker themselves.

---

## Figures exactly matching the book

The plot scripts in this repository produce richer versions. Figures with titles, axis labels, sizes, and filenames exactly like the book listings are created by a single script:

```bash
python scripts/book_figures.py            # all
python scripts/book_figures.py --only rmsstd
```

| Hands-on | Option | File |
|---|---|---|
| 8 | `anomaly` | `outputs/figures/anomaly_temperature_rule.png` |
| 9 | `room` | `outputs/figures/room_30days_sample.png` |
| 11 | `vibration` | `outputs/figures/vibration_fault_injection.png` |
| 14 | `features` | `outputs/figures/room_temp_ma6.png` |
| 15 | `rmsstd` | `outputs/figures/vibration_features_rms_std.png` |

## Mosquitto, InfluxDB and Grafana

paho-mqtt is pinned to 1.6.x (`paho-mqtt>=1.6.1,<2.0`) so the book's code `mqtt.Client(client_id=...)` with `on_connect(client, userdata, flags, reason_code, properties=None)` runs as-is. Do not use paho-mqtt 2.x for this repo.

Default values match the book: org `iotlab`, bucket `sensor_data`, token `GANTI_DENGAN_TOKEN_ANDA`.

MQTT broker: `python scripts/mqtt/run_broker.py` uses Mosquitto if installed (PATH, Homebrew, or apt), and automatically falls back to amqtt when absent. Set `IOT_BROKER=amqtt` to force amqtt.
Install Mosquitto: `sudo apt install mosquitto mosquitto-clients` (Ubuntu) or `brew install mosquitto` (macOS).

Native path (Ubuntu/macOS): install InfluxDB 2.x and Grafana, create org `iotlab` and bucket `sensor_data`, then fill in `INFLUX_TOKEN` in the scripts (book default: `GANTI_DENGAN_TOKEN_ANDA`); the book's subscriber scripts write directly to InfluxDB. In Grafana, add an InfluxDB datasource (Flux) then import `dashboards/iot-ml-capstone.json` (8 panels).

Docker path: `cd docker && docker compose up -d` (Mosquitto 1883, InfluxDB 8086, Grafana 3000, datasource and dashboard provisioned automatically; change `INFLUX_TOKEN` in the environment if needed).

Test status: Mosquitto 2.0.20, InfluxDB 2.7.10 and Grafana 11.3.0 were tested for real in a native setup (HO5, HO30/31 and capstone data writes, healthy datasource, 8 panels returning data). The `docker/docker-compose.yml` file has not been tested because Docker is not available in the development environment.

## Raspberry Pi hardware requirements

No Hands-on in this book requires Raspberry Pi hardware (GPIO, physical sensors, or a camera). The book contains no GPIO, camera, DHT or I2C/SPI code; all data comes from CSV files and the MQTT simulator, so every Hands-on runs on a laptop or Mac.

Hands-on that mention Raspberry Pi do so only as an optional deployment target:
- Hands-on 28 (model export, the Raspberry Pi deployment section) and Hands-on 29 ("Simple Classification Mini Project on Raspberry Pi / Emulator"): in the book these can run on an emulator/laptop. Running them on a real Raspberry Pi is optional and has not been tested here (see `prompt_test_lokal.md`, Test B).

## Deliberate deviations from the book

All scripts with a "Buat file" (create file) block in the book use the book's code as-is (extracted from the PDF layout). Documented exceptions:

- `scripts/inference/train_capstone_iforest.py`: the book's normal baseline (mean 140 W, std 20 W) does not match the capstone publisher's payload range, so nearly half of normal data was flagged as anomalous. The baseline was adjusted; the model formula (IsolationForest n_estimators=200, contamination=0.05, random_state=42) remains exactly as the book.
- `scripts/alert_score_demo.py` (score-based alert, Hands-on 31), `scripts/book_figures.py` (book figures) and `scripts/mqtt/run_broker.py` (Mosquitto/amqtt broker helper) are additional tools, not from the book.
- `scripts/capstone_alert_listener.py`, `scripts/mqtt/subscribe_validated.py`, `scripts/mqtt/publish_csv_to_mqtt.py`, `scripts/mqtt/publish_multi_topic.py` and `scripts/mqtt/subscribe_verify_mqtt.py` have no same-named "Buat file" block in the book and provide optional command-line options.
- Notebooks run the book's MQTT scripts as subprocesses with an external timeout (the book's scripts do not stop by themselves) and read subscriber results from InfluxDB.
- Docker compose, Raspberry Pi and physical macOS have not been tested in this development environment; see `prompt_test_lokal.md`.

## Scripts exactly from the book (filename matches the book)

The following scripts are copied from the book without logic changes (4-space indentation, and one line cut by a PDF page break was rejoined). Same-named scripts in `scripts/mqtt/` and `scripts/uji_lingkungan.py` are parameterized versions for bounded execution.

| Book file | Hands-on | Run |
|---|---|---|
| `scripts/test_env.py` | 1 | `python scripts/test_env.py` |
| `scripts/check_label_distribution.py` | 12 | `python scripts/check_label_distribution.py` |
| `scripts/publish_csv_to_mqtt.py` | 13 | `python scripts/publish_csv_to_mqtt.py` (needs a broker) |
| `scripts/subscribe_verify_mqtt.py` | 13 | `python scripts/subscribe_verify_mqtt.py` (needs a broker, Ctrl+C to stop) |
| `scripts/compare_synthetic_vs_real.py` | 22 | `python scripts/compare_synthetic_vs_real.py` |

## Directory Structure

```text
iot-ml-book/
├── .venv/                 # Python virtual environment
├── data/
│   ├── raw/               # Raw sensor datasets (dummy & synthetic CSV)
│   │   └── room_sensor_dummy.csv
│   └── processed/         # Processed/cleaned datasets
│       └── room_sensor_clean.csv
├── docs/                  # Main reference book (PDF)
├── notebooks/             # Jupyter notebooks for experiments
│   ├── 00_uji_lingkungan.ipynb
│   ├── 01_baca_data_sensor.ipynb
│   └── 02_kirim_data_mqtt.ipynb
├── outputs/
│   ├── figures/           # Visualization output (PNG)
│   │   ├── plot_suhu_ruangan.png
│   │   ├── temperature.png
│   │   ├── humidity.png
│   │   ├── co2.png
│   │   └── temperature_vs_co2.png
│   ├── logs/              # Telemetry message transmission logs
│   │   ├── publisher_room01.log
│   │   └── publisher_greenhouse.log
│   └── reports/           # Reports and model metrics
├── scripts/               # Executable Python scripts
│   ├── mqtt/
│   │   ├── publish_sensor.py
│   │   └── publish_greenhouse.py
│   ├── uji_lingkungan.py
│   ├── baseline_evaluation.py
│   ├── read_dummy_csv.py
│   └── plot_dummy_sensor.py
├── requirements.lock.txt
├── requirements.txt
├── README.md
└── README.en.md
```

---

## Hands-on Guide

### Hands-on 1: Setting Up the Python Work Environment
- Verify package installation and virtual environment:
  ```bash
  python scripts/uji_lingkungan.py
  ```
- Test notebook: `notebooks/00_uji_lingkungan.ipynb`.

### Hands-on 2: Reading Dummy Sensor CSV Data & First Visualization
- **Dataset:** `data/raw/room_sensor_dummy.csv` (temperature, humidity, CO2, power sensor data).
- **Reading Data & Statistical Summary:**
  ```bash
  python scripts/read_dummy_csv.py
  ```
- **Creating Visualizations:**
  ```bash
  python scripts/plot_dummy_sensor.py
  ```
- **Interactive Notebook:** `notebooks/01_baca_data_sensor.ipynb`.
- **Processed Result:** Saved to `data/processed/room_sensor_clean.csv`.

> Note: the book's MQTT scripts run as-is (`while True` / `loop_forever`, no flags). Stop them with Ctrl+C. Notebooks run them as subprocesses and stop them externally after a few seconds (`python -u`, `TimeoutExpired`, partial output is saved).

### Hands-on 3: Sending Sensor Data to MQTT
- **Broker:** Eclipse Mosquitto (port 1883).
- **MQTT Topics:**
  - Room: `kampus/lab1/room01/telemetry`
  - Greenhouse: `kampus/greenhouse/zone1/telemetry`
- **Run the Room Sensor Publisher:**
  ```bash
  python scripts/mqtt/publish_sensor.py
  ```
- **Run the Greenhouse Sensor Publisher (Precision Agriculture):**
  ```bash
  python scripts/mqtt/publish_greenhouse.py
  ```
- **Interactive Notebook:** `notebooks/02_kirim_data_mqtt.ipynb`.
- **Send Logs:** Saved in `outputs/logs/publisher_room01.log` and `outputs/logs/publisher_greenhouse.log`.

### Hands-on 4: Subscribing to MQTT Data with Python
- **Local broker without system installation (development):**
  ```bash
  python scripts/mqtt/run_broker.py
  ```
  (In the lab/production, the book uses Eclipse Mosquitto: `mosquitto -v`.)
- **Simple subscriber (single topic `kampus/lab1/room01/telemetry`):**
  ```bash
  python scripts/mqtt/subscribe_sensor.py
  ```
- **Multi-room wildcard subscriber (`kampus/lab1/+/telemetry`):**
  ```bash
  python scripts/mqtt/subscribe_all_rooms.py
  ```
- **Subscriber with payload validation (temperature/humidity/CO2 ranges):**
  ```bash
  python scripts/mqtt/subscribe_validated.py --timeout 10
  ```
- **Interactive Notebook:** `notebooks/03_subscribe_mqtt.ipynb` (runs the broker, 3 publishers, and all three subscribers in sequence).
- **Receive Logs:** Saved in `outputs/logs/subscriber_room01.log`, `outputs/logs/subscriber_all_rooms.log`, and `outputs/logs/subscriber_validated.log`.

### Hands-on 5: Saving MQTT Data to CSV & SQLite
- **Save telemetry to CSV (`data/raw/mqtt_room01.csv`):**
  ```bash
  python scripts/mqtt/save_to_csv.py
  ```
- **Save telemetry to SQLite (`data/raw/iot_sensor.db`):**
  ```bash
  python scripts/mqtt/save_to_sqlite.py
  ```
- **Combined multi-storage pattern (CSV + SQLite at once):**
  ```bash
  python scripts/mqtt/save_to_csv_sqlite.py
  ```
- **(Optional, needs a server) Save to InfluxDB:**
  ```bash
  pip install influxdb-client
  python scripts/mqtt/save_to_influxdb.py
  ```
  Requires an InfluxDB server (in the book: Docker `influxdb:2.7` on port 8086).
- **Interactive Notebook:** `notebooks/04_simpan_data_storage.ipynb`.

### Hands-on 6: Exploring Sensor Datasets with pandas
- **Generate a 1-week synthetic dataset (`data/raw/room_sensor_week.csv`, 1008 rows @ 10 minutes):**
  ```bash
  python scripts/generate_room_sensor_week.py
  ```
- **Explore structure, time-series index, operational summary, correlations:**
  ```bash
  python scripts/explore_sensor_dataset.py
  ```
- **Exploratory visualization to `outputs/figures/`:**
  ```bash
  python scripts/plot_exploration.py
  ```
- **Interactive Notebook:** `notebooks/05_eksplorasi_dataset.ipynb`.

### Hands-on 7: Cleaning Timestamps, Resampling, and Imputation
- **Generate a dirty dataset (`data/raw/room_sensor_dirty.csv`):**
  ```bash
  python scripts/generate_dirty_dataset.py
  ```
- **Cleaning + 10-minute resample + imputation (`data/processed/room_sensor_clean.csv`):**
  ```bash
  python scripts/clean_timestamp_resample.py
  ```
- **Interactive Notebook:** `notebooks/06_cleaning_resampling.ipynb`.

### Hands-on 8: Basic Anomaly Detection (Domain Rules, Z-Score, IQR)
- **Generate a dataset with anomalies (`data/raw/room_sensor_anomaly.csv`):**
  ```bash
  python scripts/generate_anomaly_dataset.py
  ```
- **Detection per method:**
  ```bash
  python scripts/detect_anomaly_rules.py
  python scripts/detect_anomaly_zscore.py
  python scripts/detect_anomaly_iqr.py
  ```
- **Combined version + visualization (`data/processed/room_sensor_anomaly_flags.csv`, `outputs/figures/anomali_*.png`):**
  ```bash
  python scripts/detect_anomaly_all.py
  python scripts/plot_anomaly.py
  ```
- **Interactive Notebook:** `notebooks/07_deteksi_anomali.ipynb`.

### Chapter 4 (sections 4.5 to 4.7): Synthetic IoT Data with Python
These scripts appear in the book between Hands-on 8 and Hands-on 9.
- **Generate daily data (`data/synthetic/*_daily_synthetic.csv`, `vibration_machine_synthetic.csv`):**
  ```bash
  python scripts/generate_room_synthetic.py
  python scripts/generate_energy_synthetic.py
  python scripts/generate_vibration_synthetic.py
  ```
- **Adding artificial problems (missing values, drift, outliers):** `python scripts/inject_data_issues.py`
- **Synthetic labels:**
  ```bash
  python scripts/label_room_comfort_daily.py
  python scripts/label_energy_status_daily.py
  python scripts/label_energy_efficiency_daily.py
  ```
- **Simple validation:** `python scripts/validate_synthetic_room.py`
- **Interactive Notebook:** `notebooks/08a_bab4_data_sintetik.ipynb`.

### Hands-on 9: 30-Day Room Temperature-Humidity Data Generator
- **Generate the dataset (`data/synthetic/room_30days.csv`, 4320 rows):**
  ```bash
  python scripts/generate_room_30days.py
  ```
- **Visualization (`outputs/figures/room_30days*.png`):**
  ```bash
  python scripts/plot_room_30days.py
  ```
- **Interactive Notebook:** `notebooks/08_generate_room_30days.ipynb`.

### Hands-on 10: Working-Hours-Based Energy Consumption Data Generator
- **Generate the energy dataset (`data/synthetic/energy_30days.csv`):**
  ```bash
  python scripts/generate_energy_workhours.py
  ```
- **Efficient/wasteful labels (`data/synthetic/energy_30days_labeled.csv`):**
  ```bash
  python scripts/label_energy_efficiency.py
  ```
- **Visualization (`outputs/figures/energy_*.png`):**
  ```bash
  python scripts/plot_energy_workhours.py
  ```
- **Interactive Notebook:** `notebooks/09_generate_energy.ipynb`.

### Hands-on 11: Machine Vibration Data Generator with Fault Injection
- **Generate vibration signal + faults (`data/synthetic/vibration_fault_injection.csv`, 3000 samples):**
  ```bash
  python scripts/generate_vibration_fault.py
  ```
- **Visualization (`outputs/figures/vibration_fault*.png`):**
  ```bash
  python scripts/plot_vibration_fault.py
  ```
- **Interactive Notebook:** `notebooks/10_generate_vibration_fault.ipynb`.

### Hands-on 12: Synthetic Dataset for Classification and Anomaly Detection
- **Generate the labeled dataset (`data/synthetic/room_classification_dataset.csv`):**
  ```bash
  python scripts/generate_room_classification_dataset.py
  ```
- **Label distribution visualization (`outputs/figures/room_classification_scatter.png`):**
  ```bash
  python scripts/plot_classification_dataset.py
  ```
- **Interactive Notebook:** `notebooks/11_generate_classification_dataset.ipynb`.

### Hands-on 13: Exporting Datasets to CSV and Publishing to the MQTT Simulator
- **Publish a CSV dataset to topic `iotlab/room01/telemetry`:**
  ```bash
  python scripts/mqtt/publish_csv_to_mqtt.py --limit 20 --interval 0.05
  ```
- **Payload verification subscriber:**
  ```bash
  python scripts/mqtt/subscribe_verify_mqtt.py --max-messages 20 --timeout 60
  ```
- **Multi-topic publish (warning/fault also to `iotlab/room01/alert`):**
  ```bash
  python scripts/mqtt/publish_multi_topic.py --limit 400 --interval 0.01
  ```
- **Interactive Notebook:** `notebooks/12_publish_csv_mqtt.ipynb`.

### Hands-on 14: Time-Series Features from Temperature/Humidity Data
- **Build features (lag, diff, rolling, comfort index) into `data/processed/room_30days_features.csv`:**
  ```bash
  python scripts/feature_room_timeseries.py
  ```
- **Feature visualization (`outputs/figures/features_*.png`):**
  ```bash
  python scripts/plot_room_features.py
  ```
- **Interactive Notebook:** `notebooks/13_feature_timeseries.ipynb`.

### Hands-on 15: Simple Vibration Features (RMS, Peak, Kurtosis)
- **Per-window feature extraction into `data/processed/vibration_window_features.csv`:**
  ```bash
  python scripts/feature_vibration_machine.py
  ```
- **Feature visualization (`outputs/figures/vibration_window_features.png`):**
  ```bash
  python scripts/plot_vibration_features.py
  ```
- **Interactive Notebook:** `notebooks/14_feature_vibration.ipynb`.

### Hands-on 16: PCA to Summarize Multiple Sensors
- **Standardization + 3-component PCA into `data/processed/room_30days_pca.csv`:**
  ```bash
  python scripts/pca_room_features.py
  ```
- **PC1 vs PC2 visualization (`outputs/figures/room_pca_scatter.png`):**
  ```bash
  python scripts/plot_pca_room.py
  ```
- **Interactive Notebook:** `notebooks/15_pca_room_features.ipynb`.

### Hands-on 20: Preparing the Normal vs Abnormal Classification Dataset
- **Prepare features + time-aware 70/15/15 split into `data/processed/classification_room/`:**
  ```bash
  python scripts/prepare_classification_dataset.py
  ```
- **Interactive Notebook:** `notebooks/16_prepare_classification.ipynb`.

### Hands-on 21: Preparing the Energy Consumption Prediction Regression Dataset
- **Prepare features + 1-step-ahead target + time-aware split into `data/processed/regression_energy/`:**
  ```bash
  python scripts/prepare_regression_energy_dataset.py
  ```
- **Interactive Notebook:** `notebooks/17_prepare_regression_energy.ipynb`.

### Hands-on 22: Baseline Model Evaluation (Classification and Regression)
- **Classification baseline (Logistic Regression + scaler):**
  ```bash
  python scripts/evaluate_baseline_classification.py
  ```
- **Regression baseline (Linear Regression, saves `test_predictions.csv`):**
  ```bash
  python scripts/evaluate_baseline_regression.py
  ```
- **Interactive Notebook:** `notebooks/18_baseline_evaluation.ipynb`.

### Hands-on 23: Energy Prediction with Regression (Linear, Ridge, Random Forest)
- **Train and evaluate each model (predictions saved to `data/processed/regression_energy/pred_*_test.csv`):**
  ```bash
  python scripts/regression_linear_energy.py
  python scripts/regression_ridge_energy.py
  python scripts/regression_rf_energy.py
  ```
- **Compare predictions (`outputs/figures/regression_predictions_compare.png`):**
  ```bash
  python scripts/plot_regression_predictions.py
  ```
- **Interactive Notebook:** `notebooks/19_regression_energy.ipynb`.

### Hands-on 24: Device Status Classification (normal, warning, fault)
- **Prepare the multi-class dataset into `data/processed/classification_status/`:**
  ```bash
  python scripts/prepare_multiclass_status_dataset.py
  ```
- **Train and evaluate models:**
  ```bash
  python scripts/classification_logreg_status.py
  python scripts/classification_rf_status.py
  ```
- **Interactive Notebook:** `notebooks/20_classification_status.ipynb`.

### Hands-on 25: Comparing 3 Models with Metrics and Curves
- **Compare 3 classifiers (report to `outputs/reports/model_comparison_status.csv`):**
  ```bash
  python scripts/compare_three_models_status.py
  ```
- **Accuracy/F1 visualization + ROC curves (`outputs/figures/compare_*.png`):**
  ```bash
  python scripts/plot_model_comparison.py
  ```
- **Regression variation (`outputs/reports/model_comparison_regression.csv`):**
  ```bash
  python scripts/compare_three_regressors.py
  ```
- **Interactive Notebook:** `notebooks/21_compare_models.ipynb`.

### Hands-on 21 (Chapter 9): Clustering Room Temperature-Humidity Patterns
- **K-Means (test K=2..5, report + scatter):**
  ```bash
  python scripts/cluster_room_kmeans.py
  ```
- **DBSCAN (patterns + noise detection):**
  ```bash
  python scripts/cluster_room_dbscan.py
  ```
- **Output:** `outputs/reports/room_kmeans_cluster.csv`, `outputs/reports/room_dbscan_cluster.csv`, `outputs/figures/room_kmeans_scatter.png`, `outputs/figures/room_dbscan_scatter.png`.
- **Interactive Notebook:** `notebooks/22_clustering_room.ipynb`.

### Hands-on 22 (Chapter 9): Electrical Current Anomaly Detection with Isolation Forest
- **Generate the dataset (into `data/synthetic/current_sensor_anomaly.csv`):**
  ```bash
  python scripts/generate_current_anomaly_dataset.py
  ```
- **Run Isolation Forest:**
  ```bash
  python scripts/isolation_forest_current.py
  ```
- **Evaluate against the synthetic ground truth:**
  ```bash
  python scripts/evaluate_iforest_current.py
  ```
- **Interactive Notebook:** `notebooks/23_isolation_forest_current.ipynb`.

### Hands-on 23 (Chapter 9): Static Threshold vs Isolation Forest
- **Static threshold detection:**
  ```bash
  python scripts/current_threshold_detection.py
  ```
- **Compare the metrics of both methods:**
  ```bash
  python scripts/compare_threshold_vs_iforest.py
  ```
- **F1 and recall visualization:**
  ```bash
  python scripts/plot_threshold_vs_iforest.py
  ```
- **Interactive Notebook:** `notebooks/24_threshold_vs_iforest.ipynb`.

### Hands-on 24 (Chapter 10): Room Temperature Forecasting
- **Prepare the dataset (into `data/processed/forecast_room/`):**
  ```bash
  python scripts/prepare_room_forecast_dataset.py
  ```
- **Last value & moving average baselines:**
  ```bash
  python scripts/baseline_room_forecast.py
  ```
- **Lag-based Linear Regression:**
  ```bash
  python scripts/linear_regression_room_forecast.py
  ```
- **Comparison visualization:**
  ```bash
  python scripts/plot_room_forecast_comparison.py
  ```
- **Interactive Notebook:** `notebooks/25_forecasting_suhu.ipynb`.

### Hands-on 25 (Chapter 10): Daily Energy Consumption Forecasting
- **Linear Regression baseline:**
  ```bash
  python scripts/forecast_energy_linear.py
  ```
- **Random Forest Regressor:**
  ```bash
  python scripts/forecast_energy_rf.py
  ```
- **Comparison visualization:**
  ```bash
  python scripts/plot_energy_forecast.py
  ```
- **Interactive Notebook:** `notebooks/26_forecasting_energi.ipynb`.

### Hands-on 26 (Chapter 10): Baseline vs Random Forest vs Mini LSTM
- **Random Forest on lag features:**
  ```bash
  python scripts/forecast_room_rf.py
  ```
- **Prepare LSTM sequences (into `data/processed/lstm_room/`):**
  ```bash
  python scripts/prepare_lstm_room_sequences.py
  ```
- **Train the mini LSTM (requires `pip install tensorflow-cpu`):**
  ```bash
  python scripts/lstm_room_forecast.py
  ```
- **Final comparison + bar chart:**
  ```bash
  python scripts/compare_room_forecast_models.py
  python scripts/plot_room_forecast_model_comparison.py
  ```
- **Interactive Notebook:** `notebooks/27_benchmark_forecasting.ipynb`.

### Hands-on 27 (Chapter 11): Exporting Models to Lightweight Formats
- **Path A - scikit-learn to joblib (`models/room_status_rf.joblib`):**
  ```bash
  python scripts/export_sklearn_model.py
  ```
- **Path B - Keras to TFLite (`models/room_binary.keras` + `.tflite`; requires `pip install tensorflow-cpu`):**
  ```bash
  python scripts/export_keras_to_tflite.py
  ```
- **Interactive Notebook:** `notebooks/28_export_model.ipynb`.

### Hands-on 28 (Chapter 11): Local Inference Simulation at the Edge
- **scikit-learn inference (joblib):**
  ```bash
  python scripts/simulate_edge_inference_sklearn.py
  ```
- **TFLite inference (requires `pip install tensorflow-cpu`):**
  ```bash
  python scripts/simulate_edge_inference_tflite.py
  ```
- **Interactive Notebook:** `notebooks/29_edge_inference.ipynb`.

### Hands-on 29 (Chapter 11): Edge Classification Mini Project (Raspberry Pi / Emulator)
- **Version without MQTT (logs to `outputs/reports/edge_room_predictions.csv`):**
  ```bash
  python scripts/edge_room_classifier_project.py
  ```
- **Version with MQTT (needs a local broker, e.g. `python scripts/mqtt/run_broker.py`):**
  ```bash
  python scripts/edge_room_classifier_mqtt.py
  ```
- **Interactive Notebook:** `notebooks/30_mini_proyek_edge.ipynb`.

### Hands-on 30 (Chapter 12): Complete Pipeline MQTT -> Prediction -> Storage -> Dashboard
- **Sensor simulator (needs a local broker, e.g. `python scripts/mqtt/run_broker.py`):**
  ```bash
  python scripts/publisher_room_simulator.py
  ```
- **Pipeline subscriber (preprocessing + prediction + CSV storage; add `--influx --influx-token <token>` for InfluxDB per the book):**
  ```bash
  python scripts/pipeline_room_subscriber.py --max-messages 10 --timeout 60
  ```
- **Dashboard (optional, per the book):** run InfluxDB 2 (`docker run -d -p 8086:8086 influxdb:2`, org `iotlab`, bucket `sensor_data`) and Grafana (`docker run -d -p 3000:3000 grafana/grafana-oss`), add InfluxDB as a data source, then build temperature/humidity/CO2/power/status panels with normal-green, warning-yellow, fault-red color thresholds.
- **CSV Output:** `outputs/reports/pipeline_room_predictions.csv`.
- **Interactive Notebook:** `notebooks/31_pipeline_lengkap.ipynb`.

### Hands-on 31 (Chapter 12): Simple Alerts for High Anomaly Scores
- **Pipeline subscriber + alerts (alerts to topic `iotlab/room01/alert` and CSV `outputs/reports/pipeline_room_alerts.csv`):**
  ```bash
  python scripts/pipeline_room_with_alert.py --max-messages 10 --timeout 60
  ```
- **Watch the alert topic in another terminal:**
  ```bash
  python scripts/mqtt/subscribe_sensor.py
  ```
- **Alert rule:** the model predicts FAULT, or temperature > 32 C and CO2 > 1200 ppm at the same time. This script writes to InfluxDB (org iotlab, bucket sensor_data, token GANTI_DENGAN_TOKEN_ANDA) exactly as in the book; change the INFLUX_TOKEN constant inside the script if your token differs. To see the alert topic, change TOPIC in subscribe_sensor.py to iotlab/room01/alert.
- **Simple anomaly-score version (the book's Approach B: score >= 0.7 triggers an alert):**
  ```bash
  python scripts/alert_score_demo.py
  ```
- **Interactive Notebook:** `notebooks/32_pipeline_alert.ipynb`.

### Hands-on 32 (Chapter 13): Monitoring Data Drift
- **Compare baseline vs current distributions + drift indicators:**
  ```bash
  python scripts/monitor_data_distribution.py
  ```
- **Output:** `outputs/reports/data_distribution_monitor.csv`, `outputs/figures/dist_compare_temperature_c.png`, `outputs/figures/dist_compare_humidity_pct.png`.
- **Interactive Notebook:** `notebooks/33_data_drift.ipynb`.

### Hands-on 33 (Chapter 13): Feature Importance
- **Extract Random Forest feature importance + narrative:**
  ```bash
  python scripts/feature_importance_room_model.py
  ```
- **Output:** `outputs/reports/feature_importance_room_model.csv`, `outputs/figures/feature_importance_room_model.png`.
- **Interactive Notebook:** `notebooks/34_feature_importance.ipynb`.

### Hands-on 34 (Chapter 13): IoT-ML System Operational Checklist
- **Generate the checklist template:**
  ```bash
  python scripts/generate_operational_checklist.py
  ```
- **Output:** `outputs/reports/iot_ml_operational_checklist.md`.
- **Interactive Notebook:** `notebooks/35_operational_checklist.ipynb`.

### Hands-on 35: Case Study A - Smart Room Monitoring
- **Train the comfort model (into `models/case_a_room_rf.joblib`):**
  ```bash
  python scripts/case_a_train_room_model.py
  ```
- **Simulator publisher (needs a local broker):**
  ```bash
  python scripts/case_a_room_publisher.py
  ```
- **Subscriber + classification (CSV storage; `--influx` for InfluxDB per the book):**
  ```bash
  python scripts/case_a_room_subscriber.py
  ```
- **Interactive Notebook:** `notebooks/36_studi_kasus_a.ipynb`.

### Hands-on 36: Case Study B - Predictive Maintenance
- **Generate motor data (into `data/synthetic/case_b_motor.csv`):**
  ```bash
  python scripts/case_b_generate_motor_data.py
  ```
- **Per-window feature extraction (into `data/processed/case_b_motor_features.csv`):**
  ```bash
  python scripts/case_b_feature_window.py
  ```
- **Isolation Forest + fault classification:**
  ```bash
  python scripts/case_b_detect_and_classify.py
  ```
- **Interactive Notebook:** `notebooks/37_studi_kasus_b.ipynb`.

### Hands-on 37: Case Study C - Smart Energy Analytics
- **Generate energy data (into `data/synthetic/case_c_energy.csv`):**
  ```bash
  python scripts/case_c_generate_energy.py
  ```
- **Load forecasting + alerts (into `outputs/reports/case_c_energy_results.csv`):**
  ```bash
  python scripts/case_c_energy_forecast_alert.py
  ```
- **Interactive Notebook:** `notebooks/38_studi_kasus_c.ipynb`.

### Hands-on 38 (Chapter 15): End-to-End Final Project (Capstone)
- **Train the Isolation Forest baseline (into `data/models/capstone_iforest.joblib`). The baseline is trained on the normal operating range of the deployment (the publisher's normal payload range) following the Chapter 13 principle; the model formula is exactly the book's (n_estimators=200, contamination=0.05, random_state=42):**
  ```bash
  python scripts/inference/train_capstone_iforest.py
  ```
- **Simulator publisher (needs a local broker):**
  ```bash
  python scripts/publishers/capstone_publisher.py
  ```
- **Subscriber (validation + threshold + Isolation Forest, CSV storage; `--influx` for InfluxDB per the book):**
  ```bash
  python scripts/subscribers/capstone_subscriber.py
  ```
- **Subscriber with alerts (alerts to `capstone/iotnode01/alert`):**
  ```bash
  python scripts/subscribers/capstone_subscriber_with_alert.py
  ```
- **Output:** `outputs/reports/capstone_monitoring.csv`, `outputs/reports/capstone_alerts.csv`.
- **Interactive Notebook:** `notebooks/39_proyek_akhir_capstone.ipynb`.

### Hands-on 39 (Chapter 15): Simple Notifications
- **Alert notification listener (needs a local broker and the Hands-on 38 pipeline running):**
  ```bash
  python scripts/capstone_alert_listener.py --max-messages 5 --timeout 60
  ```
- **Output:** `outputs/reports/capstone_notifications.csv`.
- **Interactive Notebook:** `notebooks/40_notifikasi.ipynb`.

### Hands-on 40 (Chapter 15): Stress Testing and Further Development Scenarios
- **Volume test (default 1000 messages, 0.05 second interval):**
  ```bash
  python scripts/publishers/capstone_stress_publisher.py
  ```
- **Corrupt payload test (3 bad payloads):**
  ```bash
  python scripts/publishers/capstone_bad_payload_publisher.py
  ```
- **Artificial drift test (default 500 messages):**
  ```bash
  python scripts/publishers/capstone_drift_publisher.py
  ```
- Run together with `scripts/subscribers/capstone_subscriber.py` and observe the stress-test checklist (broker/subscriber stability, error handling, storage, alert noise, drift signs).
- **Interactive Notebook:** `notebooks/41_stress_test.ipynb`.
