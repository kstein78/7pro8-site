# Open items

Everything the site used to say about itself while it was being built now lives
here instead. Nothing on these lines is visible to a visitor: the pages read as
finished, and this file is the list to work through.

## Audit of 13 Nov 2026 — proposed, not changed

Found while going through every page before launch. Each needs a yes or a fact
from the founders; nothing here was changed on the site. Agreed with Kosta the
same day and done: the company page says "We are looking for partners in …"
instead of "Deliveries run to …", and the photograph beside it is the Maybach
X222 interior instead of the assembly frame that is also on the production
page (`company/workshop.jpg` is no longer used by any page). Items 4–6 below
wait for Evgenii and Iliya.

- **Hero photograph — answered by Iliya, 13 Nov:** a Mercedes-Maybach S-Class
  X222, the monitors are the factory ones. Caption, alt text and file name
  (`home/hero-maybach-x222-partition.jpg`) say so.
- **Numbers — decided 13 Nov:** the headline is "450+" everywhere (the range
  page no longer says 460 in its figures; the table keeps 460 because that is
  what its rows add up to) and the history starts in 2007, the year of the
  first partition. Left as it is: the first table row, S-Class V221 Long, is
  dated 2008, while the founders' chronology dates the first partition to
  2007 — the same car (Kosta, 13 Nov), so the row now says 2007. Still unanswered: "4 premium marques"
  beside five names (Mercedes-Benz and Mercedes-Maybach counted as one?);
  20+ partition models against 14 vehicle models, eight with tooling.
- **ZiL — decided 13 Nov:** ZiL-41047 everywhere.
- **Mercedes S-Class codes — decided 13 Nov:** V everywhere (V220, V221,
  V222): only the long versions were ever built. "4 premium marques" stays.
- **Founders page split — 13 Nov:** personal and funny things live on
  `/fun/` ("Для души"), linked from the bottom of the founders page, not from
  the menu: the electric scooter (two wheels — not a trike) and the road test
  with the donkey. The taxi roof sign is off the site for now; Maybach and
  Rolls-Royce taxis with roof signs are to come instead (photographs needed).
  Lincoln Reincarnation is a joint SV-ART and CARDI project: CARDI design and
  bodywork, SV-ART interior, lighting and instrument panel. The sentence
  "the project name stayed attached to the studio" is gone (two studios).
  Unused photographs (taxi sign, marine, press, ZAZ, workshop) stay in the
  repository for now.
- **Partner presentation:** new versions will be made later (Kosta, 13 Nov);
  its "ZiL-4107" and "Novi Sad" footer are not to be patched in the PDFs.
- **70,000 € — decided 13 Nov:** not on the site (Alexey, Iliya). Removed from
  the production page and the Range Rover page.
- **Comments of Alexey and Iliya, 13 Nov evening — done:** Maybach has no
  tables in the partition (they are in the factory console), curved
  electrochromic glass instead; "plastics" -> "surface panels"; acoustic
  separation reworded by Kosta; "разъездная" reworded; "Our answer is not a
  promise…" gone; no removal times anywhere; "complements factory
  engineering", nothing about taking it off; no kit counts on the two classes;
  the timing block is "for a project in series production"; the capabilities
  page lost "A new model takes up to a year"; V-Class line 1 and line 2
  equipment lists completed; two captions; production technologies; the CAD
  figure shows the surfaces next to the mechanism.
- **Still open from the same comments:** Alexey's text for "The interior
  still looks factory" ("the interior is transformed with the best and most
  current materials … while keeping the car's overall design") does not fit
  its heading — new heading or keep? "A new model takes up to a year" is also
  said on the home page and the range page — removed there too (Kosta, 13 Nov:
  no development times on the site for now). A VLE
  visualisation (Iliya asks Evgenii) — material needed.
- **VLE timing — answered 13 Nov:** in design since 2026, physically ready in
  2027. VLE Lite: in design, most likely physically ready in 2027 as well.
  The site says so.
- **The partner presentation** carried the same two foreign photographs
  (Range Rover slide), the line 2 panels on the line 1 slide and line 1's
  previous version on the line 2 slide. Corrected in all four language PDFs
  on 13 Nov with `tools/fix_presentation.py` (slides 10, 11 and 13; the other
  twenty pages are pixel-identical, the removed photographs are no longer
  inside the files). Still in the presentation and not touched: the footer
  "Novi Sad, Serbia" on every page.
- **Files published but used on no page:** `founder/marine/01.jpg`,
  `founder/press/01.jpg`, `founder/zaz/01.jpg`, `founder/zaz/02.jpg`.

Answered by the old site itself: "V222 Long" is its own project page,
"Mercedes-Benz V222 Long ArmorTech"; the line names there are "V-class A1"
(line 2) and "V-class Busmanufacture" (line 1).

## Before launch — not the founders' to answer

- **Form backend.** `form_endpoint` in `content/site.json` is still a
  placeholder. Until it is replaced, the form opens the visitor's mail program
  with the enquiry filled in, addressed to the site email — nothing is lost, but
  a visitor without a mail program set up gets nothing. A Formspree or
  Web3Forms account takes a few minutes; paste its endpoint in and the form
  posts directly.
- **The email address.** Every page shows `7pro8design@gmail.com`. For a
  partner weighing a €25,000 order, an address at `@7pro8.com` is worth more
  than any design change. It does not wait for the site: the domain's MX
  records already point at Google; what is missing is the mailboxes and
  SPF/DKIM/DMARC. Steps in DEPLOY.md, "Mail on @7pro8.com".
- **One headline kit count.** The hero and the company page say 450+; the
  history table on the availability page adds up to 460. Both come from the
  deck. Either the hero becomes 460, or the table gets a line saying where the
  other ten went.
- **20+ partition models against 14 vehicle models.** Different counts
  (partition variants versus vehicles), but no page says so. One sentence on
  the availability page would do it, or drop one of the numbers.

## Portraits

Both are in place at the same size, 453 × 567, with the eye lines on one level and
the heads at one scale. Evgenii's original is cut a few pixels into the crown and
has no room above his head, so the top 70 px of his frame are built by
`tools/rebuild_abramov_portrait.py`: the background from the side colours of the
top rows, blurred like the rest, and the crown as the continuation of the head
outline filled with his own hair texture. If he can send the same photograph
uncropped, or any with air above the head, that step goes away.

Both are a little under the 604 px card width, which shows as slight softness on
a large retina screen and nowhere else. Photographs sent as *files* in Telegram,
not as photos, arrive at full resolution.

## Project descriptions — written from the photographs, not from the founders

These sat on the page prefixed DRAFT. The prefix is gone, so a reader now takes
them as fact: they are plausible reconstructions from the images and the dates,
and every one still needs Iliya or Evgenii to confirm or rewrite it.

- 2022 — **Electric trike with a canopy**
- 2009 — **Rolls-Royce Phantom — rear compartment** *(new, from Evgenii's deck: only the caption and the year are his)*
- 2009 — **Interiors on the water**
- 2008 — **Mercedes-Benz Viano — interior, exterior and a motorised monitor** *(new, from Evgenii's deck: two pages merged into one entry)*
- 2008 — **Taxi roof sign**
- 2008 — **ZiL-41047 — state limousine interior** (was "ZiL-4107"; Evgenii's deck says 41047, which is the real model)
- 2007 — **Mercedes-Benz S-Class W221 — the first partition**
- ≈2005 — **Mercedes-Benz Vito — VIP interior**
- 2004 — **Lamborghini Diablo VT**
- 2003 — **Chevrolet Corvette**
- ≈2003 — **Hummer H1 — VIP interior**
- 2001 — **Lincoln Reincarnation**
- ≈2000 — **Workshop, team, first volumes**
- ≈1999 — **Before the studio: a garage, racing, the press**
- 1992–2003 — **One-off cars at Cardi** *(new, Evgenii's: his caption is "Creating unique cars, 1992–2003"; which car was his and what he did on it is not known)*

## Deliberately left off the page

Neither founder is described as director, and no share split is shown. Both are
"co-founders" together and "founder" individually, which is as much as a partner
needs. The registry fields that held the directorship and the 50/50 split were
removed from `content/site.json` as well — they were not rendered anywhere, but
the repository is public.

## Facts to confirm

- **Evgenii's years — confirmed by both founders, 11 Nov 2026.** MAMI and
  CARDI 1992–1997 (CARDI is MAMI's design bureau), AZLK 1997–1998, CARDI
  1998–2005, Avtoganza 2005–2007, CARDI 2007–2009, the engineering and
  production group (formally CarFashion) 2009–2015, 7pro8 since 2015. Iliya's
  line is as he gave it.
- **Which former employers' work may be shown.** The chronology carries projects
  done inside SV-ART, A-Level, Avtoganza, Cardi Design and CarFashion. Some of
  those photographs may not be ours to publish.
- **The Hummer client.** The page no longer says the client is deliberately
  unnamed; it simply does not name them. If the name may be used, it can go in.

## Deliberately not on the site

From the bank document: turnover by year, per-unit prices, the pipeline with
named prospects, and the Russian sole-proprietorship. None of it belongs on a
public page, and it is not in the content files either.

## Chronicle

Under each title the page now says whose project it was — Iliya, Evgenii, or
both — instead of "Co-founder" on every entry. How that was decided:

- **Both:** the 2007 partition, the ZiL and the taxi sign (each is in Iliya's
  archive *and* on a page of Evgenii's deck — the same photographs), and the
  2008–2009 Viano and Phantom (Evgenii's deck, made while the two ran the group).
- **Iliya:** everything else from his archive.
- **Evgenii:** the Cardi cars, 1992–2003.

To confirm:

- **The first partition: 2007 or 2008?** Evgenii's deck dates the S600 partition
  2008; the site says 2007 in the page head, the chronicle and the "first
  partition" fact on several pages. Left at 2007 until one of them says which.
- **Mercedes-Benz Vito, ≈2005.** Both were at Avtoganza then, but the project is
  only in Iliya's archive, so it is marked as his. If Evgenii worked on it too,
  it becomes "Iliya and Evgenii".
- **2009, interiors on the water** — marked Iliya's on the same grounds.

The deck's main section (Maybach X222, Sprinter, V222 Armortech, V-class,
Range Rover, Ghost EWB, Phantom EWB) is the 7pro8 series and lives on the
model pages, not in this chronicle. Its photographs were already compared with
the site's; four were upgraded at the time.

## Photography

`/_photos/` lists every image with its resolution and a verdict. The founders'
archive photographs stay at 400–500 px because nothing better exists; they are
flagged `tight` rather than `replace` for that reason.

- **Avtoganza / Autohansa — decided 13 Nov:** "Autohansa" only in the German
  version; English and Serbian keep "Avtoganza".
