# BUILD LOG — news-image-20261123

## Rubrik (Top 5 Rin — analisis)

Kriteria judge (dari RULES.txt kit, sama untuk semua edisi harian),
urut prioritas:

1. **Satu hari + beri nama harinya** — gambar harus menyebut tanggal
   dan peristiwa spesifik hari itu, yang dikenali dari gambar. →
   Masthead "MONDAY 23 NOVEMBER 2026" besar di header + kicker
   "CLIMATE SUMMIT — ANTALYA, TURKEY" + footer sumber bertanggal.
2. **Seleksi & keluasan** — cerita paling berdampak, lintas wilayah
   dan bidang, bukan satu negara/beat. → Lead iklim (global) +
   perang laut Teluk (Timur Tengah) + kapal Rusia di Finlandia
   (Eropa) + kebakaran pabrik Indonesia (Asia) + strip ALSO:
   politik AS, Kyiv, olahraga.
3. **Terbaca** — penonton yang ketinggalan berita bisa tahu apa yang
   terjadi dari gambar saja. → Satu headline raksasa, 3 tile dengan
   judul + 2–3 baris teks, piktogram yang langsung terbaca (tanker
   terbakar, kapal terbakar, pabrik berasap), strip ALSO satu baris.
4. **Akurat** — sesuai laporan, tanpa hype/spekulasi sebagai fakta.
   → Semua angka dari sumber: 194 negara, 2 minggu, runtuh pertama
   sejak Copenhagen 2009, 2 luka di Bahrain, 7 tewas + 50 hilang,
   mayoritas DPR ≥258 kursi (terbesar sejak 1992), 14 hilang di Kyiv.
   COP31 runtuh Minggu 22 Nov malam dan jadi headline utama siklus
   berita Senin 23 Nov (CNN/Reuters/Le Monde terbit 22–23 Nov).
5. **Craft** — satu komposisi jelas, terbaca di ~300 px, tanpa teks
   rusak. → Layout broadsheet: header teal, hero kiri + globe kanan,
   3 tile sejajar, band bawah gelap. Semua teks diuji visual 3×;
   2 revisi memperbaiki tabrakan (masthead vs tanggal, subhead vs
   chip, stamp vs chip, asap melewati divider, teks tile meluber ke
   band bawah).

## Optimasi / desain

- **Komposisi satu halaman**: hero COP31 mengambil ~45% tinggi
  halaman (globe retak + palu + stempel NO DEAL = ikonik dan langsung
  terbaca bahkan kecil); tile di bawah memberi keluasan tanpa
  mengorbankan lead.
- **Palet kontras**: kertas krem + teal gelap + merah aksen; teks
  gelap di atas terang, teks krem di atas band gelap — tetap terbaca
  saat diperkecil.
- **Determinisme**: tanpa jam/network/random; font DejaVu sistem;
  render 3× hash identik; main.py hanya menyalin byte (stdlib).
- **Ukuran file**: 126.812 byte, jauh di bawah batas 1 MiB.

## Edge case

- `/output` belum ada → main.py `mkdir -p` (parents=True).
- `MAKEFUN_OUTPUT_DIR` tidak diset → default `/output`.
- `entry.png` hilang/rusak → main.py exit 1 dengan pesan (bukan
  menulis file setengah).
- PNG > 1 MiB atau bukan PNG → ditolak main.py sebelum menulis.
- Teks panjang → `wrap()` mengukur lebar nyata per kata; semua
  blok teks dibatasi lebar kolomnya dan diinspeksi visual agar tidak
  ada yang terpotong/meluber.

## Berita terpilih (fakta kunci)

| # | Cerita | Fakta |
|---|--------|-------|
| 1 | COP31 runtuh | Antalya, Turki; >2 minggu, COP terpanjang; pertama gagal sejak Copenhagen 2009; draf akhir tanpa kata "fossil fuels"/minyak/batu bara/gas; UE menolak; 194 pihak; AS absen |
| 2 | Perang di laut | Serangan Iran lukai 2 orang di Bahrain; tanker kena proyektil di Selat Hormuz (UKMTO) |
| 3 | Kapal terbakar | Kapal kargo Rusia Sparta II masih terbakar di lepas Finlandia pasca serangan drone; kru dievakuasi |
| 4 | Kebakaran pabrik | Pabrik permen Indonesia: 7 tewas, 50 hilang |
| 5 | ALSO | Demokrat raih mayoritas DPR AS terbesar sejak 1992 (≥258 kursi); 14 hilang pasca drone Rusia hantam gedung dekat Kyiv; Verstappen menangi GP Las Vegas |

Sumber: CNN, Reuters, Le Monde, AFP, phys.org (23 Nov 2026).

## Verifikasi

- `render.py` 3× → sha256 identik
  `baba0b8467b179d83858ed2b60795c73b75f44d0321ad4c534db6c31c53f4bef`
  (126.812 byte, 1024×1024 PNG).
- `main.py` 2× ke dir berbeda → hash identik dengan entry.png.
- Inspeksi visual 3× (lihat revisi di atas).
- `check_entry.py` + kit check: kit 20261123 sempat 503 kit_pending
  ~87 menit (00:40–01:27 UTC), lalu berhasil diunduh (requirements.json
  sha256 95750875…, kit.tar.gz sha256 a9620cc9…). `check_entry.py`
  **8/8 PASS** (single_commit SKIP — belum git repo; entrypoint_not_
  starter SKIP — kit hanya punya starter main.ts). Kit check
  `node cli/makefun.mjs check --kit . --repo entry --worktree`:
  **4 passed, 1 failed, 14 skipped, 5 at-submission** — lolos:
  competition_open, snapshot (7 file, 147.550 byte), license_osi,
  entrypoint (main.py → python3.13); gagal hanya transcripts_present
  (bundle tugas koordinator); at-submission: repo_public, repo_owner,
  repo_created_after_open, commit_in_repo, duplicate_snapshot
  (repo GitHub tugas koordinator).
