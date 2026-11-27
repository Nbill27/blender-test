# SKILL_CHECKLIST.md — Tes Blender adegan penutup Lustig (3 detik)

Judul: "The Con Man Who Sold the Eiffel Tower Twice" — Victor Lustig, Paris 1925.
Adegan: penutup Beat 3, L10: "He was never arrested for the Eiffel Tower.
And the tower is still standing." Menara Eiffel di senja hari, jalan Paris,
Lustig berjalan ke arah kamera.
Folder tes: `~/workspace/motion-studio/tools/blender-test/lustig-test/`
Repo GitHub: https://github.com/Nbill27/blender-test (workflow baru
`blender-lustig-test.yml`, BUKAN repo 3d-rendering, PR #13 di sana TIDAK di-merge)
Format: 90 frame, 1080x1920 vertikal, 30 fps, EEVEE_NEXT 16 sample, AgX.
Status: scene lokal selesai dan still frame 45 lolos gate (2 revisi).
Workflow GitHub SIAP di `gh-push/`, BELUM di-push — butuh browser task
sebagai Nbill27 (push MCP gagal 403 sebelumnya, sama seperti tes drone).

## Fakta yang dipakai (SCRIPT.md, terverifikasi, tidak dikarang)
- Mei 1925, Paris. Menara dibangun untuk Pameran Dunia 1889, 7.000 ton besi.
- Andre Poisson membayar sekitar 70.000 franc. Lustig kabur ke Austria,
  kembali, kabur ke Amerika. Tidak pernah ditangkap karena Eiffel.
  Menara masih berdiri.
- Perbedaan yang disengaja vs Remotion shot 10: di Remotion Lustig sudah
  pergi di shot penutup; di tes Blender ini figur Lustig dihadirkan berjalan
  sebagai figur uji gerakan kaki dan kamera, atas instruksi brief tes.
  Bukan klaim fakta baru, tidak ada dialog/kutipan yang ditambah.

## Tahap 0. gaya_video_bill + desain.md — SELESAI
- Dibaca: `~/workspace/custom-skills/gaya_video_bill/SKILL.md` dan
  `~/workspace/motion-studio/desain.md`.
- Diterapkan: vertikal 9:16 1080x1920 30 fps; adegan PADAT dan ramai
  (menara + 3 gedung + 3 pohon + 4 lampu + 2 bangku + 2 bendera + 4 pejalan
  kaki + 3 burung + 4 awan + matahari), bukan latar kosong; gerakan terlihat
  jelas dari detik pertama (dolly-in kamera + Lustig berjalan + burung
  terbang + awan hanyut + bendera berkibar + beacon berkedip); zona aman
  bawah dijaga, tidak ada teks layar di tes ini.
- Bukti: `build_lustig.py`, `renders/still_0045.png`, `ref/lustig_55s.png`,
  `ref/lustig_57s.png`, `ref/lustig_59s.png`.

## Tahap 1. cartoon_3d_short — SELESAI
- Karakter bean-head stylized: kepala bulat besar (skala 1.12), badan kecil,
  topi Lustig, jas gelap. Bukan fotorealistis.
- Kamera dinamis: dolly-in (0,-25,3.2) -> (0,-22.5,4.2), Track To menara
  (0,0,13), lensa 22. Satu shot 3 detik, tidak ada hard cut di dalam tes.
- Dunia 3D padat: plaza Paris, jalan, gedung oranye kanan, pohon, lampu.
- Bukti: `build_lustig.py` (walker, kamera), `renders/still_0045.png`.

## Tahap 2. anatomy — SELESAI
- Objek kunci: Menara Eiffel, acuan `~/workspace/motion-studio/projects/lustig/anatomy/eiffel.js`
  dan `eiffel-tower.html` (tidak ditempel mentah, dipakai sebagai acuan bentuk).
- 4 tier sesuai eiffel.js (skala /4): tier 1 z 0-8.5 kaki 5.0->3.2,
  tier 2 z 8.5-15.5 kaki 3.2->2.0, tier 3 z 15.5-21 kaki 2.0->1.1,
  spire z 21-26, antena ke 28, beacon di 28.7.
- Bagian: 12 kaki miring, ring balok, 3 dek + railing, arch depan-belakang
  (kurva sinus seperti archPts di eiffel.js), X-bracing, spire kerucut 4 sisi.
- Gerakan mengikuti mekanisme: beacon berkedip (skala 1.0-1.5),
  bendera berkibar (rotasi sinus), burung terbang, awan hanyut.
- Bukti: `build_lustig.py` (TIERS, arch, beacon), `renders/still_0045.png`.

## Tahap 3. anatomy_reveal — SELESAI
- Struktur tier terbaca terpisah: tiap dek menonjol sebagai pelat + railing,
  X-bracing tiap tier terlihat, spire terpisah dari tier 3, antena terpisah.
- Bukti: `renders/still_0045.png` — 3 dek, X-bracing, spire, dan beacon
  semuanya terlihat dan terbedakan.

## Tahap 4. hairline_create + hairline_adopt — SELESAI
- Garis tipis struktur: X-bracing 0.16, arch rib 0.28, railing 0.06,
  jendela gedung, tiang lampu dan bendera — garis yang menjawab gerakan
  kamera (parallax antar garis depan dan belakang saat dolly-in).
- Bukti: `build_lustig.py` (beam, brace), `renders/still_0045.png`.

## Tahap 5. motion_design — SELESAI
- Timing/easing: semua keyframe gerak interpolasi BEZIER; dolly-in kamera
  ease (3 keyframe, makin pelan di akhir); walk cycle kaki bergantian tiap
  11 frame (kaki kanan lalu kiri mengangkat, bukan bareng — sesuai aturan
  jalan baru bill 27 Nov 2026: tidak boleh goyang kiri-kanan, badan maju
  ke depan, tanpa drift lateral kamera; kamera di sini hanya maju lurus
  di sumbu Y, x tetap 0); lengan berlawanan dengan kaki; topi dan jas
  ikut badan (follow-through, tidak tertinggal).
- Prinsip Disney: anticipation (Lustig condong maju), follow-through
  (topi/badan ikut), squash tidak dipakai karena figur blocky kaku.
- Bukti: `build_lustig.py` (walk_cycle, key_loc/key_rot),
  CHECK frame 1/45/90: Lustig (1.8,-8.0) -> (2.2,-10.47) -> (2.6,-13.0),
  kamera (0,-25,3.2) -> (0,-23.8,3.7) -> (0,-22.5,4.2).

## Tahap 6. remotion_best_practices — SELESAI (tahap lokal)
- Alur preview -> frame check -> revisi -> verifikasi, sama seperti
  workflow Remotion Lustig.
- Still lokal frame 45 dibaca sendiri, 2 revisi:
  - v1: langit abu datar, pita horizon krem terbaca seperti dinding,
    awan pil besar di tengah menara.
  - Revisi 1: horizon dihapus, langit dihangatkan, matahari ke dalam frame,
    awan dikecilkan dan dinaikkan.
  - v2: matahari jadi cakram putih raksasa terpotong di tepi kiri.
  - Revisi 2: matahari dikecilkan (r 2.8 -> 1.6), warna dihangatkan.
  - v3 (final lokal): gate lolos — menara dan Lustig jelas, tidak terpotong.
- Cacat jujur yang tersisa di still final: langit datar tanpa gradasi
  (world EEVEE satu warna); matahari krem pucat, bukan oranye hangat;
  awan masih bentuk pil/elips; sepertiga bawah frame masih agak kosong;
  besi menara mauve pucat, bukan siluet gelap; wajah Lustig polos
  (tanpa mata/bekas luka); kepala lampu putih kotak.
- Verifikasi GitHub (chunk, ffprobe, 3 still) BELUM dilakukan — menunggu
  push dan run workflow lewat browser.
- Bukti: `renders/still_0045.png` (v3 final), `build_lustig.py`.

## Tahap 7. WhisperX dan librosa — TIDAK BERLAKU
- TIDAK BERLAKU karena tes ini bisu 3 detik, tanpa VO baru dan tanpa
  audio apa pun. Tidak ada yang perlu ditranskripsi (WhisperX) atau
  dianalisis (librosa). VO Casper Lustig yang sudah ada tidak dipakai
  ulang di tes ini.

## Tahap 8. resumable_long_renders — SELESAI (desain), run BELUM
- Render dipecah 5 chunk x 18 frame, tiap chunk bisa diulang sendiri
  tanpa mengulang 90 frame — sama seperti workflow tes drone yang sudah
  terbukti (run #1: 90 frame dalam 8m36s, rata-rata 18,86 detik/frame).
- Workflow: `gh-push/.github/workflows/blender-lustig-test.yml`,
  nama "Blender Lustig Test", workflow_dispatch, timeout 120 menit,
  5 job paralel, artifact `blender-lustig-3s-chunk-N`, retention 7 hari.
- Waktu lokal per frame: 52-56 detik/frame di VM (frame 45: 56 detik v1,
  52 detik v2). Proyeksi VM 90 frame sekitar 1,3-1,4 jam; proyeksi GitHub
  sekitar 19 detik/frame (angka tes drone), wall time sekitar 9 menit —
  perkiraan, belum terukur untuk scene ini.
- Bukti: workflow di `gh-push/`, `build_lustig.py`.

## v2 — Framing fix + 10 detik (2026-11-27, perbaikan atas pilihan bill)

### Cacat v1 yang diperbaiki
- v1 frame 90: Lustig keluar frame kanan bawah, hanya topi dan kepala
  kelihatan. Akar masalah: dia jalan KE ARAH kamera (y -8 -> -13)
  sementara kamera juga dolly-in (y -25 -> -22.5); jarak mengecil dua
  kali, dia membesar cepat.
- Perbaikan: jalur diubah jadi MENYAMPING kiri -> kanan melintasi plaza
  (x -3.0 -> +3.0 di y=-6, di atas jalan Path, jarak ke kamera konstan),
  menghadap +X. `walker()` dapat mode `sideways=True` (kaki/lengan
  berjajar sepanjang sumbu Y, badan diputar), `walk_cycle()` dapat
  `axis='x'` (kaki mengayun di bidang X-Z, rotasi sumbu Y). Kamera
  dolly-in lebih lembut dan mundur sedikit: (0,-26,3.2) -> (0,-25,3.6)
  -> (0,-24,4.0), x tetap 0, tanpa drift lateral. Menara TIDAK diubah.
- Awan/burung/bendera/beacon diperpanjang ke frame 300 dengan total
  perpindahan yang sama (awan +6, burung +16, bendera pola 11 frame,
  beacon 15 keyframe). Pejalan kaki latar juga 1-300.

### Verifikasi lokal v2 — GATE LOLOS di revisi pertama (tidak perlu revisi ke-2)
- Build: `build_lustig_v2.py`, Blender 4.5.3, 5 detik, CHECK posisi
  terverifikasi: Lustig (-3.0,-6.0) -> (-0.01,-6.0) -> (3.0,-6.0),
  kamera (0,-26,3.2) -> (0,-25,3.6) -> (0,-24,4.0). y Lustig konstan.
- Catatan: render lokal sempat gagal `Couldn't open libEGL.so.1`;
  diperbaiki dengan `sudo apt-get update && apt-get install -y libegl1
  libegl-mesa0` (paket ini hilang di VM, sebelumnya ada saat tes kandidat).
- Still dibaca sendiri, semua 1080x1920:
  - `renders-v2/still_0001.png` (56 detik): Lustig di kiri, UTUH,
    bertopi, kaki sedang melangkah, di depan kaki menara kiri. Menara
    dominan di tengah, burung di kiri, matahari kiri.
  - `renders-v2/still_0150.png` (49 detik): Lustig di TENGAH di bawah
    arch, UTUH, badan dan kaki lengkap, topi terlihat. Dua pejalan
    kaki latar di kiri dan kanan arch.
  - `renders-v2/still_0300.png` (48 detik): Lustig di kanan, UTUH,
    kaki sedang melangkah, topi dan kepala lengkap, tidak terpotong
    tepi bawah atau kanan. Burung sudah bergeser ke kanan, awan hanyut.
- Cacat jujur yang TETAP ada dari v1 (bukan target perbaikan ini):
  langit datar tanpa gradasi, matahari krem pucat, awan bentuk pil,
  wajah Lustig polos tanpa mata/bekas luka, kepala lampu putih kotak.
- Waktu lokal per frame v2: 56, 49, 48 detik (rata-rata ~51 detik).
  Proyeksi VM 300 frame sekitar 4,2 jam; proyeksi GitHub sekitar
  11-14 detik/frame (angka chunk normal run v1) jadi wall time sekitar
  15-20 menit untuk 5 job x 60 frame, atau sekitar 30 menit kalau ada
  satu chunk pencilan lambat seperti chunk 1 di run v1 (86,72 detik/frame).

### Skill (tetap dipakai semua, sama seperti v1)
- gaya_video_bill, cartoon_3d_short, anatomy, anatomy_reveal,
  hairline_create/adopt, motion_design, remotion_best_practices:
  tidak ada yang berubah dari v1 kecuali jalur Lustig dan kamera
  (motion_design) dan frame check 1/150/300 (remotion_best_practices).
- WhisperX/librosa: TIDAK BERLAKU, tes tetap bisu 10 detik tanpa VO/audio.
- resumable_long_renders: 5 chunk x 60 frame di GitHub Actions.

### Staging GitHub v2 — SIAP, BELUM di-push (butuh browser sebagai Nbill27)
- `gh-push-v2/.github/workflows/blender-lustig-test-10s.yml` — nama
  "Blender Lustig Test 10s", workflow_dispatch, 5 job paralel
  (1-60, 61-120, 121-180, 181-240, 241-300), timeout 120 menit,
  Blender 4.5.3 LTS, EEVEE, LIBGL_ALWAYS_SOFTWARE=1, artifact
  `blender-lustig-10s-chunk-N`, retention 7 hari. YAML divalidasi parser.
- `gh-push-v2/lustig-test/build_lustig_v2.py` — script yang diperbaiki.
- `gh-push-v2/lustig-test/README.md` — penjelasan v2.
- `gh-push-v2/lustig-test/SKILL_CHECKLIST.md` — salinan checklist ini.
- Jangan upload `scene_lustig_v2.blend`. Jangan sentuh repo
  3d-rendering atau PR #13. Jangan push lewat MCP kalau gagal 403.

## Langkah berikutnya (butuh browser sebagai Nbill27)
1. Upload 4 file dari `gh-push-v2/` ke repo https://github.com/Nbill27/blender-test,
   branch main, path persis `.github/workflows/blender-lustig-test-10s.yml`,
   `lustig-test/build_lustig_v2.py`, `lustig-test/README.md`,
   `lustig-test/SKILL_CHECKLIST.md`. Jangan upload `scene_lustig_v2.blend`. Jangan sentuh repo 3d-rendering, jangan merge PR #13.
2. Jalankan workflow "Blender Lustig Test 10s" dari main, catat waktu mulai/selesai
   tiap job dan isi timing-lustig-10s-chunk-0..4.txt.
3. Unduh 5 artifact, rakit klip MP4 10 detik 1080x1920 30 fps, verifikasi
   ffprobe (300 frame, 10.000 detik), baca 3 still (awal, tengah, akhir),
   buktikan Lustig utuh di semua frame dan menara tetap di tengah.

## File
- `build_lustig.py` — scene builder (Blender 4.5.3, EEVEE_NEXT 16 sample)
- `scene_lustig.blend` — hasil build lokal (1,7 MB, TIDAK di-push)
- `renders/still_0045.png` — still lokal final (v3, 1080x1920)
- `ref/lustig_55s.png`, `ref/lustig_57s.png`, `ref/lustig_59s.png` —
  referensi dari lustig-final.mp4 detik 55-60
- `gh-push/.github/workflows/blender-lustig-test.yml` — workflow GitHub
- `gh-push/lustig-test/build_lustig.py` — salinan script untuk di-push
- `gh-push/lustig-test/README.md` — penjelasan singkat untuk repo

## Langkah berikutnya (butuh browser sebagai Nbill27)
1. Upload 3 file dari `gh-push/` ke repo https://github.com/Nbill27/blender-test,
   branch main, path persis `.github/workflows/blender-lustig-test.yml`,
   `lustig-test/build_lustig.py`, `lustig-test/README.md`. Jangan upload
   `scene_lustig.blend`. Jangan sentuh repo 3d-rendering, jangan merge PR #13.
2. Jalankan workflow "Blender Lustig Test" dari main, catat waktu mulai/selesai
   tiap job dan isi timing-lustig-chunk-0..4.txt.
3. Unduh 5 artifact, rakit klip MP4 3 detik 1080x1920 30 fps, verifikasi
   ffprobe (90 frame, 3.000 detik), baca 3 still (awal, tengah, akhir),
   buktikan menara dan Lustig bergerak / kamera bergerak.
