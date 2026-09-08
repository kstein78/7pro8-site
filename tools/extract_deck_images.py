#!/usr/bin/env python3
"""Extract photography from the 2026 partner presentation into static/img/.

The presentations in the project are page renders at 1456x840, so what comes out
of here is presentation-resolution: good enough to judge a design on, not good
enough to launch with. Every slot filled by this script should eventually be
replaced by the original photograph — see IMAGES.md.

Usage:
    python3 tools/extract_deck_images.py /path/to/unpacked/slides

The argument is a directory containing the slide renders as 1.jpeg ... 23.jpeg.
"""

import pathlib
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).parent.parent
OUT = ROOT / "static" / "img"

# (destination, slide number, crop box in slide coordinates, output aspect)
# Boxes were read off the 1456x840 renders of the English deck.
CROPS = [
    # Boxes exclude the deck's own caption strip along the bottom of each photo
    # and its BEFORE/AFTER badge in the top-left corner.
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


def main(src_dir):
    src = pathlib.Path(src_dir)
    written = 0
    for dest, slide, box, aspect in CROPS:
        page = src / f"{slide}.jpeg"
        if not page.exists():
            print(f"  missing slide {slide} for {dest}")
            continue
        im = Image.open(page).convert("RGB").crop(box)
        im = cover_crop(im, aspect)
        # a modest upscale keeps the layout honest without pretending to detail
        target_w = 1400 if dest.startswith(("home/hero", "share/")) else 1000
        if im.width < target_w:
            im = im.resize((target_w, round(im.height * target_w / im.width)), Image.LANCZOS)
        out = OUT / dest
        out.parent.mkdir(parents=True, exist_ok=True)
        im.save(out, quality=86, optimize=True, progressive=True)
        written += 1
        print(f"  {dest}  {im.size[0]}x{im.size[1]}  {out.stat().st_size // 1024} KB")
    print(f"\n{written} images written to {OUT}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
