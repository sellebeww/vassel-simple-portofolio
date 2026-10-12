# Vassel Goleyu Portfolio

Portofolio statis: HTML, CSS, JavaScript, dan Python (generator). Tanpa framework atau backend.

## Menjalankan

Buka `index.html`, atau jalankan `python3 -m http.server 8000`.

## Memperbarui

1. Edit `data/portfolio.json` dan simpan gambar di `assets/github/`.
2. Jalankan `python3 scripts/build_site.py` lalu `python3 scripts/check_site.py`.

Struktur HTML ada di `scripts/build_site.py`, tampilan di `assets/css/portfolio.css`, interaksi di `assets/js/portfolio.js`. Catatan sumber: [docs/GITHUB_SYNC.md](docs/GITHUB_SYNC.md).
