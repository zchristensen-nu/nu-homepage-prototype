"""Concept 10: immersive streaming. The page opens on a full-bleed billboard
(per-feature film, synopsis, stories panel) over an "Only at Northeastern"
row of portrait feature cards; then live NGN rows (a static featured card,
then portrait posters, Netflix-style edge paddles); concept 2's scroll-driven
globe tour, research sheet and co-op rail; concept 4's portrait video reel;
concept 2's portrait quotes; and v1's "Your turn." closer. Keeps the v1 nav,
footer and brand. Deploys to concept-10/ (concept-7 belongs to the streaming concepts 7-9 build)."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = [os.path.join(ROOT, "concept-10/index.html")]

# ponytail: reuse build_c8's extraction (nav, footer, show data) by running its prefix;
# if build_c8 is restructured, lift the extraction into a shared module then.
_c8 = open(os.path.join(HERE, "build_c8.py")).read()
_pre = _c8.split("S0 = SHOWS[0]")[0]
assert "def cut(" in _pre and "SHOWS = [" in _pre
g = {}
exec(_pre, g)
head, nav_css, overlay_css, tailcss = (g[k] for k in ("head", "nav_css", "overlay_css", "tailcss"))
header_mk, footer_mk, lenis_js, rest_mk = g["header_mk"], g["footer_mk"], g["lenis"], g["rest_mk"]
land, coops, helpers, tail_js = (g[k] for k in ("land", "coops", "helpers", "tail_js"))
SHOWS, MONO, NGN_LOGO, h, NGN, U, ep = g["SHOWS"], g["MONO"], g["NGN_LOGO"], g["h"], g["NGN"], g["U"], g["ep"]

assert head.count('<meta name="concept6-rev" content="4">') == 1
head = head.replace('<meta name="concept6-rev" content="4">', '<meta name="concept10-rev" content="1">')

# expose Lenis (handy for scripted checks; anchors already route through it)
assert tail_js.count("const lenis = new Lenis({ lerp: 0.12 });") == 1
tail_js = tail_js.replace("const lenis = new Lenis({ lerp: 0.12 });", "const lenis = window.lenis = new Lenis({ lerp: 0.12 });")

def cut_from(src, a, b, inclusive_b=False):
    i = src.find(a); assert i >= 0, a[:60]
    j = src.find(b, i + len(a)); assert j > i, b[:60]
    return src[i:j + (len(b) if inclusive_b else 0)]

# concept 2 (built page): globe tour, research sheet, co-op rail, portrait quotes
C2 = open(os.path.join(ROOT, "concept-2/index.html")).read()
c2_css = (cut_from(C2, "  /* ---------- GLOBE SCROLLY ---------- */", "  .srch{")
          + cut_from(C2, "  /* ---------- SHEET SECTIONS (Adobe pattern) ---------- */", "  /* ---------- award layer ---------- */")
          + cut_from(C2, "  .line{display:block;overflow:hidden}", "  /* ---------- NGN wire ---------- */").replace(".grain{animation:none}", "")
          + cut_from(C2, "  /* ---------- co-op rail ---------- */", "  /* ---------- STUDENT LIFE IMAX ---------- */"))
globe_mk  = cut_from(C2, '<div class="scrolly" id="experience">', '<div class="sheet">')
globe_mk  = globe_mk.replace('<div class="scrolly" id="experience">', '<div class="scrolly" id="campuses">')
sheet_mk  = cut_from(C2, '<div class="sheet">', '<section class="voices-c"')
c2_js = (cut_from(C2, "/* ============ globe data ============ */", "/* ============ research counters ============ */")
         + cut_from(C2, "/* ============ research counters ============ */", "/* ============ live NGN wire")
         + cut_from(C2, "/* ============ co-op rail ============ */", "/* ============ subtle scroll movement ============ */"))
assert 'id="coop"' in sheet_mk and 'id="research"' in sheet_mk
COPY = [
 (globe_mk, "Northeastern's 14 campuses, 8 N.U.in locations, and 4,705 Fall 2026 co‑op placements. Scroll for the tour, click a red pin for a story, drag to rotate.",
            "Northeastern’s 14 campuses, eight N.U.in locations, and this fall’s co‑op locations. Scroll for the tour, select a red pin for a story, drag to rotate."),
 (globe_mk, "<p>A connected network of campuses across the U.S., U.K., and Canada, where each one opens doors to all the others.</p>",
            "<p>One network across the U.S., U.K., and Canada. No single campus sits at the center.</p>"),
 (globe_mk, "<p>Through N.U.in, new students begin their Northeastern degree at one of eight partner institutions across Europe.</p>",
            "<p>Through N.U.in, new students begin their Northeastern degree at a partner institution in Europe.</p>"),
 (globe_mk, "</b> co‑op placements</div>", "</b> co‑ops</div>"),
 (globe_mk, "<p>Full-time, paid positions in every kind of workplace.</p>",
            "<p>More than a century of students working with employer partners around the world. Each dot is a city where a student is on co‑op this fall.</p>"),
 (globe_mk, '<div class="big">And co‑op is only the start.</div><p>Research, service, global study: experience runs through the whole degree.</p>',
            '<div class="big">Co‑op is one part.</div><p>Experiential learning at Northeastern also includes research with faculty, service with community partners, and study abroad on Dialogue of Civilizations programs.</p>'),
 (sheet_mk, "patents and counting", "patents"),
 (sheet_mk, '<span class="g-n">5,000+</span><span class="g-l">cities and towns</span>', '<span class="g-n">3,900+</span><span class="g-l">employer partners worldwide</span>'),
 (sheet_mk, '<span class="g-n">10,000+</span><span class="g-l">employer partners</span>', '<span class="g-n">100+</span><span class="g-l">years of co‑op</span>'),
 (sheet_mk, '<span class="g-n">250+</span><span class="g-l">countries and territories</span>', '<span class="g-n">350K+</span><span class="g-l">alumni around the world</span>'),
 (sheet_mk, ">Research coverage on NGN<", ">More research on NGN<"),
]
fixed = {}
for src_name, a, b in [("globe_mk" if blk is globe_mk else "sheet_mk", a, b) for blk, a, b in COPY]:
    blk = globals()[src_name]
    assert blk.count(a) == 1, a[:70]
    globals()[src_name] = blk.replace(a, b)
assert c2_js.count("const COOP_DISPLAY_TOTAL = 500000;") == 1
_t = '<b>${fmt(best[2])}</b> co‑op placement${best[2] === 1 ? "" : "s"}`'
assert c2_js.count(_t) == 1
c2_js = c2_js.replace(_t, '<b>${fmt(best[2])}</b> co‑op${best[2] === 1 ? "" : "s"} this fall`')
# the co-op beat counts concept 2's all-time figure (500,000): an unverified placeholder, VERIFY before external use
c2_js = c2_js.replace("/* all-time placements, VERIFY before external use */", "/* all-time co-ops, VERIFY before external use */")

# the portrait reel (concept 4's idea): b-roll clips from seven university films, each card
# looping its own segment. Segments picked from sampled frames on 2026-09-30; the co-op
# and Jamie Wong films are mostly interviews, so they contribute at most one clip.
FILM = {
 "adm":  "https://admissions.northeastern.edu/wp-content/uploads/2023/08/07.21.26_UG-Website-Hero-Video.mp4",
 "dmsb": "https://damore-mckim.northeastern.edu/wp-content/uploads/2026/03/dmsb-hero-noaudio.webm",
 "res":  "https://research.northeastern.edu/wp-content/uploads/2024/06/VID_Homepage-Hero_Small.mp4",
 "lon":  "https://www.nulondon.ac.uk/wp-content/uploads/2026/02/Discover-your-path-at-Northeastern-University-London.mp4",
 "nyc":  "https://nyc.northeastern.edu/wp-content/uploads/NYC-Home_SLOW.mp4",
 "roux": "https://roux.northeastern.edu/wp-content/uploads/MAGGIE-VIDEO-4-2.mp4",
 "coop": "https://www.northeastern.edu/wp-content/uploads/The-Co-Op-Experience_Video-2-Fusion-v3.mp4",
 "hero": "../hero.mp4",
}
CLIPS = [("adm", .5, 6), ("res", .5, 6), ("lon", 24, 29.5), ("dmsb", 8.5, 14), ("hero", 0, 9), ("adm", 7, 11.5),
         ("nyc", 0, 9), ("res", 6.5, 9.5), ("lon", 55, 62), ("dmsb", 31, 36), ("adm", 30, 36), ("coop", 7.5, 9.5),
         ("res", 16, 19.5), ("lon", 3, 9), ("adm", 13, 18), ("roux", 1, 7)]
reel_mk = ('<section class="reel" aria-hidden="true"><div class="reel-track" id="reelTrack">'
           + "".join(f'<div class="vidcard"><video muted playsinline preload="none" data-src="{FILM[f]}" data-s="{a}" data-e="{b}"></video></div>' for f, a, b in CLIPS)
           + "</div></section>\n")

admit_mk = rest_mk[:rest_mk.index("</section>") + len("</section>")]
_a = "<p>First-year, transfer, graduate, online, or start abroad with N.U.in. However you get here, experience starts on day one.</p>"
assert admit_mk.count(_a) == 1
admit_mk = admit_mk.replace("<h2>Your turn.</h2>", "<h2>Your turn.</h2>").replace(_a,
    "<p>The world doesn’t wait. Neither do you. Undergraduate, graduate, transfer, and online programs across our campus network.</p>")
for a, b in (('<a class="pill red" href="#">Apply</a>', '<a class="pill red" href="https://admissions.northeastern.edu/">Apply</a>'),
             ('<a class="pill ghostw" href="#">Visit</a>', '<a class="pill ghostw" href="https://admissions.northeastern.edu/visit/">Visit</a>'),
             ('<a class="pill ghostw" href="#">Request info</a>', '<a class="pill ghostw" href="https://studentfinance.northeastern.edu/">Financial aid</a>')):
    assert admit_mk.count(a) == 1, a
    admit_mk = admit_mk.replace(a, b)

# features: Co-op, Research, Global network, Admissions (student life + athletics), Entrepreneurship
S = {s["title"]: s for s in SHOWS}
EP_ENT = [
 ep("Student startup develops hands-on learning toy for future engineers", U+"/2026/07/072426_MM_NextTile_002.jpg", NGN+"/2026/07/31/nexttile-startup-stem-northeastern/"),
 ep("Founders pitch startups in Dragons’ Den-style event for funding", U+"/2026/06/060426_CV_GLS_day1_048.jpg", NGN+"/2026/06/05/startup-pitch-competition-london-summit/"),
 ep("Revolutionizing dental hygiene, starting with your toothbrush", U+"/2025/08/NOOK_1400.jpg", NGN+"/2026/07/15/how-to-keep-toothbrush-clean-nook/"),
 ep("Is this healthy energy drink coming to a store near you?", U+"/2026/03/033126_MM_The_Market_031.jpg", NGN+"/2026/04/10/healthy-energy-drink-journee/"),
]
def feat(t, src, v=None, still=None, card=None, **kw):
    s = S[src] if src else {}
    return {"t": t, "v": v, "img": still or s.get("still") or s.get("thumb"), "card": card or s.get("thumb"),
            "syn": kw["syn"],
            "cta": kw.get("cta", s.get("cta")), "eps": kw.get("eps", s.get("eps", []))[:4]}
# copy: brand voice (trusted, empowering, confident), brand facts only. Co-op numbers from the
# key-terms entry; network numbers from the boilerplate; research line from the research messaging page.
FEATS = [
 feat("Co‑op", "Co‑op", v="../coop-sm.mp4", card="../img/aquarium-dive.jpg",
      syn="Up to three co‑ops, each up to six months of full-time work with an employer partner in your field. More than nine out of 10 undergraduates do at least one.",
      cta={"label": "Explore co‑op", "href": "https://www.northeastern.edu/co-op"}),
 feat("Research", "Research", v="../hero-sm.mp4",
      syn="Faculty and students advance work in health, security, and sustainability with partners in industry, government, and communities. Undergraduates join labs early.",
      cta={"label": "Explore research", "href": "https://research.northeastern.edu/"}),
 feat("Global network", "Global network", v=S["Global network"]["video"],
      syn="Our network spans 14 campuses across the U.S., U.K., and Canada and more than 3,900 partners worldwide. Start on one campus and follow opportunities across all of them.",
      cta={"label": "See the network", "href": "#campuses"}),
 feat("Admissions", "Your turn.", v="../jamie-sm.mp4", card=U+"/2026/09/090826_MM_convocation_147.jpg",
      syn="Start your degree in Boston, London, New York City, or Oakland, or begin abroad with N.U.in. Come see a campus for yourself.",
      cta={"label": "Apply", "href": "https://admissions.northeastern.edu/"},
      eps=[g["EP_LIFE"][1], g["EP_LIFE"][2], g["EP_ATHLETICS"][0], g["EP_ATHLETICS"][1]]),
 feat("Entrepreneurship", None, still=U+"/2026/06/060426_CV_GLS_day1_048.jpg", card=U+"/2026/07/072426_MM_NextTile_002.jpg",
      syn="Entrepreneurship spans the world. Student founders build ventures, test them with customers, and pitch them for funding.",
      cta={"label": "Read founder stories", "href": NGN + "/tag/entrepreneurship/"}, eps=EP_ENT),
]
assert len(FEATS) == 5 and all(f["eps"] and f["img"] and f["card"] and f["cta"] for f in FEATS)

def layer(i, f):
    on = " on" if i == 0 else ""
    if f["v"]:
        return (f'<div class="hl{on}"><video muted loop playsinline preload="{"auto" if i == 0 else "none"}" '
                f'poster="{f["img"]}" src="{f["v"]}"></video></div>')
    return f'<div class="hl kb{on}"><img src="{f["img"]}" alt="" loading="lazy"></div>'

def show_card(i, f):
    return (f'<button class="ln" data-i="{i}" aria-pressed="{"true" if i == 0 else "false"}">'
            f'<img src="{f["card"]}" alt="" loading="lazy">'
            f'<span class="ln-t">{h(f["t"])}</span><i class="ln-pb"></i></button>')

F0 = FEATS[0]
HERO = f'''<section class="hx" id="top" aria-label="Featured">
  <div class="hx-media" id="hxMedia">{"".join(layer(i, f) for i, f in enumerate(FEATS))}</div>
  <div class="hx-shade"></div>
  <h1 class="vh">Northeastern University</h1>
  <div class="hx-in" id="hxIn">
    <div class="hx-copy" aria-live="polite">
      <h2 class="hx-title" id="hxTitle">{h(F0["t"])}</h2>
      <p class="hx-syn" id="hxSyn">{h(F0["syn"])}</p>
      <a class="hx-btn" id="hxCta" href="#" hidden><span id="hxCtaL"></span>{g["ICON_ARROW"]}</a>
    </div>
    <aside class="hx-eps" id="hxEps" aria-label="Stories from this feature"></aside>
  </div>
  <div class="hx-shows" id="hxShows">
    <h2 class="hx-sh">Only at Northeastern</h2>
    <div class="hx-lineup" role="group" aria-label="Choose a feature">{"".join(show_card(i, f) for i, f in enumerate(FEATS))}</div>
  </div>
</section>
'''

CHEV = '<svg width="30" height="30" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def row(rid, label, q=None, hidden=True):
    dq = f' data-q="{q}"' if q is not None else ""
    return (f'<section class="crow"{" hidden" if hidden else ""}{dq} id="{rid}" aria-label="{label}">'
            f'<div class="wrap"><h3>{label}</h3></div><div class="crow-body">'
            f'<button class="pad prev" aria-label="Scroll {label} back" disabled>{CHEV}</button>'
            f'<div class="crow-strip"></div>'
            f'<button class="pad next" aria-label="Scroll {label} forward">{CHEV}</button></div></section>\n')

ROWS = ('<section class="rows" aria-labelledby="rowsT">\n'
        '  <div class="wrap rows-head"><h2 id="rowsT">Stories from</h2><a href="https://news.northeastern.edu/" aria-label="Northeastern Global News">'
        + NGN_LOGO + '</a></div>\n'
        + row("ngnRow", "Latest", "", hidden=False)
        + row("entRow", "Entrepreneurship", "tags=9287")
        + row("aiRow", "AI", "tags=9865,9843")
        + row("uniRow", "University news", "categories=7")
        + row("researchRow", "Research", "categories=21443")
        + "</section>\n")

NEW_CSS = r'''
  /* ---------- concept-7: immersive streaming ---------- */
  body{background:var(--dark)}
  /* the .wrap content edge; % resolves against each full-width element's own box */
  :root{--edge:max(clamp(20px,4vw,48px), calc((100% - 1280px) / 2 + clamp(20px,4vw,48px)))}
  ::selection{background:var(--red);color:#fff}
  .vh{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
  .vidcard{position:relative;border-radius:14px;overflow:hidden;background:#141419}
  .vidcard video{width:100%;height:100%;object-fit:cover;display:block}

  /* billboard */
  .hx{position:relative;height:100svh;min-height:760px;overflow:hidden;color:#fff;background:#000}
  .hx-media{position:absolute;inset:0;will-change:transform}
  .hl{position:absolute;inset:0;opacity:0;transition:opacity 1s var(--ease)}
  .hl.on{opacity:1}
  .hl video,.hl img{width:100%;height:100%;object-fit:cover;display:block}
  .hl.kb.on img{animation:kb 24s ease-in-out infinite alternate}
  @keyframes kb{from{transform:scale(1)}to{transform:scale(1.1) translate(-1.5%,-1%)}}
  .hx-shade{position:absolute;inset:0;pointer-events:none;
    background:linear-gradient(to right,rgba(11,11,14,.78) 0%,rgba(11,11,14,.3) 38%,transparent 62%),
               linear-gradient(to top,var(--dark) 0%,rgba(11,11,14,.72) 34%,transparent 62%)}
  /* the copy and the stories panel sit a full breath above the feature row */
  .hx-in{position:absolute;z-index:2;left:0;right:0;bottom:calc(var(--shh,280px) + clamp(56px,9svh,110px));
    display:flex;align-items:flex-end;justify-content:space-between;gap:48px;padding:0 var(--edge)}
  .hx-copy,.hx-eps{transition:opacity .35s var(--ease)}
  .hx-in.swap .hx-copy,.hx-in.swap .hx-eps{opacity:0}
  .hx-copy{flex:1 1 auto;min-width:0;max-width:640px}
  .hx-title{margin:0;font-size:clamp(56px,7.4vw,124px);font-weight:200;letter-spacing:-.04em;line-height:.92;white-space:nowrap}
  .hx-syn{margin:18px 0 0;font-size:clamp(16px,1.25vw,19px);line-height:1.5;color:#E5E5E5;max-width:44ch}
  .hx-btn{all:unset;box-sizing:border-box;display:inline-flex;align-items:center;gap:10px;height:48px;padding:0 24px;margin-top:22px;
    border-radius:999px;font-size:16px;font-weight:600;cursor:pointer;background:#fff;color:#0B0B0E;transition:background .2s}
  .hx-btn:hover{background:rgba(255,255,255,.84)}
  .hx-btn[hidden]{display:none}
  .hx-btn:focus-visible,.ln:focus-visible,.cc:focus-visible,.pad:focus-visible{outline:2px solid #fff;outline-offset:3px}
  .hx-eps{width:min(360px,32%);flex:0 0 auto}
  .hx-eps h3{margin:0 0 4px;font-size:17px;font-weight:600}
  .ep{display:grid;grid-template-columns:104px 1fr;gap:14px;align-items:center;padding:7px;border-radius:12px;color:#fff;
    background:rgba(20,20,26,.55);backdrop-filter:blur(14px);margin-top:8px;transition:background .2s}
  .ep:hover{background:rgba(255,255,255,.14)}
  .ep img{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:7px}
  .ep span{font-size:14px;line-height:1.35}

  /* "Only at Northeastern": portrait feature cards */
  .hx-shows{position:absolute;z-index:3;left:0;right:0;bottom:clamp(18px,3svh,36px)}
  .hx-sh{margin:0;padding:0 var(--edge);font-size:clamp(17px,1.35vw,20px);font-weight:600;color:#E5E5E5}
  .hx-lineup{display:flex;gap:12px;overflow-x:auto;scrollbar-width:none;padding:14px var(--edge) 6px}
  .hx-lineup::-webkit-scrollbar{display:none}
  .ln{all:unset;box-sizing:border-box;cursor:pointer;position:relative;flex:1 1 0;min-width:0;height:clamp(180px,26svh,270px);
    border-radius:8px;overflow:hidden;background:#141419;transition:transform .35s var(--ease),box-shadow .35s var(--ease)}
  .ln img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.62) saturate(.85);transition:filter .35s}
  .ln::after{content:"";position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,.72) 0%,transparent 48%)}
  .ln-t{position:absolute;z-index:2;left:10px;right:10px;bottom:11px;font-size:clamp(19px,1.6vw,25px);font-weight:400;line-height:1;
    letter-spacing:-.02em;color:#fff;text-shadow:0 2px 12px rgba(0,0,0,.45)}
  .ln:hover{transform:translateY(-4px)}
  .ln:hover img{filter:brightness(.9)}
  .ln[aria-pressed="true"]{transform:translateY(-8px);box-shadow:0 0 0 2px #fff,0 18px 40px rgba(0,0,0,.6)}
  .ln[aria-pressed="true"] img{filter:none}
  .ln-pb{position:absolute;z-index:3;left:0;bottom:0;height:3px;width:calc(var(--pb,0) * 100%);background:var(--red)}
  @media (max-width:899px){.hx-eps{display:none}}
  @media (max-width:640px){.hx{min-height:700px}.hx-btn{height:44px;padding:0 18px;font-size:15px}.ln{flex:0 0 118px;height:177px}}
  @media (prefers-reduced-motion: reduce){.hl,.hx-copy,.hx-eps,.ln{transition:none}.hl.kb.on img{animation:none}}

  /* rows: a featured card, then portrait posters; edge paddles scroll */
  .rows{position:relative;z-index:2;color:#fff;padding:clamp(40px,7svh,80px) 0 clamp(60px,9svh,110px)}
  .rows-head{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
  .rows-head h2{margin:0;font-size:clamp(22px,2vw,30px);font-weight:600;letter-spacing:-.015em}
  .rows-head .w-logo{height:24px;width:auto;display:block}
  .crow{margin-top:clamp(28px,4.4svh,50px);--ch:clamp(280px,23vw,360px);--pw:calc(var(--ch) * 2 / 3)}
  .crow[hidden]{display:none}
  .crow h3{margin:0;font-size:clamp(17px,1.4vw,21px);font-weight:600;color:#E5E5E5}
  .crow-body{position:relative}
  .crow-strip{display:flex;gap:12px;overflow-x:auto;scrollbar-width:none;padding:14px var(--edge) 14px;scroll-padding-inline:var(--edge)}
  .crow-strip::-webkit-scrollbar{display:none}
  .cc{position:relative;flex:0 0 auto;width:var(--pw);height:var(--ch);border-radius:10px;overflow:hidden;background:#141419;color:#fff}
  .cc img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .6s var(--ease),filter .4s}
  .cc:hover img{transform:scale(1.04);filter:brightness(1.08)}
  .cc::after{content:"";position:absolute;inset:0;pointer-events:none;
    background:linear-gradient(to top,rgba(0,0,0,.94) 0%,rgba(0,0,0,.72) 28%,rgba(0,0,0,.2) 55%,transparent 72%)}
  .cc-t{position:absolute;z-index:2;left:0;right:0;bottom:0;padding:0 16px 18px;font-size:clamp(15px,1.12vw,18px);font-weight:600;
    line-height:1.2;letter-spacing:-.005em;text-wrap:balance;text-shadow:0 1px 10px rgba(0,0,0,.6)}
  .pad{position:absolute;z-index:3;top:14px;bottom:14px;width:max(52px, calc(var(--edge) - 8px));border:0;padding:0;cursor:pointer;color:#fff;
    display:flex;align-items:center;justify-content:center;opacity:0;transition:opacity .25s}
  .pad.prev{left:0;background:linear-gradient(to right,rgba(11,11,14,.92),rgba(11,11,14,.5) 70%,transparent)}
  .pad.next{right:0;background:linear-gradient(to left,rgba(11,11,14,.92),rgba(11,11,14,.5) 70%,transparent)}
  .pad.prev svg{transform:scaleX(-1)}
  .pad svg{transition:transform .25s var(--ease)}
  .pad.next:hover svg{transform:scale(1.25)}
  .pad.prev:hover svg{transform:scaleX(-1) scale(1.25)}
  .crow-body:hover .pad:not(:disabled),.pad:focus-visible{opacity:1}
  .pad:disabled{visibility:hidden}
  @media (hover:none){.pad{display:none}}

  /* the reel: portrait b-roll drifting left to right */
  .reel{position:relative;z-index:2;padding:clamp(90px,13svh,180px) 0;overflow:hidden}
  .reel-track{display:flex;gap:16px;width:max-content;will-change:transform}
  .reel .vidcard{flex:0 0 auto;height:min(66svh,740px);aspect-ratio:9/16}
  @media (max-width:820px){.reel{padding:clamp(56px,8svh,90px) 0}.reel .vidcard{height:70svh}}
  @media (prefers-reduced-motion: reduce){.reel{overflow-x:auto}}

  /* concept 2's globe: flush on this page, dissolving into its neighbors */
  .scrolly{border-radius:0;margin-top:0}
  .gt-card{right:var(--edge)}
  .stage::before,.stage::after{content:"";position:absolute;left:0;right:0;z-index:4;pointer-events:none}
  .stage::before{top:0;height:16svh;background:linear-gradient(var(--dark),transparent)}
  .stage::after{bottom:0;height:24svh;background:linear-gradient(transparent,var(--dark))}

'''

NEW_JS = r'''{
/* ============ concept-7 ============ */
const esc = s => String(s).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");
const FEATS = __FEATS__;

/* ============ billboard ============ */
const hx = $(".hx"), hxIn = $("#hxIn"), layers = $$(".hl"), lnBtns = $$(".ln");
let cur = 0, auto = !reduceMotion, elapsed = 0, hxVisible = true;
const vidOf = i => layers[i].querySelector("video");
const playI = i => { const v = vidOf(i); if (v && !reduceMotion) v.play().catch(() => {}); };
function fillHero(f) {
  $("#hxTitle").textContent = f.t;
  $("#hxSyn").textContent = f.syn;
  const cta = $("#hxCta");
  cta.hidden = !f.cta;
  if (f.cta) { cta.href = f.cta.href; $("#hxCtaL").textContent = f.cta.label; }
  $("#hxEps").innerHTML = `<h3>More from ${esc(f.t)}</h3>` + f.eps.map(e =>
    `<a class="ep" href="${esc(e.u)}"><img src="${esc(e.img)}" alt="" loading="lazy"><span>${esc(e.t)}</span></a>`).join("");
}
/* one title size for every feature: the largest at which the longest title fits the copy column,
   so switching features never changes the type size and Entrepreneurship never meets the panel */
function fitHeroTitle() {
  const t = $("#hxTitle"), keep = t.textContent;
  t.style.fontSize = "";
  let fs = parseFloat(getComputedStyle(t).fontSize);
  for (const f of FEATS) {
    t.textContent = f.t;
    while (fs > 32 && t.scrollWidth > t.clientWidth) { fs -= 2; t.style.fontSize = fs + "px"; }
  }
  t.textContent = keep;
}
function selectF(i, byUser) {
  if (byUser) auto = false;
  elapsed = 0;
  lnBtns.forEach((b, k) => { b.setAttribute("aria-pressed", k === i ? "true" : "false"); b.style.setProperty("--pb", 0); });
  if (i === cur) return;
  const from = cur; cur = i;
  layers[from].classList.remove("on"); layers[i].classList.add("on");
  playI(i);
  setTimeout(() => { const v = vidOf(from); if (v && from !== cur) v.pause(); }, 1000);
  hxIn.classList.add("swap");
  setTimeout(() => { fillHero(FEATS[i]); hxIn.classList.remove("swap"); }, reduceMotion ? 0 : 350);
}
lnBtns.forEach(b => b.addEventListener("click", () => selectF(+b.dataset.i, true)));
setInterval(() => {
  if (!auto || !hxVisible || document.hidden || scrollY > innerHeight * .3) return;
  elapsed += .1;
  lnBtns[cur].style.setProperty("--pb", (elapsed / 12).toFixed(3));
  if (elapsed >= 12) selectF((cur + 1) % FEATS.length, false);
}, 100);
new IntersectionObserver(es => es.forEach(e => {
  hxVisible = e.isIntersecting;
  const v = vidOf(cur);
  if (v) { if (hxVisible) playI(cur); else v.pause(); }
})).observe(hx);
/* card titles wrap by word; shrink only when a single word is wider than the card */
function fitTitles() {
  $$(".ln-t").forEach(t => {
    t.style.fontSize = "";
    let fs = parseFloat(getComputedStyle(t).fontSize);
    while (fs > 11 && t.scrollWidth > t.clientWidth) { fs -= .5; t.style.fontSize = fs + "px"; }
  });
}
const shows = $("#hxShows");
const layout = () => { fitTitles(); fitHeroTitle(); hx.style.setProperty("--shh", shows.offsetHeight + "px"); };
addEventListener("resize", layout);
document.fonts.ready.then(layout); layout();
/* leaving the billboard: the film eases back and the copy lets go */
if (!reduceMotion) {
  const media = $("#hxMedia");
  addEventListener("scroll", () => requestAnimationFrame(() => {
    const p = clamp01(scrollY / innerHeight);
    media.style.transform = `translateY(${(p * 90).toFixed(1)}px) scale(${(1 + p * .06).toFixed(4)})`;
    hxIn.style.opacity = (1 - p * 1.5).toFixed(3);
  }), { passive: true });
}
fillHero(FEATS[0]);
playI(0);

/* ============ rows: a featured card, then portrait posters ============ */
const card = c => `<a class="cc" href="${esc(c.u)}">` +
  `<img src="${esc(c.img)}" alt="" loading="lazy"><span class="cc-t">${esc(c.t)}</span></a>`;
function mountRow(sec, items) {
  const strip = sec.querySelector(".crow-strip"), prev = sec.querySelector(".pad.prev"), next = sec.querySelector(".pad.next");
  strip.innerHTML = items.map(card).join("");
  const sync = () => {
    prev.disabled = strip.scrollLeft < 4;
    next.disabled = strip.scrollLeft + strip.clientWidth >= strip.scrollWidth - 4;
  };
  const by = d => strip.scrollBy({ left: d * (strip.clientWidth - 2 * parseFloat(getComputedStyle(strip).paddingLeft)), behavior: reduceMotion ? "auto" : "smooth" });
  prev.onclick = () => by(-1); next.onclick = () => by(1);
  strip.addEventListener("scroll", () => requestAnimationFrame(sync), { passive: true });
  addEventListener("resize", sync);
  sec.hidden = false;
  sync();
}

/* ============ the reel: each card loops its own clip; the strip drifts rightward ============ */
{
  const reel = $(".reel"), track = $("#reelTrack"), GAP = 16;
  const vio = new IntersectionObserver(es => es.forEach(e => {
    const v = e.target;
    if (!e.isIntersecting) { v.pause(); return; }
    if (!v.src) {
      v.addEventListener("loadedmetadata", () => { v.currentTime = +v.dataset.s; }, { once: true });
      v.src = v.dataset.src;
    }
    if (!reduceMotion) v.play().catch(() => {});
  }), { rootMargin: "300px" });
  track.querySelectorAll("video").forEach(v => {
    v.addEventListener("timeupdate", () => { if (v.currentTime >= +v.dataset.e) v.currentTime = +v.dataset.s; });
    v.addEventListener("ended", () => { v.currentTime = +v.dataset.s; v.play().catch(() => {}); });
    vio.observe(v);
  });
  if (!reduceMotion) {
    let x = -(track.firstElementChild.offsetWidth + GAP), last = 0, on = false;
    new IntersectionObserver(es => { on = es[0].isIntersecting; }).observe(reel);
    const step = now => {
      const dt = last ? Math.min(50, now - last) : 0; last = now;
      if (on) {
        x += dt * .045;
        /* once a gap opens on the left, the card that just left on the right comes round */
        if (x > 0) {
          const c = track.lastElementChild;
          track.prepend(c);
          x -= c.offsetWidth + GAP;
          const v = c.querySelector("video"); if (v.src) v.play().catch(() => {});
        }
        track.style.transform = `translateX(${x.toFixed(1)}px)`;
      }
      requestAnimationFrame(step);
    };
    track.style.transform = `translateX(${x}px)`;
    requestAnimationFrame(step);
  }
}

/* live NGN: news posts only (no "Photos:" galleries), no story repeated across rows */
const FALLBACK = FEATS.flatMap(f => f.eps).slice(0, 10).map(e => ({ t: e.t, u: e.u, img: e.img }));
(async () => {
  const API = "https://news.northeastern.edu/wp-json/wp/v2/newspost?per_page=24&_embed=wp:featuredmedia&_fields=link,title,_links,_embedded&";
  const rows = $$(".crow[data-q]");
  const data = await Promise.all(rows.map(sec => fetch(API + sec.dataset.q).then(r => r.ok ? r.json() : []).catch(() => [])));
  const shown = new Set(), tmp = document.createElement("div");
  const text = html => { tmp.innerHTML = html; return tmp.textContent.trim(); };
  rows.forEach((sec, k) => {
    const items = data[k].filter(p => !/^Photos:/i.test(p.title.rendered) && !shown.has(p.link)).map(p => {
      const m = p._embedded && p._embedded["wp:featuredmedia"] && p._embedded["wp:featuredmedia"][0];
      if (!m) return null;
      const sz = (m.media_details && m.media_details.sizes) || {};
      const img = (sz["newspack-article-block-portrait-medium"] || sz.large || sz.medium_large || m).source_url;
      if (!img) return null;
      return { t: text(p.title.rendered), u: p.link, img };
    }).filter(Boolean).slice(0, 14);
    if (items.length < 4) { if (!k) mountRow(sec, FALLBACK); return; }
    items.forEach(c => shown.add(c.u));
    mountRow(sec, items);
  });
})();
}
'''
NEW_JS = NEW_JS.replace("__FEATS__", json.dumps(FEATS, ensure_ascii=False).replace("</", "<\\/"))

page = (head + nav_css + overlay_css + c2_css + NEW_CSS + "\n" + tailcss
        + "</style>\n\n<body>\n\n"
        + header_mk + HERO + "<main>\n" + ROWS + globe_mk + sheet_mk + reel_mk + admit_mk + "\n</main>\n" + footer_mk + "\n"
        + lenis_js + "\n<script>\n" + land + "\n" + coops + "\n" + helpers + c2_js + NEW_JS
        + "\n" + tail_js + "/* ============ boot ============ */\nnav.classList.toggle(\"solid\", scrollY > 60);\nresize();\nrequestAnimationFrame(frame);\n</script>\n")

assert page.count("<header") == 1 and page.count("<footer>") == 1
assert page.count('class="ln"') == 5 and page.count('class="crow"') == 5 and page.count('class="vidcard"') == 16
assert 'class="voices-c"' not in page and "SMEET" not in page
for tok in ['id="srch"', 'concept10-rev" content="1"', 'id="stage"', "TOUR_STORIES", "stepIO", 'class="admit"', "reelTrack", "Only at Northeastern", 'id="xrow"', 'id="jRail"', "lineIO"]:
    assert tok in page, tok
for gone in ["placement", "one way in", "and counting", "Continue browsing", "hx-meta", "opens doors", "Now showing", "hxSound", "makeGlobe", "qtrack", 'class="hero"', 'class="grain"', "—"]:
    assert gone not in page, gone
for out in OUT:
    open(out, "w").write(page)
print("built", len(page), "bytes ->", OUT[0])
