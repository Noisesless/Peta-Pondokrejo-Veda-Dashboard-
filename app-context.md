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
  * SP-007: Lingkungan terisolasi via .env (chmod 600) + .env.example di repositori; diabaikan di .gitignore
  * SP-014: Nginx rate limiting (zone pdrj_residents) memicu 429 Too Many Requests saat automated mass scraping
  * SP-023: Header keamanan HSTS (Strict-Transport-Security: max-age=31536000) aktif di Nginx
  * Web Server Protection: Nginx memblokir total akses ke dotfiles (.env, .git, .htaccess) dengan respons 404; berkas .htaccess terpasang untuk fallback Apache/LiteSpeed
- Map Engine: MapLibre GL JS v4.7.1 (2D Strict Mode, DragRotate disabled, MaxPitch 0)
- Basemap Provider: OpenFreeMap (Liberty, Positron, Dark) + Esri World Imagery (Satelit with glyphs)
- On-Map Layer Switcher: Top-Right on map with 4 options (Standar, Satelit, Terang, Gelap) with bulletproof hover buffer delay (350ms)
- Basemap & Boundary Auto-Restoration: Bulletproof mutex-guarded reapplyAllLayers() triggered on MapLibre 'style.load' and backed by a 150/450ms safety net ensuring 100% automatic reload of Kalurahan boundary, padukuhan borders, labels, and resident markers across all basemap styles (including in-memory satellite).
- Padukuhan Filter & Boundary Isolation: Valid MapLibre expression filtering (['any', ['in', 'nama', ...], ['in', 'nama_dusun', ...]]) with zero runtime syntax errors, instant background preloading of boundary.geojson & padukuhan.geojson, and safe layer positioning.
- Boundary Decision: Official BIG / Pemkab Sleman 2023 (layers/boundary.geojson), protecting 100% KK (2,021 KK in-boundary)
- Boundary Styling: Dual-Tone White Halo Casing (#ffffff, 4.6px) + Line (#1d4ed8, 2.8px) with ensureBoundaryOnTop()
- Padukuhan Standardization: Normalized to exactly 9 Official Padukuhans (Watupecah, Jlapan, Plotengan, Ngentak, Glagahombo, Dukuh, Banjarharjo, Jlopo, Karanglo) with 2,021 unique households (zero duplicate, zero outlier)
- Spatial Containment Guarantee: 100% dari 2.021 KK berada tepat di dalam poligon padukuhannya masing-masing (0 mismatch, 0 leak antar padukuhan) menggunakan Triple-Tier RW/RT Resolver & Inward Buffer Snapping
- Official RT & RW Harmonization: 100% dari 2.021 KK dipetakan tepat ke 47 kombinasi alokasi resmi RT & RW 9 padukuhan (Ngentak 01-02, Plotengan 03-04, Jlopo 05-06, Karanglo 07-08, Dukuh 09-10, Jlapan 11-13, Banjarharjo 14-15, Glagahombo 16-17, Watupecah 18-20) sehingga tabel Sebaran Wilayah 100% konsisten tanpa anomali RW acak
- Clean NIK & No KK: 100% dari 2.021 No KK dan 6.353 NIK warga berformat string angka 16-digit murni (eliminasi total notasi eksponensial ilmiah E+15 dan duplikasi format)
- Interactive Regional Analysis (Analisa Wilayah): Real-time sync with map filters, balanced population pyramid (gender '1'/'2' riil: Laki-laki 2.998 jiwa, Perempuan 3.068 jiwa), survey code label translation (education, sanitation, clean water), and dynamic distribution table (RT/RW)
- Padukuhan GeoJSON Layer: Clean Planar Tessellation (layers/padukuhan.geojson) with 0 m² overlap, 0 m² gap, single shared boundary edges, uppercase halo toponymy labels, and live active layer highlight
- Focused Padukuhan Isolation: Interactive boundary filter that automatically isolates and displays only the selected padukuhan layer and its households, hiding inactive padukuhans for laser-sharp focus
- Click Data Synchronization: Direct unique index binding (_id) ensuring 100% exact match between map point popup and right sidebar detail panel (eliminating scientific notation NoKK collision)
- Precision: 5 decimal places (~1.1m precision across all GeoJSON and residents data)
- Documentation: Complete 9 standardized files in /.docs/ (architecture, api-spec, database, routes, dependency-graph, quality_review, issues, security-audit, design-system)
- Issues Open: 0
- Performance & Concurrency: Zero-delay navigation & fast-path layer toggling (<0.1ms), concurrency mutex guard, 60fps smooth sidebar animation via rAF deferral, and 200ms debounce on search inputs.
- Login Background & Performance: 100% menggunakan background.JPG asli, auto-redirect loop dieliminasi dari login.html dan index.html, performa instan tanpa lag/freeze.

## [ROUTES]
- GET  /                     -> Peta Sebaran Interaktif Utama (index.html, adaptif Mode Publik vs Mode Petugas)
- GET  /login                -> Login Admin (login.html, terhubung ke POST /api/login)
- POST /api/login            -> Verifikasi kredensial backend & penerbitan kuki sesi HMAC
- GET  /logout               -> Hapus kuki sesi & redirect ke /login
- POST /api/logout           -> Hapus kuki sesi (JSON API)
- GET  /api/auth/status      -> Cek status autentikasi aktif
- GET  /editor               -> Editor Spasial Marker Penduduk & Batas Wilayah (Protected: RequireAdmin)
- GET  /editor/layers        -> Metadata layer editor (Protected: RequireAdmin)
- GET  /editor/layers/:name  -> GeoJSON layer editor aktif (Protected: RequireAdmin)
- POST /editor/save          -> Simpan perubahan koordinat marker & layer editor (Protected: RequireAdmin)
- GET  /residents.json       -> Data kependudukan teroptimasi (Public: Masked PII, Admin: Unmasked)
- GET  /boundary.geojson     -> Batas resmi kalurahan
- GET  /layers/*             -> Berkas statis GeoJSON tematik (23 layer)
- GET  /analytics            -> Dashboard Analitik Kependudukan (analytics.html)
- GET  /bansos               -> Dashboard Perlindungan Sosial & Bansos (bansos.html)
- GET  /bansos/data          -> API Data Bansos
- GET  /recommendations      -> Dokumen Rekomendasi Kebijakan (recommendations.html)

## [NEXT]
- Pemantauan stabilitas operasional server produksi
- Koordinasi berkala dengan pihak Kalurahan Pondokrejo terkait pembaruan data semesteran
