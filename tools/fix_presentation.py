"""Corrections to the partner presentation (Iliya, 11 Nov 2026), applied to
the finished PDFs because their HTML source is not at hand.

  slide 10  line 1: "panels before trimming" is line 2's and not for showing
            -> replaced by line 1's previous version (the "light trim" card
               that sat on the line 2 slide)
  slide 11  line 2: that card removed; "rear zone" photo takes the whole row
  slide 13  Range Rover: two interiors that are not 7pro8 work removed;
            the car photograph is shown whole
"""
import io, sys, warnings
warnings.simplefilter("ignore")
import pymupdf
from PIL import Image

BG = (0.039216, 0.039216, 0.043137)
BORDER = (0.12549, 0.12549, 0.133333)
GOLD = (0.776471, 0.65098, 0.392157)
R = pymupdf.Rect


def gradient_png(w=8, h=100):
    im = Image.new("RGBA", (w, h))
    px = im.load()
    for y in range(h):
        t = y / (h - 1)
        a = int(255 * 0.82 * (t ** 1.3))
        for x in range(w):
            px[x, y] = (8, 8, 9, a)
    b = io.BytesIO(); im.save(b, "PNG"); return b.getvalue()


def one_page(doc, pno, keep=()):
    """A document holding only this page, and of its pictures only those whose
    pixel size is in `keep` — whatever is pasted from it must not carry the
    removed photographs along, hidden."""
    d = pymupdf.open(); d.insert_pdf(doc, from_page=pno, to_page=pno)
    p = d[0]
    for im in p.get_images(full=True):
        if (im[2], im[3]) not in keep:
            p.delete_image(im[0])
    return pymupdf.open("pdf", d.tobytes(garbage=4, deflate=True))


def text_only(doc, pno, rect):
    d = one_page(doc, pno); p = d[0]
    p.add_redact_annot(rect, fill=False)
    p.apply_redactions(images=1, graphics=2, text=1)   # drop pictures and line art, keep text
    return d


def tag_rect(page, x0, y0):
    for g in page.get_drawings():
        r = g["rect"]
        if g.get("fill") and abs(g["fill"][0] - GOLD[0]) < .01 and abs(r.x0 - x0) < 1 and abs(r.y0 - y0) < 1 and r.height < 20:
            return R(r)
    raise SystemExit(f"no tag at {x0},{y0}")


def caption_span(page, strip):
    hits = [R(s["bbox"]) for b in page.get_text("dict")["blocks"] for l in b.get("lines", [])
            for s in l["spans"] if R(s["bbox"]).intersects(strip) and strip.contains(pymupdf.Point(s["bbox"][0], (s["bbox"][1]+s["bbox"][3])/2))]
    if not hits: raise SystemExit(f"no caption in {strip}")
    r = hits[0]
    for h in hits[1:]: r |= h
    return r + (-1, -1.5, 1, 1.5)


def cover(page, rect):
    page.add_redact_annot(rect, fill=BG)
    page.apply_redactions(images=0, graphics=0, text=0)   # text under it is really removed
    page.draw_rect(rect, color=None, fill=BG, width=0)


def card(page, outer, *, xref=None, stream=None):
    inner = outer + (0.7, 0.7, -0.7, -0.7)
    page.draw_rect(outer, color=None, fill=BORDER, width=0)
    if xref: page.insert_image(inner, xref=xref, keep_proportion=False)
    else:    page.insert_image(inner, stream=stream, keep_proportion=False)
    page.insert_image(R(inner.x0, inner.y1 - 25, inner.x1, inner.y1), stream=gradient_png(), keep_proportion=False)
    return inner


def fix(src, dst):
    orig = pymupdf.open(src); doc = pymupdf.open(src)
    assert doc.page_count == 23

    # ---- slide 13: Range Rover
    pno = 12; page = doc[pno]; o = orig[pno]
    old_card = R(490.4, 118.2, 907.1, 305.1)
    tag = tag_rect(o, 491.1, 118.9)
    cap = caption_span(o, R(491, 280, 907, 305.1))
    txt = text_only(orig, pno, old_card + (-1, -1, 1, 1))
    tags = one_page(orig, pno)
    cover(page, R(489.9, 117.7, 907.6, 466.6))
    for x in (207, 210): page.delete_image(x)
    w = old_card.width - 1.4; h = w * 933 / 1400
    new_card = R(old_card.x0, old_card.y0, old_card.x1, old_card.y0 + h + 1.4)
    card(page, new_card, xref=204)
    page.show_pdf_page(tag, tags, 0, clip=tag)
    dy = new_card.y1 - old_card.y1
    page.show_pdf_page(cap + (0, dy, 0, dy), txt, 0, clip=cap)

    # ---- slide 11: V-Class line 2
    pno = 10; page = doc[pno]; o = orig[pno]
    left = R(432.9, 296.4, 662.9, 504.9); wide = R(432.9, 296.4, 907.1, 504.9)
    tag = tag_rect(o, 433.6, 297.1)
    cap = caption_span(o, R(433, 480, 663, 504.9))
    txt = text_only(orig, pno, left + (-1, -1, 1, 1))
    tags = one_page(orig, pno)
    light_card = one_page(orig, pno, keep={(1050, 522)})   # for slide 10: line 1, previous version
    im = Image.open(io.BytesIO(orig.extract_image(186)["image"])).convert("RGB")
    ratio = (wide.width - 1.4) / (wide.height - 1.4)
    ch = round(im.width / ratio); top = round(im.height * 0.12)
    b = io.BytesIO(); im.crop((0, top, im.width, top + ch)).save(b, "JPEG", quality=92)
    cover(page, wide + (-0.5, -0.5, 0.5, 0.5))
    card(page, wide, stream=b.getvalue())
    page.show_pdf_page(tag, tags, 0, clip=tag)
    page.show_pdf_page(cap, txt, 0, clip=cap)

    # ---- slide 10: V-Class line 1
    pno = 9; page = doc[pno]
    slot = R(295.2, 73.7, 525.2, 282.2)
    cover(page, slot + (-0.5, -0.5, 0.5, 0.5))
    page.delete_image(176)
    page.show_pdf_page(slot, light_card, 0, clip=R(677.1, 296.4, 907.1, 504.9))

    doc.save(dst, garbage=4, deflate=True)
    return dst


if __name__ == "__main__":
    fix(sys.argv[1], sys.argv[2])
