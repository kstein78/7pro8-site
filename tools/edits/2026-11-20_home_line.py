"""20.11: Kosta — the assembly-line photo (IMG_1733, three partitions in a row)
on the home page, as a centred single-image gallery right after the
"engineering company, not a tuning shop" block. Caption: process only.
Usage: python3 -I tools/edits/2026-11-20_home_line.py ru        (RU now)
       python3 -I tools/edits/2026-11-20_home_line.py en de sr  (after Kosta's OK)
"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import i18n

CAP = ("Серийная сборка: перегородки идут на участке одна за другой",
       "Series assembly: partitions move through the shop one after another",
       "Serienmontage: Trennwände durchlaufen die Werkstatt eine nach der anderen",
       "Serijska montaža: pregrade prolaze kroz radionicu jedna za drugom")
SPLIT_TITLE = {"ru": "Инженерная компания, а не тюнинг-ателье",
               "en": "An engineering company, not a tuning shop"}
IDX = {"ru": 0, "en": 1}

def edit(lang):
    p = ROOT / "content" / f"{lang}.json"
    raw = p.read_text(encoding="utf-8"); d = json.loads(raw)
    assert json.dumps(d, ensure_ascii=False, indent=2) + "\n" == raw
    blocks = d["pages"][0]["blocks"]
    hits = [n for n, b in enumerate(blocks) if b.get("type") == "split" and b.get("title") == SPLIT_TITLE[lang]]
    assert len(hits) == 1, hits
    n = hits[0]
    assert "assembly-line" not in json.dumps(blocks[n + 1])
    c = CAP[IDX[lang]]
    blocks.insert(n + 1, {"type": "gallery", "align": "center",
                          "items": [{"src": "manufacturing/assembly-line.jpg", "alt": c, "caption": c}]})
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("edited", lang)

def tables(lang):
    p = ROOT / "content" / "i18n" / f"{lang}.7.json"
    raw = p.read_text(encoding="utf-8"); d = json.loads(raw)
    assert json.dumps(d, ensure_ascii=False, indent=2) + "\n" == raw
    d[i18n.key(CAP[1])] = CAP[{"de": 2, "sr": 3}[lang]]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("tables", lang)

for a in sys.argv[1:]:
    edit(a) if a in IDX else tables(a)
