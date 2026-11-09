# Hosting plan: chalkwalkmusic.com and the Oracle free allowance

Facts are in `../AGENTS.md`; this is what was decided and what is left to do.

## Decisions (2026-11-09)

- **The site** is a professional landing page, static, on **GitHub Pages**
  (`site/` in this repository, deployed by `.github/workflows/pages.yml`). It
  leads with the GitHub/dev work; music and video are a short section. No
  Twitter/X. Bandcamp and SoundCloud stay as links (inactive, may return); YouTube
  is paused but will come back.
- **Subdomains** stay on GitHub Pages, one per project site: `antiphon.`,
  `arps.`, `canopy.`, `lockstep.`. `ninjam.` is the Oracle VM.
- **Squarespace** is only the registrar and DNS; nothing else is paid there.
- **Oracle**: one VM only. Shrink `ninjam` to 1 OCPU / 6 GB; it is used a few
  hours a month and idles at ~0.6 GB of RAM. It can host other small services
  later (the balcony, maybe a jambot room). No second VM, no micros for now.
- **Backups**: not on Oracle. GitHub already holds the code. Moving repos off the
  Raspberry Pi, and finding roomier free cloud storage, are for later.
- **Always-open jambot room**: maybe later.

## Steps to go live

1. Create the GitHub repository `chalkwalk/chalkwalkmusic.com` (public) and push
   `main`.
2. Repository settings → Pages → Source: GitHub Actions. Custom domain:
   `www.chalkwalkmusic.com`. Wait for the workflow to deploy.
3. Squarespace DNS (chalkwalk only):
   - `www`: CNAME `chalkwalk.github.io` (instead of `ghs.googlehosted.com`).
   - apex: replace the Squarespace A record (and the domain forwarding) with
     GitHub's four A records `185.199.108.153`, `.109.153`, `.110.153`,
     `.111.153`. GitHub then redirects the bare domain to `www` over HTTPS,
     which also fixes today's redirect to plain http.
   - leave MX, SPF and DKIM alone. Optionally add DMARC:
     `_dmarc` TXT `v=DMARC1; p=none; rua=mailto:<an address you read>`.
4. Once the certificate is issued, tick "Enforce HTTPS" in Pages settings.
5. Optional: verify the domain in GitHub (account settings → Pages → verified
   domains; adds one TXT record) so no one else can claim a subdomain of it on
   GitHub Pages.
6. In Google Sites, remove the custom domain from the old site (or unpublish it).

## Shrinking `ninjam`

Oracle console → Instances → `ninjam` → Edit → shape → 1 OCPU / 6 GB. The VM
reboots; do it outside a jam. Before that, make its public IP reserved
(Networking → the VNIC → IPv4 addresses) so it can't change if the VM is ever
recreated, and check the IP after the reboot. It can be grown back the same way.
Measure the first jam with the balcony to confirm it fits.

## Later

- Jam dates and how to join on the site (the Jam section says "will be posted
  here" for now). Next jam date, an `.ics` feed.
- An archive of past jams (the stems `jam-stems` renders) on the site.
- The balcony at `ninjam.chalkwalkmusic.com` with Caddy on the VM.
- Off-site storage for what isn't on GitHub or the Pi.
