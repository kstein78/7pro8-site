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

## 4. Production, when the domain is ready

Server preparation, the Caddy configuration and the required secrets are in
**README.md** under "Deployment". Once the server answers and the DNS records
point at it:

1. Add the four repository secrets: `SSH_PRIVATE_KEY`, `SSH_HOST`, `SSH_USER`,
   `SSH_KNOWN_HOSTS`.
2. Run **Actions → Deploy to Hetzner (production) → Run workflow**.
3. Check `https://www.7pro8.com/robots.txt` — it must read `Allow: /`, not
   `Disallow: /`. If it disallows, the build ran with `SITE_PREVIEW=1`.
4. Paste the contents of `dist/_redirects.caddy` into the Caddyfile so the old
   Squarespace addresses keep working, and reload Caddy.

To make production deploys automatic afterwards, add the `push:` trigger back to
`.github/workflows/deploy-hetzner.yml` — the comment at the top of the file says
where.

Keep the Squarespace subscription running until the domain has switched and you
have downloaded the photographs from its CDN (see IMAGES.md).

## Local checks before pushing

```bash
pip install -r requirements.txt
python build.py                # production build into dist/
python tools/check_links.py    # every internal link and asset
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
