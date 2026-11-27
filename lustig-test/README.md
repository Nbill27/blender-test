# Lustig Blender Test (3 detik)

Adegan penutup Lustig, Beat 3 L10: "He was never arrested for the
Eiffel Tower. And the tower is still standing."

Menara Eiffel di senja hari, jalan Paris di bawahnya, Lustig berjalan
ke arah kamera. 90 frame, 1080x1920 vertikal, 30 fps, EEVEE, Blender 4.5.3.

## Fakta (SCRIPT.md, terverifikasi)
Victor Lustig, Mei 1925 Paris, menara dibangun untuk Pameran Dunia 1889,
7.000 ton besi, Andre Poisson membayar sekitar 70.000 franc, Lustig kabur
ke Austria, kembali, kabur ke Amerika, tidak pernah ditangkap karena
Eiffel, menara masih berdiri.

## File
- `build_lustig.py` — membangun scene dari kode, lalu menyimpan
  `scene_lustig.blend`. Menara 4 tier dari anatomy/eiffel.js (skala /4).
- `SKILL_CHECKLIST.md` — semua skill motion yang dipakai, dengan bukti.
- Workflow: `.github/workflows/blender-lustig-test.yml` — 5 job paralel
  x 18 frame, workflow_dispatch dari main.

## Catatan
- Di Remotion shot penutup Lustig sudah pergi; di tes Blender ini figur
  Lustig dihadirkan berjalan sebagai figur uji gerakan, atas instruksi
  brief tes. Bukan klaim fakta baru.
- Tes bisu, tanpa VO/audio baru. WhisperX/librosa TIDAK BERLAKU.
- Jangan upload ke YouTube.
