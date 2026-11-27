# build_test_v2.py - perbaikan cacat build_test.py kandidat 3 (mromidev blender-film)
# Perubahan vs v1:
#  1. Drone TIDAK lagi pakai Follow Path constraint (itu yang macet di (0,-22,2.0)
#     saat render: offset_factor keyframe tidak dievaluasi depsgraph headless).
#     Gerakan diganti keyframe lokasi langsung di titik path yang sama
#     (y -22 -> 22, z 2.0 -> 3.5, 90 frame = 3 detik), interpolasi BEZIER.
#  2. LED dan rotor di-parent ke drone (parent + matrix_parent_inverse),
#     jadi ikut drone, bukan tertinggal di posisi awal.
#  3. Drone diperbesar (1.6 m) dan kamera didekatkan (offset -4.5, +1.0)
#     + Track To ke drone, supaya drone kelihatan di tengah frame.
#  4. Aspal roughness 0.15 -> 0.8 dan lampu 150 -> 80, supaya pantulan
#     specular lampu tidak lagi jadi kotak terang besar di bawah frame.
#  5. Frame 1-90 (3 detik), 1080x1920, 30 fps, EEVEE_NEXT 16 sample, AgX.
# Prinsip skill tetap: storyboard 1 shot, practical lights, AgX tanpa grade.
import bpy, math, os, random

D = os.path.dirname(os.path.abspath(__file__))
BLEND = os.path.join(D, "scene_v2.blend")
OUTDIR = os.path.join(D, "renders_v2")
os.makedirs(OUTDIR, exist_ok=True)

# Bersihkan scene default
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

col = bpy.data.collections.new("BF_Test")
sc.collection.children.link(col)

def mat(name, base, rough=0.5, metal=0.0, emit=None, strength=0.0, spec=0.5):
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

def box(name, loc, scale, material):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = scale
    if material:
        o.data.materials.append(material)
    try:
        sc.collection.objects.unlink(o)
    except RuntimeError:
        pass
    if o.name not in col.objects:
        col.objects.link(o)
    return o

# Jalan aspal: matte, bukan glossy (perbaikan #4)
road = box("BF_Road", (0, 0, -0.1), (4, 30, 0.1),
           mat("BF_Asphalt", (0.02, 0.02, 0.03, 1), rough=0.8, metal=0.0, spec=0.2))

random.seed(7)
win_warm = mat("BF_WinWarm", (0.1, 0.08, 0.05, 1), emit=(1.0, 0.6, 0.25, 1), strength=4.0)
win_cool = mat("BF_WinCool", (0.05, 0.08, 0.1, 1), emit=(0.5, 0.75, 1.0, 1), strength=3.0)
win_off = mat("BF_WinOff", (0.03, 0.03, 0.04, 1), rough=0.9)
bldg = mat("BF_Building", (0.08, 0.08, 0.10, 1), rough=0.85)
for side in (-1, 1):
    for i, y in enumerate(range(-24, 25, 8)):
        h = 6 + (i % 3) * 3
        box(f"BF_Bldg_{'L' if side < 0 else 'R'}{i}", (side * 7, y, h / 2 - 0.2),
            (2.5, 3.5, h / 2), bldg)
        for cx in range(3):
            for rz in range(4):
                r = random.random()
                wm = win_warm if r < 0.35 else (win_cool if r < 0.55 else win_off)
                box(f"BF_Win_{'L' if side < 0 else 'R'}{i}_{cx}_{rz}",
                    (side * 4.6, y - 2 + cx * 2, 1.5 + rz * 2.2),
                    (0.05, 0.7, 0.8), wm)

# Path curve tetap ada sebagai panduan visual (tidak dipakai constraint)
curve_data = bpy.data.curves.new("BF_Path", type='CURVE')
curve_data.dimensions = '3D'
spline = curve_data.splines.new('BEZIER')
spline.bezier_points.add(3)
pts = [(0, -22, 2.0), (0, -8, 3.0), (0, 8, 2.5), (0, 22, 3.5)]
for bp, co in zip(spline.bezier_points, pts):
    bp.co = co
    bp.handle_left_type = 'AUTO'
    bp.handle_right_type = 'AUTO'
path_obj = bpy.data.objects.new("BF_Path", curve_data)
col.objects.link(path_obj)

# Hero drone, diperbesar (perbaikan #3): 1.6 x 1.6 x 0.36 m
# Bodi v2b: abu terang (bukan 0.05 hitam) supaya kena lampu, plus panel
# emissive cyan di atas supaya siluet drone terbaca di malam hari.
drone_mat = mat("BF_Drone", (0.35, 0.36, 0.40, 1), rough=0.6, metal=0.2)
drone_top_mat = mat("BF_DroneTop", (0, 0, 0, 1), emit=(0.0, 1.0, 1.0, 1), strength=5.0)
led_c = mat("BF_LED_Cyan", (0, 0, 0, 1), emit=(0.0, 1.0, 1.0, 1), strength=8.0)
led_m = mat("BF_LED_Magenta", (0, 0, 0, 1), emit=(1.0, 0.0, 0.8, 1), strength=8.0)
drone = box("BF_Drone", (0, -22, 2.0), (0.8, 0.8, 0.18), drone_mat)
drone_top = box("BF_DroneTop", (0, -22, 2.0), (0.5, 0.5, 0.02), drone_top_mat)
# LED / rotor TIDAK di-parent (parenting manual gagal di headless, lihat CHECK
# v2 pertama: LED di (0,0.67,4.77) dan bergerak 2x drone). Sebagai gantinya
# lokasi mereka di-keyframe mengikuti drone dengan offset tetap (perbaikan #2).
led_f = box("BF_LED_F", (0, -21.4, 2.0), (0.4, 0.05, 0.05), led_c)
led_b = box("BF_LED_B", (0, -22.6, 2.0), (0.4, 0.05, 0.05), led_m)
rotors = []
for sx, sy in ((0.7, 0.7), (-0.7, 0.7), (0.7, -0.7), (-0.7, -0.7)):
    rotors.append((sx, sy, box(f"BF_Rotor_{sx}_{sy}", (sx, -22 + sy, 2.15),
                               (0.3, 0.3, 0.03), drone_mat)))

# Gerakan drone: keyframe lokasi langsung (perbaikan #1), 90 frame
drone_path = [(1, (0, -22, 2.0)), (30, (0.5, -7.3, 2.7)),
              (60, (-0.5, 7.3, 2.8)), (90, (0, 22, 3.5))]
for f, loc in drone_path:
    drone.location = loc
    drone.keyframe_insert("location", frame=f)
for fc in drone.animation_data.action.fcurves:
    if fc.data_path == "location":
        for kp in fc.keyframe_points:
            kp.interpolation = 'BEZIER'
# LED / rotor mengikuti drone (offset tetap, keyframe yang sama)
followers = [(led_f, (0, 0.6, 0)), (led_b, (0, -0.6, 0)),
             (drone_top, (0, 0, 0.2))]
for sx, sy, o in rotors:
    followers.append((o, (sx, sy, 0.15)))
for f, loc in drone_path:
    for obj, off in followers:
        obj.location = (loc[0] + off[0], loc[1] + off[1], loc[2] + off[2])
        obj.keyframe_insert("location", frame=f)
    for obj, off in followers:
        for fc in obj.animation_data.action.fcurves:
            if fc.data_path == "location":
                for kp in fc.keyframe_points:
                    kp.interpolation = 'BEZIER'
# Attitude miring ke depan
for f, deg in ((1, 12), (45, 18), (90, 8)):
    drone.rotation_euler = (math.radians(deg), 0, 0)
    drone.keyframe_insert("rotation_euler", frame=f)

# World gelap, tapi sedikit diterangkan supaya gedung/jalan tidak hitam pekat
world = bpy.data.worlds["World"]
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.005, 0.006, 0.012, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.5

# Practical lights, energi diturunkan 150 -> 80 (perbaikan #4)
def light(name, ltype, loc, energy, color=(1, 1, 1, 1)):
    ld = bpy.data.lights.new(name, type=ltype)
    ld.energy = energy
    ld.color = color[:3]
    o = bpy.data.objects.new(name, ld)
    o.location = loc
    col.objects.link(o)
    return o
for i, y in enumerate(range(-20, 25, 10)):
    side = -1 if i % 2 == 0 else 1
    light(f"BF_Lamp{i}", 'POINT', (side * 3.2, y, 4.5), 120,
          color=(1.0, 0.72, 0.42, 1))

# Fill light yang mengikuti drone dari belakang-atas (sisi kamera), supaya
# bodi drone yang menghadap kamera tidak hitam pekat. Keyframe ikut drone.
fill = light("BF_Fill", 'POINT', (0, -24, 4.0), 60, color=(0.9, 0.95, 1.0, 1))
for f, loc in drone_path:
    fill.location = (loc[0], loc[1] - 2.0, loc[2] + 2.0)
    fill.keyframe_insert("location", frame=f)

# Kamera chase: Track To ke drone, posisi keyframe mengikuti drone -4.5 / +1.0
cam_data = bpy.data.cameras.new("BF_Cam")
cam_data.lens = 35
cam = bpy.data.objects.new("BF_Cam", cam_data)
col.objects.link(cam)
sc.camera = cam
track = cam.constraints.new('TRACK_TO')
track.target = drone
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'
for f, loc in drone_path:
    cam.location = (loc[0], loc[1] - 8.0, loc[2] + 2.0)
    cam.keyframe_insert("location", frame=f)
for fc in cam.animation_data.action.fcurves:
    if fc.data_path == "location":
        for kp in fc.keyframe_points:
            kp.interpolation = 'BEZIER'

bpy.ops.wm.save_as_mainfile(filepath=BLEND)
print("BUILD V2 OK engine=%s res=%sx%s frames=%s-%s fps=%s" % (
    sc.render.engine, sc.render.resolution_x, sc.render.resolution_y,
    sc.frame_start, sc.frame_end, sc.render.fps))

# Verifikasi depsgraph: drone + LED harus bergerak dan LED ikut drone
import mathutils
for f in (1, 45, 90):
    sc.frame_set(f)
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    d_eval = drone.evaluated_get(dg)
    led = bpy.data.objects["BF_LED_F"].evaluated_get(dg)
    cam_eval = cam.evaluated_get(dg)
    print("CHECK frame=%d drone=%s led_f=%s cam=%s" % (
        f, tuple(round(v, 2) for v in d_eval.matrix_world.translation),
        tuple(round(v, 2) for v in led.matrix_world.translation),
        tuple(round(v, 2) for v in cam_eval.matrix_world.translation)))
