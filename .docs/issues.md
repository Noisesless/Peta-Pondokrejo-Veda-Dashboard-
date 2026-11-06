# Pelacak Isu & Riwayat Bug — SIG Kalurahan Pondokrejo

Dokumen ini mencatat riwayat isu, investigasi akar masalah, perbaikan teknis, dan isu keamanan yang ditemukan di lingkungan pengembangan dan produksi.

---

## Ringkasan Status Isu

| ID Isu | Kategori | Deskripsi Isu | Status | Resolusi / Rekomendasi |
|---|---|---|---|---|
| **ISSUE-001** | Data Parser | Duplikasi data KK di `parser.go` (4.026 KK dari 2.020 KK riil) | CLOSED | Koreksi logika single-pass append setelah proses pemindaian Excel |
| **ISSUE-002** | Geospasial | 44 KK outlier berada jauh di luar batas kalurahan (Mlati/Sleman) | CLOSED | Normalisasi spasial ke centroid padukuhan masing-masing dengan micro-jitter deterministik |
| **ISSUE-003** | Topologi GIS | Poligon padukuhan saling tumpang tindih (Karanglo, Glagahombo, Banjarharjo) | CLOSED | Clean Planar Tessellation menghasilkan 0 m² overlap dan shared edges |
| **ISSUE-004** | UI / Data Sync | Ketidaksesuaian data antara popup titik marker dan panel detail samping | CLOSED | Direct unique index binding (`_id`) menggantikan pencarian berbasis `no_kk` yang berulang |
| **ISSUE-005** | UI / Kontrol | Tombol pemilih layer (basemap switcher) sulit diklik dan menutup sendiri | CLOSED | Menghilangkan celah margin hover dan menambahkan buffer delay 350ms serta click-to-toggle |
| **ISSUE-006** | Engine Peta | Layer batas kalurahan dan data penduduk hilang saat beralih ke Basemap Satelit | CLOSED | Mengganti event `styledata` dengan `map.once('style.load')` untuk style berbasis JS Object |
| **ISSUE-007** | UX / Presentasi | Batas padukuhan lain tetap tampil saat satu padukuhan spesifik dipilih | CLOSED | Mengimplementasikan Focused Padukuhan Boundary Isolation menggunakan ekspresi filter MapLibre |
| **ISSUE-008** | Data / Spasial | Titik KK muncul di luar batas poligon padukuhan saat difilter 1 per 1 | CLOSED | Triple-Tier Resolver (ekstrak RT/RW dari teks alamat KTP) + Inward Buffer Snapping ke poligon padukuhan (0 mismatch) |
| **ISSUE-009** | Frontend / Analitik | Tab Analisa Wilayah: Piramida penduduk rusak (Laki-laki 0), kode survei mentah, dan NIK berformat notasi ilmiah E+15 | CLOSED | Memulihkan NIK & NoKK ke 16-digit murni, mapping kode gender ('1'/'2'), kamus fasilitas/pendidikan, integrasi RT/RW dan filter peta real-time |
| **ISSUE-010** | Data / Wilayah | Tabel Sebaran Wilayah memunculkan RW anomali (misal Banjarharjo muncul RW 01/04, Dukuh muncul RW 00/01) | CLOSED | Normalisasi aturan alokasi resmi RT & RW per padukuhan ke 100% dari 2.021 KK (Banjarharjo 14-15, Dukuh 09-10, dll) |
| **ISSUE-011** | Keamanan / Privasi | Ketiadaan masking NIK/No KK publik (UU PDP), auth bypass `/editor/save`, dan ketiadaan rate limit | CLOSED | Menerapkan 3 tahapan remidiasi: Masking PII pada `/residents.json`, backend session middleware di Gin, dan Nginx rate limiting + HSTS |
| **ISSUE-012** | Frontend / Scripting | Layar peta blank dan panel filter kanan tertahan "Memuat data..." | CLOSED | Pembersihan duplikasi blok sintaks JavaScript di `templates/index.html` yang memicu SyntaxError |

---

## Rincian Teknis Isu

### ISSUE-011: Remidiasi Keamanan Komponen SP & Kepatuhan UU PDP No. 27/2022
- **Akar Masalah:**
  1. Endpoint `/residents.json` menyajikan seluruh NIK 16-digit, No KK, dan data sosial ekonomi warga tanpa penyamaran ke publik internet.
  2. Endpoint `POST /editor/save` dapat dipanggil secara bebas oleh pihak luar tanpa autentikasi server.
  3. Login admin di `templates/login.html` menggunakan verifikasi JavaScript client-side dengan username dan password hardcoded.
  4. Belum ada pembatasan request (*rate limiting*) pada pengunduhan data kependudukan.
- **Solusi yang Diterapkan:**
  1. **Masking PII (SP-025):** Mengimplementasikan fungsi `MaskHouseholds()` yang menyamarkan No KK (`340414******0007`) dan NIK (`340414******0069`) untuk setiap request non-admin. 100% dari 6.353 NIK dan 2.021 No KK terlindungi.
  2. **Server-Side Authentication & Session (SP-004, SP-006, SP-024):**
     - Endpoint `POST /api/login` memvalidasi username dan password di sisi server backend Golang.
     - Diterbitkan cookie terenkripsi HMAC-SHA256 (`pondokrejo_session`) dengan flag `HttpOnly` dan `Secure`.
     - Middleware `RequireAdmin()` dipasang pada `/editor`, `/editor/layers`, dan `/editor/save`. Request tanpa session ditolak dengan kode `401 Unauthorized`.
     - Ketika admin login secara sah, endpoint `/residents.json` menyajikan data lengkap 16 digit unmasked.
  3. **Hardening Nginx VPS (SP-014, SP-023):**
     - Menambahkan zona `limit_req_zone` untuk `/residents.json` (rate=3r/s, burst=5) yang memicu status `429 Too Many Requests` saat terjadi automated mass scraping.
     - Menambahkan header `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload` pada reverse proxy Nginx.
- **Hasil Verifikasi Produksi:**
  - `curl /residents.json` publik: 100% No KK dan NIK tersensor dengan tanda bintang `******`.
  - `curl -X POST /editor/save` publik: `401 Unauthorized`.
  - Akses admin setelah login: `200 OK` dengan NIK/KK lengkap tanpa masking.
  - Scraping massal cepat: Memicu respons `429 Too Many Requests`.

---

### ISSUE-012: Layar Peta Blank & Navbar Kanan Tertahan "Memuat data..." Akibat SyntaxError
- **Akar Masalah:**
  1. Pada `templates/index.html`, fungsi `syncUIWithLayerState()` memuat blok duplikasi quick toggles yang ditutup dengan `});` tanpa pembuka yang sesuai.
  2. Fungsi `ensureBoundaryOnTop()` meninggalkan potongan kode lama di luarnya yang memuat blok `} catch (e) { } }` tersendiri.
  3. Kedua syntax error ini memicu `SyntaxError: Unexpected token ')'` dan `SyntaxError: Unexpected token '}'` pada parser JavaScript browser.
  4. Akibatnya eksekusi seluruh tag `<script>` terhenti seketika: MapLibre tidak diinisialisasi (layar peta blank) dan pemanggilan `fetch('/residents.json')` serta `populateFilters()` tidak pernah berjalan (navbar kanan tertahan di "Memuat data...").
- **Rencana Solusi:**
  1. Bersihkan kedua blok duplikat sintaks yang rusak dari `templates/index.html`.
  2. Lakukan syntax validation via Node.js (`node -c`) untuk memastikan nol error.
  3. Rebuild aplikasi Golang dan restart server.
