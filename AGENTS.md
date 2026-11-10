# chalkwalkmusic.com

The source for chalkwalk's main website, and the place where the plan for
hosting it (and other public services) on Oracle Cloud is worked out.
`/home/programming/AGENTS.md` (the shared workspace notes) applies first; it
also describes the Oracle VM and the domains in general.

Status (2026-11-09): the new landing page is live at https://chalkwalkmusic.com
(GitHub Pages); the Google Site is retired. Decisions and next steps are
in `docs/hosting-plan.md`.

## Layout

- `site/`: the whole website, plain static HTML and CSS, no build step.
  `index.html`, `style.css`, `favicon.png`, `apple-touch-icon.png`, `img/` (the
  roundel, each project's own mark at 128 px from its site's `img/logo.*`, and
  the social card), `CNAME`.
- `.github/workflows/pages.yml`: deploys `site/` to GitHub Pages on every push to
  `main` that touches it.
- `docs/`: planning notes. Not published.
- `ops/ninjam-vm/`: the utilization recorder installed on the Oracle VM, which
  records every jam automatically (see its README).

GitHub: `chalkwalk/chalkwalkmusic.com` (public). Pages is set to deploy from
GitHub Actions, with the custom domain `chalkwalkmusic.com` (bare; `www` redirects to it).

Preview locally: open `site/index.html` in a browser, or
`python3 -m http.server -d site 8000`. Check it at phone width (390px) too.

## Design (third version, 2026-11-09)

The brand page for the person, not a fifth project site. chalkwalk rejected the
first version (near-black, Inter, cyan, identical cards) as looking AI-made or
stock; the brief is "a high-end brand": real information, presented directly,
bespoke. The second version (light chalk ground) got the layout right, but
chalkwalk prefers a dark background and wanted the Chalk Walk logo used.

- The logo is the "CW" roundel (orange C, cyan W, purple ring segments, dark
  aubergine outline): the YouTube and GitHub avatar. `img/chalkwalk.webp` is cut
  from the 1024 px YouTube avatar with a transparent edge; `favicon.png` and
  `apple-touch-icon.png` come from the same cut.
- Palette, all taken from the roundel: Ground `#1a0e15` (aubergine, not stock
  near-black), Ink `#eee8e4` (chalk), Muted `#a8979f`, Rule `#3a2834` (hairlines),
  Ring `#6b2a66` (section rules), Accent `#5ec6df` (the W: the line, links,
  subdomains), Hit `#f08920` (the C: the rhythm's hits, focus outlines).
- Type: Archivo with its width axis (wordmark at 125% width, weight 800; names at
  ~118%) and Source Serif 4 for all running text. No monospace, no all-caps labels,
  no middle-dot lists, no arrows.
- The one bold element: the roundel and "Chalk Walk" as one lockup, sized by
  `calc()` to span the column exactly, over a chalk-textured line that is the
  Euclidean rhythm E(5,16) (SVG with an feTurbulence filter). It draws once on
  load, at a constant pace; its resting state is drawn, and reduced motion skips
  the animation. The caption says what it is (beside the statement on desktop,
  directly under the line on phones). Two drawings of the same 16 steps, wide for
  desktop and compressed for phones (≤820px), so the whole rhythm always shows;
  `tools/walk.py` generates both into `index.html` between `<!--walk:…-->`
  markers. Don't edit the SVG by hand.
- Layout: an index. Each section has its name in a narrow left column (sticky on
  desktop) and content on the right; rows, not cards; left-aligned throughout.
  The hero uses the same grid.
- `img/social-card.jpg` (1200×630) is the link preview, rendered from the page's
  own CSS; re-render it if the hero changes.
- Voice: first person, plain, specific. The focus is the GitHub/dev work; teaching
  and music are one section. No Twitter/X.

## DNS (2026-11-09)

DNS for `chalkwalkmusic.com` is served by Squarespace Domains
(`ns-cloud-e{1..4}.googledomains.com`), edited in the Squarespace console;
only chalkwalk has access.

| Name | Record | Serves |
|---|---|---|
| apex | A 185.199.108–111.153 (GitHub Pages) | this site, the main address |
| `www` | CNAME `chalkwalk.github.io` | redirects to the apex |
| `_github-pages-challenge-chalkwalk` | TXT | GitHub domain verification; keep it |
| `m3dwkxsirt7c`, `p3ym6rf3yin6` | CNAME `…dv.googlehosted.com` | Google ownership checks; keep them |
| `antiphon` | CNAME `chalkwalk.github.io` | GitHub Pages of `chalkwalk/antiphon` |
| `arps` | CNAME `chalkwalk.github.io` | GitHub Pages of `chalkwalk/arps-euclidya` |
| `canopy` | CNAME `chalkwalk.github.io` | GitHub Pages of `chalkwalk/star-canopy` |
| `lockstep` | CNAME `chalkwalk.github.io` | GitHub Pages of `chalkwalk/lockstep` |
| `ninjam` | A 163.192.60.76 | the Oracle VM `ninjam` (Ninjam room, on demand) |
| MX | Google Workspace (`aspmx.l.google.com` + alts) | mail |
| TXT | `v=spf1 include:_spf.google.com ~all`; DKIM at `google._domainkey` | mail auth |

DMARC: `_dmarc` TXT `v=DMARC1; p=none; rua=mailto:dmarc@chalkwalkmusic.com`
(added 2026-11-09; reports only, nothing blocked). Tighten to `p=quarantine`, then
`p=reject`, once the reports show only Google sends as the domain. No CAA record.

All four GitHub Pages project sites use `build_type: workflow` (built by a GitHub
Actions workflow in each repository) with HTTPS enforced. `solvespace-ng` also
has Pages, at `chalkwalk.github.io/solvespace-ng/`, with no custom domain.

Any change to the website must leave MX, SPF and DKIM alone: mail is Google
Workspace and is unrelated to where the site is hosted.

Mail stays on Google Workspace (decided 2026-11-09): one user, used only for
email, under $1/month on a discount kept in perpetuity; the YouTube channel is on
a different account. Self-hosting mail was ruled out (Oracle blocks outbound port
25 by default; deliverability). Extra addresses are made in the Admin console:
aliases (Directory → Users → Add alternate emails, up to 30) for mail to
chalkwalk, Google Groups with external members for forwarding to others.

### The old Google Sites site (retired 2026-11-09), for reference

Three pages, all thin, out of date. Its custom domain was removed.
- **Home**: "Electronic Music & More": Chalk Walk is a person and Chalk Walk Music
  their electronic music and tech project; the YouTube channel is the main outlet
  (FM and subtractive synthesis, music theory, hardware and software).
- **Educational Content**: seven embedded YouTube tutorial series: Sonicware Liven
  XFM (sound design + a track walkthrough), subtractive synthesis, keyboard and music
  theory for synth players, Korg opsix, Sound Design Here:Create, ASM Hydrasynth.
- **Sound Design Here:Create** (`/SDHC`): prompt-driven sound design projects, each
  with source media and a finished piece: Sound for a Sculpture, Bloom & Wilt,
  Machine Life, Pine's Fog.
- Footer links: YouTube (`youtube.com/ChalkWalkMusic`), Bandcamp
  (`chalkwalk.bandcamp.com`), SoundCloud (`soundcloud.com/chalkwalk`), Twitch
  (`twitch.tv/chalk_walk`), Twitter/X (`@ChalkWalkMusic`).

Nothing on it mentions the software projects below.

## Public projects (github.com/chalkwalk, 2026-11-09)

Only public work goes on the site. Active (pushed in the last few months):

- **Plugins / apps**: `antiphon` (NINJAM client as a VST3/CLAP plugin, records
  stems; site at `antiphon.`), `lockstep` (playable step sequencer; site at
  `lockstep.`), `arps-euclidya` (euclidean arpeggiator, MPE; site at
  `arps.`, the most starred), `star-canopy`
  (procedural HDR space skyboxes; site at `canopy.`), `solvespace-ng` (SolveSpace
  fork with OCCT kernel and assemblies), `asteroid-generator` (Blender + numpy).
- **NINJAM ecosystem**: `chalkwalk-ninjam` (protocol library), `chalkwalk-jambot`
  (bots that play in a room), plus the monthly room on the Oracle VM and the
  planned `ninjam-balcony` web listener (local, not yet on GitHub).
- **Libraries** (C++17, JUCE-free, MIT): `chalkwalk-dsp`, `chalkwalk-tape`,
  `chalkwalk-music`, `chalkwalk-physical`, `chalkwalk-seed`; `chalkwalk-soundfont`
  (patched FluidLite).
- Older: `euclidean-arp` (prototype), `clipsort_merge`, `markwords`, `albgen`,
  `mpk261-bitwig` (fork).

`gh repo list chalkwalk` refreshes this.

## Oracle Cloud free allowance, as it applies here

Pay As You Go held inside Always Free (a $1 budget alert at 1%). What matters:
- Ampere A1: 4 OCPU and 24 GB in total, in steps of 1 OCPU / 6 GB per VM.
  The VM `ninjam` uses 2 OCPU / 12 GB.
- Two VM.Standard.E2.1.Micro (AMD, 1/8 OCPU, 1 GB): fine for tiny services only.
- **200 GB block storage in total, boot volumes included.** A boot volume is at
  least ~47 GB, so storage, not CPU, caps the number of VMs at four (e.g. three A1s
  and one micro, or two A1s and two micros), and each extra VM eats the room
  left for data volumes.
- About 10 TB/month outbound. Network speed per VM as chalkwalk understood it at
  sign-up: ~50 Mbit/s public, 480 Mbit/s between VMs (to be confirmed by measuring).
- Being on Pay As You Go, idle Always Free VMs are not reclaimed (Oracle reclaims
  idle ones only on free-trial/free-only accounts). New A1 capacity in a region can
  run out, so don't terminate a working A1 VM expecting to recreate it at once.
- Anything outside Always Free is billable; check the shape says "Always Free
  eligible" before creating anything.
