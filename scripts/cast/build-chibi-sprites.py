"""Build high-resolution pixelized Q-chibi sprite strips from the generated 3x2 pose sheets.

Reads the 3x2 chroma-key green sheets in assets/cast/source/ (whale-{blue,black}-chibi-sheet{1,2,3}.jpg),
keys out the background with key_unmix (from projects/game-aesthetic-asset/scripts/key-unmix.py),
area-downscales (premultiplied BOX) to PIXEL_H (~240 px tall so faces and details remain crisp),
quantizes each character to a unified 96-color palette (no dithering), aligns poses on a shared
foot anchor, synthesizes frame-stepped animation strips (blink, bounce, hop, sway, celebrate),
and writes lossless WebP strips + assets/cast/sprites.json.

Usage: python -I scripts/cast/build-chibi-sprites.py
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC_DIR = os.path.join(ROOT, "assets", "cast", "source")
OUT_DIR = os.path.join(ROOT, "assets", "cast", "sprites")
QA_DIR = os.path.join(ROOT, "temp", "cast-gen", "strips-qa")

# Reuse key_unmix from projects/game-aesthetic-asset/scripts/key-unmix.py when present.
KEY_UNMIX_DIR = os.path.normpath(os.path.join(ROOT, "..", "game-aesthetic-asset", "scripts"))
if os.path.isdir(KEY_UNMIX_DIR):
    sys.path.insert(0, KEY_UNMIX_DIR)
    key_unmix = __import__("key-unmix").key_unmix
else:
    def key_unmix(rgb):
        c = rgb.astype(np.float32)
        s = c[..., 1] - np.maximum(c[..., 0], c[..., 2])
        bgm = s > 150
        bg = np.median(c[bgm], 0)
        floor = np.percentile(s[bgm], 1) * 0.97
        alpha = np.clip(1.0 - s / floor, 0.0, 1.0)
        a3 = np.maximum(alpha, 0.05)[..., None]
        fg = (c - (1.0 - alpha[..., None]) * bg) / a3
        fg = np.where(alpha[..., None] > 0.02, fg, c)
        return np.clip(fg, 0, 255).astype(np.uint8), (alpha * 255).round().astype(np.uint8)

PIXEL_H = 240       # target standing pixel height (~256px stage height, clear facial details)
UNIT = 3            # sprite pixels per logical UI unit (scale={2} => ~170px CSS tall)
PALETTE_COLORS = 96
SIT_SCALE = 0.93

SHEETS = {
    "blue": [
        ("whale-blue-chibi-sheet1.jpg", ["idle", "wave", "walk", "jump_start", "jump_air", "jump_land"]),
        ("whale-blue-chibi-sheet2.jpg", ["coy", "sit", "dance", "think", "read", "cheer"]),
        ("whale-blue-chibi-sheet3.jpg", ["idle_blink", "wave_b", "walk_b", "dance_b", "cheer_b", "coy_b"]),
    ],
    "black": [
        ("whale-black-chibi-sheet1.jpg", ["idle", "wave", "walk", "jump_start", "jump_air", "jump_land"]),
        ("whale-black-chibi-sheet2.jpg", ["coy", "sit", "cast", "think", "read", "cheer"]),
        ("whale-black-chibi-sheet3.jpg", ["idle_blink", "wave_b", "walk_b", "cast_b", "cheer_b", "coy_b"]),
    ],
}


def find_mid_gap(vec, lo, hi):
    sub = vec[lo:hi] == 0
    best_len, best_mid, cur = -1, (lo + hi) // 2, 0
    for i, v in enumerate(sub):
        if v:
            cur += 1
            if cur > best_len:
                best_len = cur
                best_mid = lo + i - cur // 2
        else:
            cur = 0
    return best_mid


def extract_sheet_cells(path, names):
    rgb = np.array(Image.open(path).convert("RGB"))
    f = rgb.astype(np.float32)
    fg = (f[..., 1] - np.maximum(f[..., 0], f[..., 2])) < 55
    col_fg, row_fg = fg.sum(axis=0), fg.sum(axis=1)
    cx1 = find_mid_gap(col_fg, 250, 580)
    cx2 = find_mid_gap(col_fg, 680, 1020)
    ry1 = find_mid_gap(row_fg, 320, 520)
    xs = [0, cx1, cx2, rgb.shape[1]]
    ys = [0, ry1, rgb.shape[0]]

    k_rgb, k_alpha = key_unmix(rgb)
    # Trim 2px outer border against JPEG edge artifacts, and drop near-zero alpha noise.
    k_alpha[:2, :] = 0
    k_alpha[-2:, :] = 0
    k_alpha[:, :2] = 0
    k_alpha[:, -2:] = 0
    k_alpha[k_alpha <= 18] = 0

    out = {}
    for idx, name in enumerate(names):
        r, c = divmod(idx, 3)
        sub_rgb = k_rgb[ys[r]:ys[r + 1], xs[c]:xs[c + 1]]
        sub_al = k_alpha[ys[r]:ys[r + 1], xs[c]:xs[c + 1]].copy()
        lab, n = ndimage.label(sub_al > 24)
        if n > 0:
            sz = ndimage.sum(np.ones_like(sub_al), lab, range(1, n + 1))
            main_id = 1 + int(np.argmax(sz))
            my, mx = np.nonzero(lab == main_id)
            y0, y1 = max(0, my.min() - 45), min(sub_al.shape[0], my.max() + 45)
            x0, x1 = max(0, mx.min() - 45), min(sub_al.shape[1], mx.max() + 45)
            keep = np.zeros_like(sub_al, dtype=bool)
            keep[lab == main_id] = True
            # Retain intentional nearby sparkles (>= 10 px inside the padded character box).
            for cid in range(1, n + 1):
                if cid == main_id or sz[cid - 1] < 10:
                    continue
                cy, cx = np.nonzero(lab == cid)
                if (cy >= y0).all() and (cy <= y1).all() and (cx >= x0).all() and (cx <= x1).all():
                    keep[lab == cid] = True
            sub_al[~keep] = 0
        im = Image.fromarray(np.dstack([sub_rgb, sub_al]), "RGBA")
        im = im.crop(im.getchannel("A").getbbox())
        out[name] = im
    return out


def premul_resize(im, nw, nh, filt=Image.BOX):
    p = np.array(im, dtype=np.float64)
    p[..., :3] *= p[..., 3:4] / 255.0
    chs = [Image.fromarray(p[..., c].round().astype(np.uint8)).resize((nw, nh), filt) for c in range(4)]
    q = np.stack([np.array(c, np.float64) for c in chs], -1)
    al = q[..., 3:4]
    q[..., :3] = np.where(al > 0, q[..., :3] * 255.0 / np.maximum(al, 1), 0)
    return Image.fromarray(q.clip(0, 255).round().astype(np.uint8), "RGBA")


def build_palette(poses):
    samples = []
    for name, im in poses.items():
        arr = np.array(im)
        h, w = arr.shape[:2]
        mask = arr[..., 3] > 200
        pts = arr[mask][..., :3]
        if len(pts) > 4000:
            pts = pts[::max(1, len(pts) // 4000)]
        samples.append(pts)
        # Oversample face/chest area so blush and jewel tones retain dedicated colors.
        face = arr[int(h * 0.22):int(h * 0.55), int(w * 0.25):int(w * 0.75)]
        fpts = face[face[..., 3] > 200][..., :3]
        if len(fpts) > 2500:
            fpts = fpts[::max(1, len(fpts) // 2500)]
        if len(fpts):
            samples.append(fpts)
    all_pts = np.vstack(samples)
    strip = Image.fromarray(all_pts[:min(len(all_pts), 80000)].reshape(-1, 1, 3), "RGB")
    return strip.quantize(colors=PALETTE_COLORS, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)


def foot_x_of(im, name):
    """Center horizontally on the character's face-skin cluster so hair/tail/kicks never shift body center."""
    arr = np.array(im)
    h, w = arr.shape[:2]
    top = arr[:int(h * 0.50)]
    r, g, b, a = top[..., 0].astype(int), top[..., 1].astype(int), top[..., 2].astype(int), top[..., 3]
    skin = (a > 200) & (r > 205) & (g > 165) & (b > 140) & (r > g) & ((r - b) > 18) & ((r - b) < 95)
    lab, n = ndimage.label(skin)
    if n > 0:
        sz = ndimage.sum(np.ones_like(skin, dtype=np.int32), lab, range(1, n + 1))
        main_face = lab == (1 + int(np.argmax(sz)))
        _, xs = np.nonzero(main_face)
        if len(xs):
            return int(round(float(np.median(xs))))
    al = a > 128
    _, xs = np.nonzero(al)
    return int(round((xs.min() + xs.max()) / 2.0)) if len(xs) else w // 2


def align_pair_offset(base_im, alt_im, base_fx, alt_fx):
    """Find small integer (dx, dy) that best aligns alt_im onto base_im on lower body."""
    bw, bh = base_im.size
    aw, ah = alt_im.size
    b_arr = np.array(base_im, dtype=np.int16)
    a_arr = np.array(alt_im, dtype=np.int16)
    init_dx = base_fx - alt_fx
    init_dy = bh - ah
    best = (1e18, init_dx, init_dy)
    for dy in range(init_dy - 10, init_dy + 11):
        for dx in range(init_dx - 10, init_dx + 11):
            x0, y0 = max(0, dx), max(0, dy)
            x1, y1 = min(bw, dx + aw), min(bh, dy + ah)
            if x1 <= x0 or y1 <= y0:
                continue
            bs = b_arr[y0:y1, x0:x1]
            as_ = a_arr[y0 - dy:y1 - dy, x0 - dx:x1 - dx]
            # Compare lower 45% (outfit/shoes) so eye blink or hand change doesn't bias alignment.
            y_cut = max(0, int((y1 - y0) * 0.55))
            bs_l, as_l = bs[y_cut:], as_[y_cut:]
            m = (bs_l[..., 3] > 128) & (as_l[..., 3] > 128)
            if m.sum() < 400:
                continue
            err = float(np.abs(bs_l[m][..., :3] - as_l[m][..., :3]).mean())
            if err < best[0]:
                best = (err, dx, dy)
    return best[1], best[2]


def transform_pose(im, fx, fy, stage_w, stage_h, dx=0, dy=0, sx=1.0, sy=1.0, rot=0.0):
    """Place a single pose onto a uniform stage canvas with foot anchored at (stage_w//2, stage_h - ground_pad)."""
    canvas = Image.new("RGBA", (stage_w, stage_h), (0, 0, 0, 0))
    w, h = im.size
    nw = max(1, int(round(w * sx)))
    nh = max(1, int(round(h * sy)))
    cur = premul_resize(im, nw, nh, Image.BILINEAR) if (nw != w or nh != h) else im
    nfx = int(round(fx * sx))
    nfy = int(round(fy * sy))

    if abs(rot) > 0.05:
        # Rotate around foot anchor by padding symmetrically around (nfx, nfy).
        pad = max(nw, nh)
        tmp = Image.new("RGBA", (pad * 2, pad * 2), (0, 0, 0, 0))
        tmp.paste(cur, (pad - nfx, pad - nfy))
        tmp = tmp.rotate(-rot, resample=Image.BILINEAR, center=(pad, pad))
        px = stage_w // 2 - pad + int(round(dx))
        py = stage_h - pad + int(round(dy))
        canvas.paste(tmp, (px, py), tmp)
    else:
        px = stage_w // 2 - nfx + int(round(dx))
        py = stage_h - nfy + int(round(dy))
        canvas.paste(cur, (px, py), cur)
    return canvas


def quantize_frame(im, pal_im):
    al = im.getchannel("A").point(lambda v: 255 if v >= 115 else 0)
    rgb_q = im.convert("RGB").quantize(palette=pal_im, dither=Image.Dither.NONE).convert("RGB")
    out = rgb_q.convert("RGBA")
    out.putalpha(al)
    return out


def build_action_frames(who, poses, fx_map, pal_im):
    """Return dict of action -> (frames_list, fps, loop, foot_y_offset)."""
    celeb = "dance" if who == "blue" else "cast"
    celeb_b = "cheer_b" if who == "blue" else "cast_b"
    sw, sh = 290, 290
    ground = 266  # leave 24px below ground for slight crouch/landing if needed, and 266px above

    def place(key, dx=0, dy=0, sx=1.0, sy=1.0, rot=0.0):
        im = poses[key]
        fx = fx_map[key]
        fy = im.height
        c = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
        w, h = im.size
        nw, nh = max(1, int(round(w * sx))), max(1, int(round(h * sy)))
        cur = premul_resize(im, nw, nh, Image.BILINEAR) if (nw != w or nh != h) else im
        nfx, nfy = int(round(fx * sx)), int(round(fy * sy))
        if abs(rot) > 0.05:
            pad = max(nw, nh)
            tmp = Image.new("RGBA", (pad * 2, pad * 2), (0, 0, 0, 0))
            tmp.paste(cur, (pad - nfx, pad - nfy))
            tmp = tmp.rotate(-rot, resample=Image.BILINEAR, center=(pad, pad))
            c.paste(tmp, (sw // 2 - pad + int(round(dx)), ground - pad + int(round(dy))), tmp)
        else:
            c.paste(cur, (sw // 2 - nfx + int(round(dx)), ground - nfy + int(round(dy))), cur)
        return quantize_frame(c, pal_im)

    # Align blink/alt frames to their primary poses
    aligned_pairs = [
        ("idle", "idle_blink"),
        ("wave", "wave_b"),
    ]
    if who == "black":
        aligned_pairs.append(("cast", "cast_b"))

    pair_shift = {}
    for base, alt in aligned_pairs:
        dx, dy = align_pair_offset(poses[base], poses[alt], fx_map[base], fx_map[alt])
        # Store shift relative to base foot placement
        alt_dx = (fx_map[alt] + dx) - fx_map[base]
        alt_dy = (poses[alt].height + dy) - poses[base].height
        pair_shift[alt] = (alt_dx, alt_dy)

    actions = {}

    # 1. idle: 24 frames @ 10fps — gentle breathing + natural blink
    idle_frames = []
    for i in range(24):
        ph = 2 * math.pi * i / 24.0
        dy = round(-2.0 * (0.5 - 0.5 * math.cos(ph * 2)))
        k = "idle_blink" if i in (16, 17, 18) else "idle"
        adx, ady = pair_shift.get(k, (0, 0))
        idle_frames.append(place(k, dx=adx, dy=dy + ady))
    actions["idle"] = (idle_frames, 10, True, ground)

    # 2. wave: 16 frames @ 10fps — friendly wave + happy ^^ blink
    wave_frames = []
    for i in range(16):
        ph = math.pi * i / 15.0
        dy = round(-5.0 * math.sin(ph) * abs(math.sin(2 * ph)))
        rot = 2.5 * math.sin(2 * math.pi * i / 15.0)
        k = "wave_b" if 5 <= i <= 10 else "wave"
        adx, ady = pair_shift.get(k, (0, 0))
        wave_frames.append(place(k, dx=adx, dy=dy + ady, rot=rot))
    actions["wave"] = (wave_frames, 10, False, ground)

    # 3. walk: 12 frames @ 10fps — lively double-bounce step cycle
    walk_frames = []
    for i in range(12):
        ph = 2 * math.pi * i / 12.0
        dy = round(-6.0 * abs(math.sin(ph)))
        rot = 2.0 * math.sin(ph)
        dx = round(1.5 * math.sin(ph))
        walk_frames.append(place("walk", dx=dx, dy=dy, rot=rot))
    actions["walk"] = (walk_frames, 10, True, ground)

    # 4. jump_start: 6 frames @ 12fps — anticipation crouch
    js_frames = [
        place("jump_start", sx=1.01, sy=0.98),
        place("jump_start", sx=1.04, sy=0.94),
        place("jump_start", sx=1.06, sy=0.91),
        place("jump_start", sx=1.05, sy=0.93),
        place("jump_start", sx=1.01, sy=0.98),
        place("jump_start", sx=0.98, sy=1.02, dy=-4),
    ]
    actions["jump_start"] = (js_frames, 12, False, ground)

    # 5. jump_air: 8 frames @ 10fps — joyful mid-air float
    ja_frames = []
    for i in range(8):
        dy = round(-16 - 6 * math.sin(math.pi * i / 7.0))
        ja_frames.append(place("jump_air", dy=dy, rot=1.5 * math.cos(2 * math.pi * i / 8.0)))
    actions["jump_air"] = (ja_frames, 10, True, ground)

    # 6. jump_land: 8 frames @ 12fps — drop + squash & happy bounce
    jl_seq = [
        (-12, 0.97, 1.03),
        (-3, 1.00, 1.00),
        (1, 1.06, 0.92),
        (0, 1.03, 0.96),
        (-3, 0.99, 1.02),
        (0, 1.00, 1.00),
        (0, 1.00, 1.00),
        (0, 1.00, 1.00),
    ]
    jl_frames = [place("jump_land", dy=dy, sx=sx, sy=sy) for dy, sx, sy in jl_seq]
    actions["jump_land"] = (jl_frames, 12, False, ground)

    # 7. coy: 16 frames @ 8fps — shy blush gentle sway (consistent pose/tail)
    coy_frames = []
    for i in range(16):
        rot = 1.8 * math.sin(2 * math.pi * i / 16.0)
        dy = -1 if i % 4 in (1, 2) else 0
        coy_frames.append(place("coy", dy=dy, rot=rot))
    actions["coy"] = (coy_frames, 8, True, ground)

    # 8. sit: 12 frames @ 8fps — relaxed breathing
    sit_frames = []
    for i in range(12):
        dy = round(-2.0 * (0.5 - 0.5 * math.cos(2 * math.pi * i / 12.0)))
        sit_frames.append(place("sit", dy=dy))
    actions["sit"] = (sit_frames, 8, True, ground)

    # 9. dance (blue) / cast (black): 20 frames @ 10fps — joyful celebratory sequence
    cel_frames = []
    for i in range(20):
        if who == "blue":
            if i < 6:
                dy = round(-12.0 * math.sin(math.pi * i / 5.0))
                cel_frames.append(place("dance", dy=dy, rot=-2.5 * math.sin(math.pi * i / 5.0)))
            elif i < 13:
                dy = round(-14.0 * math.sin(math.pi * (i - 6) / 6.0))
                cel_frames.append(place("cheer_b", dy=dy, rot=2.5 * math.sin(math.pi * (i - 6) / 6.0)))
            else:
                dy = round(-8.0 * math.sin(math.pi * (i - 13) / 6.0))
                cel_frames.append(place("dance", dy=dy))
        else:
            dy = round(-8.0 * (0.5 - 0.5 * math.cos(2 * math.pi * i / 10.0)))
            k = "cast_b" if 5 <= i <= 14 else "cast"
            adx, ady = pair_shift.get(k, (0, 0))
            rot = 1.8 * math.sin(2 * math.pi * i / 20.0)
            cel_frames.append(place(k, dx=adx, dy=dy + ady, rot=rot))
    actions[celeb] = (cel_frames, 10, False, ground)

    # 10. think: 14 frames @ 8fps — thoughtful tilt & breathing
    think_frames = []
    for i in range(14):
        ph = 2 * math.pi * i / 14.0
        rot = -2.2 * (0.5 - 0.5 * math.cos(ph))
        dy = round(-1.5 * (0.5 - 0.5 * math.cos(ph)))
        think_frames.append(place("think", dy=dy, rot=rot))
    actions["think"] = (think_frames, 8, True, ground)

    # 11. read: 14 frames @ 8fps — calm reading/teaching nod
    read_frames = []
    for i in range(14):
        ph = 2 * math.pi * i / 14.0
        rot = 1.6 * (0.5 - 0.5 * math.cos(ph))
        dy = round(-2.0 * (0.5 - 0.5 * math.cos(ph)))
        read_frames.append(place("read", dy=dy, rot=rot))
    actions["read"] = (read_frames, 8, True, ground)

    # 12. cheer: 16 frames @ 10fps — double-hop cheer alternating cheer <-> cheer_b
    cheer_frames = []
    for i in range(16):
        hop = abs(math.sin(2 * math.pi * i / 16.0))
        dy = round(-11.0 * hop)
        k = "cheer_b" if 4 <= i <= 12 else "cheer"
        rot = 2.0 * math.sin(2 * math.pi * i / 8.0)
        cheer_frames.append(place(k, dy=dy, rot=rot))
    actions["cheer"] = (cheer_frames, 10, False, ground)

    return actions, sw


def main():
    os.makedirs(QA_DIR, exist_ok=True)
    manifest = {"unit": UNIT, "pixelated": True, "packs": {}}

    for who, sheet_list in SHEETS.items():
        raw_poses = {}
        for fn, names in sheet_list:
            raw_poses.update(extract_sheet_cells(os.path.join(SRC_DIR, fn), names))

        base_h = float(raw_poses["idle"].height)
        scale_base = PIXEL_H / base_h
        poses = {}
        fx_map = {}
        for name, im in raw_poses.items():
            s = scale_base * (SIT_SCALE if name == "sit" else 1.0)
            nw, nh = max(1, round(im.width * s)), max(1, round(im.height * s))
            resized = premul_resize(im, nw, nh, Image.BOX)
            poses[name] = resized
            fx_map[name] = foot_x_of(resized, name)

        pal_im = build_palette(poses)
        actions, sw = build_action_frames(who, poses, fx_map, pal_im)

        out_pack_dir = os.path.join(OUT_DIR, who)
        os.makedirs(out_pack_dir, exist_ok=True)
        # Remove stale files in out_pack_dir
        for old in os.listdir(out_pack_dir):
            if old.endswith(".webp"):
                os.remove(os.path.join(out_pack_dir, old))

        manifest["packs"][who] = {}
        total_kb = 0
        for act_name, (frames, fps, loop, ground) in actions.items():
            boxes = [f.getchannel("A").getbbox() for f in frames]
            boxes = [b for b in boxes if b]
            x0 = min(b[0] for b in boxes)
            y0 = min(b[1] for b in boxes)
            x1 = max(b[2] for b in boxes)
            y1 = max(b[3] for b in boxes)
            # Align foot anchor and frame dimensions to multiples of UNIT so CSS scale=2/UNIT stays integer.
            fx = sw // 2 - x0
            fy = ground - y0
            pad_l = (UNIT - (fx % UNIT)) % UNIT
            pad_t = (UNIT - (fy % UNIT)) % UNIT
            fx += pad_l
            fy += pad_t
            fw = ((x1 - x0 + pad_l + UNIT - 1) // UNIT) * UNIT
            fh = ((y1 - y0 + pad_t + UNIT - 1) // UNIT) * UNIT
            strip = Image.new("RGBA", (fw * len(frames), fh), (0, 0, 0, 0))
            cropped_frames = []
            for i, fr in enumerate(frames):
                cf = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
                cf.paste(fr.crop((x0, y0, x1, y1)), (pad_l, pad_t))
                strip.paste(cf, (i * fw, 0))
                cropped_frames.append(cf)
            out_file = os.path.join(out_pack_dir, f"{act_name}.webp")
            strip.save(out_file, "WEBP", lossless=True, quality=100, method=6)
            kb = os.path.getsize(out_file) // 1024
            total_kb += kb
            manifest["packs"][who][act_name] = {
                "file": f"sprites/{who}/{act_name}.webp",
                "w": fw,
                "h": fh,
                "frames": len(frames),
                "fps": fps,
                "loop": loop,
                "foot": [fx, fy],
            }
            print(f"{who}/{act_name:10s}: {len(frames):2d} frames {fw}x{fh}, foot={[fx, fy]}, {kb} KB")
            # Save animated preview GIF for QA
            bg_frames = []
            for cf in cropped_frames:
                bg = Image.new("RGBA", (fw, fh), (20, 20, 43, 255))
                bg.alpha_composite(cf)
                bg_frames.append(bg.convert("P", palette=Image.ADAPTIVE))
            bg_frames[0].save(
                os.path.join(QA_DIR, f"{who}_{act_name}.gif"),
                save_all=True,
                append_images=bg_frames[1:],
                duration=round(1000 / fps),
                loop=0,
            )
        print(f"{who} total sprite size: {total_kb} KB")

    manifest_path = os.path.join(ROOT, "assets", "cast", "sprites.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    print("Wrote", manifest_path)


if __name__ == "__main__":
    main()
