# Arsitektur Sistem — SIG & Analitik Kalurahan Pondokrejo

Dokumen ini menjelaskan arsitektur teknis, desain sistem, aliran data, dan infrastruktur dari aplikasi Sistem Informasi Geografis (SIG) dan Analitik Kependudukan Kalurahan Pondokrejo.

---

## 1. Ringkasan Eksekutif & Stack Teknologi

| Komponen | Teknologi | Deskripsi |
|---|---|---|
| **Backend Runtime** | Golang 1.22+ | Single binary executable dengan zero runtime dependency |
| **Web Framework** | Gin Framework (HTTP Engine) | Routing berkecepatan tinggi, static asset serving, dan REST API |
| **Asset Embedding** | Go `embed.FS` | Seluruh HTML, template, GeoJSON layers, dan gambar di-embed ke binary |
| **Map Engine** | MapLibre GL JS v4.7.1 | WebGL/2D Vector map rendering, GPU-accelerated marker clustering |
| **Basemap Provider** | OpenFreeMap & Esri Satellite | OpenFreeMap (Liberty, Positron, Dark) + Esri World Imagery |
| **Data Engine** | Excelize v2 & In-Memory Struct | Parsing langsung dari data BPS/Dinsos (`1 KK_ART Pondokrejo.xlsx`) |
| **Frontend Styling** | Tailwind CSS + Font Awesome | Antarmuka responsif laptop-first (1366px) dan mobile-friendly |
| **Analitik Visual** | Chart.js | Visualisasi piramida penduduk, distribusi desil, dan tren sosial |
| **Deployment Server** | Linux VPS (Ubuntu/Debian) | Reverse proxy Nginx dengan terminasi HTTPS SSL/TLS |

---

## 2. Diagram Aliran Data & Arsitektur

```
                      +-----------------------------+
                      |  1 KK_ART Pondokrejo.xlsx   |
                      |   (Sumber Data Mentah BPS)  |
                      +--------------+--------------+
                                     |
                                     v
                        [ parser.go: ParseExcel() ]
                         - Normalisasi 9 Padukuhan & 47 RT Resmi
                         - Single-pass Deduplication (2.021 KK)
                         - Pemulihan NIK & No KK 16-Digit Murni
                         - Spatial Inward Snapping ke Poligon
                                     |
                                     v
                            [ residents.json ]
                         (Embedded Cache Data)
                                     |
                                     v
        +--------------------------------------------------------+
        |            Golang Backend (pondokrejo-app)             |
        |  - Gin Router                                          |
        |  - Editor Storage (editor_state.json)                  |
        |  - Embedded Assets & Layers (embed.FS)                 |
        +---------------------------+----------------------------+
                                    | HTTP / JSON API
                                    v
     +--------------------------------------------------------------+
     |                 Frontend Web Application                     |
     |  - MapLibre GL JS Engine (2D Strict Mode)                    |
     |    * Boundary Layer (Halo Casing #fff + Solid Line #1d4ed8)  |
     |    * Padukuhan Layer (Clean Planar Tessellation)             |
     |    * Household Clusters & Points (_id index binding)         |
     |    * Focused Padukuhan Isolation (filter on selection)       |
     |  - Sidebar Interaktif (Dua Tab Utama):                       |
     |    1. Peta Sebaran (Filter Tematik, Legenda, Detail Warga)   |
     |    2. Analisa Wilayah (Piramida Demografi, Kamus Label,      |
     |       Indikator Ketergantungan, Tabel Sebaran RT & RW)       |
     +--------------------------------------------------------------+
```

---

## 3. Komponen Utama

### A. Geospasial Engine (MapLibre GL JS 2D)
- **Strict 2D Mode:** `dragRotate: false`, `maxPitch: 0`, orientasi paten ke utara kartografis.
- **Topological Boundary Layers:**
  1. `layer-boundary-casing`: Garis putih tebal (4.6px, opacity 0.95) untuk kontras tinggi di atas satelit/sawah.
  2. `layer-boundary-line`: Garis biru pekat (2.8px, `#1d4ed8`).
  3. `layer-boundary-fill`: Arsiran lembut (5% opacity) penanda wilayah hukum Pondokrejo.
- **Clean Planar Tessellation Padukuhan:** 9 poligon padukuhan resmi dengan shared edges (0 overlap, 0 gap).
- **Cluster & Heatmap Layer:** Penanganan ribuan titik marker keluarga dengan transisi zoom otomatis.

### B. State Management & Binding
- **Direct Unique Index Binding (`_id`):** Setiap KK di-inject integer unik yang memetakan titik di peta langsung ke objek data array $O(1)$. Mengeliminasi salah data akibat duplikasi nomor KK berbasis scientific notation.
- **Focused Padukuhan Isolation:** Saat satu padukuhan dipilih, sistem menerapkan `setFilter` pada layer garis dan label padukuhan sehingga wilayah lain otomatis diredam demi fokus analitik yang tajam.
- **Real-Time Regional Analytics Sync:** Tab Analisa Wilayah mendengarkan state filter peta secara instan, menghitung ulang distribusi demografi dan tabel alokasi RT/RW tanpa perlu request baru ke backend.

### C. Infrastruktur & Keamanan Produksi
- **Web Server:** Nginx menangani terminasi SSL Let's Encrypt, HTTP/2, dan reverse proxy ke port internal aplikasi Golang.
- **Isolasi Proses:** Aplikasi Go berjalan di bawah akun pengguna terisolasi dengan akses terbatas ke direktori aplikasi.
- **Rencana Hardening Mendatang:** Pemasangan rate limiting Nginx, otentikasi session server-side untuk editor, dan masking PII kependudukan publik sesuai UU PDP No. 27/2022.
