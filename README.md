# Sistem Informasi Geografis & Analitik Kependudukan Kalurahan Pondokrejo

Aplikasi Sistem Informasi Geografis (SIG) dan Dasbor Analitik Kependudukan berbasis web untuk Kalurahan Pondokrejo, Kapanewon Tempel, Kabupaten Sleman, D.I. Yogyakarta. 

Aplikasi ini mengintegrasikan data sosial ekonomi kependudukan (desil kesejahteraan, kepesertaan bansos, stunting, kelompok rentan, demografi usia) dengan data geospasial kalurahan (batas wilayah resmi, 9 padukuhan resmi, alokasi RW/RT, fasilitas umum, jaringan jalan, pemukiman terpotong batas yurisdiksi, serta zona risiko bencana Merapi).

Domain Produksi: **[https://peta.pondokrejo.id](https://peta.pondokrejo.id)**

---

## 1. Arsitektur & Mesin Peta (MapLibre GL 2D)

Aplikasi dibangun menggunakan arsitektur single-binary Golang performa tinggi dengan engine visualisasi peta vektor **MapLibre GL JS v4.7.1 (2D Strict Mode)**:

- **Bebas Kuota & Tanpa API Key Berbayar:** Seluruh peta dasar (*basemap*) menggunakan sumber terbuka legal dari OpenFreeMap dan Esri World Imagery tanpa batasan kuota atau blokir referrer.
- **Pilihan Layer Peta On-Map (4 Pilihan):** Kontrol layer di pojok kanan atas kanvas menyediakan tombol beralih cepat:
  - **Standar**: OpenFreeMap Liberty (vektor jalan, toponimi, dan kontur halus)
  - **Satelit**: Esri World Imagery (resolusi tinggi dengan penanganan glyphs font otomatis)
  - **Terang**: OpenFreeMap Positron (minimalis abu-abu terang)
  - **Gelap**: OpenFreeMap Dark (kontras tinggi untuk presentasi malam/analisis tematik)
- **Batas Kalurahan Dual-Tone Casing:** Batas luar Kalurahan Pondokrejo menggunakan *white halo casing* (`#ffffff`, 4.6px) dan garis solid biru pekat (`#1d4ed8`, 2.8px) yang selalu terkunci di layer teratas (`ensureBoundaryOnTop`), sehingga tidak pernah tertutup oleh poligon sawah, pemukiman, atau KRB.
- **Normalisasi 9 Padukuhan Resmi (Clean Planar Tessellation):** Lapisan batas padukuhan (`layers/padukuhan.geojson`) bebas 100% dari tumpang tindih (*overlap* 0 m²) dan celah (*gap* 0 m²), dengan garis batas bersama tunggal (*shared edges*) yang rapi dan bebas dari tampilan garis ganda/bergerigi.
- **WebGL 4-Tier Z-Index Stacking:** Pengorganisasian visual yang tertib mencegah layer area (pemukiman/sawah) menutupi jaringan jalan, titik fasilitas, atau garis batas administratif desa.
- **Dual-Sidebar Spatial Harmonization:**
  - **Bilah Navigasi Kiri (Saklar Layer):** Mengontrol visibilitas layer (Batas Padukuhan, Batas RW/RT, Pemukiman, Jaringan Jalan, Warga, Mitigasi Bencana).
  - **Bilah Navigasi Kanan (Filter Wilayah & Analitik):** Mengontrol fokus wilayah (9 Padukuhan) dan atribut kependudukan.
  - Saat padukuhan dipilih (misal: "Dukuh"), padukuhan aktif di-highlight dengan garis tebal biru (`#1d4ed8`) dan arsiran halus, sementara 8 padukuhan lainnya bertransformasi menjadi garis kontur konteks yang halus (`#94a3b8`) agar pengguna tetap memiliki orientasi batas wilayah desa.

---

## 2. Fitur Utama Aplikasi

### A. Peta Sebaran Penduduk (`/`)
- **Visualisasi Desil Kesejahteraan Sosial-Ekonomi:**
  - 🔴 **Desil 1**: Sangat Miskin
  - 🟠 **Desil 2**: Miskin
  - 🟡 **Desil 3**: Hampir Miskin
  - 🟢 **Desil 4+**: Menengah ke Atas / Mampu
- **Marker Clustering & Heatmap:** Pengelompokan titik dinamis berbasis zoom dengan popup detail Kepala Keluarga, No KK, Dusun, RT/RW, dan daftar bantuan sosial (BPNT, PKH, BLT, dll).
- **Sinkronisasi Data Presisi 100%:** Penanganan klik titik marker menggunakan *Direct Unique Index Binding* (`_id`) untuk memastikan data di popup peta selalu identik dan sinkron dengan panel samping kanan.
- **Mode Pemilihan Layer Ganda:**
  - **Mode Sederhana (Preset Tematik & Tombol Cepat):** Pintasan cepat untuk Padukuhan, RW/RT, Pemukiman, Jaringan Jalan, Titik Persebaran Warga, dan Mitigasi Bencana.
  - **Mode Detail (Layer Spasial Lengkap):** Kontrol granular atas seluruh layer spasial (pemukiman, sawah, sungai, irigasi, jalan, kontur, toponimi, jalur evakuasi, barak pengungsian, dan fasilitas umum).

### B. Dasbor Analisa Wilayah & Demografi (Tab Interaktif di Sidebar)
- **Sinkronisasi Filter Real-Time:** Statistik otomatis menyesuaikan dengan filter padukuhan, status desil, dan bansos yang aktif di peta.
- **Piramida Penduduk Seimbang:** Visualisasi struktur demografi kelompok umur (0-4 s/d 75+ tahun) terbagi proporsional berdasarkan jenis kelamin Laki-laki dan Perempuan.
- **Indikator Rasio Ketergantungan (*Dependency Ratio*):** Perbandingan populasi non-produktif (usia <15 dan >64) terhadap usia produktif (15-64).
- **Kamus Label Survei Baku:** Pemetaan otomatis kode survei numerik menjadi label deskriptif manusia (Pendidikan, Jenis Pekerjaan, Sumber Air Minum Bersih, dan Fasilitas Jamban/Sanitasi).
- **Tabel Distribusi Sebaran Wilayah (RT & RW):** Rekapitulasi jumlah KK dan jiwa per kombinasi resmi RT/RW per padukuhan yang dinamis mengikuti cakupan filter.

### C. Editor Marker & Spasial (`/editor`)
- **Pergeseran Marker KK:** Drag-and-drop marker keluarga langsung di peta untuk memperbarui koordinat lintang/bujur secara presisi.
- **Digitasi Batas Wilayah:** Pembuatan dan penyuntingan garis atau poligon batas Padukuhan, RW, dan RT secara visual.
- **Manajemen Titik Fasilitas:** Penambahan dan penandaan titik fasilitas umum desa (masjid, sekolah, kantor desa, posyandu).
- **Simpan Status:** Sinkronisasi langsung ke penyimpanan state editor (`editor_state.json`) dengan proteksi otentikasi administrator.

### D. Dashboard Analitik Kependudukan & Bansos (`/analytics` & `/bansos`)
- Piramida penduduk makro, distribusi usia kerja, dan rasio ketergantungan desa.
- Analisis *inclusion* dan *exclusion error* bantuan sosial berdasarkan desil kesejahteraan riil.
- Pemantauan keluarga berisiko stunting dan ibu hamil.

### E. Rekomendasi Kebijakan Berbasis Data (`/recommendations`)
- Laporan rekomendasi kebijakan berbasis data spasial dan sosial-ekonomi yang siap dicetak untuk pimpinan dan pengambil keputusan Kalurahan Pondokrejo.

---

## 3. Data Kependudukan & Rekapitulasi 9 Padukuhan

Total populasi terdata: **2.021 KK unik** (6.353 jiwa) bebas duplikasi data dan 0 KK outlier di luar batas desa:

| No | Padukuhan Resmi | Alokasi RW Resmi | Alokasi RT Resmi | Jumlah KK | Titik Centroid Resmi |
|---|---|---|---|---|---|
| 1 | **Ngentak** | RW 01 – RW 02 | RT 01 – RT 04 | 247 KK | `[110.31169, -7.65448]` |
| 2 | **Plotengan** | RW 03 – RW 04 | RT 01 – RT 07 | 270 KK | `[110.31029, -7.65922]` |
| 3 | **Jlopo** | RW 05 – RW 06 | RT 01 – RT 04 | 164 KK | `[110.30538, -7.65750]` |
| 4 | **Karanglo** | RW 07 – RW 08 | RT 01 – RT 04 | 129 KK | `[110.31072, -7.66543]` |
| 5 | **Dukuh** | RW 09 – RW 10 | RT 01 – RT 05 | 213 KK | `[110.31497, -7.66730]` |
| 6 | **Jlapan** | RW 11 – RW 13 | RT 01 – RT 07 | 292 KK | `[110.30131, -7.66259]` |
| 7 | **Banjarharjo** | RW 14 – RW 15 | RT 01 – RT 04 | 185 KK | `[110.30579, -7.66443]` |
| 8 | **Glagahombo** | RW 16 – RW 17 | RT 01 – RT 05 | 226 KK | `[110.30810, -7.67037]` |
| 9 | **Watupecah** | RW 18 – RW 20 | RT 01 – RT 07 | 295 KK | `[110.30146, -7.66725]` |

- **Batas Resmi Wilayah:** Menggunakan batas resmi BIG / Pemkab Sleman 2023 (`layers/boundary.geojson`).
- **Presisi Koordinat 5 Desimal:** Seluruh layer GeoJSON dan koordinat penduduk terstandarisasi presisi 5 desimal (~1,1 meter).
- **Format Identitas Baku:** 100% No KK dan NIK disimpan dalam format string angka 16 digit murni.

---

## 4. Keamanan & Kepatuhan Perlindungan Data Pribadi (UU PDP No. 27/2022)

Sistem telah diaudit dan memenuhi 15 Security Patterns (SP) serta undang-undang perlindungan data pribadi:
- **Sensor Data Pribadi Publik (Dynamic PII Masking):** 100% dari 6.353 NIK dan 2.021 No KK publik disamarkan menjadi `340414******0007` pada endpoint `/residents.json`. Data unmasked 16 digit murni hanya dapat diakses oleh administrator terotentikasi.
- **Server-Side Authentication & Session Signing:** Endpoint mutasi koordinat `POST /editor/save` dan antarmuka `/editor` dikunci ketat dengan middleware `RequireAdmin()` berbasis kuki sesi terenkripsi HMAC-SHA256 (`pondokrejo_session`).
- **Anti-Scraping Rate Limiting:** Konfigurasi Nginx membatasi frekuensi request download massal kependudukan (`limit_req_zone` rate=3r/s burst=5) yang memicu status `429 Too Many Requests`.
- **Keamanan Transport:** Header `Strict-Transport-Security` (HSTS), `X-Frame-Options`, dan `X-Content-Type-Options` aktif penuh.

---

## 5. Struktur Repositori

```
peta_pondokrejo_main/
├── .docs/                      # Dokumentasi teknis terpusat (9 berkas standar)
│   ├── architecture.md         # Arsitektur sistem, WebGL 4-tier & dual-sidebar
│   ├── api-spec.md             # Spesifikasi rute API & payload otentikasi
│   ├── database.md             # Skema kependudukan & katalog layer terpotong
│   ├── routes.md               # Pemetaan route & middleware backend
│   ├── dependency-graph.md     # Graf dependensi Go, embed & frontend
│   ├── quality_review.md       # Audit kualitas kode & evidence faktual
│   ├── issues.md               # Pelacak isu & riwayat bug (ISSUE-001 s/d ISSUE-013)
│   ├── security-audit.md       # Audit keamanan & matriks kepatuhan 15 SP
│   └── design-system.md        # Desain UI/UX & standar kartografi
├── main.go                     # Entry point server Gin & embedded assets
├── analytics.go                # Logika pemrosesan analitik kependudukan
├── bansos_analytics.go         # Logika analitik perlindungan sosial
├── parser.go                   # Parser Excel BPS (deduplikasi & normalisasi)
├── editor_storage.go           # Penyimpanan state revisi koordinat editor
├── geo_clip.go                 # Utilitas clipping GeoJSON
├── editor_state.json           # State persistensi pergeseran marker
├── residents.json              # Data kependudukan 2.021 KK teroptimasi
├── layers/                     # Direktori berkas GeoJSON tematik terpotong batas
│   ├── boundary.geojson        # Batas kalurahan resmi BIG/Sleman 2023
│   ├── padukuhan.geojson       # Batas 9 Padukuhan (Clean Planar Tessellation)
│   ├── pemukiman-area.geojson  # Poligon pemukiman warga dalam yurisdiksi desa
│   ├── sawah-area.geojson      # Poligon area persawahan desa
│   ├── sungai-line.geojson     # Jaringan sungai terpotong batas desa
│   ├── jalan-line.geojson      # Jaringan jalan terpotong batas desa
│   └── ...                     # Layer tematik lainnya
├── templates/                  # Template antarmuka web (Go embed)
│   ├── index.html              # Peta sebaran interaktif utama
│   ├── editor.html             # Editor spasial marker & batas wilayah
│   ├── login.html              # Halaman login administrator
│   ├── analytics.html          # Dasbor grafik analitik kependudukan
│   ├── bansos.html             # Dasbor perlindungan sosial & bansos
│   └── recommendations.html    # Dokumen rekomendasi kebijakan
├── app-context.md              # Snapshot state aktif proyek
├── handover.md                 # Dokumen serah terima sesi & status teknis
└── run.sh                      # Skrip proses runner produksi (Linux)
```

---

## 6. Menjalankan Aplikasi Secara Lokal

### Prasyarat
- Go versi 1.22 atau lebih baru
- Browser modern dengan dukungan WebGL (Chrome, Firefox, Edge, Safari)

### Langkah Menjalankan
1. Masuk ke direktori proyek:
   ```bash
   cd /path/to/peta_pondokrejo_main
   ```
2. Jalankan aplikasi via Go:
   ```bash
   go run .
   ```
3. Buka browser pada alamat:
   ```
   http://localhost:8080/
   ```

### Kompilasi Binary Produksi (Linux amd64 & Windows)
```bash
# Kompilasi untuk Server Linux VPS
GOOS=linux GOARCH=amd64 go build -o pondokrejo-app-linux .

# Kompilasi untuk Windows
go build -o pondokrejo-app.exe .
```
