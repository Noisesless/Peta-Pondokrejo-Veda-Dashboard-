# Audit Keamanan & Hardening Server — SIG Kalurahan Pondokrejo

Dokumen ini mencatat evaluasi keamanan aplikasi, sanitasi data, proteksi endpoint, dan konfigurasi server produksi.

---

## 1. Verifikasi Keamanan Aplikasi

| Poin Audit | Status | Evaluasi & Implementasi |
|---|---|---|
| **SQL Injection** | ✅ SECURE | Aplikasi tidak menggunakan SQL database runtime; seluruh data disajikan via in-memory struct dan GeoJSON |
| **Cross-Site Scripting (XSS)** | ✅ SECURE | Sanitasi teks masukan pada popup dan filter pencarian; escaping bawaan Gin HTML renderer |
| **Path Traversal** | ✅ SECURE | Endpoint `/layers/*` dan asset dibatasi hanya melayani direktori statis dan embedded filesystem |
| **Sensitivitas Kredensial** | ✅ SECURE | Tidak ada API key berbayar yang bocor di frontend; basemap menggunakan open source tiles |
| **Eksekusi Skrip Berbahaya** | ✅ SECURE | Blokir berkas `.php` aktif di level Nginx (`location ~* ^/desa/upload/.*\.php$ { deny all; }`) |

---

## 2. Hardening Server Produksi (Nginx Reverse Proxy)

- **Enkripsi Transit (SSL/TLS):** Enkripsi penuh HTTPS dengan sertifikat Let's Encrypt aktif di domain `peta.pondokrejo.id`.
- **HTTP Strict Transport Security & Redirect:** Port 80 otomatis dialihkan permanen (301) ke HTTPS port 443.
- **Isolasi Port Internal:** Aplikasi Go hanya membuka listening port lokal di `127.0.0.1:5092`, tidak terbuka langsung ke internet publik.
- **Proteksi Buffer & Timeout:** Nginx dikonfigurasi dengan buffer teroptimasi (`proxy_buffers 4 256k;`, `proxy_buffer_size 128k;`) untuk menangani payload JSON kependudukan (4.5 MB) secara efisien tanpa I/O bottleneck.
