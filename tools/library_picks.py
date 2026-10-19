#!/usr/bin/env python3
"""Replace chosen site images with photographs picked by hand from the library.

`upgrade_from_library.py` is automatic: it only swaps an image for a larger copy
of the *same frame*. This file is the opposite — a deliberate, reviewed list of
"this slot should use that photograph instead", for the places where the deck's
version was the weakest thing on the page and the old site has something better.

Each pick names the library file, so the choice is auditable and re-runnable.
The crop is a centre cover-crop to the slot's current aspect ratio, so nothing
in the layout moves.

    python3 tools/library_picks.py /path/to/library [--dry-run]
"""

import argparse
import pathlib
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).parent.parent
SITE = ROOT / "static" / "img"

# destination -> (library file, why this one)
PICKS = {
    # The hero carried a 1500 px crop into a full-bleed slot. This is the same
    # subject — a V-Class rear zone with the partition — shot properly.
    "home/hero-v-class-partition.jpg": (
        "010__5.webp", "partition with twin monitors seen from the rear cabin, 2500 px"),

    # company/workshop.jpg and manufacturing/v-class-assembly.jpg were tried
    # against 145_DSC_8364 and 072_DSC_4182 and put back: both library shots are
    # better photographs but worse captions — one is a dark detail of a man with
    # a lamp, the other a stripped van. The deck's versions actually show
    # finished partitions on the shop floor, which is what the text promises.

    # Three slots were showing the same 834 px CAD crop from the deck. The
    # library has the V-Class partition CAD at 2500 px, in several views, so
    # each slot can show a different stage instead of the same picture.
    "capabilities/cad-model.jpg": (
        "067_V__004.webp", "V-Class partition frame, CAD"),
    "home/vle-development.jpg": (
        "069_V-CLASS_004.webp", "V-Class partition, CAD, another view"),
    "vle/cad-development.jpg": (
        "071_V-CLASS_008.webp", "V-Class partition, CAD, section"),

    # Tooling: the deck's versions were 900 px crops of a page render.
    "home/tooling-mould.jpg": (
        "028_32c24cbf-255a-4484-814b-774090568ac3.webp", "mould on the bench"),
    # manufacturing/mould-panel-forming.jpg keeps the deck's version: the
    # library's equivalent is a mould on a pallet in a corner of the shop,
    # which gains 50 px and loses the page.

    # 651 px into a 604 px slot, and the library has the same kind of light-trim
    # V-Class interior at 1125 px.
    "portfolio/v-class-line-2/04.jpg": (
        "016_photo_2023-06-22_18-23-00.webp", "V-Class interior in light trim"),
}


def cover_crop(im, aspect):
    target = aspect[0] / aspect[1]
    w, h = im.size
    if w / h > target:
        new_w = int(h * target)
        left = (w - new_w) // 2
        return im.crop((left, 0, left + new_w, h))
    new_h = int(w / target)
    top = (h - new_h) // 2
    return im.crop((0, top, w, top + new_h))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("library")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    lib = pathlib.Path(args.library)

    done = 0
    for dest, (src_name, why) in PICKS.items():
        src = lib / src_name
        out = SITE / dest
        if not src.exists():
            print(f"  !! {dest}: {src_name} not in the library")
            continue
        if not out.exists():
            print(f"  !! {dest}: no current file to take the aspect from")
            continue
        with Image.open(out) as cur:
            aspect = cur.size
        with Image.open(src) as im:
            new = cover_crop(im.convert("RGB"), aspect)
        print(f"  {dest:44s} {aspect[0]}x{aspect[1]} -> {new.width}x{new.height}"
              f"   {why}")
        if not args.dry_run:
            new.save(out, quality=92, optimize=True, progressive=True)
        done += 1

    print(f"\n{done}/{len(PICKS)} slots {'would be ' if args.dry_run else ''}replaced")
    return 0


if __name__ == "__main__":
    sys.exit(main())
