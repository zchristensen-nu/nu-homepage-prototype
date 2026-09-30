"""Concept 8 · Northeastern+, Apple TV-style. Light page, center-stage hero with
peeking neighbors (seamless loop, pill-dot progress, trailer fades in on the
active card), then shelves with captions under the art: pillars, colleges as
channels, films, campus posters, a promo banner, live top stories, co-op
posters, research, athletics, and a closing browse grid."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stream_common import *

P = PBYKEY
STAGE = [P[k] for k in ("coop", "research", "campuses", "life", "athletics", "admissions")]
STAGE_DATA = [{"t": p["t"], "img": p["img"], "u": p["u"], "line": p["line"], "big": p.get("big"),
               "cta": "Explore " + (p["t"].lower() if p["key"] not in ("admissions",) else "admissions")} for p in STAGE]
STAGE_DATA[5]["cta"] = "Start your application"
STAGE_DATA[4]["cta"] = "Go to GoNU.com"

FILMS = [
 {"t": "The co‑op experience", "s": "Film · Co‑op", "film": "../coop-sm.mp4", "img": IMG + "apple-coop.jpg", "u": P["coop"]["u"]},
 {"t": "A day in Oakland", "s": "Film · Campuses", "film": "../jamie-sm.mp4", "img": U + "/2026/09/092226_LC_Student_Government_Event_020.jpg", "u": "https://oakland.northeastern.edu/"},
 {"t": "Boston, in motion", "s": "Film · Campuses", "film": "../hero-sm.mp4", "img": U + "/2026/09/AImakerspace1400.jpg", "u": "https://www.northeastern.edu/campuses/"},
]

CSS = r"""
  /* ================= concept 8: Northeastern+ ================= */
  body{background:#F5F5F7;color:#1D1D1F}
  .nav{background:rgba(11,11,14,.94);backdrop-filter:blur(12px)}
  :root{--g:calc(max(0px, (100vw - 1280px) / 2) + clamp(20px, 4vw, 48px));--gap:18px;--sub:#6E6E73}

  /* stage */
  .stage{position:relative;padding:96px 0 0}
  .stage-vp{overflow:hidden;padding:6px 0 10px}
  .stage-track{display:flex;gap:20px;will-change:transform}
  .stage-track.anim{transition:transform .85s cubic-bezier(.4,0,.1,1)}
  .slide{position:relative;flex:0 0 var(--sw);height:clamp(380px, calc(var(--sw) * .44), 66svh);border-radius:20px;overflow:hidden;
    background:#1b1b1f;color:#fff;display:block;transition:opacity .7s var(--ease),transform .7s var(--ease);
    box-shadow:0 18px 44px rgba(0,0,0,.14)}
  .slide:not(.on){opacity:.5;transform:scale(.955)}
  .slide > img,.slide > video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
  .slide video{opacity:0;transition:opacity 1.2s var(--ease)}
  .slide video.live{opacity:1}
  .slide::after{content:"";position:absolute;inset:0;
    background:linear-gradient(20deg,rgba(0,0,0,.72) 0%,rgba(0,0,0,.3) 38%,transparent 62%)}
  .slide-in{position:absolute;z-index:2;left:clamp(24px,4vw,56px);right:24px;bottom:clamp(24px,4vw,52px);max-width:600px;
    opacity:0;transform:translateY(12px);transition:opacity .6s var(--ease) .15s,transform .6s var(--ease) .15s}
  .slide.on .slide-in{opacity:1;transform:none}
  .slide-in > span{display:block}
  .brandchip{display:flex !important;align-items:center;gap:8px;font-size:14px;font-weight:600;color:rgba(255,255,255,.9)}
  .brandchip img{height:17px;width:auto}
  .brandchip b{font-weight:700;color:#fff}
  .slide-t{margin-top:10px;font-size:clamp(40px,5.2vw,82px);font-weight:700;letter-spacing:-.04em;line-height:.95}
  .slide-l{margin-top:12px;font-size:clamp(16px,1.35vw,20px);font-weight:500;color:rgba(255,255,255,.88)}
  .slide-in > .slide-cta{display:inline-flex;align-items:center;gap:10px;margin-top:22px;height:46px;padding:0 24px;border-radius:999px;
    background:#fff;color:#1D1D1F;font-size:16px;font-weight:600}
  .stage-arrow{all:unset;position:absolute;top:calc(96px + 6px + clamp(380px, calc(var(--sw) * .44), 66svh) / 2);transform:translateY(-50%);
    z-index:5;width:46px;height:46px;border-radius:50%;background:rgba(255,255,255,.9);color:#1D1D1F;
    display:grid;place-items:center;cursor:pointer;box-shadow:0 6px 18px rgba(0,0,0,.18);transition:transform .2s}
  .stage-arrow:hover{transform:translateY(-50%) scale(1.08)}
  .stage-arrow:focus-visible{outline:3px solid var(--red);outline-offset:3px}
  .stage-arrow.l{left:calc((100vw - var(--sw)) / 4 - 23px)}
  .stage-arrow.r{right:calc((100vw - var(--sw)) / 4 - 23px)}
  .dots{display:flex;justify-content:center;gap:8px;margin-top:14px}
  .dot{all:unset;position:relative;width:8px;height:8px;border-radius:999px;background:#C7C7CC;cursor:pointer;overflow:hidden;
    transition:width .4s var(--ease)}
  .dot.on{width:34px}
  .dot i{position:absolute;inset:0;width:0;background:#1D1D1F}
  .dot.on.run i{animation:dotfill var(--dur,7s) linear forwards}
  .dot.on:not(.run) i{width:100%}
  @keyframes dotfill{to{width:100%}}
  .dot:focus-visible{outline:2px solid var(--red);outline-offset:3px}

  /* shelves */
  .shelf{position:relative;margin-top:clamp(40px,5vw,64px)}
  .shelf[hidden]{display:none}
  .sh-head{display:flex;align-items:baseline;justify-content:space-between;gap:20px;padding:0 var(--g);margin-bottom:14px}
  .sh-head h2{font-size:clamp(21px,1.7vw,26px);font-weight:700;letter-spacing:-.02em;color:#1D1D1F}
  .sh-head p{margin-top:4px;font-size:15px;color:var(--sub);font-weight:400}
  .sh-all{flex:0 0 auto;font-size:15px;font-weight:600;color:var(--red)}
  .sh-all::after{content:" \203A"}
  .strip{display:grid;grid-auto-flow:column;grid-auto-columns:var(--cw);gap:var(--gap);overflow-x:auto;overscroll-behavior-x:contain;
    scroll-snap-type:x mandatory;scroll-padding-inline:var(--g);padding:6px var(--g) 18px;scrollbar-width:none;
    --cw:calc((100vw - 2 * var(--g) - (var(--cols) - 1) * var(--gap)) / var(--cols))}
  .strip::-webkit-scrollbar{display:none}
  .strip > *{scroll-snap-align:start}
  .strip.land{--cols:4}.strip.poster{--cols:6}.strip.chan{--cols:5}.strip.film{--cols:3}
  .tile{display:block;color:inherit}
  .art{position:relative;display:block;border-radius:12px;overflow:hidden;background:#E3E3E8;
    box-shadow:0 1px 2px rgba(0,0,0,.06);transition:transform .35s var(--ease),box-shadow .35s var(--ease)}
  .tile:hover .art,.tile:focus-visible .art{transform:translateY(-4px) scale(1.02);box-shadow:0 16px 34px rgba(0,0,0,.16)}
  .tile:focus-visible{outline:none}
  .tile:focus-visible .art{outline:3px solid var(--red);outline-offset:3px}
  .art img,.art video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
  .land .art,.film .art{aspect-ratio:16/9}
  .poster .art{aspect-ratio:2/3}
  .cap-t{display:block;margin-top:10px;font-size:15px;font-weight:600;line-height:1.32;color:#1D1D1F;
    display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
  .cap-s{display:block;margin-top:3px;font-size:13.5px;color:var(--sub)}
  .film .art video{opacity:0;transition:opacity .4s}
  .film .tile:hover .art video.live{opacity:1}
  .film .art::after{content:"";position:absolute;right:12px;bottom:12px;width:34px;height:34px;border-radius:50%;
    background:rgba(255,255,255,.92) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M5 3.5v9l7-4.5z' fill='%231D1D1F'/%3E%3C/svg%3E") center/14px no-repeat;
    transition:opacity .3s}
  .film .tile:hover .art::after{opacity:0}
  .typo{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:flex-end;padding:18px;color:#fff;
    background:radial-gradient(130% 90% at 80% 0%,#4b0a17 0%,#16161a 60%)}
  .typo b{display:block;font-size:clamp(22px,1.9vw,30px);font-weight:700;letter-spacing:-.03em;line-height:1}
  .typo small{display:block;margin-top:6px;font-size:12.5px;line-height:1.35;color:rgba(255,255,255,.7)}
  .chan .art{aspect-ratio:16/10;background:#0E0E12}
  .chan .typo{background:radial-gradient(120% 110% at 100% 0%,rgba(200,16,46,.55) 0%,rgba(200,16,46,0) 55%),#101014;justify-content:space-between}
  .chan .typo img{width:22px;height:auto;position:static}
  .chan .typo b{font-size:clamp(19px,1.6vw,27px)}
  .chan .art{aspect-ratio:3/2}
  .sh-arrow{all:unset;position:absolute;z-index:4;top:calc(50% + 10px);transform:translateY(-50%);width:44px;height:44px;border-radius:50%;
    background:#fff;color:#1D1D1F;display:grid;place-items:center;cursor:pointer;box-shadow:0 6px 18px rgba(0,0,0,.16);
    opacity:0;transition:opacity .25s}
  .sh-arrow.l{left:max(8px, calc(var(--g) - 22px))}.sh-arrow.r{right:max(8px, calc(var(--g) - 22px))}
  .shelf:hover .sh-arrow,.sh-arrow:focus-visible{opacity:1}
  .sh-arrow[hidden]{display:none}
  .sh-arrow:focus-visible{outline:3px solid var(--red);outline-offset:3px}

  /* promo banner */
  .promo{position:relative;display:block;margin:clamp(48px,6vw,80px) var(--g) 0;border-radius:22px;overflow:hidden;color:#fff;
    min-height:clamp(300px,30vw,440px);background:#111}
  .promo img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform 1.4s var(--ease)}
  .promo:hover img{transform:scale(1.03)}
  .promo::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(0,0,0,.72) 0%,rgba(0,0,0,.25) 50%,transparent 75%)}
  .promo-in{position:relative;z-index:2;padding:clamp(28px,4vw,60px);max-width:560px}
  .promo-in h2{font-size:clamp(44px,5.4vw,84px);font-weight:700;letter-spacing:-.045em;line-height:.92}
  .promo-in p{margin-top:14px;font-size:18px;line-height:1.45;color:rgba(255,255,255,.9)}
  .promo-row{display:flex;gap:12px;margin-top:22px;flex-wrap:wrap}
  .promo-row span{display:inline-flex;align-items:center;height:46px;padding:0 24px;border-radius:999px;background:#fff;color:#1D1D1F;font-weight:600;font-size:16px}

  /* browse grid */
  .browse{padding:0 var(--g);display:grid;grid-template-columns:repeat(4,1fr);gap:var(--gap)}
  .browse .tile .art{aspect-ratio:16/10}
  .browse .art::after{content:"";position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,.7),transparent 60%)}
  .browse .bt{position:absolute;left:16px;bottom:14px;z-index:2;color:#fff;font-size:clamp(18px,1.6vw,24px);font-weight:700;letter-spacing:-.02em}
  .page-end{height:clamp(70px,9vw,120px)}

  @media (max-width:1100px){.strip.land{--cols:3}.strip.poster{--cols:4}.strip.chan{--cols:4}.strip.film{--cols:2}.browse{grid-template-columns:repeat(2,1fr)}}
  @media (max-width:700px){
    :root{--gap:12px}
    .strip.land{--cols:1.35}.strip.poster{--cols:2.3}.strip.chan{--cols:1.8}.strip.film{--cols:1.2}
    .stage-arrow,.sh-arrow{display:none}
    .slide{height:62svh}
    .browse{grid-template-columns:1fr 1fr}
  }
  @media (prefers-reduced-motion: reduce){
    .stage-track.anim,.slide,.slide-in,.art,.dot{transition:none}
  }
"""

ICON_L = '<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_R = '<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def h(x): return (x or "").replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")
def cb(t, img, u, tag=""):
    return h(json.dumps({"t": t, "img": img or "", "u": u, "tag": tag}, ensure_ascii=False))

def art_img(img, t, sub=""):
    if img: return f'<img src="{img}" alt="" loading="lazy">'
    return f'<span class="typo"><b>{h(t)}</b>{f"<small>{h(sub)}</small>" if sub else ""}</span>'

def tile(t, img, u, sub="", tag=""):
    return (f'<a class="tile" href="{u}" data-cb="{cb(t, img, u, tag)}"><span class="art">{art_img(img, t)}</span>'
            f'<span class="cap-t">{h(t)}</span>' + (f'<span class="cap-s">{h(sub)}</span>' if sub else "") + '</a>')

def shelf(sid, title, kind, tiles, href=None, sub=None, hidden=False):
    link = f'<a class="sh-all" href="{href}">See all</a>' if href else ""
    subp = f"<p>{h(sub)}</p>" if sub else ""
    hid = " hidden" if hidden else ""
    return (f'<section class="shelf" id="{sid}"{hid} aria-label="{h(title)}">\n'
            f'  <div class="sh-head"><div><h2>{h(title)}</h2>{subp}</div>{link}</div>\n'
            f'  <button class="sh-arrow l" hidden aria-label="Scroll {h(title)} back">{ICON_L}</button>'
            f'<button class="sh-arrow r" aria-label="Scroll {h(title)} forward">{ICON_R}</button>\n'
            f'  <div class="strip {kind}">' + "".join(tiles) + '</div>\n</section>\n')

pillar_tiles = [tile(p["t"], p["img"], p["u"], p["line"]) for p in PILLARS]
chan_tiles = [(f'<a class="tile" href="{u}" data-cb="{cb(full, None, u, "College")}"><span class="art"><span class="typo">'
               f'<img src="{MONO}" alt=""><span><b>{h(short)}</b><small>{h(full)}</small></span></span></span></a>')
              for short, full, u in COLLEGES]
film_tiles = [(f'<a class="tile" href="{f["u"]}" data-cb="{cb(f["t"], f["img"], f["u"], "Film")}"><span class="art">'
               f'<img src="{f["img"]}" alt="" loading="lazy"><video muted loop playsinline preload="none" src="{f["film"]}"></video></span>'
               f'<span class="cap-t">{h(f["t"])}</span><span class="cap-s">{h(f["s"])}</span></a>') for f in FILMS]
campus_tiles = [tile(n, img, u, "Campus" if img else "Campus") for n, img, u in CAMPUS_SITES]
campus_tiles = [tile(n, img, u, ("Northeastern campus" if n != "And nine more" else "Across the U.S., U.K., and Canada"))
                for n, img, u in CAMPUS_SITES]
coop_tiles = [tile(s["t"], s["img"], s["u"], s["tag"]) for s in COOP_STORIES]
research_tiles = [tile(s["t"], s["img"], s["u"], s["tag"]) for s in RESEARCH_STORIES]
sport_tiles = [tile(s["t"], s["img"], s["u"], s["tag"]) for s in ATHLETICS_STORIES]
top_tiles = [tile(s["t"], s["img"], s["u"], "") for s in SNAP["latest"][:12]]
browse = "".join(f'<a class="tile" href="{p["u"]}" data-cb="{cb(p["t"], p["img"], p["u"], "Browse")}"><span class="art">{art_img(p["img"], "", "") if p["img"] else "<span class=typo></span>"}'
                 f'<span class="bt">{h(p["t"])}</span></span></a>' for p in PILLARS)

BODY = f'''
<section class="stage" id="top" aria-label="Featured">
  <div class="stage-vp"><div class="stage-track" id="stTrack"></div></div>
  <button class="stage-arrow l" id="stPrev" aria-label="Previous feature">{ICON_L}</button>
  <button class="stage-arrow r" id="stNext" aria-label="Next feature">{ICON_R}</button>
  <div class="dots" id="stDots" role="group" aria-label="Choose a feature"></div>
</section>

{shelf("shContinue", "Up next for you", "land", [], sub="Pick up where you left off.", hidden=True)}
{shelf("shStart", "Start here", "land", pillar_tiles, sub="The whole of Northeastern, one pillar at a time.")}
{shelf("shChan", "Channels", "chan", chan_tiles, href="https://www.northeastern.edu/academics/", sub="Nine colleges. Browse by the one that fits.")}
{shelf("shFilms", "Films", "film", film_tiles)}
{shelf("shCampus", "Around the network", "poster", campus_tiles, href="https://www.northeastern.edu/campuses/")}

<a class="promo" href="https://admissions.northeastern.edu/" data-cb="{cb("Apply to Northeastern", P["admissions"]["img"], "https://admissions.northeastern.edu/", "Admissions")}">
  <img src="{P["admissions"]["img"]}" alt="" loading="lazy">
  <div class="promo-in"><h2>Your turn.</h2><p>Four campuses to start from, and a world to work in after that.</p>
  <div class="promo-row"><span>Start your application</span></div></div>
</a>

{shelf("shTop", "Top stories", "land", top_tiles, href=NGN + "/", sub="Live from Northeastern Global News.")}
{shelf("shCoop", "On the job", "poster", coop_tiles, href=P["coop"]["u"], sub="Co‑op stories from all over the map.")}
{shelf("shResearch", "Research", "land", research_tiles, href=P["research"]["u"])}
{shelf("shSport", "Huskies", "land", sport_tiles, href="https://gonu.com/")}

<section class="shelf" aria-label="Browse Northeastern">
  <div class="sh-head"><div><h2>Browse Northeastern</h2></div></div>
  <div class="browse">{browse}</div>
</section>
<div class="page-end"></div>
'''

JS = SHARED_JS + r"""
/* ============ concept 8: center stage ============ */
const STAGE = """ + jsdata(STAGE_DATA) + r""";
const MONO = """ + jsdata(MONO) + r""";
const stTrack = $("#stTrack"), stDots = $("#stDots");
const ST_N = STAGE.length, ST_MS = 7000;
const slideHTML = (s, clone) =>
  `<a class="slide" href="${esc(s.u)}" ${clone ? 'aria-hidden="true" tabindex="-1"' : `data-cb="${cbAttr({ t: s.t, img: s.img, u: s.u, tag: "Featured" })}"`}>` +
  `<img src="${esc(s.img)}" alt="">` + (!clone && s.big ? `<video muted loop playsinline preload="none" data-src="${esc(s.big)}"></video>` : "") +
  `<span class="slide-in"><span class="brandchip"><img src="${MONO}" alt=""><span>Northeastern<b>+</b></span></span>` +
  `<span class="slide-t">${esc(s.t)}</span><span class="slide-l">${esc(s.line)}</span>` +
  `<span class="slide-cta">${esc(s.cta)}</span></span></a>`;
stTrack.innerHTML = slideHTML(STAGE[ST_N - 1], true) + STAGE.map(s => slideHTML(s, false)).join("") + slideHTML(STAGE[0], true);
stDots.innerHTML = STAGE.map((s, i) => `<button class="dot" aria-label="${esc(s.t)}"><i></i></button>`).join("");
const slides = [...stTrack.children], dots = [...stDots.children];
let stIdx = 1, stTimer = null, stHover = false, stVisible = true;
const real = i => (i - 1 + ST_N) % ST_N;
function stLayout(anim) {
  const vw = document.documentElement.clientWidth;
  const sw = Math.min(vw * (vw < 700 ? .9 : .84), 1400);
  document.documentElement.style.setProperty("--sw", sw + "px");
  stTrack.classList.toggle("anim", !!anim && !reduceMotion);
  stTrack.style.transform = `translateX(${(vw - sw) / 2 - stIdx * (sw + 20)}px)`;
  const r = real(stIdx);
  slides.forEach((s, j) => s.classList.toggle("on", real(j) === r));
  dots.forEach((d, j) => { d.classList.toggle("on", j === r); d.setAttribute("aria-current", j === r ? "true" : "false"); });
}
function stVideos() {
  slides.forEach(s => { const v = s.querySelector("video"); if (v && !s.classList.contains("on")) { v.pause(); v.classList.remove("live"); } });
  const act = slides[stIdx], v = act && act.querySelector("video");
  if (!v || reduceMotion || !stVisible) return;
  setTimeout(() => {
    if (slides[stIdx] !== act) return;
    if (!v.src) v.src = v.dataset.src;
    v.addEventListener("timeupdate", function f() { if (v.currentTime > .15) { v.classList.add("live"); v.removeEventListener("timeupdate", f); } });
    v.play().catch(() => {});
  }, 900);
}
function stArm() {
  clearTimeout(stTimer);
  dots.forEach(d => d.classList.remove("run"));
  if (reduceMotion || stHover || !stVisible) return;
  const d = dots[real(stIdx)];
  d.style.setProperty("--dur", ST_MS + "ms");
  void d.offsetWidth; d.classList.add("run");
  stTimer = setTimeout(() => stGo(stIdx + 1), ST_MS);
}
function stGo(i) {
  stIdx = i;
  stLayout(true);
  stArm();
  if (reduceMotion) stSettle();
}
function stSettle() {
  if (stIdx === 0) { stIdx = ST_N; stLayout(false); }
  else if (stIdx === ST_N + 1) { stIdx = 1; stLayout(false); }
  stVideos();
}
stTrack.addEventListener("transitionend", e => { if (e.target === stTrack) stSettle(); });
$("#stNext").addEventListener("click", () => stGo(stIdx + 1));
$("#stPrev").addEventListener("click", () => stGo(stIdx - 1));
dots.forEach((d, j) => d.addEventListener("click", () => stGo(j + 1)));
slides.forEach((s, j) => s.addEventListener("click", e => {
  if (!s.classList.contains("on")) { e.preventDefault(); stGo(j); }
}));
const stage = $(".stage");
stage.addEventListener("mouseenter", () => { stHover = true; stArm(); });
stage.addEventListener("mouseleave", () => { stHover = false; stArm(); });
stage.addEventListener("focusin", () => { stHover = true; stArm(); });
stage.addEventListener("focusout", () => { stHover = false; stArm(); });
new IntersectionObserver(es => es.forEach(e => { stVisible = e.isIntersecting; stArm(); stVideos(); }), { threshold: .3 }).observe(stage);
addEventListener("resize", () => stLayout(false));
stLayout(false); stArm(); stVideos();

/* ============ shelves ============ */
function shelfArrows(sh) {
  const strip = sh.querySelector(".strip"), l = sh.querySelector(".sh-arrow.l"), r = sh.querySelector(".sh-arrow.r");
  if (!strip || !l) return;
  const upd = () => {
    l.hidden = strip.scrollLeft < 8;
    r.hidden = strip.scrollLeft + strip.clientWidth >= strip.scrollWidth - 8;
  };
  const step = dir => {
    const first = strip.firstElementChild;
    const w = first ? first.getBoundingClientRect().width + 18 : 300;
    const n = Math.max(1, Math.floor((strip.clientWidth - 2 * parseFloat(getComputedStyle(strip).paddingLeft)) / w));
    strip.scrollBy({ left: dir * n * w, behavior: reduceMotion ? "auto" : "smooth" });
  };
  l.onclick = () => step(-1); r.onclick = () => step(1);
  strip.addEventListener("scroll", () => requestAnimationFrame(upd), { passive: true });
  addEventListener("resize", upd);
  upd();
}
$$(".shelf").forEach(shelfArrows);

/* hover-play films */
$$(".film .tile").forEach(t => {
  const v = t.querySelector("video");
  v.addEventListener("timeupdate", () => { if (v.currentTime > .15) v.classList.add("live"); });
  t.addEventListener("mouseenter", () => { if (reduceMotion) return; if (!v.dataset.l) { v.dataset.l = 1; v.load(); } v.play().catch(() => {}); });
  t.addEventListener("mouseleave", () => { v.pause(); v.classList.remove("live"); });
});

/* up next (continue browsing) */
const tileHTML = it => `<a class="tile" href="${esc(it.u)}" data-cb="${cbAttr(it)}"><span class="art">` +
  (it.img ? `<img src="${esc(it.img)}" alt="" loading="lazy">` : `<span class="typo"><b>${esc(it.t)}</b></span>`) +
  `</span><span class="cap-t">${esc(it.t)}</span>${it.tag ? `<span class="cap-s">${esc(it.tag)}</span>` : ""}</a>`;
const seen = cbRead().slice(0, 12);
if (seen.length) {
  const sh = $("#shContinue");
  sh.querySelector(".strip").innerHTML = seen.map(tileHTML).join("");
  sh.hidden = false;
  shelfArrows(sh);
}

/* top stories: live refresh */
(async () => {
  try {
    const items = await ngnFetch(null, 14);
    if (items.length < 4) return;
    const sh = $("#shTop");
    sh.querySelector(".strip").innerHTML = items.map(x => tileHTML(Object.assign(x, { tag: fmtDate(x.d) }))).join("");
    shelfArrows(sh);
  } catch (e) { /* snapshot remains */ }
})();
"""

html = page("concept8", 1, CSS, BODY, JS)
for tok in ["stTrack", "shChan", "shFilms", "Khoury", "Your turn.", "nu-stream-continue", "Browse Northeastern"]:
    assert tok in html, tok
write("concept-8", html)
