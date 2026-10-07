# Builder guide: homepage concepts (impeccable)

This is the shared playbook for every agent that builds or polishes a homepage concept in this repo. The direction contract for your concept, at `.impeccable/surfaces/concept-N-index-html.md`, decides the look. This guide covers everything else.

## Read first
1. `PRODUCT.md` (repo root): product truth, brand commitments, and the rules for globe journeys.
2. Your surface brief: `.impeccable/surfaces/concept-N-index-html.md`. Build that direction at full commitment, not a safer interpretation of it.
3. `/Users/z.christensen/.claude/plugins/cache/impeccable/impeccable/4.3.1/skills/impeccable/reference/craft-floor.md`: the quality floor and the bans. Re-read it right before editing.
4. For a polish pass, also read `.../reference/polish.md` in the same folder.

## Boundaries
- Edit only `concept-N/` (your number). You may add files inside it.
- Never edit:
  - `concept-12/` or any other concept
  - `tools/` (unless told to)
  - `PRODUCT.md`
  - `.impeccable/surfaces/`
  - this guide
- Do not commit or push. Do not run concept-seed or the decision page.
- Do not spawn the finish reviewer or documenter. The coordinator does that.

## The file
`concept-N/index.html` started as a byte copy of concept 12 (git tag `concept-12-v1`). It is a single self-contained HTML file of about 330KB with all CSS and JS inline.

### Tokens and nav
- `:root` tokens: `--red`, `--ink`, `--dark:#0B0B0E`, `--sans`, `--edge`. A lot of the CSS assumes a dark page.
- Nav: `header.nav.navx#nav`. Inside it:
  - `.row` grid
  - the `.wordmark` / `.lockup` SVG; its `.lk-word` path is white and fades on `.nav.scrolled`. Make it #111 on light grounds; the N stays red.
  - `nav.mnav` with `.mnav-btn` triggers that open `.mpanel` panels
  - `.nvright` with search, More and the `.apply` Giving pill
- The phone menu is `.tkv*`. `nav` gets the `solid` class (background) and the `scrolled` class (logo peel).

### Hero
`section.hx` contains:
- `#hxMedia` films (`.hl` layers)
- `.hx-title`, `.hx-syn`, `.hx-btn`
- `.hx-eps` story links
- `.hx-lineup .ln` tabs, with progress in `--pb`

It is driven by the `FEATS` JSON array in the script.

### NGN rows
`section.rows` holds `.crow.sp` sections (#ngnRow, #entRow, #aiRow, #uniRow, #researchRow). Each has a spotlight `.sp-*` and a scroll row `.crow-body`. Stories are fetched live from news.northeastern.edu. The `rows` URL param picks a layout variant: the default is `b`, and `b3` is the framed-photo layout.

### Globe
`#campuses.scrolly` holds `#stage`, with `canvas#globe` and the journeys UI `.hz`:
- `.hz-h`, `.hz-nav`
- `.hz-stops li`, each with a `.hz-p` city and a `.hz-x` note
- the map callout `.hz-call`

The canvas engine draws land, ocean, arcs and labels with colors set inside the script (search `render(`, `label(`, `fillStyle`, `strokeStyle`, `PATH_ARCS`).

### Research, closer, footer
- Research sheet: `.sheet #research`, with expanding `.xcard` cards and `.rc` stats.
- Closer: `section#admit.admit`, a lazy-loaded slideshow.
- `footer`

### Behavior to preserve
- dropdowns, phone menu, search overlay
- hero autoplay and tabs
- row arrows and auto-advance
- globe journeys, stops and hover-hold
- reduced motion
- keyboard focus

## Hard rules (learned from the first review round)
- **Brand:**
  - FF Real Head only (already @font-face'd; Lato fallback). No other faces, and no monospace.
  - Color: black/white primary, with greys #111111 #FAFAFA #F5F5F5 #E5E5E5 #D4D4D4 #A3A3A3 #737373 #404040.
  - Northeastern Red #C8102E as accent only, under 25% of any view.
  - Gold #A4804A / #C8A978 at most about 5%.
- **Copy:** approved copy does not change. Reordering hero features is allowed if your contract says so.
  - No kickers or eyebrows above headings. "From the newsroom" in the nav panels is approved copy: keep it as that column's own heading, at the same style as the sibling column headings.
- **Truth:**
  - Never invent places, coordinates, dates, stats or testimonials. Show a place only where the page has a source; the globe journey stops are the only sourced places.
  - Globe stops show city and note only: no coordinates, no "Student"/"Research" kind labels, no journey titles.
  - The research stats ($296M, 50+, 510) stay exactly as written, shown statically with no count-up and no "unverified" marker; the coordinator handles that with the user.
- **Globe motion is calm, and it's a hard requirement (the user got motion sickness).** Never change camera motion, zoom, speed, easing, or the flags FLY_NODIP and FLY_SLOW.
  - The engine's pins and arcs use an off-brand #EE5566 / rgba(238,85,102). Recolor them to #C8102E on the active stop and the leg in flight only, with grey or white elsewhere.
  - No zero-offset colored halos.
- **Icons:** no Unicode glyph icons (←, →, ×, +, &#8594;). Use one authored single-stroke SVG arrow family everywhere, including `.storylink` arrows, globe prev/next, the phone menu, and close buttons.
- **Craft floor "browser surfaces":** theme the text selection, caret, scrollbars, focus rings and underline offset, and use tabular numerals for figures.
- **One authored motion moment.** Remove blanket fade-up entrances, the stat count-up, and scattered effects. Exponential ease-out throughout.
- **Autoplay must be pausable:** the hero films need a visible pause/play control (SVG icon, accessible name that reflects state, keyboard-operable) that stops both the film and the lineup advance. Start paused under reduced motion.
- **All autoplay is pausable with a visible control, not just the hero.** The news rows' auto-advance and the closer slideshow each need a visible SVG pause/play control (state-reflecting accessible name, keyboard-operable). Pause-on-hover alone does not count.
- **Row titles are not eyebrows.** "Latest", "Entrepreneurship", "Human-Centered AI", "University News" and "Research" must never be a small label stacked on a larger spotlight headline. Make each a real heading that matches or outranks the spotlight headline, or restructure.
- **Footer wordmark:** the "y" descender in "Northeastern University" must not be clipped, on desktop or mobile.
- **No covering controls on phones:** no control (pause button, paddles) may cover the lineup or any text. Give scrollers a clean end (reserved space or an edge fade).
- **Gutters around rules:** content must never touch decorative rules or meridians; leave a real gutter between type or images and any hairline.
- **Accessibility:** WCAG AA contrast (sample real pixels when text sits on photos), no horizontal overflow at any width, no clipped text, and visible keyboard focus.
- Remove dead hidden elements that make broken requests (for example `#gtc-img` if unused).

## Verify (bounded passes)
- **Server:** `http://localhost:4610/concept-N/`, a python http.server serving the repo root. Check with curl; if it's down, start it with `python3 -m http.server 4610 --directory /Users/z.christensen/Projects/nu-homepage-prototype` in the background.
- **Playwright:** `require('/Users/z.christensen/environment/node_modules/playwright')`, headless Chromium.
  - For video under CSS blur or filters, launch with `args: ['--use-gl=angle','--enable-gpu']`, or headless renders it black.
  - Scroll with `window.lenis ? lenis.scrollTo(y,{immediate:true}) : scrollTo(0,y)`.
  - The globe section is pinned; wait about 2.5s for a stop to land, or wait for `.hz-call.on`.
- **Scratch files:** only under `/private/tmp/claude-506/-Users-z-christensen-environment--claude-worktrees-northeastern-netflix-hero-3fd1e4/39705b40-d144-48dd-8850-46465ee09514/scratchpad/cN/` (your concept number). Several agents share the scratchpad root.
- **Passes:** build fully, then one batched inspection round at 1440×900, 1280×800, 1024×768 and 390×844. Fix everything in one batch, then confirm with at most one more round.
- **Detector, once at the end:** `"/Users/z.christensen/.claude/plugins/cache/impeccable/impeccable/4.3.1/skills/impeccable/scripts/impeccable" detect --json concept-N/index.html` from the repo root. Fix the mechanical findings and list the rest.

## Final captures (all required) → `.impeccable/review/concept-N/`
- **Full-page captures:** first scroll the whole page top to bottom in about 60%-viewport steps, wait for the lazy images (closer and research) to finish loading, then return to the top. Without this, lazy images capture blank.
  - `desktop.png` (1440 wide, full page) and `mobile.png` (390 wide, full page).
- **Viewport captures:**
  - `hero-desktop.png` and `hero-mobile.png`: about 5s after a fresh load, with no prior hover.
  - `globe-desktop.png` and `globe-mobile.png`: with a stop landed.
  - `rows-desktop.png` and `rows-mobile.png`: the top of the news rows.
  - `research-desktop.png` and `research-mobile.png`
  - `closer-desktop.png` and `closer-mobile.png`: after the photo has loaded.
  - `nav-panel-desktop.png`: a dropdown open.
  - `menu-mobile.png`: the phone menu open.
- Open each file once to confirm it's valid. The globe canvas renders blank in full-page captures, which is expected; the globe-*.png files cover it.

## Report back (concise)
1. What your version does, section by section (one line each), and the signature interaction.
2. The capture paths.
3. Remaining detector findings, compromises, and anything unfinished (be honest).
4. Any copy or fact you were unsure about.
