#!/usr/bin/env python3
"""Concept 16 (Conversation): built from the frozen concept 12 bytes.
Reads concept-12/index.html (never writes it), writes concept-16/index.html."""
import re, pathlib, sys

REPO = pathlib.Path("/Users/z.christensen/Projects/nu-homepage-prototype")
HERE = pathlib.Path(__file__).parent
src = (REPO / "concept-12/index.html").read_text()
s = src


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if count is not None and n != count:
        sys.exit(f"expected {count} of {old[:90]!r}, found {n}")
    s = s.replace(old, new)


def rx(pat, new, count=1, flags=re.S):
    global s
    s2, n = re.subn(pat, new, s, flags=flags)
    if count is not None and n != count:
        sys.exit(f"expected {count} of /{pat[:90]}/, found {n}")
    s = s2


# ---------- one single-stroke icon family (16px grid, 1.6 stroke, round caps) ----------
def ic(d, cls="ic"):
    return (f'<svg class="{cls}" width="16" height="16" viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
            f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')


ARW = ic("M3 8h9M8.5 4l4 4-4 4")
ARW_L = ic("M13 8H4M7.5 4l-4 4 4 4")
ARW_UP = ic("M8 13V4M4 7.5l4-4 4 4")
CLOSE = ic("M4 4l8 8M12 4l-8 8")
PLUS = ic("M4 6l4 4 4-4")  # menu groups open on a chevron, distinct from close
PAUSE = ic("M5.75 4v8M10.25 4v8", "ic i-pause")
PLAY = ic("M5.5 3.6v8.8L12.4 8z", "ic i-play")
SEARCH = ('<svg class="ic-s" width="18" height="18" viewBox="0 0 20 20" fill="none" aria-hidden="true" focusable="false">'
          '<circle cx="9" cy="9" r="6.5" stroke="currentColor" stroke-width="1.6"/>'
          '<path d="M14 14l4.5 4.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>')


def composer(cls, input_attrs, label_id):
    return (f'<form action="https://search.northeastern.edu" method="get" role="search" class="cmp {cls}">'
            f'{SEARCH}<label class="vh" for="{label_id}">Search Northeastern</label>'
            f'<input type="search" name="query" id="{label_id}" placeholder="Search Northeastern" autocomplete="off" enterkeyhint="search"{input_attrs}>'
            f'<button type="submit" class="cmp-send" aria-label="Search">{ARW_UP}</button></form>')


rep('<meta name="concept12-rev" content="18">', '<meta name="concept16-rev" content="1">\n<meta name="description" content="Northeastern University: experiential learning, research, and a global university system.">')

# ---------- icons: replace every Unicode glyph icon ----------
rep('<path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>',
    '<path d="M3 8h9M8.5 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>', None)
rep('<svg width="30" height="30" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 8h9', '<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h9', None)
rep('stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></a>', 'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></a>')
rep('const ARROW = `<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h9M8.5 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.8"',
    'const ARROW = `<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h9M8.5 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.6"')
rep('<span class="fl">Read on NGN &#8594;</span>', '<span class="fl">Read on NGN</span>', 4)
rep('aria-label="Close search">&times;</button>', f'aria-label="Close search">{CLOSE}</button>')
rep('aria-label="Close menu">&times;</button>', f'aria-label="Close menu">{CLOSE}</button>')
rep('<span class="tkv-c" aria-hidden="true">+</span>', f'<span class="tkv-c" aria-hidden="true">{PLUS}</span>', 7)
rep('AI<span aria-hidden="true">&#8594;</span></a>', f'AI<span aria-hidden="true">{ARW}</span></a>')
rep('aria-label="Previous story">&#8592;</button>', f'aria-label="Previous story">{ARW_L}</button>')
rep('aria-label="Next story">&#8594;</button>', f'aria-label="Next story">{ARW}</button>')
rep('aria-label="Previous path">←</button>', f'aria-label="Previous path">{ARW_L}</button>', 2)
rep('aria-label="Next path">→</button>', f'aria-label="Next path">{ARW}</button>', 2)
rep('<span aria-hidden="true"> →</span>', ' ' + ARW, 3)

# ---------- search overlay and phone-menu search become the composer ----------
rx(r'<div class="srch" id="srch" hidden>.*?</div>\n<div class="tkv"',
   '<div class="srch" id="srch" hidden>\n  <div class="wrap srch-in">'
   + composer("cmp-ov", "", "srch-in")
   + f'<button type="button" class="srch-x" id="srch-x" aria-label="Close search">{CLOSE}</button></div>\n</div>\n<div class="tkv"')
rx(r'<form action="https://search.northeastern.edu" method="get" role="search" class="tkv-search">\s*<input[^>]*>\s*</form>',
   '<div class="tkv-search">' + composer("cmp-menu", "", "tkv-q") + '</div>')

# ---------- hero: media card + the response column (response, suggestion chips, composer) ----------
m = re.search(r'<div class="hx-media" id="hxMedia">.*?</div></div>\n', s, re.S)
media = m.group(0).strip()
m2 = re.search(r'<div class="hx-lineup".*?</div>\n', s, re.S)
lineup = m2.group(0).strip()
rx(r'<section class="hx" id="top" aria-label="Featured">.*?</section>\n<main>',
   '<section class="hx" id="top" aria-label="Featured">\n'
   '  <h1 class="vh">Northeastern University</h1>\n'
   '  <div class="hx-grid">\n'
   '    <div class="hx-card">\n      ' + media + '\n'
   f'      <button class="hx-pp" id="hxPP" type="button" aria-label="Pause video">{PAUSE}{PLAY}</button>\n'
   '    </div>\n'
   '    <div class="hx-chat">\n'
   '      <div class="hx-in" id="hxIn">\n'
   '        <div class="hx-copy" aria-live="polite">\n'
   '          <h2 class="hx-title" id="hxTitle">Learn by doing</h2>\n'
   '          <p class="hx-syn" id="hxSyn">Every part of your journey at Northeastern is built for immersive learning, innovation, and integrating emerging technologies, like AI, to enhance creativity and career readiness.</p>\n'
   f'          <a class="hx-btn" id="hxCta" href="#" hidden><span id="hxCtaL"></span>{ARW}</a>\n'
   '        </div>\n'
   '        <aside class="hx-eps" id="hxEps" aria-label="Stories from this feature"></aside>\n'
   '      </div>\n'
   '      <div class="hx-shows" id="hxShows">\n        ' + lineup + '\n      </div>\n'
   '      ' + composer("cmp-hero", "", "cmpQ") + '\n'
   '    </div>\n'
   '  </div>\n'
   '</section>\n<main>')

# ---------- research: no reveal fades, static figures ----------
rep('class="sechead rv"', 'class="sechead"')
rep('class="xrow rv"', 'class="xrow"')
rep('<a class="storylink rv" style="margin-top:34px"', '<a class="storylink rc-more"')
rep('$<span data-count="296">0</span>M', '$296M')
rep('<span data-count="50">0</span>+', '50+')
rep('<span data-count="510">0</span>', '510')
rx(r'/\* ============ research counters ============ \*/.*?(?=/\* ============ research expanding row)', '')

# ---------- closer: a rounded photo card, the invitation set beneath it ----------
rx(r'<section class="admit" id="admit">\n  (<div class="bg") data-plx="34"(>.*?</div>)\n  <div class="inner">',
   r'<section class="admit" id="admit">\n  <div class="wrap">\n  <div class="ad-card">\1\2</div>\n  <div class="inner">')
rep('''      <a class="pill red" href="https://admissions.northeastern.edu/">Apply</a>
      <a class="pill ghostw" href="https://admissions.northeastern.edu/visit/">Visit</a>
      <a class="pill ghostw" href="https://studentfinance.northeastern.edu/">Financial aid</a>
    </div>
  </div>
</section>''', '''      <a class="pill solid" href="https://admissions.northeastern.edu/">Apply</a>
      <a class="pill" href="https://admissions.northeastern.edu/visit/">Visit</a>
      <a class="pill" href="https://studentfinance.northeastern.edu/">Financial aid</a>
    </div>
  </div>
  </div>
</section>''')

# ---------- globe engine: light ground, red only for the active stop and the leg in flight ----------
rep("ctx.save(); ctx.shadowColor = `rgba(0,0,0,${.85 * a})`; ctx.shadowBlur = 10;\n    ctx.fillStyle = `rgba(255,255,255,${a})`;",
    "ctx.save();\n    ctx.fillStyle = `rgba(17,17,17,${a})`;")
rep("ctx.fillStyle = `rgba(11,11,14,${.55 * a})`;\n  ctx.fillRect(bx, by, w + 12, 18);\n  ctx.fillStyle = `rgba(255,255,255,${.95 * a})`;",
    "ctx.fillStyle = `rgba(255,255,255,${.94 * a})`;\n  ctx.fillRect(bx, by, w + 12, 18);\n  ctx.fillStyle = `rgba(17,17,17,${a})`;")
rep('''  atm.addColorStop(0, "rgba(226,230,242,0)");
  atm.addColorStop(0.4, "rgba(226,230,242,.04)");
  atm.addColorStop(1, "rgba(226,230,242,0)");''', '''  atm.addColorStop(0, "rgba(17,17,17,.035)");
  atm.addColorStop(0.4, "rgba(17,17,17,.012)");
  atm.addColorStop(1, "rgba(17,17,17,0)");''')
rep('g.addColorStop(0, "#1A1B22"); g.addColorStop(1, "#101014");', 'g.addColorStop(0, "#FFFFFF"); g.addColorStop(1, "#FFFFFF");')
rep('ctx.strokeStyle = "rgba(255,255,255,.045)"; ctx.lineWidth = 1;', 'ctx.strokeStyle = "rgba(17,17,17,.05)"; ctx.lineWidth = 1;')
rep('ctx.fillStyle = "#26262D";\n  ctx.strokeStyle = "rgba(255,255,255,.09)";', 'ctx.fillStyle = "#F5F5F5";\n  ctx.strokeStyle = "rgba(115,115,115,.38)"; ctx.lineWidth = .7;')
rep('''  term.addColorStop(0, "rgba(0,0,6,0)");
  term.addColorStop(0.55, "rgba(0,0,6,0)");
  term.addColorStop(1, "rgba(0,0,6,.5)");''', '''  term.addColorStop(0, "rgba(17,17,17,0)");
  term.addColorStop(0.6, "rgba(17,17,17,0)");
  term.addColorStop(1, "rgba(17,17,17,.04)");''')
rep('ctx.strokeStyle = "rgba(255,255,255,.14)"; ctx.lineWidth = 1.2; ctx.stroke();', 'ctx.strokeStyle = "rgba(17,17,17,.14)"; ctx.lineWidth = 1; ctx.stroke();')
rep("ctx.strokeStyle = `rgba(255,255,255,${.30 * a})`;", "ctx.strokeStyle = `rgba(115,115,115,${.35 * a})`;")
rep("ctx.fillStyle = `rgba(210,210,222,${.6 * a})`;", "ctx.fillStyle = `rgba(115,115,115,${.45 * a})`;")
rep("ctx.fillStyle = `rgba(255,255,255,${cur.nuin})`; ctx.fill();", "ctx.fillStyle = `rgba(64,64,64,${cur.nuin})`; ctx.fill();")
rep("ctx.strokeStyle = `rgba(255,255,255,${.4 * cur.nuin})`; ctx.lineWidth = 1; ctx.stroke();", "ctx.strokeStyle = `rgba(64,64,64,${.3 * cur.nuin})`; ctx.lineWidth = 1; ctx.stroke();")
# campus pins: grey marks (red is reserved for the active stop)
rep('''      ctx.beginPath(); ctx.arc(x, y, 8.5, 0, 7);
      ctx.fillStyle = `rgba(200,16,46,${.28 * cur.campus})`; ctx.fill();
      ctx.beginPath(); ctx.arc(x, y, 4.6, 0, 7);
      ctx.fillStyle = `rgba(200,16,46,${cur.campus})`; ctx.fill();
      ctx.lineWidth = 1.4;
      ctx.strokeStyle = `rgba(255,255,255,${.85 * cur.campus})`; ctx.stroke();''', '''      ctx.beginPath(); ctx.arc(x, y, 4.6, 0, 7);
      ctx.fillStyle = `rgba(64,64,64,${cur.campus})`; ctx.fill();
      ctx.lineWidth = 1.4;
      ctx.strokeStyle = `rgba(255,255,255,${cur.campus})`; ctx.stroke();''')
# arcs: the leg in flight is red; earlier legs settle to grey
rep('''    for (const arc of window.PATH_ARCS) {''', '''    const legNow = window.PATH_ARCS[window.PATH_ARCS.length - 1];
    for (const arc of window.PATH_ARCS) {
      const live = arc === legNow;''')
rep('''      ctx.strokeStyle = `rgba(238,85,102,${.16 * fadeA})`; ctx.lineWidth = 5; ctx.stroke();
      ctx.strokeStyle = `rgba(255,190,200,${.75 * fadeA})`; ctx.lineWidth = 1.3; ctx.stroke();
      if (head && f < 1) { ctx.beginPath(); ctx.arc(head[0], head[1], 3, 0, 7); ctx.fillStyle = `rgba(255,255,255,${.95 * fadeA})`; ctx.fill(); }''',
    '''      ctx.strokeStyle = live ? `rgba(200,16,46,${fadeA})` : `rgba(115,115,115,${.6 * fadeA})`; ctx.lineWidth = live ? 1.6 : 1.2; ctx.stroke();
      if (head && f < 1) { ctx.beginPath(); ctx.arc(head[0], head[1], 3, 0, 7); ctx.fillStyle = `rgba(200,16,46,${fadeA})`; ctx.fill(); }''')
# story pins: no pulsing rings; the active stop is the one red pin
rep('''      const p = ((now + i * 400) % 2400) / 2400;
      ctx.beginPath(); ctx.arc(x, y, 7 + p * 16, 0, 7);
      ctx.strokeStyle = `rgba(238,85,102,${(1 - p) * .5 * cur.spins})`;
      ctx.lineWidth = 1.6; ctx.stroke();
      const boost = (typeof storySel !== "undefined" && i === storySel) ? 1.4 : 1;
      ctx.beginPath(); ctx.arc(x, y, 5 * boost, 0, 7);
      ctx.fillStyle = `rgba(238,85,102,${.95 * cur.spins})`; ctx.fill();
      ctx.lineWidth = 1.5;
      ctx.strokeStyle = `rgba(255,255,255,${.9 * cur.spins})`; ctx.stroke();''', '''      const on = typeof storySel !== "undefined" && i === storySel;
      ctx.beginPath(); ctx.arc(x, y, on ? 6 : 4.2, 0, 7);
      ctx.fillStyle = on ? `rgba(200,16,46,${cur.spins})` : `rgba(115,115,115,${cur.spins})`; ctx.fill();
      ctx.lineWidth = on ? 2 : 1.5;
      ctx.strokeStyle = `rgba(255,255,255,${cur.spins})`; ctx.stroke();''')
rep('''      const p = (now % 2200) / 2200;
      ctx.beginPath(); ctx.arc(x, y, 6 + p * 22, 0, 7);
      ctx.strokeStyle = `rgba(238,85,102,${(1 - p) * .9})`; ctx.lineWidth = 2; ctx.stroke();
      ctx.beginPath(); ctx.arc(x, y, 5.5, 0, 7);
      ctx.fillStyle = "#EE5566"; ctx.fill();''', '''      ctx.beginPath(); ctx.arc(x, y, 5.5, 0, 7);
      ctx.fillStyle = "#C8102E"; ctx.fill();''')
rep('"background:rgba(16,16,20,.85);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,.14);" +\n  "border-radius:8px;padding:8px 11px;font-size:12.5px;line-height:1.4;color:#fff;max-width:220px";',
    '"background:#FFFFFF;border:1px solid #E5E5E5;box-shadow:0 6px 18px rgba(17,17,17,.08);" +\n  "border-radius:14px;padding:8px 12px;font-size:12.5px;line-height:1.4;color:#111111;max-width:220px";')

# ---------- billboard: the response streams in; chips choose; a real pause control ----------
rep('''const playI = i => { const v = vidOf(i); if (v && !reduceMotion) v.play().catch(() => {}); };
function fillHero(f) {
  $("#hxTitle").textContent = f.h;
  $("#hxSyn").textContent = f.syn;
  const cta = $("#hxCta");
  cta.hidden = !f.cta;
  if (f.cta) { cta.href = f.cta.href; $("#hxCtaL").textContent = f.cta.label; }
  $("#hxEps").innerHTML = f.eps.slice(0, 3).map(e =>
    `<a class="ep" href="${esc(e.u)}"><img src="${esc(e.img)}" alt="" loading="lazy"><span>${esc(e.t)}</span></a>`).join("");
}''', '''/* the film plays until the visitor pauses it; reduced motion starts paused */
let hxPaused = reduceMotion;
const playI = i => { const v = vidOf(i); if (v && !hxPaused) v.play().catch(() => {}); };
const hxPP = $("#hxPP");
const ppSync = () => { hxPP.classList.toggle("paused", hxPaused); hxPP.setAttribute("aria-label", hxPaused ? "Play video" : "Pause video"); };
hxPP.addEventListener("click", () => {
  hxPaused = !hxPaused; ppSync();
  const v = vidOf(cur);
  if (v) { if (hxPaused) v.pause(); else v.play().catch(() => {}); }
});
ppSync();
/* the response streams in word by word, once per feature (instantly under reduced motion);
   screen readers get the whole sentence from the hidden copy, never the fragments */
const STREAM_MS = 38;
const streamTo = (el, text, i0) => {
  const ws = text.split(/\\s+/);
  el.innerHTML = `<span class="vh">${esc(text)}</span><span class="st" aria-hidden="true">` +
    ws.map((w, k) => `<span class="w" style="--i:${i0 + k}">${esc(w)}</span>`).join(" ") + `</span>`;
  return i0 + ws.length;
};
function fillHero(f) {
  let n = streamTo($("#hxTitle"), f.h, 0);
  n = streamTo($("#hxSyn"), f.syn, n + 5);
  const cta = $("#hxCta");
  cta.hidden = !f.cta;
  if (f.cta) { cta.href = f.cta.href; $("#hxCtaL").textContent = f.cta.label; }
  $("#hxEps").innerHTML = f.eps.slice(0, 3).map(e =>
    `<a class="ep" href="${esc(e.u)}"><img src="${esc(e.img)}" alt="" loading="lazy"><span>${esc(e.t)}</span></a>`).join("");
  [cta, $("#hxEps")].forEach(el => { el.style.setProperty("--i", n + 3); el.classList.remove("tail"); void el.offsetWidth; el.classList.add("tail"); });
}''')
rep('''  hxIn.classList.add("swap");
  setTimeout(() => { fillHero(FEATS[i]); hxIn.classList.remove("swap"); }, reduceMotion ? 0 : 350);''',
    '''  hxIn.classList.add("swap");
  setTimeout(() => { fillHero(FEATS[i]); hxIn.classList.remove("swap"); }, reduceMotion ? 0 : 200);''')
rep('''if (!reduceMotion) {
  let lastT = 0;
  const tick = now => {
    const dt = lastT ? Math.min(100, now - lastT) : 0; lastT = now;
    if (hxVisible && !hoverShows && !document.hidden && scrollY < innerHeight * .3) {''', '''{
  let lastT = 0;
  const tick = now => {
    const dt = lastT ? Math.min(100, now - lastT) : 0; lastT = now;
    if (!hxPaused && hxVisible && !hoverShows && !document.hidden && scrollY < innerHeight * .3) {''')
rx(r'/\* card titles wrap by word; shrink only when.*?document\.fonts\.ready\.then\(layout\); layout\(\);\n', '')
rx(r'/\* leaving the billboard: the film eases back and the copy lets go \*/\nif \(!reduceMotion\) \{.*?\n\}\nfillHero', 'fillHero')
rx(r'/\* one title size for every feature:.*?\n\}\nfunction selectF', 'function selectF')

# the composer: the send control wakes (red) once there is something to search; empty submits just focus
rep('/* ============ closer: photos crossfade every 5s while it\'s on screen ============ */', '''/* composers: every one is the site search; the send control is red only while it can send */
$$(".cmp").forEach(f => {
  const q = f.querySelector("input");
  const sync = () => f.classList.toggle("has", q.value.trim().length > 0);
  q.addEventListener("input", sync); sync();
  f.addEventListener("submit", e => { if (!q.value.trim()) { e.preventDefault(); q.focus(); } });
});

/* ============ closer: photos crossfade every 5s while it's on screen ============ */''')

# every autoplay gets a visible pause/play: the news rows and the closer slideshow
PP_HTML = PAUSE + PLAY
s = s.replace('<div class="ad-card"><div class="bg"', '<div class="ad-card"><button class="pp ad-pp" id="adPP" type="button" aria-label="Pause slideshow">' + PP_HTML + '</button><div class="bg"', 1)
rep("""  let k = 0, vis = false, started = false;""", """  let k = 0, vis = false, started = false, adPaused = reduceMotion;
  const adPP = $("#adPP");
  const adSync = () => { adPP.classList.toggle("paused", adPaused); adPP.setAttribute("aria-label", adPaused ? "Play slideshow" : "Pause slideshow"); };
  adPP.addEventListener("click", () => { adPaused = !adPaused; adSync(); });
  adSync();""")
rep("    if (vis && !document.hidden) {\n      shots[k]", "    if (vis && !adPaused && !document.hidden) {\n      shots[k]")
rep("ready(shots[0]); prime(shots[1]); if (!reduceMotion) setTimeout(step, 5000); }", "ready(shots[0]); prime(shots[1]); setTimeout(step, 5000); }")
rep("""  let elapsedS = 0, lastS = 0, visS = false, hoverS = false, holdS = 0;""", """  let elapsedS = 0, lastS = 0, visS = false, hoverS = false, holdS = 0, pausedS = reduceMotion;
  const head = sec.querySelector(".wrap"), lbl = tp.label;
  head.insertAdjacentHTML("beforeend", `<button class="pp row-pp" type="button">PP_HTML</button>`);
  const rpp = head.querySelector(".row-pp");
  const rSync = () => { rpp.classList.toggle("paused", pausedS); rpp.setAttribute("aria-label", (pausedS ? "Play " : "Pause ") + lbl + " stories"); };
  rpp.addEventListener("click", () => { pausedS = !pausedS; rSync(); });
  rSync();""".replace("PP_HTML", PP_HTML))
rep("""  if (!reduceMotion) {
    const tickS = now => {
      const dt = lastS ? Math.min(100, now - lastS) : 0; lastS = now;
      if (visS && !hoverS && !document.hidden && now > holdS) {""", """  {
    const tickS = now => {
      const dt = lastS ? Math.min(100, now - lastS) : 0; lastS = now;
      if (!pausedS && visS && !hoverS && !document.hidden && now > holdS) {""")

# the co-op story card's image is unused in this treatment: no src-less <img> left in the page
rep('      <img id="gtc-img" alt="">\n', '')
rep('  $("#gtc-img").src = st.img;\n  $("#gtc-img").alt = st.t;\n', '')
# the closer's queued photos carry a transparent placeholder until they are decoded in
rx(r'<img (class="on" )?data-src=', lambda m: '<img ' + (m.group(1) or '') + 'src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEAAAAALAAAAAABAAEAAAIBRAA7" data-src=', None)
rep('const ready = img => { if (!img.src) img.src = img.dataset.src;', 'const ready = img => { if (img.src !== img.dataset.src) img.src = img.dataset.src;')

# rows: the framed-photo layout (b3) is this concept's default
rep('const RV = (new URLSearchParams(location.search).get("rows") || "b").toLowerCase();',
    'const RV = (new URLSearchParams(location.search).get("rows") || "b3").toLowerCase();')

# review round 1, item 2: stream only on first load and on a chip choice;
# autoplay swaps the copy with a plain fade and the CTA and sources stay in place
rep('''function fillHero(f) {
  let n = streamTo($("#hxTitle"), f.h, 0);
  n = streamTo($("#hxSyn"), f.syn, n + 5);''', '''function fillHero(f, stream) {
  let n = 0;
  if (stream) { n = streamTo($("#hxTitle"), f.h, 0); n = streamTo($("#hxSyn"), f.syn, n + 5); }
  else { $("#hxTitle").textContent = f.h; $("#hxSyn").textContent = f.syn; }''')
rep('''  [cta, $("#hxEps")].forEach(el => { el.style.setProperty("--i", n + 3); el.classList.remove("tail"); void el.offsetWidth; el.classList.add("tail"); });''',
    '''  [cta, $("#hxEps")].forEach(el => { el.classList.remove("tail"); if (stream) { el.style.setProperty("--i", n + 3); void el.offsetWidth; el.classList.add("tail"); } });''')
rep("function selectF(i) {", "function selectF(i, stream) {")
rep('setTimeout(() => { fillHero(FEATS[i]); hxIn.classList.remove("swap"); }, reduceMotion ? 0 : 200);',
    'setTimeout(() => { fillHero(FEATS[i], stream); hxIn.classList.remove("swap"); }, reduceMotion ? 0 : 200);')
rep('lnBtns.forEach(b => b.addEventListener("click", () => selectF(+b.dataset.i)));',
    'lnBtns.forEach(b => b.addEventListener("click", () => selectF(+b.dataset.i, true)));')
rep("\nfillHero(FEATS[0]);\n", "\nfillHero(FEATS[0], true);\n")

# item 3: the composer persists; once the hero's scrolls away (wide screens) the bar's icon becomes a compact composer
rep('</svg></a>\n    <nav class="mnav" aria-label="Primary">',
    '</svg></a>\n    ' + composer("cmp-nav", ' tabindex="-1"', "navQ").replace('class="cmp cmp-nav"', 'class="cmp cmp-nav" aria-hidden="true"')
    .replace('class="cmp-send"', 'class="cmp-send" tabindex="-1"')
    + '\n    <nav class="mnav" aria-label="Primary">')
JS_R1 = '''/* chips: the row fades at its end only when it actually overflows */
{
  const row = $(".hx-lineup");
  const ovf = () => row.classList.toggle("ovf", row.scrollWidth > row.clientWidth + 1);
  addEventListener("resize", ovf); document.fonts.ready.then(ovf); ovf();
}
/* the bar's composer fades in beside the N once the hero's composer has left the screen (wide screens only);
   it sits in space the peeled lockup has already freed, so nothing in the bar moves */
{
  const heroCmp = $(".cmp-hero"), navCmp = $(".cmp-nav"), links = $(".mnav"), wide = matchMedia("(min-width:1280px)");
  let away = false;
  const setOn = () => {
    const on = away && wide.matches;
    if (nav.classList.contains("cmp-on") === on) return;
    nav.classList.toggle("cmp-on", on);
    navCmp.setAttribute("aria-hidden", on ? "false" : "true");
    navCmp.querySelectorAll("input,button").forEach(el => el.tabIndex = on ? 0 : -1);
    if (!on && navCmp.contains(document.activeElement)) document.activeElement.blur();
  };
  new IntersectionObserver(es => { away = !es[0].isIntersecting && es[0].boundingClientRect.top < 0; setOn(); }).observe(heroCmp);
  wide.addEventListener("change", setOn);
}
'''
JS_R1 += """/* once the button and sources have arrived they stay arrived: a later re-layout never replays their fade */
[$("#hxCta"), $("#hxEps")].forEach(el => el.addEventListener("animationend", e => { if (e.target === el) el.classList.remove("tail"); }));
"""
rep("/* composers: every one is the site search;", JS_R1 + "/* composers: every one is the site search;")

# item 4: sections answer like the hero; their onward links are source pills
rep('`<a class="storylink sp-btn" href="#">Read story</a>', '`<a class="src-pill sp-btn" href="#">Read story' + ARW + '</a>')
rep('<a class="storylink rc-more"', '<a class="src-pill rc-more"')
rep('href="https://news.northeastern.edu/category/research/">More research on NGN</a>',
    'href="https://news.northeastern.edu/category/research/">More research on NGN' + ARW + '</a>')

# item 8: the research figures read as a plain answer, figure then words, exactly as written
rx(r'<div class="rc-grid" id="counters">.*?</div>\n      </div>\n', '''<dl class="rc-list" id="counters">
        <div class="rc"><dt class="n">$296M</dt><dd class="l">external research awards last year</dd></div>
        <div class="rc"><dt class="n">50+</dt><dd class="l">federally funded centers and institutes</dd></div>
        <div class="rc"><dt class="n">510</dt><dd class="l">patents</dd></div>
      </dl>
''')

# ---------- styles ----------
css =(HERE / "conv.css").read_text()
rep('</style>\n</head>', css + '\n</style>\n</head>') if '</style>\n</head>' in s else rep('</style>\n\n<body>', css + '\n</style>\n\n<body>')

(REPO / "concept-16/index.html").write_text(s)
print("ok", len(s))
