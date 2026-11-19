"""19.11: workshop photos (Kosta). 5 shots: 3 into the manufacturing gallery,
2 as a new gallery on the partners page after the responsibilities block.
Captions describe the process only, never the location.
Usage: python3 -I tools/edits/2026-11-19_shop_photos.py ru        (RU now)
       python3 -I tools/edits/2026-11-19_shop_photos.py en de sr  (after Kosta's OK)
"""
import json, sys, glob
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import i18n

T = {  # key: (ru, en, de, sr)
 "frame":  ("Силовой каркас перегородки с механизмами подъёма стёкол",
            "Partition structural frame with the glass lift mechanisms",
            "Tragrahmen einer Trennwand mit Scheibenhubmechanismen",
            "Noseći ram pregrade sa mehanizmima podizanja stakla"),
 "mould":  ("Формование композитной детали в оснастке",
            "Moulding a composite part in the production mould",
            "Laminieren eines Verbundbauteils in der Produktionsform",
            "Oblikovanje kompozitnog dela u proizvodnom kalupu"),
 "print":  ("3D-печать детали", "3D printing a part", "3D-Druck eines Bauteils", "3D štampa dela"),
 "title":  ("Предварительная сборка и проверка", "Pre-assembly and inspection",
            "Vormontage und Prüfung", "Predmontaža i provera"),
 "team":   ("Предварительная сборка комплектов", "Kits in pre-assembly",
            "Bausätze in der Vormontage", "Kompleti u predmontaži"),
 "kits":   ("У каждого комплекта — свой номер и карта сборки",
            "Every kit carries its own number and build sheet",
            "Jeder Bausatz hat seine eigene Nummer und Montagekarte",
            "Svaki komplet ima svoj broj i montažnu kartu"),
}
IDX = {"ru": 0, "en": 1}

def item(src, k, i):
    return {"src": src, "alt": T[k][i], "caption": T[k][i]}

def edit(lang):
    i = IDX[lang]
    p = ROOT / "content" / f"{lang}.json"
    raw = p.read_text(encoding="utf-8"); d = json.loads(raw)
    assert json.dumps(d, ensure_ascii=False, indent=2) + "\n" == raw
    # manufacturing gallery: unique by its first image
    gals = [b for pg in d["pages"] for b in pg.get("blocks", [])
            if b.get("type") == "gallery" and any(x["src"] == "manufacturing/frame-sprinter.jpg" for x in b["items"])]
    assert len(gals) == 1, len(gals)
    g = gals[0]
    assert not any(x["src"] == "manufacturing/partition-frame.jpg" for x in g["items"])
    g["items"] += [item("manufacturing/partition-frame.jpg", "frame", i),
                   item("manufacturing/composite-moulding.jpg", "mould", i),
                   item("manufacturing/3d-printing.jpg", "print", i)]
    # partners page: the twocol block is unique site-wide
    hits = [(pg, n) for pg in d["pages"] for n, b in enumerate(pg.get("blocks", [])) if b.get("type") == "twocol"]
    assert len(hits) == 1, len(hits)
    pg, n = hits[0]
    assert pg["blocks"][n + 1].get("type") != "gallery"
    pg["blocks"].insert(n + 1, {"type": "gallery", "cols": 2, "title": T["title"][i], "items": [
        item("manufacturing/assembly-team.jpg", "team", i),
        item("manufacturing/kits-in-work.jpg", "kits", i)]})
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("edited", lang)

def tables(lang):
    col = {"de": 2, "sr": 3}[lang]
    p = ROOT / "content" / "i18n" / f"{lang}.7.json"
    raw = p.read_text(encoding="utf-8"); d = json.loads(raw)
    assert json.dumps(d, ensure_ascii=False, indent=2) + "\n" == raw
    for k, v in T.items():
        d[i18n.key(v[1])] = v[col]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("tables", lang)

for a in sys.argv[1:]:
    edit(a) if a in IDX else tables(a)
