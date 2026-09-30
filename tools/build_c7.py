"""Concept 6: the streaming-shelf build. Everything concept 4 has, plus the Full-bleed video carries each pillar
(campus network, co-op, research), the globe survives as a broadcast-style
inset, and five personas are addressed by name: students and families, faculty
candidates, employer talent teams, school counselors, media. Three videos
total; the hero montage is deliberately reused for research. Every persona
link verified 200 on 2026-09-01. Deploys to concept-4/."""
import re, os

V1 = "/Users/z.christensen/environment/prototypes/northeastern-homepage-v2.html"
OUT = ["/Users/z.christensen/Projects/nu-homepage-prototype/concept-6/index.html",
       "/Users/z.christensen/environment/prototypes/concept-6/index.html"]
src = open(V1).read()

def cut(a, b, inclusive_b=False):
    i = src.find(a); assert i >= 0, a[:60]
    j = src.find(b, i + len(a)); assert j > i, b[:60]
    return src[i:j + (len(b) if inclusive_b else 0)]

head        = src[:src.find("  /* ---------- NAV ---------- */")]
nav_css     = cut("  /* ---------- NAV ---------- */", "  /* ---------- HERO ---------- */")
hero_css    = cut("  /* ---------- HERO ---------- */", "  /* ---------- GLOBE SCROLLY ---------- */")
overlay_css = cut("  .srch{", "  /* ---------- SHEET SECTIONS (Adobe pattern) ---------- */")
sheet_css   = cut("  /* ---------- SHEET SECTIONS (Adobe pattern) ---------- */", "  /* ---------- QUOTES (large-card carousel) ---------- */")
tailcss     = cut("  /* ---------- ADMISSIONS CTA ---------- */", "</style>")
imax_css    = cut("  /* ---------- STUDENT LIFE IMAX ---------- */", "  /* ---------- ADMISSIONS CTA ---------- */")

header_mk   = cut("<header", '<section class="hero"')
hero_mk     = cut('<section class="hero"', '<div class="scrolly"')
rest_mk     = cut('<section class="admit"', "<footer>")
footer_mk   = cut("<footer>", "</footer>", True)
assert '<section class="admit"' in rest_mk

lenis       = cut("<script>/* Lenis", "</script>", True)
helpers     = cut("/* ============ shared helpers ============ */", "/* ============ globe data ============ */")
land        = re.search(r"const LAND=\[.*?\];", src).group(0)
coops       = re.search(r"const COOPS=\[.*?\];", src).group(0)
globedata   = cut("/* ============ globe data ============ */", "/* ============ globe engine ============ */")
engine      = cut("/* ============ globe engine ============ */", "/* ============ scrollytelling ============ */")

# engine: near-still idle so an aimed city stays centered; dots always lit
assert engine.count("tgt.lon += 0.03;") == 1
engine = engine.replace("tgt.lon += 0.03;", "tgt.lon += 0.02;")
old_ign = "      ignite = reduceMotion ? 1 : easeOut(p);\n"
assert engine.count(old_ign) == 1
engine = engine.replace(old_ign, "")

# wrap the singleton engine into a per-canvas factory that exposes startFly
assert engine.count('const canvas = $("#globe");') == 1
engine = engine.replace('const canvas = $("#globe");', 'const canvas = stageEl.querySelector("canvas");')
assert engine.count('.observe($("#stage"))') == 1
engine = engine.replace('.observe($("#stage"))', '.observe(stageEl)')
assert engine.count('$("#stage").appendChild(gtip)') == 1
engine = engine.replace('$("#stage").appendChild(gtip)', 'stageEl.appendChild(gtip)')
assert engine.count("of CAMPUSES)") == 1 and engine.count("of NUIN)") == 1
engine = engine.replace("of CAMPUSES)", "of CAMPUSES_)").replace("of NUIN)", "of NUIN_)")
assert engine.count('LAYER_KEYS = ["coops", "campus", "nuin", "labelC", "labelN"]') == 1
engine = engine.replace('LAYER_KEYS = ["coops", "campus", "nuin", "labelC", "labelN"]',
                        'LAYER_KEYS = ["coops", "campus", "nuin", "labelC", "labelN", "spins", "arcs"]')
assert engine.count("labelC: 0, labelN: 0 };") == 1
engine = engine.replace("labelC: 0, labelN: 0 };", "labelC: 0, labelN: 0, spins: 0, arcs: 0 };")
assert engine.count("const p = ((now + i * 400) % 2400) / 2400;") == 1
engine = engine.replace("const p = ((now + i * 400) % 2400) / 2400;",
                        "const p = reduceMotion ? .35 : ((now + i * 400) % 2400) / 2400;")
assert engine.count("const p = (now % 2200) / 2200;") == 1
engine = engine.replace("const p = (now % 2200) / 2200;",
                        "const p = reduceMotion ? .35 : (now % 2200) / 2200;")
engine = ("function makeGlobe(stageEl, opts) {\n"
          "let CAMPUSES_ = opts.campuses || CAMPUSES;\n"
          "const NUIN_ = opts.nuin || NUIN;\n"
          + engine +
          "\nObject.assign(tgt, opts.layers); Object.assign(cur, opts.layers);\n"
          "tgt.k = opts.k || 1.02; cur.k = tgt.k;\n"
          "if (opts.lon !== undefined) cur.lon = tgt.lon = opts.lon;\n"
          "if (opts.lat !== undefined) cur.lat = tgt.lat = opts.lat;\n"
          "resize();\n"
          "requestAnimationFrame(frame);\n"
          "return { fly: startFly, layers: function(o){ Object.assign(tgt, o); },\n"
          "         setCampuses: function(a){ CAMPUSES_ = a; } };\n"
          "}\n")

ARC_BLOCK = """  if (typeof ARCS !== "undefined" && cur.arcs > .01) {
    const gcLerp = (la1, lo1, la2, lo2, t) => {
      const Vv = (la, lo) => { const p = la * RAD, l = lo * RAD;
        return [Math.cos(p) * Math.cos(l), Math.cos(p) * Math.sin(l), Math.sin(p)]; };
      const a = Vv(la1, lo1), b = Vv(la2, lo2);
      const om = Math.acos(Math.max(-1, Math.min(1, a[0]*b[0] + a[1]*b[1] + a[2]*b[2])));
      if (om < 1e-6) return [la1, lo1];
      const sa = Math.sin((1 - t) * om) / Math.sin(om), sb = Math.sin(t * om) / Math.sin(om);
      const x = sa*a[0] + sb*b[0], y = sa*a[1] + sb*b[1], z = sa*a[2] + sb*b[2];
      return [Math.asin(Math.max(-1, Math.min(1, z))) / RAD, Math.atan2(y, x) / RAD];
    };
    ctx.lineWidth = 1;
    ctx.setLineDash([3, 9]);
    ctx.lineDashOffset = -((now / 28) % 12);
    for (let ai = 0; ai < ARCS.length; ai++) {
      const A = ARCS[ai];
      ctx.beginPath();
      let started = false;
      for (let ti = 0; ti <= 24; ti++) {
        const t = ti / 24;
        const pt = gcLerp(A[0], A[1], A[2], A[3], t);
        const alt = Math.sin(Math.PI * t) * 0.10;
        const pr = project(pt[0], pt[1], R, cx, cy, alt);
        if (pr[2] > 0.02) {
          if (!started) { ctx.moveTo(pr[0], pr[1]); started = true; }
          else ctx.lineTo(pr[0], pr[1]);
        } else started = false;
      }
      ctx.strokeStyle = `rgba(238,85,102,${(A[4] || .12) * cur.arcs})`;
      ctx.stroke();
    }
    ctx.setLineDash([]);
  }
"""
ARC_ANCHOR = '  if (typeof STORY_PINS !== "undefined" && cur.spins > .01) {'
assert engine.count(ARC_ANCHOR) == 1
engine = engine.replace(ARC_ANCHOR, ARC_BLOCK + ARC_ANCHOR)

counters_js = cut("/* ============ research counters ============ */", "/* ============ research expanding row ============ */")
tail_js     = cut("/* ============ subtle scroll movement ============ */", "/* ============ boot ============ */")
i0 = tail_js.find("/* student life imax:"); i1 = tail_js.find("/* smooth scrolling via Lenis")
assert 0 < i0 < i1
tail_js = tail_js[:i0] + tail_js[i1:]


head = head.replace('<meta name="prototype-rev" content="53">',
                    '<meta name="concept6-rev" content="1">')
assert 'concept6-rev' in head


hero_mk = hero_mk.replace('href="#experience"', 'href="#campuses"')



for name in ("header_mk", "hero_mk", "rest_mk", "footer_mk"):
    v = (globals()[name].replace('src="img/', 'src="../img/')
         .replace("url('img/", "url('../img/").replace('src="hero.mp4"', 'src="../hero.mp4"'))
    globals()[name] = v

NGN = "https://news.northeastern.edu"
U = NGN + "/wp-content/uploads"
V_CAMPUS = "https://www.northeastern.edu/wp-content/uploads/Jamie-Wong-Video-Fade.mp4"
V_COOP   = "https://www.northeastern.edu/wp-content/uploads/The-Co-Op-Experience_Video-2-Fusion-v3.mp4"
V_HERO   = "../hero.mp4"
V_HEROSM = "../hero-sm.mp4"
V_JAMIESM = "../jamie-sm.mp4"
V_COOPSM = "../coop-sm.mp4"
V_LONDON = "https://www.nulondon.ac.uk/wp-content/uploads/2026/02/Discover-your-path-at-Northeastern-University-London.mp4"
V_NYC    = "https://nyc.northeastern.edu/wp-content/uploads/NYC-Home_SLOW.mp4"

TICKER = [
 ("Aug 28","This student toiled in aviaries, barns and pens for his co-op","/2026/08/28/wildlife-sanctuary-co-op-experience/"),
 ("Aug 28","Samantha Johnson '21, robotics CEO, to speak at Boston Convocation","/2026/08/28/samantha-johnson-convocation-alumni-speaker/"),
 ("Aug 28","Scientists put algae to work making fuel. AI keeps watch.","/2026/08/28/algae-biofuel-ai-research/"),
 ("Aug 27","Many causes for floods, many causes for their devastation","/2026/08/27/nepal-tibet-flood/"),
 ("Aug 27","Boston convocation welcomes new Huskies to Northeastern","/2026/08/27/boston-convocation-guide-2026/"),
 ("Aug 20","Slow down and zoom in: the case for microfilm research","/2026/08/20/microfilm-research-archivist/"),
 ("Aug 12","These racing club students were given nine months to make their 'EV baby'","/2026/08/12/northeastern-electric-racing-club-2/"),
 ("Jul 29","This researcher is launching satellites to unlock faster data speeds","/2026/07/29/satellite-internet-6g-speeds-research/"),
 ("Jul 27","Cracking the axolotl code: how to regrow limbs and stay young","/2026/07/27/axolotl-regeneration-anti-aging/"),
 ("Jul 22","Northeastern graduate finds success and comfort in computer codes","/2026/07/22/ai-career-amazon-graduate/"),
]

NGN_LOGO = (
 '<svg class="w-logo" viewBox="0 0 380 102" fill="none" xmlns="http://www.w3.org/2000/svg" '
 'role="img" aria-label="Northeastern Global News">'
 '<path d="M330.519 1.38965V11.2966H362.874L334.034 40.1918L341.025 47.2092L370.112 18.0525V50.9655H380V1.38965H330.519Z" fill="#C8102E"></path>'
 '<path d="M0 100.541V1.4585H17.8395L72.5255 69.4585V1.4585H92.1915V100.541H74.0636L19.6661 33.2707V100.541H0Z" fill="white"></path>'
 '<path d="M107.751 50.9931C107.751 22.0291 129.587 0 158.496 0C175.607 0 191.414 8.17321 201.824 23.2675L186.319 34.3577C178.601 22.6896 168.548 18.2315 158.496 18.2315C140.505 18.2315 127.912 31.7985 127.912 50.9931C127.912 70.1878 141.013 83.7548 159.004 83.7548C175.456 83.7548 184.712 74.0542 186.965 63.5419H157.04V46.5488H206.85C207.139 49.1081 207.207 52.0251 207.207 54.5018C207.207 79.9709 189.299 102 159.004 102C128.708 102 107.737 79.9709 107.737 51.0069L107.751 50.9931Z" fill="white"></path>'
 '<path d="M222.781 100.541V1.4585H240.621L295.307 69.4585V1.4585H314.973V100.541H296.845L242.447 33.2707V100.541H222.781V100.541Z" fill="white"></path>'
 '</svg>')

def ticker_items(rows):
    return "".join(f'<a class="w-item" href="{NGN}{u}"><span class="w-d">{d}</span>{t}</a>'
                   for d, t, u in rows)

NEW_CSS = """  /* ---------- concept-6 layer ---------- */
  ::selection{background:var(--red);color:#fff}
  body{background:var(--dark)}
  .vidcard{position:relative;border-radius:14px;overflow:hidden;background:#141419}
  .vidcard video{width:100%;height:100%;object-fit:cover;display:block}
  .line{display:block;overflow:hidden}
  .line > span{display:block;transform:translateY(115%);transition:transform 1s var(--ease)}
  .line.in > span, .in .line > span{transform:none}

  /* ---------- NGN wire ---------- */
  .wire{background:var(--dark);color:#fff;overflow:hidden;position:relative;z-index:6}
  .wire.top{margin-top:-28px;border-radius:28px 28px 0 0;padding-bottom:28px}
  .wire.top .wire-in{margin-top:14px}
  .wire-in{display:flex;align-items:center;height:56px}
  .w-label{flex:0 0 auto;display:flex;align-items:center;gap:10px;padding:0 22px;height:100%}
  .w-label::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--red);
    animation:wpulse 2.2s ease infinite;flex-shrink:0}
  @keyframes wpulse{0%,100%{box-shadow:0 0 0 0 rgba(200,16,46,.5)}50%{box-shadow:0 0 0 7px rgba(200,16,46,0)}}
  .w-logo{height:15px;width:auto;display:block}
  .w-belt{overflow:hidden;flex:1;display:flex;align-items:center;height:100%;
    mask-image:linear-gradient(to right,transparent,#000 40px,#000 calc(100% - 40px),transparent)}
  .w-track{display:flex;align-items:baseline;gap:44px;padding-left:44px;width:max-content;animation:wireX 80s linear infinite}
  .wire:hover .w-track{animation-play-state:paused}
  @keyframes wireX{to{transform:translateX(-50%)}}
  .w-item{display:inline-flex;align-items:baseline;gap:10px;font-size:14px;color:#E5E5E5;white-space:nowrap}
  .w-item:hover{color:#fff}
  .w-d{font-size:11.5px;color:#A9A9B2}
  @media (prefers-reduced-motion: reduce){
    .w-track{animation:none}.w-belt{overflow-x:auto}
    .w-label::before{animation:none}
  }

  /* ---------- the shelves ---------- */
  .shelves{position:relative;z-index:2;color:#fff;padding:clamp(28px,4svh,56px) 0 clamp(70px,10svh,130px)}
  .trow{margin-top:clamp(34px,5svh,60px)}
  .trow[hidden]{display:none}
  .trow-head{display:flex;align-items:baseline;justify-content:space-between;gap:16px}
  .trow-head h2{margin:0;font-size:clamp(19px,1.6vw,24px);font-weight:600;letter-spacing:-.01em}
  .tr-btns{display:flex;gap:8px}
  .tr-btn{width:36px;height:36px;border-radius:50%;border:1px solid rgba(255,255,255,.35);
    background:transparent;color:#fff;font-size:15px;cursor:pointer;transition:.2s;
    display:flex;align-items:center;justify-content:center}
  .tr-btn:hover{background:#fff;color:var(--ink);border-color:#fff}
  .tr-strip{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x proximity;
    scrollbar-width:none;margin-top:14px;padding:14px 0 18px;
    padding-inline:max(24px, calc((100vw - 1280px) / 2))}
  .tr-strip::-webkit-scrollbar{display:none}
  .card{position:relative;flex:0 0 auto;width:clamp(230px,22vw,350px);aspect-ratio:16/9;
    border-radius:10px;overflow:hidden;background:#141419;scroll-snap-align:start;
    transition:transform .35s var(--ease),box-shadow .35s var(--ease);display:block}
  .card:hover,.card:focus-visible{transform:scale(1.06);z-index:3;
    box-shadow:0 18px 44px rgba(0,0,0,.55)}
  .card:focus-visible{outline:2px solid #fff;outline-offset:3px}
  .card img,.card video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
  .card .c-t{position:absolute;left:0;right:0;bottom:0;z-index:2;margin:0;padding:34px 14px 12px;
    font-size:14px;font-weight:500;line-height:1.3;color:#fff;
    background:linear-gradient(to top,rgba(0,0,0,.78),transparent)}
  .card.wide{width:clamp(300px,30vw,470px)}
  @media (prefers-reduced-motion: reduce){.card{transition:none}}

  /* ---------- the network globe band ---------- */
  .s-orbit{position:relative;z-index:2;color:#fff;height:100svh;overflow:hidden}
  .o-globe{position:absolute;inset:0;touch-action:pan-y;cursor:grab;
    -webkit-mask-image:linear-gradient(to bottom,transparent,#000 12%,#000 88%,transparent);
    mask-image:linear-gradient(to bottom,transparent,#000 12%,#000 88%,transparent)}
  .o-globe canvas{position:absolute;inset:0;width:100%;height:100%}
  .o-overlay{position:relative;z-index:2;height:100%;display:flex;align-items:center;pointer-events:none}
  .n-copy{max-width:min(520px,44vw);padding-left:max(24px, calc((100vw - 1280px) / 2))}
  .n-copy h2{margin:0;font-size:clamp(40px,4.6vw,84px);font-weight:200;
    letter-spacing:-.03em;line-height:1.05}
  .n-copy .n-legend{margin:18px 0 0;font-size:15px;color:#D4D4D4}
  .n-copy .n-lede{margin:14px 0 0;font-size:15px;line-height:1.55;color:#A9A9B2;max-width:36ch}
  @media (max-width:820px){
    .s-orbit{height:auto}
    .o-globe{position:relative;inset:auto;height:52svh}
    .o-overlay{height:auto;display:block}
    .n-copy{max-width:none;padding:36px 18px 10px}
    .n-copy h2{font-size:clamp(34px,9vw,52px)}
  }
"""

NGN = "https://news.northeastern.edu"
U = NGN + "/wp-content/uploads"

def card(img, title, url=None, video=None, wide=False):
    cls = "card wide" if wide else "card"
    inner = (f'<video src="{video}" muted loop playsinline preload="none" data-hovplay></video>'
             if video else f'<img src="{img}" alt="" loading="lazy">')
    cap = f'<p class="c-t">{title}</p>'
    if url:
        return f'<a class="{cls}" href="{url}" data-ct="{title}" data-cimg="{img or ""}">{inner}{cap}</a>'
    return f'<div class="{cls}">{inner}{cap}</div>'

RESEARCH_CARDS = [
 card(None, "Inside the labs", video="../jamie-sm.mp4", wide=True),
 card(U+"/2026/09/Xufeng-Zhang_1400.jpg", "This Northeastern researcher is making &lsquo;waves&rsquo; with magnets", NGN+"/2026/09/14/magnons-quantum-computing-research/"),
 card(U+"/2025/09/093025_MM_Field_Robotos_Lab_033.jpg", "Robots walk to class here. Researchers are teaching them how", NGN+"/2025/10/01/walking-the-future/"),
 card(U+"/2026/07/072226_AS_-Calina_Copos_010.jpg", "Cracking the axolotl code: how to regrow limbs and stay young", NGN+"/2026/07/27/axolotl-regeneration-anti-aging/"),
 card(U+"/2026/08/Biofuel1400.jpg", "Scientists put algae to work making fuel. AI keeps watch", NGN+"/2026/08/28/algae-biofuel-ai-research/"),
 card(U+"/2026/08/quantumsystem1400.jpg", "Quieting &lsquo;the noise&rsquo; in quantum computing", NGN+"/2026/08/07/modular-quantum-computing-research/"),
]

COOP_CARDS = [
 card(None, "The co&#8209;op experience", video="../coop-sm.mp4", wide=True),
 card("../img/apple-coop.jpg", "Developing cameras for Apple products, on co&#8209;op", NGN+"/2025/01/15/apple-co-op-camera-process-engineer/"),
 card(U+"/2023/11/Cecile-Doehrty_1400.jpg", "Teacher, mentor, big sister: six months in a Cambodian dormitory", NGN+"/2023/11/06/harpswell-foundation-co-op-cambodian-women/"),
 card(U+"/2023/11/Dialogue-of-Civilization_1400.jpg", "Learning how global negotiation really works", NGN+"/2023/11/27/dialogue-of-civilizations-geneva-anniversary/"),
 card(U+"/2023/09/Vienna1400.jpg", "Coffeehouses, Mozart and international finance, on co&#8209;op", NGN+"/2023/10/13/unitcargo-finance-co-op-vienna-switzerland/"),
 card("../img/oyster-dock.jpg", "Harvesting oysters on Maine&rsquo;s Nonesuch River, on co&#8209;op", NGN+"/2022/11/01/oyster-harvesting-maine/"),
]

LIFE_CARDS = [
 card(None, "Boston campus", video="../hero-sm.mp4", wide=True),
 card(U+"/2025/07/070125_AS_RPS_orientation_004.jpg", "Orientation"),
 card(U+"/2026/06/063026_AS_Husky101_019.jpg", "Husky 101"),
 card(U+"/2024/02/021324_MM_beanpot_cele_015.jpg", "Beanpot night"),
 card(U+"/2025/04/JIM28826.jpg", "On campus"),
 card(U+"/2023/09/Convocation1400.jpg", "Convocation"),
]

ATHLETICS_CARDS = [
 card(U+"/2024/02/021224_MM_M_beanpot_083.jpg", "Beanpot champions", "https://gonu.com/"),
 card(U+"/2024/02/021324_MM_beanpot_cele_015.jpg", "Northeastern Athletics", "https://gonu.com/"),
 card(U+"/2023/09/Convocation1400.jpg", "Sports at NGN", NGN+"/category/sports/"),
]

ADMIT_CARDS = [
 card("../img/oyster-coop.jpg", "Apply to Northeastern", "https://admissions.northeastern.edu/"),
 card("../img/microscopy-coop.jpg", "Visit a campus", "https://admissions.northeastern.edu/visit/"),
 card("../img/apple-coop.jpg", "Start abroad with N.U.in", "https://nuin.northeastern.edu/"),
 card(U+"/2023/09/Convocation1400.jpg", "Financial aid", "https://studentfinance.northeastern.edu/"),
]

NGN_FALLBACK = RESEARCH_CARDS[1:5]

def row(rid, label, cards, hidden=False):
    h = " hidden" if hidden else ""
    return (f'<section class="trow"{h} id="{rid}" aria-label="{label}">\n'
            f'  <div class="wrap trow-head"><h2>{label}</h2>'
            f'<div class="tr-btns"><button class="tr-btn" data-dir="-1" aria-label="Scroll {label} back">&#8592;</button>'
            f'<button class="tr-btn" data-dir="1" aria-label="Scroll {label} forward">&#8594;</button></div></div>\n'
            f'  <div class="tr-strip">\n    ' + "\n    ".join(cards) + "\n  </div>\n</section>\n")

NEW_BODY = f"""
<section class="wire top" aria-label="Latest from Northeastern Global News">
  <div class="wire-in">
    <span class="w-label">{NGN_LOGO}</span>
    <div class="w-belt"><div class="w-track">{ticker_items(TICKER)}{ticker_items(TICKER)}</div></div>
  </div>
</section>

<div class="shelves">
{row("continueRow", "Continue browsing", [], hidden=True)}
{row("coopRow", "Co&#8209;op", COOP_CARDS)}
{row("researchRow", "Research", RESEARCH_CARDS)}
{row("ngnRow", "New from Northeastern Global News", NGN_FALLBACK)}
{row("lifeRow", "Student life", LIFE_CARDS)}
{row("athleticsRow", "Athletics", ATHLETICS_CARDS)}
{row("admitRow", "Admissions", ADMIT_CARDS)}
</div>

<section class="s-orbit" id="campuses">
  <div class="o-globe" id="oGlobe" role="img" aria-label="Interactive globe showing the connected Northeastern network: campuses, N.U.in cities, and co&#8209;op locations"><canvas></canvas></div>
  <div class="o-overlay">
    <div class="n-copy">
      <h2>The world is our campus.</h2>
      <p class="n-legend">Campuses in white. Co&#8209;op cities in red.</p>
      <p class="n-lede">Every campus opens doors to all the others. Students move between them, and so does the work.</p>
    </div>
  </div>
</section>

"""

NEW_JS = """
/* ============ live NGN wire ============ */
(async () => {
  try {
    const r = await fetch("https://news.northeastern.edu/wp-json/wp/v2/newspost?per_page=18&_fields=title,link,date");
    if (!r.ok) return;
    const posts = (await r.json()).filter(p => !/^Photos:/i.test(p.title.rendered)).slice(0, 14);
    if (!posts.length) return;
    const mo = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
    const strip = document.createElement("div");
    const html = posts.map(p => {
      strip.innerHTML = p.title.rendered;
      const d = new Date(p.date);
      return `<a class="w-item" href="${p.link}"><span class="w-d">${mo[d.getMonth()]} ${d.getDate()}</span>${strip.textContent}</a>`;
    }).join("");
    $$(".w-track").forEach(tr => { tr.innerHTML = html + html; });
  } catch (e) { /* baked headlines remain */ }
})();

/* ============ shelf controls: arrows, hover-play tiles ============ */
$$(".trow").forEach(sec => {
  const strip = sec.querySelector(".tr-strip");
  sec.querySelectorAll(".tr-btn").forEach(b => b.addEventListener("click", () => {
    strip.scrollBy({ left: +b.dataset.dir * strip.clientWidth * 0.85,
                     behavior: reduceMotion ? "auto" : "smooth" });
  }));
});
$$("video[data-hovplay]").forEach(v => {
  const cardEl = v.closest(".card");
  cardEl.addEventListener("mouseenter", () => {
    if (reduceMotion) return;
    if (!v.dataset.loaded) { v.dataset.loaded = "1"; v.load(); }
    v.play().catch(() => {});
  });
  cardEl.addEventListener("mouseleave", () => v.pause());
});

/* ============ continue browsing (this browser only) ============ */
const CB_KEY = "nu-continue";
const cbRead = () => { try { return JSON.parse(localStorage.getItem(CB_KEY)) || []; } catch (e) { return []; } };
const cbRow = $("#continueRow");
if (cbRow) {
  const seen = cbRead().slice(0, 8);
  if (seen.length) {
    cbRow.querySelector(".tr-strip").innerHTML = seen.map(c =>
      `<a class="card" href="${c.u}" data-ct="${c.t}" data-cimg="${c.img}">` +
      `<img src="${c.img}" alt="" loading="lazy"><p class="c-t">${c.t}</p></a>`).join("");
    cbRow.hidden = false;
  }
  addEventListener("click", e => {
    const a = e.target.closest("a.card");
    if (!a || !a.dataset.cimg) return;
    try {
      const list = cbRead().filter(c => c.u !== a.href);
      list.unshift({ t: a.dataset.ct, img: a.dataset.cimg, u: a.href });
      localStorage.setItem(CB_KEY, JSON.stringify(list.slice(0, 12)));
    } catch (e2) { /* private mode etc */ }
  });
}

/* ============ live NGN shelf with real thumbnails ============ */
(async () => {
  try {
    const r = await fetch("https://news.northeastern.edu/wp-json/wp/v2/newspost?per_page=12&_embed=wp:featuredmedia");
    if (!r.ok) return;
    const strip = document.createElement("div");
    const cards = (await r.json())
      .filter(p => !/^Photos:/i.test(p.title.rendered))
      .map(p => {
        const m = p._embedded && p._embedded["wp:featuredmedia"] && p._embedded["wp:featuredmedia"][0];
        if (!m) return null;
        const sz = m.media_details && m.media_details.sizes;
        const img = (sz && (sz.medium_large || sz.large || sz.medium) || m).source_url || m.source_url;
        strip.innerHTML = p.title.rendered;
        const t = strip.textContent;
        return `<a class="card" href="${p.link}" data-ct="${t.replace(/"/g, "&quot;")}" data-cimg="${img}">` +
               `<img src="${img}" alt="" loading="lazy"><p class="c-t">${t}</p></a>`;
      })
      .filter(Boolean).slice(0, 10);
    if (cards.length >= 4) $("#ngnRow .tr-strip").innerHTML = cards.join("");
  } catch (e) { /* baked cards remain */ }
})();

/* ============ the network: everything lit, everything connected ============ */
let STORY_PINS, storySel = -1;
const oGlobeEl = $("#oGlobe");
if (oGlobeEl) {
  const ARCS = [];
  for (let i = 0; i < CAMPUSES.length; i++)
    for (let j = i + 1; j < CAMPUSES.length; j++)
      ARCS.push([CAMPUSES[i][0], CAMPUSES[i][1], CAMPUSES[j][0], CAMPUSES[j][1], .10]);
  const BOS = CAMPUSES.find(c => c[2] === "Boston");
  NUIN.forEach(n => ARCS.push([BOS[0], BOS[1], n[0], n[1], .22]));
  window.ARCS = ARCS;
  makeGlobe(oGlobeEl, {
    layers: { campus: 1, labelC: .9, nuin: 1, labelN: 0, coops: .8, spins: 0, arcs: 1 },
    k: 1.05, lat: 35, lon: -45
  });
}

/* ============ clip-reveal lines ============ */
const lineIO = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add("in"); lineIO.unobserve(e.target); }
}), { threshold: 0.3 });
$$(".line").forEach(el => lineIO.observe(el));
"""

NEW_BOOT = """/* ============ boot ============ */
nav.classList.toggle("solid", scrollY > 60);
"""

page = (head + nav_css + hero_css + overlay_css + sheet_css + NEW_CSS + "\n" + tailcss
        + "</style>\n\n<body>\n\n"
        + header_mk + hero_mk + NEW_BODY + rest_mk + footer_mk + "\n"
        + lenis + "\n<script>\n" + land + "\n" + coops + "\n" + helpers + globedata + engine + counters_js + NEW_JS + "\n" + tail_js + NEW_BOOT + "</script>\n")

assert page.count("<header") == 1 and page.count("<footer>") == 1
assert page.count("<video") == 4  # hero + three hover-play shelf tiles
assert page.count('class="trow"') == 7
for tok in ['id="srch"', 'id="tkv"', "tr-strip", "tr-btn", "continueRow", "ngnRow", "athleticsRow",
            "data-hovplay", "nu-continue", "ARCS", "n-copy", 'class="admit"',
            "concept6-rev", 'content="1"', "newspost", "gonu.com", "admissions.northeastern.edu"]:
    assert tok in page, tok
for gone in ["s-grow", "rb-main", "s-reel", "vc-vid", "o-tab", "gt-card", "lifeimax", "rphrase", "wire foot"]:
    assert gone not in page, gone
for out in OUT:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(page)
print("built", len(page), "bytes ->", OUT[0])
