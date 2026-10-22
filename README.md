# iot-ml-book

Repositori praktikum Sistem Tertanam - Departemen Informatika Universitas Diponegoro (2026).

---

## Buku & Dokumen Referensi Utama

Seluruh implementasi hands-on, arsitektur kode, skrip simulator, serta model analitik dan machine learning di repositori ini mengacu langsung pada dokumen rujukan yang tersimpan di dalam folder `docs/`:

1. **Buku Utama:**
   - Path: `docs/Onno W. Purbo, IoT Terintegrasi dengan Machine Learning Data Analytics, 2026.pdf`
   - Penulis: Onno W. Purbo (ITTS / OnnoCenter, 2026)
   - Deskripsi: Sumber acuan utama (536 halaman) yang mencakup Hands-on 1 hingga Hands-on 40 (Fondasi Praktis IoT Analytics, Data Analytics Python, Machine Learning IoT, Integrasi End-to-End Open Source, dan Studi Kasus Praktis).
2. **Slide Praktikum:**
   - Path: `docs/08. Sister IF 2026 - Persiapan Lingkungan Kerja.pdf`
   - Pemateri: Indra Waspada (Universitas Diponegoro, 2026)
   - Deskripsi: Slide panduan silabus dan persiapan lingkungan kerja praktikum.

---

---

## Setup di macOS (Apple Silicon / Intel)

Seluruh hands-on berjalan lokal tanpa Docker dan tanpa Mosquitto; broker MQTT disediakan skrip Python (`scripts/mqtt/run_broker.py`, berbasis amqtt).

```bash
brew install python@3.11 git
git clone https://github.com/sulhanfuadi/iot-ml-book.git && cd iot-ml-book
python3.11 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m ipykernel install --user --name iot-ml-book
jupyter lab
```

Catatan:
- Gunakan Python 3.10-3.12. TensorFlow belum mendukung Python 3.13 ke atas.
- TensorFlow >=2.16 memakai wheel native Apple Silicon; `tensorflow-metal` tidak diperlukan. Hanya Hands-on 26-29 yang memakai TensorFlow/TFLite.
- Jalankan notebook dari folder mana pun; setiap notebook otomatis pindah ke root repo.
- Pastikan port 1883 kosong. Jika memakai Mosquitto Homebrew (`brew install mosquitto && brew services start mosquitto`), jangan jalankan `run_broker.py` bersamaan.
- InfluxDB/Grafana (opsional, flag `--influx`): `brew install influxdb grafana` atau Docker Desktop.
- Notebook 00-02 memakai kernel bernama `iot-ml-book` (perintah `ipykernel install` di atas).
- Jalankan satu notebook MQTT pada satu waktu; notebook memulai dan menghentikan broker sendiri.

## Struktur Direktori

```text
iot-ml-book/
├── .venv/                 # Virtual environment Python
├── data/
│   ├── raw/               # Dataset sensor mentah (CSV dummy & sintetis)
│   │   └── room_sensor_dummy.csv
│   └── processed/         # Dataset hasil olahan/pembersihan
│       └── room_sensor_clean.csv
├── docs/                  # Buku referensi utama dan slide kuliah
│   ├── 08. Sister IF 2026 - Persiapan Lingkungan Kerja.pdf
│   └── Onno W. Purbo, IoT Terintegrasi dengan Machine Learning Data Analytics, 2026.pdf
├── notebooks/             # Jupyter Notebook eksperimen
│   ├── 00_uji_lingkungan.ipynb
│   ├── 01_baca_data_sensor.ipynb
│   └── 02_kirim_data_mqtt.ipynb
├── outputs/
│   ├── figures/           # Hasil visualisasi grafik (PNG)
│   │   ├── plot_suhu_ruangan.png
│   │   ├── temperature.png
│   │   ├── humidity.png
│   │   ├── co2.png
│   │   └── temperature_vs_co2.png
│   ├── logs/              # Log transmisi pesan telemetri
│   │   ├── publisher_room01.log
│   │   └── publisher_greenhouse.log
│   └── reports/           # Laporan dan metrik model
├── scripts/               # Skrip Python executable
│   ├── mqtt/
│   │   ├── publish_sensor.py
│   │   └── publish_greenhouse.py
│   ├── uji_lingkungan.py
│   ├── baseline_evaluation.py
│   ├── read_dummy_csv.py
│   └── plot_dummy_sensor.py
├── requirements.lock.txt
├── requirements.txt
└── README.md
```

---

## Panduan Hands-on

### Hands-on 1: Menyiapkan Lingkungan Kerja Python
- Verifikasi instalasi paket dan virtual environment:
  ```bash
  python scripts/uji_lingkungan.py
  ```
- Notebook pengujian: `notebooks/00_uji_lingkungan.ipynb`.

### Hands-on 2: Membaca Data Sensor Dummy CSV & Visualisasi Pertama
- **Dataset:** `data/raw/room_sensor_dummy.csv` (data sensor suhu, kelembaban, CO2, daya).
- **Membaca Data & Ringkasan Statistik:**
  ```bash
  python scripts/read_dummy_csv.py
  ```
- **Membuat Visualisasi:**
  ```bash
  python scripts/plot_dummy_sensor.py
  ```
- **Notebook Interaktif:** `notebooks/01_baca_data_sensor.ipynb`.
- **Hasil Olahan:** Disimpan ke `data/processed/room_sensor_clean.csv`.

### Hands-on 3: Mengirim Data Sensor ke MQTT
- **Broker:** Eclipse Mosquitto (port 1883).
- **Topik MQTT:**
  - Ruang: `kampus/lab1/room01/telemetry`
  - Greenhouse: `kampus/greenhouse/zone1/telemetry`
- **Jalankan Publisher Sensor Ruang:**
  ```bash
  python scripts/mqtt/publish_sensor.py --count 5
  ```
- **Jalankan Publisher Sensor Greenhouse (Pertanian Presisi):**
  ```bash
  python scripts/mqtt/publish_greenhouse.py --count 3
  ```
- **Notebook Interaktif:** `notebooks/02_kirim_data_mqtt.ipynb`.
- **Log Pengiriman:** Tersimpan di `outputs/logs/publisher_room01.log` dan `outputs/logs/publisher_greenhouse.log`.

### Hands-on 4: Subscribe Data MQTT dengan Python
- **Broker lokal tanpa instalasi sistem (pengembangan):**
  ```bash
  python scripts/mqtt/run_broker.py
  ```
  (Di lab/produksi, buku memakai Eclipse Mosquitto: `mosquitto -v`.)
- **Subscriber sederhana (satu topik `kampus/lab1/room01/telemetry`):**
  ```bash
  python scripts/mqtt/subscribe_sensor.py --max-messages 3 --timeout 25
  ```
- **Subscriber wildcard multi-ruangan (`kampus/lab1/+/telemetry`):**
  ```bash
  python scripts/mqtt/subscribe_all_rooms.py --max-messages 6 --timeout 25
  ```
- **Subscriber dengan validasi payload (rentang suhu/kelembaban/CO2):**
  ```bash
  python scripts/mqtt/subscribe_validated.py --timeout 10
  ```
- **Notebook Interaktif:** `notebooks/03_subscribe_mqtt.ipynb` (menjalankan broker, 3 publisher, dan ketiga subscriber secara berurutan).
- **Log Penerimaan:** Tersimpan di `outputs/logs/subscriber_room01.log`, `outputs/logs/subscriber_all_rooms.log`, dan `outputs/logs/subscriber_validated.log`.

### Hands-on 5: Simpan Data MQTT ke CSV & SQLite
- **Simpan telemetri ke CSV (`data/raw/mqtt_room01.csv`):**
  ```bash
  python scripts/mqtt/save_to_csv.py --max-messages 5 --timeout 25
  ```
- **Simpan telemetri ke SQLite (`data/raw/iot_sensor.db`):**
  ```bash
  python scripts/mqtt/save_to_sqlite.py --max-messages 5 --timeout 25
  ```
- **Pola gabungan multi-storage (CSV + SQLite sekaligus):**
  ```bash
  python scripts/mqtt/save_to_csv_sqlite.py --max-messages 5 --timeout 25
  ```
- **(Opsional, butuh server) Simpan ke InfluxDB:**
  ```bash
  pip install influxdb-client
  python scripts/mqtt/save_to_influxdb.py --influx-url http://localhost:8086 --influx-token <TOKEN>
  ```
  Memerlukan server InfluxDB (di buku: Docker `influxdb:2.7` pada port 8086).
- **Notebook Interaktif:** `notebooks/04_simpan_data_storage.ipynb`.

### Hands-on 6: Eksplorasi Dataset Sensor dengan pandas
- **Bangkitkan dataset sintetis 1 minggu (`data/raw/room_sensor_week.csv`, 1008 baris @ 10 menit):**
  ```bash
  python scripts/generate_room_sensor_week.py
  ```
- **Eksplorasi struktur, time-series index, ringkasan operasional, korelasi:**
  ```bash
  python scripts/explore_sensor_dataset.py
  ```
- **Visualisasi eksploratif ke `outputs/figures/`:**
  ```bash
  python scripts/plot_exploration.py
  ```
- **Notebook Interaktif:** `notebooks/05_eksplorasi_dataset.ipynb`.

### Hands-on 7: Membersihkan Timestamp, Resampling, dan Imputasi
- **Bangkitkan dataset kotor (`data/raw/room_sensor_dirty.csv`):**
  ```bash
  python scripts/generate_dirty_dataset.py
  ```
- **Cleaning + resample 10 menit + imputasi (`data/processed/room_sensor_clean.csv`):**
  ```bash
  python scripts/clean_timestamp_resample.py
  ```
- **Notebook Interaktif:** `notebooks/06_cleaning_resampling.ipynb`.

### Hands-on 8: Deteksi Anomali Dasar (Aturan Domain, Z-Score, IQR)
- **Bangkitkan dataset dengan anomali (`data/raw/room_sensor_anomaly.csv`):**
  ```bash
  python scripts/generate_anomaly_dataset.py
  ```
- **Deteksi per metode:**
  ```bash
  python scripts/detect_anomaly_rules.py
  python scripts/detect_anomaly_zscore.py
  python scripts/detect_anomaly_iqr.py
  ```
- **Versi gabungan + visualisasi (`data/processed/room_sensor_anomaly_flags.csv`, `outputs/figures/anomali_*.png`):**
  ```bash
  python scripts/detect_anomaly_all.py
  python scripts/plot_anomaly.py
  ```
- **Notebook Interaktif:** `notebooks/07_deteksi_anomali.ipynb`.

### Hands-on 9: Generator Data Suhu-Kelembaban Ruangan 30 Hari
- **Generate dataset (`data/synthetic/room_30days.csv`, 4320 baris):**
  ```bash
  python scripts/generate_room_30days.py
  ```
- **Visualisasi (`outputs/figures/room_30days*.png`):**
  ```bash
  python scripts/plot_room_30days.py
  ```
- **Notebook Interaktif:** `notebooks/08_generate_room_30days.ipynb`.

### Hands-on 10: Generator Data Konsumsi Energi Berbasis Jam Kerja
- **Generate dataset energi (`data/synthetic/energy_30days.csv`):**
  ```bash
  python scripts/generate_energy_workhours.py
  ```
- **Label hemat/boros (`data/synthetic/energy_30days_labeled.csv`):**
  ```bash
  python scripts/label_energy_efficiency.py
  ```
- **Visualisasi (`outputs/figures/energy_*.png`):**
  ```bash
  python scripts/plot_energy_workhours.py
  ```
- **Notebook Interaktif:** `notebooks/09_generate_energy.ipynb`.

### Hands-on 11: Generator Data Getaran Mesin dengan Fault Injection
- **Generate sinyal getaran + fault (`data/synthetic/vibration_fault_injection.csv`, 3000 sampel):**
  ```bash
  python scripts/generate_vibration_fault.py
  ```
- **Visualisasi (`outputs/figures/vibration_fault*.png`):**
  ```bash
  python scripts/plot_vibration_fault.py
  ```
- **Notebook Interaktif:** `notebooks/10_generate_vibration_fault.ipynb`.

### Hands-on 12: Dataset Sintetis untuk Klasifikasi dan Anomaly Detection
- **Generate dataset berlabel (`data/synthetic/room_classification_dataset.csv`):**
  ```bash
  python scripts/generate_room_classification_dataset.py
  ```
- **Visualisasi sebaran label (`outputs/figures/room_classification_scatter.png`):**
  ```bash
  python scripts/plot_classification_dataset.py
  ```
- **Notebook Interaktif:** `notebooks/11_generate_classification_dataset.ipynb`.

### Hands-on 13: Ekspor Dataset ke CSV dan Publish ke MQTT Simulator
- **Publish dataset CSV ke topik `iotlab/room01/telemetry`:**
  ```bash
  python scripts/mqtt/publish_csv_to_mqtt.py --limit 20 --interval 0.05
  ```
- **Subscriber verifikasi payload:**
  ```bash
  python scripts/mqtt/subscribe_verify_mqtt.py --max-messages 20 --timeout 60
  ```
- **Publish multi-topic (warning/fault juga ke `iotlab/room01/alert`):**
  ```bash
  python scripts/mqtt/publish_multi_topic.py --limit 400 --interval 0.01
  ```
- **Notebook Interaktif:** `notebooks/12_publish_csv_mqtt.ipynb`.

### Hands-on 14: Fitur Time-Series dari Data Suhu/Kelembaban
- **Bangun fitur (lag, diff, rolling, comfort index) ke `data/processed/room_30days_features.csv`:**
  ```bash
  python scripts/feature_room_timeseries.py
  ```
- **Visualisasi fitur (`outputs/figures/features_*.png`):**
  ```bash
  python scripts/plot_room_features.py
  ```
- **Notebook Interaktif:** `notebooks/13_feature_timeseries.ipynb`.

### Hands-on 15: Fitur Getaran Sederhana (RMS, Peak, Kurtosis)
- **Ekstraksi fitur per jendela ke `data/processed/vibration_window_features.csv`:**
  ```bash
  python scripts/feature_vibration_machine.py
  ```
- **Visualisasi fitur (`outputs/figures/vibration_window_features.png`):**
  ```bash
  python scripts/plot_vibration_features.py
  ```
- **Notebook Interaktif:** `notebooks/14_feature_vibration.ipynb`.

### Hands-on 16: PCA untuk Merangkum Beberapa Sensor
- **Standarisasi + PCA 3 komponen ke `data/processed/room_30days_pca.csv`:**
  ```bash
  python scripts/pca_room_features.py
  ```
- **Visualisasi PC1 vs PC2 (`outputs/figures/room_pca_scatter.png`):**
  ```bash
  python scripts/plot_pca_room.py
  ```
- **Notebook Interaktif:** `notebooks/15_pca_room_features.ipynb`.

### Hands-on 20: Menyiapkan Dataset Klasifikasi Normal vs Abnormal
- **Siapkan fitur + split time-aware 70/15/15 ke `data/processed/classification_room/`:**
  ```bash
  python scripts/prepare_classification_dataset.py
  ```
- **Notebook Interaktif:** `notebooks/16_prepare_classification.ipynb`.

### Hands-on 21: Menyiapkan Dataset Regresi Prediksi Konsumsi Energi
- **Siapkan fitur + target 1 langkah ke depan + split time-aware ke `data/processed/regression_energy/`:**
  ```bash
  python scripts/prepare_regression_energy_dataset.py
  ```
- **Notebook Interaktif:** `notebooks/17_prepare_regression_energy.ipynb`.

### Hands-on 22: Evaluasi Baseline Model (Klasifikasi dan Regresi)
- **Baseline klasifikasi (Logistic Regression + scaler):**
  ```bash
  python scripts/evaluate_baseline_classification.py
  ```
- **Baseline regresi (Linear Regression, simpan `test_predictions.csv`):**
  ```bash
  python scripts/evaluate_baseline_regression.py
  ```
- **Notebook Interaktif:** `notebooks/18_baseline_evaluation.ipynb`.

### Hands-on 23: Prediksi Energi dengan Regresi (Linear, Ridge, Random Forest)
- **Latih dan evaluasi tiap model (prediksi disimpan ke `data/processed/regression_energy/pred_*_test.csv`):**
  ```bash
  python scripts/regression_linear_energy.py
  python scripts/regression_ridge_energy.py
  python scripts/regression_rf_energy.py
  ```
- **Bandingkan prediksi (`outputs/figures/regression_predictions_compare.png`):**
  ```bash
  python scripts/plot_regression_predictions.py
  ```
- **Notebook Interaktif:** `notebooks/19_regression_energy.ipynb`.

### Hands-on 24: Klasifikasi Status Perangkat (normal, warning, fault)
- **Siapkan dataset multi-kelas ke `data/processed/classification_status/`:**
  ```bash
  python scripts/prepare_multiclass_status_dataset.py
  ```
- **Latih dan evaluasi model:**
  ```bash
  python scripts/classification_logreg_status.py
  python scripts/classification_rf_status.py
  ```
- **Notebook Interaktif:** `notebooks/20_classification_status.ipynb`.

### Hands-on 25: Perbandingan 3 Model dengan Metrik dan Kurva
- **Bandingkan 3 klasifier (laporan ke `outputs/reports/model_comparison_status.csv`):**
  ```bash
  python scripts/compare_three_models_status.py
  ```
- **Visualisasi accuracy/F1 + kurva ROC (`outputs/figures/compare_*.png`):**
  ```bash
  python scripts/plot_model_comparison.py
  ```
- **Variasi regresi (`outputs/reports/model_comparison_regression.csv`):**
  ```bash
  python scripts/compare_three_regressors.py
  ```
- **Notebook Interaktif:** `notebooks/21_compare_models.ipynb`.

### Hands-on 21 (Bab 9): Clustering Pola Ruangan Suhu-Kelembaban
- **K-Means (uji K=2..5, laporan + scatter):**
  ```bash
  python scripts/cluster_room_kmeans.py
  ```
- **DBSCAN (pola + deteksi noise):**
  ```bash
  python scripts/cluster_room_dbscan.py
  ```
- **Output:** `outputs/reports/room_kmeans_cluster.csv`, `outputs/reports/room_dbscan_cluster.csv`, `outputs/figures/room_kmeans_scatter.png`, `outputs/figures/room_dbscan_scatter.png`.
- **Notebook Interaktif:** `notebooks/22_clustering_room.ipynb`.

### Hands-on 22 (Bab 9): Deteksi Anomali Arus Listrik dengan Isolation Forest
- **Generate dataset (ke `data/synthetic/current_sensor_anomaly.csv`):**
  ```bash
  python scripts/generate_current_anomaly_dataset.py
  ```
- **Jalankan Isolation Forest:**
  ```bash
  python scripts/isolation_forest_current.py
  ```
- **Evaluasi terhadap ground truth sintetis:**
  ```bash
  python scripts/evaluate_iforest_current.py
  ```
- **Notebook Interaktif:** `notebooks/23_isolation_forest_current.ipynb`.

### Hands-on 23 (Bab 9): Threshold Statis vs Isolation Forest
- **Deteksi threshold statis:**
  ```bash
  python scripts/current_threshold_detection.py
  ```
- **Bandingkan metrik kedua metode:**
  ```bash
  python scripts/compare_threshold_vs_iforest.py
  ```
- **Visualisasi F1 dan recall:**
  ```bash
  python scripts/plot_threshold_vs_iforest.py
  ```
- **Notebook Interaktif:** `notebooks/24_threshold_vs_iforest.ipynb`.

### Hands-on 24 (Bab 10): Forecasting Suhu Ruang
- **Siapkan dataset (ke `data/processed/forecast_room/`):**
  ```bash
  python scripts/prepare_room_forecast_dataset.py
  ```
- **Baseline last value & moving average:**
  ```bash
  python scripts/baseline_room_forecast.py
  ```
- **Linear Regression berbasis lag:**
  ```bash
  python scripts/linear_regression_room_forecast.py
  ```
- **Visualisasi perbandingan:**
  ```bash
  python scripts/plot_room_forecast_comparison.py
  ```
- **Notebook Interaktif:** `notebooks/25_forecasting_suhu.ipynb`.

### Hands-on 25 (Bab 10): Forecasting Konsumsi Energi Harian
- **Baseline Linear Regression:**
  ```bash
  python scripts/forecast_energy_linear.py
  ```
- **Random Forest Regressor:**
  ```bash
  python scripts/forecast_energy_rf.py
  ```
- **Visualisasi perbandingan:**
  ```bash
  python scripts/plot_energy_forecast.py
  ```
- **Notebook Interaktif:** `notebooks/26_forecasting_energi.ipynb`.

### Hands-on 26 (Bab 10): Baseline vs Random Forest vs LSTM Mini
- **Random Forest pada fitur lag:**
  ```bash
  python scripts/forecast_room_rf.py
  ```
- **Siapkan sequence LSTM (ke `data/processed/lstm_room/`):**
  ```bash
  python scripts/prepare_lstm_room_sequences.py
  ```
- **Latih LSTM mini (membutuhkan `pip install tensorflow-cpu`):**
  ```bash
  python scripts/lstm_room_forecast.py
  ```
- **Perbandingan akhir + bar chart:**
  ```bash
  python scripts/compare_room_forecast_models.py
  python scripts/plot_room_forecast_model_comparison.py
  ```
- **Notebook Interaktif:** `notebooks/27_benchmark_forecasting.ipynb`.

### Hands-on 27 (Bab 11): Ekspor Model ke Format Ringan
- **Jalur A - scikit-learn ke joblib (`outputs/models/room_status_rf.joblib`):**
  ```bash
  python scripts/export_sklearn_model.py
  ```
- **Jalur B - Keras ke TFLite (`outputs/models/room_binary.keras` + `.tflite`; membutuhkan `pip install tensorflow-cpu`):**
  ```bash
  python scripts/export_keras_to_tflite.py
  ```
- **Notebook Interaktif:** `notebooks/28_export_model.ipynb`.

### Hands-on 28 (Bab 11): Simulasi Inferensi Lokal di Edge
- **Inferensi scikit-learn (joblib):**
  ```bash
  python scripts/simulate_edge_inference_sklearn.py --max-rows 30 --delay 0.05
  ```
- **Inferensi TFLite (membutuhkan `pip install tensorflow-cpu`):**
  ```bash
  python scripts/simulate_edge_inference_tflite.py --max-rows 30 --delay 0.05
  ```
- **Notebook Interaktif:** `notebooks/29_edge_inference.ipynb`.

### Hands-on 29 (Bab 11): Mini Proyek Klasifikasi Edge (Raspberry Pi / Emulator)
- **Versi tanpa MQTT (log ke `outputs/reports/edge_room_predictions.csv`):**
  ```bash
  python scripts/edge_room_classifier_project.py --steps 30 --delay 0.05
  ```
- **Versi dengan MQTT (butuh broker lokal, misal `python scripts/mqtt/run_broker.py`):**
  ```bash
  python scripts/edge_room_classifier_mqtt.py --steps 20 --delay 0.05
  ```
- **Notebook Interaktif:** `notebooks/30_mini_proyek_edge.ipynb`.

### Hands-on 30 (Bab 12): Pipeline Lengkap MQTT -> Prediksi -> Storage -> Dashboard
- **Simulator sensor (butuh broker lokal, misal `python scripts/mqtt/run_broker.py`):**
  ```bash
  python scripts/publisher_room_simulator.py --count 20 --interval 1
  ```
- **Subscriber pipeline (preprocessing + prediksi + storage CSV; tambahkan `--influx --influx-token <token>` untuk InfluxDB sesuai buku):**
  ```bash
  python scripts/pipeline_room_subscriber.py --max-messages 10 --timeout 60
  ```
- **Dashboard (opsional, sesuai buku):** jalankan InfluxDB 2 (`docker run -d -p 8086:8086 influxdb:2`, org `iotlab`, bucket `sensor_data`) dan Grafana (`docker run -d -p 3000:3000 grafana/grafana-oss`), tambahkan InfluxDB sebagai data source, lalu susun panel suhu/kelembaban/CO2/daya/status dengan ambang warna normal-hijau, warning-kuning, fault-merah.
- **Output CSV:** `outputs/reports/pipeline_room_predictions.csv`.
- **Notebook Interaktif:** `notebooks/31_pipeline_lengkap.ipynb`.

### Hands-on 31 (Bab 12): Alert Sederhana untuk Skor Anomali Tinggi
- **Subscriber pipeline + alert (alert ke topik `iotlab/room01/alert` dan CSV `outputs/reports/pipeline_room_alerts.csv`):**
  ```bash
  python scripts/pipeline_room_with_alert.py --max-messages 10 --timeout 60
  ```
- **Pantau topik alert di terminal lain:**
  ```bash
  python scripts/mqtt/subscribe_sensor.py --topic "iotlab/room01/alert"
  ```
- **Aturan alert:** model memprediksi FAULT, atau suhu > 32 C dan CO2 > 1200 ppm bersamaan. Tambahkan `--influx --influx-token <token>` untuk storage InfluxDB sesuai buku.
- **Notebook Interaktif:** `notebooks/32_pipeline_alert.ipynb`.

### Hands-on 32 (Bab 13): Monitoring Data Drift
- **Bandingkan distribusi baseline vs current + indikator drift:**
  ```bash
  python scripts/monitor_data_distribution.py
  ```
- **Output:** `outputs/reports/data_distribution_monitor.csv`, `outputs/figures/dist_compare_temperature_c.png`, `outputs/figures/dist_compare_humidity_pct.png`.
- **Notebook Interaktif:** `notebooks/33_data_drift.ipynb`.

### Hands-on 33 (Bab 13): Feature Importance
- **Ekstrak feature importance Random Forest + narasi:**
  ```bash
  python scripts/feature_importance_room_model.py
  ```
- **Output:** `outputs/reports/feature_importance_room_model.csv`, `outputs/figures/feature_importance_room_model.png`.
- **Notebook Interaktif:** `notebooks/34_feature_importance.ipynb`.

### Hands-on 34 (Bab 13): Checklist Operasional Sistem IoT-ML
- **Generate template checklist:**
  ```bash
  python scripts/generate_operational_checklist.py
  ```
- **Output:** `outputs/reports/iot_ml_operational_checklist.md`.
- **Notebook Interaktif:** `notebooks/35_operational_checklist.ipynb`.

### Hands-on 35: Studi Kasus A - Smart Room Monitoring
- **Latih model kenyamanan (ke `outputs/models/case_a_room_rf.joblib`):**
  ```bash
  python scripts/case_a_train_room_model.py
  ```
- **Publisher simulator (butuh broker lokal):**
  ```bash
  python scripts/case_a_room_publisher.py --count 20 --interval 1
  ```
- **Subscriber + klasifikasi (storage CSV; `--influx` untuk InfluxDB sesuai buku):**
  ```bash
  python scripts/case_a_room_subscriber.py --max-messages 10 --timeout 60
  ```
- **Notebook Interaktif:** `notebooks/36_studi_kasus_a.ipynb`.

### Hands-on 36: Studi Kasus B - Predictive Maintenance
- **Generate data motor (ke `data/synthetic/case_b_motor.csv`):**
  ```bash
  python scripts/case_b_generate_motor_data.py
  ```
- **Ekstraksi fitur per jendela (ke `data/processed/case_b_motor_features.csv`):**
  ```bash
  python scripts/case_b_feature_window.py
  ```
- **Isolation Forest + klasifikasi fault:**
  ```bash
  python scripts/case_b_detect_and_classify.py
  ```
- **Notebook Interaktif:** `notebooks/37_studi_kasus_b.ipynb`.

### Hands-on 37: Studi Kasus C - Smart Energy Analytics
- **Generate data energi (ke `data/synthetic/case_c_energy.csv`):**
  ```bash
  python scripts/case_c_generate_energy.py
  ```
- **Forecasting beban + alert (ke `outputs/reports/case_c_energy_results.csv`):**
  ```bash
  python scripts/case_c_energy_forecast_alert.py
  ```
- **Notebook Interaktif:** `notebooks/38_studi_kasus_c.ipynb`.

### Hands-on 38 (Bab 15): Proyek Akhir End-to-End (Capstone)
- **Latih baseline Isolation Forest (ke `outputs/models/capstone_iforest.joblib`). Baseline dilatih pada rentang operasi normal deployment (rentang payload normal publisher) sesuai prinsip Bab 13; formula model persis buku (n_estimators=200, contamination=0.05, random_state=42):**
  ```bash
  python scripts/inference/train_capstone_iforest.py
  ```
- **Publisher simulator (butuh broker lokal):**
  ```bash
  python scripts/publishers/capstone_publisher.py --count 20 --interval 1
  ```
- **Subscriber (validasi + threshold + Isolation Forest, storage CSV; `--influx` untuk InfluxDB sesuai buku):**
  ```bash
  python scripts/subscribers/capstone_subscriber.py --max-messages 10 --timeout 60
  ```
- **Subscriber dengan alert (alert ke `capstone/iotnode01/alert`):**
  ```bash
  python scripts/subscribers/capstone_subscriber_with_alert.py --max-messages 15 --timeout 60
  ```
- **Output:** `outputs/reports/capstone_monitoring.csv`, `outputs/reports/capstone_alerts.csv`.
- **Notebook Interaktif:** `notebooks/39_proyek_akhir_capstone.ipynb`.

### Hands-on 39 (Bab 15): Notifikasi Sederhana
- **Listener notifikasi alert (butuh broker lokal dan pipeline Hands-on 38 berjalan):**
  ```bash
  python scripts/capstone_alert_listener.py --max-messages 5 --timeout 60
  ```
- **Output:** `outputs/reports/capstone_notifications.csv`.
- **Notebook Interaktif:** `notebooks/40_notifikasi.ipynb`.

### Hands-on 40 (Bab 15): Uji Beban dan Skenario Pengembangan Lanjut
- **Uji volume (default 1000 pesan, jeda 0.05 detik):**
  ```bash
  python scripts/publishers/capstone_stress_publisher.py --count 1000 --interval 0.05
  ```
- **Uji payload rusak (3 payload buruk):**
  ```bash
  python scripts/publishers/capstone_bad_payload_publisher.py
  ```
- **Uji drift buatan (default 500 pesan):**
  ```bash
  python scripts/publishers/capstone_drift_publisher.py --count 500 --interval 0.1
  ```
- Jalankan bersama `scripts/subscribers/capstone_subscriber.py` dan amati checklist uji beban (stabilitas broker/subscriber, error handling, storage, kebisingan alert, tanda drift).
- **Notebook Interaktif:** `notebooks/41_stress_test.ipynb`.
