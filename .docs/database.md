# Model Data & Skema Spasial — SIG Kalurahan Pondokrejo

Dokumen ini menjelaskan struktur data kependudukan, pemetaan atribut sosial ekonomi, dan skema geospasial yang digunakan di Kalurahan Pondokrejo.

---

## 1. Skema Data Kependudukan (`Household` & `Resident`)

Data kependudukan diproses secara in-memory menggunakan struktur data Golang dan diserialisasi ke JSON:

### A. Struktur `Household` (Kepala Keluarga)
| Atribut | Tipe Data | Deskripsi |
|---|---|---|
| `no_kk` | String | Nomor Kartu Keluarga (16 digit) |
| `head_name` | String | Nama Kepala Keluarga |
| `address` | String | Alamat domisili lengkap |
| `dusun` | String | Padukuhan resmi (salah satu dari 9 Padukuhan) |
| `latitude` | Float64 | Koordinat Lintang (Presisi 5 desimal, range ~ -7.676 s/d -7.651) |
| `longitude` | Float64 | Koordinat Bujur (Presisi 5 desimal, range ~ 110.296 s/d 110.318) |
| `welfare_level`| String | Desil Kesejahteraan (1: Sangat Miskin, 2: Miskin, 3: Hampir Miskin, 4+: Mampu) |
| `members` | Array[`Resident`] | Daftar Anggota Rumah Tangga (ART) |
| `is_pkh` | Boolean | Status kepesertaan Program Keluarga Harapan |
| `is_bpnt` | Boolean | Status kepesertaan Bantuan Pangan Non-Tunai |
| `is_blt` | Boolean | Status penerima Bantuan Langsung Tunai |
| `has_toddler` | Boolean | Terdapat balita di dalam rumah tangga |
| `is_elderly_head`| Boolean | Kepala keluarga berusia lanjut (>= 60 tahun) |

### B. Struktur `Resident` (Anggota Keluarga / ART)
| Atribut | Tipe Data | Deskripsi |
|---|---|---|
| `name` | String | Nama lengkap anggota keluarga |
| `nik` | String | Nomor Induk Kependudukan (16 digit) |
| `gender` | String | Jenis kelamin (1: Laki-laki, 2: Perempuan) |
| `age` | String | Usia dalam tahun |
| `education` | String | Jenjang pendidikan |
| `aid_list` | Array[String] | Daftar bantuan yang diterima individu (misal Jamkes, PIP, dll) |
| `kerja_detail` | String | Rincian pekerjaan utama |
| `ush_detail` | String | Rincian usaha mandiri/UMKM yang dijalankan |

---

## 2. Normalisasi 9 Padukuhan Resmi Kalurahan Pondokrejo

Sesuai peraturan kalurahan, Pondokrejo terbagi atas **9 Padukuhan resmi**. Seluruh data kependudukan (2.021 KK) telah dinormalisasi ke 9 entitas ini:

1. **Jlapan** (292 KK) — Centroid: `[110.30131, -7.66259]`
2. **Watupecah** (295 KK) — Centroid: `[110.30146, -7.66725]` (mencakup kampung Balan & Mlesen)
3. **Plotengan** (270 KK) — Centroid: `[110.31029, -7.65922]` (mencakup kampung Badalan)
4. **Ngentak** (247 KK) — Centroid: `[110.31169, -7.65448]`
5. **Glagahombo** (226 KK) — Centroid: `[110.30810, -7.67037]`
6. **Dukuh** (213 KK) — Centroid: `[110.31497, -7.66730]`
7. **Banjarharjo** (185 KK) — Centroid: `[110.30579, -7.66443]`
8. **Jlopo** (164 KK) — Centroid: `[110.30538, -7.65750]`
9. **Karanglo** (129 KK) — Centroid: `[110.31072, -7.66543]`

---

## 3. Skema Topologi Spasial (`layers/padukuhan.geojson`)

Lapisan padukuhan dibangun menggunakan **Clean Planar Tessellation**:
- **0 m² Overlap:** Tidak ada poligon yang saling tumpang tindih antar-padukuhan.
- **0 m² Gap:** Seluruh area di dalam `boundary.geojson` terpartisi habis tanpa rongga kosong.
- **Single Shared Boundaries:** Setiap perbatasan antar tetangga berbagi garis simpul (*vertices*) yang identik.
