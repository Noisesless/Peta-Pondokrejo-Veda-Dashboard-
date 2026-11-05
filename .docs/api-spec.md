# Spesifikasi API — SIG Kalurahan Pondokrejo

Dokumen ini mendokumentasikan antarmuka pemrograman aplikasi (API) dan spesifikasi endpoint yang disediakan oleh server backend Golang.

---

## 1. Daftar Endpoint Publik

### `GET /`
- **Deskripsi:** Halaman utama Peta Sebaran Penduduk & Analitik Spasial.
- **Content-Type:** `text/html; charset=utf-8`
- **Response:** Template HTML terkompilasi (`templates/index.html`).
- **Catatan Keamanan:** Di browser terdapat pengecekan `sessionStorage` ke `/login`.

### `GET /residents.json`
- **Deskripsi:** Mengambil seluruh data kependudukan (2.021 KK, 6.353 jiwa) yang telah dinormalisasi dan digabungkan dengan state revisi editor.
- **Content-Type:** `application/json`
- **Response Format:** Array of Household Objects:
```json
[
  {
    "no_kk": "3404141811140007",
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
        "nik": "3404147112560069",
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
- **Catatan Keamanan (SP-025):** Saat ini menyajikan data NIK 16 digit dan No KK utuh tanpa masking ke publik internet. Direkomendasikan segera dipasang masking untuk akses non-admin.

### `GET /boundary.geojson`
- **Deskripsi:** Batas resmi Kalurahan Pondokrejo (Badan Informasi Geospasial / Pemkab Sleman 2023).
- **Content-Type:** `application/json`
- **Format:** `GeoJSON FeatureCollection` (Polygon tunggal).

### `GET /layers/:filename`
- **Deskripsi:** Mengambil berkas layer GeoJSON tematik (misal `padukuhan.geojson`, `pemukiman-area.geojson`, `jalan-line.geojson`, dll).
- **Content-Type:** `application/json`

---

## 2. Endpoint Editor Spasial & Administrasi

### `GET /editor`
- **Deskripsi:** Halaman editor penyesuaian titik koordinat dan digitasi batas wilayah.
- **Content-Type:** `text/html; charset=utf-8`
- **Catatan Keamanan:** Belum dilindungi middleware autentikasi server (hanya redirect JavaScript client-side).

### `GET /editor/layers`
- **Deskripsi:** Snapshot seluruh layer editor yang tersimpan di `editor_state.json`.
- **Content-Type:** `application/json`

### `GET /editor/layers/:name`
- **Deskripsi:** Mengambil data GeoJSON layer tertentu di editor (`padukuhan`, `rw`, `rt`).
- **Content-Type:** `application/json`

### `POST /editor/save`
- **Deskripsi:** Menyimpan revisi koordinat marker KK atau pembaruan poligon layer editor.
- **Content-Type:** `application/json`
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
- **Catatan Keamanan (SP-006):** Saat ini menerima POST publik tanpa autentikasi server. Perlu segera dipasang middleware otentikasi.

---

## 3. Endpoint Analitik & Bantuan Sosial

### `GET /analytics`
- **Deskripsi:** Dasbor grafis analitik kependudukan (Piramida penduduk, rasio ketergantungan, demografi).
- **Content-Type:** `text/html; charset=utf-8`

### `GET /bansos`
- **Deskripsi:** Dasbor perlindungan sosial, verifikasi inclusion/exclusion error bantuan sosial.
- **Content-Type:** `text/html; charset=utf-8`

### `GET /bansos/data`
- **Deskripsi:** Ringkasan metrik statistik agregasi bansos dalam format JSON.
- **Content-Type:** `application/json`

### `GET /recommendations`
- **Deskripsi:** Dokumen rekomendasi kebijakan desa berbasis data spasial dan sosial-ekonomi.
- **Content-Type:** `text/html; charset=utf-8`
