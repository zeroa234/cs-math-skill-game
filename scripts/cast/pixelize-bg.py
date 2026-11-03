"""Turn generated scenery into game pixel art: area downscale to 480x270, then a 48-colour palette
without dithering (the same recipe as projects/kabu-quest: ImageScale area + ImageQuantize).

usage: python -I scripts/cast/pixelize-bg.py <source.png> <name>   → assets/bg/<name>.png
The source images and the prompts that made them are listed in assets/bg/README.md.
"""
import os
import sys

from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
SIZE, COLORS = (480, 270), 48


def main(src, name):
    im = Image.open(src).convert("RGB")
    im = im.resize(SIZE, Image.BOX)
    im = im.quantize(colors=COLORS, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")
    out = os.path.join(ROOT, "assets", "bg", name + ".png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out, optimize=True)
    print(out, os.path.getsize(out) // 1024, "KB")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
