# SESSION CONTINUATION — CLAW Command Deck

**Project:** CLAW // Philip Command Deck — the website at https://claw.outtatime.dev
**Status:** LIVE — full 10-section command center (v3)
**Last Updated:** 2026-06-04 (v3 — all sections restored)

## Where everything is

- **Local source (THIS directory):** `/Volumes/Expansion/claw-command-deck/`
- **GitHub:** https://github.com/pdubbbbbs/claw-command-deck (public)
- **Hosting:** GitHub Pages (branch `main`, root) — NOT Manus, NOT Hetzner
- **DNS:** Cloudflare zone `outtatime.dev`, CNAME `claw` → `pdubbbbbs.github.io` (DNS-only)
- Full docs, architecture, history, troubleshooting: see `README.md` here

## What was done (2026-06-04 session)

1. Diagnosed "site reverted to old version": DNS still pointed at the abandoned
   Manus deployment (`clawassist-bqyvbier.manus.space`, build frozen May 14).
   The "advanced version" Philip remembered was the May 31 Roku deck redesign,
   which had never been deployed to the web.
2. Rebuilt the advanced deck as a static web app (floating glass repo cards,
   live GitHub data, README detail views, keyboard nav, ember particles).
3. Created GitHub repo `pdubbbbbs/claw-command-deck`, enabled GitHub Pages with
   custom domain claw.outtatime.dev.
4. Repointed the Cloudflare CNAME from Manus to `pdubbbbbs.github.io` via API.

## Next steps / open items

- [ ] Verify HTTPS cert fully issued, then enable "Enforce HTTPS" in repo
      Settings → Pages (`gh api -X PUT repos/pdubbbbbs/claw-command-deck/pages -F https_enforced=true`)
- [ ] Optional: re-enable Cloudflare proxy (orange cloud) on the `claw` record
      after the GitHub cert is issued — works fine gray, proxy adds CF caching/WAF
- [ ] Optional: periodic refresh of baked `repos.json` (command in README)
- [ ] Consider porting extra sections from the old Manus "Personal Claw"
      (Expansion Drive file index, AI chat) — would need a backend, this site is
      intentionally static
- [ ] Old Manus mirror repo `pdubbbbbs/personal-claw` kept for history — do not deploy

## Resume command

```bash
cd /Volumes/Expansion/claw-command-deck && claude
```

## v3 update (same day)

Restored ALL sections from the original Personal Claw (content ported from
pdubbbbbs/personal-claw source): Command Deck home, Repositories, Search,
Ask CLAW (local index), Expansion Drive, Topics, Infrastructure (LIVE
homelab.json feed from the Synology gen-homelab.sh, baked fallback),
Projects (full 5-phase runbook), Tools & Scripts, Hardware Setup.

Open item: live Infrastructure feed needs an Access-Control-Allow-Origin
header on roku.philipwright.me/feeds/ to work in browsers (currently the
deck falls back to the baked snapshot). Add via the cloudflared/Web Station
config on the Synology, or a Cloudflare response-header rule on the
philipwright.me zone.

Open item (paused, user deprioritized): delete wellnessbylisa.fit and
wellness-invoice repos from GitHub — needs `gh auth refresh -h github.com -s delete_repo`.
They're already excluded from the deck client-side.
