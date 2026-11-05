# Sistem Desain UI/UX & Standar Kartografi — SIG Kalurahan Pondokrejo

Dokumen ini mendefinisikan palet warna, tipografi, token desain, geometri kartografis, dan hierarki visual yang digunakan di seluruh antarmuka aplikasi.

---

## 1. Visual DNA & Palet Warna

Aplikasi mengadopsi gaya **Non-Rounded Administrative Enterprise** yang bersih, fungsional, dan berkontras tinggi:

### A. Skema Warna Utama
- **Primary Brand (Kalurahan Blue):** `#1d4ed8` (Blue 700) — Digunakan untuk batas luar desa, header detail warga, dan aksen aktif.
- **Secondary Accent (Emerald):** `#059669` (Emerald 600) — Digunakan untuk badge desil mampu, ikon toponimi, dan tombol aksi.
- **Surface / Background:** `#f8fafc` (Slate 50) & `#ffffff` (White).
- **Text Main:** `#0f172a` (Slate 900) & Text Sub: `#475569` (Slate 600).

### B. Skema Warna Desil Kesejahteraan (SSOT)
- 🔴 **Desil 1 (Sangat Miskin):** `#ef4444` (Red 500)
- 🟠 **Desil 2 (Miskin):** `#f97316` (Orange 500)
- 🟡 **Desil 3 (Hampir Miskin):** `#eab308` (Yellow 500)
- 🟢 **Desil 4+ (Mampu):** `#10b981` (Emerald 500)

---

## 2. Standar Kartografi & Hierarki Garis Peta

1. **Batas Luar Kalurahan (Dual-Tone Halo Casing):**
   - *Halo Casing (Layer Bawah):* `#ffffff`, tebal `4.6px`, opacity `0.95`.
   - *Garis Utama (Layer Atas):* `#1d4ed8`, tebal `2.8px`, solid.
   - *Tujuan:* Menjamin batas kalurahan selalu terlihat tajam dan terbaca jelas di atas seluruh jenis basemap (Satelit, Sawah, Pemukiman, Terang, maupun Gelap).
2. **Batas Padukuhan (Clean Planar Edges):**
   - *Garis:* `#2563eb`, tebal `2.2px`, pola putus-putus `[4, 2]`.
   - *Label Toponimi:* Huruf kapital (*uppercase*), halo putih `2.5px`, font `Noto Sans Regular`.
   - *Perilaku Fokus:* Ketika padukuhan tertentu dipilih, seluruh garis dan label padukuhan lain otomatis diredam, memfokuskan visual hanya pada padukuhan aktif.
3. **Marker Penduduk:**
   - *Lingkaran Titik:* Radius `5px`, stroke putih `2px` (`#ffffff`), fill sesuai warna desil.

---

## 3. Komponen Antarmuka & Responsivitas

- **Laptop-First Optimization (1366×768):** Layout peta 2-kolom dengan sidebar kanan Veda selebar 380px dan area kanvas peta maksimal.
- **Non-Rounded Geometry:** Dropdown, panel detail, legenda floating, dan kartu filter menggunakan radius presisi (`rounded-none` / `rounded-sm`) yang mencerminkan ketegasan sistem informasi pemerintahan.
- **Peta Dasar 4 Mode:** Standar (Liberty), Satelit (Esri), Terang (Positron), dan Gelap (Dark) yang dapat dialihkan secara instan melalui kontrol di pojok kanan atas kanvas.
