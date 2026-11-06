# Graf Ketergantungan & Dependensi — SIG Kalurahan Pondokrejo

Dokumen ini mendokumentasikan seluruh pustaka (*libraries*), dependensi Go module, berkas aset ter-embed (*embedded assets*), pustaka antarmuka frontend, dan layanan pihak ketiga yang digunakan.

---

## 1. Dependensi Backend (Golang Modules)

Didefinisikan dalam `go.mod`:

| Modul | Versi | Tujuan / Fungsi |
|---|---|---|
| `github.com/gin-gonic/gin` | v1.9.1+ | Framework HTTP server performa tinggi, routing, static serving |
| `github.com/xuri/excelize/v2` | v2.8.0+ | Library pembaca dan parser berkas spreadsheet Excel `.xlsx` |
| `golang.org/x/crypto` | Terkini | Keamanan kriptografi dan hashing kredensial |
| `golang.org/x/net` | Terkini | Ekstensi jaringan standar Golang |
| `golang.org/x/sys` | Terkini | Panggilan sistem operasi level rendah |
| `golang.org/x/text` | Terkini | Pengolahan teks dan encoding karakter |

---

## 2. Berkas Ter-Embed & Target Build Binary

Semua aset frontend, template, dan lapisan geospasial di-embed langsung ke dalam binary Go (`//go:embed`):

| Direktori / File Embed | Target File | Fungsi |
|---|---|---|
| `templates/*` | `index.html`, `editor.html`, `login.html`, dll | Template HTML antarmuka pengguna |
| `layers/*` | 19 Berkas GeoJSON Terpotong Batas | Lapisan spasial resmi kalurahan |
| `residents.json` | Embedded Data Cache | Basis data 2.021 KK teroptimasi |
| `*.png`, `*.jpg` | Logo Kalurahan, VEDA, ClasNet, background | Aset grafis statis |

### Target Kompilasi
- **Linux amd64:** `pondokrejo-app-linux` (Deploy target untuk VPS Ubuntu/Debian)
- **Windows amd64:** `pondokrejo-app.exe` (Local development & demonstration)

---

## 3. Dependensi Frontend (Client-side CDN Libraries)

Dimuat via CDN andal pada template HTML:

| Pustaka | Versi | Integrasi / Fungsi |
|---|---|---|
| **MapLibre GL JS** | v4.7.1 | Engine peta vektor 2D, clustering GPU, dan penanganan event klik |
| **Tailwind CSS** | v3.x | Styling utility-first, sistem grid responsif, non-rounded flat UI |
| **Chart.js** | v4.x | Render grafik piramida penduduk, bar chart desil, dan distribusi sosial |
| **Font Awesome** | v6.x | Ikonografi antarmuka admin, filter, dan tombol kontrol |
| **Noto Sans Regular** | PBF Font | Fontstack bebas error 404 untuk label cluster & toponimi MapLibre |

---

## 4. Layanan Peta Eksternal (Basemap & Tiles)

| Provider | URL Endpoint | Format | Keterangan |
|---|---|---|---|
| **OpenFreeMap Liberty** | `https://tiles.openfreemap.org/styles/liberty` | Vector Tiles | Bebas API key, bebas batas kuota |
| **OpenFreeMap Positron** | `https://tiles.openfreemap.org/styles/positron` | Vector Tiles | Gaya minimalis terang |
| **OpenFreeMap Dark** | `https://tiles.openfreemap.org/styles/dark` | Vector Tiles | Gaya kontras gelap |
| **Esri World Imagery** | `https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}` | Raster Tile (256px) | Foto udara satelit resolusi tinggi |
| **OpenFreeMap Glyphs** | `https://tiles.openfreemap.org/fonts/{fontstack}/{range}.pbf` | PBF Glyphs | Sumber glyphs font untuk rendering teks MapLibre |
