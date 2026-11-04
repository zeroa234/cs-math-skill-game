"""宣传片开场 / 片尾的像素 3D 镜头（Blender 5.2，Eevee + 合成器雾和 Bloom）：“我的远征”的关卡沿一座星图学院的塔盘旋而上。

几何全部来自游戏数据，不手摆（src/promo/public/build/facts.json，scripts/promo/build-facts.mjs 从 src/gen/ 算出）：
- 关卡 = 我的远征 5 站的每一课（124 个圆台）+ 每站最后的结业挑战（5 个方形大台），顺序和游戏里的路线一样，
  按等弧长排在一条往上收的螺旋上；颜色 = 这一站技能所在领域的颜色（游戏里关卡的颜色也是它）。站与站之间空出一段。
- 每站的结业挑战旁边一根水晶；塔顶一颗大水晶 = 终点“操作系统”。塔是一圈圈方块，几扇窗随机亮着（固定种子）。
画法：渲 640×360（像素密度和游戏 480×270 的像素背景同一档），不抗锯齿（filter_size 0）；之后 scripts/promo/render-blender.sh
用一套固定调色板量化（无抖动）、最近邻放大 3 倍到 1920×1080，就是像素画。
动画时刻读 src/promo/public/build/timeline.json / words.json（旁白时间轴），画面跟着旁白走：
- intro：cold + hook 两拍里关卡从第 1 课起一个个亮起，镜头跟着往上盘；说到“点亮之路”时塔顶水晶亮；
- outro：说到“一路点亮”时整条路从下往上变成“已点亮”的金色（游戏深色主题的 --lit #f2bd3a）。

用法（项目根目录）：
  blender -b --factory-startup -P scripts/promo/blender-route.py -- --shot intro --out temp/promo/blender/intro [--samples 16] [--frames 0,120,300]
--frames 只渲这几帧（试看用）；不给就渲整段。--res 640x360 可改分辨率（封面用更高的）。
"""
import argparse
import json
import math
import random
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
FPS = 30


def hexc(h, a=1.0):
    h = h.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return (*[c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb], a)


def lighten(h, t):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    return "#" + "".join(f"{round(v + (255 - v) * t):02x}" for v in c)


def smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


# ── 数据 ─────────────────────────────────────────────────
facts = json.loads((ROOT / "src/promo/public/build/facts.json").read_text(encoding="utf-8"))
tl = json.loads((ROOT / "src/promo/public/build/timeline.json").read_text(encoding="utf-8"))
words = json.loads((ROOT / "src/promo/public/build/words.json").read_text(encoding="utf-8"))
BEAT = {b["id"]: b for b in tl["beats"]}
STOPS = facts["route"]["stops"]
GOLD, LOCKED = "#f2bd3a", "#2a2a50"


def w(beat, word):
    """旁白说到 word 的那一帧（和 src/promo/src/lib/core.ts 的 w() 一样）"""
    for s in words[beat]:
        i = s["text"].find(word)
        if i < 0:
            continue
        hit = next((x for x in s["words"] if x[0] <= i < x[0] + x[1]), None) or min(s["words"], key=lambda x: abs(x[0] - i))
        return hit[2]
    raise SystemExit(f"旁白里没有“{word}”（拍 {beat}）")


# 关卡序列：每站 n 课 + 1 个结业挑战；站与站之间空 GAP 个关卡的距离
GAP = 1.6
seq = []
for si, st in enumerate(STOPS):
    for k in range(st["lessons"]):
        seq.append({"stop": si, "boss": False, "k": k})
    seq.append({"stop": si, "boss": True, "k": st["lessons"]})
N = len(seq)
pos_u = []
u = 0.0
for i, s in enumerate(seq):
    if i and seq[i - 1]["stop"] != s["stop"]:
        u += GAP
    pos_u.append(u)
    u += 1.0
U = pos_u[-1]

# 螺旋：半径从 R0 收到 R1，高度 0 → H，转 TURNS 圈；按弧长均匀取点（先密采样再插值）
R0, R1, H, TURNS, TH0 = 9.0, 4.6, 13.5, 2.35, math.radians(-100)


def helix(t):
    r = R0 + (R1 - R0) * t
    a = TH0 + TURNS * 2 * math.pi * t
    return Vector((math.cos(a) * r, math.sin(a) * r, H * t)), a, r


samples = [helix(i / 4000)[0] for i in range(4001)]
arc = [0.0]
for i in range(1, len(samples)):
    arc.append(arc[-1] + (samples[i] - samples[i - 1]).length)


def at_arc(frac):
    target = frac * arc[-1]
    lo, hi = 0, len(arc) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if arc[mid] < target:
            lo = mid
        else:
            hi = mid
    t = (lo + (target - arc[lo]) / max(1e-9, arc[hi] - arc[lo])) / 4000
    return helix(t)


TILES = []
for i, s in enumerate(seq):
    p, a, r = at_arc(pos_u[i] / U)
    TILES.append({**s, "p": p, "a": a, "r": r, "color": lighten(STOPS[s["stop"]]["color"], 0.1)})


# ── 场景 ─────────────────────────────────────────────────
def setup(samples, res):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.fps = FPS
    sc.render.filter_size = 0.0                     # 不抗锯齿：边缘是硬的像素
    sc.eevee.taa_render_samples = samples
    sc.view_settings.view_transform = "Standard"
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    wd = bpy.data.worlds.new("world")
    wd.use_nodes = True
    nt = wd.node_tree
    bg = nt.nodes["Background"]
    # 天空：下面深紫、上面更深（游戏开场 title.png 的夜空色）
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = hexc("#2a1d5e")
    ramp.color_ramp.elements[1].position = 0.55
    ramp.color_ramp.elements[1].color = hexc("#0e0d24")
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = 1.4
    sc.world = wd
    wd.mist_settings.start, wd.mist_settings.depth = 24.0, 70.0
    vl = sc.view_layers[0]
    vl.use_pass_mist = True
    # 合成器：按雾的深度往夜空色混，再 Bloom
    ng = bpy.data.node_groups.new("comp", "CompositorNodeTree")
    ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    rl = ng.nodes.new("CompositorNodeRLayers")
    mix = ng.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs["B"].default_value = hexc("#1b1640")
    mul = ng.nodes.new("ShaderNodeMath")
    mul.operation = "MULTIPLY"
    mul.inputs[1].default_value = 0.6
    gl = ng.nodes.new("CompositorNodeGlare")
    gl.inputs["Type"].default_value = "Bloom"
    gl.inputs["Threshold"].default_value = 0.9
    gl.inputs["Strength"].default_value = 0.5
    gl.inputs["Size"].default_value = 0.7
    out = ng.nodes.new("NodeGroupOutput")
    ng.links.new(rl.outputs["Mist"], mul.inputs[0])
    ng.links.new(mul.outputs[0], mix.inputs["Factor"])
    ng.links.new(rl.outputs["Image"], mix.inputs["A"])
    ng.links.new(mix.outputs["Result"], gl.inputs["Image"])
    ng.links.new(gl.outputs["Image"], out.inputs[0])
    sc.compositing_node_group = ng
    sc.render.use_compositing = True
    return sc


def obj_color_mat(name, base, emit_strength):
    """底色 base 的漫反射 + 发光（颜色 / 亮度从物体颜色 Object Info 的 Color / Alpha 取，每个物体自己打关键帧）"""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    oi = nt.nodes.new("ShaderNodeObjectInfo")
    bs = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bs.inputs["Base Color"].default_value = hexc(base)
    bs.inputs["Roughness"].default_value = 0.9
    mul = nt.nodes.new("ShaderNodeMath")
    mul.operation = "MULTIPLY"
    mul.inputs[1].default_value = emit_strength
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(oi.outputs["Color"], bs.inputs["Emission Color"])
    nt.links.new(oi.outputs["Alpha"], mul.inputs[0])
    nt.links.new(mul.outputs[0], bs.inputs["Emission Strength"])
    nt.links.new(bs.outputs[0], out.inputs["Surface"])
    return m


def flat_mat(name, color, emit=0.0, emit_color=None):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bs = m.node_tree.nodes["Principled BSDF"]
    bs.inputs["Base Color"].default_value = hexc(color)
    bs.inputs["Roughness"].default_value = 0.95
    if emit:
        bs.inputs["Emission Color"].default_value = hexc(emit_color or color)
        bs.inputs["Emission Strength"].default_value = emit
    return m


def key_color(ob, frame, hexcol, alpha):
    ob.color = hexc(hexcol, alpha)
    ob.keyframe_insert("color", frame=frame)


def cubes_mesh(name, boxes, mat_slots):
    """boxes: [(中心, 尺寸, 材质序号), ...] → 一个网格（几千个方块一个物体）"""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    for c, size, mi in boxes:
        r = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=size, verts=r["verts"])
        bmesh.ops.translate(bm, vec=c, verts=r["verts"])
        for f in {f for v in r["verts"] for f in v.link_faces}:
            f.material_index = mi
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    for m in mat_slots:
        me.materials.append(m)
    return ob


def build():
    rnd = random.Random(20261104)
    # 塔：每层一圈方块，半径跟着螺旋往上收（比关卡所在半径小 1.5），窗户随机亮
    VOX = 0.5
    stone, stone2, window = flat_mat("stone", "#4d4688"), flat_mat("stone2", "#3b3670"), flat_mat("window", "#f6c86a", emit=1.6)
    boxes = []
    layers = int((H + 2.5) / VOX)
    for L in range(-6, layers):
        z = L * VOX + VOX / 2
        t = max(0.0, min(1.0, z / H))
        rt = R0 + (R1 - R0) * t - 1.5 if z < H + 0.6 else 1.6
        n = max(8, int(2 * math.pi * rt / VOX))
        for k in range(n):
            a = 2 * math.pi * k / n
            mi = 2 if (L % 3 == 1 and rnd.random() < 0.035 and 0 < z < H) else (0 if (k + L) % 2 else 1)
            boxes.append((Vector((math.cos(a) * rt, math.sin(a) * rt, z)), Vector((VOX, VOX, VOX)), mi))
    # 塔顶平台
    for x in range(-4, 5):
        for y in range(-4, 5):
            if x * x + y * y <= 16:
                boxes.append((Vector((x * VOX, y * VOX, H + 0.75)), Vector((VOX, VOX, VOX * 0.5)), 1))
    # 关卡下面的托架：从塔身伸出来的一块方块
    for tile in TILES:
        a, r = tile["a"], tile["r"]
        for d in (0.0, 0.5, 1.0):
            rr = r - d
            boxes.append((Vector((math.cos(a) * rr, math.sin(a) * rr, tile["p"].z - 0.22)), Vector((0.55, 0.55, 0.28)), 1))
    cubes_mesh("tower", boxes, [stone, stone2, window])

    # 地面：一圈起伏的方块，越远越暗（雾）
    gboxes = []
    for x in range(-34, 35):
        for y in range(-34, 35):
            d = math.hypot(x, y)
            if d < 18 or d > 34:
                continue
            h = 0.35 * math.sin(x * 0.45) * math.cos(y * 0.38) + 0.25 * rnd.random() + max(0, (d - 18)) * 0.05
            gboxes.append((Vector((x * 1.0, y * 1.0, -3.0 + round(h * 2) / 2)), Vector((1.0, 1.0, 1.0)), (x + y) % 2))
    for x in range(-18, 19):
        for y in range(-18, 19):
            if math.hypot(x, y) < 18:
                gboxes.append((Vector((x * 1.0, y * 1.0, -3.0)), Vector((1.0, 1.0, 1.0)), (x + y) % 2))
    cubes_mesh("ground", gboxes, [flat_mat("grass", "#1b3a3e"), flat_mat("grass2", "#173236")])

    # 关卡：课 = 八边形圆台（游戏里关卡是像素圆）；结业挑战 = 方台
    tile_mat = obj_color_mat("tile", LOCKED, 2.2)
    obs = []
    for tile in TILES:
        if tile["boss"]:
            bpy.ops.mesh.primitive_cube_add(size=1.0, location=tile["p"])
            ob = bpy.context.active_object
            ob.scale = (0.82, 0.82, 0.24)
            ob.rotation_euler = (0, 0, tile["a"] + math.pi / 4)
        else:
            bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.33, depth=0.18, location=tile["p"])
            ob = bpy.context.active_object
            ob.rotation_euler = (0, 0, math.pi / 8)
        ob.data.materials.append(tile_mat)
        obs.append(ob)
    # 每站一根水晶（结业挑战外侧）+ 塔顶大水晶
    crystals = []
    for tile in TILES:
        if not tile["boss"]:
            continue
        out = Vector((math.cos(tile["a"]), math.sin(tile["a"]), 0))
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.32, radius2=0.0, depth=0.9, location=tile["p"] + out * 0.9 + Vector((0, 0, 0.75)))
        top = bpy.context.active_object
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.32, radius2=0.0, depth=0.45, location=tile["p"] + out * 0.9 + Vector((0, 0, 0.075)), rotation=(math.pi, 0, 0))
        bot = bpy.context.active_object
        for o in (top, bot):
            o.data.materials.append(tile_mat)
        crystals.append((tile, [top, bot]))
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.95, radius2=0.0, depth=2.4, location=(0, 0, H + 2.4))
    sum_top = bpy.context.active_object
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.95, radius2=0.0, depth=1.2, location=(0, 0, H + 0.6), rotation=(math.pi, 0, 0))
    sum_bot = bpy.context.active_object
    for o in (sum_top, sum_bot):
        o.data.materials.append(tile_mat)
    summit = [sum_top, sum_bot]
    sl = bpy.data.lights.new("summit", "POINT")
    sl.color = hexc(GOLD)[:3]
    sl.shadow_soft_size = 0.5
    slo = bpy.data.objects.new("summit-light", sl)
    slo.location = (0, 0, H + 2.0)
    bpy.context.scene.collection.objects.link(slo)

    # 星星：天上的小方块（像素星）
    star_mat = obj_color_mat("star", "#000000", 3.0)
    me = bpy.data.meshes.new("stars")
    bm = bmesh.new()
    for _ in range(520):
        d = Vector((rnd.gauss(0, 1), rnd.gauss(0, 1), abs(rnd.gauss(0, 0.8)) + 0.15)).normalized() * rnd.uniform(70, 95)
        s = rnd.choice([0.18, 0.18, 0.28, 0.4])
        r = bmesh.ops.create_cube(bm, size=s)
        bmesh.ops.translate(bm, vec=d + Vector((0, 0, 4)), verts=r["verts"])
    bm.to_mesh(me)
    bm.free()
    stars = bpy.data.objects.new("stars", me)
    bpy.context.scene.collection.objects.link(stars)
    me.materials.append(star_mat)

    # 月光 + 一点环境补光，塔身能看出方块
    sun = bpy.data.lights.new("moon", "SUN")
    sun.energy = 2.4
    sun.color = hexc("#9fb0ff")[:3]
    so = bpy.data.objects.new("moon", sun)
    so.rotation_euler = (math.radians(55), 0, math.radians(35))
    bpy.context.scene.collection.objects.link(so)
    return obs, crystals, summit, sl, stars


def camera(path, target_path, lens=32):
    cam_data = bpy.data.cameras.new("cam")
    cam_data.lens = lens
    cam_data.clip_end = 400
    cam = bpy.data.objects.new("cam", cam_data)
    bpy.context.scene.collection.objects.link(cam)
    tgt = bpy.data.objects.new("target", None)
    bpy.context.scene.collection.objects.link(tgt)
    for f, p in path:
        cam.location = p
        cam.keyframe_insert("location", frame=f)
    for f, p in target_path:
        tgt.location = p
        tgt.keyframe_insert("location", frame=f)
    c = cam.constraints.new("TRACK_TO")
    c.target = tgt
    c.track_axis, c.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"
    bpy.context.scene.camera = cam
    return cam


def orbit(f, r, ang_deg, z):
    a = math.radians(ang_deg)
    return (f, (math.cos(a) * r, math.sin(a) * r, z))


def side(ang_deg, z, d):
    """镜头在 ang_deg 方位时，注视点往镜头左手边挪 d：塔落在画面右边，左边留给字"""
    a = math.radians(ang_deg)
    return (math.sin(a) * d, -math.cos(a) * d, z)


def light_tile(ob, t, col, boss=False):
    s0 = ob.scale.copy()
    ob.keyframe_insert("scale", frame=t - 1)
    ob.scale = s0 * (1.5 if boss else 1.35)
    ob.keyframe_insert("scale", frame=t + 4)
    ob.scale = s0
    ob.keyframe_insert("scale", frame=t + 12)
    key_color(ob, t - 1, col, 0.0)
    key_color(ob, t + 3, "#ffffff", 1.4)
    key_color(ob, t + 14, col, 0.75)


# ── 两个镜头 ─────────────────────────────────────────────
def deg(a):
    return math.degrees(a)


def shot_intro(obs, crystals, summit, sl, stars):
    end = BEAT["title"]["end"]
    t_sum = w("title", "点亮之路")
    first, last = 14, BEAT["hook"]["speech"][-1]["end"] + 6
    # 关卡按序号亮起：前面慢（看得清一个个亮），后面越来越快（时刻 ∝ 序号^0.62）
    t_of = [round(first + (last - first) * ((i / (N - 1)) ** 0.62)) for i in range(N)]
    for i, (ob, tile) in enumerate(zip(obs, TILES)):
        key_color(ob, 0, tile["color"], 0.0)
        light_tile(ob, t_of[i], tile["color"], tile["boss"])
    idx = {id(t): i for i, t in enumerate(TILES)}
    for tile, parts in crystals:
        t = t_of[idx[id(tile)]] + 3
        for o in parts:
            key_color(o, 0, tile["color"], 0.15)
            key_color(o, t, tile["color"], 0.15)
            key_color(o, t + 5, "#ffffff", 2.2)
            key_color(o, t + 18, tile["color"], 1.3)
    for o in summit:
        key_color(o, 0, GOLD, 0.1)
        key_color(o, t_sum - 2, GOLD, 0.1)
        key_color(o, t_sum + 5, "#fff6d8", 3.0)
        key_color(o, t_sum + 24, GOLD, 1.6)
    sl.energy = 0
    sl.keyframe_insert("energy", frame=t_sum - 2)
    sl.energy = 900
    sl.keyframe_insert("energy", frame=t_sum + 8)
    sl.energy = 450
    sl.keyframe_insert("energy", frame=t_sum + 30)
    key_color(stars, 0, "#cfd8ff", 0.0)
    key_color(stars, 50, "#cfd8ff", 0.7)
    a0 = deg(TILES[0]["a"])
    # 镜头：从塔脚第 1 课外侧的低处起，绕塔往上升、拉远，塔一直在画面右边（左边是旁白的大字）
    i10 = t_of[10]
    i64 = t_of[N // 2]
    p0 = TILES[0]["p"]
    camera([orbit(0, 15.5, a0 - 12, 1.4), orbit(i10, 19.0, a0 + 2, 3.0), orbit(i64, 24.0, a0 + 50, 7.0),
            orbit(last, 31.0, a0 + 100, 12.0), orbit(end, 34.0, a0 + 115, 12.5)],
           [(0, (p0.x * 0.8, p0.y * 0.8, 0.9)), (i10, (p0.x * 0.45, p0.y * 0.45, 2.2)), (i64, side(a0 + 50, 3.6, 4.6)),
            (last, side(a0 + 100, 7.2, 6.6)), (end, side(a0 + 115, 7.2, 7.2))])
    return 0, end - 1


def shot_outro(obs, crystals, summit, sl, stars):
    b = BEAT["outro"]
    start, end = b["start"], tl["frames"]
    n = end - start
    t_lit = w("outro", "一路点亮") - start
    key_color(stars, 0, "#cfd8ff", 0.7)
    for i, (ob, tile) in enumerate(zip(obs, TILES)):
        t = t_lit + round(i / (N - 1) * 42)
        key_color(ob, 0, tile["color"], 0.75)
        key_color(ob, t, tile["color"], 0.75)
        key_color(ob, t + 4, "#fff6d8", 2.0)
        key_color(ob, t + 16, GOLD, 1.0)
    idx = {id(t): i for i, t in enumerate(TILES)}
    for tile, parts in crystals:
        t = t_lit + round(idx[id(tile)] / (N - 1) * 42) + 3
        for o in parts:
            key_color(o, 0, tile["color"], 1.3)
            key_color(o, t, tile["color"], 1.3)
            key_color(o, t + 14, GOLD, 1.8)
    t_sum = t_lit + 46
    for o in summit:
        key_color(o, 0, GOLD, 1.6)
        key_color(o, t_sum, GOLD, 1.6)
        key_color(o, t_sum + 6, "#fffbea", 4.0)
        key_color(o, t_sum + 30, GOLD, 2.2)
    sl.energy = 450
    sl.keyframe_insert("energy", frame=t_sum)
    sl.energy = 1400
    sl.keyframe_insert("energy", frame=t_sum + 8)
    sl.energy = 700
    sl.keyframe_insert("energy", frame=t_sum + 34)
    a0 = deg(TILES[0]["a"]) + 200
    camera([orbit(0, 37.0, a0, 13.0), orbit(n - 1, 35.0, a0 + 45, 12.0)], [(0, side(a0, 7.4, 8.0)), (n - 1, side(a0 + 45, 7.4, 8.0))])
    return 0, n - 1


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--shot", choices=["intro", "outro"], required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--samples", type=int, default=16)
    ap.add_argument("--res", default="640x360")
    ap.add_argument("--frames", default="")
    ap.add_argument("--save", help="另存 .blend（看场景用）")
    a = ap.parse_args(argv)
    sc = setup(a.samples, tuple(int(x) for x in a.res.split("x")))
    parts = build()
    f0, f1 = (shot_intro if a.shot == "intro" else shot_outro)(*parts)
    sc.frame_start, sc.frame_end = f0, f1
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    if a.save:
        bpy.ops.wm.save_as_mainfile(filepath=str(Path(a.save).resolve()))
    print(f"shot {a.shot}: 帧 {f0}-{f1}（{f1 - f0 + 1} 帧），{N} 个关卡（{len(STOPS)} 站）", flush=True)
    frames = [int(x) for x in a.frames.split(",") if x] or None
    if frames:
        for f in frames:
            sc.frame_set(f)
            sc.render.filepath = str(out / f"{f:04d}.png")
            bpy.ops.render.render(write_still=True)
    else:
        sc.render.filepath = str(out / "####")
        bpy.ops.render.render(animation=True)


main()
