# Sinkronisasi konten GitHub

Diperiksa: **12 Oktober 2026**. Ruang lingkup: melengkapi website lokal ini
dengan profil, proyek, deskripsi, dan foto dari GitHub pengguna.

## Sumber

- [Repo website asal](https://github.com/sellebeww/vassel-simple-portofolio):
  branch `main` pada `b63773f6c91c8cd5c8fa262c144459582b5292d6`, sama dengan HEAD lokal sebelum perubahan.
- [Data portofolio](https://github.com/sellebeww/vassel-portfolio/blob/7ca030871f2575fe1d33c974ed9bee33e5b4e3e7/src/data/portfolio.ts):
  profil, 10 pengalaman, 9 prestasi, 9 proyek pilihan, tech stack, dan kontak.
- [Gambar portofolio](https://github.com/sellebeww/vassel-portfolio/tree/7ca030871f2575fe1d33c974ed9bee33e5b4e3e7/public/images):
  1 foto profil, 27 foto pengalaman, 9 sertifikat, dan 21 screenshot proyek.
  File WebP disalin tanpa modifikasi ke `assets/github/`.
- [Profil GitHub](https://github.com/sellebeww/sellebeww): minat Node.js,
  design systems, serta PLC/automation.
- [Repositori publik](https://github.com/sellebeww?tab=repositories):
  metadata 17 repo, termasuk profil dan website ini; bukan 17 produk terpisah.
  README tersedia dibaca sebagai referensi; `IF433_Lab_Works` tidak
  menyediakan README melalui endpoint saat pemeriksaan sehingga memakai deskripsi repo.

## Perubahan

- Menyesuaikan pengalaman dengan portofolio terbaru, termasuk President Duta
  Anti Narkoba UMN pada 2025 dan Supervisor Mister & Miss UMN pada 2026.
- Menambah foto pengalaman, sertifikat, screenshot, detail proyek, source, dan demo.
- Menampilkan 8 repo lain sebagai kartu ringkas; tidak membuat screenshot fiktif
  untuk repo yang belum masuk galeri portofolio sumber.
- Memperbaiki email `vasse.jgo` menjadi `vassel.jgo`, menambah LinkedIn/GitHub,
  dan mengganti tautan placeholder dengan tujuan nyata.
- Memperbaiki layout untuk ponsel/landscape; tidak lagi memblokir orientasi layar.
- Mengganti formulir tanpa handler dengan pembuka draf email yang membutuhkan
  pengiriman oleh pengunjung di aplikasi email mereka.
- Mengembalikan komposisi hero dan foto asli, burger di semua ukuran layar,
  menu perspektif dengan bingkai biru, serta navigasi per section sesuai
  [website rujukan](https://sellebeww.github.io/vassel-simple-portofolio/).
- Enam section: Home, Experiences, About Me, Achievements, Projects, Contact. Formulir Chat berada di bawah informasi Contact.
  Konten panjang digulir di dalam section; tersedia tombol sebelumnya/berikutnya.
- Menghapus 42 file lama tak terpakai (2.23 MB): vendor jQuery/Hammer, bundle JS,
  CSS/Sass lama, format font duplikat, dan gambar tanpa referensi. Tetap memakai
  logo, foto hero, dan latar kontak asli serta font Montserrat WOFF yang diperlukan.

## Batas

Snapshot tidak memperbarui dirinya sendiri. Tidak mengambil repositori privat,
mengaudit kode seluruh akun, atau memverifikasi prestasi secara independen.
Keterangan prestasi dan pengalaman mengikuti data pemilik. Demo dan status
produk mengikuti sumber, bukan hasil pengujian ulang proyek-proyek tersebut.
Perubahan hanya ada di checkout lokal; tidak ada push atau deployment.

## Validasi lokal

- `python3 scripts/check_site.py`: 174 referensi, 40 ID unik, seluruh aset
  lokal dan tautan 17 repositori; termasuk pemeriksaan font/latar CSS dan aset tak terpakai.
- `node --check assets/js/portfolio.js` dan `git diff --check` lolos.
- Chrome headless dengan profil sementara memeriksa setiap section pada lebar
  1440, 1000, 850, 600, 390, dan 320 px, serta landscape 844 × 390.
- Pencarian Kotlin (4 repo), pencarian tanpa hasil, reset (17 repo), menu
  ponsel, galeri gambar, Escape, pengembalian fokus, serta validasi formulir lolos.
- Semua gambar halaman berhasil didekode; tidak ada error JavaScript.
- Tanpa JavaScript: keenam section tampil berurutan, navigasi dan kartu tetap tersedia, tombol form
  dinonaktifkan, tautan kontak langsung tetap bisa digunakan.
- Pemeriksaan menggunakan file lokal. Tidak mengirim email, membuka WhatsApp,
  menguji aplikasi email pengguna, atau memverifikasi uptime setiap demo eksternal.

## Penyesuaian sesuai screenshot

- Menghapus tiga highlight Home, kalimat pendamping judul Experiences, serta
  blok “At UMN Medical Center” dan catatan tech stack di About.
- Chat tidak lagi menjadi chapter tersendiri; formulir berada setelah informasi
  Contact dan tetap memiliki anchor `#chat` untuk semua tombol Chat.
- Scroll/swipe menggunakan batas section: baca konten sampai ujung, lalu langsung
  melanjutkan chapter dalam gerakan scroll yang sama. Kembali ke chapter sebelumnya membuka bagian
  bawahnya. Ada jeda transisi 400 ms sebelum menerima scroll pada chapter baru.

Pengujian revisi: enam section, konten screenshot hilang, tautan Chat di Contact,
scroll dalam section, transisi dua arah di batas, perlindungan momentum, batas
section terakhir, simulasi swipe, serta layout 1440/850/390/320 px lolos di Chrome.
Tidak ada error JavaScript selama pengujian.

Revisi lanjutan: judul “Projects”, komposisi Home terpusat tanpa teks/foto bertumpuk,
dan scroll berkelanjutan langsung berpindah saat mencapai batas section.
