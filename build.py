#!/usr/bin/env python3
"""
7pro8.com static site builder.

Reads content/site.json (shared config) and content/<lang>.json (per-language
content), renders every page through templates/page.html and writes a fully
static tree to dist/ that can be served by any web server.

Usage:
    python3 build.py            # build into dist/
    python3 build.py --serve    # build, then serve dist/ on :8000
"""

import argparse
import html
import json
import os
import shutil
import sys
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

sys.path.insert(0, str(Path(__file__).parent / "tools"))
import i18n  # noqa: E402

ROOT = Path(__file__).parent.resolve()
CONTENT = ROOT / "content"
STATIC = ROOT / "static"
TEMPLATES = ROOT / "templates"

DIST = ROOT / "dist"

# Preview builds (GitHub Pages, any staging host) must not be indexed: the draft
# should never outrank or pre-empt the real site. Set SITE_PREVIEW=1.
PREVIEW = os.environ.get("SITE_PREVIEW") == "1"

MISSING_IMAGES = []


# --------------------------------------------------------------------------
# image handling
# --------------------------------------------------------------------------

PLACEHOLDER_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" \
role="img" aria-label="{alt}">
  <rect width="1200" height="800" fill="{bg}"/>
  <g fill="none" stroke="{line}" stroke-width="2">
    <path d="M0 0 L1200 800 M1200 0 L0 800"/>
    <rect x="1" y="1" width="1198" height="798"/>
  </g>
  <rect x="360" y="330" width="480" height="140" fill="{bg}" stroke="{line}"/>
  <text x="600" y="382" font-family="Helvetica, Arial, sans-serif" font-size="26"
        fill="{text}" text-anchor="middle">photo to be supplied</text>
  <text x="600" y="424" font-family="Helvetica, Arial, sans-serif" font-size="20"
        fill="{dim}" text-anchor="middle">{short}</text>
</svg>
"""

PALETTE = {"bg": "#16181c", "line": "#33302a", "text": "#c0a265", "dim": "#6d6a64"}


def resolve_image(src, alt=""):
    """Return a usable URL for an image reference.

    If static/img/<src> exists it is used as-is. If it does not, a labelled
    SVG placeholder is generated so the layout can be reviewed before the
    photography is dropped in. Every miss is reported at the end of the build.
    """
    if not src:
        return ""
    if src.startswith(("http://", "https://", "data:")):
        return src

    rel = src.lstrip("/")
    real = STATIC / "img" / rel
    if real.exists():
        return f"/static/img/{rel}"

    if rel not in MISSING_IMAGES:
        MISSING_IMAGES.append(rel)

    ph_rel = f"_placeholder/{rel}.svg"
    ph_path = DIST / "static" / "img" / ph_rel
    ph_path.parent.mkdir(parents=True, exist_ok=True)
    short = rel
    ph_path.write_text(
        PLACEHOLDER_SVG.format(alt=html.escape(rel), short=html.escape(short), **PALETTE),
        encoding="utf-8",
    )
    return f"/static/img/{ph_rel}"


# --------------------------------------------------------------------------
# build
# --------------------------------------------------------------------------


def load(name):
    with open(CONTENT / name, encoding="utf-8") as fh:
        return json.load(fh)


def page_url(lang, slug, default_lang):
    """URL for a page. The default language lives at the site root."""
    prefix = "" if lang == default_lang else f"/{lang}"
    if slug in ("", "index", "/"):
        return f"{prefix}/" if prefix else "/"
    return f"{prefix}/{slug.strip('/')}/"


UNTRANSLATED = {}


def content_for(lang):
    """Hand-written content/<lang>.json wins; otherwise generate from the
    English source and content/i18n/<lang>.json."""
    path = CONTENT / f"{lang}.json"
    if path.exists():
        return load(f"{lang}.json")
    data, missing = i18n.generate(lang)
    if data is not None:
        UNTRANSLATED[lang] = missing
    return data


def build():
    MISSING_IMAGES.clear()
    UNTRANSLATED.clear()

    site = load("site.json")
    default_lang = site["default_language"]
    langs = [l["code"] for l in site["languages"]]

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.globals["img"] = resolve_image
    env.globals["build_year"] = date.today().year
    env.globals["preview"] = PREVIEW

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)

    # static assets
    shutil.copytree(STATIC, DIST / "static", dirs_exist_ok=True)

    all_urls = []
    page_template = env.get_template("page.html")

    available = {
        l["code"] for l in site["languages"]
        if (CONTENT / f"{l['code']}.json").exists() or (CONTENT / "i18n" / f"{l['code']}.json").exists()
    }

    for lang_meta in site["languages"]:
        lang = lang_meta["code"]
        data = content_for(lang)
        if data is None:
            print(f"  skip {lang}: no content file and no translation table")
            continue

        pages = data["pages"]
        # every page needs to know where its siblings live, for the nav and
        # for the language switcher
        for page in pages:
            page["url"] = page_url(lang, page["slug"], default_lang)

        by_slug = {p["slug"]: p for p in pages}

        for page in pages:
            alternates = []
            for other in site["languages"]:
                if other["code"] not in langs:
                    continue
                alternates.append(
                    {
                        "code": other["code"],
                        "hreflang": other.get("html_lang", other["code"]),
                        "label": other["label"],
                        "url": page_url(other["code"], page["slug"], default_lang),
                        "current": other["code"] == lang,
                        "available": other["code"] in available,
                    }
                )

            nav = []
            for item in data["nav"]:
                target = by_slug.get(item["slug"])
                if not target:
                    continue
                nav.append(
                    {
                        "label": item["label"],
                        "url": target["url"],
                        "current": target["slug"] == page["slug"],
                    }
                )

            rendered = page_template.render(
                site=site,
                lang=lang,
                lang_meta=lang_meta,
                data=data,
                page=page,
                nav=nav,
                alternates=alternates,
                pages=by_slug,
            )

            out_dir = DIST / page["url"].strip("/")
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "index.html").write_text(rendered, encoding="utf-8")

            if not page.get("noindex"):
                all_urls.append(
                    (site["base_url"].rstrip("/") + page["url"], page.get("changed", ""))
                )

        print(f"  {lang}: {len(pages)} pages")

    # sitemap + robots
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, changed in all_urls:
        sitemap.append("  <url>")
        sitemap.append(f"    <loc>{html.escape(url)}</loc>")
        if changed:
            sitemap.append(f"    <lastmod>{changed}</lastmod>")
        sitemap.append("  </url>")
    sitemap.append("</urlset>")
    (DIST / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")

    # Redirect stubs: old addresses (the Squarespace site, renamed pages) keep
    # working on any static host. The Caddyfile gets proper 301s as well.
    REDIRECT_HTML = (
        '<!DOCTYPE html><html><head><meta charset="utf-8">'
        '<title>Moved</title><meta name="robots" content="noindex">'
        '<link rel="canonical" href="{abs}">'
        '<meta http-equiv="refresh" content="0; url=/{new}"></head>'
        '<body><a href="/{new}">{abs}</a></body></html>\n'
    )
    for old, new in site.get("redirects", {}).items():
        stub = DIST / old.strip("/") / "index.html"
        if stub.exists():
            continue
        stub.parent.mkdir(parents=True, exist_ok=True)
        stub.write_text(
            REDIRECT_HTML.format(new=new, abs=site["base_url"].rstrip("/") + "/" + new),
            encoding="utf-8",
        )
    caddy = ["# generated by build.py — paste inside the www.7pro8.com block"]
    for old, new in site.get("redirects", {}).items():
        caddy.append(f"redir /{old.rstrip('/')} /{new} permanent")
        caddy.append(f"redir /{old} /{new} permanent")
    (DIST / "_redirects.caddy").write_text("\n".join(caddy) + "\n", encoding="utf-8")

    (DIST / "404.html").write_text(
        env.get_template("404.html").render(site=site), encoding="utf-8"
    )

    if PREVIEW:
        (DIST / "robots.txt").write_text(
            "# preview build — not for indexing\nUser-agent: *\nDisallow: /\n",
            encoding="utf-8",
        )
    else:
        (DIST / "robots.txt").write_text(
            "User-agent: *\nAllow: /\n\nSitemap: "
            + site["base_url"].rstrip("/")
            + "/sitemap.xml\n",
            encoding="utf-8",
        )

    print(f"\nBuilt {len(all_urls)} pages into {DIST}"
          + (" (preview: noindex)" if PREVIEW else ""))

    for lang, missing in UNTRANSLATED.items():
        report = DIST / f"_untranslated-{lang}.txt"
        report.write_text("\n".join(missing) + ("\n" if missing else ""), encoding="utf-8")
        state = f"{len(missing)} strings still in English" if missing else "fully translated"
        print(f"{lang}: {state}" + (f" (see {report.name})" if missing else ""))

    if MISSING_IMAGES:
        report = DIST / "_missing-images.txt"
        report.write_text("\n".join(sorted(MISSING_IMAGES)) + "\n", encoding="utf-8")
        print(
            f"{len(MISSING_IMAGES)} image slots are still placeholders "
            f"(list written to {report.name}; see IMAGES.md)"
        )
    return 0


def serve(port=8000):
    import http.server
    import socketserver

    os.chdir(DIST)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"serving {DIST.name}/ on http://localhost:{port}")
        httpd.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    rc = build()
    if args.serve:
        serve(args.port)
    sys.exit(rc)
