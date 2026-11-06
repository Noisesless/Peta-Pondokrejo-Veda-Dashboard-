# APP-CONTEXT — Kalurahan Pondokrejo Geospasial & Analitik

## [APP]
- Name: Peta Sebaran Penduduk & Analitik Kalurahan Pondokrejo
- Slug: peta-pondokrejo
- Domain: https://peta.pondokrejo.id
- Stack: Golang 1.22+ (Gin Framework), MapLibre GL JS v4.7.1 (2D Engine), Tailwind CSS, Chart.js
- Local Port: 8080 (env: PORT)
- Production Server: Linux VPS (Reverse proxy Nginx HTTPS, Port 5092)
- Binary: pondokrejo-app-linux (Go single-binary with //go:embed)

## [STATE]
- Security Status: 100% COMPLIANT & VERIFIED (UU PDP No. 27/2022 & Security Patterns SP-001 s/d SP-031)
  * SP-025: 100% dari 6.353 NIK dan 2.021 No KK disamarkan (masked) untuk akses publik non-admin
  * SP-006 & SP-024: Backend middleware RequireAdmin() memproteksi /editor, /editor/layers, dan /editor/save
  * SP-004 & SP-009: Otentikasi server-side POST /api/login dengan HMAC-SHA256 signed session cookie (HttpOnly, Secure)
  * Public Read-Only Layers: GET /editor/layers/:name dibuka untuk publik sehingga batas RW, RT, dan Fasilitas Desa tampil tanpa error 401
- Spatial Harmonization & Cross-Sidebar Coordination:
  * 100% Spatial Clipping Kalurahan: Seluruh 19 layer tematik dipotong presisi tepat di dalam poligon batas Kalurahan Pondokrejo (jalan, pemukiman, sawah, sungai, kontur, 2.399 bangunan, pendidikan, toponimi).
  * Out-of-Bounds Sanitasi: Layer Sleman luar wilayah (0 fitur di Pondokrejo seperti TPS timur, bank sampah, sirene EWS Merapi) dibersihkan dari tampilan utama.
  * Tagging Dusun Geospasial: Seluruh fitur titik, garis, dan poligon tematik diberi atribut properti `dusun` & `dusuns` sesuai 9 padukuhan resmi.
  * Dynamic Padukuhan Isolation: Saat padukuhan dipilih di navbar kanan (misal "Plotengan"), seluruh layer tematik aktif di navbar kiri otomatis difilter ke padukuhan tersebut via `syncThematicLayersWithDusunFilter()`.
  * Non-Destructive Multi-Select Preset: Mode Sederhana di navbar kiri diubah menjadi tombol preset aditif (Default, Lingkungan, Infrastruktur, Mitigasi, Semua) dengan tombol "Reset Layer", bebas dikombinasikan secara acak.
  * WebGL 4-Tier Z-Index Stacking: Hirarki rendering terstruktur (Tier 1: Fills -> Tier 2: Lines -> Tier 3: Points/Residents -> Tier 4: Labels) menjamin tidak ada layer yang tertutup atau tenggelam.
- Map Engine: MapLibre GL JS v4.7.1 (2D Strict Mode, DragRotate disabled, MaxPitch 0)
- Basemap Provider: OpenFreeMap (Liberty, Positron, Dark) + Esri World Imagery (Satelit with glyphs)
- On-Map Layer Switcher: Top-Right on map with 4 options (Standar, Satelit, Terang, Gelap) with bulletproof hover buffer delay (350ms)
- Basemap & Boundary Auto-Restoration: Mutex-guarded reapplyAllLayers() pada MapLibre 'style.load'
- Boundary Decision: Official BIG / Pemkab Sleman 2023 (layers/boundary.geojson), protecting 100% KK (2,021 KK in-boundary)
- Boundary Styling: Dual-Tone White Halo Casing (#ffffff, 4.6px) + Line (#1d4ed8, 2.8px) with ensureBoundaryOnTop()
- Padukuhan Standardization: Normalized to exactly 9 Official Padukuhans with 2,021 unique households (zero outlier, zero leak)
- Official RT & RW Harmonization: 100% dari 2.021 KK dipetakan tepat ke 47 kombinasi alokasi resmi RT & RW 9 padukuhan
- Documentation: Complete 9 standardized files in /.docs/
- Issues Open: 0 (ISSUE-012: Closed - pembersihan duplikasi sintaks JavaScript pada templates/index.html & verifikasi node -c lolos)

## [ROUTES]
- GET  /                     -> Peta Sebaran Interaktif Utama (index.html, adaptif Mode Publik vs Mode Petugas)
- GET  /login                -> Login Admin (login.html, terhubung ke POST /api/login)
- POST /api/login            -> Verifikasi kredensial backend & penerbitan kuki sesi HMAC
- GET  /logout               -> Hapus kuki sesi & redirect ke /login
- POST /api/logout           -> Hapus kuki sesi (JSON API)
- GET  /api/auth/status      -> Cek status autentikasi aktif
- GET  /editor               -> Editor Spasial Marker Penduduk & Batas Wilayah (Protected: RequireAdmin)
- GET  /editor/layers        -> Metadata layer editor (Protected: RequireAdmin)
- GET  /editor/layers/:name  -> GeoJSON layer editor aktif (Public Read-Only)
- POST /editor/save          -> Simpan perubahan koordinat marker & layer editor (Protected: RequireAdmin)
- GET  /residents.json       -> Data kependudukan teroptimasi (Public: Masked PII, Admin: Unmasked)
- GET  /boundary.geojson     -> Batas resmi kalurahan
- GET  /layers/*             -> Berkas statis GeoJSON tematik (terpotong presisi Kalurahan Pondokrejo)
- GET  /analytics            -> Dashboard Analitik Kependudukan (analytics.html)
- GET  /bansos               -> Dashboard Perlindungan Sosial & Bansos (bansos.html)
- GET  /bansos/data          -> API Data Bansos
- GET  /recommendations      -> Dokumen Rekomendasi Kebijakan (recommendations.html)

## [NEXT]
- Sinkronisasi deployment pembaruan spasial dan binary Linux ke server VPS produksi
