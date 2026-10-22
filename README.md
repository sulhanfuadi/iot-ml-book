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
