# Sistem Informasi Geografis & Analitik Kependudukan Kalurahan Pondokrejo

Aplikasi Sistem Informasi Geografis (SIG) dan Dasbor Analitik Kependudukan berbasis web untuk Kalurahan Pondokrejo, Kapanewon Tempel, Kabupaten Sleman, D.I. Yogyakarta. 

Aplikasi ini mengintegrasikan data sosial ekonomi penduduk (desil kesejahteraan, kepesertaan bansos, stunting, kelompok rentan) dengan data geospasial kalurahan (batas wilayah resmi, padukuhan, RW, RT, fasilitas umum, serta zona risiko bencana Merapi).

---

## 1. Arsitektur & Mesin Peta (MapLibre GL 2D)

Aplikasi telah dimigrasikan dari Leaflet raster menuju **MapLibre GL JS v4.7.1 (Engine Vektor 2D)**.

- **Bebas Error 403 & Tanpa API Key:** Seluruh basemap menggunakan sumber terbuka legal dari OpenFreeMap dan Esri World Imagery tanpa kuota atau blokir referrer.
- **Pilihan Layer Peta On-Map:** Tombol kontrol layer di pojok kanan atas peta menyediakan 4 pilihan gaya peta dasar:
  - **Standar**: OpenFreeMap Liberty (vektor jalan, toponimi, dan kontur halus)
  - **Satelit**: Esri World Imagery (resolusi tinggi dengan *glyph font stack* otomatis)
  - **Terang**: OpenFreeMap Positron (minimalis abu-abu terang)
  - **Gelap**: OpenFreeMap Dark (kontras tinggi untuk presentasi malam/analisis tematik)
- **Batas Kalurahan Dual-Tone Casing:** Batas luar Kalurahan Pondokrejo menggunakan *white halo casing* (`#ffffff`, 4.6px) dan garis solid biru pekat (`#1d4ed8`, 2.8px) yang selalu terkunci di layer teratas (`ensureBoundaryOnTop`), sehingga tidak pernah tertutup oleh poligon sawah, pemukiman, atau KRB.

---

## 2. Fitur Utama

### A. Peta Sebaran Penduduk (`/`)
- **Visualisasi Desil Kesejahteraan:**
  - 🔴 **Desil 1**: Sangat Miskin
  - 🟠 **Desil 2**: Miskin
  - 🟡 **Desil 3**: Hampir Miskin
  - 🟢 **Desil 4+**: Menengah ke Atas / Mampu
- **Marker Clustering & Heatmap:** Pengelompokan titik dinamis berbasis zoom dengan popup detail Kepala Keluarga, No KK, Dusun, dan daftar bantuan sosial (BPNT, PKH, BLT, dll).
- **Mode Pemilihan Layer Ganda:**
  - **Mode Sederhana (Preset Tematik):** Pintasan cepat untuk Padukuhan, RW/RT, Pemukiman, Sebaran Warga, dan Mitigasi Bencana.
  - **Mode Detail (23 Layer Spasial):** Kontrol penuh atas seluruh layer spasial (pemukiman, sawah, sungai, irigasi, jalan, kontur, tambang, toponimi, KRB 1–3, jalur evakuasi, barak pengungsian, titik kumpul, dan EWS).

### B. Editor Marker & Spasial (`/editor`)
- **Autentikasi Terintegrasi:** Dilengkapi proteksi sesi login admin.
- **Pergeseran Marker KK:** Drag-and-drop marker keluarga langsung di peta untuk memperbarui koordinat lintang/bujur secara presisi.
- **Digitasi Batas Wilayah:** Pembuatan dan penyuntingan garis atau poligon batas Padukuhan, RW, dan RT secara visual.
- **Manajemen Titik Fasilitas:** Penambahan dan penandaan titik fasilitas umum desa (masjid, sekolah, kantor, posyandu).
- **Simpan Status:** Sinkronisasi langsung ke penyimpanan state editor (`editor_state.json`).

### C. Dashboard Analitik Kependudukan (`/analytics`)
- Piramida penduduk, distribusi usia kerja, rasio ketergantungan.
- Analisis korelasi status pekerjaan dan penerima bantuan sosial.
- Grafik interaktif menggunakan Chart.js.

### D. Dashboard Perlindungan Sosial (`/bansos`)
- Validasi data penerima program bansos (PKH, BPNT, BLT-DD).
- Analisis *inclusion* dan *exclusion error* berdasarkan desil riil.
- Pemantauan keluarga berisiko stunting dan ibu hamil.

### E. Rekomendasi Hasil Analitik (`/recommendations`)
- Laporan rekomendasi kebijakan berbasis data spasial dan sosial-ekonomi yang siap dicetak untuk pengambil keputusan di Kalurahan.

---

## 3. Data Spasial & Optimasi

- **Batas Resmi Wilayah:** Menggunakan data batas resmi Badan Informasi Geospasial (BIG) dan Pemerintah Kabupaten Sleman 2023 (`layers/boundary.geojson`), melindungi 3.959 KK (98,34%) termasuk 38 KK di bantaran sungai batas utara-barat.
- **Presisi Koordinat 5 Desimal:** Seluruh layer GeoJSON dan koordinat penduduk telah dipotong menjadi presisi 5 angka di belakang koma (~1,1 meter). Hal ini mengurangi beban unduh data browser secara signifikan tanpa mengorbankan akurasi pemetaan.

---

## 4. Struktur Repositori

```
peta_pondokrejo_main/
├── main.go                     # Entry point server Gin & routing
├── analytics.go                # Logika pemrosesan analitik kependudukan
├── bansos_analytics.go         # Logika analitik perlindungan sosial & bansos
├── parser.go                   # Parser berkas Excel data keluarga (KK & ART)
├── editor_storage.go           # Penyimpanan state revisi koordinat & layer editor
├── geo_clip.go                 # Utilitas spasial clipping GeoJSON
├── editor_state.json           # State persistensi pergeseran marker & batas editor
├── residents.json              # Cache data kependudukan teroptimasi 5 desimal
├── PONDOKREJO.geojson          # Berkas batas wilayah kalurahan baku
├── layers/                     # Direktori berkas GeoJSON tematik (23 layer)
│   ├── boundary.geojson        # Batas kalurahan resmi BIG/Sleman 2023
│   ├── pemukiman-area.geojson  # Poligon pemukiman warga
│   ├── sawah-area.geojson      # Poligon area persawahan
│   ├── sungai-line.geojson     # Garis aliran sungai
│   ├── krb_1.geojson           # Kawasan Rawan Bencana I Merapi
│   ├── krb_2.geojson           # Kawasan Rawan Bencana II Merapi
│   ├── krb_3.geojson           # Kawasan Rawan Bencana III Merapi
│   ├── evacuation_route.geojson# Jalur evakuasi bencana
│   └── ...                     # Layer tematik lainnya
├── templates/                  # Template antarmuka web (Go embed)
│   ├── index.html              # Peta sebaran interaktif utama
│   ├── editor.html             # Editor spasial marker & batas wilayah
│   ├── login.html              # Halaman login petugas admin
│   ├── analytics.html          # Dasbor grafik analitik kependudukan
│   ├── bansos.html             # Dasbor perlindungan sosial & verifikasi bansos
│   └── recommendations.html    # Dokumen rekomendasi kebijakan
└── run.sh                      # Skrip manajemen proses produksi (Linux)
```

---

## 5. Menjalankan Aplikasi Secara Lokal

### Prasyarat
- Go 1.22 atau lebih baru.
- Berkas data `1 KK_ART Pondokrejo.xlsx` atau `residents.json`.

### Langkah Menjalankan
```bash
# 1. Unduh dependensi
go mod tidy

# 2. Jalankan aplikasi (port default: 5092 atau dari env PORT)
go run .
```
Buka peramban di: `http://localhost:5092`

---

## 6. Kompilasi & Deployment Produksi (Linux)

Aplikasi dikemas dalam *single static binary* menggunakan fitur `//go:embed` bawaan Go, sehingga template dan aset GeoJSON terbungkus langsung di dalam berkas binary tanpa dependensi eksternal.

### Kompilasi untuk Linux amd64
```bash
# Windows PowerShell:
$env:GOOS="linux"; $env:GOARCH="amd64"; $env:CGO_ENABLED="0"; go build -ldflags="-s -w" -o pondokrejo-app-linux

# Linux / macOS:
GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -ldflags="-s -w" -o pondokrejo-app-linux
```

### Konfigurasi Produksi Nargaroth Server
- **Host Target:** `103.255.133.227:64001`
- **User / Path:** `pondokrejo-peta` di `/home/pondokrejo-peta/htdocs/peta.pondokrejo.id/`
- **Port Layanan:** `5092`
- **Reverse Proxy:** Nginx dengan sertifikat SSL otomatis di [https://peta.pondokrejo.id](https://peta.pondokrejo.id)

Untuk menjalankan ulang di server:
```bash
cd /home/pondokrejo-peta/htdocs/peta.pondokrejo.id
./run.sh
```

---

## 7. Daftar Endpoint API

| Method | Path | Deskripsi |
|---|---|---|
| `GET` | `/` | Antarmuka peta utama interaktif MapLibre GL 2D |
| `GET` | `/login` | Halaman login admin kalurahan |
| `GET` | `/editor` | Antarmuka editor spasial marker & layer |
| `GET` | `/editor/layers` | Daftar layer spasial yang tersimpan di editor |
| `GET` | `/editor/layers/:name` | Mengambil GeoJSON layer editor (`padukuhan`, `rw`, `rt`, `fasilitas`) |
| `POST` | `/editor/save` | Menyimpan perubahan koordinat marker & geometri layer |
| `GET` | `/residents.json` | Data agregat keluarga & anggota keluarga teroptimasi |
| `GET` | `/boundary.geojson` | Berkas GeoJSON batas resmi Kalurahan Pondokrejo |
| `GET` | `/layers/*` | Berkas statis GeoJSON tematik kalurahan |
| `GET` | `/analytics` | Dasbor analitik demografi & kependudukan |
| `GET` | `/bansos` | Dasbor perlindungan sosial & pemetaan bansos |
| `GET` | `/bansos/data` | Endpoint API data statistik bansos |
| `GET` | `/recommendations` | Dokumen laporan rekomendasi hasil analitik |
