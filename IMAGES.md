# Photography

**Every image on the site is © 7pro8.com** (`site.json` → `photo_credit`). The
credit is printed in the footer of every page and on the inventory page.

## The inventory page

`/_photos/` — built on every run, linked from nowhere, `noindex`, and excluded
in `robots.txt`. It lists every photograph the site uses with:

* the size it is stored at,
* the width of the slot it is painted into at the widest desktop layout,
* the ratio between the two, which is what decides sharp or soft,
* a verdict — **missing / replace / tight / ok / good** — and why,
* where it is used, and where it came from.

The same check runs on the command line:

```bash
python3 tools/photo_audit.py          # table
python3 tools/photo_audit.py --json   # machine-readable
```

`replace` means the file is below three quarters of its slot width and is
visibly soft — that one needs a new original. `good` means it also covers a 2×
display.

## Where the deck images come from

`tools/extract_deck_images.py` takes photography from the 2026 partner deck —
**not** from page renders, but from the originals embedded in the PDF:

```bash
python3 tools/extract_deck_images.py path/to/7pro8_Presentation_EN.pdf
```

The crop boxes in that file are still expressed in the coordinates of the
1456 px-wide page renders the design was composed against, because that is the
readable way to describe a crop. The script maps them onto the originals:
pdfplumber reports where each embedded image sits on its page in points, the
render is a uniform scale of the page, so a render box becomes a fraction of
the placed image's rectangle and then a rectangle on its native pixel grid.

Two consequences worth knowing:

* **Nothing is upscaled.** Output sizes are whatever the originals hold —
  typically 830 to 1500 px wide, against the 350–720 px the renders gave.
* **A crop that is a narrow strip is grown, not cut.** Forcing a 5:1 strip to
  4:3 by centre-cropping throws away most of its width; the script widens the
  short side inside the original instead, and only cuts when the original has
  no room left.

Where an image is still flagged after that, the deck's own original is the
limit and the replacement has to come from the photography itself.

`portfolio/escalade/02.jpg` and the two founder portraits
(`founders/abramov.jpg`, `founders/bolshakov.jpg`) have no file at all: the
Escalade slide carries a single photograph, and no portraits were supplied.

Any slot without a file renders a labelled placeholder, so nothing breaks while
the set is incomplete. Run `python build.py` and check
`dist/_missing-images.txt` for what is outstanding.

## Format

- **JPEG**, sRGB, quality 80–85.
- **Long edge 2000 px** for full-width and hero images, 1400 px for gallery
  items. Everything is displayed at 3:2, so crop to 3:2 before export — the
  browser will centre-crop otherwise and may cut the subject.
- Keep files under 400 KB. `cwebp` or `squoosh` will halve them again if needed.
- `share/7pro8-share.jpg` must be **1200 × 630** — that is the aspect ratio
  LinkedIn, WhatsApp and Telegram use for link previews. The current site has no
  share description at all, so this one file changes how every link to 7pro8
  looks when it is pasted anywhere.

## Sources

Two places to pull from:

- **The 2026 partner presentation** — the curated set, already selected and
  captioned. This is the better source for most slots.
- **The current Squarespace site** — the originals are on the Squarespace CDN.
  Download them before the subscription is cancelled; they are lost afterwards.

## Slots

### Home

| Path | What it should show | Suggested source |
|---|---|---|
| `home/hero-v-class-partition.jpg` | The strongest single photograph you own: a finished V-Class rear zone with the partition, monitor and ambient lighting. This is the first thing anyone sees. | Deck, V-Class line 1 slide, "after" image |
| `home/tooling-mould.jpg` | The production mould for a surface panel — the object that makes the argument about repeatability. | Deck, capabilities slide |
| `home/vle-development.jpg` | CAD model or development render. | Deck, product range slide |
| `share/7pro8-share.jpg` | 1200 × 630 crop of the hero image. | derived |

### Product

| Path | What it should show | Suggested source |
|---|---|---|
| `product/maybach-x222-interior.jpg` | Maybach rear zone with the partition integrated into the factory interior. | Deck, X222 slide |

### Engineering and manufacturing

| Path | What it should show | Suggested source |
|---|---|---|
| `capabilities/cad-model.jpg` | CAD model of a partition with the glass mechanism. | Deck, capabilities slide |
| `manufacturing/mould-panel-forming.jpg` | Forming a surface panel from the mould. | Deck, production slide |
| `manufacturing/frame-sprinter.jpg` | Sprinter structural frame. | Deck, production slide |
| `manufacturing/glass-mechanism.jpg` | Glass lift mechanism, metal work. | Deck, production slide |
| `manufacturing/v-class-assembly.jpg` | V-Class partitions on the assembly line. | Deck, production slide |

### Projects

Each project needs a `cover.jpg` for the grid plus its numbered gallery images.
The cover should be the single clearest "after" shot — the grid is what most
visitors will judge the company on.

| Path | Deck slide | Current site page |
|---|---|---|
| `portfolio/v-class-line-1/cover.jpg`, `01`–`03` | V-Class line 1 | `/main/mercedes-benz-v-class-a1` |
| `portfolio/v-class-line-2/cover.jpg`, `01`–`04` | V-Class line 2 | `/main/mercedesbenz-vclass-busmanufacture` |
| `portfolio/sprinter/cover.jpg`, `01`–`03` | Sprinter | `/main/mercedes-benz-sprinter` |
| `portfolio/maybach-x222/cover.jpg`, `01`–`03` | Maybach X222 | `/main/maybach-x222-a1` |
| `portfolio/range-rover/cover.jpg`, `01`–`04` | Range Rover LWB | `/main/range-rover-long-a1` |
| `portfolio/rr-phantom/cover.jpg`, `01`–`03` | Rolls-Royce Phantom EWB | `/main/rolls-royce-phantom-ewb` |
| `portfolio/rr-ghost/cover.jpg`, `01`–`04` | Rolls-Royce Ghost EWB | `/main/rolls-royce-ghost-ewb` |
| `portfolio/s-class-v222/cover.jpg`, `01`–`04` | S-Class V222 armoured | `/main/mercedes-benz-v222-long-armortech` |
| `portfolio/escalade/cover.jpg`, `01`–`02` | Cadillac Escalade ESV | — |

### Company

| Path | What it should show |
|---|---|
| `company/workshop.jpg` | The shop floor in Novi Sad, with work visibly in progress. |
| `company/novi-sad.jpg` | The building or the city — used on the contact page. |

## The logo

`static/img/logo-7pro8.svg` is the isometric 7pro8 mark, redrawn as vector from
the largest version in the decks (the TopCar cover slide). It is three flat
polygon paths, one per face, at 619 bytes — so it stays sharp at any size and the
favicon is generated from the same paths.

It was traced, not copied, which means the geometry is accurate to within a pixel
of the source render but is not the original artwork. **If the original vector
file exists — .ai, .eps, .svg or .pdf from whoever drew it — replace this file
with it.** The build will pick it up with no other change, as long as it keeps a
`viewBox` and transparent background.

## Two things to check before publishing

1. **Rights to the vehicles.** Several projects were carried out for official
   dealers and distributors. Confirm you are free to publish photographs of
   those specific cars, and that no customer plate, VIN or interior monogram is
   legible.
2. **The armoured V222.** Armoured vehicles for diplomatic and security clients
   are the most likely of the nine projects to carry a confidentiality
   obligation. Confirm before that page goes live, or publish it with detail
   shots only.
