# CLAW // Philip Command Deck

> **THE website at `https://claw.outtatime.dev`** — Philip S. Wright's command center.
> Cybernetic-noir dashboard for the public GitHub fleet: floating glass repo cards,
> live data, README detail views, fully keyboard-driven.

---

## ⚡ TL;DR — what is this and where does it live?

| Question | Answer |
|---|---|
| **What is it?** | The CLAW command center website ("Philip Command Deck") |
| **Live URL** | https://claw.outtatime.dev |
| **Hosted on** | **GitHub Pages**, served from `pdubbbbbs/claw-command-deck` (branch `main`, root) |
| **DNS** | Cloudflare zone `outtatime.dev` → CNAME `claw` → `pdubbbbbs.github.io` (DNS-only) |
| **Source of truth** | GitHub repo `pdubbbbbs/claw-command-deck`. Local working copy: `/Volumes/Expansion/claw-command-deck/` |
| **Build step?** | **None.** Pure static — `index.html` + `repos.json`. Edit, commit, push = deployed. |
| **NOT hosted on** | ~~Manus~~ (migrated off June 4, 2026 — see History), not Hetzner, not the homelab |

## 🚀 How to update the site

```bash
cd /Volumes/Expansion/claw-command-deck
# edit index.html (single self-contained file)
git add -A && git commit -m "update deck" && git push
# GitHub Pages redeploys automatically in ~30 seconds
```

To refresh the baked fallback repo data (`repos.json`) — only used when the GitHub
API is unreachable/rate-limited in the visitor's browser:

```bash
gh api "users/pdubbbbbs/repos?per_page=100&sort=pushed" \
  --jq '{generated: (now|strftime("%Y-%m-%d")), total: length, repos: [.[] | {name, desc: (.description // ""), lang: (.language // "—"), stars: .stargazers_count, pushed: (.pushed_at[:10]), url: .html_url, topics}]}' \
  > repos.json
git add repos.json && git commit -m "chore: refresh baked repo data" && git push
```

## 🎛 Features

- **Floating glass repo cards** — glassmorphism, cyan glow + lift on hover/focus, drifting float animation
- **Live GitHub data** — fetches `api.github.com/users/pdubbbbbs/repos` client-side; falls back to baked `repos.json` (statline shows `LIVE` vs `CACHED`)
- **Repo detail view** — language · ★stars · pushed date · topics, plus the full rendered README (sanitized)
- **Keyboard-driven** — `?` help overlay, `/` focus filter, arrow keys between cards, `Enter` opens, `Esc` backs out
- **Filter + language dropdown**, live clock, language-distribution statline
- **Ambient FX** — drifting cyan ember particles (canvas), CRT scanlines, perspective grid floor
- **Security** — public repos only (private repos filtered from baked data, never fetched); README HTML sanitized (scripts/event-handlers/`javascript:` URLs stripped)

Design language: black `#04070a`, cyan `#22d3ee`, JetBrains Mono, terminal-noir. Ported from
the Roku CLAW deck (`/Volumes/Expansion/roku/philip-tv/`) built May 31, 2026.

## 🗺 Architecture

```
┌──────────────────────┐     CNAME claw → pdubbbbbs.github.io
│ Cloudflare DNS       │ ◄── (zone: outtatime.dev, record kept DNS-only/gray cloud)
└─────────┬────────────┘
          ▼
┌──────────────────────┐     repo: pdubbbbbs/claw-command-deck (main, /)
│ GitHub Pages         │ ◄── CNAME file in repo pins claw.outtatime.dev
└─────────┬────────────┘
          ▼
  index.html  ── client-side fetch ──►  api.github.com (public repos, READMEs)
  repos.json  (baked fallback, public repos only)
```

## 📜 History — read this before "fixing" anything

- **May 12–14, 2026** — v1/v2 built by **Manus** ("Personal Claw"), served at claw.outtatime.dev
  via CNAME to `clawassist-bqyvbier.manus.space`. Source mirror: `pdubbbbbs/personal-claw` (history only).
- **May 31, 2026** — the much richer "floating glass deck" redesign was built **for Roku**
  (`/Volumes/Expansion/roku/philip-tv/`) and never reached the website — which made the site
  look like it had "reverted" by comparison.
- **June 4, 2026** — this repo: the Roku deck design rebuilt for the web, deployed to GitHub
  Pages, Cloudflare CNAME repointed from Manus to `pdubbbbbs.github.io`. **Manus is fully out of the loop.**

## 🧭 Disambiguation — similarly-named things that are NOT this project

| Thing | What it is | Where |
|---|---|---|
| `pdubbbbbs/personal-claw` | OLD Manus version of this site (May 2026) — keep for history, do not deploy | GitHub (private) |
| **Hermes** | AI agent on a Hetzner VPS (`5.78.214.21`) | `hermes.philipwright.me` |
| `claw.philipwright.me` | noVNC embedded desktop on the Hermes VPS — **different project, different domain** | Hetzner |
| `ClawCommandCenter.app` | Swift/WKWebView macOS shell that *displays* this website | `/Volumes/Expansion/command_center/` |
| Roku CLAW deck | BrightScript port of this design for Philip TV | `/Volumes/Expansion/roku/philip-tv/` |

## 🔧 Troubleshooting

- **Site looks old/wrong** → check DNS first: `dig +short claw.outtatime.dev` must resolve via
  `pdubbbbbs.github.io`. If it shows `*.manus.space`, the CNAME regressed — fix it in Cloudflare
  (zone `outtatime.dev`, record `claw`).
- **Empty deck / "CACHED"** → visitor hit the GitHub API rate limit (60/hr unauthenticated); the baked
  fallback takes over automatically. Refresh `repos.json` if stale (see above).
- **Cert errors after DNS changes** → GitHub repo Settings → Pages: re-save the custom domain and
  re-enable "Enforce HTTPS" after the cert reissues; keep the Cloudflare record gray-cloud (DNS only)
  during issuance.

---
*CLAW // Philip S. Wright · [github.com/pdubbbbbs](https://github.com/pdubbbbbs) · [philipwright.me](https://philipwright.me)*
