"""Mentor portraits from the transparent standing illustrations in assets/cast/source/ (whale sisters, by ZipZipPipe,
CC BY-NC 4.0; copies of projects/deepseek-sisters/output/). The sources are already transparent: crop to the opaque area
(alpha > 8), scale to 1200 px high (Lanczos, on premultiplied colour so the edge does not darken), save WebP (quality 90, exact alpha).
No new cut-out (cutting a cut-out again leaves ragged hair edges, see assets/cast/README.md).

usage: python -I scripts/cast/make-portraits.py
"""
import os

import numpy as np
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = {"blue": "whale-blue-portrait.png", "black": "whale-black-portrait.png"}
H = 1200


def main():
    for who, name in SRC.items():
        im = Image.open(os.path.join(ROOT, "assets", "cast", "source", name)).convert("RGBA")
        a = np.array(im)
        box = Image.fromarray(((a[..., 3] > 8) * 255).astype(np.uint8)).getbbox()
        im = im.crop(box)
        w = round(im.width * H / im.height)
        p = np.array(im).astype(np.float64)
        p[..., :3] *= p[..., 3:4] / 255                     # premultiply
        big = [Image.fromarray(p[..., c].round().astype(np.uint8)).resize((w, H), Image.LANCZOS) for c in range(4)]
        q = np.stack([np.array(c, np.float64) for c in big], -1)
        al = q[..., 3:4]
        q[..., :3] = np.where(al > 0, q[..., :3] * 255 / np.maximum(al, 1), 0)
        out = Image.fromarray(q.clip(0, 255).round().astype(np.uint8), "RGBA")
        dst = os.path.join(ROOT, "assets", "cast", "portraits", f"{who}.webp")
        out.save(dst, "WEBP", quality=90, alpha_quality=100, method=6)   # lossy colour like the earlier portraits (~200 KB)
        print(f"{who}: crop {box} -> {out.size}, {os.path.getsize(dst) // 1024} KB")


if __name__ == "__main__":
    main()
