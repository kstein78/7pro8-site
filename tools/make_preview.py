#!/usr/bin/env python3
"""Build standalone, single-file previews of chosen pages.

Inlines the stylesheet, the script and every local image as a data URI, so the
resulting file can be opened straight from disk or emailed to someone for
review without running a web server.

    python3 tools/make_preview.py                 # default set of pages
    python3 tools/make_preview.py /ru/ /partners/ # specific pages
"""

import base64
import mimetypes
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent.parent
DIST = ROOT / "dist"
OUT = ROOT / "preview"

DEFAULT_PAGES = ["/", "/portfolio/mercedes-benz-v-class-line-1/", "/partners/", "/ru/"]


def data_uri(path):
    mime, _ = mimetypes.guess_type(path.name)
    if mime is None:
        mime = "application/octet-stream"
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}"


def inline(page_url):
    src = DIST / page_url.strip("/") / "index.html" if page_url != "/" else DIST / "index.html"
    if not src.exists():
        print(f"  missing: {page_url}")
        return None
    html = src.read_text(encoding="utf-8")

    # stylesheet
    css = (DIST / "static/css/site.css").read_text(encoding="utf-8")
    html = re.sub(
        r'<link rel="stylesheet" href="/static/css/site\.css">',
        f"<style>\n{css}\n</style>",
        html,
    )

    # script
    js = (DIST / "static/js/site.js").read_text(encoding="utf-8")
    html = re.sub(
        r'<script src="/static/js/site\.js" defer></script>',
        f"<script>\n{js}\n</script>",
        html,
    )

    # images and favicon
    def swap(match):
        attr, url = match.group(1), match.group(2)
        local = DIST / url.lstrip("/")
        if local.exists() and local.is_file():
            return f'{attr}="{data_uri(local)}"'
        return match.group(0)

    html = re.sub(r'(src|href)="(/static/img/[^"]+)"', swap, html)

    # internal links go nowhere in a standalone file — make that visible rather
    # than letting a reviewer click into a broken page
    html = html.replace("<body ", '<body data-preview="true" ')

    name = "home" if page_url == "/" else page_url.strip("/").replace("/", "-")
    dest = OUT / f"7pro8-preview-{name}.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html, encoding="utf-8")
    size = dest.stat().st_size / 1024
    print(f"  {dest.relative_to(ROOT)}  ({size:.0f} KB)")
    return dest


if __name__ == "__main__":
    pages = sys.argv[1:] or DEFAULT_PAGES
    print("standalone previews:")
    for page in pages:
        inline(page)
