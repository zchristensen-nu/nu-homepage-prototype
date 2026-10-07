#!/usr/bin/env python3
"""Concept 18 (Lab notebook): transforms the concept-12 byte copy into the lab-notebook build.
Re-runnable: always starts from orig.html (the untouched copy)."""
import re, pathlib
S = pathlib.Path(__file__).parent
REPO = pathlib.Path("/Users/z.christensen/Projects/nu-homepage-prototype")
src = (S / "orig.html").read_text()
css = (S / "lab.css").read_text()
js = (S / "lab.js").read_text()

def rep(old, new, count=1):
    global src
    n = src.count(old)
    assert n == count, f"expected {count} of {old[:90]!r}, found {n}"
    src = src.replace(old, new)

def rre(pat, new, count=1, flags=re.S):
    global src
    src, n = re.subn(pat, new, src, flags=flags)
    assert n == count, f"expected {count} of /{pat[:80]}/, found {n}"

# one authored arrow family (single stroke, 1.6) -----------------------------------------------
AR = '<svg class="ar" width="16" height="16" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M2.5 8h10.5M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARL = AR.replace('class="ar"', 'class="ar ar-l"')
XX = '<svg class="ar" width="18" height="18" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M3.5 3.5l9 9M12.5 3.5l-9 9" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'
CHD = '<svg class="ar ar-d" width="16" height="16" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M8 2.5v10.5M4 9l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
TRACE = '<svg class="tr-l" viewBox="0 0 100 2" preserveAspectRatio="none" aria-hidden="true" focusable="false"><line x1="0" y1="1" x2="100" y2="1" vector-effect="non-scaling-stroke"/></svg><s class="tr-pen"></s>'
PAUSE = '<svg class="ic-pause" width="16" height="16" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M5.5 3.5v9M10.5 3.5v9" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg><svg class="ic-play" width="16" height="16" viewBox="0 0 16 16" aria-hidden="true" focusable="false"><path d="M5 3.2l7.5 4.8L5 12.8z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>'

rep('<meta name="concept18-rev" content="1">', '<meta name="concept18-rev" content="2">\n<meta name="description" content="Northeastern University: research, co-op and one global university system.">')
rep('</style>\n\n<body>', css + '\n</style>\n\n<body>')

# glyph icons -> authored SVG ---------------------------------------------------------------
rep('<span class="fl">Read on NGN &#8594;</span>', '<span class="fl">Read on NGN ' + AR + '</span>', 4)
rep('aria-label="Close search">&times;</button>', 'aria-label="Close search">' + XX + '</button>')
rep('aria-label="Close menu">&times;</button>', 'aria-label="Close menu">' + XX + '</button>')
rep('<span class="tkv-c" aria-hidden="true">+</span>', '<span class="tkv-c" aria-hidden="true">' + CHD + '</span>', 7)
rep('AI<span aria-hidden="true">&#8594;</span></a>', 'AI' + AR + '</a>')
rep('aria-label="Previous story">&#8592;</button>', 'aria-label="Previous story">' + ARL + '</button>')
rep('aria-label="Next story">&#8594;</button>', 'aria-label="Next story">' + AR + '</button>')
rep('Read the story<span aria-hidden="true"> →</span>', 'Read the story ' + AR, 3)
rep('aria-label="Previous path">←</button>', 'aria-label="Previous path">' + ARL + '</button>', 2)
rep('aria-label="Next path">→</button>', 'aria-label="Next path">' + AR + '</button>', 2)
# dead hidden image in the unused co-op story card (no source; never shown in this treatment)
rep('      <img id="gtc-img" alt="">\n', '')
rep('  $("#gtc-img").src = st.img;\n  $("#gtc-img").alt = st.t;', '  const gi = $("#gtc-img"); if (gi) { gi.src = st.img; gi.alt = st.t; }')

# hero: a captioned figure beside the notebook entry; the lineup becomes instrument channels -----
m = re.search(r'<div class="hx-media" id="hxMedia">.*?</div></div>\n', src, re.S)
media = m.group(0)
src = src.replace(media, '')
rep('  <div class="hx-shade"></div>\n  <h1 class="vh">Northeastern University</h1>\n  <div class="hx-in" id="hxIn">',
    '  <h1 class="vh">Northeastern University</h1>\n  <div class="hx-grid">\n  <div class="hx-in" id="hxIn">')
rep('    <aside class="hx-eps" id="hxEps" aria-label="Stories from this feature"></aside>\n  </div>\n',
    '    <aside class="hx-eps" id="hxEps" aria-label="Stories from this feature"></aside>\n  </div>\n'
    '  <figure class="fig hx-fig" data-fig>\n    <div class="plate hx-plate"><span class="rule rule-x hx-ruler" id="hxRuler" aria-hidden="true"></span><span class="rule rule-y" aria-hidden="true"></span>\n    '
    + media.strip() + '\n    </div>\n'
    '    <figcaption class="cap hx-cap"><span class="fig-n">Fig. 1</span><span class="cap-t" id="hxCapT">Co‑op</span>'
    '<span class="ro hx-tc" id="hxTc" aria-hidden="true">0:00</span>'
    '<button class="hx-pause" id="hxPause" type="button" aria-label="Pause the feature films">' + PAUSE + '</button></figcaption>\n'
    '  </figure>\n  </div>\n')
# channels: numeral, name, trace (thumbnails dropped: the film is the figure)
src, n = re.subn(r'<button class="ln" data-i="(\d)" aria-pressed="(\w+)"><img [^>]*><span class="ln-t">([^<]*)</span><i class="ln-pb"></i></button>',
                 lambda mm: f'<button class="ln" data-i="{mm.group(1)}" aria-pressed="{mm.group(2)}"><i class="trace ln-pb" aria-hidden="true">{TRACE}</i>'
                            f'<span class="ln-n" aria-hidden="true">{int(mm.group(1))+1}</span><span class="ln-t">{mm.group(3)}</span><span class="ro ln-r" aria-hidden="true"></span></button>', src)
assert n == 5, n

# rows: the framed-photo layout is the notebook default ---------------------------------------
rep('const RV = (new URLSearchParams(location.search).get("rows") || "b").toLowerCase();',
    'const RV = (new URLSearchParams(location.search).get("rows") || "b3").toLowerCase();')
rep('<a class="storylink sp-btn" href="#">Read story</a></div><div class="sp-fig" aria-hidden="true"><img alt=""><img alt=""></div></div>`);',
    '<a class="storylink sp-btn" href="#">Read story</a></div>' +
    '<figure class="fig sp-figw" data-fig><div class="plate"><span class="rule rule-x" aria-hidden="true"></span><span class="rule rule-y" aria-hidden="true"></span>' +
    '<div class="sp-fig" aria-hidden="true"><img alt=""><img alt=""></div></div>' +
    '<figcaption class="cap"><span class="fig-n"></span><span class="cap-t sp-c"></span><span class="ro sp-d"></span><span class="sp-cr"></span></figcaption></figure></div>`);')
rep('      copy.querySelector(".sp-btn").href = it.u;',
    '      copy.querySelector(".sp-btn").href = it.u;\n      sec.querySelector(".sp-d").textContent = it.d ? fmtDate(it.d) : "";\n      sec.querySelector(".sp-c").textContent = it.cap || "";\n      sec.querySelector(".sp-cr").textContent = it.cr || "";')
rep('''cards.forEach(c => c.insertAdjacentHTML("beforeend", '<i class="cc-pb" aria-hidden="true"></i>'));''',
    '''cards.forEach(c => c.insertAdjacentHTML("beforeend", '<i class="trace cc-pb" aria-hidden="true">''' + TRACE + '''</i>'));''')
rep('  if (["b", "b2", "b3"].includes(RV)) topics.forEach(spotlight);',
    '  if (["b", "b2", "b3"].includes(RV)) topics.forEach(spotlight);\n  if (window.numberFigs) numberFigs();')

rep('x: text((p.excerpt && p.excerpt.rendered) || ""), d: p.date };',
    'x: text((p.excerpt && p.excerpt.rendered) || ""), d: p.date,\n               ...splitCap(text((m.caption && m.caption.rendered) || ""), String(((m.media_details || {}).image_meta || {}).credit || "").trim()) };')
rep('const fmtDate = d =>', (S / "splitcap.js").read_text() + 'const fmtDate = d =>')
# globe journeys: each stop's progress is the same instrument trace ----------------------------
rep('`<li tabindex="0" data-k="${k}"><i aria-hidden="true"><b></b></i>`', '`<li tabindex="0" data-k="${k}"><i class="trace" aria-hidden="true">' + TRACE + '</i>`')
rep('      const b = li.querySelector("b");', '      const b = li.querySelector(".trace");')
rep('      const b = list.children[j] && list.children[j].querySelector("b");', '      const b = list.children[j] && list.children[j].querySelector(".trace");')

# research: panel letters, a figure caption, static figures -----------------------------------
rep('      <div class="xrow rv" id="xrow">', '      <figure class="fig xfig" data-fig>\n      <div class="plate"><span class="rule rule-x" aria-hidden="true"></span><span class="rule rule-y" aria-hidden="true"></span>\n      <div class="xrow" id="xrow">')
for i, L in enumerate("abcde"):
    pass
src, n = re.subn(r'(<article class="xcard[^"]*" tabindex="0">)', lambda mm, c=iter("abcde"): mm.group(1) + f'\n          <span class="xl" aria-hidden="true">{next(c)}</span>', src)
assert n == 5, n
rep('''          <span class="xtag">Soft robotics</span>
        </article>
      </div>
''', '''          <span class="xtag">Soft robotics</span>
        </article>
      </div>
      </div>
      <figcaption class="cap xcap"><span class="fig-n"></span><span class="xcap-l" id="xcapL"></span></figcaption>
      </figure>
''')
rep('<div class="n">$<span data-count="296">0</span>M</div>', '<div class="n">$296M</div>')
rep('<div class="n"><span data-count="50">0</span>+</div>', '<div class="n">50+</div>')
rep('<div class="n"><span data-count="510">0</span></div>', '<div class="n">510</div>')
rep('<div class="sechead rv">', '<div class="sechead">')
rep('<a class="storylink rv" style="margin-top:34px" href', '<a class="storylink rs-more" href')

# closer: the photo is a framed plate beside the call; no parallax ----------------------------
rep('  <div class="bg" data-plx="34">', '  <figure class="ad-col fig" data-fig><div class="plate ad-plate"><span class="rule rule-x" aria-hidden="true"></span><span class="rule rule-y" aria-hidden="true"></span><div class="bg">')
rep('alt="" decoding="async"></div>\n  <div class="inner">', 'alt="" decoding="async"></div></div>'
    '<figcaption class="cap ad-cap"><span class="fig-n"></span><span class="ro" id="adN">1 / 8</span>'
    '<button class="hx-pause" id="adPause" type="button" aria-label="Pause the photo slideshow">' + PAUSE + '</button></figcaption></figure>\n  <div class="inner">')
# closer slideshow: pausable, with a frame readout
rep('    if (vis && !document.hidden) {\n      shots[k].classList.remove("on"); k = (k + 1) % shots.length;',
    '    if (vis && !document.hidden && !adPaused) {\n      const old = shots[k]; old.classList.add("was"); setTimeout(() => old.classList.remove("was"), 900);\n      admit.querySelector(".bg").classList.add("go");\n      shots[k].classList.remove("on"); k = (k + 1) % shots.length; adN.textContent = (k + 1) + " / " + shots.length;')
rep('  let k = 0, vis = false, started = false;',
    '''  let k = 0, vis = false, started = false, adPaused = reduceMotion;
  const adN = $("#adN"), adBtn = $("#adPause");
  const adSet = p => { adPaused = p; adBtn.classList.toggle("is-paused", p); adBtn.setAttribute("aria-label", p ? "Play the photo slideshow" : "Pause the photo slideshow"); };
  adBtn.addEventListener("click", () => adSet(!adPaused)); adSet(adPaused);''')
rep('ready(shots[0]); prime(shots[1]); if (!reduceMotion) setTimeout(step, 5000); }', 'ready(shots[0]); prime(shots[1]); setTimeout(step, 5000); }')
# news rows: a visible pause control per row, beside its heading
rep('''  strip.addEventListener("touchstart", hold, { passive: true });
  if (!reduceMotion) {
    const tickS = now => {
      const dt = lastS ? Math.min(100, now - lastS) : 0; lastS = now;
      if (visS && !hoverS && !document.hidden && now > holdS) {''', '''  strip.addEventListener("touchstart", hold, { passive: true });
  let pausedS = reduceMotion;
  sec.querySelector(".wrap").insertAdjacentHTML("beforeend", `<button class="hx-pause row-pause" type="button">PAUSE_SVG</button>`);
  const rbtn = sec.querySelector(".row-pause");
  const setS = p => { pausedS = p; rbtn.classList.toggle("is-paused", p); rbtn.setAttribute("aria-label", (p ? "Play " : "Pause ") + tp.label + " stories"); };
  rbtn.addEventListener("click", () => setS(!pausedS)); setS(pausedS);
  {
    const tickS = now => {
      const dt = lastS ? Math.min(100, now - lastS) : 0; lastS = now;
      if (!pausedS && visS && !hoverS && !document.hidden && now > holdS) {'''.replace("PAUSE_SVG", PAUSE))


# hero JS: pausable films + channels, timecode readout, no scroll parallax --------------------
rep('let cur = 0, elapsed = 0, hxVisible = true, hoverShows = false;',
    'let cur = 0, elapsed = 0, hxVisible = true, hoverShows = false, paused = reduceMotion;')
rep('const playI = i => { const v = vidOf(i); if (v && !reduceMotion) v.play().catch(() => {}); };',
    'const playI = i => { const v = vidOf(i); if (v && !paused) v.play().catch(() => {}); };')
rep('  $("#hxTitle").textContent = f.h;', '  $("#hxTitle").textContent = f.h;\n  $("#hxCapT").textContent = f.t;')
rep('  lnBtns.forEach((b, k) => { b.setAttribute("aria-pressed", k === i ? "true" : "false"); b.style.setProperty("--pb", 0); });',
    '  lnBtns.forEach((b, k) => { b.setAttribute("aria-pressed", k === i ? "true" : "false"); b.classList.toggle("done", k < i); b.style.setProperty("--pb", 0); });')
rep('''if (!reduceMotion) {
  let lastT = 0;
  const tick = now => {
    const dt = lastT ? Math.min(100, now - lastT) : 0; lastT = now;
    if (hxVisible && !hoverShows && !document.hidden && scrollY < innerHeight * .3) {''',
'''{
  let lastT = 0, lastS = -1;
  const tc = $("#hxTc"), pbtn = $("#hxPause"), ruler = $("#hxRuler"), lnR = { s: -1, c: -1 };
  /* the plate's top ruler indexes the current film's real running time: a tick per second, labelled majors */
  const drawRuler = D => {
    ruler.d = D;
    if (!D) { ruler.innerHTML = '<i class="tk-pen"></i>'; ruler.pen = ruler.firstChild; return; }
    const step = [5, 10, 15, 30, 60, 120].find(x => D / x <= 8) || 300, minor = D > 150 ? 5 : 1;
    let h = "";
    for (let x = 0; x <= D + .001; x += minor) {
      const M = Math.round(x) % step === 0, L = (x / D * 100).toFixed(3);
      h += `<span class="tk${M ? " M" : ""}" style="left:${L}%">${M ? `<b>${Math.floor(x / 60)}:${String(Math.round(x) % 60).padStart(2, "0")}</b>` : ""}</span>`;
    }
    ruler.innerHTML = h + '<i class="tk-pen"></i>'; ruler.pen = ruler.lastChild;
  };
  drawRuler(0);
  const setPaused = p => {
    paused = p;
    pbtn.setAttribute("aria-label", p ? "Play the feature films" : "Pause the feature films");
    pbtn.classList.toggle("is-paused", p);
    hx.classList.toggle("paused", p);
    const v = vidOf(cur);
    if (v) { if (p) v.pause(); else if (hxVisible) playI(cur); }
  };
  pbtn.addEventListener("click", () => setPaused(!paused));
  setPaused(paused);
  const tick = now => {
    const dt = lastT ? Math.min(100, now - lastT) : 0; lastT = now;
    const v = vidOf(cur), s = v ? Math.floor(v.currentTime || 0) : 0;
    const mmss = x => Math.floor(x / 60) + ":" + String(Math.floor(x) % 60).padStart(2, "0");
    const D = v && isFinite(v.duration) && v.duration > 0 ? v.duration : 0;
    if (D !== ruler.d) drawRuler(D);
    if (s !== lastS || D !== tc.d) { lastS = s; tc.d = D; tc.textContent = mmss(s) + (D ? " / " + mmss(D) : ""); }
    if (D) ruler.pen.style.left = (Math.min(1, (v.currentTime || 0) / D) * 100).toFixed(3) + "%";
    const es = Math.min(12, Math.floor(elapsed / 1000));
    if (es !== lnR.s || cur !== lnR.c) { lnR.s = es; lnR.c = cur; lnBtns.forEach((bb, k) => bb.querySelector(".ln-r").textContent = k === cur ? es + " s" : ""); }
    if (!paused && hxVisible && !hoverShows && !document.hidden && scrollY < innerHeight * .3) {''')
rep('''/* leaving the billboard: the film eases back and the copy lets go */
if (!reduceMotion) {
  const media = $("#hxMedia");
  addEventListener("scroll", () => requestAnimationFrame(() => {
    const p = clamp01(scrollY / innerHeight);
    media.style.transform = `translateY(${(p * 90).toFixed(1)}px) scale(${(1 + p * .06).toFixed(4)})`;
    hxIn.style.opacity = (1 - p * 1.5).toFixed(3);
  }), { passive: true });
}
''', '')

rep('t.offsetHeight <= fs * .98 * 2 + 2;', 't.offsetHeight <= fs * .98 * 3 + 2;  /* up to three lines in the notebook column */')
# the light sheet: retire the dark build's pale text colours at the source
rep('.hx-syn{margin:18px 0 0;font-size:clamp(16px,1.25vw,19px);line-height:1.5;color:#E5E5E5;', '.hx-syn{margin:18px 0 0;font-size:clamp(16px,1.25vw,19px);line-height:1.5;color:#404040;')
rep('.crow h3{margin:0;font-size:clamp(17px,1.4vw,21px);font-weight:600;color:#E5E5E5}', '.crow h3{margin:0;font-size:clamp(17px,1.4vw,21px);font-weight:600;color:#111111}')
rep('.admit p{margin:18px auto 0;font-size:17px;color:#E5E5E5;', '.admit p{margin:18px auto 0;font-size:17px;color:#404040;')
rep('.tkv-sub .tkv-sec a{display:block;padding:7px 0;font-size:16px;color:#E5E5E5}', '.tkv-sub .tkv-sec a{display:block;padding:7px 0;font-size:16px;color:#404040}')
# boot: shared lab helpers (figure numbering, research caption)
rep('/* ============ boot ============ */', js + '\n/* ============ boot ============ */')

# globe engine: an ink plate on graph paper; red only on the active stop and the leg in flight ---
rep('''  atm.addColorStop(0, "rgba(226,230,242,0)");
  atm.addColorStop(0.4, "rgba(226,230,242,.04)");
  atm.addColorStop(1, "rgba(226,230,242,0)");''', '''  atm.addColorStop(0, "rgba(17,17,17,0)");
  atm.addColorStop(1, "rgba(17,17,17,0)");''')
rep('g.addColorStop(0, "#1A1B22"); g.addColorStop(1, "#101014");', 'g.addColorStop(0, "#FFFFFF"); g.addColorStop(1, "#FAFAFA");')
rep('ctx.strokeStyle = "rgba(255,255,255,.045)"; ctx.lineWidth = 1;', 'ctx.strokeStyle = "rgba(17,17,17,.075)"; ctx.lineWidth = 1;')
rep('''  ctx.fillStyle = "#26262D";
  ctx.strokeStyle = "rgba(255,255,255,.09)";''', '''  ctx.fillStyle = "#F5F5F5";
  ctx.strokeStyle = "rgba(64,64,64,.5)"; ctx.lineWidth = .7;''')
rep('''  term.addColorStop(0, "rgba(0,0,6,0)");
  term.addColorStop(0.55, "rgba(0,0,6,0)");
  term.addColorStop(1, "rgba(0,0,6,.5)");''', '''  term.addColorStop(0, "rgba(17,17,17,0)");
  term.addColorStop(0.6, "rgba(17,17,17,0)");
  term.addColorStop(1, "rgba(17,17,17,.05)");''')
rep('ctx.strokeStyle = "rgba(255,255,255,.14)"; ctx.lineWidth = 1.2; ctx.stroke();', 'ctx.strokeStyle = "rgba(17,17,17,.55)"; ctx.lineWidth = 1; ctx.stroke();')
rep('ctx.strokeStyle = `rgba(255,255,255,${.30 * a})`;', 'ctx.strokeStyle = `rgba(17,17,17,${.22 * a})`;')
rep('ctx.fillStyle = `rgba(210,210,222,${.6 * a})`;', 'ctx.fillStyle = `rgba(115,115,115,${.5 * a})`;')
rep('ctx.fillStyle = `rgba(255,255,255,${cur.nuin})`; ctx.fill();', 'ctx.fillStyle = `rgba(17,17,17,${cur.nuin})`; ctx.fill();')
rep('ctx.strokeStyle = `rgba(255,255,255,${.4 * cur.nuin})`; ctx.lineWidth = 1; ctx.stroke();', 'ctx.strokeStyle = `rgba(17,17,17,${.3 * cur.nuin})`; ctx.lineWidth = 1; ctx.stroke();')
rep('''      ctx.beginPath(); ctx.arc(x, y, 8.5, 0, 7);
      ctx.fillStyle = `rgba(200,16,46,${.28 * cur.campus})`; ctx.fill();
      ctx.beginPath(); ctx.arc(x, y, 4.6, 0, 7);
      ctx.fillStyle = `rgba(200,16,46,${cur.campus})`; ctx.fill();
      ctx.lineWidth = 1.4;
      ctx.strokeStyle = `rgba(255,255,255,${.85 * cur.campus})`; ctx.stroke();''',
'''      ctx.beginPath(); ctx.arc(x, y, 4, 0, 7);
      ctx.fillStyle = `rgba(64,64,64,${cur.campus})`; ctx.fill();
      ctx.lineWidth = 1.4;
      ctx.strokeStyle = `rgba(250,250,250,${.9 * cur.campus})`; ctx.stroke();''')
# small labels: paper tag, ink text
rep('  ctx.fillStyle = `rgba(11,11,14,${.55 * a})`;\n  ctx.fillRect(bx, by, w + 12, 18);\n  ctx.fillStyle = `rgba(255,255,255,${.95 * a})`;',
    '  ctx.fillStyle = `rgba(250,250,250,${.94 * a})`;\n  ctx.fillRect(bx, by, w + 12, 18);\n  ctx.strokeStyle = `rgba(17,17,17,${.18 * a})`; ctx.lineWidth = 1; ctx.strokeRect(bx + .5, by + .5, w + 11, 17);\n  ctx.fillStyle = `rgba(17,17,17,${a})`;')
# the stop label: ink on a paper tag with a hairline leader, no glow
rep('''    ctx.save(); ctx.shadowColor = `rgba(0,0,0,${.85 * a})`; ctx.shadowBlur = 10;
    ctx.fillStyle = `rgba(255,255,255,${a})`; ctx.fillText(text, bx, y + .5); ctx.restore();''',
'''    ctx.save();
    ctx.fillStyle = `rgba(250,250,250,${.9 * a})`; ctx.fillRect(bx - 6, by - 2, w + 12, h + 4);
    ctx.strokeStyle = `rgba(17,17,17,${.45 * a})`; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(x + 6, y + .5); ctx.lineTo(bx - 6, y + .5); ctx.stroke();
    ctx.fillStyle = `rgba(17,17,17,${a})`; ctx.fillText(text, bx, y + .5); ctx.restore();''')
# arcs: earlier legs in grey, the leg in flight in red; no glow stroke
rep('''    for (const arc of window.PATH_ARCS) {''', '''    const lastArc = window.PATH_ARCS[window.PATH_ARCS.length - 1];
    for (const arc of window.PATH_ARCS) {
      const live = arc === lastArc;''')
rep('''      ctx.strokeStyle = `rgba(238,85,102,${.16 * fadeA})`; ctx.lineWidth = 5; ctx.stroke();
      ctx.strokeStyle = `rgba(255,190,200,${.75 * fadeA})`; ctx.lineWidth = 1.3; ctx.stroke();
      if (head && f < 1) { ctx.beginPath(); ctx.arc(head[0], head[1], 3, 0, 7); ctx.fillStyle = `rgba(255,255,255,${.95 * fadeA})`; ctx.fill(); }''',
'''      ctx.strokeStyle = live ? `rgba(200,16,46,${fadeA})` : `rgba(115,115,115,${.8 * fadeA})`; ctx.lineWidth = live ? 1.6 : 1; ctx.stroke();
      if (head && f < 1) { ctx.beginPath(); ctx.arc(head[0], head[1], 2.5, 0, 7); ctx.fillStyle = `rgba(200,16,46,${fadeA})`; ctx.fill(); }''')
# stop pins: a red crosshair on the active stop; reached stops are ink points; no pulsing rings
rep('''      const p = ((now + i * 400) % 2400) / 2400;
      ctx.beginPath(); ctx.arc(x, y, 7 + p * 16, 0, 7);
      ctx.strokeStyle = `rgba(238,85,102,${(1 - p) * .5 * cur.spins})`;
      ctx.lineWidth = 1.6; ctx.stroke();
      const boost = (typeof storySel !== "undefined" && i === storySel) ? 1.4 : 1;
      ctx.beginPath(); ctx.arc(x, y, 5 * boost, 0, 7);
      ctx.fillStyle = `rgba(238,85,102,${.95 * cur.spins})`; ctx.fill();
      ctx.lineWidth = 1.5;
      ctx.strokeStyle = `rgba(255,255,255,${.9 * cur.spins})`; ctx.stroke();''',
'''      const on = typeof storySel !== "undefined" && i === storySel, a = cur.spins;
      if (on) {
        ctx.strokeStyle = `rgba(200,16,46,${a})`; ctx.lineWidth = 1.2; ctx.beginPath();
        for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { ctx.moveTo(x + dx * 8, y + dy * 8); ctx.lineTo(x + dx * 15, y + dy * 15); }
        ctx.stroke();
        ctx.beginPath(); ctx.arc(x, y, 9, 0, 7); ctx.strokeStyle = `rgba(200,16,46,${.9 * a})`; ctx.lineWidth = 1; ctx.stroke();
      }
      ctx.beginPath(); ctx.arc(x, y, on ? 4 : 3.2, 0, 7);
      ctx.fillStyle = on ? `rgba(200,16,46,${a})` : `rgba(17,17,17,${a})`; ctx.fill();
      ctx.lineWidth = 1.5;
      ctx.strokeStyle = `rgba(250,250,250,${a})`; ctx.stroke();''')
rep('''      const p = (now % 2200) / 2200;
      ctx.beginPath(); ctx.arc(x, y, 6 + p * 22, 0, 7);
      ctx.strokeStyle = `rgba(238,85,102,${(1 - p) * .9})`; ctx.lineWidth = 2; ctx.stroke();
      ctx.beginPath(); ctx.arc(x, y, 5.5, 0, 7);
      ctx.fillStyle = "#EE5566"; ctx.fill();
      ctx.lineWidth = 1.6; ctx.strokeStyle = "#fff"; ctx.stroke();''',
'''      ctx.beginPath(); ctx.arc(x, y, 9, 0, 7);
      ctx.strokeStyle = "rgba(200,16,46,.9)"; ctx.lineWidth = 1; ctx.stroke();
      ctx.beginPath(); ctx.arc(x, y, 4, 0, 7);
      ctx.fillStyle = "#C8102E"; ctx.fill();
      ctx.lineWidth = 1.5; ctx.strokeStyle = "#FAFAFA"; ctx.stroke();''')

# unused treatments still carried the off-brand pink: bring them to brand red
src = src.replace("#EE5566", "#C8102E").replace("238,85,102", "200,16,46")
(REPO / "concept-18/index.html").write_text(src)
print("ok", len(src))
