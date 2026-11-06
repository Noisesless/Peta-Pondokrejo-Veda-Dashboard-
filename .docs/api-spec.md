# Spesifikasi API — SIG Kalurahan Pondokrejo

Dokumen ini mendokumentasikan seluruh antarmuka pemrograman aplikasi (API), format request/response, dan spesifikasi endpoint yang disediakan oleh server backend Golang aplikasi Sistem Informasi Geografis Kalurahan Pondokrejo.

---

## 1. Daftar Endpoint Publik & Autentikasi

### `GET /`
- **Deskripsi:** Halaman utama Peta Sebaran Penduduk & Analitik Spasial (`templates/index.html`).
- **Content-Type:** `text/html; charset=utf-8`
- **Response:** Template HTML terkompilasi (Go embed).
- **Hak Akses:** Publik (dengan opsi navigasi login administrator).

### `GET /login`
- **Deskripsi:** Halaman login administrator Kalurahan Pondokrejo (`templates/login.html`).
- **Content-Type:** `text/html; charset=utf-8`
- **Response:** Formulir login terproteksi CSRF & visual branding resmi Kalurahan.

### `POST /api/login`
- **Deskripsi:** Endpoint otentikasi kredensial administrator.
- **Content-Type:** `application/json`
- **Request Body:**
```json
{
  "username": "admin",
  "password": "secret_password"
}
```
- **Response `200 OK`:**
```json
{
  "ok": true,
  "message": "Login berhasil."
}
```
- **Kuki Diterbitkan:** `pondokrejo_session` (Signed HMAC-SHA256, `HttpOnly`, `SameSite=Lax`, `Secure`, kedaluwarsa 7 hari).
- **Response `401 Unauthorized`:**
```json
{
  "ok": false,
  "error": "Kredensial tidak valid."
}
```

### `POST /api/logout` / `GET /logout`
- **Deskripsi:** Menghapus kuki sesi administrator dan mengakhiri sesi aktif.
- **Content-Type:** `application/json` (POST) / `302 Found` redirect ke `/login` (GET).
- **Response `200 OK`:**
```json
{
  "ok": true,
  "message": "Sesi telah ditutup."
}
```

### `GET /api/auth/status`
- **Deskripsi:** Memeriksa status autentikasi kuki sesi aktif pengguna.
- **Content-Type:** `application/json`
- **Response:**
```json
{
  "is_authenticated": true,
  "username": "admin"
}
```

---

## 2. Endpoint Data Kependudukan & Geospasial

### `GET /residents.json`
- **Deskripsi:** Mengambil data kependudukan (2.021 KK, 6.353 jiwa) yang dinormalisasi dan digabungkan dengan state revisi editor.
- **Content-Type:** `application/json`
- **Perlindungan Data Pribadi (UU PDP No. 27/2022 & SP-025):**
  - **Akses Publik (Non-Admin):** NIK dan No KK disamarkan (*masked*) dengan format `340414******0007`, atribut medis sensitif dikosongkan.
  - **Akses Administrator:** Disajikan utuh 16 digit murni untuk kebutuhan verifikasi resmi desa.
- **Response Format:** Array of Household Objects:
```json
[
  {
    "no_kk": "340414******0007",
    "head_name": "BIDAYAH",
    "address": "NGENTAK 001/001 PONDOKREJO TEMPEL",
    "dusun": "Ngentak",
    "rt": "01",
    "rw": "01",
    "latitude": -7.65350,
    "longitude": 110.31193,
    "welfare_level": "4",
    "members": [
      {
        "name": "BIDAYAH",
        "nik": "340414******0069",
        "gender": "2",
        "age": "57",
        "education": "1",
        "job": "",
        "aid_list": ["BLT", "Jamkes"]
      }
    ],
    "is_pkh": false,
    "is_bpnt": false,
    "is_blt": true,
    "has_toddler": false,
    "is_elderly_head": false,
    "floor_type": "2",
    "wall_type": "1",
    "roof_type": "2",
    "water_source": "4",
    "sanitation": "1"
  }
]
```
- **Anti-Scraping Rate Limit:** Nginx menerapkan `limit_req_zone` (rate=3r/s burst=5) yang memicu status `429 Too Many Requests` saat terjadi pembacaan massal tak wajar.

### `GET /boundary.geojson`
- **Deskripsi:** Batas resmi Kalurahan Pondokrejo (Badan Informasi Geospasial / Pemkab Sleman 2023).
- **Content-Type:** `application/json`
- **Format:** `GeoJSON FeatureCollection` (Single boundary Polygon).

### `GET /layers/:filename`
- **Deskripsi:** Mengambil 19 berkas GeoJSON tematik yang telah terpotong rapi (*spatially clipped*) sesuai batas Kalurahan Pondokrejo (`layers/padukuhan.geojson`, `layers/pemukiman-area.geojson`, `layers/jalan-line.geojson`, dll).
- **Content-Type:** `application/json`

---

## 3. Endpoint Editor Spasial & Administrasi

### `GET /editor`
- **Deskripsi:** Halaman web visual editor penyesuaian titik koordinat dan digitasi batas wilayah (`templates/editor.html`).
- **Content-Type:** `text/html; charset=utf-8`
- **Status Proteksi:** 🔒 `RequireAdmin()` (Redirect `302 Found` ke `/login?redirect=/editor` jika belum login).

### `GET /editor/layers`
- **Deskripsi:** Snapshot seluruh metadata layer editor yang tersimpan di `editor_state.json`.
- **Content-Type:** `application/json`
- **Status Proteksi:** 🔒 `RequireAdmin()`

### `GET /editor/layers/:name`
- **Deskripsi:** Menyajikan data GeoJSON layer aktif (`padukuhan`, `rw`, `rt`, `fasilitas`).
- **Content-Type:** `application/json`
- **Status Proteksi:** 🌐 `Public Read-Only` (Dapat diakses oleh peta publik tanpa login).

### `POST /editor/save`
- **Deskripsi:** Menyimpan revisi koordinat marker KK atau pembaruan poligon layer editor.
- **Content-Type:** `application/json`
- **Status Proteksi:** 🔒 `RequireAdmin()` (Menolak akses non-admin dengan `401 Unauthorized`).
- **Request Body:**
```json
{
  "household_coords": {
    "3404141811140007": { "lat": -7.65412, "lng": 110.31205 }
  },
  "geo_layers": {
    "padukuhan": { "type": "FeatureCollection", "features": [...] }
  }
}
```
- **Response:** `200 OK` dengan format `{ "ok": true }`.

---

## 4. Endpoint Analitik & Bantuan Sosial

### `GET /analytics`
- **Deskripsi:** Dasbor grafis analitik kependudukan makro (Piramida penduduk, rasio ketergantungan, demografi).
- **Content-Type:** `text/html; charset=utf-8`
- **Status Proteksi:** 🔒 `RequireAdmin()`

### `GET /bansos`
- **Deskripsi:** Dasbor perlindungan sosial, verifikasi inclusion/exclusion error bantuan sosial.
- **Content-Type:** `text/html; charset=utf-8`
- **Status Proteksi:** 🔒 `RequireAdmin()`

### `GET /bansos/data`
- **Deskripsi:** Ringkasan metrik statistik agregasi bansos dalam format JSON.
- **Content-Type:** `application/json`
- **Status Proteksi:** 🔒 `RequireAdmin()`

### `GET /recommendations`
- **Deskripsi:** Dokumen rekomendasi kebijakan desa berbasis data spasial dan sosial-ekonomi siap cetak.
- **Content-Type:** `text/html; charset=utf-8`
- **Status Proteksi:** 🔒 `RequireAdmin()`
