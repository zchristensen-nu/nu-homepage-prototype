"""Concept 7 · Northeastern, Netflix-style. Billboard hero + paged rows with edge
paddles, page dashes, and a hover preview panel. Every tile leads to a landing
page or a story. Rows: continue browsing (local), pillar posters, live NGN,
ten ways in (numbered), co-op, research, campus life, live NGN categories."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stream_common import *

P = PBYKEY
def pill_item(p):
    return {"t": p["t"], "img": p["img"], "u": p["u"], "ex": p["ex"], "tags": p["tags"],
            "film": p.get("film"), "cities": p.get("cities")}

TEN = [
 ("Apply", ADMIT_PATHS[0]), ("Visit a campus", ADMIT_PATHS[1]), ("Financial aid", ADMIT_PATHS[2]),
 ("Explore academics", ADMIT_PATHS[4]), ("Graduate programs", ADMIT_PATHS[5]),
]
TEN = [dict(it, t=t) for t, it in TEN] + [
 {"t": "Co‑op", "img": P["coop"]["img"], "u": P["coop"]["u"], "ex": P["coop"]["ex"], "tag": "Experiential learning"},
 {"t": "Research", "img": P["research"]["img"], "u": P["research"]["u"], "ex": P["research"]["ex"], "tag": "Research"},
 {"t": "N.U.in", "img": None, "u": P["nuin"]["u"], "ex": P["nuin"]["ex"], "tag": "First year abroad", "cities": P["nuin"]["cities"]},
 {"t": "Student life", "img": P["life"]["img"], "u": P["life"]["u"], "ex": P["life"]["ex"], "tag": "Student life"},
 {"t": "Athletics", "img": P["athletics"]["img"], "u": P["athletics"]["u"], "ex": P["athletics"]["ex"], "tag": "NCAA Division I"},
]

def snap(slug, tagname=None):
    return [dict(x, tag=tagname or "") for x in SNAP[slug]]

research_rows = RESEARCH_STORIES + [x for x in snap("research", "Research") if x["u"] not in {r["u"] for r in RESEARCH_STORIES}][:7]

ROWS = [
 {"id": "rowContinue", "title": "Continue browsing", "kind": "land", "items": []},
 {"id": "rowOnly", "title": "Only at Northeastern", "kind": "poster", "items": [pill_item(p) for p in PILLARS]},
 {"id": "rowNew", "title": "New on Northeastern Global News", "kind": "land", "href": NGN + "/", "live": "latest",
  "items": snap("latest", "")},
 {"id": "rowTen", "title": "Ten ways into Northeastern", "kind": "top", "href": "https://admissions.northeastern.edu/", "items": TEN},
 {"id": "rowCoop", "title": "Co‑op stories", "kind": "land", "href": P["coop"]["u"], "items": COOP_STORIES},
 {"id": "rowResearch", "title": "Research", "kind": "land", "href": P["research"]["u"], "items": research_rows},
 {"id": "rowLife", "title": "Campus life", "kind": "land", "href": P["life"]["u"], "items": LIFE_STORIES},
 {"id": "rowSport", "title": "Huskies", "kind": "land", "href": "https://gonu.com/", "items": ATHLETICS_STORIES},
]
for slug, name in [("science-technology", "Science & Technology"), ("health", "Health"),
                   ("society-culture", "Society & Culture"), ("arts-entertainment", "Arts & Entertainment"),
                   ("business", "Business")]:
    ROWS.append({"id": "row-" + slug, "title": name.replace("&", "&amp;"), "kind": "land",
                 "href": f"{NGN}/category/{slug}/", "live": slug, "tagname": name, "items": snap(slug, name)})

BB = P["coop"]

CSS = r"""
  /* ================= concept 7: Northeastern, streaming ================= */
  body{background:var(--dark);color:#fff}
  :root{--g:calc(max(0px, (100vw - 1280px) / 2) + clamp(20px, 4vw, 48px))}

  /* billboard */
  .nf-bb{position:relative;height:clamp(600px, 56.25vw, 100svh);overflow:hidden;background:#000}
  .nf-bb video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
  .nf-vig{position:absolute;inset:0;pointer-events:none;
    background:linear-gradient(77deg,rgba(0,0,0,.78) 0%,rgba(0,0,0,.35) 38%,transparent 64%),
               linear-gradient(to top,var(--dark) 0%,rgba(11,11,14,.72) 14%,transparent 42%)}
  .nf-bb-in{position:absolute;left:var(--g);bottom:clamp(170px,19vw,330px);width:min(46vw,600px);z-index:2}
  .nf-kick{display:flex;align-items:center;gap:9px;font-size:15px;font-weight:600;color:#E5E5E5;letter-spacing:.02em}
  .nf-kick img{height:24px;width:auto}
  .nf-title{margin-top:10px;font-size:clamp(66px,8.4vw,150px);font-weight:700;letter-spacing:-.045em;line-height:.88;
    transform-origin:left bottom;transition:transform 1.1s var(--ease);text-shadow:0 2px 30px rgba(0,0,0,.35)}
  .nf-syn{margin-top:18px;font-size:clamp(16px,1.3vw,20px);font-weight:400;line-height:1.45;color:#F1F1F1;max-width:36ch;
    text-shadow:0 1px 12px rgba(0,0,0,.5);max-height:8em;overflow:hidden;
    transition:opacity .8s var(--ease),max-height 1.1s var(--ease),margin 1.1s var(--ease)}
  .nf-bb.settled .nf-title{transform:scale(.72)}
  .nf-bb.settled .nf-syn{opacity:0;max-height:0;margin-top:0}
  .nf-cta{display:inline-flex;align-items:center;gap:12px;margin-top:22px;height:52px;padding:0 28px 0 24px;
    border-radius:6px;background:#fff;color:#0B0B0E;font-size:18px;font-weight:600;transition:background .2s}
  .nf-cta:hover{background:rgba(255,255,255,.78)}
  .nf-side{position:absolute;right:0;bottom:clamp(170px,19vw,330px);z-index:2;display:flex;align-items:center;gap:14px}
  .nf-mute{all:unset;box-sizing:border-box;width:44px;height:44px;border-radius:50%;border:1px solid rgba(255,255,255,.7);
    display:grid;place-items:center;cursor:pointer;color:#fff;transition:background .2s}
  .nf-mute:hover{background:rgba(255,255,255,.12)}
  .nf-mute:focus-visible{outline:2px solid #fff;outline-offset:3px}
  .nf-mute .on{display:none}.nf-mute[aria-pressed="true"] .on{display:block}.nf-mute[aria-pressed="true"] .off{display:none}
  .nf-est{background:rgba(51,51,51,.62);border-left:3px solid #DCDCDC;padding:8px 44px 8px 12px;font-size:15px;font-weight:500}

  /* rows */
  .nf-rows{position:relative;z-index:3;margin-top:calc(-1 * clamp(120px,13vw,250px));padding-bottom:clamp(60px,8vw,120px);overflow-x:clip}
  .nf-row{margin-bottom:clamp(30px,3.4vw,54px)}
  .nf-row[hidden]{display:none}
  .nf-head{display:flex;align-items:flex-end;justify-content:space-between;padding:0 var(--g);margin-bottom:12px}
  .nf-head h2{font-size:clamp(17px,1.4vw,23px);font-weight:600;color:#E8E8E8;letter-spacing:-.005em}
  .nf-head h2 a{display:inline-flex;align-items:baseline;gap:10px}
  .nf-ex{font-size:13.5px;font-weight:600;color:#fff;opacity:0;transform:translateX(-8px);transition:opacity .3s,transform .3s var(--ease);white-space:nowrap}
  .nf-ex::after{content:" \203A";font-size:17px}
  .nf-head h2 a:hover .nf-ex,.nf-head h2 a:focus-visible .nf-ex{opacity:1;transform:none}
  .nf-pag{display:flex;gap:2px;opacity:0;transition:opacity .3s}
  .nf-pag i{width:14px;height:2px;background:#4a4a4f}
  .nf-pag i.on{background:#B3B3B3}
  .nf-row:hover .nf-pag{opacity:1}
  .nf-slider{position:relative}
  .nf-track{display:flex;gap:var(--gap,8px);padding:0 var(--g);transition:transform .85s cubic-bezier(.5,0,.1,1);will-change:transform}
  .nf-card,.nf-poster,.nf-top{position:relative;flex:0 0 var(--cw,260px);display:block;color:#fff}
  .nf-card{aspect-ratio:16/9;border-radius:6px;overflow:hidden;background:#1a1a1f}
  .nf-card img,.nf-poster img,.nf-tp img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
  .nf-card::after,.nf-poster::after{content:"";position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,.78) 0%,transparent 55%)}
  .nf-card .t{position:absolute;left:12px;right:12px;bottom:10px;z-index:2;font-size:13.5px;font-weight:600;line-height:1.28;
    display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
  .nf-card .tg{position:absolute;left:12px;top:10px;z-index:2;font-size:11.5px;font-weight:600;color:#fff;
    background:rgba(11,11,14,.55);padding:3px 8px;border-radius:4px}
  .nf-poster{aspect-ratio:2/3;border-radius:6px;overflow:hidden;background:#1a1a1f}
  .nf-pn{position:absolute;left:12px;top:12px;z-index:2}
  .nf-pn img{position:static;height:18px;width:auto}
  .nf-pt{position:absolute;left:14px;right:14px;bottom:14px;z-index:2;font-size:clamp(20px,1.8vw,30px);font-weight:700;
    letter-spacing:-.03em;line-height:.95}
  .nf-typo{position:absolute;inset:0;background:radial-gradient(120% 90% at 20% 10%,#5a0c1a 0%,#1a0a0e 55%,#0e0e12 100%);
    padding:44px 14px 0;display:grid;grid-template-columns:1fr 1fr;align-content:start;gap:3px 10px;
    font-size:12px;line-height:1.35;color:rgba(255,255,255,.66)}
  .nf-top{display:flex;align-items:flex-end;height:calc(var(--cw,260px) * .8)}
  .nf-num{flex:0 0 46%;font-size:calc(var(--cw,260px) * .92);font-weight:700;line-height:.8;letter-spacing:-.12em;text-align:right;
    color:var(--dark);-webkit-text-stroke:3px #5b5b62;margin-right:-4%;user-select:none}
  .nf-top.ten .nf-num{flex-basis:56%;letter-spacing:-.16em}
  .nf-tp{position:relative;flex:0 0 54%;height:100%;border-radius:6px;overflow:hidden;background:#1a1a1f}
  .nf-tp::after{content:"";position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,.8) 0%,transparent 50%)}
  .nf-tp .nf-pt{font-size:clamp(15px,1.25vw,20px);left:10px;right:10px;bottom:10px}
  .nf-card:focus-visible,.nf-poster:focus-visible,.nf-top:focus-visible .nf-tp{outline:2px solid #fff;outline-offset:3px}
  .nf-h{all:unset;position:absolute;top:0;bottom:0;z-index:4;width:max(40px, calc(var(--g) - 8px));display:flex;align-items:center;justify-content:center;
    background:rgba(11,11,14,.5);color:#fff;cursor:pointer;opacity:0;transition:opacity .25s,background .25s}
  .nf-h.prev{left:0;border-radius:0 6px 6px 0}.nf-h.next{right:0;border-radius:6px 0 0 6px}
  .nf-h svg{transition:transform .2s}
  .nf-slider:hover .nf-h,.nf-h:focus-visible{opacity:1}
  .nf-h:hover{background:rgba(11,11,14,.78)}
  .nf-h:hover svg{transform:scale(1.25)}
  .nf-h[hidden]{display:none}

  /* hover preview */
  #nfPop{position:absolute;z-index:80;border-radius:8px;overflow:hidden;background:#18181c;color:#fff;
    box-shadow:0 22px 60px rgba(0,0,0,.8);opacity:0;pointer-events:none;
    transition:transform .3s cubic-bezier(.2,.8,.2,1),opacity .22s}
  #nfPop.open{opacity:1;transform:none !important;pointer-events:auto}
  #nfPop a{display:block;color:#fff}
  .pop-m{position:relative;aspect-ratio:16/9;background:#000}
  .pop-m img,.pop-m video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
  .pop-m video{opacity:0;transition:opacity .5s}
  .pop-m video.live{opacity:1}
  .pop-b{padding:14px 16px 18px}
  .pop-r{display:flex;align-items:center;gap:12px}
  .pop-go{flex:0 0 auto;width:40px;height:40px;border-radius:50%;background:#fff;color:#111;display:grid;place-items:center}
  .pop-t{font-size:16px;font-weight:600;line-height:1.28}
  .pop-meta{margin-top:10px;display:flex;flex-wrap:wrap;font-size:13px;font-weight:500;color:#bdbdc4}
  .pop-meta{gap:2px 0}
  .pop-meta span:not(:last-child)::after{content:"\2022";margin:0 8px;color:#65656c}
  .pop-ex{margin-top:8px;font-size:13.5px;line-height:1.45;color:#d6d6dc;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}

  @media (max-width:699px){
    .nf-bb{height:88svh}
    .nf-bb-in{width:auto;right:var(--g);bottom:120px}
    .nf-side{bottom:auto;top:92px}
    .nf-rows{margin-top:-70px}
    .nf-track{overflow-x:auto;transform:none !important;scroll-snap-type:x mandatory;scroll-padding-inline:var(--g);scrollbar-width:none}
    .nf-track::-webkit-scrollbar{display:none}
    .nf-card,.nf-poster,.nf-top{scroll-snap-align:start}
    .nf-card{flex-basis:62vw}.nf-poster{flex-basis:38vw}.nf-top{flex-basis:56vw;height:44vw}
    .nf-num{font-size:52vw}
    .nf-h,.nf-pag,.nf-ex{display:none}
  }
  @media (prefers-reduced-motion: reduce){
    .nf-track,.nf-title,.nf-syn,#nfPop{transition:none}
  }
"""

ICON_R = '<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_L = '<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_ARROW = '<svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><path d="M4 10h11M11 5.5l4.5 4.5-4.5 4.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SPK_OFF = '<svg class="off" width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><path d="M3 7.5h3l4-3.5v12l-4-3.5H3z" fill="currentColor"/><path d="M13 7.5l4 5M17 7.5l-4 5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'
SPK_ON = '<svg class="on" width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><path d="M3 7.5h3l4-3.5v12l-4-3.5H3z" fill="currentColor"/><path d="M13 7a4 4 0 010 6M15.2 5a7 7 0 010 10" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'

def row_shell(r):
    title = r["title"]
    h = (f'<a href="{r["href"]}">{title}<span class="nf-ex">Explore all</span></a>' if r.get("href")
         else f'<span>{title}</span>')
    hid = " hidden" if r["id"] == "rowContinue" else ""
    return (f'<section class="nf-row" id="{r["id"]}" data-kind="{r["kind"]}"{hid} aria-label="{title}">\n'
            f'  <div class="nf-head"><h2>{h}</h2><div class="nf-pag" aria-hidden="true"></div></div>\n'
            f'  <div class="nf-slider"><button class="nf-h prev" hidden aria-label="Previous in {title}">{ICON_L}</button>'
            f'<div class="nf-track"></div>'
            f'<button class="nf-h next" aria-label="Next in {title}">{ICON_R}</button></div>\n</section>\n')

BODY = f'''
<section class="nf-bb" id="top" aria-label="Featured: {BB["t"]}">
  <video autoplay muted loop playsinline poster="{BB["img"]}" src="{BB["big"]}"></video>
  <div class="nf-vig"></div>
  <div class="nf-bb-in">
    <div class="nf-kick"><img src="{MONO}" alt="">Series</div>
    <h1 class="nf-title">{BB["t"]}</h1>
    <p class="nf-syn">{BB["ex"]}</p>
    <a class="nf-cta" href="{BB["u"]}">{ICON_ARROW}Explore co&#8209;op</a>
  </div>
  <div class="nf-side">
    <button class="nf-mute" id="nfMute" aria-pressed="false" aria-label="Unmute">{SPK_OFF}{SPK_ON}</button>
    <span class="nf-est">Est. 1898</span>
  </div>
</section>

<div class="nf-rows">
{"".join(row_shell(r) for r in ROWS)}</div>
<div id="nfPop" aria-hidden="true"></div>
'''

JS = SHARED_JS + r"""
/* ============ concept 7: billboard ============ */
const nfBB = $(".nf-bb"), nfVid = $(".nf-bb video"), nfMute = $("#nfMute");
if (!reduceMotion) setTimeout(() => nfBB.classList.add("settled"), 6500);
else nfVid.pause();
nfMute.addEventListener("click", () => {
  const on = nfMute.getAttribute("aria-pressed") !== "true";
  nfMute.setAttribute("aria-pressed", on ? "true" : "false");
  nfMute.setAttribute("aria-label", on ? "Mute" : "Unmute");
  nfVid.muted = !on;
  if (on) nfVid.play().catch(() => {});
});
new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { if (!reduceMotion) nfVid.play().catch(() => {}); } else nfVid.pause();
}), { threshold: .2 }).observe(nfBB);

/* ============ rows ============ */
const ROWS = """ + jsdata(ROWS) + r""";
const CAT_IDS = """ + jsdata(CAT_IDS) + r""";
const MONO = """ + jsdata(MONO) + r""";
const typo = it => `<span class="nf-typo">${(it.cities || []).map(c => `<span>${esc(c)}</span>`).join("")}</span>`;
function tileHTML(row, it, i) {
  const k = row.kind, data = `data-r="${row.id}" data-i="${i}" data-cb="${cbAttr(it)}"`;
  const media = it.img ? `<img src="${esc(it.img)}" alt="" loading="lazy">` : typo(it);
  if (k === "poster") return `<a class="nf-poster" href="${esc(it.u)}" ${data}>${media}` +
    `<span class="nf-pn"><img src="${MONO}" alt=""></span><span class="nf-pt">${esc(it.t)}</span></a>`;
  if (k === "top") return `<a class="nf-top${i === 9 ? " ten" : ""}" href="${esc(it.u)}" ${data} aria-label="${i + 1}. ${esc(it.t)}">` +
    `<span class="nf-num" aria-hidden="true">${i + 1}</span><span class="nf-tp">${media}<span class="nf-pt">${esc(it.t)}</span></span></a>`;
  return `<a class="nf-card" href="${esc(it.u)}" ${data}>${media}` +
    (it.tag ? `<span class="tg">${esc(it.tag)}</span>` : "") + `<span class="t">${esc(it.t)}</span></a>`;
}
const SL = new Map();
function renderRow(row) {
  const el = document.getElementById(row.id);
  if (!el) return;
  if (!row.items.length) { el.hidden = true; return; }
  el.hidden = false;
  el.querySelector(".nf-track").innerHTML = row.items.map((it, i) => tileHTML(row, it, i)).join("");
  const s = SL.get(row.id) || { page: 0, moved: false };
  s.row = row; s.el = el; s.track = el.querySelector(".nf-track"); s.page = 0;
  SL.set(row.id, s);
  layoutOne(s);
}
const PER = { land: [[1500, 6], [1100, 5], [860, 4], [0, 3]], poster: [[1500, 8], [1100, 7], [860, 5], [0, 4]], top: [[1500, 5], [1100, 4], [860, 3], [0, 3]] };
function layoutOne(s) {
  const vw = document.documentElement.clientWidth;
  const prev = s.el.querySelector(".prev"), next = s.el.querySelector(".next"), pag = s.el.querySelector(".nf-pag");
  if (vw < 700) { s.track.style.removeProperty("--cw"); s.desktop = false; return; }
  s.desktop = true;
  const g = parseFloat(getComputedStyle(s.track).paddingLeft), gap = vw >= 1400 ? 10 : 8;
  s.per = PER[s.row.kind].find(([w]) => vw >= w)[1];
  s.cw = (vw - 2 * g - (s.per - 1) * gap) / s.per;
  s.track.style.setProperty("--cw", s.cw + "px");
  s.track.style.setProperty("--gap", gap + "px");
  s.step = s.cw + gap;
  s.n = s.row.items.length;
  s.pages = Math.max(1, Math.ceil(s.n / s.per));
  s.maxOff = Math.max(0, s.n * s.step - gap - (vw - 2 * g));
  s.page = Math.min(s.page, s.pages - 1);
  pag.innerHTML = s.pages > 1 ? Array.from({ length: s.pages }, () => "<i></i>").join("") : "";
  next.hidden = s.pages <= 1;
  prev.hidden = s.pages <= 1 || !s.moved;
  applyPage(s);
}
function applyPage(s) {
  if (!s.desktop) return;
  s.track.style.transform = `translateX(${-Math.min(s.page * s.per * s.step, s.maxOff)}px)`;
  [...s.el.querySelectorAll(".nf-pag i")].forEach((d, j) => d.classList.toggle("on", j === s.page));
  s.track.querySelectorAll("a").forEach((a, j) => {
    const vis = j >= s.page * s.per && j < s.page * s.per + s.per;
    a.tabIndex = vis ? 0 : -1;
  });
}
function page(s, dir) {
  s.moved = true;
  s.el.querySelector(".prev").hidden = false;
  s.page = (s.page + dir + s.pages) % s.pages;
  applyPage(s);
  closePop(true);
}
document.addEventListener("click", e => {
  const h = e.target.closest(".nf-h");
  if (!h) return;
  const s = SL.get(h.closest(".nf-row").id);
  page(s, h.classList.contains("next") ? 1 : -1);
});
let rzT;
addEventListener("resize", () => { cancelAnimationFrame(rzT); rzT = requestAnimationFrame(() => SL.forEach(layoutOne)); });

/* continue browsing first, then everything else */
const contRow = ROWS.find(r => r.id === "rowContinue");
contRow.items = cbRead().slice(0, 12).map(c => ({ t: c.t, img: c.img || null, u: c.u, tag: c.tag || "" }));
ROWS.forEach(renderRow);

/* live NGN: refresh the rows that carry a category */
ROWS.filter(r => r.live).forEach(async r => {
  try {
    const items = await ngnFetch(CAT_IDS[r.live], 16);
    if (items.length < 4) return;
    const tag = r.tagname || "";
    const fresh = items.map(x => Object.assign(x, { tag }));
    r.items = fresh;
    renderRow(r);
  } catch (err) { /* snapshot remains */ }
});

/* ============ hover preview ============ */
const pop = $("#nfPop");
const finePointer = matchMedia("(hover: hover) and (pointer: fine)").matches;
let popT = null, popCloseT = null, popFor = null;
function itemFor(a) {
  const row = ROWS.find(r => r.id === a.dataset.r);
  return row && row.items[+a.dataset.i];
}
function openPop(a) {
  const it = itemFor(a);
  if (!it) return;
  popFor = a;
  const r = a.getBoundingClientRect(), vw = document.documentElement.clientWidth;
  const media = a.querySelector(".nf-tp") || a;
  const mr = media.getBoundingClientRect();
  const w = Math.max(320, Math.min(440, mr.width * (a.classList.contains("nf-card") ? 1.5 : 2.1)));
  const mh = w * 9 / 16;
  let left = mr.left + mr.width / 2 - w / 2;
  left = Math.max(10, Math.min(vw - w - 10, left));
  const top = Math.max(scrollY + 84, mr.top + scrollY + mr.height / 2 - mh / 2 - 10);
  const tags = it.tags || [it.tag, it.d ? fmtDate(it.d) : ""].filter(Boolean);
  pop.innerHTML = `<a href="${esc(it.u)}" data-cb="${cbAttr(it)}">` +
    `<div class="pop-m">${it.img ? `<img src="${esc(it.img)}" alt="">` : typo(it)}` +
    (it.film && !reduceMotion ? `<video muted loop playsinline src="${esc(it.film)}"></video>` : "") + `</div>` +
    `<div class="pop-b"><div class="pop-r"><span class="pop-go">${""}<svg width="18" height="18" viewBox="0 0 20 20" aria-hidden="true"><path d="M4 10h11M11 5.5l4.5 4.5-4.5 4.5" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></span>` +
    `<span class="pop-t">${esc(it.t)}</span></div>` +
    (tags.length ? `<div class="pop-meta">${tags.map(t => `<span>${esc(t)}</span>`).join("")}</div>` : "") +
    (it.ex ? `<p class="pop-ex">${esc(it.ex)}</p>` : "") + `</div></a>`;
  pop.style.width = w + "px";
  pop.style.left = left + "px";
  pop.style.top = top + "px";
  const s0 = mr.width / w;
  pop.style.transformOrigin = `${mr.left + mr.width / 2 - left}px ${mh / 2 + 10}px`;
  pop.style.transform = `scale(${s0})`;
  pop.classList.remove("open");
  void pop.offsetWidth;
  pop.classList.add("open");
  const v = pop.querySelector("video");
  if (v) { v.addEventListener("timeupdate", () => { if (v.currentTime > .15) v.classList.add("live"); }); v.play().catch(() => {}); }
}
function closePop(now) {
  clearTimeout(popT); clearTimeout(popCloseT);
  const go = () => { pop.classList.remove("open"); const v = pop.querySelector("video"); if (v) v.pause(); popFor = null; };
  if (now === true) go(); else popCloseT = setTimeout(go, 140);
}
if (finePointer) {
  document.addEventListener("mouseover", e => {
    const a = e.target.closest(".nf-track a");
    if (!a || a === popFor) return;
    clearTimeout(popT); clearTimeout(popCloseT);
    popT = setTimeout(() => openPop(a), popFor ? 60 : 480);
  });
  document.addEventListener("mouseout", e => {
    const a = e.target.closest(".nf-track a");
    if (!a || (e.relatedTarget && (a.contains(e.relatedTarget) || pop.contains(e.relatedTarget)))) return;
    clearTimeout(popT);
    if (popFor) closePop();
  });
  pop.addEventListener("mouseenter", () => clearTimeout(popCloseT));
  pop.addEventListener("mouseleave", () => closePop());
  addEventListener("scroll", () => { if (popFor) closePop(true); }, { passive: true });
}
"""

html = page("concept7", 1, CSS, BODY, JS)
for tok in ["nf-bb", "nfPop", "rowContinue", "rowOnly", "rowTen", "nu-stream-continue", "Est. 1898", "ngnFetch"]:
    assert tok in html, tok
assert html.count("<video autoplay") == 1
write("concept-7", html)
