# Model Data & Skema Spasial — SIG Kalurahan Pondokrejo

Dokumen ini menjelaskan struktur data kependudukan, pemetaan atribut sosial ekonomi, dan skema geospasial yang digunakan di Kalurahan Pondokrejo.

---

## 1. Skema Data Kependudukan (`Household` & `Resident`)

Data kependudukan diproses secara in-memory menggunakan struktur data Golang dan diserialisasi ke JSON:

### A. Struktur `Household` (Kepala Keluarga)
| Atribut | Tipe Data | JSON Tag | Deskripsi |
|---|---|---|---|
| `no_kk` | String | `json:"no_kk"` | Nomor Kartu Keluarga (16 digit murni, e.g. "3404141811140007") |
| `head_name` | String | `json:"head_name"` | Nama Kepala Keluarga |
| `address` | String | `json:"address"` | Alamat domisili lengkap KTP |
| `dusun` | String | `json:"dusun"` | Padukuhan resmi (salah satu dari 9 Padukuhan) |
| `rt` | String | `json:"rt"` | Alokasi Rukun Tetangga (2 digit, e.g. "01", "04") |
| `rw` | String | `json:"rw"` | Alokasi Rukun Warga (2 digit, e.g. "01", "15") |
| `latitude` | Float64 | `json:"latitude"` | Koordinat Lintang (Presisi 5 desimal, range ~ -7.676 s/d -7.651) |
| `longitude` | Float64 | `json:"longitude"` | Koordinat Bujur (Presisi 5 desimal, range ~ 110.296 s/d 110.318) |
| `welfare_level`| String | `json:"welfare_level"` | Desil Kesejahteraan (1: Sangat Miskin, 2: Miskin, 3: Hampir Miskin, 4+: Mampu) |
| `members` | Array[`Resident`] | `json:"members"` | Daftar Anggota Rumah Tangga (ART) |
| `is_pkh` | Boolean | `json:"is_pkh"` | Status kepesertaan Program Keluarga Harapan |
| `is_bpnt` | Boolean | `json:"is_bpnt"` | Status kepesertaan Bantuan Pangan Non-Tunai |
| `is_blt` | Boolean | `json:"is_blt"` | Status penerima Bantuan Langsung Tunai |
| `has_toddler` | Boolean | `json:"has_toddler"` | Terdapat balita di dalam rumah tangga |
| `is_elderly_head`| Boolean | `json:"is_elderly_head"` | Kepala keluarga berusia lanjut (>= 60 tahun) |
| `floor_type` | String | `json:"floor_type"` | Kode jenis lantai (1: Keramik/Granit, 2: Semen/Ubin, 3: Tanah) |
| `wall_type` | String | `json:"wall_type"` | Kode jenis dinding (1: Tembok, 2: Kayu/Triplek, 3: Bambu/Gedek) |
| `roof_type` | String | `json:"roof_type"` | Kode jenis atap (1: Genteng beton/keramik, 2: Genteng tanah liat, 3: Seng/Asbes) |
| `water_source` | String | `json:"water_source"` | Kode sumber air bersih (1: Kemasan, 2: Ledeng/PDAM, 3: Sumur bor, 4: Sumur terlindung, 5: Mata air) |
| `sanitation` | String | `json:"sanitation"` | Kode fasilitas sanitasi/jamban (1: Sendiri dengan leher angsa, 2: Bersama, 3: Tidak ada) |

### B. Struktur `Resident` (Anggota Keluarga / ART)
| Atribut | Tipe Data | JSON Tag | Deskripsi |
|---|---|---|---|
| `name` | String | `json:"name"` | Nama lengkap anggota keluarga |
| `nik` | String | `json:"nik"` | Nomor Induk Kependudukan (16 digit murni) |
| `gender` | String | `json:"gender"` | Jenis kelamin ('1': Laki-laki [2.998 jiwa], '2': Perempuan [3.068 jiwa]) |
| `age` | String | `json:"age"` | Usia dalam tahun |
| `education` | String | `json:"education"` | Kode jenjang pendidikan (1: Tidak/Belum Sekolah, 2: SD, 3: SMP, 4: SMA/SMK, 5: Diploma/S1+) |
| `job` | String | `json:"job"` | Kode kategori pekerjaan utama (Petani, Buruh, Swasta, ASN, Pedagang) |
| `aid_list` | Array[String] | `json:"aid_list"` | Daftar bantuan individu (Jamkes, KIP/PIP, PKH, dll) |
| `pregnant` | String | `json:"pregnant"` | Status kehamilan ibu (1: Hamil, 0/kosong: Tidak Hamil) |
| `disability` | String | `json:"disability"` | Kode penyandang disabilitas fisik/mental |
| `relation` | String | `json:"relation"` | Hubungan dalam keluarga (1: Kepala Keluarga, 2: Istri, 3: Anak, 4: Lainnya) |

---

## 2. Pola Resmi Alokasi RT & RW 9 Padukuhan Kalurahan Pondokrejo (SSOT)

Berdasarkan peraturan administrasi Kalurahan Pondokrejo dan hasil normalisasi data konsensus, seluruh 2.021 KK terbagi tepat ke dalam 9 padukuhan dengan alokasi wilayah RW dan RT resmi berikut:

| No | Padukuhan Resmi | Alokasi RW Resmi | Alokasi RT Resmi | Wilayah / Dusun Bagian | Total KK | Total Jiwa |
|---|---|---|---|---|---|---|
| 1 | **Ngentak** | RW 01 – RW 02 | RT 01 – RT 04 | Ngentak | 247 KK | 741 Jiwa |
| 2 | **Plotengan** | RW 03 – RW 04 | RT 01 – RT 07 | Plotengan (RW 03) & Badalan (RW 04) | 270 KK | 851 Jiwa |
| 3 | **Jlopo** | RW 05 – RW 06 | RT 01 – RT 04 | Jlopo | 164 KK | 520 Jiwa |
| 4 | **Karanglo** | RW 07 – RW 08 | RT 01 – RT 04 | Karanglo | 129 KK | 389 Jiwa |
| 5 | **Dukuh** | RW 09 – RW 10 | RT 01 – RT 05 | Dukuh | 213 KK | 674 Jiwa |
| 6 | **Jlapan** | RW 11 – RW 13 | RT 01 – RT 07 | Jlapan | 292 KK | 933 Jiwa |
| 7 | **Banjarharjo** | RW 14 – RW 15 | RT 01 – RT 04 | Banjarharjo | 185 KK | 586 Jiwa |
| 8 | **Glagahombo** | RW 16 – RW 17 | RT 01 – RT 05 | Glagahombo (RW 16) & Cemoro (RW 17) | 226 KK | 711 Jiwa |
| 9 | **Watupecah** | RW 18 – RW 20 | RT 01 – RT 07 | Watupecah (RW 18), Jenengan (RW 19), Mlesan Balan (RW 20) | 295 KK | 948 Jiwa |
| **TOTAL** | **9 Padukuhan** | **RW 01 – RW 20** | **47 Titik RT Resmi** | **Seluruh Kalurahan Pondokrejo** | **2.021 KK** | **6.353 Jiwa** |

---

## 3. Skema Topologi Spasial (`layers/padukuhan.geojson`)

Lapisan batas padukuhan dibangun menggunakan standar **Clean Planar Tessellation**:
- **0 m² Overlap:** Tidak ada poligon yang saling tumpang tindih antar-padukuhan.
- **0 m² Gap:** Seluruh area di dalam `boundary.geojson` terpartisi habis tanpa rongga kosong.
- **Single Shared Boundaries:** Setiap perbatasan antar tetangga berbagi garis simpul (*vertices*) yang identik.
- **Topological Boundary Layers:**
  1. `layer-boundary-casing`: Garis putih tebal (4.6px, opacity 0.95) untuk kontras tinggi di atas satelit/sawah.
  2. `layer-boundary-line`: Garis biru pekat (2.8px, `#1d4ed8`).
  3. `layer-boundary-fill`: Arsiran lembut (5% opacity) penanda wilayah hukum Pondokrejo.
