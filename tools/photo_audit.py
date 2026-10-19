#!/usr/bin/env python3
"""Audit every photograph the site uses: where it appears, how big it is,
and whether it is good enough to launch with.

The question this answers is not "does the file exist" — build.py already
reports that — but "is this file large enough for the slot it is shown in".
A 430 px wide photograph dropped into a 604 px wide card is what makes a page
look soft, and that is invisible in a file listing.

For every image reference in content/en.json the audit works out:

  * the slot width in CSS pixels at the widest desktop layout (the shell is
    78rem = 1248 px), from the block type and its column count;
  * the stored pixel width of the file;
  * a verdict — ok / tight / replace — from the ratio between the two, plus
    whether the file also covers a 2x display.

Provenance is recorded as well, because it says what a replacement would take:
an image lifted from the partner deck can only ever be as good as the deck's
embedded original, while an archive scan may have a better original somewhere.

    python3 tools/photo_audit.py          # table on stdout
    python3 tools/photo_audit.py --json   # machine-readable

build.py imports `collect()` to render the service page at /_photos/.
"""

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent.parent
CONTENT = ROOT / "content"
IMG = ROOT / "static" / "img"

# Content shell: 78rem at the 16px root = 1248 px. Grid gap ~40 px.
SHELL = 1248
GAP = 40
# The chronicle entry puts its gallery in the right-hand column, after a 9rem
# year gutter and the column gap.
CHRONICLE_COL = SHELL - 144 - 56

# Below this share of the slot width the image is visibly soft on a normal
# display and has to be replaced; between the two it is usable but tight.
REPLACE_BELOW = 0.75
TIGHT_BELOW = 1.0


def slot_width(block_type, cols, column_span=SHELL):
    """How wide, in CSS pixels, this image is painted at the widest layout."""
    if block_type == "hero":
        return 1920  # full-bleed, not limited by the shell
    if block_type in ("split", "duo"):
        return (SHELL - GAP) // 2
    if block_type == "projects":
        return (SHELL - GAP) // 2
    if block_type in ("gallery", "chronicle"):
        n = max(1, int(cols or 3))
        return (column_span - GAP * (n - 1)) // n
    return SHELL


def _image_size(path):
    """Pixel size of an image file, read from its header.

    The build runs this on every image on every build, including in CI, so it
    deliberately does not import Pillow: the site build should not acquire an
    image-processing dependency just to read two integers. The extraction tools
    in this folder do use Pillow, and they are run by hand.
    """
    suffix = path.suffix.lower()
    if suffix == ".svg":
        text = path.read_text(encoding="utf-8", errors="ignore")[:2000]
        m = re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', text)
        if m:
            return int(float(m.group(1))), int(float(m.group(2)))
        m = re.search(r'\bwidth="([\d.]+)"[^>]*\bheight="([\d.]+)"', text)
        if m:
            return int(float(m.group(1))), int(float(m.group(2)))
        return 0, 0

    with open(path, "rb") as fh:
        head = fh.read(32)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            return (int.from_bytes(head[16:20], "big"),
                    int.from_bytes(head[20:24], "big"))
        if head[:6] in (b"GIF87a", b"GIF89a"):
            return (int.from_bytes(head[6:8], "little"),
                    int.from_bytes(head[8:10], "little"))
        if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
            return _webp_size(fh, head)
        if head[:2] == b"\xff\xd8":
            return _jpeg_size(fh)
    return 0, 0


def _jpeg_size(fh):
    """Walk the JPEG segments to the frame header that carries the size."""
    fh.seek(2)
    while True:
        b = fh.read(1)
        if not b:
            return 0, 0
        if b != b"\xff":
            continue
        marker = fh.read(1)
        while marker == b"\xff":          # fill bytes are legal between segments
            marker = fh.read(1)
        if not marker:
            return 0, 0
        m = marker[0]
        if m in (0xD8, 0xD9) or 0xD0 <= m <= 0xD7:
            continue                       # standalone markers carry no length
        length_bytes = fh.read(2)
        if len(length_bytes) < 2:
            return 0, 0
        length = int.from_bytes(length_bytes, "big")
        # SOF0..SOF15, except the four that are not frame headers
        if 0xC0 <= m <= 0xCF and m not in (0xC4, 0xC8, 0xCC):
            data = fh.read(5)
            if len(data) < 5:
                return 0, 0
            return (int.from_bytes(data[3:5], "big"),
                    int.from_bytes(data[1:3], "big"))
        fh.seek(length - 2, 1)


def _webp_size(fh, head):
    """VP8, VP8L and VP8X each state the size differently."""
    fh.seek(12)
    chunk = fh.read(8)
    if len(chunk) < 8:
        return 0, 0
    kind = chunk[:4]
    if kind == b"VP8X":
        data = fh.read(10)
        if len(data) < 10:
            return 0, 0
        w = int.from_bytes(data[4:7], "little") + 1
        h = int.from_bytes(data[7:10], "little") + 1
        return w, h
    if kind == b"VP8 ":
        data = fh.read(10)
        if len(data) < 10 or data[3:6] != b"\x9d\x01\x2a":
            return 0, 0
        return (int.from_bytes(data[6:8], "little") & 0x3FFF,
                int.from_bytes(data[8:10], "little") & 0x3FFF)
    if kind == b"VP8L":
        data = fh.read(5)
        if len(data) < 5 or data[0] != 0x2F:
            return 0, 0
        bits = int.from_bytes(data[1:5], "little")
        return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    return 0, 0


def _provenance():
    """Which tool produced which file, read from the extraction scripts.

    Reading the scripts rather than hard-coding a second list means the audit
    cannot drift away from what actually generated the images.
    """
    out = {}
    deck = ROOT / "tools" / "extract_deck_images.py"
    if deck.exists():
        for m in re.finditer(r'\("([^"]+\.jpg)", (\d+), \(', deck.read_text(encoding="utf-8")):
            out[m.group(1)] = f"partner deck, slide {m.group(2)}"
    founder = ROOT / "tools" / "extract_founder_images.py"
    if founder.exists():
        text = founder.read_text(encoding="utf-8")
        for m in re.finditer(r'"(founder/[^"]+\.jpg)"', text):
            out.setdefault(m.group(1), "project archive / scan")
    return out


def collect(lang="en"):
    """Every image reference in the content, with its slot and verdict."""
    path = CONTENT / f"{lang}.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    prov = _provenance()

    uses = {}

    def note(src, alt, page, block_type, cols, span=SHELL):
        if not src or src.startswith(("http", "data:")):
            return
        rel = src.lstrip("/")
        rec = uses.setdefault(rel, {"src": rel, "uses": [], "alt": alt})
        rec["uses"].append(
            {
                "page": page,
                "block": block_type,
                "slot": slot_width(block_type, cols, span),
            }
        )
        if alt and not rec.get("alt"):
            rec["alt"] = alt

    for page in data.get("pages", []):
        slug = page.get("slug") or "index"
        for block in page.get("blocks", []):
            bt = block.get("type")
            if bt == "hero" and isinstance(block.get("image"), dict):
                note(block["image"].get("src"), block["image"].get("alt"), slug, "hero", None)
            if bt == "split" and isinstance(block.get("image"), dict):
                note(block["image"].get("src"), block["image"].get("alt"), slug, "split", None)
            if bt == "split" and block.get("src"):
                note(block.get("src"), block.get("alt"), slug, "split", None)
            if bt == "gallery":
                cols = block.get("cols") or 3
                for im in block.get("items", []):
                    note(im.get("src"), im.get("alt"), slug, "gallery", cols)
            if bt == "projects":
                for it in block.get("items", []):
                    note(it.get("image"), it.get("title"), slug, "projects", None)
            if bt == "duo":
                for person in block.get("people", []):
                    note(person.get("portrait"), person.get("name"), slug, "duo", None)
            if bt == "chronicle":
                for e in block.get("entries", []):
                    cols = e.get("cols") or 3
                    for im in e.get("images", []):
                        note(im.get("src"), im.get("alt"), slug, "chronicle", cols, CHRONICLE_COL)

    rows = []
    for rel, rec in uses.items():
        f = IMG / rel
        if f.exists():
            w, h = _image_size(f)
            kb = f.stat().st_size // 1024
            missing = False
        else:
            w = h = kb = 0
            missing = True
        need = max(u["slot"] for u in rec["uses"])
        ratio = (w / need) if need and w else 0.0
        if missing:
            verdict, note_text = "missing", "no file — the page shows a placeholder"
        elif ratio < REPLACE_BELOW:
            verdict, note_text = "replace", "too small for the slot — visibly soft; needs a new original"
        elif ratio < TIGHT_BELOW:
            verdict, note_text = "tight", "just under the slot width — acceptable, better replaced"
        elif ratio < 1.5:
            verdict, note_text = "ok", "fills the slot on a normal display, not on a 2x screen"
        else:
            verdict, note_text = "good", "covers the slot on a 2x display"
        rows.append(
            {
                "src": rel,
                "alt": rec.get("alt") or "",
                "width": w,
                "height": h,
                "kb": kb,
                "slot": need,
                "ratio": round(ratio, 2),
                "verdict": verdict,
                "note": note_text,
                "source": prov.get(rel, "supplied separately"),
                "uses": rec["uses"],
            }
        )

    rows.sort(key=lambda r: ({"missing": 0, "replace": 1, "tight": 2, "ok": 3, "good": 4}[r["verdict"]], r["src"]))
    return rows


# Referenced from the page head, the manifest or site.json rather than from a
# content block, so the block walk above never sees them.
NON_BLOCK = {"favicon.svg", "logo-7pro8.svg", "share/7pro8-share.jpg"}


def unused():
    """Files in static/img that no page references — candidates for deletion."""
    referenced = {r["src"] for r in collect()} | NON_BLOCK
    out = []
    for f in sorted(IMG.rglob("*")):
        if not f.is_file() or f.name.startswith("."):
            continue
        rel = str(f.relative_to(IMG))
        if rel not in referenced:
            out.append(rel)
    return out


def summary(rows):
    counts = {}
    for r in rows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    return counts


def main():
    rows = collect()
    if "--json" in sys.argv:
        print(json.dumps({"images": rows, "unused": unused()}, indent=2))
        return 0
    print(f"{'file':46s} {'stored':>11s} {'slot':>6s} {'×':>5s}  verdict")
    print("-" * 92)
    for r in rows:
        size = f"{r['width']}x{r['height']}" if r["width"] else "—"
        print(f"{r['src']:46s} {size:>11s} {r['slot']:>6d} {r['ratio']:>5.2f}  {r['verdict']}")
    print("\n" + ", ".join(f"{v}: {n}" for v, n in sorted(summary(rows).items())))
    u = unused()
    if u:
        print(f"\n{len(u)} files in static/img are not referenced by any page:")
        for rel in u[:20]:
            print(f"  {rel}")
        if len(u) > 20:
            print(f"  … and {len(u) - 20} more")
    return 0


if __name__ == "__main__":
    sys.exit(main())
