# Deployment

Two targets, in the order they are needed:

1. **GitHub Pages** — the temporary address, for showing the site to the
   founders before the domain is arranged. Rebuilds on every push.
2. **Hetzner + 7pro8.com** — production. Manual, and only once the server and
   the domain are ready.

---

## 1. Push the repository to GitHub

The archive already contains a git repository with its full history, so nothing
needs initialising — only a remote and a push.

### Windows (PowerShell)

PowerShell has no `unzip`, `head` or `grep`; these are the equivalents.

```powershell
cd C:\Users\kstei\Desktop\7pro8\Site\Git

# unpack (skip if the folder is already there)
Expand-Archive -Path .\7pro8-site.zip -DestinationPath . -Force
cd .\7pro8-site

# the repository must already have commits and no remote
git --no-pager log --oneline -3
git remote -v
```

If `git --no-pager log` prints nothing or complains that this is not a
repository, you are in the wrong folder or the archive was unpacked one level
too deep: look for the folder that contains `build.py` and `.git`.

```powershell
# the repository on GitHub may already exist — creating it again fails with
# "Name already exists on this account", which is harmless. Just point at it:
git remote add origin https://github.com/kstein78/7pro8-site.git
git branch -M main
git push -u origin main
```

If `git remote add` says the remote already exists, replace it instead:

```powershell
git remote set-url origin https://github.com/kstein78/7pro8-site.git
```

If the push asks for a password, let the GitHub CLI handle the credentials:

```powershell
gh auth setup-git
git push -u origin main
```

`gh repo create ... --source=. --push` only works from a folder that already
has commits. Run from an empty folder it creates the repository on GitHub and
then stops, which is the state to recover from above.

### macOS / Linux

```bash
unzip 7pro8-site.zip && cd 7pro8-site
git --no-pager log --oneline -3

git remote add origin https://github.com/kstein78/7pro8-site.git
git branch -M main
git push -u origin main
```

**Private or public?** A private repository is the right default here: the site
is a draft and carries the founders' biographies and archive photographs.
GitHub Pages works from a private repository on all current paid plans; on a
free account, Pages for a private repository is not available — in that case
either make the repository public (the source is not secret, but see the
warning about the preview URL below) or use one of the alternatives in §3.

## 2. Turn on the preview

In the repository: **Settings → Pages → Build and deployment → Source:
GitHub Actions**. That is the only setting to change; the workflow is already
in the repository at `.github/workflows/pages.yml`.

Then go to **Actions → Preview on GitHub Pages → Run workflow** (or just push a
commit). The build takes about a minute, and the address appears in the
workflow summary:

```
https://kstein78.github.io/7pro8-site/
```

Every later `git push` to `main` republishes it automatically.

The preview build differs from production in exactly two ways, both deliberate:

- **It is not indexable.** Every page carries `noindex, nofollow` and
  `robots.txt` disallows everything, so the draft cannot appear in Google before
  the real site does, and cannot compete with it afterwards.
- **Links are relative.** GitHub Pages serves a project site from a sub-path
  (`/7pro8-site/`), where root-absolute links would break. `tools/make_relative.py`
  handles this; production keeps the root-absolute form.

A small `preview` marker sits in the bottom-left corner of every page, so nobody
mistakes the draft for the live site. Both differences disappear in the
production build.

### What the founders will see

The URL is **public to anyone who has it** — the noindex tag keeps search
engines away, but it is not a password. For a draft with biographies and
archive photographs that is usually acceptable for a few days of review;
if it is not, use §3.

## 3. If the preview must not be public

| Option | What it gives | Cost |
|---|---|---|
| The claude.ai artifact link already published | Private: only people you share it with can open it | — |
| Cloudflare Pages + Cloudflare Access | Same automatic deployment from the repository, plus a login wall (email one-time codes) in front of the site | Free for up to 50 users |
| Netlify + password protection | Simple site-wide password | Paid feature |

For Cloudflare Pages: connect the repository, set the build command to
`pip install -r requirements.txt && SITE_PREVIEW=1 python build.py && python tools/make_relative.py`,
the output directory to `dist-relative`, then add an Access policy over the
`*.pages.dev` hostname.

## 4. Production: Hetzner + 7pro8.com

Decided on 13 Nov 2026. Squarespace cannot serve a generated static site — it
stays only as the registrar and the DNS panel of the domain. The Hetzner path
is already in the repository and was tested locally (`deploy/Caddyfile` served
the built site: pages 200, `/contact` → `/contact/`, old Squarespace addresses
301 to their new pages, unknown address → the 404 page, apex → www).

What the DNS of 7pro8.com holds today (looked up on 13 Nov 2026):

| Record | Value | Meaning |
|---|---|---|
| NS | `ns01–04.squarespacedns.com`, `dns1–4.p01.nsone.net` | records are edited in the Squarespace domain panel |
| A `@` | four Squarespace addresses (198.49.23.144/145, 198.185.159.144/145) | the old site |
| CNAME `www` | `ext-sq.squarespace.com` | the old site |
| MX | Google (`aspmx.l.google.com` + alt1–4) | mail is already pointed at Google |
| TXT `@` | `google-site-verification=…` | the domain was verified with Google once |
| SPF, DKIM, DMARC | none | mail from @7pro8.com would not be trusted |

### The order of work

1. **Server.** The smallest Hetzner Cloud server with Ubuntu is enough for a
   static site. Run the block from README.md, "One-time setup on the Hetzner
   server" (Caddy, the `deploy` user, `/srv/7pro8`, `deploy/Caddyfile`).
2. **Repository secrets** (Settings → Secrets and variables → Actions):
   `SSH_PRIVATE_KEY`, `SSH_HOST`, `SSH_USER`, `SSH_KNOWN_HOSTS`.
3. **First deploy, before touching DNS.** Actions → Deploy to Hetzner
   (production) → Run workflow. Check the result on the server itself, with the
   domain pinned to the new address:
   `curl -I --resolve www.7pro8.com:80:<server IP> http://www.7pro8.com/`
4. **Switch the domain** in the Squarespace DNS panel — only these two, the
   mail records stay as they are:
   - A `@` → the server's IPv4 (remove the four Squarespace addresses);
     AAAA `@` → its IPv6, if the server has one
   - `www`: remove the CNAME, add A (and AAAA) → the same server
   Caddy obtains the certificate on the first request after the records resolve.
5. **Check:** `https://www.7pro8.com/robots.txt` reads `Allow: /`;
   `https://7pro8.com/` lands on `https://www.7pro8.com/`;
   `https://www.7pro8.com/main/range-rover-long-a1` lands on the Range Rover
   page. The old addresses need no manual step any more: the Caddyfile imports
   the list from the release.
6. **Search.** Add the property in Google Search Console (the domain is
   verifiable by the same kind of TXT record), submit
   `https://www.7pro8.com/sitemap.xml`. Then switch the GitHub Pages preview
   off, or leave it — it is `noindex` and cannot compete.
7. **Afterwards:** add the `push:` trigger back to
   `.github/workflows/deploy-hetzner.yml` so every push to `main` publishes.

Keep the Squarespace *domain* registration; the Squarespace *site* subscription
can end once the photographs are downloaded from its CDN (see IMAGES.md) and
the new site has been live for a few days.

### Mail on @7pro8.com

Independent of the site: the MX records do not change in step 4.

1. Find out whether a Google Workspace account for 7pro8.com already exists
   (the MX and the verification record date from 2023). If it does, add the
   users there; if not, sign up for Workspace with this domain.
2. Mailboxes for Kosta, Iliya and Evgenii; `info@` as an alias (aliases are
   free) — that is the address the site should show.
3. DNS, in the Squarespace panel:
   - TXT `@` → `v=spf1 include:_spf.google.com ~all`
   - TXT `google._domainkey` → the DKIM key generated in the Google Admin
     console (Apps → Google Workspace → Gmail → Authenticate email)
   - TXT `_dmarc` → `v=DMARC1; p=none; rua=mailto:dmarc@7pro8.com`; after two
     to four weeks of clean reports, `p=quarantine`
4. In the repository: `email` in `content/site.json`, and the form endpoint
   (OPEN-ITEMS.md).

## Local checks before pushing

```bash
pip install -r requirements.txt
python build.py                # production build into dist/
python tools/check_links.py    # every internal link and asset
python tools/check_workflows.py  # the GitHub Actions files parse
python build.py --serve        # look at it on http://localhost:8000
```

On Windows the same commands work in PowerShell with `python` (not `python3`).

To see exactly what the preview will look like, including the sub-path:

```bash
SITE_PREVIEW=1 python build.py && python tools/make_relative.py
mkdir -p /tmp/pages && cp -r dist-relative /tmp/pages/7pro8-site
cd /tmp/pages && python3 -m http.server 8080
# then open http://localhost:8080/7pro8-site/
```

PowerShell (the environment variable is set differently):

```powershell
$env:SITE_PREVIEW = "1"; python build.py; python tools\make_relative.py
$env:SITE_PREVIEW = ""          # clear it, or later builds stay noindex
New-Item -ItemType Directory -Force $env:TEMP\pages | Out-Null
Copy-Item -Recurse -Force .\dist-relative $env:TEMP\pages\7pro8-site
cd $env:TEMP\pages; python -m http.server 8080
# then open http://localhost:8080/7pro8-site/
```
