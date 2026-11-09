#!/usr/bin/env python3
"""Cut the early-project photographs out of Evgenii Abramov's portfolio deck.

The last section of "Portfolio Abramov.pptx" ("Others projects", slides
135-141) is seven scanned print pages, each a collage of photographs on an
olive background, stored on its side. This rotates each page upright and
cuts the photographs out at the resolution of the scan — nothing is upscaled.

    python3 tools/extract_abramov_pages.py "/path/to/Portfolio Abramov.pptx"
    python3 tools/extract_abramov_pages.py /folder/with/image164.jpeg...   # media already pulled out

Pages already covered by the chronicle at better resolution (ZiL-41047, the
S600 partition, the taxi) are not cut: the photographs there are the same
ones, from Iliya's archive, at two to three times the size.
"""

import io
import pathlib
import sys
import zipfile

from PIL import Image

ROOT = pathlib.Path(__file__).parent.parent
OUT = ROOT / "static" / "img" / "founder"

# media file in the deck -> list of (output path, box on the upright page).
# Boxes were found by thresholding against the olive page colour and then
# inset a few pixels so no page colour shows at the edges.
INSET = 6
PAGES = {
    # slide 135, "Creating unique cars, made in 1992-2003" (Cardi)
    "image164.jpeg": [
        ("cardi/01.jpg", (68, 37, 992, 646)),
        ("cardi/02.jpg", (1011, 37, 1615, 339)),
        ("cardi/03.jpg", (1012, 368, 1618, 700)),
        ("cardi/04.jpg", (72, 668, 994, 1084)),
        ("cardi/05.jpg", (1015, 724, 1617, 1084)),
    ],
    # slide 138, "Changing the interior and the face of the Mercedes-Benz Viano", 2008
    "image167.jpeg": [
        ("viano/01.jpg", (882, 39, 1619, 490)),
        ("viano/02.jpg", (128, 514, 865, 1086)),
        ("viano/03.jpg", (882, 514, 1619, 1088)),
    ],
    # slide 139, "Motorized monitor for the Mercedes-Benz Viano", 2008
    "image168.jpeg": [
        ("viano/04.jpg", (127, 37, 776, 604)),
        ("viano/05.jpg", (792, 38, 1620, 455)),
        ("viano/06.jpg", (130, 620, 778, 1085)),
    ],
    # slide 140, "Changing the interior of the Rolls-Royce Phantom", 2009
    "image169.jpeg": [
        ("phantom/01.jpg", (129, 53, 1067, 371)),
        ("phantom/02.jpg", (129, 371, 1067, 1087)),
        ("phantom/03.jpg", (1097, 53, 1617, 371)),
        ("phantom/04.jpg", (1097, 371, 1621, 1087)),
    ],
}


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    src = pathlib.Path(sys.argv[1])
    if src.is_dir():
        read = lambda name: (src / name).read_bytes()
    else:
        deck = zipfile.ZipFile(src)
        read = lambda name: deck.read(f"ppt/media/{name}")
    for media, cuts in PAGES.items():
        page = Image.open(io.BytesIO(read(media)))
        page = page.rotate(270, expand=True).convert("RGB")   # stored on its side
        for rel, (x0, y0, x1, y1) in cuts:
            box = (x0 + INSET, y0 + INSET, x1 - INSET, y1 - INSET)
            out = OUT / rel
            out.parent.mkdir(parents=True, exist_ok=True)
            page.crop(box).save(out, quality=90, optimize=True, progressive=True)
            print(f"  {rel:22s} {box[2] - box[0]}x{box[3] - box[1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
