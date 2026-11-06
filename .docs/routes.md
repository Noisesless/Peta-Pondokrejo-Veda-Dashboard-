# Pemetaan Rute & Handler — SIG Kalurahan Pondokrejo

Dokumen ini mencatat pemetaan rute HTTP lengkap, metode akses, handler fungsi Golang, dan status proteksi akses pada aplikasi Sistem Informasi Geografis Kalurahan Pondokrejo.

---

## 1. Tabel Rute Sistem & Status Proteksi Keamanan

| Method | Path | Handler Backend | Status Proteksi | Deskripsi & Hak Akses |
|---|---|---|---|---|
| `GET` | `/` | `main.func1` | 🔒 RequireAdmin | Halaman peta sebaran utama (`templates/index.html`). Memerlukan kuki sesi admin valid. |
| `GET` | `/login` | `main.func2` | 🌐 Publik | Halaman login administrator (`templates/login.html`). Otomatis redirect ke `/` jika sudah login. |
| `POST` | `/api/login` | `main.func3` | 🌐 Publik | Endpoint otentikasi kredensial administrator. Menerbitkan kuki sesi `pondokrejo_session` (Signed HMAC-SHA256, HttpOnly, Secure). |
| `GET` | `/logout` | `main.func4` | 🔒 Authenticated | Menghapus kuki sesi admin dan mengarahkan kembali ke `/login`. |
| `POST` | `/api/logout` | `main.func5` | 🔒 Authenticated | Menghapus kuki sesi admin via API JSON (`{"ok": true}`). |
| `GET` | `/api/auth/status` | `main.func6` | 🌐 Publik | Memeriksa status autentikasi kuki sesi aktif (`{"is_authenticated": bool, "username": string}`). |
| `GET` | `/editor` | `main.func7` | 🔒 RequireAdmin | Halaman visual editor koordinat marker KK & batas wilayah (`templates/editor.html`). |
| `GET` | `/editor/layers` | `main.func8` | 🔒 RequireAdmin | Metadata seluruh layer editor aktif yang tersimpan di `editor_state.json`. |
| `GET` | `/editor/layers/:name` | `main.func9` | 🌐 Public Read-Only | Menyajikan GeoJSON layer editor aktif (`rw`, `rt`, `fasilitas`) untuk publik tanpa autentikasi. |
| `POST` | `/editor/save` | `main.func10` | 🔒 RequireAdmin | Endpoint mutasi koordinat KK dan geometri layer editor. Menolak akses non-admin dengan `401 Unauthorized`. |
| `GET` | `/residents.json` | `main.func11` | 🔒 RequireAdmin / Masked | Data kependudukan 2.021 KK. Disajikan lengkap 16-digit untuk Admin; tersensor `******` (UU PDP) jika publik. |
| `GET` | `/boundary.geojson` | `main.func12` | 🌐 Publik | Berkas GeoJSON batas resmi Kalurahan Pondokrejo (BIG / Sleman 2023). |
| `GET` | `/layers/*filepath` | `StaticFS` | 🌐 Publik | Serving statis 19 berkas GeoJSON tematik terpotong batas kalurahan (`//go:embed layers/*`). |
| `GET` | `/analytics` | `main.func20` | 🔒 RequireAdmin | Dasbor analitik kependudukan makro, piramida penduduk, dan indikator sosial (`analytics.html`). |
| `GET` | `/bansos` | `main.func21` | 🔒 RequireAdmin | Dasbor analitik perlindungan sosial dan inclusion/exclusion error bansos (`bansos.html`). |
| `GET` | `/bansos/data` | `main.func22` | 🔒 RequireAdmin | API agregasi statistik data penerima bantuan sosial. |
| `GET` | `/recommendations` | `main.func19` | 🔒 RequireAdmin | Halaman dokumen rekomendasi kebijakan kependudukan berbasis data spasial (`recommendations.html`). |
| `GET` | `/logo.png` | `main.func13` | 🌐 Publik | Logo resmi Kalurahan Pondokrejo (embedded asset). |
| `GET` | `/veda-logo.png` | `main.func14` | 🌐 Publik | Logo Visual Economic Data Analytics (VEDA). |
| `GET` | `/clasnet-logo.png` | `main.func15` | 🌐 Publik | Logo pengembang ClasNet. |
| `GET` | `/background.jpg` | `main.func16` | 🌐 Publik | Foto latar belakang visual Pondokrejo (JPEG). |
| `GET` | `/background.JPG` | `main.func17` | 🌐 Publik | Fallback foto latar belakang huruf kapital. |
| `GET` | `/login.jpg` | `main.func18` | 🌐 Publik | Foto kartu login administrator. |

---

## 2. Arsitektur Keamanan & Middleware

1. **Middleware `RequireAdmin()`:**
   - Memvalidasi keberadaan kuki sesi `pondokrejo_session`.
   - Melakukan verifikasi kriptografis tanda tangan digital HMAC-SHA256 menggunakan secret server (`SESSION_SECRET`).
   - Jika kuki tidak ada atau tidak valid:
     - Untuk request HTML: Mengalihkan pengguna ke `/login?redirect=[path]`.
     - Untuk request API/JSON: Mengembalikan status `401 Unauthorized` dengan pesan error terstandarisasi.
2. **Public Read-Only Layer Serving:**
   - Endpoint `GET /editor/layers/:name` dibuka untuk umum (`Public Read-Only`) sehingga data batas RW, RT, dan Fasilitas Desa dapat ditampilkan pada dasbor peta tanpa menuntut login.
   - Endpoint mutasi `POST /editor/save` tetap terkunci ketat di bawah proteksi `RequireAdmin()`.
3. **Hardening Reverse Proxy Nginx VPS:**
   - Rate limiting `limit_req_zone` (rate=3r/s burst=5) memicu status `429 Too Many Requests` saat terjadi scraping otomatis massal.
   - Header keamanan HSTS (`Strict-Transport-Security: max-age=31536000`), `X-Frame-Options: SAMEORIGIN`, dan `X-Content-Type-Options: nosniff` aktif penuh.
