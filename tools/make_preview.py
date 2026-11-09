#!/usr/bin/env python3
"""Build standalone, single-file previews of chosen pages.

Inlines the stylesheet, the script and every local image as a data URI, so the
resulting file opens straight from disk or can be emailed to someone for review
without running a web server.

    python3 tools/make_preview.py                        # minimal theme, default pages
    python3 tools/make_preview.py --dist=dist-lux        # lux theme
    python3 tools/make_preview.py --dist=dist-lux /ru/   # a specific page
"""

import base64
import io
import mimetypes
import pathlib
import re
import sys

from PIL import Image

# Previews inline every image, so they are downscaled to keep the single file
# openable. The built site in dist/ always uses the full-size originals.
PREVIEW_MAX_W = 900
PREVIEW_QUALITY = 76

ROOT = pathlib.Path(__file__).parent.parent
OUT = ROOT / "preview"

DEFAULT_PAGES = ["/", "/portfolio/mercedes-benz-v-class-line-1/", "/partners/", "/ru/"]


def data_uri(path):
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    if mime in ("image/jpeg", "image/png"):
        im = Image.open(path).convert("RGB")
        if im.width > PREVIEW_MAX_W:
            im = im.resize(
                (PREVIEW_MAX_W, round(im.height * PREVIEW_MAX_W / im.width)),
                Image.LANCZOS,
            )
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=PREVIEW_QUALITY, optimize=True)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}"


def inline(dist, prefix, page_url):
    src = dist / "index.html" if page_url == "/" else dist / page_url.strip("/") / "index.html"
    if not src.exists():
        print(f"  missing: {page_url}")
        return None
    html = src.read_text(encoding="utf-8")

    def swap_css(match):
        css_file = dist / match.group(1).lstrip("/")
        if not css_file.exists():
            return match.group(0)
        return "<style>\n" + css_file.read_text(encoding="utf-8") + "\n</style>"

    html = re.sub(r'<link rel="stylesheet" href="(/static/css/[^"]+)">', swap_css, html)

    def swap_js(match):
        js_file = dist / match.group(1).lstrip("/")
        if not js_file.exists():
            return match.group(0)
        return "<script>\n" + js_file.read_text(encoding="utf-8") + "\n</script>"

    html = re.sub(r'<script src="(/static/js/[^"]+)" defer></script>', swap_js, html)

    def swap_img(match):
        attr, url = match.group(1), match.group(2)
        local = dist / url.lstrip("/")
        if local.is_file():
            return f'{attr}="{data_uri(local)}"'
        return match.group(0)

    html = re.sub(r'(src|href)="(/static/img/[^"]+)"', swap_img, html)

    name = "home" if page_url == "/" else page_url.strip("/").replace("/", "-")
    dest = OUT / f"{prefix}-{name}.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8")
    print(f"  {dest.relative_to(ROOT)}  ({dest.stat().st_size / 1024:.0f} KB)")
    return dest


def main(argv):
    dist_name = "dist"
    args = list(argv)
    if args and args[0].startswith("--dist="):
        dist_name = args.pop(0).split("=", 1)[1]

    dist = ROOT / dist_name
    if not dist.exists():
        print(f"{dist_name} does not exist — run build.py first")
        return 1

    prefix = "7pro8"

    print("standalone previews:")
    for page in args or DEFAULT_PAGES:
        inline(dist, prefix, page)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
