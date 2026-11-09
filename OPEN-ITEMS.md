# Open items

Everything the site used to say about itself while it was being built now lives
here instead. Nothing on these lines is visible to a visitor: the pages read as
finished, and this file is the list to work through.

## Before launch — not the founders' to answer

- **Form backend.** `form_endpoint` in `content/site.json` is still a
  placeholder. Until it is replaced, the form opens the visitor's mail program
  with the enquiry filled in, addressed to the site email — nothing is lost, but
  a visitor without a mail program set up gets nothing. A Formspree or
  Web3Forms account takes a few minutes; paste its endpoint in and the form
  posts directly.
- **The email address.** Every page shows `7pro8design@gmail.com`. For a
  partner weighing a five-figure order, an address at `@7pro8.com` is worth more
  than any design change — and it needs the domain moved off Squarespace first.
- **One headline kit count.** The hero and the company page say 450+; the
  history table on the availability page adds up to 460. Both come from the
  deck. Either the hero becomes 460, or the table gets a line saying where the
  other ten went.
- **20+ partition models against 14 vehicle models.** Different counts
  (partition variants versus vehicles), but no page says so. One sentence on
  the availability page would do it, or drop one of the numbers.

## Portraits

Both are in place at the same size, 453 × 567, with the eye lines on one level and
the heads at one scale. Evgenii's original is cut at the crown and has no room
above his head, so to bring his eyes down to Iliya's height the top 60 px of his
frame were rebuilt: out-of-focus background and the last few millimetres of hair
(`tools/` has no script for it; it was a one-off). If he can send the same
photograph uncropped, or any with air above the head, that patch goes away.

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

- **AZLK, 1997–98.** On Evgenii's card as he asked, and now on the timeline as a
  second line under Cardi. Worth confirming the job title.
- **Avtoganza, Evgenii's years.** Evgenii says the two of them worked together
  in Avtoganza's tuning department, engineering and production, and that he was
  there a little longer than Iliya — "you can ignore that". The timeline gives
  him Iliya's 2005–2007, drawn on a second line under Cardi because the page also
  says he stayed at Cardi until 2007. If Cardi actually ended when Avtoganza
  began, his Cardi bar should stop there and Avtoganza move up onto the first line.
- **The group and CarFashion are one thing** (Evgenii). Both founders' work books
  sat at CarFashion while they worked independently as their own group, so the
  timeline now calls Iliya's 2009–2015 the engineering and production group,
  "formally on the staff of CarFashion", same as Evgenii's. Evgenii's bar starts
  in 2008 and Iliya's in 2009 (his Cardi Design runs 2007–2009) — the years are
  as each of them gave them; one of the two may want to match the other.
- **SKB MAMI is Cardi** (Evgenii). Iliya's 2000–2001 now reads "Cardi (SKB MAMI)",
  which also makes it the place the two met.
- **Which former employers' work may be shown.** The chronology carries projects
  done inside SV-ART, A-Level, Avtoganza, Cardi Design and CarFashion. Some of
  those photographs may not be ours to publish.
- **The Hummer client.** The page no longer says the client is deliberately
  unnamed; it simply does not name them. If the name may be used, it can go in.

## Deliberately not on the site

From the bank document: turnover, per-unit prices, the pipeline with named
prospects and the corporate details behind them. None of it belongs on a
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

