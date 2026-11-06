# Sistem Desain UI/UX & Standar Kartografi — SIG Kalurahan Pondokrejo

Dokumen ini mendefinisikan palet warna, tipografi, token desain, geometri kartografis, hierarki visual WebGL, dan standar bilah antarmuka ganda yang digunakan di seluruh aplikasi.

---

## 1. Visual DNA & Palet Warna

Aplikasi mengadopsi gaya **Non-Rounded Administrative Enterprise** yang bersih, fungsional, dan berkontras tinggi:

### A. Skema Warna Utama
- **Primary Brand (Kalurahan Blue):** `#1d4ed8` (Blue 700) — Digunakan untuk batas luar desa, header detail warga, dan aksen aktif.
- **Administrative Emerald (Navbar Kiri):** `#064e3b` (Emerald 900) & `#047857` (Emerald 700) — Identitas resmi pemerintahan Kalurahan Pondokrejo.
- **Analytics Brand (Navbar Kanan):** `#dc2626` (Red 600) & `#0f172a` (Slate 900) — Visual Economic Data Analytics (VEDA).
- **Surface / Background:** `#f8fafc` (Slate 50) & `#ffffff` (White).
- **Text Main:** `#0f172a` (Slate 900) & Text Sub: `#475569` (Slate 600).

### B. Skema Warna Desil Kesejahteraan (SSOT)
- 🔴 **Desil 1 (Sangat Miskin):** `#ef4444` (Red 500)
- 🟠 **Desil 2 (Miskin):** `#f97316` (Orange 500)
- 🟡 **Desil 3 (Hampir Miskin):** `#eab308` (Yellow 500)
- 🟢 **Desil 4+ (Mampu):** `#10b981` (Emerald 500)

---

## 2. Standar Kartografi & Hierarki Garis Peta

### A. Batas Luar Kalurahan (Dual-Tone Halo Casing)
- *Halo Casing (Layer Bawah):* `#ffffff`, tebal `4.6px`, opacity `0.95`.
- *Garis Utama (Layer Atas):* `#1d4ed8`, tebal `2.8px`, solid.
- *Tujuan:* Menjamin batas kalurahan selalu terlihat tajam dan terbaca jelas di atas seluruh jenis basemap (Satelit, Sawah, Pemukiman, Terang, maupun Gelap).

### B. Hierarki Visual Batas Padukuhan Kontekstual
1. **Mode Peta Penuh (Tanpa Filter Padukuhan):**
   - *Garis:* `#2563eb` (Blue 600), tebal `2.0px`, pola solid atau putus-putus halus.
   - *Label Toponimi:* Huruf kapital (*uppercase*), halo putih `2.5px`, font `Noto Sans Regular`.
2. **Mode Fokus Wilayah (Satu Padukuhan Dipilih di Navbar Kanan):**
   - *Padukuhan Terpilih:* `#1d4ed8` (Blue 700), tebal `2.5px`, fill `#2563eb` dengan opacity `0.15`.
   - *8 Padukuhan Sekitar (Context Lines):* `#94a3b8` (Slate 400), tebal `1.2px`, tanpa label toponimi, sehingga tidak menimbulkan polusi visual namun pengguna tetap memiliki orientasi batas spasial desa.

### C. WebGL 4-Tier Z-Index Stacking Hierarchy
- **Tier 1 (Base Fills):** `boundary-fill`, `padukuhan-fill`, `pemukiman-fill`, `sawah-fill`.
- **Tier 2 (Vector Lines):** `jalan-line`, `sungai-line`, `jalur-evakuasi-line`, `rw-line`, `rt-line`.
- **Tier 3 (Thematic Points):** `mitigasi-barak-point`, `fasilitas-point`, `pendidikan-point`, cluster dan marker warga.
- **Tier 4 (Master Boundaries & Labels):** `layer-boundary-casing`, `layer-boundary-line`, `layer-padukuhan-line`, `layer-padukuhan-label`. Terkunci di posisi teratas via `ensureBoundaryOnTop()`.

---

## 3. Komponen Antarmuka & Responsivitas

- **Laptop-First Optimization (1366×768):**
  - Bilah Kiri (Navbar Kiri): Lebar 280px (Mode Sederhana & Mode Detail saklar layer tematik).
  - Bilah Kanan (VEDA Analytics): Lebar 380px (Filter Spasial, Pencarian Penduduk, dan Tab Analisa Wilayah).
  - Area Kanvas Peta: Fleksibel dan responsif memanfaatkan seluruh sisa ruang viewport.
- **Non-Rounded Geometry:** Dropdown, panel detail, legenda floating, dan kartu filter menggunakan radius presisi (`rounded-none` / `rounded-sm`) yang mencerminkan ketegasan sistem informasi pemerintahan.
- **Peta Dasar 4 Mode:** Standar (Liberty), Satelit (Esri), Terang (Positron), dan Gelap (Dark) yang dapat dialihkan secara instan melalui kontrol di pojok kanan atas kanvas.

---

## 4. Standar Desain Laporan Resmi Tata Naskah Dinas (A4)

Laporan rekomendasi kebijakan (`templates/recommendations.html`) menerapkan standar **Tata Naskah Dinas Pemerintah Daerah**:
- **Format Kertas:** Standar ISO A4 (`210mm × 297mm`), margin formal (Kiri 25mm, Kanan 20mm, Atas 22mm, Bawah 20mm).
- **Kop Surat Resmi:** Lambang Kabupaten Sleman di kiri, teks instansi bertingkat tengah (*Pemerintah Kabupaten Sleman - Kapanewon Tempel - Pemerintah Kalurahan Pondokrejo*), alamat lengkap & kontak resmi, logo VEDA di kanan, serta **garis pembatas ganda** (garis tebal 3px + garis tipis 1px).
- **Tipografi Resmi:** Font sans-serif modern (`Plus Jakarta Sans`) untuk ketajaman angka dan tabel, dipadukan dengan font serif formal (`Merriweather`) pada judul laporan.
- **Kartu Metrik Eksekutif (Snapshot):** 4 kotak metrik kompak dengan border halus `#cbd5e1` penanda data kunci.
- **Tabel Resmi Naskah Dinas:** Header abu-abu `#f8fafc` dengan teks kapital, border solid `#334155`, dan baris zebra tipis.
- **Styling Cetak (`@media print`):** Navigasi layar disembunyikan otomatis (`.no-print`), pemutusan halaman diatur ketat via `page-break-after: always` antar-lembar dan `page-break-inside: avoid` pada setiap bab dan tabel sehingga bebas dari pemotongan acak.
- **Pengesahan Resmi:** Format tanda tangan Lurah Kalurahan Pondokrejo: **R. WIDAYATMA, SE**.

