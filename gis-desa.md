Membangun **Sistem Informasi Geografis (GIS) Desa** merupakan langkah strategis untuk mengubah data tekstual menjadi alat pengambilan keputusan visual yang akurat.

Berikut adalah tahapan teknis alur kerja pembangunan GIS untuk Kalurahan Pondokrejo:

---

### **TAHAPAN TEKNIS PEMBANGUNAN GIS DESA**

#### **1. Persiapan Data (Data Inventory)**

Sebelum masuk ke perangkat lunak, data harus dalam kondisi "bersih".

* **Data Atribut:** Menyiapkan data penduduk hasil ekspor Excel (seperti yang Anda miliki). Pastikan setiap baris memiliki identitas unik (NIK atau Nomor KK) dan kode wilayah (RT/RW).
* **Data Spasial (Peta Dasar):** Mendapatkan file batas administrasi desa/kalurahan dalam format **Shapefile (.shp)** atau **GeoJSON**. Anda bisa mendapatkannya dari BIG (Badan Informasi Geospasial) atau melakukan *digitasi* mandiri menggunakan citra satelit Google Maps/Bing.

#### **2. Penentuan Koordinat (Geocoding)**

Data penduduk di Excel biasanya belum memiliki koordinat (Latitude/Longitude).

* **Plotting Lapangan:** Menggunakan aplikasi seperti *Ona*, *KoboCollect*, atau *Google Maps* untuk mengambil titik koordinat setiap rumah.
* **Join Data:** Menghubungkan titik koordinat tersebut dengan data atribut (Excel) menggunakan kunci unik (Nomor Rumah/KK).

#### **3. Pemilihan Platform GIS**

Pilih alat yang sesuai dengan kapasitas SDM di Kalurahan:

* **Opsi Gratis/Open Source (Desktop):** **QGIS**. Sangat kuat untuk membuat peta cetak dan analisis mendalam.
* **Opsi Web-Based (Interaktif):** **Google My Maps** (mudah namun terbatas) atau **ArcGIS Online** (berbayar namun profesional).
* **Opsi Mandiri (Web GIS kustom):** Menggunakan *Leaflet.js* atau *Mapbox* untuk membangun dasbor yang terintegrasi dengan Sistem Informasi Desa (SID).

#### **4. Analisis dan Pembuatan Peta Tematik**

Di tahap ini, data angka diubah menjadi visualisasi:

* **Peta Choropleth:** Mewarnai wilayah RT/RW berdasarkan kepadatan penduduk atau tingkat kemiskinan.
* **Point Map:** Menampilkan sebaran fasilitas umum, sebaran rumah tangga miskin, atau lokasi balita stunting.
* **Heatmap:** Melihat konsentrasi area tertentu, misalnya area dengan risiko sanitasi buruk tertinggi.

#### **5. Publikasi dan Integrasi Dasbor**

Agar hasil GIS dapat digunakan oleh Lurah dan Perangkat Desa:

* **Dasbor Interaktif:** Membuat tampilan *User Interface* (UI) yang memudahkan orang awam membaca peta. Misalnya, ketika klik sebuah rumah, muncul data profil keluarga tersebut (sesuai hak akses/privasi).
* **Integrasi SID:** Menghubungkan peta dengan database kependudukan desa agar peta ter-update secara otomatis saat ada perubahan data warga.

---

### **Rekomendasi Arsitektur Sederhana untuk Pondokrejo:**

1. **Input:** Data Excel SDGs Desa yang Anda miliki.
2. **Proses:** Gunakan **QGIS** untuk menggabungkan data Excel dengan batas wilayah RT/RW.
3. **Output:** Unggah ke **Mapbox** atau **Google My Maps** agar bisa diakses oleh Lurah melalui *smartphone* saat tinjauan lapangan.
