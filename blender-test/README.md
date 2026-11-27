# Blender Test 3s (kandidat 3: mromidev/claude-blender-skills, blender-film)

Tes kecil, BUKAN produksi. 90 frame (3 detik), 1080x1920, 30 fps, EEVEE
ringan 16 sample, Blender 4.5.3 LTS headless via Mesa.

## File

- `.github/workflows/blender-test.yml` — workflow tes, 5 job paralel,
  tiap job 18 frame, upload PNG + `timing-chunk-N.txt` sebagai artifact.
- `blender-test/build_test_v2.py` — membangun scene dari nol (jalan malam,
  gedung + jendela emissive, hero drone + LED + rotor, kamera chase).
  Scene TIDAK di-push sebagai `.blend` biner; workflow membangunnya di
  runner dengan `blender -b --python blender-test/build_test_v2.py`.

## Perbaikan vs build_test.py v1 (tes VM)

- v1: drone macet di awal path karena Follow Path constraint tidak
  dievaluasi saat render headless, LED/rotor tidak ter-parent dan
  tertinggal di posisi awal, aspal glossy (roughness 0.15) bikin kotak
  terang besar di bawah frame.
- v2: drone digerakkan keyframe lokasi langsung (frame 1 y -22, frame 45
  y 0.08, frame 90 y 22, dicek depsgraph), LED/rotor/top panel di-keyframe
  mengikuti drone dengan offset tetap, aspal roughness 0.8, lampu
  150 -> 120, fill light mengikuti drone, bodi drone abu terang + panel
  emissive cyan supaya terbaca di malam hari, kamera Track To ke drone
  offset -8 / +2.0.
- Still lokal frame 45 (66-74 detik/frame di VM): drone kelihatan jelas
  di tengah jalan, bodi abu, panel cyan, LED magenta, 4 rotor cakram,
  gedung + jendela di kiri kanan. File:
  `~/workspace/motion-studio/tools/blender-test/claude-blender-skills/renders_v2/still_0045.png`

## Hasil VM (pembanding)

- 1 frame full-res: 66-77 detik/frame di VM (1,5 CPU, 7,7 GB RAM, tanpa GPU).
- Proyeksi 90 frame di VM: sekitar 1,8-1,9 jam. Proyeksi 1800 frame
  (60 detik): sekitar 33-38 jam di VM.
- Tujuan tes GitHub ini: ukur waktu nyata per frame di runner GitHub
  (repo public: 4 vCPU, 16 GB RAM) dan total wall time 5 job paralel.

## Jangan

- Jangan merge branch ini ke main tanpa persetujuan bill.
- Jangan pakai workflow ini untuk video 60 detik penuh sebelum hasil
  tes 3 detik ini dinilai.
- Skill ini TIDAK dipasang permanen ke `~/workspace/custom-skills/`.
