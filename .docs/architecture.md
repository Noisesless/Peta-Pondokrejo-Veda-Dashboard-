# Arsitektur Sistem — SIG & Analitik Kalurahan Pondokrejo

Dokumen ini menjelaskan arsitektur teknis, desain sistem, aliran data, model perlapisan WebGL, dan infrastruktur dari aplikasi Sistem Informasi Geografis (SIG) dan Analitik Kependudukan Kalurahan Pondokrejo.

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
| **Security Layer** | HMAC-SHA256 & Nginx WAF | Session signing, role middleware, rate-limiting, dan UU PDP PII masking |

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
        |  - Gin Router & Session Middleware (RequireAdmin)      |
        |  - Dynamic PII Masking Engine (UU PDP No. 27/2022)     |
        |  - Editor Storage (editor_state.json)                  |
        |  - 19 Spatially-Clipped GeoJSON Layers (embed.FS)      |
        +---------------------------+----------------------------+
                                    | HTTP / JSON API
                                    v
     +--------------------------------------------------------------+
     |                 Frontend Web Application                     |
     |  - MapLibre GL JS Engine (2D Strict Mode)                    |
     |    * WebGL 4-Tier Z-Index Stacking (ensureBoundaryOnTop)     |
     |    * Clean Planar Tessellation Padukuhan (0 Overlap, 0 Gap)  |
     |    * Dual-Sidebar Spatial Harmonization:                     |
     |        - Bilah Navigasi Kiri: Pengontrol Visibilitas Layer   |
     |        - Bilah Navigasi Kanan: Filter Wilayah & Analitik     |
     |    * Household Clusters & Points (_id index binding)         |
     |  - Tab Interaktif:                                           |
     |    1. Peta Sebaran (Filter Tematik, Legenda, Detail Warga)   |
     |    2. Analisa Wilayah (Piramida Demografi, Kamus Label,      |
     |       Indikator Ketergantungan, Tabel Sebaran RT & RW)       |
     +--------------------------------------------------------------+
```

---

## 3. Komponen Arsitektur Utama

### A. Geospasial Engine & WebGL 4-Tier Z-Index Stacking
Untuk menjamin kerapian kartografis dan mencegah poligon area (seperti sawah atau pemukiman) menimpa batas administratif resmi desa, MapLibre GL JS menerapkan model **4-Tier Z-Index Stacking Hierarchy**:

1. **Tier 1 — Base Fills & Polygons:**
   - Layer: `layer-boundary-fill`, `padukuhan-fill`, `pemukiman-fill`, `sawah-fill`, `sungai-fill`.
   - Karakteristik: Fill warna lembut dengan opacity 5%–35% untuk penanda kawasan tanpa mengaburkan citra satelit atau jalan.
2. **Tier 2 — Vector Lines & Infrastructure Networks:**
   - Layer: `jalan-line`, `jalur-evakuasi-line`, `sungai-line`, `kontur-line`, `rw-line`, `rt-line`.
   - Karakteristik: Garis vektor jalan lokal, kolektor, dan jalur evakuasi bencana.
3. **Tier 3 — Thematic Points & Markers:**
   - Layer: `mitigasi-barak-point`, `fasilitas-point`, `pendidikan-point`, `titik-kumpul-point`, `cluster-points`, `unclustered-points`.
   - Karakteristik: Titik sebaran warga desil 1-4+, fasilitas desa, dan titik evakuasi berbobot visual tinggi.
4. **Tier 4 — Master Boundaries & Toponimi (Protected Topmost Tier):**
   - Layer: `layer-boundary-casing` (garis putih 4.6px), `layer-boundary-line` (garis biru solid `#1d4ed8` 2.8px), `layer-padukuhan-line`, dan `layer-padukuhan-label`.
   - Penegakan: Fungsi `ensureBoundaryOnTop()` mengunci layer ini pada urutan paling atas WebGL canvas setiap kali layer baru dimuat atau gaya basemap berganti.

### B. Dual-Sidebar Spatial Harmonization (Harmonisasi Bilah Ganda)
Sistem memisahkan tugas kedua bilah antarmuka secara tegas guna mencegah benturan filter visual:

- **Bilah Navigasi Kiri (Saklar Layer — *What to See*):**
  - Mengontrol visibilitas kategori layer tematik (Peta Standar, Tata Ruang & Pemukiman, Infrastruktur, Mitigasi Bencana).
  - Saklar Cepat ON/OFF: Batas Padukuhan, Batas RW/RT, Pemukiman, Jaringan Jalan, Persebaran Warga, Mitigasi.
- **Bilah Navigasi Kanan (Filter Wilayah & Analitik — *Where to Focus*):**
  - Mengontrol fokus batas kewilayahan (Pilihan 9 Padukuhan resmi) dan atribut kependudukan (Pencarian Nama/NIK, Desil Kesejahteraan, Kategori Bansos).
- **Protokol Harmonisasi Spasial:**
  - **Kondisi Tanpa Padukuhan Dipilih:** Seluruh 9 padukuhan ditampilkan dengan batas biru resmi (`#2563eb`, 2.0px) beserta label nama padukuhan.
  - **Kondisi 1 Padukuhan Dipilih (misal: Dukuh):**
    - Padukuhan terpilih di-highlight dengan garis tebal berbobot tinggi (`#1d4ed8`, 2.5px solid) dan arsiran warna (`fill-opacity: 0.15`).
    - 8 padukuhan lainnya tidak dimatikan secara destruktif, melainkan beralih menjadi garis kontur konteks yang halus (*subtle context line*: `#94a3b8`, 1.2px) tanpa label, sehingga pengguna tetap memiliki orientasi batas wilayah sekitarnya.
    - Layer tematik (jalan, pemukiman, fasilitas, mitigasi) otomatis tersaring (*dynamically clipped/filtered*) hanya pada padukuhan tersebut melalui evaluasi atribut `dusun == selectedPadukuhan || dusuns.includes(selectedPadukuhan)`.

### C. Pre-Clipped GeoJSON Pipeline (Pemotongan Batas Resmi)
Seluruh 19 berkas layer geospasial tematik (`layers/*`) telah dipotong presisi (*spatially clipped*) tepat di batas resmi Kalurahan Pondokrejo (BIG & Pemkab Sleman 2023) menggunakan operasi *geometric intersection* GDAL/Shapely. Ini menjamin:
- Nol poligon pemukiman atau sawah yang merembet ke kalurahan tetangga (Lumbungrejo, Somokaton, Tambakrejo, Margorejo, Ngluwar).
- Performa muat vektor instan karena data yang dikirim ke browser murni hanya data dalam yurisdiksi desa.

### D. Arsitektur Keamanan & Kepatuhan UU PDP No. 27/2022
- **Dynamic PII Masking Engine:** Mengamankan 100% data 6.353 NIK dan 2.021 No KK publik via fungsi `MaskHouseholds()` Golang. Data identitas disamarkan menjadi `340414******0007`. Akses unmasked hanya diberikan setelah validasi otentikasi kuki admin.
- **HMAC-SHA256 Session Middleware:** Endpoint mutasi koordinat `POST /editor/save` dan halaman editor `GET /editor` dilindungi middleware `RequireAdmin()` yang memverifikasi tanda tangan kriptografis kuki sesi server-side.
- **Reverse Proxy Nginx Hardening:** Rate limiting `limit_req_zone` (rate=3r/s, burst=5) memblokir upaya automated scraping publik dengan respons `429 Too Many Requests`. Header keamanan HSTS, X-Frame-Options, dan X-Content-Type-Options aktif penuh.
