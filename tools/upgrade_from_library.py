#!/usr/bin/env python3
"""Re-cut site images from a higher-resolution twin in an image library.

The old Squarespace site holds the same photographs at up to 2500 px, where the
partner deck only carries 800–1500 px versions of some of them. This finds the
twin, locates the current crop inside it, and re-cuts the same framing at the
library's resolution.

Locating is multi-scale template matching on grayscale: the current site image
is slid over the library image at a range of scales and the best normalised
correlation gives both where the crop sits and how much of the library image it
covers. A match below `--min-score` is not used — a confident match here looks
like 0.8–1.0, and anything near 0.6 is a different photograph of the same car.

    python3 tools/upgrade_from_library.py /path/to/library [--min-score 0.75]
    python3 tools/upgrade_from_library.py /path/to/library --dry-run

Only images that gain resolution are written. The framing is preserved, so the
page layout does not move.
"""

import argparse
import pathlib
import sys

import cv2
import numpy as np
from PIL import Image

ROOT = pathlib.Path(__file__).parent.parent
SITE = ROOT / "static" / "img"

# founder/* comes from the project archives and scans, not from the web library
SKIP_PREFIXES = ("founder/",)


def gray(path, width=None):
    im = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if im is None:
        return None
    if width and im.shape[1] != width:
        h = max(1, round(im.shape[0] * width / im.shape[1]))
        im = cv2.resize(im, (width, h), interpolation=cv2.INTER_AREA)
    return im


def locate(probe_path, lib_path, coarse=260, fine=900):
    """Where the probe sits inside the library image, as a fraction rectangle.

    Two passes: a coarse sweep to find the scale, then a finer one around it.
    Returns (score, (fx0, fy0, fx1, fy1)) in library-image fractions.
    """
    probe_full = cv2.imread(str(probe_path), cv2.IMREAD_GRAYSCALE)
    if probe_full is None:
        return 0.0, None

    best = (0.0, None)
    for stage, (lw, fracs) in enumerate((
        (coarse, np.arange(0.30, 1.01, 0.05)),
        (fine, None),
    )):
        lib = gray(lib_path, lw)
        if lib is None:
            return 0.0, None
        if fracs is None:
            centre = best[1]
            if centre is None:
                break
            f = centre[2] - centre[0]
            fracs = np.clip(np.arange(f - 0.06, f + 0.061, 0.015), 0.05, 1.0)
        for frac in fracs:
            pw = int(round(lib.shape[1] * float(frac)))
            ph = int(round(probe_full.shape[0] * pw / probe_full.shape[1]))
            if pw < 24 or ph < 24 or ph > lib.shape[0] or pw > lib.shape[1]:
                continue
            probe = cv2.resize(probe_full, (pw, ph), interpolation=cv2.INTER_AREA)
            res = cv2.matchTemplate(lib, probe, cv2.TM_CCOEFF_NORMED)
            _, score, _, loc = cv2.minMaxLoc(res)
            if score > best[0]:
                fx0 = loc[0] / lib.shape[1]
                fy0 = loc[1] / lib.shape[0]
                best = (float(score), (fx0, fy0, fx0 + pw / lib.shape[1],
                                       fy0 + ph / lib.shape[0]))
    return best


def fit_aspect(box, size, target):
    """Grow the box to the target aspect inside the image rather than cutting."""
    x0, y0, x1, y1 = box
    W, H = size
    w, h = x1 - x0, y1 - y0
    if w / h > target:
        room = min(w / target, H)
        cy = (y0 + y1) / 2
        y0, y1 = cy - room / 2, cy + room / 2
        if y0 < 0:
            y1, y0 = y1 - y0, 0
        if y1 > H:
            y0, y1 = y0 - (y1 - H), H
        y0 = max(0.0, y0)
    else:
        room = min(h * target, W)
        cx = (x0 + x1) / 2
        x0, x1 = cx - room / 2, cx + room / 2
        if x0 < 0:
            x1, x0 = x1 - x0, 0
        if x1 > W:
            x0, x1 = x0 - (x1 - W), W
        x0 = max(0.0, x0)
    return (round(x0), round(y0), round(x1), round(y1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("library")
    ap.add_argument("--min-score", type=float, default=0.75)
    ap.add_argument("--min-gain", type=float, default=1.15,
                    help="only write when the library image is this much wider")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    lib_dir = pathlib.Path(args.library)
    library = [f for f in sorted(lib_dir.iterdir())
               if f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")]
    if not library:
        print(f"no images in {lib_dir}")
        return 1
    # coarse signatures once, so the expensive pass runs only on a shortlist
    coarse = [(f, gray(f, 260)) for f in library]
    coarse = [(f, g) for f, g in coarse if g is not None]
    print(f"library: {len(coarse)} images")

    targets = [f for f in sorted(SITE.rglob("*.jpg"))
               if not str(f.relative_to(SITE)).startswith(SKIP_PREFIXES)]

    written = 0
    for t in targets:
        rel = str(t.relative_to(SITE))
        probe_full = cv2.imread(str(t), cv2.IMREAD_GRAYSCALE)
        if probe_full is None:
            continue
        # shortlist by a quick sweep
        shortlist = []
        for f, g in coarse:
            best = 0.0
            for frac in (1.0, 0.75, 0.55, 0.4):
                pw = max(24, int(g.shape[1] * frac))
                ph = max(24, round(probe_full.shape[0] * pw / probe_full.shape[1]))
                if ph > g.shape[0] or pw > g.shape[1]:
                    continue
                probe = cv2.resize(probe_full, (pw, ph), interpolation=cv2.INTER_AREA)
                best = max(best, float(cv2.matchTemplate(g, probe, cv2.TM_CCOEFF_NORMED).max()))
            shortlist.append((best, f))
        shortlist.sort(reverse=True, key=lambda x: x[0])
        if not shortlist or shortlist[0][0] < args.min_score * 0.85:
            continue

        cand = shortlist[0][1]
        with Image.open(t) as im:
            tw, th = im.size
        with Image.open(cand) as im:
            lw, lh = im.size
        if lw < tw * args.min_gain:
            continue

        score, frac_box = locate(t, cand)
        if score < args.min_score or frac_box is None:
            print(f"  skip {rel}: best {score:.2f} < {args.min_score}")
            continue

        with Image.open(cand) as im:
            src = im.convert("RGB")
        W, H = src.size
        box = (frac_box[0] * W, frac_box[1] * H, frac_box[2] * W, frac_box[3] * H)
        box = fit_aspect(box, (W, H), tw / th)
        out_im = src.crop(box)
        if out_im.width < tw * args.min_gain:
            print(f"  skip {rel}: located crop is only {out_im.width}px")
            continue
        # keep the slot's exact aspect; the fit above gets within a pixel or two
        target_h = round(out_im.width * th / tw)
        if abs(target_h - out_im.height) > 2:
            out_im = out_im.crop((0, max(0, (out_im.height - target_h) // 2),
                                  out_im.width,
                                  max(0, (out_im.height - target_h) // 2) + target_h))

        print(f"  {rel:44s} {tw}x{th} -> {out_im.width}x{out_im.height}"
              f"  score {score:.2f}  {cand.name[:40]}")
        if not args.dry_run:
            out_im.save(t, quality=92, optimize=True, progressive=True)
        written += 1

    print(f"\n{written} images {'would be ' if args.dry_run else ''}re-cut from the library")
    return 0


if __name__ == "__main__":
    sys.exit(main())
