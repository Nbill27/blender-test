# Tes Blender Lustig 10 detik (v2)

Adegan penutup Lustig, Beat 3 L10: "He was never arrested for the Eiffel
Tower. And the tower is still standing." Menara Eiffel di senja hari,
jalan Paris, Lustig berjalan menyamping kiri ke kanan melintasi plaza.

## Framing fix v2 (dari v1 3 detik)

Di v1 Lustig jalan ke arah kamera (y -8 ke -13) sementara kamera juga
dolly-in mendekat, jadi dia membesar cepat dan keluar frame kanan bawah
di frame 90. Di v2 jalurnya diubah jadi menyamping (x -3.0 ke +3.0 di
y=-6, jarak ke kamera konstan), ukurannya tetap, utuh di frame 1, 150,
dan 300. Menara tetap dominan di tengah. Kamera dolly-in lebih lembut
dan mundur sedikit: (0,-26,3.2) ke (0,-24,4.0), tanpa drift lateral.

## Format

300 frame, 1080x1920 vertikal, 30 fps, EEVEE_NEXT 16 sample, AgX.
Tes bisu, tanpa VO/audio baru. Walk cycle: kaki kanan lalu kiri
bergantian mengangkat, badan maju ke depan, tanpa goyang kiri-kanan.

## File

- `build_lustig_v2.py` — scene builder (Blender 4.5.3, EEVEE)
- `SKILL_CHECKLIST.md` — checklist semua skill motion (v2)
- Workflow GitHub: `.github/workflows/blender-lustig-test-10s.yml`,
  nama "Blender Lustig Test 10s", 5 job paralel tiap 60 frame,
  artifact `blender-lustig-10s-chunk-N`, retention 7 hari.
- Scene TIDAK di-push sebagai `.blend`; tiap job membangun sendiri
  dari script ini. Jangan upload ke YouTube.
