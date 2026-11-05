# Pemetaan Rute & Handler — SIG Kalurahan Pondokrejo

Dokumen ini mencatat pemetaan rute HTTP lengkap, metode akses, handler fungsi Golang, dan status proteksi akses pada aplikasi.

---

## Tabel Rute Sistem & Status Proteksi Keamanan

| Method | Path | Handler Backend | Status Proteksi | Deskripsi & Catatan Keamanan |
|---|---|---|---|---|
| `GET` | `/` | `main.func1` | Publik (Client Redirect) | Halaman peta sebaran utama (Catatan: dilindungi redirect client-side JS di browser) |
| `GET` | `/login` | `main.func2` | Publik | Halaman login administrator (Kredensial hardcoded JS) |
| `GET` | `/editor` | `main.func3` | ⚠️ Publik (No Server Auth) | Halaman visual editor marker & batas wilayah (Hanya dilindungi JS sessionStorage) |
| `GET` | `/editor/layers` | `main.func4` | Publik | Endpoint metadata layer spasial yang aktif di editor |
| `GET` | `/editor/layers/:name` | `main.func5` | Publik | Endpoint data GeoJSON spesifik (`padukuhan`, `rw`, `rt`) |
| `POST` | `/editor/save` | `main.func7` | 🔴 Vulnerable (Unauthenticated) | Endpoint penyimpanan revisi titik koordinat & GeoJSON (Siapa saja bisa POST tanpa auth) |
| `GET` | `/residents.json` | `main.func6` | 🔴 Vulnerable (Unmasked PII) | Menyajikan seluruh 2.021 KK dan 6.353 NIK 16-digit tanpa masking ke publik |
| `GET` | `/boundary.geojson` | `main.func8` | Publik | Berkas GeoJSON batas resmi Kalurahan Pondokrejo |
| `GET` | `/layers/*filepath` | `StaticFileHandler` | Publik | Serving statis 23 layer geospasial tematik dari embedded FS |
| `GET` | `/analytics` | `main.func14` | Publik | Dasbor analitik demografi & grafik kependudukan |
| `GET` | `/bansos` | `main.func15` | Publik | Dasbor analisis perlindungan sosial & bansos |
| `GET` | `/bansos/data` | `main.func16` | Publik | API statistik data penerima bantuan sosial |
| `GET` | `/recommendations` | `main.func13` | Publik | Halaman dokumen rekomendasi kebijakan kalurahan |
| `GET` | `/logo.png` | `main.func9` | Publik | Logo resmi Kalurahan Pondokrejo (embedded asset) |
| `GET` | `/veda-logo.png` | `main.func10` | Publik | Logo Visual Economic Data Analytics (VEDA) |
| `GET` | `/clasnet-logo.png` | `main.func11` | Publik | Logo pengembang ClasNet |
| `GET` | `/background.jpg` | `main.func12` | Publik | Foto latar belakang visual Pondokrejo |

---

## Rekomendasi Pengamanan Rute Backend (Action Plan)

1. **Rute Terlindungi (Admin Only):**
   - Rute `GET /editor` dan `POST /editor/save` wajib dibungkus middleware otentikasi Gin (`gin.BasicAuth` atau session cookie bertanda tangan HMAC).
2. **Rute Sanitasi PII (Public Safe):**
   - Rute `GET /residents.json` wajib menerapkan penyaringan (*data masking*): NIK dan No KK disamarkan dengan tanda bintang (`340414******XXXX`) jika diakses oleh pengguna umum non-admin.
3. **Endpoint Login API:**
   - Menyediakan rute `POST /api/login` yang melakukan verifikasi username dan password hash Bcrypt di sisi backend.
