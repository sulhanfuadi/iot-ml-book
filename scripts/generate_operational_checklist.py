"""
Hands-on 34 (Bab 13): Checklist Operasional Sistem IoT-ML
Buku Referensi: IoT Terintegrasi dengan Machine Learning & Data Analytics (Onno W. Purbo)

Menghasilkan template checklist operasional dalam Markdown agar tim bisa memakainya
berulang (sebelum demo, deployment mini, setelah retraining, dsb).
Output: outputs/reports/iot_ml_operational_checklist.md
"""

from pathlib import Path

OUTPUT_PATH = Path("outputs/reports/iot_ml_operational_checklist.md")

CONTENT = """# Checklist Operasional Sistem IoT-ML

## A. Data & Sensor
- [ ] Semua field wajib tersedia pada payload (`timestamp`, `device_id`, sensor utama)
- [ ] Tipe data numerik sudah diverifikasi
- [ ] Rentang nilai sensor masuk akal
- [ ] Timestamp valid dan konsisten
- [ ] Data hilang dicatat
- [ ] Data rusak / log parsing error dicatat

## B. MQTT & Jaringan
- [ ] Broker MQTT berjalan stabil
- [ ] Topik telemetry dan alert dipisah
- [ ] Autentikasi minimum diterapkan
- [ ] Hak publish/subscribe jelas
- [ ] Pesan uji berhasil masuk dan diterima subscriber

## C. Preprocessing
- [ ] Semua fitur yang dibutuhkan model tersedia
- [ ] Lag / rolling feature punya fallback bila data awal belum cukup
- [ ] Data invalid tidak langsung masuk ke model
- [ ] Pipeline preprocessing konsisten dengan saat training

## D. Model
- [ ] File model aktif tersedia
- [ ] Versi model tercatat
- [ ] Metadata model tersedia (tanggal training, metrik)
- [ ] Feature importance / penjelasan ringan tersedia
- [ ] Model diuji pada data terbaru

## E. Inferensi
- [ ] Inferensi berjalan otomatis
- [ ] Error inferensi tercatat
- [ ] Latensi inferensi masih wajar
- [ ] Output model tersimpan

## F. Storage
- [ ] Data mentah tersimpan
- [ ] Hasil inferensi tersimpan
- [ ] Alert tersimpan
- [ ] Historis dapat dibaca ulang untuk retraining

## G. Dashboard & Alert
- [ ] Dashboard menampilkan sensor utama
- [ ] Dashboard menampilkan hasil model
- [ ] Alert terlihat jelas
- [ ] Alert tidak terlalu sering salah
- [ ] Operator paham makna tiap panel utama

## H. Monitoring Drift & Retraining
- [ ] Distribusi fitur utama dimonitor
- [ ] Error model dipantau
- [ ] Drift dicatat
- [ ] Jadwal retraining sederhana tersedia

## I. Stress Test
- [ ] Pipeline pernah diuji dengan payload rusak
- [ ] Pipeline pernah diuji dengan anomali sintetis
- [ ] Pipeline pernah diuji dengan volume data lebih tinggi
- [ ] Sistem tetap stabil saat uji beban ringan

## Kesimpulan
- [ ] Sistem siap untuk demo internal
- [ ] Sistem siap untuk pilot terbatas
- [ ] Sistem butuh perbaikan sebelum dipakai
"""


def main():
  OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
  OUTPUT_PATH.write_text(CONTENT, encoding="utf-8")
  print("[SUKSES] Checklist disimpan ke:", OUTPUT_PATH)


if __name__ == "__main__":
  main()
