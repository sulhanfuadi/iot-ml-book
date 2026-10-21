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
│   └── 01_baca_data_sensor.ipynb
├── outputs/
│   ├── figures/           # Hasil visualisasi grafik (PNG)
│   │   ├── plot_suhu_ruangan.png
│   │   ├── temperature.png
│   │   ├── humidity.png
│   │   ├── co2.png
│   │   └── temperature_vs_co2.png
│   └── reports/           # Laporan dan metrik model
├── scripts/               # Skrip Python executable
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
- **Notebook Interaktif:** `notebooks/01_baca_data_sensor.ipynb` (eksplorasi grafik time series dan scatter plot relasi suhu vs CO2).
- **Hasil Olahan:** Data bertipe datetime disimpan ke `data/processed/room_sensor_clean.csv`.
