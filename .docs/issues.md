# Pelacak Isu & Riwayat Bug — SIG Kalurahan Pondokrejo

Dokumen ini mencatat riwayat isu, investigasi akar masalah, dan perbaikan teknis yang telah diterapkan di lingkungan pengembangan dan produksi.

---

## Ringkasan Status Isu

| ID Isu | Kategori | Deskripsi Isu | Status | Resolusi |
|---|---|---|---|---|
| **ISSUE-001** | Data Parser | Duplikasi data KK di `parser.go` (4.026 KK dari 2.020 KK riil) | CLOSED | Koreksi logika single-pass append setelah proses pemindaian Excel |
| **ISSUE-002** | Geospasial | 44 KK outlier berada jauh di luar batas kalurahan (Mlati/Sleman) | CLOSED | Normalisasi spasial ke centroid padukuhan masing-masing dengan micro-jitter deterministik |
| **ISSUE-003** | Topologi GIS | Poligon padukuhan saling tumpang tindih (Karanglo, Glagahombo, Banjarharjo) | CLOSED | Clean Planar Tessellation menghasilkan 0 m² overlap dan shared edges |
| **ISSUE-004** | UI / Data Sync | Ketidaksesuaian data antara popup titik marker dan panel detail samping | CLOSED | Direct unique index binding (`_id`) menggantikan pencarian berbasis `no_kk` yang berulang |
| **ISSUE-005** | UI / Kontrol | Tombol pemilih layer (basemap switcher) sulit diklik dan menutup sendiri | CLOSED | Menghilangkan celah margin hover dan menambahkan buffer delay 350ms serta click-to-toggle |
| **ISSUE-006** | Engine Peta | Layer batas kalurahan dan data penduduk hilang saat beralih ke Basemap Satelit | CLOSED | Mengganti event `styledata` dengan `map.once('style.load')` untuk style berbasis JS Object |
| **ISSUE-007** | UX / Presentasi | Batas padukuhan lain tetap tampil saat satu padukuhan spesifik dipilih | CLOSED | Mengimplementasikan Focused Padukuhan Boundary Isolation menggunakan ekspresi filter MapLibre |

---

## Rincian Teknis Isu Kritis

### ISSUE-004: Desinkronisasi Data Titik dan Panel Samping
- **Akar Masalah:** Format nomor KK pada berkas Excel terbaca dalam notasi ilmiah eksponensial (`3.404141502E+15`), sehingga terdapat 651 KK yang memiliki string `no_kk` yang sama persis. Fungsi `allHouseholds.find(h => h.no_kk === p.no_kk)` selalu mengembalikan entri pertama (`SUPIYAH`), meskipun yang diklik adalah warga lain.
- **Solusi:** Memberikan indeks integer unik (`_id`) pada setiap objek keluarga saat dimuat dan membacanya langsung via `allHouseholds[p._id]` $O(1)$.

### ISSUE-006: Hilangnya Data pada Basemap Satelit
- **Akar Masalah:** Style Satelit adalah objek JavaScript lokal `{ version: 8, ... }`. MapLibre GL JS tidak memicu `styledata (dataType: style)` untuk objek in-memory, melainkan `style.load`. Listener lama tidak pernah terpicu.
- **Solusi:** Menggunakan event resmi `map.once('style.load')` disertai pengecekan kesiapan style.
