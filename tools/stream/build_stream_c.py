"""Concept 9 · Northeastern Live, a live-TV program guide. Each pillar and NGN desk is a
channel that loops its real stories on half-hour slots (a clock-anchored schedule, so
every channel always has something on now and up next). Preview screen on top, guide
below with a real-time Now line; arrow keys surf like a remote; click opens the story
or landing page."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stream_common import *

P = PBYKEY
def s(slug): return [dict(x, tag="") for x in SNAP[slug]]
def dedupe(a, b, n):
    seen = {x["u"] for x in a}
    return a + [x for x in b if x["u"] not in seen][: max(0, n - len(a))]

campus_items = [LIFE_STORIES[2], LIFE_STORIES[3], LIFE_STORIES[1]] + [
    item(f"Northeastern in {n}" if n != "And nine more" else "Fourteen campuses, one university", img, u,
         P["campuses"]["ex"], "Campus") for n, img, u in CAMPUS_SITES]
CHANNELS = [
 {"n": 100, "name": "Northeastern Now", "u": NGN + "/", "live": "latest", "film": "../hero-sm.mp4", "items": s("latest")},
 {"n": 101, "name": "Co‑op", "u": P["coop"]["u"], "film": "../coop-sm.mp4",
  "items": COOP_STORIES + [item("What co‑op is", P["coop"]["img"], P["coop"]["u"], P["coop"]["ex"], "Experiential learning")]},
 {"n": 102, "name": "Research", "u": P["research"]["u"], "live": "research",
  "items": dedupe(RESEARCH_STORIES, s("research"), 12)},
 {"n": 103, "name": "Admissions", "u": P["admissions"]["u"], "film": "../hero-sm.mp4", "items": ADMIT_PATHS},
 {"n": 104, "name": "Campuses", "u": P["campuses"]["u"], "film": "../jamie-sm.mp4", "items": campus_items},
 {"n": 105, "name": "Student life", "u": P["life"]["u"], "film": "../jamie-sm.mp4", "items": LIFE_STORIES},
 {"n": 106, "name": "Huskies", "u": "https://gonu.com/", "items": ATHLETICS_STORIES},
]
for i, (slug, name) in enumerate([("science-technology", "Science & Tech"), ("health", "Health"),
        ("society-culture", "Society & Culture"), ("business", "Business"),
        ("arts-entertainment", "Arts"), ("law", "Law"), ("world-news", "World & Nation")]):
    CHANNELS.append({"n": 107 + i, "name": name, "u": f"{NGN}/category/{slug}/", "live": slug, "items": s(slug)})

CSS = r"""
  /* ================= concept 9: Northeastern Live ================= */
  body{background:#08080B;color:#fff}
  :root{--g:calc(max(0px, (100vw - 1280px) / 2) + clamp(20px, 4vw, 48px));--chw:190px;--rowh:84px;--timesh:44px}
  .nav.solid{background:rgba(8,8,11,.94)}
  .lv-app{height:100svh;min-height:760px;display:grid;grid-template-columns:minmax(0,1fr);grid-template-rows:auto minmax(0,1fr);padding-top:72px}
  .lv-top{display:grid;grid-template-columns:auto minmax(0,1fr);gap:clamp(24px,3vw,44px);align-items:stretch;
    padding:18px var(--g) 18px;height:clamp(300px,43svh,470px)}
  .lv-screen{position:relative;height:100%;aspect-ratio:16/9;max-width:56vw;border-radius:10px;overflow:hidden;background:#000;
    box-shadow:0 0 0 1px rgba(255,255,255,.08),0 24px 60px rgba(0,0,0,.6)}
  .lv-screen > img:not(.lv-bug),.lv-screen > video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
  .lv-screen > img:not(.lv-bug){animation:lvkb 18s ease-in-out infinite alternate}
  @keyframes lvkb{from{transform:scale(1)}to{transform:scale(1.09) translate(-1.2%,-1%)}}
  .lv-screen video{opacity:0;transition:opacity .5s}
  .lv-screen video.live{opacity:1}
  .lv-screen::before{content:"";position:absolute;inset:0;z-index:2;pointer-events:none;
    background:linear-gradient(to top,rgba(0,0,0,.55),transparent 35%),linear-gradient(to bottom,rgba(0,0,0,.45),transparent 30%)}
  .lv-screen::after{content:"";position:absolute;inset:-50%;z-index:4;pointer-events:none;opacity:0;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='1.2' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}
  .lv-screen.flip::after{animation:lvstatic .32s steps(4)}
  @keyframes lvstatic{0%{opacity:.75;transform:translate(0,0)}33%{opacity:.6;transform:translate(-3%,2%)}66%{opacity:.35;transform:translate(2%,-3%)}100%{opacity:0}}
  .lv-osd{position:absolute;z-index:3;left:16px;top:14px;display:flex;align-items:center;gap:10px;font-size:13px;font-weight:600}
  .lv-badge{display:inline-flex;align-items:center;gap:7px;padding:4px 10px;border-radius:4px;background:rgba(0,0,0,.55)}
  .lv-badge::before{content:"";width:7px;height:7px;border-radius:50%;background:#8E8E96}
  .lv-badge.on::before{background:var(--red);animation:lvpulse 1.8s ease infinite}
  @keyframes lvpulse{0%,100%{box-shadow:0 0 0 0 rgba(200,16,46,.6)}50%{box-shadow:0 0 0 6px rgba(200,16,46,0)}}
  .lv-chnum{position:absolute;z-index:3;right:16px;top:10px;font-size:30px;font-weight:700;letter-spacing:-.02em;
    color:rgba(255,255,255,.92);text-shadow:0 2px 10px rgba(0,0,0,.6);font-variant-numeric:tabular-nums}
  .lv-bug{position:absolute;z-index:3;right:16px;bottom:14px;height:22px;width:auto;opacity:.75}
  .lv-info{display:flex;flex-direction:column;justify-content:flex-end;min-width:0;padding-bottom:4px}
  .lv-kick{display:flex;align-items:center;gap:10px;font-size:14px;font-weight:600;color:#A9A9B2}
  .lv-kick b{color:#fff}
  .lv-title{margin-top:12px;font-size:clamp(24px,2.6vw,42px);font-weight:600;letter-spacing:-.025em;line-height:1.1;
    display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
  .lv-when{margin-top:14px;display:flex;align-items:center;gap:12px;font-size:14px;color:#D4D4D9;font-variant-numeric:tabular-nums}
  .lv-prog{position:relative;width:120px;height:3px;border-radius:2px;background:rgba(255,255,255,.18);overflow:hidden}
  .lv-prog i{position:absolute;left:0;top:0;bottom:0;background:var(--red)}
  .lv-ex{margin-top:12px;font-size:15px;line-height:1.5;color:#C9C9D0;max-width:56ch;
    display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
  .lv-acts{margin-top:18px;display:flex;align-items:center;gap:18px;flex-wrap:wrap}
  .lv-go{display:inline-flex;align-items:center;gap:10px;height:46px;padding:0 22px;border-radius:6px;background:#fff;color:#0B0B0E;
    font-size:15.5px;font-weight:600}
  .lv-go:hover{background:rgba(255,255,255,.8)}
  .lv-next{font-size:13.5px;color:#A9A9B2;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:46ch}
  .lv-next b{color:#E5E5EA;font-weight:600}

  /* guide */
  .lv-guide{min-height:0;min-width:0;margin-left:var(--g);border-top:1px solid rgba(255,255,255,.08);position:relative}
  .lv-scroll{height:100%;overflow:auto;overscroll-behavior:contain;scrollbar-width:thin;scrollbar-color:#2a2a31 transparent}
  .lv-grid{position:relative}
  .lv-times{position:sticky;top:0;z-index:5;height:var(--timesh);background:#08080B;border-bottom:1px solid rgba(255,255,255,.08)}
  .lv-corner{position:sticky;left:0;z-index:6;width:var(--chw);height:100%;background:#08080B;display:flex;align-items:center;
    gap:8px;font-size:13px;font-weight:600;color:#fff;font-variant-numeric:tabular-nums}
  .lv-corner span{color:#A9A9B2;font-weight:500}
  .lv-tl{position:absolute;top:0;height:100%;display:flex;align-items:flex-start;padding:7px 0 0 10px;font-size:12.5px;font-weight:500;
    color:#A9A9B2;border-left:1px solid rgba(255,255,255,.08);font-variant-numeric:tabular-nums}
  .lv-row{position:relative;display:flex;height:var(--rowh);border-bottom:1px solid rgba(255,255,255,.05)}
  .lv-ch{position:sticky;left:0;z-index:4;flex:0 0 var(--chw);display:flex;align-items:center;gap:12px;padding:0 14px 0 0;
    background:#08080B;color:#fff;border-right:1px solid rgba(255,255,255,.08)}
  .lv-ch:hover .lv-chn{color:#fff}
  .lv-ch .num{font-size:13px;font-weight:600;color:#6E6E78;font-variant-numeric:tabular-nums;width:30px}
  .lv-chn{font-size:14.5px;font-weight:600;color:#E5E5EA;line-height:1.2}
  .lv-ch:focus-visible{outline:2px solid #fff;outline-offset:-3px}
  .lv-progs{position:relative;flex:1}
  .pg{position:absolute;top:5px;bottom:5px;border-radius:7px;background:#15151A;color:#fff;padding:9px 12px;overflow:hidden;
    display:flex;flex-direction:column;justify-content:space-between;transition:background .15s,box-shadow .15s}
  .pg.live{background:#1D1D24;box-shadow:inset 3px 0 0 var(--red)}
  .pg.past{opacity:.42}
  .pg:hover,.pg:focus-visible,.pg.sel{background:#2A2A33}
  .pg.sel{box-shadow:inset 0 0 0 2px #fff}
  .pg.live.sel{box-shadow:inset 3px 0 0 var(--red),inset 0 0 0 2px #fff}
  .pg:focus-visible{outline:none}
  .pg-t{font-size:13.5px;font-weight:600;line-height:1.28;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
  .pg-m{font-size:11.5px;color:#9A9AA3;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-variant-numeric:tabular-nums}
  .lv-nowline{position:absolute;top:0;bottom:0;z-index:3;width:2px;margin-left:-1px;background:var(--red);pointer-events:none}
  .lv-nowtag{position:absolute;z-index:7;bottom:4px;transform:translateX(-50%);padding:1px 7px;border-radius:4px;background:var(--red);
    font-size:11.5px;font-weight:700;color:#fff;pointer-events:none}
  .lv-hint{margin-left:auto;font-size:12px;font-weight:500;color:#6E6E78;white-space:nowrap}
  .lv-hint kbd{font-family:inherit;border:1px solid #33333b;border-radius:4px;padding:0 5px;color:#A9A9B2}

  @media (max-width:820px){
    :root{--chw:118px;--rowh:80px}
    .lv-app{height:auto;min-height:0;grid-template-rows:auto auto}
    .lv-top{grid-template-columns:1fr;height:auto;padding-top:14px}
    .lv-screen{width:100%;height:auto;max-width:none}
    .lv-app{grid-template-rows:auto auto}
    .lv-guide{margin-left:0;height:72svh}
    .lv-chn{font-size:13px}.lv-ch .num{display:none}.lv-ch{padding-left:12px}
    .lv-hint{display:none}
  }
  @media (prefers-reduced-motion: reduce){
    .lv-screen img{animation:none}
      .lv-screen.flip::after,.lv-badge.on::before{animation:none}
  }
"""

BODY = f'''
<main class="lv-app" id="top">
  <section class="lv-top" aria-label="Now showing">
    <a class="lv-screen" id="lvScreen" href="#"><span class="lv-osd"><span class="lv-badge on" id="lvBadge">On now</span></span>
      <span class="lv-chnum" id="lvNum"></span><img class="lv-bug" src="{MONO}" alt=""></a>
    <div class="lv-info" aria-live="polite">
      <div class="lv-kick"><span id="lvCh"></span><span class="lv-hint" aria-hidden="true">Surf with <kbd>&larr;</kbd><kbd>&uarr;</kbd><kbd>&darr;</kbd><kbd>&rarr;</kbd></span></div>
      <h1 class="lv-title" id="lvTitle"></h1>
      <div class="lv-when"><span id="lvWhen"></span><span class="lv-prog" id="lvProgWrap"><i id="lvProg"></i></span></div>
      <p class="lv-ex" id="lvEx"></p>
      <div class="lv-acts"><a class="lv-go" id="lvGo" href="#"><span id="lvGoL">Read the story</span>
        <svg width="18" height="18" viewBox="0 0 20 20" aria-hidden="true"><path d="M4 10h11M11 5.5l4.5 4.5-4.5 4.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
        <span class="lv-next" id="lvNext"></span></div>
    </div>
  </section>
  <section class="lv-guide" aria-label="Program guide">
    <div class="lv-scroll" id="lvScroll" data-lenis-prevent><div class="lv-grid" id="lvGrid"></div></div>
  </section>
</main>
'''

JS = SHARED_JS + r"""
/* ============ concept 9: Northeastern Live ============ */
const CHANNELS = """ + jsdata(CHANNELS) + r""";
const LV_CAT_IDS = """ + jsdata(CAT_IDS) + r""";
const lvGrid = $("#lvGrid"), lvScroll = $("#lvScroll"), lvScreen = $("#lvScreen");
const narrow = () => document.documentElement.clientWidth <= 820;
const PXM = () => narrow() ? 4.4 : 6.2;                 /* px per minute */
const CHW = () => narrow() ? 118 : 190;
const localMin = () => { const d = new Date(); return Math.floor((d.getTime() - d.getTimezoneOffset() * 60000) / 60000); };
const fmtT = m => { const h = Math.floor(((m % 1440) + 1440) % 1440 / 60), mm = ((m % 60) + 60) % 60;
  return `${(h % 12) || 12}:${String(mm).padStart(2, "0")} ${h < 12 ? "AM" : "PM"}`; };
const fmtS = m => { const h = Math.floor(((m % 1440) + 1440) % 1440 / 60), mm = ((m % 60) + 60) % 60;
  return `${(h % 12) || 12}:${String(mm).padStart(2, "0")}`; };
let lvWin = null, lvRows = [], lvSel = null, lvSlot = -1;

function schedule(ch, ci, w0, w1) {
  const L = ch.items, n = L.length;
  if (!n) return [];
  const dur = i => (i % 3 === 1 ? 60 : 30);
  let C = 0; for (let i = 0; i < n; i++) C += dur(i);
  const shift = ((ci * 90) % C);
  let t = w0 - ((((w0 - shift) % C) + C) % C), i = 0;
  const out = [];
  while (t < w1) {
    const d = dur(i % n);
    if (t + d > w0) out.push({ s: t, e: t + d, it: L[i % n] });
    t += d; i++;
  }
  return out;
}
function progHTML(p, r, k, now) {
  const px = PXM(), w0 = lvWin[0];
  const L = Math.max(p.s, w0), left = (L - w0) * px + 2, width = (p.e - L) * px - 4;
  const live = p.s <= now && now < p.e, past = p.e <= now;
  const label = `${p.it.t}. ${live ? "On now" : fmtT(p.s)}, until ${fmtT(p.e)}, on ${CHANNELS[r].name}`;
  return `<a class="pg${live ? " live" : ""}${past ? " past" : ""}" href="${esc(p.it.u)}" data-r="${r}" data-k="${k}" ` +
    `data-cb="${cbAttr(p.it)}" style="left:${left}px;width:${width}px" aria-label="${esc(label)}">` +
    `<span class="pg-t">${esc(p.it.t)}</span><span class="pg-m">${fmtS(p.s)} – ${fmtT(p.e)}</span></a>`;
}
function renderGuide(keepScroll) {
  const now = localMin(), px = PXM(), chw = CHW();
  const w0 = Math.floor(now / 30) * 30 - 30, w1 = w0 + 6 * 60;
  lvWin = [w0, w1]; lvSlot = Math.floor(now / 30);
  lvRows = CHANNELS.map((ch, ci) => schedule(ch, ci, w0, w1));
  const width = chw + (w1 - w0) * px;
  let times = "";
  for (let t = w0; t < w1; t += 30) times += `<span class="lv-tl" style="left:${chw + (t - w0) * px}px;width:${30 * px}px">${fmtT(t)}</span>`;
  const d = new Date();
  const rows = CHANNELS.map((ch, r) =>
    `<div class="lv-row" role="group" aria-label="Channel ${ch.n}, ${esc(ch.name)}">` +
    `<a class="lv-ch" href="${esc(ch.u)}"><span class="num">${ch.n}</span><span class="lv-chn">${esc(ch.name)}</span></a>` +
    `<div class="lv-progs">${lvRows[r].map((p, k) => progHTML(p, r, k, now)).join("")}</div></div>`).join("");
  const sl = keepScroll ? lvScroll.scrollLeft : null, st = keepScroll ? lvScroll.scrollTop : 0;
  lvGrid.style.width = width + "px";
  lvGrid.innerHTML = `<div class="lv-times"><div class="lv-corner">${d.toLocaleDateString("en-US", { weekday: "short" })} <span id="lvClock"></span></div>${times}` +
    `<span class="lv-nowtag" id="lvNowTag">Now</span></div>${rows}<span class="lv-nowline" id="lvNowLine"></span>`;
  placeNow();
  if (keepScroll) { lvScroll.scrollLeft = sl; lvScroll.scrollTop = st; }
  else lvScroll.scrollLeft = 30 * px;
  const keep = lvSel && lvGrid.querySelector(`.pg[data-r="${lvSel.r}"].live`);
  select(keep || lvGrid.querySelector('.pg[data-r="0"].live') || lvGrid.querySelector(".pg"), false);
}
function placeNow() {
  const d = new Date(), now = localMin() + d.getSeconds() / 60, x = CHW() + (now - lvWin[0]) * PXM();
  const ln = $("#lvNowLine"), tg = $("#lvNowTag"), ck = $("#lvClock");
  if (ln) ln.style.left = x + "px";
  if (tg) tg.style.left = x + "px";
  if (ck) ck.textContent = d.toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" });
  if (lvSel) updateWhen();
}
function updateWhen() {
  const p = lvRows[lvSel.r][lvSel.k], now = localMin() + new Date().getSeconds() / 60;
  const live = p.s <= now && now < p.e, past = p.e <= now;
  $("#lvWhen").textContent = live ? `On now · ${fmtS(p.s)} – ${fmtT(p.e)}` :
    past ? `Earlier · ${fmtS(p.s)} – ${fmtT(p.e)}` : `Up later · ${fmtS(p.s)} – ${fmtT(p.e)}`;
  $("#lvProgWrap").hidden = !live;
  $("#lvProg").style.width = live ? ((now - p.s) / (p.e - p.s) * 100).toFixed(1) + "%" : "0";
  const b = $("#lvBadge");
  b.classList.toggle("on", live);
  b.textContent = live ? "On now" : past ? "Earlier" : "Coming up";
}
function select(el, flash) {
  if (!el) return;
  const r = +el.dataset.r, k = +el.dataset.k, p = lvRows[r][k], ch = CHANNELS[r];
  const changed = !lvSel || lvSel.r !== r || lvSel.k !== k;
  if (lvSel && lvSel.el) lvSel.el.classList.remove("sel");
  lvSel = { r, k, el }; el.classList.add("sel");
  if (!changed && flash !== false) return;
  const it = p.it;
  if (flash !== false && !reduceMotion) { lvScreen.classList.remove("flip"); void lvScreen.offsetWidth; lvScreen.classList.add("flip"); }
  lvScreen.href = it.u;
  lvScreen.querySelectorAll("img:not(.lv-bug),video").forEach(n => n.remove());
  const bug = lvScreen.querySelector(".lv-bug");
  if (it.img) bug.insertAdjacentHTML("beforebegin", `<img src="${esc(it.img)}" alt="">`);
  else if (ch.film) {
    bug.insertAdjacentHTML("beforebegin", `<video muted loop playsinline src="${esc(ch.film)}"></video>`);
    const v = lvScreen.querySelector("video");
    v.addEventListener("timeupdate", () => { if (v.currentTime > .15) v.classList.add("live"); });
    if (!reduceMotion) v.play().catch(() => {});
  }
  $("#lvNum").textContent = ch.n;
  $("#lvCh").innerHTML = `<b>${ch.n}</b> ${esc(ch.name)}`;
  $("#lvTitle").textContent = it.t;
  $("#lvEx").textContent = it.ex || it.tag || "";
  const go = $("#lvGo");
  go.href = it.u;
  go.dataset.cb = JSON.stringify({ t: it.t, img: it.img || "", u: it.u, tag: it.tag || "" });
  $("#lvGoL").textContent = /news\.northeastern\.edu\/\d{4}\//.test(it.u) ? "Read the story" : "Go there";
  const nx = lvRows[r].find(q => q.s >= p.e);
  $("#lvNext").innerHTML = nx ? `Up next <b>${esc(nx.it.t)}</b>` : "";
  updateWhen();
}
/* hover and focus preview; click follows the link */
let lvHoverT;
lvGrid.addEventListener("mouseover", e => {
  const el = e.target.closest(".pg"); if (!el) return;
  clearTimeout(lvHoverT); lvHoverT = setTimeout(() => select(el), 70);
});
lvGrid.addEventListener("focusin", e => { const el = e.target.closest(".pg"); if (el) select(el); });
/* surf with the arrow keys */
lvGrid.addEventListener("keydown", e => {
  const el = e.target.closest(".pg");
  if (!el || !["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown"].includes(e.key)) return;
  e.preventDefault();
  let r = +el.dataset.r, k = +el.dataset.k;
  const p = lvRows[r][k], mid = Math.max(p.s, lvWin[0]) + 1;
  if (e.key === "ArrowRight") k = Math.min(k + 1, lvRows[r].length - 1);
  if (e.key === "ArrowLeft") k = Math.max(k - 1, 0);
  if (e.key === "ArrowUp" || e.key === "ArrowDown") {
    r = Math.min(Math.max(r + (e.key === "ArrowDown" ? 1 : -1), 0), lvRows.length - 1);
    k = Math.max(0, lvRows[r].findIndex(q => q.s <= mid && mid < q.e));
  }
  const t = lvGrid.querySelector(`.pg[data-r="${r}"][data-k="${k}"]`);
  if (t) { t.focus({ preventScroll: true }); t.scrollIntoView({ block: "nearest", inline: "nearest", behavior: reduceMotion ? "auto" : "smooth" }); }
});
/* the clock drives the guide */
setInterval(() => {
  if (Math.floor(localMin() / 30) !== lvSlot) renderGuide(true); else placeNow();
}, 15000);
let lvRz; addEventListener("resize", () => { clearTimeout(lvRz); lvRz = setTimeout(() => renderGuide(true), 150); });
renderGuide(false);

/* live NGN: refresh the news channels */
CHANNELS.forEach(async (ch, i) => {
  if (!ch.live) return;
  try {
    const items = await ngnFetch(LV_CAT_IDS[ch.live], 16);
    if (items.length < 4) return;
    if (ch.n === 102) { const keep = ch.items.slice(0, 5); ch.items = keep.concat(items.filter(x => !keep.some(k => k.u === x.u))).slice(0, 12); }
    else ch.items = items.map(x => Object.assign(x, { tag: "" }));
    renderGuide(true);
  } catch (err) { /* snapshot remains */ }
});
"""

html = page("concept9", 1, CSS, BODY, JS)
for tok in ["lvGrid", "lvScreen", "Northeastern Now", "renderGuide", "ArrowDown", "data-lenis-prevent", "nu-stream-continue"]:
    assert tok in html, tok
write("concept-9", html)
