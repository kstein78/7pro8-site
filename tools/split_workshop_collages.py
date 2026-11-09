#!/usr/bin/env python3
"""Cut the two "workshop" collages (scans of prints laid out on a sheet) into
single photographs for the ≈1999 chronicle entry.

The boxes were measured on the 1280 px copies that extract_founder_images.py
writes; run this after it. The dark second shot of the white crowned seat
(collage 2, top left) is left out: it repeats the seat in collage 1.

    python3 tools/split_workshop_collages.py
"""
import pathlib
from PIL import Image

DIR = pathlib.Path(__file__).parent.parent / "static" / "img" / "founder" / "workshop"
CUTS = [  # (collage, box) in display order
    ("01.jpg", (2, 2, 629, 428)),      # moulded part on the bench
    ("01.jpg", (634, 2, 1278, 428)),   # rear seat, crowned headrest
    ("01.jpg", (320, 436, 967, 860)),  # night, pile of boxes
    ("02.jpg", (448, 2, 886, 650)),    # pier, motor yachts
    ("02.jpg", (2, 650, 438, 1278)),   # Audi estate, rear
    ("02.jpg", (447, 654, 886, 1278)), # mirrored ceiling
]

def main():
    src = {n: Image.open(DIR / n).convert("RGB") for n in {c for c, _ in CUTS}}
    # the singles are written over the collages' names, so a second run would
    # cut the cut photographs; refuse unless the collages are there
    if src["01.jpg"].size != (1280, 868) or src["02.jpg"].size != (888, 1280):
        raise SystemExit("01.jpg / 02.jpg are not the collages; run extract_founder_images.py first")
    for i, (name, box) in enumerate(CUTS, 1):
        src[name].crop(box).save(DIR / f"{i:02d}.jpg", quality=92)
    print(f"{len(CUTS)} photographs in {DIR}")

if __name__ == "__main__":
    main()
