#!/usr/bin/env python3
"""Generate translated content files from English plus a translation table.

content/en.json is the source. For each language in content/i18n/<lang>.json
(a table of short hash -> translated string), this produces the full content
structure in that language: every human-readable string is looked up by the
hash of its English text, and every internal link gets the language prefix.

If the English text of a string changes, its hash changes, so the string shows
up as untranslated instead of silently keeping a stale translation. Missing
strings fall back to English and are listed.

    python3 tools/i18n.py pending de      # strings still needing translation
    python3 tools/i18n.py review de       # side-by-side EN | DE, for proofreading

build.py calls generate() for every language that has a table but no
hand-written content file (Russian is hand-written; German and Serbian are not).
"""

import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent.parent
CONTENT = ROOT / "content"
TABLES = CONTENT / "i18n"

# keys whose values are identifiers, paths or options — never translated
SKIP_KEYS = {
    "slug", "type", "src", "href", "tag_kind", "kind", "variant", "anchor",
    "portrait", "tone", "image", "share_image",
}
NUMERIC = re.compile(r"[\d\s.,–\-+%€≈/]*")


def key(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]


def translatable(text):
    return isinstance(text, str) and text.strip() and not NUMERIC.fullmatch(text)


def strings(node, parent=None):
    """Yield every translatable string in the content tree, in order."""
    if isinstance(node, dict):
        for k, v in node.items():
            if k in SKIP_KEYS and isinstance(v, str):
                continue
            yield from strings(v, k)
    elif isinstance(node, list):
        for v in node:
            yield from strings(v, parent)
    elif translatable(node):
        yield node


def localise_href(href, lang):
    if not href.startswith("/") or href.startswith(("//", "/static/")):
        return href
    return f"/{lang}{href}"


def transform(node, table, lang, missing, parent=None):
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            if k == "href" and isinstance(v, str):
                out[k] = localise_href(v, lang)
            elif k in SKIP_KEYS and isinstance(v, str):
                out[k] = v
            else:
                out[k] = transform(v, table, lang, missing, k)
        return out
    if isinstance(node, list):
        return [transform(v, table, lang, missing, parent) for v in node]
    if translatable(node):
        t = table.get(key(node))
        if t is None:
            missing.append(node)
            return node
        return t
    return node


def load_table(lang):
    path = TABLES / f"{lang}.json"
    if not path.exists():
        return None
    table = {}
    # tables may be split into several files: de.json, de.2.json, ...
    for part in sorted(TABLES.glob(f"{lang}*.json")):
        if re.fullmatch(rf"{lang}(\.\d+)?\.json", part.name):
            table.update(json.loads(part.read_text(encoding="utf-8")))
    return table


def generate(lang):
    """Return (content, missing strings) for a table-driven language."""
    table = load_table(lang)
    if table is None:
        return None, []
    en = json.loads((CONTENT / "en.json").read_text(encoding="utf-8"))
    missing = []
    content = transform(en, table, lang, missing)
    return content, list(dict.fromkeys(missing))


def main(argv):
    if len(argv) < 2 or argv[0] not in ("pending", "review", "keys"):
        print(__doc__)
        return 1
    cmd, lang = argv[0], argv[1]
    en = json.loads((CONTENT / "en.json").read_text(encoding="utf-8"))
    unique = list(dict.fromkeys(strings(en)))
    table = load_table(lang) or {}
    if cmd == "keys":
        for s in unique:
            print(f"{key(s)}\t{s}")
    elif cmd == "pending":
        todo = [s for s in unique if key(s) not in table]
        for s in todo:
            print(f"{key(s)}\t{s}")
        print(f"\n{len(todo)} of {len(unique)} strings untranslated", file=sys.stderr)
    elif cmd == "review":
        for s in unique:
            print(f"EN  {s}\n{lang.upper()}  {table.get(key(s), '— MISSING —')}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
