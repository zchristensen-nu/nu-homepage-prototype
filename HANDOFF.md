# Northeastern homepage redesign prototype — full handoff

High-fidelity redesign prototype of the www.northeastern.edu homepage, built July 2026.
This doc is the complete knowledge dump: where everything lives, every design decision and
directive, the technical architecture, the deploy workflow, and open items. Written so a
fresh session (or fresh Claude account) can pick up with zero prior context.

## Where everything lives

| Thing | Location |
|---|---|
| **Live site** | https://zchristensen-nu.github.io/nu-homepage-prototype/ |
| **GitHub repo** | https://github.com/zchristensen-nu/nu-homepage-prototype (public, personal account `zchristensen-nu`, NOT the org) |
| **Deployed page** | `index.html` in this repo (single self-contained file, ~195KB) |
| **Hero video** | `hero.mp4` in this repo (14.7MB, 1920×1080, ~20s) |
| **Canonical working copy** | `~/environment/prototypes/northeastern-homepage-v2.html` — same bytes as `index.html`. Lives in the work monorepo but is **untracked there** (never committed to the org repo). This GitHub repo is the only version control it has. |
| **Asset manifest** | `ASSETS.md` in this repo (copied from `~/environment/prototypes/nu-homepage-assets.md`) — brand colors/fonts/logos, video URLs, campus + N.U.in coordinates, vetted NGN story list |
| **v1 prototype** | `~/environment/prototypes/northeastern-homepage.html` — the original lower-fidelity version from a claude.ai chat (source of the co-op map data). Superseded; kept for reference only, not in GitHub. |

The current page carries `<meta name="prototype-rev" content="NN">` (rev **45** as of this
writing). Bump it on every deploy — it's how you verify which version is live
(`curl -s <live-url> | grep prototype-rev`).

## Page structure (top to bottom), and how each section was decided

Most sections were chosen by building 2–4 competing variants, deploying them side-by-side
with a fixed switcher bar, and having Zach pick. Winners were folded into the canonical
page and the variants deleted.

1. **Hybrid mega nav** (winner over a takeover-only variant). Transparent over the hero,
   turns **black** (`rgba(11,11,14,.92)`) on scroll — not gray. Red **N monogram** (inline
   data-URI PNG, un-blended from the brand favicon), not the full wordmark. Five top-level
   items (Admissions, Academics, Experiential Learning, Research, Global & Campuses) with
   dark hover-open mega panels (90ms enter / 280ms leave intent delays; click on touch).
   Each panel: a lead block, labeled sub-columns, and a "From the newsroom" featured NGN
   story card. "More" opens a full takeover overlay which doubles as the mobile menu
   (<960px). Search overlay POSTs to search.northeastern.edu (input `name="query"`).
2. **Hero**: self-hosted `hero.mp4` full-bleed video (see Video notes), headline
   "Experience. Everything. Anywhere.", one paragraph, ONE CTA ("See where they are" →
   globe section). No quick-link pills, no "watch the co-op experience" link — both were
   explicitly removed.
3. **Globe scrolly** (winner: "Scrolly" over "Tour" and "Split" variants). Canvas globe,
   4 scroll steps: 13 campuses → 8 N.U.in launch cities → co-op counter (counts to 4,705
   with dot-ignition sweep) → outro. A **staple story card** (can't be dismissed) docks on
   the right during the co-op beat with 5 co-op stories, prev/next stepper, and red pins on
   the globe. First beat rides in with the section (steps are `margin-top:-100svh`);
   camera interpolates on entry progress so the globe is never top-cropped.
4. **Research** ("Adobe-style" expanding cards). Headline is brand-approved language:
   "Our research story starts in the world." + the pillar lede. Five cards with hand-tuned
   `object-position` focal points (verified by actually looking at each photo).
5. **Quote carousel** (winner: "Bare" card — no red quote mark, no keyline). Real curly
   quotes in the text, `text-wrap:balance`, bottom-left→top-right gradient scrim, track
   and slides capped at 1240–1440px. All quotes are **verbatim from NGN articles**.
6. **Student life "IMAX"** (winner over tunnel/dolly/lanes/filmstrip/cinema variants).
   "Class is only half of it." pinned in a CSS-perspective 3D corridor; images pass on
   lanes (12–18° tilt), blur up to 9px as they near the camera, velocity-reactive FOV warp
   (950px→~610px). Text releases with a velocity-matched rise (`t*(2-t)`) so there's no
   scroll snag; images pre-decode via IntersectionObserver at 150% rootMargin.
7. **Admissions closer ("Your turn.")**: Fenway commencement photo with parallax, now with
   a scroll-in reveal (rev 45): image fades from black over 1.4s at ~35% visibility;
   headline/line/CTAs rise 26px staggered 0/.18s/.36s. Fires once. Photo credit caption
   was removed. Reduced-motion gets everything instantly.
8. **Footer**: nav-level IA. Head row: N monogram + address + social **text links**
   (Facebook, X, YouTube, LinkedIn, Instagram, TikTok). Seven-column link grid
   (`repeat(7,1fr)` → 4 → 2 responsive), including a Quick Links column (Registrar,
   Directory, Libraries, Emergency Information). Legal base bar (Privacy Policy,
   Accessibility, **Cookie Preferences as a `<button>`**, © line). Below: giant
   **solid-white** wordmark, cropped by the section bottom (`transform: translateY(22%)`),
   contained to the same `.wrap` container as everything else — the "Adobe big-logo" trend,
   done subtle.

## Standing design directives (Zach's accumulated rules — apply to ALL future edits)

- **No em dashes anywhere** in copy.
- **"co-op" must NEVER split across two lines.** Use the literal non-breaking hyphen
  character U+2011 (`co‑op`) — NOT the `&#8209;` entity, which renders literally when set
  via `textContent`.
- **No eyebrow labels** (all-caps, letter-spaced accent text). Let headings speak.
  This includes location labels on cards — redesigned to plain sentence-case with no
  tracking.
- **No red accent glyphs** — no red periods, no red quote marks, no red dots before
  locations. Red stays under 25% of any composition (brand rule).
- **Minimal text; "show, don't tell."** Cut supporting copy hard.
- **Subtle premium motion.** Globe zoom dips capped (~6%), soft outer glow, no city-light
  bloom, no arcs. Motion sickness complaints came from big camera moves — keep them gentle.
- **Brand-approved language only** for section voice — pull from
  brand.northeastern.edu/voice-and-messaging/. Use "advances, develops, discovers"; avoid
  "groundbreaking, revolutionary, world-class."
- **Quotes are verbatim from NGN articles.** Never fabricate or trim into new meanings.
- **Content sits in a max-width container** (~1280px, footer wordmark included) on wide
  viewports.
- **Focal points matter**: when cropping editorial photos, look at the actual image and set
  `object-position` so faces/subjects survive the crop.
- Every section links real NGN stories (news.northeastern.edu) — the page doubles as an
  NGN showcase.

## Technical architecture (single self-contained HTML file)

- **No build step, no external JS deps.** Everything inline: Lenis smooth scroll v1.1.14
  (vendored, lerp 0.12), the globe engine, all data.
- **Globe engine** (vanilla canvas): orthographic projection with
  `project(lat,lng,R,cx,cy,alt)`; land rendered from `const LAND` (Natural Earth 110m,
  ~59KB; 50m was rejected — 568KB+). Far-side polygon points are rim-pushed, and visible
  segments are closed with **horizon arcs along the limb** — this is the fix that stops
  Antarctica's pole ring flooding the whole disk; don't "simplify" it away.
- **Layer system**: `LAYER_KEYS` on `cur`/`tgt` objects with eased opacity per layer
  (coops/campus/nuin/labels/spins). Camera flights via `startFly()` — two-phase with a
  zoom dip capped at `Math.min(0.12,(dist/180)*0.25)*Math.min(from.k,to.k,2)/2`.
- **Labels**: 8-candidate placement walk per label (collision-avoiding). All 13 campus and
  8 N.U.in labels must place — verified; don't regress to drop-on-collision.
- **Co-op data**: `const COOPS`, 519 rows `[lat,lng,n,city,country]` (~23KB), total 4,705.
- **Counter**: dot-ignition sweep synced to the count-up; counter refresh must also run
  inside the caption-swap callback (fixes "0" after instant jumps).
- **Scroll choreography**: scroll handlers + IntersectionObservers. The `.rv` class is the
  generic reveal system; the admissions closer uses its own observer (threshold .35).
- **Position:sticky** does the pinning — never wrap a sticky section in `overflow:hidden`
  (it silently kills sticky; bit us once on the Cinema variant).
- **Fonts**: FF Real Head hotlinked from northeastern.edu webfont files. **Images**: all
  hotlinked from news.northeastern.edu uploads. Fine for a prototype; both would need
  proper hosting for anything real.
- **N monogram**: 4KB transparent data-URI PNG inline (alpha reconstructed from the green
  channel of the brand favicon, which had a baked background).

## Deploy workflow

1. Edit the canonical: `~/environment/prototypes/northeastern-homepage-v2.html`
   (assert-guarded Python string-replace scripts have been the safest way — **if any assert
   fails, abort the whole script**; a partial patch once shipped rev 40 broken).
2. Bump `prototype-rev` meta.
3. Copy byte-identical to the repo: `cp` to `~/Projects/nu-homepage-prototype/index.html`
   (also keep `~/environment/prototypes/hero.mp4` beside the canonical so the relative
   video src works locally).
4. Commit + push to `origin` (HTTPS, auth via `gh` credential helper).
5. **GitHub Pages legacy builder is flaky** — builds randomly error. Poll
   `gh api repos/zchristensen-nu/nu-homepage-prototype/pages/builds/latest --jq .status`
   and on `errored`, retrigger with
   `gh api -X POST repos/zchristensen-nu/nu-homepage-prototype/pages/builds`. Loop until
   `built`, then confirm the live rev:
   `curl -s "https://zchristensen-nu.github.io/nu-homepage-prototype/?nc=$RANDOM" | grep prototype-rev`.
   Pages caches ~10 min; always bust with a `?nc=` query when checking.
6. `.nojekyll` is present — keep it.

## Video notes

- Current hero: Zach's "Hero Video Test.mov" transcoded to `hero.mp4` via **macOS
  `avconvert --preset Preset1920x1080`** (no ffmpeg on the machine).
- Deferred: compress below ~5MB (ffmpeg CRF ~26) + poster frame, if this footage is kept.
- Previous hero (hotlinkable fallback):
  `https://www.northeastern.edu/wp-content/uploads/The-Co-Op-Experience_Video-2-Fusion-v3.mp4`

## Verification gotchas (hard-won)

- **Lenis fights programmatic scrolling** in tests — `scrollIntoView` gets pulled back.
  Use the page's own anchor clicks, `lenis.scrollTo`, or double-scrollTo with delays.
- Synthetic `mouseenter` with `bubbles:true` falsely fails hover tests (real mouseenter
  doesn't bubble) — dispatch with `bubbles:false`.
- The Claude Code browser pane sometimes runs tabs as `document.visibilityState==="hidden"`:
  rAF freezes, **IntersectionObservers never fire**, screenshots go blank after any JS
  call. That's a pane artifact, not a page bug — verify observers by computed-style checks
  after adding classes manually, or eyeball the live site in a real browser.
- Same artifact makes autoplay video look paused in the pane; a successful `play()` with
  nonzero `currentTime` proves autoplay is actually fine.

## Open items / known gaps

- **Social link URLs** in the footer use standard handles from general knowledge — verify
  against the live site's footer before showing anyone.
- **Entrepreneurship** nav link is `href="#"` — no URL was ever provided.
- The **drone rail image** in the research section is a text-baked thumbnail — weakest
  photo on the page; candidate for swap.
- Hero video is 14.7MB — fine for a prototype, compress if kept (see Video notes).
- The rev-45 entrance animation was verified by computed styles + code review but not
  visually observed live (pane artifact above) — worth one human scroll-through.

## Concept 2: the elevated v1 (current direction)

Lives at **https://zchristensen-nu.github.io/nu-homepage-prototype/concept-2/**
(`concept-2/index.html`, meta `concept2-rev`, rev 6). Direction settled after two
discarded explorations (a 24/7 dashboard, then a literal one-day narrative): **take v1
and raise it to award-site grammar** (references: landonorris.com, schemeengine.com),
articulate the three pillars (Global network / Experiential / Research), tie in the NGN
stream, and replace the globe with a different global expression. Zach's fixed point:
the pinned horizontal photo+giant-stat gallery is the one loved pattern; keep it.

- Built by `tools/build_c3.py` from the v1 canonical: keeps v1's hero video (path
  rewritten to `../hero.mp4`), quotes, IMAX life, closer, footer, nav + overlays.
- New: award motion layer (preloader with rAF-independent failsafes, custom cursor
  with mix-blend difference, grain, clip-reveal lines); an NGN wire ticker under the
  hero and above the footer that **fetches live headlines from the NGN REST API**
  (CORS verified; baked August list is the fallback); the globe replaced by "Boston is
  only the beginning.", a 560svh pinned rail: Boston (live clock) > 14 campuses >
  London (live clock) > N.U.in cities > a canvas constellation of the real 519-city
  co-op dataset igniting with rail progress > the loved photo/stat gallery (4,705 /
  519 / 3,000+ / 151 with linked, verified co-op story captions) > "Where will yours
  be?"; research rebuilt as a two-beat platform on light background: the approved
  headline + investment line over giant count-up numerals ($296M / 50+ / 510, v1's
  counter JS reused) + a drag shelf of 8 dated, verified research stories.
- Rev 7 (Zach's second pass): rail reframed to the real campus hierarchy (Boston flagship
  + Oakland/NYC/London undergraduate, "10 more campuses with graduate programs", N.U.in);
  the v1 globe engine returned as a rail panel (slow spin, white campus labels, red co-op
  dots, drag + hover tooltips); co-op stats switched to ALL-TIME figures **that are
  unverified placeholders by Zach's instruction: 500K+ placed / 5,000+ cities / 10,000+
  employers / 250+ countries and territories. VERIFY all four before any external eyes;
  "250+" exceeds the number of countries on Earth unless territories genuinely carry it.**
  Research counters respaced (rules + tabular numerals), drag hint removed; the quote
  carousel is now a full-bleed auto-advancing cinema with line reveals and progress bars;
  student life headline is "Some of this you can't major in."; the wire reads the
  `newspost` REST type (the editorial feed; `seen-around` is the photo-of-the-day type).
- Earlier concept-2 builders remain for history (`tools/build_c2.py`, superseded).

## Provenance

- Built across several Claude Code sessions in `~/environment` (the NGN monorepo), July
  2026, iterating with Zach Christensen. The original v1 concept came from a claude.ai
  chat whose HTML Zach pasted in.
- All editorial content (headlines aside), imagery, and quotes are from
  news.northeastern.edu; brand rules from brand.northeastern.edu. This is an internal
  design exploration, not a published university property.
