# build_lustig.py - Tes Blender adegan penutup Lustig (Beat 3, L10)
# "He was never arrested for the Eiffel Tower. And the tower is still standing."
# Menara Eiffel di senja hari, jalan Paris di bawahnya, Lustig berjalan ke arah kamera.
#
# Fakta (SCRIPT.md, terverifikasi): Victor Lustig, Mei 1925 Paris, menara
# dibangun untuk Pameran Dunia 1889, 7.000 ton besi, Andre Poisson membayar
# sekitar 70.000 franc, Lustig kabur ke Austria, kembali, kabur ke Amerika,
# tidak pernah ditangkap karena Eiffel, menara masih berdiri.
# Referensi visual: lustig-final.mp4 detik 55-60 (shot 10 sunset Remotion)
# dan anatomy/eiffel.js (4 tier: 0-34, 36-62, 64-84, spire 86-104, antena 112).
# Perbedaan yang disengaja vs Remotion shot 10: di Remotion Lustig sudah pergi,
# di tes Blender ini figur Lustig dihadirkan berjalan sebagai figur uji
# gerakan kaki dan kamera, atas instruksi brief tes. Bukan klaim fakta baru.
#
# Skill yang diterapkan (lihat SKILL_CHECKLIST.md di folder ini):
# - gaya_video_bill/desain.md: padat, ramai, gerakan jelas dari detik pertama.
# - cartoon_3d_short: karakter bean-head stylized, kamera glide, dunia 3D padat.
# - anatomy/anatomy_reveal: menara 4 tier dari eiffel.js, dek, X-bracing, spire,
#   antena, beacon; bagian bergerak mengikuti mekanismenya (beacon berkedip,
#   bendera berkibar, burung terbang, awan hanyut).
# - hairline_create/adopt: garis tipis X-bracing, arch rib, railing, jendela.
# - motion_design: dolly-in ease, walk cycle kaki bergantian + squash,
#   topi dan jas follow-through, easing BEZIER di semua keyframe gerak.
# - remotion_best_practices: still frame check lokal dulu, baru GitHub.
# - WhisperX/librosa: TIDAK BERLAKU, tes bisu 3 detik tanpa VO/audio baru.
# - resumable_long_renders: 5 chunk x 18 frame di GitHub Actions.
#
# Format: 90 frame, 1080x1920 vertikal, 30 fps, EEVEE_NEXT 16 sample, AgX.
import bpy, math, os, random
from mathutils import Vector

D = os.path.dirname(os.path.abspath(__file__))
BLEND = os.path.join(D, "scene_lustig.blend")
OUTDIR = os.path.join(D, "renders")
os.makedirs(OUTDIR, exist_ok=True)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for coll in list(bpy.data.collections):
    if coll.name != "Collection":
        bpy.data.collections.remove(coll)

sc = bpy.context.scene
sc.frame_start, sc.frame_end = 1, 90
sc.render.fps = 30
sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
sc.render.resolution_percentage = 100
sc.render.engine = 'BLENDER_EEVEE_NEXT'
sc.render.image_settings.file_format = 'PNG'
sc.render.image_settings.color_mode = 'RGB'
sc.render.filepath = os.path.join(OUTDIR, "frame_")
sc.view_settings.view_transform = 'AgX'
sc.eevee.taa_render_samples = 16

col = bpy.data.collections.new("Lustig_Test")
sc.collection.children.link(col)

def mat(name, base, rough=0.6, metal=0.0, emit=None, strength=0.0, spec=0.5):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = base
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if "Specular IOR Level" in b.inputs:
        b.inputs["Specular IOR Level"].default_value = spec
    if emit is not None:
        key = "Emission Color" if "Emission Color" in b.inputs else "Emission"
        b.inputs[key].default_value = emit
        if "Emission Strength" in b.inputs:
            b.inputs["Emission Strength"].default_value = strength
    return m

def _link(o):
    try:
        sc.collection.objects.unlink(o)
    except RuntimeError:
        pass
    if o.name not in col.objects:
        col.objects.link(o)
    return o

def box(name, loc, scale, material, rot=None):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = scale
    if rot:
        o.rotation_euler = rot
    if material:
        o.data.materials.append(material)
    return _link(o)

def beam(name, p0, p1, thick, material):
    """Balok tipis dari p0 ke p1 (hairline: garis struktur menara)."""
    p0, p1 = Vector(p0), Vector(p1)
    mid = (p0 + p1) / 2
    d = p1 - p0
    length = d.length
    bpy.ops.mesh.primitive_cube_add(location=mid)
    o = bpy.context.active_object
    o.name = name
    o.scale = (thick, thick, length / 2)
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    if material:
        o.data.materials.append(material)
    return _link(o)

def cyl(name, loc, radius, depth, material, rot=None, vertices=16):
    bpy.ops.mesh.primitive_cylinder_add(location=loc, radius=radius,
                                        depth=depth, vertices=vertices)
    o = bpy.context.active_object
    o.name = name
    if rot:
        o.rotation_euler = rot
    if material:
        o.data.materials.append(material)
    return _link(o)

def sphere(name, loc, radius, material, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_uv_sphere_add(location=loc, radius=radius)
    o = bpy.context.active_object
    o.name = name
    o.scale = scale
    if material:
        o.data.materials.append(material)
    return _link(o)

def key_loc(obj, frames_locs, interp='BEZIER'):
    for f, loc in frames_locs:
        obj.location = loc
        obj.keyframe_insert("location", frame=f)
    if obj.animation_data and obj.animation_data.action:
        for fc in obj.animation_data.action.fcurves:
            if fc.data_path == "location":
                for kp in fc.keyframe_points:
                    kp.interpolation = interp

def key_rot(obj, frames_rots, interp='BEZIER'):
    for f, rot in frames_rots:
        obj.rotation_euler = rot
        obj.keyframe_insert("rotation_euler", frame=f)
    if obj.animation_data and obj.animation_data.action:
        for fc in obj.animation_data.action.fcurves:
            if fc.data_path == "rotation_euler":
                for kp in fc.keyframe_points:
                    kp.interpolation = interp

# ---------- Material ----------
iron = mat("Iron", (0.11, 0.10, 0.22, 1), rough=0.55, metal=0.35, spec=0.4)
iron_dark = mat("IronDark", (0.08, 0.08, 0.17, 1), rough=0.6, metal=0.3)
ground_mat = mat("Cobble", (0.45, 0.28, 0.14, 1), rough=0.95)
path_mat = mat("Path", (0.80, 0.60, 0.35, 1), rough=0.9)
bldg_orange = mat("BldgOrange", (0.75, 0.32, 0.10, 1), rough=0.85)
bldg_blue = mat("BldgBlue", (0.30, 0.32, 0.55, 1), rough=0.85)
win_warm = mat("WinWarm", (0.1, 0.07, 0.04, 1), emit=(1.0, 0.62, 0.25, 1), strength=3.5)
win_cool = mat("WinCool", (0.05, 0.08, 0.10, 1), emit=(0.55, 0.75, 1.0, 1), strength=2.5)
win_off = mat("WinOff", (0.15, 0.12, 0.10, 1), rough=0.9)
tree_mat = mat("Tree", (0.10, 0.28, 0.24, 1), rough=0.9)
trunk_mat = mat("Trunk", (0.25, 0.16, 0.10, 1), rough=0.9)
lamp_mat = mat("LampPost", (0.12, 0.12, 0.16, 1), rough=0.6, metal=0.4)
lamp_glow = mat("LampGlow", (0.1, 0.07, 0.03, 1), emit=(1.0, 0.7, 0.35, 1), strength=5.0)
sun_mat = mat("Sun", (0.1, 0.04, 0.01, 1), emit=(1.0, 0.55, 0.20, 1), strength=7.0)
cloud_mat = mat("Cloud", (0.95, 0.75, 0.70, 1), rough=1.0, emit=(0.95, 0.7, 0.6, 1), strength=0.35)
horizon_mat = mat("Horizon", (0.1, 0.04, 0.02, 1), emit=(1.0, 0.55, 0.25, 1), strength=2.0)
suit_mat = mat("Suit", (0.08, 0.08, 0.14, 1), rough=0.7)
skin_mat = mat("Skin", (0.85, 0.65, 0.50, 1), rough=0.6)
hat_mat = mat("Hat", (0.02, 0.02, 0.02, 1), rough=0.5)
shirt_mat = mat("Shirt", (0.9, 0.9, 0.85, 1), rough=0.8)
beacon_mat = mat("Beacon", (0.1, 0.02, 0.02, 1), emit=(1.0, 0.15, 0.1, 1), strength=6.0)
flag_blue = mat("FlagBlue", (0.10, 0.20, 0.70, 1), rough=0.8)
flag_white = mat("FlagWhite", (0.9, 0.9, 0.9, 1), rough=0.8)
flag_red = mat("FlagRed", (0.75, 0.10, 0.15, 1), rough=0.8)

# ---------- Tanah dan jalan ----------
box("Ground", (0, 0, -0.15), (22, 30, 0.15), ground_mat)
box("Path", (0, -5, 0.02), (3.2, 26, 0.02), path_mat)
# Jalur samping kiri
box("PathL", (-6.5, -5, 0.02), (2.5, 26, 0.02), path_mat)

# ---------- Menara Eiffel, 4 tier dari eiffel.js (skala /4) ----------
# Tier: 1 z 0-8.5 (kaki 5.0 -> 3.2), 2 z 8.5-15.5 (3.2 -> 2.0),
#       3 z 15.5-21 (2.0 -> 1.1), spire z 21-26 (1.1 -> 0.15), antena ke 28.
TIERS = [
    (0.0, 8.5, 5.0, 3.2),
    (8.5, 15.5, 3.2, 2.0),
    (15.5, 21.0, 2.0, 1.1),
]
def half_at(tier, z):
    z0, z1, h0, h1 = tier
    t = (z - z0) / (z1 - z0)
    return h0 + (h1 - h0) * t

for ti, tier in enumerate(TIERS):
    z0, z1, h0, h1 = tier
    # 4 kaki miring ke dalam
    for sx in (-1, 1):
        for sy in (-1, 1):
            beam(f"Leg_T{ti+1}_{sx}_{sy}",
                 (sx * h0, sy * h0, z0), (sx * h1, sy * h1, z1), 0.42, iron)
    # Ring balok di atas tiap tier
    hz = half_at(tier, z1)
    for y in (-hz, hz):
        beam(f"Ring_T{ti+1}_Y{y:.0f}", (-hz, y, z1), (hz, y, z1), 0.30, iron_dark)
    for x in (-hz, hz):
        beam(f"Ring_T{ti+1}_X{x:.0f}", (x, -hz, z1), (x, hz, z1), 0.30, iron_dark)
    # X-bracing tipis di 4 sisi (hairline)
    zm, hm = (z0 + z1) / 2, (h0 + h1) / 2
    for face in range(4):
        if face == 0:
            beam(f"Brace_T{ti+1}_F0a", (-hm, hm, z0 + 0.6), (hm, hm, z1 - 0.6), 0.16, iron_dark)
            beam(f"Brace_T{ti+1}_F0b", (hm, hm, z0 + 0.6), (-hm, hm, z1 - 0.6), 0.16, iron_dark)
        elif face == 1:
            beam(f"Brace_T{ti+1}_F1a", (-hm, -hm, z0 + 0.6), (hm, -hm, z1 - 0.6), 0.16, iron_dark)
            beam(f"Brace_T{ti+1}_F1b", (hm, -hm, z0 + 0.6), (-hm, -hm, z1 - 0.6), 0.16, iron_dark)
        elif face == 2:
            beam(f"Brace_T{ti+1}_F2a", (hm, -hm, z0 + 0.6), (hm, hm, z1 - 0.6), 0.16, iron_dark)
            beam(f"Brace_T{ti+1}_F2b", (hm, hm, z0 + 0.6), (hm, -hm, z1 - 0.6), 0.16, iron_dark)
        else:
            beam(f"Brace_T{ti+1}_F3a", (-hm, -hm, z0 + 0.6), (-hm, hm, z1 - 0.6), 0.16, iron_dark)
            beam(f"Brace_T{ti+1}_F3b", (-hm, hm, z0 + 0.6), (-hm, -hm, z1 - 0.6), 0.16, iron_dark)
    # Dek + railing
    box(f"Deck_T{ti+1}", (0, 0, z1 + 0.2), (hz + 0.6, hz + 0.6, 0.2), iron_dark)
    for y in (-hz - 0.5, hz + 0.5):
        box(f"Rail_T{ti+1}_Y{y:.0f}", (0, y, z1 + 0.75), (hz + 0.6, 0.06, 0.5), iron)
    for x in (-hz - 0.5, hz + 0.5):
        box(f"Rail_T{ti+1}_X{x:.0f}", (x, 0, z1 + 0.75), (0.06, hz + 0.6, 0.5), iron)

# Arch di dasar, depan dan belakang (kurva sinus seperti eiffel.js archPts)
for face_y in (5.0, -5.0):
    pts = []
    for k in range(9):
        t = k / 8
        z = 1.5 + 4.0 * math.sin(math.pi * t)
        x = -5.0 + 10.0 * t
        pts.append((x, face_y, z))
    for k in range(8):
        beam(f"Arch_{face_y:.0f}_{k}", pts[k], pts[k + 1], 0.28, iron)

# Spire: kerucut 4 sisi + antena + beacon yang berkedip (skala)
bpy.ops.mesh.primitive_cone_add(location=(0, 0, 23.5), radius1=1.1, radius2=0.15,
                                depth=5.0, vertices=4)
spire = bpy.context.active_object
spire.name = "Spire"
spire.rotation_euler = (0, 0, math.radians(45))
spire.data.materials.append(iron)
_link(spire)
cyl("Antenna", (0, 0, 27.2), 0.09, 2.6, iron_dark)
beacon = sphere("Beacon", (0, 0, 28.7), 0.32, beacon_mat)
for f, s in ((1, 1.0), (23, 1.5), (45, 1.0), (68, 1.5), (90, 1.0)):
    beacon.scale = (s, s, s)
    beacon.keyframe_insert("scale", frame=f)

# ---------- Langit senja: matahari, awan, burung ----------
# REVISI 1 (setelah still 45 v1): pita HorizonGlow dihapus, itu terbaca
# seperti dinding krem di belakang menara. Matahari dipindah ke dalam frame
# kiri. Awan dikecilkan, dinaikkan ke sepertiga atas, dibuat lebih lembut.
sphere("Sun", (-10, 2, 10), 1.6, sun_mat)
random.seed(11)
clouds = []
for i, (cx, cy, cz, cs) in enumerate([(-9, 6, 24, 2.2), (8, 10, 25, 2.6),
                                      (-4, 14, 26, 1.8), (11, 2, 23, 1.6)]):
    c = sphere(f"Cloud{i}", (cx, cy, cz), cs, cloud_mat, scale=(1.4, 0.4, 0.35))
    clouds.append((c, cx))
    key_loc(c, [(1, (cx, cy, cz)), (90, (cx + 1.8, cy, cz))], interp='LINEAR')
birds = []
for i, (bx, by, bz) in enumerate([(-9, 4, 18), (-6, 8, 20), (-11, 0, 16)]):
    b1 = box(f"Bird{i}a", (bx, by, bz), (0.35, 0.05, 0.05), iron_dark,
             rot=(0, 0, math.radians(25)))
    b2 = box(f"Bird{i}b", (bx, by, bz), (0.35, 0.05, 0.05), iron_dark,
             rot=(0, 0, math.radians(-25)))
    birds.append((b1, b2, bx, by, bz))
    for o, dx in ((b1, -0.3), (b2, 0.3)):
        key_loc(o, [(1, (bx + dx, by, bz)), (90, (bx + dx + 16, by + 2, bz + 1))],
                interp='LINEAR')

# ---------- Gedung Paris kanan (oranye, banyak jendela) + kiri jauh ----------
def building(name, loc, scale, bmat):
    box(name, loc, scale, bmat)
    # jendela di sisi menghadap jalan (sisi -x untuk gedung kanan)
    x_face = loc[0] - scale[0] - 0.05
    for rz in range(4):
        for ry in range(3):
            r = random.random()
            wm = win_warm if r < 0.45 else (win_cool if r < 0.65 else win_off)
            box(f"{name}_Win_{rz}_{ry}",
                (x_face, loc[1] - scale[1] + 1.2 + ry * 1.6, 1.6 + rz * 2.0),
                (0.05, 0.55, 0.75), wm)
building("BldgR1", (12.5, 2, 5.0), (2.5, 4.0, 5.0), bldg_orange)
building("BldgR2", (13.0, 10, 6.0), (2.5, 3.5, 6.0), bldg_orange)
building("BldgR3", (12.0, -8, 4.0), (2.5, 3.5, 4.0), bldg_blue)
building("BldgL1", (-14.0, 14, 4.5), (2.5, 4.0, 4.5), bldg_blue)

# ---------- Pohon, lampu, bangku, bendera ----------
for tx, ty in [(-8.5, -2), (-10.5, 6), (-8.0, 12)]:
    cyl(f"Trunk_{tx}_{ty}", (tx, ty, 1.0), 0.25, 2.0, trunk_mat)
    sphere(f"Tree_{tx}_{ty}_a", (tx, ty, 2.8), 1.4, tree_mat, scale=(1, 1, 0.85))
    sphere(f"Tree_{tx}_{ty}_b", (tx - 0.8, ty, 2.2), 0.9, tree_mat, scale=(1, 1, 0.85))
    sphere(f"Tree_{tx}_{ty}_c", (tx + 0.8, ty, 2.2), 0.9, tree_mat, scale=(1, 1, 0.85))
for lx, ly in [(-3.6, -12), (3.6, -4), (-3.6, 4), (3.6, 12)]:
    cyl(f"Lamp_{lx}_{ly}", (lx, ly, 1.3), 0.09, 2.6, lamp_mat)
    box(f"LampHead_{lx}_{ly}", (lx, ly, 2.7), (0.25, 0.25, 0.35), lamp_glow)
for bx, by, br in [(-5.5, 2, 0), (5.5, -8, 0)]:
    box(f"Bench_{bx}_{by}", (bx, by, 0.45), (1.1, 0.35, 0.08), lamp_mat)
    box(f"BenchBack_{bx}_{by}", (bx, by + 0.35, 0.8), (1.1, 0.06, 0.4), lamp_mat)
flags = []
for fx, fy in [(-6.5, -1), (6.5, -1)]:
    cyl(f"FlagPole_{fx}_{fy}", (fx, fy, 1.8), 0.06, 3.6, lamp_mat)
    flag = box(f"Flag_{fx}_{fy}", (fx + 0.7, fy, 3.2), (0.65, 0.03, 0.35), flag_white)
    box(f"FlagB_{fx}_{fy}", (fx + 0.25, fy, 3.2), (0.2, 0.035, 0.35), flag_blue)
    box(f"FlagR_{fx}_{fy}", (fx + 1.15, fy, 3.2), (0.2, 0.035, 0.35), flag_red)
    flags.append(flag)
    # Berkibar: rotasi kecil bolak-balik (motion_design: sine ease)
    for f, deg in ((1, 0), (12, 7), (23, -7), (34, 7), (45, -7), (56, 7),
                   (67, -7), (78, 7), (90, 0)):
        flag.rotation_euler = (0, 0, math.radians(deg))
        flag.keyframe_insert("rotation_euler", frame=f)

# ---------- Karakter bean-head ----------
def walker(name, loc, suit, hat=False, scale_h=1.0):
    """Karakter stylized kepala bulat besar (bean-head), badan kecil."""
    parts = {}
    # kaki
    for side, sx in (("L", -0.12), ("R", 0.12)):
        leg = box(f"{name}_Leg{side}", (loc[0] + sx, loc[1], 0.4 * scale_h),
                  (0.09, 0.09, 0.4 * scale_h), suit)
        # pivot di pinggul: pindahkan origin lewat keyframe rotasi di bawah
        parts[f"leg{side}"] = leg
    body = box(f"{name}_Body", (loc[0], loc[1], 0.95 * scale_h),
               (0.28, 0.18, 0.35 * scale_h), suit)
    parts["body"] = body
    # lengan
    for side, sx in (("L", -0.32), ("R", 0.32)):
        arm = box(f"{name}_Arm{side}", (loc[0] + sx, loc[1], 0.95 * scale_h),
                  (0.07, 0.07, 0.3 * scale_h), suit)
        parts[f"arm{side}"] = arm
    # kepala bean-head besar
    head = sphere(f"{name}_Head", (loc[0], loc[1], 1.55 * scale_h), 0.32 * scale_h,
                  skin_mat, scale=(1.12, 1.0, 1.05))
    parts["head"] = head
    if hat:
        cyl(f"{name}_Hat", (loc[0], loc[1], 1.88 * scale_h), 0.20 * scale_h,
            0.30 * scale_h, hat_mat)
        cyl(f"{name}_HatBrim", (loc[0], loc[1], 1.74 * scale_h), 0.30 * scale_h,
            0.04 * scale_h, hat_mat)
        parts["hat"] = bpy.data.objects[f"{name}_Hat"]
        parts["hatbrim"] = bpy.data.objects[f"{name}_HatBrim"]
    return parts

def walk_cycle(parts, start_loc, end_loc, frames=(1, 90), bob=True):
    """Jalan: kaki bergantian (Disney: kaki kanan lalu kiri, bukan bareng),
    lengan berlawanan, badan bob kecil, topi follow-through.
    SEMUA bagian ikut berpindah dari start ke end (offset tiap bagian
    dihitung dari posisi awalnya), supaya kaki tidak tertinggal."""
    f0, f1 = frames
    # Semua bagian bergerak bersama: offset = posisi awal - start_loc
    for o in parts.values():
        off = (o.location.x - start_loc[0], o.location.y - start_loc[1],
               o.location.z - start_loc[2])
        key_loc(o, [(f0, (start_loc[0] + off[0], start_loc[1] + off[1],
                          start_loc[2] + off[2])),
                    (f1, (end_loc[0] + off[0], end_loc[1] + off[1],
                          end_loc[2] + off[2]))],
                interp='LINEAR')
    # kaki: rotasi bergantian tiap 11 frame (langkah ~0,37 dtk)
    for f in range(f0, f1 + 1, 11):
        phase = ((f - f0) // 11) % 2
        a = 26 if phase == 0 else -26
        for leg, ang in ((parts["legL"], a), (parts["legR"], -a)):
            leg.rotation_euler = (math.radians(ang), 0, 0)
            leg.keyframe_insert("rotation_euler", frame=f)
        for arm, ang in ((parts["armL"], -a), (parts["armR"], a)):
            arm.rotation_euler = (math.radians(ang * 0.7), 0, 0)
            arm.keyframe_insert("rotation_euler", frame=f)
    # Bob badan dihapus: walk cycle kaki + lengan sudah memberi gerak.

# Lustig hero: berjalan ke arah kamera (y -8 -> -13), sedikit ke kanan
lustig = walker("Lustig", (1.8, -8, 0), suit_mat, hat=True, scale_h=1.0)
walk_cycle(lustig, (1.8, -8, 0), (2.6, -13, 0))
# 3 pejalan kaki latar, berjalan pelan menyamping
for i, (sx, sy, ex) in enumerate([(-4.0, 3, -1.5), (0.5, 6, 3.0), (4.5, 1, 6.5)]):
    w = walker(f"Walker{i}", (sx, sy, 0), suit_mat if i % 2 == 0 else lamp_mat,
               hat=(i == 1), scale_h=0.95)
    walk_cycle(w, (sx, sy, 0), (ex, sy + 1.5, 0), bob=False)

# ---------- Cahaya senja ----------
world = bpy.data.worlds["World"]
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.88, 0.48, 0.32, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 1.0

def light(name, ltype, loc, energy, color=(1, 1, 1, 1), rot=None):
    ld = bpy.data.lights.new(name, type=ltype)
    ld.energy = energy
    ld.color = color[:3]
    o = bpy.data.objects.new(name, ld)
    o.location = loc
    if rot:
        o.rotation_euler = rot
    col.objects.link(o)
    return o
# Matahari rendah dari kiri (seperti referensi: matahari di kiri bawah)
light("SunLight", 'SUN', (0, 0, 10), 5.0, color=(1.0, 0.62, 0.35, 1),
      rot=(math.radians(62), 0, math.radians(-28)))
light("FillWarm", 'POINT', (0, -10, 4), 80, color=(1.0, 0.65, 0.4, 1))
light("FillCool", 'POINT', (0, 6, 6), 50, color=(0.6, 0.65, 1.0, 1))

# ---------- Kamera: dolly-in pelan (smootherstep), Track To menara ----------
cam_data = bpy.data.cameras.new("Lustig_Cam")
cam_data.lens = 22
cam = bpy.data.objects.new("Lustig_Cam", cam_data)
col.objects.link(cam)
sc.camera = cam
tower_target = bpy.data.objects.new("TowerTarget", None)
tower_target.location = (0, 0, 13)
col.objects.link(tower_target)
track = cam.constraints.new('TRACK_TO')
track.target = tower_target
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'
# Dolly-in ease: posisi awal jauh, akhir lebih dekat dan sedikit naik
key_loc(cam, [(1, (0, -25, 3.2)), (45, (0, -23.8, 3.7)), (90, (0, -22.5, 4.2))])

bpy.ops.wm.save_as_mainfile(filepath=BLEND)
print("BUILD LUSTIG OK engine=%s res=%sx%s frames=%s-%s fps=%s" % (
    sc.render.engine, sc.render.resolution_x, sc.render.resolution_y,
    sc.frame_start, sc.frame_end, sc.render.fps))
for f in (1, 45, 90):
    sc.frame_set(f)
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    l = bpy.data.objects["Lustig_Body"].evaluated_get(dg)
    c = cam.evaluated_get(dg)
    print("CHECK frame=%d lustig=%s cam=%s" % (
        f, tuple(round(v, 2) for v in l.matrix_world.translation),
        tuple(round(v, 2) for v in c.matrix_world.translation)))
