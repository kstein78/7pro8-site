#!/usr/bin/env python3
"""Turn dist/ into a relative-URL copy that works from any sub-path.

The production build uses root-absolute links (/partners/, /static/css/...),
which is right for 7pro8.com but breaks the moment the site is served from a
sub-path — a preview host, an artifact, a file:// folder. This writes
dist-relative/ where every internal link is relative and points at an explicit
index.html, and only the images actually referenced are copied.

    python3 tools/make_relative.py            # after build.py
"""

import os
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).parent.parent
SRC = ROOT / "dist"
OUT = ROOT / "dist-relative"

ATTR = re.compile(r'(href|src)="(/[^"]*)"')


def rel_target(from_dir, url):
    path, _, frag = url.partition("#")
    path, _, query = path.partition("?")
    if path.endswith("/") or path == "":
        path = path + "index.html"
    target = path.lstrip("/")
    rel = os.path.relpath(target, from_dir.as_posix() or ".")
    if query:
        rel += "?" + query
    if frag:
        rel += "#" + frag
    return rel


def main():
    if not SRC.exists():
        print("run build.py first")
        return 1
    if OUT.exists():
        shutil.rmtree(OUT)

    redirect_dirs = set()
    used_assets = set()
    pages = []
    for f in SRC.rglob("index.html"):
        html = f.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in html:
            redirect_dirs.add(f.parent)
            continue
        pages.append(f)

    for f in pages:
        rel_dir = f.parent.relative_to(SRC)
        html = f.read_text(encoding="utf-8")

        def swap(m):
            attr, url = m.group(1), m.group(2)
            if url.startswith("//"):
                return m.group(0)
            if url.startswith("/static/"):
                used_assets.add(url.split("#")[0].split("?")[0].lstrip("/"))
            return f'{attr}="{rel_target(rel_dir, url)}"'

        html = ATTR.sub(swap, html)
        dest = OUT / rel_dir / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")

    # stylesheet and script are always needed; images only when referenced
    for asset in used_assets | {"static/css/site.css", "static/js/site.js"}:
        src = SRC / asset
        if src.exists():
            dst = OUT / asset
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    files = [p for p in OUT.rglob("*") if p.is_file()]
    size = sum(p.stat().st_size for p in files) / 1e6
    print(f"{len(pages)} pages, {len(files)} files, {size:.1f} MB in {OUT.name}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
