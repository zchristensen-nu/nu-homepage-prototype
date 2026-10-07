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
rep('<meta name="concept12-rev" content="18">', '<meta name="concept15-rev" content="1">')
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
    'function navHere() { NAVFOR.forEach((n, k) => n && n.classList.toggle("here", hxVisible && k === cur)); }')
rep('  placeHere();\n  layers.forEach(l => l.classList.remove("was"));', '  placeHere(); navHere();\n  layers.forEach(l => l.classList.remove("was"));')
rep('  hxVisible = e.isIntersecting;', '  hxVisible = e.isIntersecting; navHere();')
open(f"{ROOT}/concept-15/index.html", "w", encoding="utf-8").write(s)
print("ok", len(s))
