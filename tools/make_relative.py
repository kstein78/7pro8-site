#!/usr/bin/env python3
"""Turn dist/ into a relative-URL copy that works from any sub-path.

The production build uses root-absolute links (/partners/, /static/css/...),
which is right for 7pro8.com but breaks the moment the site is served from a
sub-path — a preview host, an artifact, a file:// folder. This writes
dist-relative/ where every internal link is relative and points at an explicit
index.html, and only the images actually referenced are copied.

    python3 tools/make_relative.py              # after build.py
    python3 tools/make_relative.py --artifact   # also prepare the entry page
                                                # for hosting as a claude.ai artifact
"""

import json
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


def prepare_entry(title="7pro8.com"):
    """Artifact hosting wraps the entry page in its own document skeleton, so
    the entry file must not carry doctype/html/head/body of its own."""
    p = OUT / "index.html"
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"<!DOCTYPE html>\s*", "", s, flags=re.I)
    s = re.sub(r"<html[^>]*>\s*", "", s, count=1)
    s = re.sub(r"</?head>\s*", "", s)
    s = re.sub(r"<body[^>]*>\s*", "", s, count=1)
    s = s.replace("</body>", "").replace("</html>", "")
    s = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", s, count=1, flags=re.S)
    p.write_text(s, encoding="utf-8")
    listing = sorted(str(f.relative_to(OUT)) for f in OUT.rglob("*")
                     if f.is_file() and f.name != "index.html" or (f.is_file() and f.parent != OUT))
    (OUT.parent / "dist-relative.files.json").write_text(json.dumps(listing), encoding="utf-8")
    print(f"entry page prepared; {len(listing)} supporting files listed in dist-relative.files.json")


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
    # fonts are referenced from the stylesheet, not the pages
    fonts = {str(f.relative_to(SRC)) for f in (SRC / "static/fonts").glob("*.woff2")}
    for asset in used_assets | fonts | {"static/css/site.css", "static/js/site.js"}:
        src = SRC / asset
        if src.exists():
            dst = OUT / asset
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    # site-level files that are not pages and are not referenced from any page
    for extra in ("robots.txt",):
        src = SRC / extra
        if src.exists():
            shutil.copy2(src, OUT / extra)
    # 404.html is deliberately not copied: its links are root-absolute, which
    # cannot work from a sub-path, and the host's own 404 page is fine for a
    # preview. Production serves dist/404.html from the site root.

    files = [p for p in OUT.rglob("*") if p.is_file()]
    size = sum(p.stat().st_size for p in files) / 1e6
    print(f"{len(pages)} pages, {len(files)} files, {size:.1f} MB in {OUT.name}/")
    if "--artifact" in sys.argv:
        prepare_entry()
    return 0


if __name__ == "__main__":
    sys.exit(main())
