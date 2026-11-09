#!/usr/bin/env python3
"""Check that every internal link and asset reference in dist/ resolves."""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent.parent
DIST = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "dist")


def main():
    pages = set()
    for p in DIST.rglob("index.html"):
        rel = p.parent.relative_to(DIST).as_posix()
        pages.add("/" if rel == "." else f"/{rel}/")

    bad = []
    for f in DIST.rglob("index.html"):
        html = f.read_text(encoding="utf-8")
        for href in re.findall(r'href="([^"]+)"', html) + re.findall(r'src="([^"]+)"', html):
            if href.startswith(("http", "mailto:", "tel:", "#", "data:")):
                continue
            target = href.split("#")[0]
            if not target:
                continue
            if target.startswith("/static/"):
                if not (DIST / target.lstrip("/")).exists():
                    bad.append((str(f.relative_to(DIST)), href, "missing asset"))
            elif target not in pages:
                bad.append((str(f.relative_to(DIST)), href, "no such page"))

    print(f"{DIST.name}: {len(pages)} pages")
    if bad:
        print("BROKEN:")
        for item in sorted(set(bad)):
            print("  ", *item)
        return 1
    print("all internal links and assets resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
