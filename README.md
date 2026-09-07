# 7pro8.com

Static site for 7pro8 DOO Novi Sad. Every page is generated from JSON content
files, so adding a language means translating one file rather than rewriting
HTML, and correcting a figure means editing one line rather than hunting through
markup.

No database, no CMS, no build toolchain beyond Python and Jinja2. The output is
plain HTML that any web server can serve.

---

## Quick start

```bash
pip install -r requirements.txt
python build.py --serve     # builds into dist/ and serves it on :8000
```

Build only:

```bash
python build.py
python tools/check_links.py   # verifies every internal link and asset resolves
```

---

## Layout

```
content/
  site.json        identity, contacts, languages, form endpoint  (shared)
  en.json          English content — all 19 pages
  ru.json          Russian content — all 19 pages
templates/
  base.html        head, header, language switcher, footer
  page.html        renders a page's list of content blocks
  404.html
  blocks/          one template per block type (hero, grid, table, form, ...)
static/
  css/site.css
  js/site.js       mobile nav, glass toggle, form submit — all optional
  img/             photography goes here (see IMAGES.md)
tools/
  check_links.py
deploy/
  Caddyfile        recommended server config
  nginx.conf       alternative
dist/              generated — not committed
```

## How a page is built

A page is a list of blocks. Each block has a `type` that maps to a template in
`templates/blocks/`. To change a page, reorder or edit its blocks; to add a new
kind of section, add one small template and use it.

Available block types: `hero`, `pagehead`, `prose`, `grid`, `split`, `process`,
`metrics`, `table`, `twocol`, `projects`, `lineup`, `gallery`, `spec`, `note`,
`cta`, `form`.

Most blocks accept `"tone": "paper"` or `"tone": "dark"` to change the band
background.

## Adding a language

1. Copy `content/en.json` to `content/<code>.json`.
2. Translate the values. Leave every `slug` and `type` exactly as it is —
   URLs stay identical across languages so the language switcher works.
3. Update the `href` values inside the file to point at the language prefix
   (Russian links start with `/ru/`; English, as the default language, has no
   prefix).
4. Make sure the language is listed in `content/site.json`.

The build skips any language whose file does not exist yet, and the switcher
greys out that language instead of linking to a 404. German and Serbian are
listed and greyed out — the source text for both already exists in
`7pro8_Praesentation_DE.pdf` and `7pro8_Prezentacija_SR.pdf`.

## Images

All photography lives in `static/img/`. Any slot without a file gets a labelled
placeholder at build time and is listed in `dist/_missing-images.txt`, so the
layout can be reviewed before the photos exist. See **IMAGES.md** for the full
list of slots and what belongs in each.

---

## Data you have to supply before going live

These are marked `TODO` in `content/site.json` and appear in the footer of every
page and in the structured data:

| Field | Why it matters |
|---|---|
| `email` | Currently a Gmail address on the live site. A `@7pro8.com` address is worth more than any design change on a €25,000 sale. |
| `phone` | There is no telephone number anywhere on the current site. |
| `address.street`, `address.postcode` | Required for the Organization schema and for basic credibility. |
| `registration_no`, `vat_no` | Serbian company registration (matični broj) and PIB. |
| `form_endpoint` | A form backend. Formspree or Web3Forms both work with a static site; free tiers are enough for this volume. Without it the form falls back to the mailto link underneath. |

---

## Data audit — every figure published on the site

All figures come from the 2026 partner presentation. Nothing was estimated,
rounded or invented during the build.

| Figure | Where it appears | Source |
|---|---|---|
| Founded 2007 | Hero, company, footer copyright | Deck cover, "2007 — founded" |
| 450+ kits delivered | Hero, company | Deck cover and company slide |
| 20+ partition models | Hero | Deck cover |
| 4 premium marques | Hero | Deck cover |
| 19 years in the segment | Company | Deck company slide |
| 30–40 complex partitions a year | Home, company, availability | Deck company slide and history slide |
| 3–4 simple partitions a year | Home, availability | Deck history slide |
| 4 months / 1 day / 1–3 days | Home, partners, project pages | Deck cooperation slide |
| €70,000 tooling investment | Manufacturing, Range Rover page | Deck production slide; Range Rover slide |
| 14 models / 8 series-tooled / 460 kits | Availability | Deck history slide |
| Every row of the project history table | Availability | Deck history slide, verbatim |
| Per-project volumes and years | Project pages | Deck portfolio slides |
| VLE unveiled 10 March 2026, series production at Vitoria since June 2026 | Home, VLE, availability | Deck product range slide |

### Three inconsistencies in the source material — please resolve

These exist in the presentation itself. The site currently follows the deck's
own front-page claims, but a careful reader will notice all three.

1. **2005 vs 2007.** The live site footer reads `© 2005-2026`; the deck says the
   company was founded in 2007 and produced its first partition that year. The
   new site uses 2007 everywhere. If 2005 is the correct incorporation date and
   2007 the first partition, the copy should say both explicitly.

2. **450+ vs 460 kits.** The deck cover says "over 450 kits delivered since
   2007"; the history table totals 460 kits since 2008. The site uses 450+ in
   the hero and 460 in the history table, which is defensible but looks careless
   side by side. Pick one headline number.

3. **20+ partition models vs 14 vehicle models.** The cover claims more than 20
   partition models; the history table lists 14 vehicles and 8 projects taken to
   series tooling. These count different things — partition variants versus
   vehicle models — but nothing on the page explains that. Either add the
   explanation or use one number.

### Deliberately not published

The indicative price table from the deck (V-Class €25,000–28,000, Rolls-Royce
Phantom €60,000–70,000, new project from €70,000, Escalade completion cost
€80,000–90,000) is **not** on the site, by design:

- it is the negotiating position, and publishing it removes the room to move;
- it points KLASSEN and every other competitor straight at the price shelf;
- the figures are for a partition *without* trimming and installation, so an end
  client reading them as retail prices would break the partner's own economics.

Instead every page routes to the enquiry form, which asks for model, market and
volume — the three things needed to quote properly. If you want a public price
anchor later, the right form is a "from €X" figure on the availability page, not
the table.

---

## Deployment

### One-time setup on the Hetzner server

```bash
# as root
apt update && apt install -y caddy rsync
mkdir -p /srv/7pro8/releases
adduser --disabled-password --gecos "" deploy
mkdir -p /home/deploy/.ssh
# paste the deploy key's public half into /home/deploy/.ssh/authorized_keys
chown -R deploy:deploy /srv/7pro8 /home/deploy/.ssh
chmod 700 /home/deploy/.ssh && chmod 600 /home/deploy/.ssh/authorized_keys

cp deploy/Caddyfile /etc/caddy/Caddyfile
systemctl reload caddy
```

Point the DNS A and AAAA records for `7pro8.com` and `www.7pro8.com` at the
server. Caddy issues the certificate on the first request.

### One-time setup on GitHub

Create the repository, push, then add four repository secrets under
Settings → Secrets and variables → Actions:

| Secret | Value |
|---|---|
| `SSH_PRIVATE_KEY` | private half of a deploy-only ed25519 key |
| `SSH_HOST` | server hostname or IP |
| `SSH_USER` | `deploy` |
| `SSH_KNOWN_HOSTS` | output of `ssh-keyscan -H <host>` |

After that every push to `main` builds the site, checks the links, and rsyncs it
to a timestamped release directory. The `current` symlink is switched
atomically, so a half-uploaded build is never served, and the last five releases
are kept for instant rollback:

```bash
ln -sfn /srv/7pro8/releases/<previous> /srv/7pro8/current.tmp
mv -Tf /srv/7pro8/current.tmp /srv/7pro8/current
```

### Migrating away from Squarespace

Keep the Squarespace subscription running until the new site is live and the DNS
has propagated. Before cancelling, download the images — the current site's
photography lives on the Squarespace CDN and disappears with the subscription.
IMAGES.md lists which page each one is on.

Old Squarespace URLs worth redirecting, since they may be linked from elsewhere:

| Old | New |
|---|---|
| `/main/maybach-x222-a1` | `/portfolio/mercedes-maybach-s-class-x222/` |
| `/main/mercedes-benz-sprinter` | `/portfolio/mercedes-benz-sprinter/` |
| `/main/mercedes-benz-v-class-a1` | `/portfolio/mercedes-benz-v-class-line-1/` |
| `/main/mercedesbenz-vclass-busmanufacture` | `/portfolio/mercedes-benz-v-class-line-2/` |
| `/main/mercedes-benz-v222-long-armortech` | `/portfolio/mercedes-benz-s-class-v222/` |
| `/main/range-rover-long-a1` | `/portfolio/range-rover-lwb/` |
| `/main/rolls-royce-ghost-ewb` | `/portfolio/rolls-royce-ghost-ewb/` |
| `/main/rolls-royce-phantom-ewb` | `/portfolio/rolls-royce-phantom-ewb/` |
| `/contact` | `/contact/` |

Add them to the Caddyfile as `redir` lines once the mapping is confirmed.

---

## Design notes

The palette is taken from the product rather than from a stock luxury template:
the grey of a composite panel before trimming as the page ground, the graphite of
a finished interior for dark bands, and the blue-grey of electrochromic glass in
its opaque state as the only accent.

The one interactive element on the site is the switch in the hero, which makes
the glass opaque. It demonstrates the product instead of describing it. Nothing
else animates on load or on scroll.

Typography is Archivo for headings and figures — tabular numerals throughout, so
tables and specification lists align — and Newsreader for body text. Both load
from Google Fonts; self-hosting them is a worthwhile change before launch, since
it removes a third-party request and the associated cookie-consent question in
the EU.
