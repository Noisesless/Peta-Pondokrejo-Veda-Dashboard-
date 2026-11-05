# APP-CONTEXT — Kalurahan Pondokrejo Geospasial & Analitik

## [APP]
- Name: Peta Sebaran Penduduk & Analitik Kalurahan Pondokrejo
- Slug: peta-pondokrejo
- Domain: https://peta.pondokrejo.id
- Stack: Golang 1.26 (Gin Framework), MapLibre GL JS v4.7.1 (2D Engine), Tailwind CSS, Chart.js
- Local Port: 5092 (env: PORT)
- Production Server: Linux VPS (Port 5092 behind Nginx HTTPS)
- Binary: pondokrejo-app-linux (Go single-binary with //go:embed)

## [STATE]
- Map Engine: MapLibre GL JS v4.7.1 (2D Strict Mode, DragRotate disabled, MaxPitch 0)
- Basemap Provider: OpenFreeMap (Liberty, Positron, Dark) + Esri World Imagery (Satelit with glyphs)
- On-Map Layer Switcher: Top-Right on map with 4 options (Standar, Satelit, Terang, Gelap)
- Boundary Decision: Official BIG / Pemkab Sleman 2023 (layers/boundary.geojson), protecting 3,959 KK (98.34%)
- Boundary Styling: Dual-Tone White Halo Casing (#ffffff, 4.6px) + Line (#1d4ed8, 2.8px) with ensureBoundaryOnTop()
- Padukuhan Standardization: Normalized 4,026 KK into exactly 9 Official Padukuhans (Watupecah, Jlapan, Plotengan, Ngentak, Glagahombo, Dukuh, Banjarharjo, Jlopo, Karanglo) via parser.go
- Padukuhan GeoJSON Layer: Clean Planar Partition (layers/padukuhan.geojson) 100% bebas overlap (0 m²), bebas gap (0 m²), single shared boundary edges tanpa garis ganda/silang, dan sinkron dengan editor_state.json. Di-embed ke single binary dan aktif di MapLibre GL JS.
- Geospasial Filter & Active Layer: Interactive Right Sidebar (Veda) with official boundary highlight, Auto-focus fitBounds, Active Filter Floating Chips, Fontstack Noto Sans Regular (Zero 404), and Synchronized Map Legend
- Precision: 5 decimal places (~1.1m precision across all GeoJSON and residents data)
- Issues Open: 0

## [ROUTES]
- GET  /                     -> Peta Sebaran Interaktif Utama (index.html)
- GET  /login                -> Login Admin (login.html)
- GET  /editor               -> Editor Spasial Marker Penduduk & Batas Wilayah (editor.html)
- GET  /editor/layers        -> Metadata layer editor
- GET  /editor/layers/:name  -> GeoJSON layer editor aktif (padukuhan, rw, rt, fasilitas)
- POST /editor/save          -> Simpan perubahan koordinat marker & layer editor
- GET  /residents.json       -> Data seluruh penduduk/KK teroptimasi
- GET  /boundary.geojson     -> Batas resmi kalurahan
- GET  /layers/*             -> Berkas statis GeoJSON tematik (23 layer)
- GET  /analytics            -> Dashboard Analitik Kependudukan (analytics.html)
- GET  /bansos               -> Dashboard Perlindungan Sosial & Bansos (bansos.html)
- GET  /bansos/data          -> API Data Bansos
- GET  /recommendations      -> Dokumen Rekomendasi Kebijakan (recommendations.html)

## [NEXT]
- Pemeliharaan data KK berkala sesuai pembaruan dari Kalurahan
- Penambahan layer tematik baru jika tersedia data spasial tambahan dari Kapanewon/Pemkab Sleman

