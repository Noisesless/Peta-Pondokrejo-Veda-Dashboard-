# Arsitektur Sistem — SIG & Analitik Kalurahan Pondokrejo

Dokumen ini menjelaskan arsitektur teknis, desain sistem, aliran data, dan infrastruktur dari aplikasi Sistem Informasi Geografis (SIG) dan Analitik Kependudukan Kalurahan Pondokrejo.

---

## 1. Ringkasan Eksekutif & Stack Teknologi

| Komponen | Teknologi | Deskripsi |
|---|---|---|
| **Backend Runtime** | Golang 1.26 | Single binary executable dengan zero runtime dependency |
| **Web Framework** | Gin Framework (HTTP Engine) | Routing berkecepatan tinggi, static asset serving, dan REST API |
| **Asset Embedding** | Go `embed.FS` | Seluruh HTML, template, GeoJSON layers, dan gambar di-embed ke binary |
| **Map Engine** | MapLibre GL JS v4.7.1 | WebGL/2D Vector map rendering, GPU-accelerated marker clustering |
| **Basemap Provider** | OpenFreeMap & Esri Satellite | OpenFreeMap (Liberty, Positron, Dark) + Esri World Imagery |
| **Data Engine** | Excelize v2 & In-Memory Struct | Parsing langsung dari data BPS/Dinsos (`1 KK_ART Pondokrejo.xlsx`) |
| **Frontend Styling** | Tailwind CSS + Font Awesome | Antarmuka responsif laptop-first (1366px) dan mobile-friendly |
| **Analitik Visual** | Chart.js | Visualisasi piramida penduduk, distribusi desil, dan tren sosial |
| **Deployment Server** | Linux VPS (Ubuntu/Debian) | Reverse proxy Nginx dengan HTTPS SSL/TLS aktif di port 5092 |

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
                         - Normalisasi 9 Padukuhan
                         - Single-pass Deduplication (2.021 KK)
                         - Deterministic Outlier Correction
                                     |
                                     v
                           [ residents.json ]
                         (Embedded Cache Data)
                                     |
                                     v
        +--------------------------------------------------------+
        |            Golang Backend (pondokrejo-app)             |
        |  - Gin Router (:5092)                                  |
        |  - Editor Storage (editor_state.json)                  |
        |  - Embedded Assets & Layers (embed.FS)                 |
        +---------------------------+----------------------------+
                                    | HTTP / JSON API
                                    v
     +-------------------------------------------------------------+
     |                 Frontend Web Application                    |
     |  - MapLibre GL JS Engine                                    |
     |    * Boundary Layer (Halo Casing #fff + Solid Line #1d4ed8) |
     |    * Padukuhan Layer (Clean Planar Tessellation)            |
     |    * Household Clusters & Points (_id index binding)        |
     |    * Focused Padukuhan Isolation (filter on selection)      |
     |  - Sidebar Interaktif (Veda Analytics & Detail Penduduk)    |
     +-------------------------------------------------------------+
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

### C. Infrastruktur Produksi
- **Web Server:** Nginx 1.24+ menangani terminasi SSL, HTTP/2, dan reverse proxy ke `127.0.0.1:5092`.
- **Process Manager:** `run.sh` dengan proteksi `pkill` per-user dan background execution via `nohup`.
