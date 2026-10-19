#!/usr/bin/env python3
"""Trim near-white slide or print margins off photographs, keeping the aspect.

Sketches and CAD renders are white by design and must not be passed here.

    python3 tools/trim_margins.py static/img/home/tooling-mould.jpg ...
"""
import sys
import numpy as np
from PIL import Image

THRESHOLD = 238


def run(v):
    n = 0
    for x in v:
        if x > THRESHOLD:
            n += 1
        else:
            break
    return n


def trim(path):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im.convert("L"), dtype=float)
    col, row = a.mean(axis=0), a.mean(axis=1)
    l, r, t, b = run(col), run(col[::-1]), run(row), run(row[::-1])
    pad = 4
    box = (l + pad if l else 0, t + pad if t else 0,
           im.width - (r + pad if r else 0), im.height - (b + pad if b else 0))
    inner = im.crop(box)
    # restore the original aspect by centre-cropping, never by stretching
    target = im.width / im.height
    w, h = inner.size
    if w / h > target:
        nw = int(h * target); x = (w - nw) // 2
        inner = inner.crop((x, 0, x + nw, h))
    else:
        nh = int(w / target); y = (h - nh) // 2
        inner = inner.crop((0, y, w, y + nh))
    inner = inner.resize(im.size, Image.LANCZOS)
    inner.save(path, quality=86, optimize=True, progressive=True)
    print(f"  {path}: trimmed l{l} r{r} t{t} b{b}")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        trim(p)
