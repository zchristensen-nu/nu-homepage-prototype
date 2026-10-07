import re, sys, os
ROOT = "/Users/z.christensen/Projects/nu-homepage-prototype"
SC = os.path.dirname(os.path.abspath(__file__))
s = open(f"{ROOT}/concept-12/index.html", encoding="utf-8").read()
css = open(f"{SC}/wayfinding.css", encoding="utf-8").read()

def rep(old, new, count=1, regex=False):
    global s
    if regex:
        s2, n = re.subn(old, new, s, count=0 if count == 0 else count, flags=re.S)
    else:
        n = s.count(old)
        s2 = s.replace(old, new) if count == 0 else s.replace(old, new, count)
    if n == 0:
        sys.exit(f"NOT FOUND: {old[:90]!r}")
    s = s2

AR = '<svg class="ar" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 12h17M13.5 5.5 20 12l-6.5 6.5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
AL = '<svg class="ar" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12H4M10.5 5.5 4 12l6.5 6.5" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
X = '<svg class="ic" viewBox="0 0 22 22" aria-hidden="true"><path d="M5 5l12 12M17 5 5 17" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
PLUS = '<svg class="tkv-c" viewBox="0 0 22 22" aria-hidden="true"><path d="M11 4v14M4 11h14" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'

# meta + title
rep('<meta name="concept12-rev" content="18">', '<meta name="concept15-rev" content="2">')
# stylesheet: append the Wayfinding layer at the end of the main <style>
i = s.index("</style>")
s = s[:i] + css + s[i:]

# glyph icons -> authored SVG
rep('aria-label="Close search">&times;</button>', f'aria-label="Close search">{X}</button>')
rep('aria-label="Close menu">&times;</button>', f'aria-label="Close menu">{X}</button>')
rep('<span class="tkv-c" aria-hidden="true">+</span>', PLUS, count=0)
rep('AI<span aria-hidden="true">&#8594;</span></a>', f'AI{AR}</a>')
rep('Read on NGN &#8594;</span>', 'Read on NGN</span>', count=0)
rep('aria-label="Previous story">&#8592;</button>', f'aria-label="Previous story">{AL}</button>')
rep('aria-label="Next story">&#8594;</button>', f'aria-label="Next story">{AR}</button>')
rep('<span aria-hidden="true"> →</span>', '', count=0)
rep('aria-label="Previous path">←</button>', f'aria-label="Previous path">{AL}</button>', count=0)
rep('aria-label="Next path">→</button>', f'aria-label="Next path">{AR}</button>', count=0)

# hero: film panel, white headline sign, black directory with the travelling marker
m = re.search(r'<div class="hx-media" id="hxMedia">.*?</video></div></div>', s, re.S)
media = m.group(0)
labels = re.findall(r'<button class="ln" data-i="(\d)" aria-pressed="(\w+)">.*?<span class="ln-t">(.*?)</span><i class="ln-pb"></i></button>', s)
assert len(labels) == 5, labels
lns = "".join(f'<button class="ln" data-i="{i}" aria-pressed="{p}"><span class="ln-t">{t}</span>{AR}<i class="ln-pb"></i></button>' for i, p, t in labels)
hero = f'''<section class="hx" id="top" aria-label="Featured">
  <h1 class="vh">Northeastern University</h1>
  <div class="hx-film">{media}</div>
  <div class="hx-in" id="hxIn">
    <div class="hx-copy" aria-live="polite">
      <h2 class="hx-title" id="hxTitle">Learn by doing</h2>
      <p class="hx-syn" id="hxSyn">Every part of your journey at Northeastern is built for immersive learning, innovation, and integrating emerging technologies, like AI, to enhance creativity and career readiness.</p>
      <a class="hx-btn sbtn" id="hxCta" href="#" hidden><span id="hxCtaL"></span>{AR}</a>
    </div>
  </div>
  <div class="hx-shows" id="hxShows">
    <div class="hx-lineup" role="group" aria-label="Choose a feature"><span class="hx-here" aria-hidden="true"></span>{lns}</div>
    <aside class="hx-eps" id="hxEps" aria-label="Stories from this feature"></aside>
  </div>
</section>'''
rep(r'<section class="hx" id="top" aria-label="Featured">.*?</section>', hero.replace("\\", "\\\\"), regex=True)

# research: the way onward as a directory row
rep('<a class="storylink rv" style="margin-top:34px" href="https://news.northeastern.edu/category/research/">More research on NGN</a>',
    f'<a class="onward" href="https://news.northeastern.edu/category/research/"><span>More research on NGN</span>{AR}</a>')

# closer: black sign beside the photographs; the three CTAs become directory rows, Apply carries the marker
m = re.search(r'(<section class="admit" id="admit">\s*)(<div class="bg".*?</div>)(\s*<div class="inner">.*?)<div class="ctas">.*?</div>', s, re.S)
ctas = re.findall(r'<a class="pill[^"]*" href="([^"]+)">([^<]+)</a>', m.group(0))
assert [c[1] for c in ctas] == ["Apply", "Visit", "Financial aid"], ctas
rows = "".join(f'<a class="dir{" here" if k == 0 else ""}" href="{h}"><span>{t}</span>{AR}</a>' for k, (h, t) in enumerate(ctas))
s = s[:m.start()] + m.group(1) + f'<div class="admit-media">{m.group(2)}</div>' + m.group(3) + f'<div class="ctas">{rows}</div>' + s[m.end():]

# ---- JS ----
rep('const ARROW = `<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h9M8.5 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>`',
    f'const ARROW = `{AR}`')
# row paddles: arrows, not chevrons
rep('<path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>',
    '<path d="M3 12h17M13.5 5.5 20 12l-6.5 6.5" fill="none" stroke="currentColor" stroke-width="1.6"/>', count=0)
# story rows default to the framed spotlight, on alternating faces
rep('get("rows") || "b").toLowerCase()', 'get("rows") || "b3").toLowerCase()')
rep('else { topics.forEach(tp => mountRow(tp.sec, tp.items)); if (RV === "a") previews(topics); }',
    'else { topics.forEach(tp => mountRow(tp.sec, tp.items)); if (RV === "a") previews(topics); }\n'
    '  $$(".rows .crow").filter(x => !x.hidden).forEach((x, k) => x.classList.add(k % 2 ? "face-k" : "face-w"));')

# hero: the directory and the billboard are one control
rep('''  lnBtns.forEach((b, k) => { b.setAttribute("aria-pressed", k === i ? "true" : "false"); b.style.setProperty("--pb", 0); });
  if (i === cur) return;
  const from = cur; cur = i;
  layers[from].classList.remove("on"); layers[i].classList.add("on");''',
'''  lnBtns.forEach((b, k) => { b.setAttribute("aria-pressed", k === i ? "true" : "false"); b.style.setProperty("--pb", 0); });
  if (i === cur) return;
  const from = cur; cur = i;
  placeHere();
  layers.forEach(l => l.classList.remove("was"));
  layers[from].classList.remove("on"); layers[from].classList.add("was"); layers[i].classList.add("on");
  clearTimeout(selectF.wt); selectF.wt = setTimeout(() => layers[from].classList.remove("was"), reduceMotion ? 0 : 820);''')
rep('setTimeout(() => { fillHero(FEATS[i]); hxIn.classList.remove("swap"); }, reduceMotion ? 0 : 350);',
    'clearTimeout(selectF.ct); selectF.ct = setTimeout(() => { fillHero(FEATS[cur]); hxIn.classList.remove("swap"); }, reduceMotion ? 0 : 170);')
rep('lnBtns.forEach(b => b.addEventListener("click", () => selectF(+b.dataset.i)));',
'''lnBtns.forEach(b => b.addEventListener("click", () => selectF(+b.dataset.i)));
/* pointing at a destination is enough: hover (with a short intent delay) or keyboard focus switches the film */
const here = $(".hx-here");
function placeHere() { const b = lnBtns[cur]; if (here && b) here.style.setProperty("--here-y", (b.offsetTop + b.offsetHeight / 2) + "px"); }
let hvT;
lnBtns.forEach(b => {
  b.addEventListener("pointerenter", e => { if (e.pointerType !== "mouse") return; clearTimeout(hvT); hvT = setTimeout(() => selectF(+b.dataset.i), 110); });
  b.addEventListener("pointerleave", () => clearTimeout(hvT));
  b.addEventListener("focus", () => selectF(+b.dataset.i));
});''')
rep('const layout = () => { fitTitles(); fitHeroTitle(); hx.style.setProperty("--shh", shows.offsetHeight + "px"); };',
    'const layout = () => { fitTitles(); fitHeroTitle(); placeHere(); };')
# the hero no longer drifts on scroll: it is a fixed sign, not a parallax plate
rep(r'/\* leaving the billboard: the film eases back and the copy lets go \*/\nif \(!reduceMotion\) \{.*?\n\}\n', '', regex=True)
# hero: the eps
rep("`<a class=\"ep\" href=\"${esc(e.u)}\"><img src=\"${esc(e.img)}\" alt=\"\" loading=\"lazy\"><span>${esc(e.t)}</span></a>`",
    "`<a class=\"ep\" href=\"${esc(e.u)}\"><img src=\"${esc(e.img)}\" alt=\"\" loading=\"lazy\"><span>${esc(e.t)}</span></a>`")

# globe: brand red for the pins, white for the trail (motion untouched)
g0 = s.index("/* ============ globe engine ============ */")
g1 = s.index("/* ============ globe on phones")
seg = s[g0:g1].replace('"#EE5566"', '"#C8102E"').replace("rgba(238,85,102,", "rgba(200,16,46,").replace("rgba(255,190,200,", "rgba(255,255,255,")
s = s[:g0] + seg + s[g1:]

# globe ground: neutral brand greys instead of cool slate (camera untouched)
g0 = s.index("/* ============ globe engine ============ */"); g1 = s.index("/* ============ globe on phones")
seg = s[g0:g1]
for a, b in [('g.addColorStop(0, "#1A1B22"); g.addColorStop(1, "#101014");', 'g.addColorStop(0, "#000"); g.addColorStop(1, "#000");'),
             ('ctx.fillStyle = "#26262D";\n  ctx.strokeStyle = "rgba(255,255,255,.09)";', 'ctx.fillStyle = "#111111";\n  ctx.strokeStyle = "#404040";'),
             ('rgba(226,230,242,', 'rgba(229,229,229,'), ('rgba(0,0,6,', 'rgba(0,0,0,')]:
    assert a in seg, a
    seg = seg.replace(a, b)
s = s[:g0] + seg + s[g1:]
# the globe is locked and plays journeys on its own: say so
s, n = re.subn(r'<canvas id="globe" aria-label="[^"]*"', '<canvas id="globe" role="img" aria-label="A globe that plays journeys between Northeastern locations, one stop at a time. Use the arrow buttons to change journey."', s)
assert n == 1
# the active destination is marked in the top nav too, while the hero is on screen
rep('lnBtns.forEach(b => b.addEventListener("click", () => selectF(+b.dataset.i)));',
    'lnBtns.forEach(b => b.addEventListener("click", () => selectF(+b.dataset.i)));\n'
    'const NAVFOR = [1, 2, 3, 5, 4].map(k => $$("#nav .mnav > *")[k]);  /* Co-op: Experiential Learning; then Research, Global Network, AI, Entrepreneurship */\n'
    'function navHere() { const on = hxVisible && scrollY < innerHeight * .5; NAVFOR.forEach((n, k) => n && n.classList.toggle("here", on && k === cur)); }\n'
    'addEventListener("scroll", () => requestAnimationFrame(navHere), { passive: true });')
rep('  placeHere();\n  layers.forEach(l => l.classList.remove("was"));', '  placeHere(); navHere();\n  layers.forEach(l => l.classList.remove("was"));')
rep('  hxVisible = e.isIntersecting;', '  hxVisible = e.isIntersecting; navHere();')
# ---- polish pass (builder-guide hard rules) ----
rep('  .storylink::after{content:"\\2192";transition:transform .25s var(--ease)}\n', '')
PAUSE_SVG = ('<svg class="ic ic-pause" viewBox="0 0 22 22" aria-hidden="true"><path d="M8 5v12M14 5v12" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>'
             '<svg class="ic ic-play" viewBox="0 0 22 22" aria-hidden="true"><path d="M7 4.5v13l11-6.5z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>')
# hero films: a visible pause/play control that stops the film and the lineup advance
rep('<div class="hx-film"><div class="hx-media" id="hxMedia">', '<div class="hx-film"><button class="hx-pause" id="hxPause" type="button" aria-label="Pause films">' + PAUSE_SVG + '</button><div class="hx-media" id="hxMedia">')
rep('const playI = i => { const v = vidOf(i); if (v && !reduceMotion) v.play().catch(() => {}); };',
    'let paused = reduceMotion;  /* reduced motion starts paused: posters, no advance */\n'
    'const playI = i => { const v = vidOf(i); if (v && !paused) v.play().catch(() => {}); };')
rep('''if (!reduceMotion) {
  let lastT = 0;
  const tick = now => {
    const dt = lastT ? Math.min(100, now - lastT) : 0; lastT = now;
    if (hxVisible && !hoverShows''', '''{
  let lastT = 0;
  const tick = now => {
    const dt = lastT ? Math.min(100, now - lastT) : 0; lastT = now;
    if (hxVisible && !paused && !hoverShows''')
rep('fillHero(FEATS[0]);\nplayI(0);', '''fillHero(FEATS[0]);
/* pause/play: one control for the film and the lineup advance; its name says what it will do */
const pauseBtn = $("#hxPause");
function setPaused(v) {
  paused = v;
  pauseBtn.setAttribute("aria-label", v ? "Play films" : "Pause films");
  pauseBtn.classList.toggle("is-paused", v);
  const vd = vidOf(cur);
  if (vd) { if (v) vd.pause(); else if (hxVisible) vd.play().catch(() => {}); }
}
pauseBtn.addEventListener("click", () => setPaused(!paused));
setPaused(paused);
playI(0);''')

# research stats: static, exactly as written (no count-up)
for n in ("296", "50", "510"):
    rep(f'<span data-count="{n}">0</span>', n)
rep(r"let countersDone = false;\nnew IntersectionObserver\(es => es\.forEach\(e => \{\n  if \(e\.isIntersecting && !countersDone\) \{.*?\}\), \{ threshold: 0\.4 \}\)\.observe\(\$\(\"#counters\"\)\);\n", "", regex=True)

# the unused co-op story card: removed, and the code that referenced it made null-safe
rep(r'\s*<aside class="gt-card" id="gt-card" hidden aria-label="Co‑op story">.*?</aside>', '', regex=True)
rep('const gtCard = $("#gt-card");', 'const gtCard = $("#gt-card") || { hidden: true, getBoundingClientRect: () => null };')
rep('function fillCard(i) {\n', 'function fillCard(i) {\n  if (!$("#gtc-img")) return;\n')
rep('$("#gtc-prev").addEventListener(', '$("#gtc-prev")?.addEventListener(')
rep('$("#gtc-next").addEventListener(', '$("#gtc-next")?.addEventListener(')

# globe marks: red only on the active stop and the leg in flight; grey and white elsewhere; no colored halos
g0 = s.index("/* ============ globe engine ============ */"); g1 = s.index("/* ============ globe on phones")
seg = s[g0:g1]
for a, b in [
    ('ctx.fillStyle = `rgba(11,11,14,${.55 * a})`;', 'ctx.fillStyle = `rgba(0,0,0,${.6 * a})`;'),
    ('''      ctx.beginPath(); ctx.arc(x, y, 8.5, 0, 7);
      ctx.fillStyle = `rgba(200,16,46,${.28 * cur.campus})`; ctx.fill();
      ctx.beginPath(); ctx.arc(x, y, 4.6, 0, 7);
      ctx.fillStyle = `rgba(200,16,46,${cur.campus})`; ctx.fill();''',
     '''      ctx.beginPath(); ctx.arc(x, y, 4.6, 0, 7);
      ctx.fillStyle = `rgba(163,163,163,${cur.campus})`; ctx.fill();'''),
    ('''      ctx.strokeStyle = `rgba(200,16,46,${.16 * fadeA})`; ctx.lineWidth = 5; ctx.stroke();
      ctx.strokeStyle = `rgba(255,255,255,${.75 * fadeA})`; ctx.lineWidth = 1.3; ctx.stroke();''',
     '''      /* the leg in flight is the red one; once the camera lands it settles to white */
      ctx.strokeStyle = f < 1 ? `rgba(200,16,46,${fadeA})` : `rgba(255,255,255,${.75 * fadeA})`;
      ctx.lineWidth = f < 1 ? 1.8 : 1.3; ctx.stroke();'''),
    ('''      const p = ((now + i * 400) % 2400) / 2400;
      ctx.beginPath(); ctx.arc(x, y, 7 + p * 16, 0, 7);
      ctx.strokeStyle = `rgba(200,16,46,${(1 - p) * .5 * cur.spins})`;
      ctx.lineWidth = 1.6; ctx.stroke();
      const boost = (typeof storySel !== "undefined" && i === storySel) ? 1.4 : 1;
      ctx.beginPath(); ctx.arc(x, y, 5 * boost, 0, 7);
      ctx.fillStyle = `rgba(200,16,46,${.95 * cur.spins})`; ctx.fill();''',
     '''      const on = typeof storySel !== "undefined" && i === storySel;  /* the active stop is the only red pin */
      ctx.beginPath(); ctx.arc(x, y, on ? 6.5 : 4.5, 0, 7);
      ctx.fillStyle = on ? `rgba(200,16,46,${cur.spins})` : `rgba(229,229,229,${.95 * cur.spins})`; ctx.fill();'''),
    ('''      ctx.beginPath(); ctx.arc(x, y, 6 + p * 22, 0, 7);
      ctx.strokeStyle = `rgba(200,16,46,${(1 - p) * .9})`; ctx.lineWidth = 2; ctx.stroke();
''', ''),
]:
    assert a in seg, a[:80]
    seg = seg.replace(a, b)
s = s[:g0] + seg + s[g1:]
# ---- review round 3 ----
# row headings: directory signs that link to their live NGN section
ROWS = [("Latest", "https://news.northeastern.edu/"),
        ("Entrepreneurship", "https://news.northeastern.edu/tag/entrepreneurship/"),
        ("Human-Centered AI", "https://news.northeastern.edu/tag/artificial-intelligence/"),
        ("University News", "https://news.northeastern.edu/category/university-news/"),
        ("Research", "https://news.northeastern.edu/category/research/")]
for t, u in ROWS:
    rep(f'<div class="wrap"><h3>{t}</h3></div>', f'<div class="wrap crow-head"><h3><a class="rowlink" href="{u}"><span>{t}</span>{AR}</a></h3></div>')
# row auto-advance: a visible pause/play per row
rep('''  if (!reduceMotion) {
    const tickS = now => {
      const dt = lastS ? Math.min(100, now - lastS) : 0; lastS = now;
      if (visS && !hoverS''', '''  let pausedS = reduceMotion;
  const head = sec.querySelector(":scope > .wrap");
  head.insertAdjacentHTML("beforeend", '<button class="rp" type="button" aria-label="Pause stories">' + PAUSE_ICONS + '</button>');
  const rp = head.querySelector(".rp");
  const setRowPaused = v => { pausedS = v; rp.classList.toggle("is-paused", v); rp.setAttribute("aria-label", v ? "Play stories" : "Pause stories"); };
  rp.addEventListener("click", () => setRowPaused(!pausedS));
  setRowPaused(pausedS);
  {
    const tickS = now => {
      const dt = lastS ? Math.min(100, now - lastS) : 0; lastS = now;
      if (visS && !pausedS && !hoverS''')
rep('const fmtDate = d =>', 'const PAUSE_ICONS = `' + PAUSE_SVG + '`;\nconst fmtDate = d =>')
# closer: no parallax; a visible pause/play for the photo crossfade
rep('<div class="admit-media"><div class="bg" data-plx="34">', '<div class="admit-media"><button class="hx-pause ad-pause" id="adPause" type="button" aria-label="Pause photos">' + PAUSE_SVG + '</button><div class="bg">')
rep('  let k = 0, vis = false, started = false;', '  let k = 0, vis = false, started = false, adPaused = reduceMotion;')
rep('    if (vis && !document.hidden) {\n      shots[k].classList.remove("on");', '    if (vis && !adPaused && !document.hidden) {\n      shots[k].classList.remove("on");')
rep('if (!reduceMotion) setTimeout(step, 5000); }', 'setTimeout(step, 5000); }')
rep('  }), { rootMargin: "800px 0px" }).observe(admit);', '''  }), { rootMargin: "800px 0px" }).observe(admit);
  const ap = $("#adPause");
  const setAd = v => { adPaused = v; ap.classList.toggle("is-paused", v); ap.setAttribute("aria-label", v ? "Play photos" : "Pause photos"); };
  ap.addEventListener("click", () => setAd(!adPaused));
  setAd(adPaused);''')
# no count-up code left
rep(r'/\* ============ research counters ============ \*/\nfunction countUp\(el, to, ms\) \{.*?\n\}\n', '', regex=True)
# stats as ruled directory rows (figure, label)
rep('<div class="rc-grid" id="counters">', '<div class="rc-grid rc-rows" id="counters">')
# globe ground: no atmosphere lift around the limb
g0 = s.index("/* ============ globe engine ============ */"); g1 = s.index("/* ============ globe on phones")
seg = s[g0:g1]
a = 'atm.addColorStop(0.4, "rgba(229,229,229,.04)");'
assert a in seg; seg = seg.replace(a, 'atm.addColorStop(0.4, "rgba(229,229,229,0)");')
s = s[:g0] + seg + s[g1:]
open(f"{ROOT}/concept-15/index.html", "w", encoding="utf-8").write(s)
print("ok", len(s))
