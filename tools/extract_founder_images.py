#!/usr/bin/env python3
"""Collect the founder-page photography from the project archives and scans.

Sources are two directories: the unpacked per-project archives, and the loose
scans of film prints. Everything is resized to a common maximum width and
written into static/img/founder/<entry>/.

    python3 tools/extract_founder_images.py <archives-dir> <scans-dir>
"""

import pathlib
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).parent.parent
OUT = ROOT / "static" / "img" / "founder"
MAX_W = 1400

# entry slug -> (source directory, [file names in display order])
FROM_ARCHIVES = {
    "scooter": ("SCOOTER_2022", [
        "photo_2023-03-02_19-55-21.jpg",
        "photo_2023-03-02_20-07-02.jpg",
        "photo_2023-03-02_20-07-11.jpg",
    ]),
    "princess": ("PRINCESS", ["1241770642_7133.jpg", "15.jpg", "16.jpg"]),
    "plafon": ("PLAFON", ["11.JPG", "13.JPG", "15.JPG", "17.jpg"]),
    "zil": ("ZIL_INTERIOR", ["ZiL_01.jpg", "ZiL_04.jpg", "ZiL_03.jpg"]),
    "w221": ("W221_1st_PARTITION_WALL", ["50.jpg", "51.jpg", "52.jpg", "54.jpg"]),
    "vito": ("MERCEDES_VITO", ["1.jpg", "10b.jpg", "11b.jpg", "13b.jpg"]),
    "diablo": ("Lamborghini_Diablo_VT_2004", ["1b.jpg", "19b.jpg", "20b.jpg", "24b.jpg"]),
    "corvette": ("Corvette_2003_RED", ["0.jpg", "1b.jpg", "7b.jpg"]),
    "hummer": ("Hummer_1_Киркоров", ["1b.jpg", "5b.jpg", "7b.jpg", "12b.jpg"]),
    "lincoln": ("Lincoln_Reincarnation_2001", ["1b.jpg", "2b.jpg", "3b.jpg", "10b.jpg"]),
}

# entry slug -> [scan file names in display order]
FROM_SCANS = {
    "team": [
        "photo_2026-09-09_14-29-09.jpg",
        "photo_2026-09-09_14-29-09__2_.jpg",
        "photo_2026-09-09_14-29-09__3_.jpg",
        "photo_2026-09-09_14-37-31.jpg",
    ],
    "workshop": [
        "photo_2026-09-09_14-10-03.jpg",
        "photo_2026-09-09_15-27-09.jpg",
    ],
    "marine": ["photo_2026-09-09_14-10-04.jpg"],
    "zaz": ["photo_2026-09-09_14-15-52.jpg", "photo_2026-09-09_14-15-53.jpg"],
    "press": ["photo_2026-09-09_14-10-03__2_.jpg"],
}


def save(src, dest):
    im = Image.open(src).convert("RGB")
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest, quality=86, optimize=True, progressive=True)
    return im.size


def main(archives, scans):
    archives, scans = pathlib.Path(archives), pathlib.Path(scans)
    n = 0
    for slug, (folder, names) in FROM_ARCHIVES.items():
        for i, name in enumerate(names, 1):
            src = archives / folder / name
            if not src.exists():
                matches = list((archives / folder).rglob(name))
                if not matches:
                    print(f"  missing {folder}/{name}")
                    continue
                src = matches[0]
            size = save(src, OUT / slug / f"{i:02d}.jpg")
            n += 1
            print(f"  founder/{slug}/{i:02d}.jpg  {size[0]}x{size[1]}")
    for slug, names in FROM_SCANS.items():
        for i, name in enumerate(names, 1):
            src = scans / name
            if not src.exists():
                print(f"  missing scan {name}")
                continue
            size = save(src, OUT / slug / f"{i:02d}.jpg")
            n += 1
            print(f"  founder/{slug}/{i:02d}.jpg  {size[0]}x{size[1]}")
    print(f"\n{n} images written to {OUT}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    sys.exit(main(sys.argv[1], sys.argv[2]))
