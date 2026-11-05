# Pemetaan Rute & Handler — SIG Kalurahan Pondokrejo

Dokumen ini mencatat pemetaan rute HTTP lengkap, metode akses, handler fungsi Golang, dan proteksi akses pada aplikasi.

---

## Tabel Rute Sistem

| Method | Path | Handler Backend | Middleware / Proteksi | Deskripsi |
|---|---|---|---|---|
| `GET` | `/` | `main.func1` | Publik | Halaman peta sebaran interaktif utama |
| `GET` | `/login` | `main.func2` | Publik | Halaman login administrator |
| `GET` | `/editor` | `main.func3` | Admin Session | Halaman visual editor marker & batas wilayah |
| `GET` | `/editor/layers` | `main.func4` | Publik / Admin | Endpoint metadata layer spasial yang aktif di editor |
| `GET` | `/editor/layers/:name` | `main.func5` | Publik / Admin | Endpoint data GeoJSON spesifik (`padukuhan`, `rw`, `rt`) |
| `POST` | `/editor/save` | `main.func7` | Admin Session | Endpoint penyimpanan revisi titik koordinat & GeoJSON |
| `GET` | `/residents.json` | `main.func6` | Publik | Data kependudukan terpadu (Excel + State Editor) |
| `GET` | `/boundary.geojson` | `main.func8` | Publik | Berkas GeoJSON batas resmi Kalurahan Pondokrejo |
| `GET` | `/layers/*filepath` | `StaticFileHandler` | Publik | Serving statis 23 layer geospasial tematik |
| `GET` | `/analytics` | `main.func14` | Publik | Dasbor analitik demografi & grafik kependudukan |
| `GET` | `/bansos` | `main.func15` | Publik | Dasbor analisis perlindungan sosial & bansos |
| `GET` | `/bansos/data` | `main.func16` | Publik | API statistik data penerima bantuan sosial |
| `GET` | `/recommendations` | `main.func13` | Publik | Halaman dokumen rekomendasi kebijakan kalurahan |
| `GET` | `/logo.png` | `main.func9` | Publik | Logo resmi Kalurahan Pondokrejo (embedded) |
| `GET` | `/veda-logo.png` | `main.func10` | Publik | Logo Visual Economic Data Analytics (VEDA) |
| `GET` | `/clasnet-logo.png` | `main.func11` | Publik | Logo pengembang ClasNet |
| `GET` | `/background.jpg` | `main.func12` | Publik | Foto latar belakang visual Pondokrejo |
