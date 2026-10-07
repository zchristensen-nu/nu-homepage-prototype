#!/usr/bin/env python3
"""Concept 21 (Cinema Conversation): concept 14's page with concept 16's conversational hero, in the dark Cinema world.
Reads concept-14/index.html, writes concept-21/index.html."""
import re, pathlib, sys
REPO = pathlib.Path("/Users/z.christensen/Projects/nu-homepage-prototype")
s = (REPO / "concept-14/index.html").read_text()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if count is not None and n != count: sys.exit(f"expected {count} of {old[:90]!r}, found {n}")
    s = s.replace(old, new)

def ic(d, cls="ic"):
    return (f'<svg class="{cls}" width="16" height="16" viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
            f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>')
ARW_UP = ic("M8 13V4M4 7.5l4-4 4 4")
SEARCH = ('<svg class="ic-s" width="18" height="18" viewBox="0 0 20 20" fill="none" aria-hidden="true" focusable="false">'
          '<circle cx="9" cy="9" r="6.5" stroke="currentColor" stroke-width="1.5"/>'
          '<path d="M14 14l4.5 4.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>')
def composer(cls, label_id, extra=""):
    return (f'<form action="https://search.northeastern.edu" method="get" role="search" class="cmp {cls}"{extra}>'
            f'{SEARCH}<label class="vh" for="{label_id}">Search Northeastern</label>'
            f'<input type="search" name="query" id="{label_id}" placeholder="Search Northeastern" autocomplete="off" enterkeyhint="search">'
            f'<button type="submit" class="cmp-send" aria-label="Search">{ARW_UP}</button></form>')

s = re.sub(r'<meta name="concept14-rev" content="\d+">', '<meta name="concept21-rev" content="1">', s, count=1)

# ---------- hero: the response column over the film (response, sources, chips, composer) ----------
rep('  <div class="hx-in" id="hxIn">\n', '  <div class="hx-chat" id="hxChat">\n  <div class="hx-in" id="hxIn">\n')
m = re.search(r'(  <div class="hx-shows" id="hxShows">\n.*?\n  </div>\n)(</section>\n<main>)', s, re.S)
if not m: sys.exit("hx-shows block not found")
s = s[:m.end(1)] + '  ' + composer("cmp-hero", "cmpQ") + '\n  </div>\n' + s[m.start(2):]
rep('<aside class="hx-eps" id="hxEps" aria-label="Stories from this feature"></aside>',
    '<aside class="hx-eps" id="hxEps" aria-label="Sources for this answer"></aside>')
rep('aria-label="Choose a feature"', 'aria-label="Suggestions"')

# ---------- the bar's composer (wide screens), hidden until the hero composer has scrolled away ----------
rep('    <nav class="mnav" aria-label="Primary">',
    '    ' + composer("cmp-nav", "navQ", ' aria-hidden="true"').replace('<input ', '<input tabindex="-1" ').replace('class="cmp-send"', 'class="cmp-send" tabindex="-1"')
    + '\n    <nav class="mnav" aria-label="Primary">')

# ---------- JS: streaming response replaces the line-set title ----------
a = s.index('/* the title is set line by line:')
b = s.index('function selectF(i) {')
s = s[:a] + r'''/* the response streams onto the film word by word: once on load and again on a chip choice.
   Screen readers get the whole sentence from the hidden copy, never the fragments; autoplay swaps with a plain fade */
const STREAM_MS = 40;
const streamTo = (el, text, i0) => {
  const ws = text.split(/\s+/);
  el.innerHTML = `<span class="vh">${esc(text)}</span><span class="st" aria-hidden="true">` +
    ws.map((w, k) => `<span class="w" style="--i:${i0 + k}">${esc(w)}</span>`).join(" ") + `</span>`;
  return i0 + ws.length;
};
/* the headline keeps concept 14's title craft inside the stream: words are measured into their real lines,
   each line is a mask, and the words resolve up into it in reading order */
function setTitle(text, stream) {
  const t = $("#hxTitle"), ws = text.split(/\s+/);
  t.innerHTML = `<span class="vh">${esc(text)}</span><span class="tt" aria-hidden="true">${ws.map(w => `<span class="tw">${esc(w)}</span>`).join(" ")}</span>`;
  const lines = []; let top = null;
  t.querySelectorAll(".tw").forEach(w => { if (w.offsetTop !== top) { lines.push([]); top = w.offsetTop; } lines[lines.length - 1].push(w.textContent); });
  let i = 0;
  const cls = stream && !reduceMotion ? "w" : "w0";
  t.querySelector(".tt").innerHTML = lines.map(l => `<span class="tl">${l.map(w => `<span class="${cls}" style="--i:${i++}">${esc(w)}</span>`).join(" ")}</span>`).join("");
  return i;
}
function fillHero(f, stream) {
  let n = setTitle(f.h, stream);
  if (stream && !reduceMotion) n = streamTo($("#hxSyn"), f.syn, n + 3);
  else $("#hxSyn").textContent = f.syn;
  const cta = $("#hxCta");
  cta.hidden = !f.cta;
  if (f.cta) { cta.href = f.cta.href; $("#hxCtaL").textContent = f.cta.label; }
  $("#hxEps").innerHTML = f.eps.slice(0, 3).map(e =>
    `<a class="ep" href="${esc(e.u)}"><img src="${esc(e.img)}" alt="" loading="lazy"><span>${esc(e.t)}</span></a>`).join("");
  [cta, $("#hxEps")].forEach(el => { el.classList.remove("tail"); if (stream && !reduceMotion) { el.style.setProperty("--i", n + 2); void el.offsetWidth; el.classList.add("tail"); } });
}
/* one headline size for every feature (the largest at which each title holds two lines in the column), then the
   tallest answer block is reserved, so the headline's top edge never moves between features */
function fitHeroTitle() {
  const t = $("#hxTitle"), hin = $("#hxIn");
  t.style.fontSize = "";
  let fs = parseFloat(getComputedStyle(t).fontSize);
  const over = () => t.scrollWidth > t.clientWidth + 1 || t.offsetHeight > fs * 1.02 * 2 + 4;
  for (const f of FEATS) { t.textContent = f.h; while (fs > 32 && over()) { fs -= 2; t.style.fontSize = fs + "px"; } }
  hin.style.minHeight = "0";
  let hmax = 0;
  for (const f of FEATS) { fillHero(f, false); hmax = Math.max(hmax, hin.offsetHeight); }
  hin.style.minHeight = hmax + "px";
  fillHero(FEATS[cur], false);
}
''' + s[b:]
rep('function selectF(i) {', 'function selectF(i, stream) {')
rep('hxIn.classList.add("swap");\n  /* the dissolve waits', 'hxIn.classList.toggle("fade", !stream); hxIn.classList.add("swap");\n  /* the dissolve waits')
rep('setTimeout(() => { if (cur === i) { fillHero(FEATS[i], true); hxIn.classList.remove("swap"); } }, reduceMotion ? 0 : 380);',
    'setTimeout(() => { if (cur === i) { fillHero(FEATS[i], stream); hxIn.classList.remove("swap"); } }, reduceMotion ? 0 : (stream ? 240 : 420));')
rep('lnBtns.forEach(b => b.addEventListener("click", () => selectF(+b.dataset.i)));',
    'lnBtns.forEach(b => b.addEventListener("click", () => selectF(+b.dataset.i, true)));')
rep('const open = () => { if (done) return; done = true; layout(); setTitle(FEATS[cur].h, true); root.classList.remove("intro"); };',
    'const open = () => { if (done) return; done = true; layout(); fillHero(FEATS[cur], true); root.classList.remove("intro"); };')
rep('    hxIn.style.opacity = (1 - p * 1.5).toFixed(3);', '    $("#hxChat").style.opacity = (1 - p * 1.2).toFixed(3);')
# without the intro (reduced motion), the first answer is simply present
rep('fillHero(FEATS[0], false);\nplayI(0);', 'fillHero(FEATS[0], false);\nplayI(0);')

# ---------- composer behaviour + the bar's composer ----------
rep('/* ============ closer: photos crossfade every 5s while it\'s on screen ============ */', r'''/* composers: each is the real site search; the send control turns red only once there is something to send */
$$(".cmp").forEach(f => {
  const q = f.querySelector("input");
  const sync = () => f.classList.toggle("has", q.value.trim().length > 0);
  q.addEventListener("input", sync); sync();
  f.addEventListener("submit", e => { if (!q.value.trim()) { e.preventDefault(); q.focus(); } });
});
/* chips: the row ends in a fade only when it actually overflows */
{
  const row = $(".hx-lineup");
  const ovf = () => row.classList.toggle("ovf", row.scrollWidth > row.clientWidth + 1);
  addEventListener("resize", ovf); document.fonts.ready.then(ovf); ovf();
}
/* once the button and sources have arrived they stay arrived */
[$("#hxCta"), $("#hxEps")].forEach(el => el.addEventListener("animationend", e => { if (e.target === el) el.classList.remove("tail"); }));
/* the bar's composer fades in beside the N once the hero's composer has left the screen (1280px and up);
   it sits in room the peeled lockup has already freed, so the links never move */
{
  const heroCmp = $(".cmp-hero"), navCmp = $(".cmp-nav"), wide = matchMedia("(min-width:1280px)");
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

/* ============ closer: photos crossfade every 5s while it's on screen ============ */''')

# ---------- styles ----------
css = (pathlib.Path(__file__).parent / "c21.css").read_text()
rep('  .f-giant{margin-top:var(--s6);padding-bottom:var(--s5)}\n', '  .f-giant{margin-top:var(--s6);padding-bottom:var(--s5)}\n' + css)

(REPO / "concept-21/index.html").write_text(s)
print("ok", len(s))
