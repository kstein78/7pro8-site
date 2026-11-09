#!/usr/bin/env python3
"""Extract photography from the 2026 partner presentation at native resolution.

The earlier version of this script cropped 1456x820 page *renders* and upscaled
the result, which is why several images looked soft or pixelated next to the
rest of the page. This version goes to the embedded originals instead.

How it works, and why it is exact rather than guessed:

  * The crop boxes below were read off the 1456x820 renders of the English deck
    and are kept unchanged — they are what the design was composed against.
  * pdfplumber reports where every embedded image sits on its page, in points.
    The render is a uniform scale of the page, so a box in render pixels maps to
    page points by a single factor.
  * The box is then expressed as a fraction of the placed image's rectangle, and
    that fraction is applied to the image's native pixel grid.

So each output is a crop of the original photograph, at whatever resolution the
original holds — typically 834x590 to 2260x1301 instead of the 350-720 px the
renders gave. Nothing is upscaled; where an original is genuinely small, the
output stays small and `tools/photo_inventory.py` flags it for replacement.

Usage:
    python3 tools/extract_deck_images.py path/to/7pro8_Presentation_EN.pdf
"""

import io
import pathlib
import sys

import pdfplumber
import pikepdf
from PIL import Image

ROOT = pathlib.Path(__file__).parent.parent
OUT = ROOT / "static" / "img"

# Width the renders were measured at. Only the ratio to the page width matters.
RENDER_W = 1456

# (destination, page number, crop box in render coordinates, output aspect)
# Boxes exclude the deck's own caption strip along the bottom of each photo and
# its BEFORE/AFTER badge in the top-left corner.
CROPS = [
    # home page
    ("home/hero-v-class-partition.jpg", 10, (77, 452, 798, 738), (3, 2)),
    ("home/tooling-mould.jpg", 3, (962, 194, 1380, 388), (3, 2)),
    ("home/vle-development.jpg", 3, (518, 194, 936, 388), (3, 2)),
    ("share/7pro8-share.jpg", 10, (77, 452, 798, 738), (1200, 630)),
    # project covers
    ("portfolio/v-class-line-1/cover.jpg", 4, (830, 118, 1378, 396), (4, 3)),
    ("portfolio/v-class-line-2/cover.jpg", 11, (656, 478, 1006, 740), (4, 3)),
    ("portfolio/sprinter/cover.jpg", 12, (76, 478, 424, 740), (4, 3)),
    ("portfolio/maybach-x222/cover.jpg", 14, (76, 142, 798, 400), (4, 3)),
    ("portfolio/range-rover/cover.jpg", 13, (740, 186, 1380, 400), (4, 3)),
    ("portfolio/rr-phantom/cover.jpg", 16, (76, 140, 796, 398), (4, 3)),
    ("portfolio/rr-ghost/cover.jpg", 17, (657, 142, 1010, 394), (4, 3)),
    ("portfolio/s-class-v222/cover.jpg", 15, (657, 142, 1010, 394), (4, 3)),
    ("portfolio/escalade/cover.jpg", 18, (76, 150, 700, 600), (4, 3)),
    # supporting images
    ("product/maybach-x222-interior.jpg", 14, (76, 142, 798, 400), (4, 3)),
    ("capabilities/cad-model.jpg", 3, (518, 194, 936, 388), (4, 3)),
    ("manufacturing/mould-panel-forming.jpg", 3, (962, 194, 1380, 388), (4, 3)),
    ("manufacturing/frame-sprinter.jpg", 4, (854, 458, 1070, 736), (4, 3)),
    ("manufacturing/glass-mechanism.jpg", 4, (446, 492, 798, 566), (4, 3)),
    ("manufacturing/v-class-assembly.jpg", 4, (830, 118, 1378, 396), (4, 3)),
    ("vle/cad-development.jpg", 3, (518, 194, 936, 388), (4, 3)),
    ("company/workshop.jpg", 4, (830, 118, 1378, 396), (4, 3)),
    ("company/novi-sad.jpg", 12, (450, 478, 798, 740), (4, 3)),
    # project galleries
    ("portfolio/v-class-line-1/01.jpg", 10, (77, 140, 428, 400), (3, 2)),
    ("portfolio/v-class-line-1/02.jpg", 10, (449, 140, 798, 400), (3, 2)),
    ("portfolio/v-class-line-1/03.jpg", 10, (77, 452, 798, 738), (3, 2)),
    ("portfolio/v-class-line-2/01.jpg", 11, (656, 138, 1006, 396), (3, 2)),
    ("portfolio/v-class-line-2/02.jpg", 11, (1026, 138, 1380, 396), (3, 2)),
    ("portfolio/v-class-line-2/03.jpg", 11, (656, 478, 1006, 740), (3, 2)),
    ("portfolio/v-class-line-2/04.jpg", 11, (1026, 478, 1380, 740), (3, 2)),
    ("portfolio/sprinter/01.jpg", 12, (76, 138, 298, 396), (3, 2)),
    ("portfolio/sprinter/02.jpg", 12, (324, 138, 542, 396), (3, 2)),
    ("portfolio/sprinter/03.jpg", 12, (76, 478, 424, 740), (3, 2)),
    ("portfolio/maybach-x222/01.jpg", 14, (76, 142, 798, 400), (3, 2)),
    ("portfolio/maybach-x222/02.jpg", 14, (76, 478, 304, 740), (3, 2)),
    ("portfolio/maybach-x222/03.jpg", 14, (324, 478, 544, 740), (3, 2)),
    ("portfolio/range-rover/01.jpg", 13, (76, 210, 712, 620), (3, 2)),
    ("portfolio/range-rover/02.jpg", 13, (740, 186, 1380, 400), (3, 2)),
    ("portfolio/range-rover/03.jpg", 13, (740, 505, 1050, 676), (3, 2)),
    ("portfolio/range-rover/04.jpg", 13, (1070, 505, 1380, 676), (3, 2)),
    ("portfolio/rr-phantom/01.jpg", 16, (76, 140, 796, 398), (3, 2)),
    ("portfolio/rr-phantom/02.jpg", 16, (76, 478, 300, 740), (3, 2)),
    ("portfolio/rr-phantom/03.jpg", 16, (320, 478, 550, 740), (3, 2)),
    ("portfolio/rr-ghost/01.jpg", 17, (657, 142, 1010, 394), (3, 2)),
    ("portfolio/rr-ghost/02.jpg", 17, (1029, 142, 1380, 394), (3, 2)),
    ("portfolio/rr-ghost/03.jpg", 17, (657, 478, 1010, 740), (3, 2)),
    ("portfolio/rr-ghost/04.jpg", 17, (1029, 478, 1380, 740), (3, 2)),
    ("portfolio/s-class-v222/01.jpg", 15, (657, 142, 1010, 394), (3, 2)),
    ("portfolio/s-class-v222/02.jpg", 15, (1029, 142, 1380, 394), (3, 2)),
    ("portfolio/s-class-v222/03.jpg", 15, (657, 478, 1010, 740), (3, 2)),
    ("portfolio/s-class-v222/04.jpg", 15, (1029, 478, 1380, 740), (3, 2)),
    ("portfolio/escalade/01.jpg", 18, (76, 150, 700, 600), (3, 2)),
]

# Decorative marks that are never photography: the logo watermark that sits in
# the top-right corner of every slide.
IGNORE_SMALLER_THAN = 64 * 64


def cover_crop(im, aspect):
    """Centre-crop to the requested aspect ratio without distorting."""
    target = aspect[0] / aspect[1]
    w, h = im.size
    if w / h > target:
        new_w = int(h * target)
        left = (w - new_w) // 2
        return im.crop((left, 0, left + new_w, h))
    new_h = int(w / target)
    top = (h - new_h) // 2
    return im.crop((0, top, w, top + new_h))


def fit_aspect(box, size, aspect):
    """Bring `box` to the requested aspect by growing it, not by cutting it.

    The deck frames some photographs as narrow strips. Forcing such a strip to
    4:3 by centre-cropping throws away most of its width — and most of the
    resolution with it. Growing the short side inside the original instead
    keeps every pixel the box had and only falls back to cutting when the
    original has no room left to give.
    """
    x0, y0, x1, y1 = box
    W, H = size
    target = aspect[0] / aspect[1]
    w, h = x1 - x0, y1 - y0

    if w / h > target:  # too wide: grow height around the centre
        want = w / target
        room = min(want, H)
        cy = (y0 + y1) / 2
        y0 = cy - room / 2
        y1 = cy + room / 2
        if y0 < 0:
            y1, y0 = y1 - y0, 0
        if y1 > H:
            y0, y1 = y0 - (y1 - H), H
        y0 = max(0, y0)
    else:  # too tall: grow width around the centre
        want = h * target
        room = min(want, W)
        cx = (x0 + x1) / 2
        x0 = cx - room / 2
        x1 = cx + room / 2
        if x0 < 0:
            x1, x0 = x1 - x0, 0
        if x1 > W:
            x0, x1 = x0 - (x1 - W), W
        x0 = max(0, x0)

    return (round(x0), round(y0), round(x1), round(y1))


def overlap(a, b):
    """Area shared by two (x0, y0, x1, y1) rectangles."""
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    return w * h if w > 0 and h > 0 else 0.0


def native_image(pdf, objid, gen=0):
    """The embedded image stored as PDF object `objid`, as a PIL image.

    pdfplumber names images with a synthetic key, but it does report the PDF
    object number, which addresses the same stream in pikepdf.
    """
    xobj = pdf.get_object(objid, gen)
    try:
        return pikepdf.PdfImage(xobj).as_pil_image().convert("RGB")
    except Exception:
        raw = xobj.read_raw_bytes()
        return Image.open(io.BytesIO(raw)).convert("RGB")


def main(pdf_path):
    src = pathlib.Path(pdf_path)
    if not src.exists():
        print(f"not found: {src}")
        return 1

    plumb = pdfplumber.open(str(src))
    pike = pikepdf.open(str(src))

    # cache of decoded originals, keyed by (page_index, resource name)
    cache = {}
    report = []
    written = 0

    for dest, page_no, box, aspect in CROPS:
        page = plumb.pages[page_no - 1]
        scale = RENDER_W / float(page.width)
        bx = [c / scale for c in box]  # render px -> page points, top-left origin

        best, best_area = None, 0.0
        for im in page.images:
            if im["srcsize"][0] * im["srcsize"][1] < IGNORE_SMALLER_THAN:
                continue
            rect = (im["x0"], im["top"], im["x1"], im["bottom"])
            area = overlap(bx, rect)
            # later in the content stream means drawn on top; ties go to the
            # one painted last, which is what the render shows
            if area >= best_area:
                best, best_area = im, area

        box_area = (bx[2] - bx[0]) * (bx[3] - bx[1])
        if best is None or best_area <= 0:
            print(f"  !! {dest}: no embedded image under the crop box on page {page_no}")
            continue
        covered = best_area / box_area

        objid = best["stream"].objid
        if objid not in cache:
            cache[objid] = native_image(pike, objid)
        orig = cache[objid]

        rx0, ry0, rx1, ry1 = best["x0"], best["top"], best["x1"], best["bottom"]
        fx0 = (bx[0] - rx0) / (rx1 - rx0)
        fx1 = (bx[2] - rx0) / (rx1 - rx0)
        fy0 = (bx[1] - ry0) / (ry1 - ry0)
        fy1 = (bx[3] - ry0) / (ry1 - ry0)
        W, H = orig.size
        crop = (
            max(0, round(fx0 * W)), max(0, round(fy0 * H)),
            min(W, round(fx1 * W)), min(H, round(fy1 * H)),
        )
        if crop[2] - crop[0] < 16 or crop[3] - crop[1] < 16:
            print(f"  !! {dest}: crop maps outside the original — skipped")
            continue

        crop = fit_aspect(crop, orig.size, aspect)
        im = cover_crop(orig.crop(crop), aspect)
        out = OUT / dest
        out.parent.mkdir(parents=True, exist_ok=True)
        # quality 92: these are the originals now, so the JPEG should not be
        # the thing that softens them
        im.save(out, quality=92, optimize=True, progressive=True)
        written += 1
        kb = out.stat().st_size // 1024
        report.append((dest, f"{W}x{H}", f"{im.size[0]}x{im.size[1]}", kb, covered))
        print(f"  {dest:48s} orig {W:>4}x{H:<4}  ->  {im.size[0]:>4}x{im.size[1]:<4} "
              f"{kb:>4} KB  box covered {covered:.0%}")

    plumb.close()
    pike.close()
    print(f"\n{written}/{len(CROPS)} images written from the embedded originals")
    thin = [r for r in report if r[4] < 0.9]
    if thin:
        print("\nCrop boxes not fully covered by one original (check these):")
        for r in thin:
            print(f"  {r[0]:48s} {r[4]:.0%}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
