"""Concept 5: the maximal build. Everything concept 4 has, plus the Full-bleed video carries each pillar
(campus network, co-op, research), the globe survives as a broadcast-style
inset, and five personas are addressed by name: students and families, faculty
candidates, employer talent teams, school counselors, media. Three videos
total; the hero montage is deliberately reused for research. Every persona
link verified 200 on 2026-09-01. Deploys to concept-4/."""
import re, os

V1 = "/Users/z.christensen/environment/prototypes/northeastern-homepage-v2.html"
OUT = ["/Users/z.christensen/Projects/nu-homepage-prototype/concept-5/index.html",
       "/Users/z.christensen/environment/prototypes/concept-5/index.html"]
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
rest_mk     = cut('<section class="lifezoom lifeimax"', "<footer>")
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


head = head.replace('<meta name="prototype-rev" content="53">',
                    '<meta name="concept5-rev" content="1">')
assert 'concept5-rev' in head


hero_mk = hero_mk.replace('href="#experience"', 'href="#campuses"')

ROTOR = ('<h1 class="rotor" aria-label="Experience. Everything. Anywhere.">'
         '<span class="rphrase on" aria-hidden="true">Experience. Everything. Anywhere.</span>'
         '<span class="rphrase" aria-hidden="true">An education in the world.</span>'
         '<span class="rphrase" aria-hidden="true">Put experience to work.</span>'
         '<span class="rphrase" aria-hidden="true">Work that leaves the building.</span>'
         '<span class="rphrase" aria-hidden="true">This place doesn\u2019t slow down.</span>'
         '</h1>')
old_h1 = '<h1><span class="w">Experience.</span> <span class="w">Everything.</span> <span class="w">Anywhere.</span></h1>'
assert hero_mk.count(old_h1) == 1
hero_mk = hero_mk.replace(old_h1, ROTOR)

old_h = "<h2>Class is only half of it.</h2>"
assert rest_mk.count(old_h) == 1
rest_mk = rest_mk.replace(old_h, "<h2>This place doesn\u2019t slow down.</h2>")

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

NEW_CSS = """  /* ---------- concept-4 layer ---------- */
  ::selection{background:var(--red);color:#fff}
  .grain{position:fixed;inset:-50%;z-index:400;pointer-events:none;opacity:.045;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
    animation:grain 900ms steps(3) infinite}
  @keyframes grain{0%{transform:translate(0,0)}34%{transform:translate(-2%,1%)}67%{transform:translate(1%,-2%)}100%{transform:translate(0,0)}}
  .line{display:block;overflow:hidden}
  .line > span{display:block;transform:translateY(115%);transition:transform 1s var(--ease)}
  .line.in > span, .in .line > span{transform:none}
  .bl{opacity:0;filter:blur(16px);transform:translateY(22px);
    transition:opacity 1.05s var(--ease),filter 1.05s var(--ease),transform 1.05s var(--ease)}
  .bl.in{opacity:1;filter:blur(0);transform:none}
  .d1{transition-delay:.12s}.d2{transition-delay:.24s}.d3{transition-delay:.36s}.d4{transition-delay:.48s}
  @media (prefers-reduced-motion: reduce){
    .grain{animation:none}
    .line > span{transform:none;transition:none}
    .bl{opacity:1;filter:none;transform:none;transition:none}
  }

  /* ---------- NGN wire ---------- */
  .wire{background:var(--dark);color:#fff;overflow:hidden;position:relative;z-index:6}
  .wire.top{margin-top:-28px;border-radius:28px 28px 0 0;padding-bottom:28px}
  .wire.top .wire-in{margin-top:14px}
  .wire.foot{border-top:1px solid rgba(255,255,255,.1)}
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

  /* ---------- one dark continuum ---------- */
  body{background:var(--dark)}
  .vidcard{position:relative;border-radius:14px;overflow:hidden;background:#141419}
  .vidcard video{width:100%;height:100%;object-fit:cover;display:block}

  /* ---------- research band: one lead story, four strips ---------- */
  .s-research{position:relative;z-index:2;color:#fff;padding:clamp(64px,9vh,120px) 0 0}
  .rb{display:flex;gap:10px;height:min(72svh,640px)}
  .rb a{position:relative;flex:1;min-width:0;display:block;border-radius:14px;overflow:hidden;
    background:#141419;transition:flex .65s var(--ease)}
  .rb a.on{flex:4.4}
  .rb img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
    transition:filter .6s var(--ease)}
  .rb a:not(.on) img{filter:brightness(.58) saturate(.85)}
  .rb a:not(.on):hover img{filter:brightness(.85) saturate(1)}
  .rb a::after{content:"";position:absolute;left:0;right:0;bottom:0;height:40%;z-index:1;
    background:linear-gradient(to top,rgba(0,0,0,.72),transparent);
    opacity:0;transition:opacity .35s var(--ease)}
  .rb a.on::after{opacity:1}
  .rb-cap{position:absolute;left:0;bottom:0;z-index:2;margin:0;padding:26px 24px 20px;
    width:clamp(340px,36vw,560px);box-sizing:border-box;
    font-size:clamp(16px,1.5vw,21px);font-weight:500;line-height:1.3;color:#fff;
    opacity:0;transform:translateY(10px);
    transition:opacity .25s var(--ease),transform .25s var(--ease);pointer-events:none}
  .rb a.on .rb-cap{opacity:1;transform:none;
    transition:opacity .5s var(--ease) .3s,transform .5s var(--ease) .3s}
  @media(max-width:820px){
    .rb{flex-direction:column;height:auto}
    .rb a{flex:none !important;aspect-ratio:16/10}
    .rb a:not(.on) img{filter:none}
    .rb a::after{opacity:1}
    .rb-cap{opacity:1;transform:none;width:100%}
  }
  @media (prefers-reduced-motion: reduce){
    .rb a{transition:none}.rb-cap{transition:none}
  }

  /* ---------- research counters ---------- */
  .s-rstats{position:relative;z-index:2;color:#fff;padding:clamp(56px,8vh,110px) 0 clamp(72px,10vh,150px)}
  .rc-grid{position:relative;z-index:2;display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(24px,3vw,48px)}
  .rc{border-left:1px solid rgba(255,255,255,.14);padding-left:clamp(18px,2vw,30px)}
  .rc:first-child{border-left:0;padding-left:0}
  .rc .n{font-size:clamp(40px,4.6vw,76px);font-weight:200;letter-spacing:-.03em;line-height:1;
    color:#fff;font-variant-numeric:tabular-nums;white-space:nowrap}
  .rc .l{margin-top:10px;font-size:14px;color:#A9A9B2;max-width:26ch}
  @media(max-width:820px){
    .rc-grid{grid-template-columns:1fr;gap:26px}
    .rc{border-left:0;padding-left:0;border-top:1px solid rgba(255,255,255,.14);padding-top:20px}
    .rc:first-child{border-top:0;padding-top:0}
  }

  /* ---------- co-op film grows to fill, stats blur in over it ---------- */
  .s-grow{position:relative;z-index:2;color:#fff}
  .g-track{height:340svh}
  .g-stage{position:sticky;top:0;height:100svh;overflow:hidden;display:grid;place-items:center}
  .g-media{position:relative;width:62vw;height:60svh;border-radius:18px;overflow:hidden;
    background:#141419;will-change:width,height}
  .g-media video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
    transition:filter .7s var(--ease)}
  .g-stage.dim .g-media video{filter:brightness(.42)}
  .g-stats{position:absolute;inset:0;z-index:2;display:flex;flex-direction:column;
    justify-content:center;align-items:center;gap:clamp(26px,5.5svh,58px);pointer-events:none}
  .g-stat{text-align:center}
  .g-stat .n{font-size:clamp(56px,7.6vw,132px);font-weight:200;letter-spacing:-.035em;line-height:.95;
    font-variant-numeric:tabular-nums;white-space:nowrap}
  .g-stat .l{margin-top:8px;font-size:15px;color:#D4D4D4}
  @media (prefers-reduced-motion: reduce){
    .g-track{height:auto}
    .g-stage{position:static;height:100svh}
    .g-media{width:100vw !important;height:100svh !important;border-radius:0 !important}
    .g-stage .g-media video{filter:brightness(.42)}
  }

  /* ---------- across the network: categories left, globe right ---------- */
  .s-nethead{position:relative;z-index:2;color:#fff;padding:clamp(110px,16vh,220px) 0 0;text-align:center}
  .s-nethead h2{margin:0 auto;font-size:clamp(40px,5vw,84px);font-weight:200;
    letter-spacing:-.03em;line-height:1.05;max-width:14ch;text-wrap:balance}
  .s-orbit{position:relative;z-index:2;color:#fff;height:100svh;overflow:hidden}
  .o-globe{position:absolute;inset:0;touch-action:pan-y;cursor:grab;
    -webkit-mask-image:linear-gradient(to bottom,transparent,#000 12%,#000 88%,transparent);
    mask-image:linear-gradient(to bottom,transparent,#000 12%,#000 88%,transparent)}
  .o-globe canvas{position:absolute;inset:0;width:100%;height:100%}
  .o-overlay{position:relative;z-index:2;height:100%;display:flex;align-items:center;
    padding-left:max(24px, calc((100vw - 1280px) / 2));pointer-events:none}
  .n-copy{position:relative;z-index:2;height:100%;display:flex;flex-direction:column;
    justify-content:center;max-width:min(520px,44vw);
    padding-left:max(24px, calc((100vw - 1280px) / 2));pointer-events:none}
  .n-copy h2{margin:0;font-size:clamp(40px,4.6vw,84px);font-weight:200;
    letter-spacing:-.03em;line-height:1.05}
  .n-copy .n-legend{margin:18px 0 0;font-size:15px;color:#D4D4D4}
  .n-copy .n-lede{margin:14px 0 0;font-size:15px;line-height:1.55;color:#A9A9B2;max-width:36ch}
  @media (max-width:820px){
    .n-copy{max-width:none;height:auto;padding:36px 18px 10px}
    .n-copy h2{font-size:clamp(34px,9vw,52px)}
  }

  /* ---------- rotating hero phrases ---------- */
  .rotor{position:relative;min-height:2.95em}
  @media (max-width:820px){.rotor{min-height:4em}}
  .rphrase{position:absolute;left:0;right:0;top:0;opacity:0;filter:blur(14px);
    transform:translateY(14px);transition:opacity .8s var(--ease),filter .8s var(--ease),
    transform .8s var(--ease)}
  .rphrase.on{opacity:1;filter:blur(0);transform:none}
  @media (prefers-reduced-motion: reduce){
    .rphrase{transition:none}
  }

  /* ---------- decorative film reel ---------- */
  .s-reel{position:relative;z-index:2;padding:clamp(90px,13svh,180px) 0;overflow:hidden}

  .reel-track{display:flex;gap:16px;width:max-content;animation:reelX 56s linear infinite}
  .s-reel:hover .reel-track{animation-play-state:paused}
  @keyframes reelX{to{transform:translateX(-50%)}}
  .reel-track .vidcard{flex:0 0 auto;height:min(66svh,740px);aspect-ratio:9/16}
  @media (max-width:820px){
    .s-reel{padding:clamp(56px,8svh,90px) 0}
    .reel-track .vidcard{height:82svh}
  }
  @media (prefers-reduced-motion: reduce){
    .reel-track{animation:none;overflow-x:auto;width:auto}
  }

  /* ---------- portrait quotes ---------- */
  .voices-c{position:relative;z-index:6;background:var(--dark);color:#fff;
    padding:clamp(90px,13vh,190px) 0 100px}
  .vc{display:grid;grid-template-columns:5fr 7fr;gap:clamp(28px,5vw,84px);align-items:start}
  .vc-media{position:sticky;top:calc(50svh - min(33svh,320px));height:min(66svh,640px);
    border-radius:16px;overflow:hidden}
  .vc-vid{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;
    transition:opacity .6s var(--ease)}
  .vc-vid.on{opacity:1}
  .vc-flow .vc-q{min-height:72svh;display:flex;flex-direction:column;justify-content:center;
    opacity:.32;transition:opacity .5s var(--ease)}
  .vc-flow .vc-q.on{opacity:1}
  .vc-q blockquote{font-size:clamp(24px,2.8vw,42px);font-weight:300;letter-spacing:-.015em;
    line-height:1.25;max-width:24ch;text-wrap:balance}
  .v-who{margin-top:20px;font-size:15px;color:#D4D4D4}
  .v-who b{display:block;font-weight:600;color:#fff;font-size:16.5px}
  .vc-q .storylink{color:#fff}
  @media(max-width:820px){
    .vc{grid-template-columns:1fr}
    .vc-media{display:none}
    .vc-flow .vc-q{min-height:0;padding:34px 0;opacity:1}
  }
"""

# ---- research band: the lead story is 2 days old; strips are the vetted five ----
RB_MAIN = (U+"/2026/09/Xufeng-Zhang_1400.jpg",
  "Xufeng Zhang in his lab at Northeastern.",
  "This Northeastern researcher is making &lsquo;waves&rsquo; with magnets",
  "/2026/09/14/magnons-quantum-computing-research/")
RB_STRIPS = [
 (U+"/2025/09/093025_MM_Field_Robotos_Lab_033.jpg",
  "A Boston Dynamics Spot robot walks alongside student researchers near ISEC.",
  "Robots walk to class here. Researchers are teaching them how",
  "/2025/10/01/walking-the-future/"),
 (U+"/2026/07/072226_AS_-Calina_Copos_010.jpg",
  "A researcher in the Copos lab studies axolotl regeneration.",
  "Cracking the axolotl code: how to regrow limbs and stay young",
  "/2026/07/27/axolotl-regeneration-anti-aging/"),
 (U+"/2026/08/Biofuel1400.jpg",
  "Algae cultures used in AI-monitored biofuel research.",
  "Scientists put algae to work making fuel. AI keeps watch",
  "/2026/08/28/algae-biofuel-ai-research/"),
 (U+"/2026/08/quantumsystem1400.jpg",
  "A modular quantum computing system in the lab.",
  "Quieting 'the noise' in quantum computing",
  "/2026/08/07/modular-quantum-computing-research/"),
]

def research_band():
    img, alt, cap, u = RB_MAIN
    out = (f'<a class="rb-main on" aria-expanded="true" href="{NGN}{u}"><img src="{img}" alt="{alt}">'
           f'<p class="rb-cap">{cap}</p></a>\n')
    for i, (img, alt, cap, u) in enumerate(RB_STRIPS):
        out += (f'      <a class="rb-strip" aria-expanded="false" href="{NGN}{u}" aria-label="{cap}">'
                f'<img src="{img}" alt="{alt}"><p class="rb-cap">{cap}</p></a>\n')
    return out

QUOTES = [
 ("../img/microscopy-coop.jpg", "center 30%",
  ["&ldquo;I really enjoyed the process of research from my previous co&#8209;op.",
   "But taking a step further and working with a physical product was an evolution that I wanted to achieve.&rdquo;"],
  "Cameron D&rsquo;Mello", "Bioengineering &middot; Co&#8209;ops at Beth Israel Medical Center and QuantumScape",
  "/2025/01/24/microscopy-skills-transfer-industries/", "Read Cameron&rsquo;s story"),
 ("../img/oyster-dock.jpg", "20% 35%",
  ["&ldquo;I wanted to do this job and test myself and see",
   "if I like working outdoors as much as I hoped. So far, so good.&rdquo;"],
  "Maddy Russell", "Environmental &amp; sustainability science &middot; Co&#8209;op at Nonesuch Oyster Farm, Maine",
  "/2022/11/01/oyster-harvesting-maine/", "Read Maddy&rsquo;s story"),
 ("https://news.northeastern.edu/wp-content/uploads/2023/04/CAMBODIA_coop1400.jpg", "center",
  ["&ldquo;I really wanted the chance to go out into the field.",
   "You just have to push past it, and that&rsquo;s something I&rsquo;ve gotten pretty good at.&rdquo;"],
  "Paris Graff", "International affairs &middot; Co&#8209;op with the Landmine Relief Fund, Cambodia",
  "/2023/04/25/landmine-relief-fund-cambodia-co-op/", "Read Paris&rsquo;s story"),
]

def portrait_stack():
    # placeholder pairing: these films are NOT footage of the named speakers
    vids = [V_COOP, V_HERO, V_CAMPUS]
    imgs = "".join(
        f'<video class="vc-vid{" on" if i == 0 else ""}" data-i="{i}" src="{vids[i]}" '
        f'muted loop playsinline preload="none" data-vio></video>'
        for i in range(len(QUOTES)))
    blocks = ""
    for i, (img, pos, lines, name, who, u, cta) in enumerate(QUOTES):
        q = " ".join(lines)
        blocks += (f'<div class="vc-q{" on" if i == 0 else ""}" data-i="{i}"><blockquote>{q}</blockquote>'
                   f'<div class="v-who"><b>{name}</b> {who}</div>'
                   f'<a class="storylink" href="{NGN}{u}">{cta}</a></div>\n')

    return imgs, blocks

_vc_imgs, _vc_blocks = portrait_stack()
_rb = research_band()

NEW_BODY = f"""
<div class="grain" aria-hidden="true"></div>

<section class="wire top" aria-label="Latest from Northeastern Global News">
  <div class="wire-in">
    <span class="w-label">{NGN_LOGO}</span>
    <div class="w-belt"><div class="w-track">{ticker_items(TICKER)}{ticker_items(TICKER)}</div></div>
  </div>
</section>

<section class="s-research" id="research" aria-label="Research at Northeastern">
  <div class="wrap">
    <div class="rb bl">
      {_rb}
    </div>
  </div>
</section>

<section class="s-rstats">
  <div class="wrap">
    <div class="rc-grid bl" id="counters">
      <div class="rc"><div class="n">$<span data-count="296">0</span>M</div><div class="l">external research awards last year</div></div>
      <div class="rc"><div class="n"><span data-count="50">0</span>+</div><div class="l">federally funded centers and institutes</div></div>
      <div class="rc"><div class="n"><span data-count="510">0</span></div><div class="l">patents held</div></div>
    </div>
  </div>
</section>

<section class="s-grow" id="coop" aria-label="Co-op by the numbers">
  <div class="g-track" id="gTrack">
    <div class="g-stage" id="gStage">
      <div class="g-media" id="gMedia"><video src="{V_COOP}" muted loop playsinline preload="none" data-vio></video></div>
      <div class="g-stats">
        <div class="g-stat bl"><div class="n">500,000+</div><div class="l">co&#8209;op placements, all time</div></div>
        <div class="g-stat bl"><div class="n">10,000+</div><div class="l">employer partners</div></div>
        <div class="g-stat bl"><div class="n">250+</div><div class="l">countries and territories</div></div>
      </div>
    </div>
  </div>
</section>

<section class="s-nethead">
  <div class="wrap"><h2 class="bl">Across our global campus network</h2></div>
</section>

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

<section class="s-reel" aria-hidden="true">
  <div class="reel-tilt">
    <div class="reel-track">
      <div class="vidcard"><video src="{V_HERO}" muted loop playsinline preload="none" data-vio></video></div>
      <div class="vidcard"><video src="{V_COOP}" muted loop playsinline preload="none" data-vio></video></div>
      <div class="vidcard"><video src="{V_CAMPUS}" muted loop playsinline preload="none" data-vio></video></div>
      <div class="vidcard"><video src="{V_HERO}" muted loop playsinline preload="none" data-vio></video></div>
      <div class="vidcard"><video src="{V_COOP}" muted loop playsinline preload="none" data-vio></video></div>
      <div class="vidcard"><video src="{V_CAMPUS}" muted loop playsinline preload="none" data-vio></video></div>
      <div class="vidcard"><video src="{V_HERO}" muted loop playsinline preload="none" data-vio></video></div>
      <div class="vidcard"><video src="{V_COOP}" muted loop playsinline preload="none" data-vio></video></div>
      <div class="vidcard"><video src="{V_CAMPUS}" muted loop playsinline preload="none" data-vio></video></div>
      <div class="vidcard"><video src="{V_HERO}" muted loop playsinline preload="none" data-vio></video></div>
      <div class="vidcard"><video src="{V_COOP}" muted loop playsinline preload="none" data-vio></video></div>
      <div class="vidcard"><video src="{V_CAMPUS}" muted loop playsinline preload="none" data-vio></video></div>
      <div class="vidcard"><video src="{V_HERO}" muted loop playsinline preload="none" data-vio></video></div>
      <div class="vidcard"><video src="{V_COOP}" muted loop playsinline preload="none" data-vio></video></div>
      <div class="vidcard"><video src="{V_CAMPUS}" muted loop playsinline preload="none" data-vio></video></div>
      <div class="vidcard"><video src="{V_HERO}" muted loop playsinline preload="none" data-vio></video></div>
      <div class="vidcard"><video src="{V_COOP}" muted loop playsinline preload="none" data-vio></video></div>
      <div class="vidcard"><video src="{V_CAMPUS}" muted loop playsinline preload="none" data-vio></video></div>
    </div>
  </div>
</section>

<section class="voices-c" id="voices" aria-label="Student voices">
  <div class="wrap vc">
    <div class="vc-media">{_vc_imgs}</div>
    <div class="vc-flow" id="vcFlow">
{_vc_blocks}    </div>
  </div>
</section>

"""

WIRE_FOOT = f"""
<section class="wire foot" aria-label="Latest from Northeastern Global News">
  <div class="wire-in">
    <span class="w-label">{NGN_LOGO}</span>
    <div class="w-belt"><div class="w-track">{ticker_items(TICKER)}{ticker_items(TICKER)}</div></div>
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

/* ============ pillar videos: load and play only while on screen ============ */
const vio = new IntersectionObserver(es => es.forEach(e => {
  const v = e.target;
  if (e.isIntersecting) {
    if (!v.dataset.loaded) { v.dataset.loaded = "1"; v.load(); }
    if (!reduceMotion) v.play().catch(() => {});
  } else v.pause();
}), { rootMargin: "200px" });
$$("video[data-vio]").forEach(v => vio.observe(v));

/* ============ statement text: blur in on arrival ============ */
const blIO = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add("in"); blIO.unobserve(e.target); }
}), { threshold: 0.3 });
$$(".bl").forEach(el => { if (!el.closest(".g-stats")) blIO.observe(el); });

/* ============ co-op film grows to fill, stats blur in ============ */
const gTrack = $("#gTrack"), gMedia = $("#gMedia"), gStage = $("#gStage");
if (gTrack && !reduceMotion) {
  const gStats = $$(".g-stats .g-stat");
  const easeIO2 = t => t < .5 ? 2*t*t : 1 - Math.pow(-2*t + 2, 2) / 2;
  const gUpd = () => {
    const r = gTrack.getBoundingClientRect();
    const p = clamp01((innerHeight - r.top) / r.height);
    const e = easeIO2(clamp01(p / .45));
    gMedia.style.width = (62 + 38 * e) + "vw";
    gMedia.style.height = (60 + 40 * e) + "svh";
    gMedia.style.borderRadius = (18 * (1 - e)) + "px";
    gStage.classList.toggle("dim", p > .47);
    [.52, .66, .80].forEach((t, i) => gStats[i].classList.toggle("in", p > t));
  };
  addEventListener("scroll", () => requestAnimationFrame(gUpd), { passive: true });
  addEventListener("resize", gUpd);
  gUpd();
} else if (gTrack) {
  $$(".g-stats .g-stat").forEach(el => el.classList.add("in"));
  gStage.classList.add("dim");
}

/* ============ research rail: one card open, rotating ============ */
const rbRow = document.querySelector(".rb");
if (rbRow) {
  const rbCards = $$(".rb a");
  let rbCur = 0, rbTimer = null, rbHover = false, rbSeen = false;
  const openCard = i => { rbCur = i; rbCards.forEach((c, j) => {
    c.classList.toggle("on", j === i); c.setAttribute("aria-expanded", j === i ? "true" : "false"); }); };
  const rbArm = () => {
    if (rbTimer) clearInterval(rbTimer);
    if (reduceMotion || innerWidth <= 820) return;
    rbTimer = setInterval(() => { if (!rbHover && rbSeen) openCard((rbCur + 1) % rbCards.length); }, 4000);
  };
  rbCards.forEach((c, i) => c.addEventListener("click", e => {
    if (innerWidth > 820 && !c.classList.contains("on")) { e.preventDefault(); openCard(i); rbArm(); }
  }));
  rbRow.addEventListener("mouseenter", () => { rbHover = true; });
  rbRow.addEventListener("mouseleave", () => { rbHover = false; });
  rbRow.addEventListener("focusin", () => { rbHover = true; });
  rbRow.addEventListener("focusout", () => { rbHover = false; });
  new IntersectionObserver(es => es.forEach(e => { rbSeen = e.isIntersecting; }), { threshold: .25 }).observe(rbRow);
  rbArm();
  addEventListener("resize", rbArm);
}

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

/* ============ hero phrases rotate through the stakeholders ============ */
const rphrases = $$(".rphrase");
if (rphrases.length > 1 && !reduceMotion) {
  let ri = 0;
  setInterval(() => {
    ri = (ri + 1) % rphrases.length;
    rphrases.forEach((p, i) => p.classList.toggle("on", i === ri));
  }, 3800);
}

/* ============ portrait quotes follow the reader ============ */
const vcFlow = $("#vcFlow");
if (vcFlow) {
  const vcQs = $$(".vc-q"), vcImgs = $$(".vc-vid");
  let vcCur = 0;
  const vcUpd = () => {
    const mid = innerHeight / 2;
    let best = 0, bestD = Infinity;
    vcQs.forEach((q, i) => {
      const r = q.getBoundingClientRect();
      const d = Math.abs(r.top + r.height / 2 - mid);
      if (d < bestD) { bestD = d; best = i; }
    });
    if (best !== vcCur) {
      vcCur = best;
      vcQs.forEach((q, i) => q.classList.toggle("on", i === best));
      vcImgs.forEach((im, i) => im.classList.toggle("on", i === best));
    }
  };
  addEventListener("scroll", () => requestAnimationFrame(vcUpd), { passive: true });
  addEventListener("resize", vcUpd);
  vcUpd();
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

page = (head + nav_css + hero_css + overlay_css + sheet_css + NEW_CSS + "\n" + imax_css + tailcss
        + "</style>\n\n<body>\n\n"
        + header_mk + hero_mk + NEW_BODY + rest_mk + WIRE_FOOT + footer_mk + "\n"
        + lenis + "\n<script>\n" + land + "\n" + coops + "\n" + helpers + globedata + engine + counters_js + NEW_JS + "\n" + tail_js + NEW_BOOT + "</script>\n")

assert page.count("<header") == 1 and page.count("<footer>") == 1
assert page.count("<video") == 23  # hero, grow film, 18 reel cells, 3 quote-panel films
for tok in ['id="srch"', 'id="tkv"', "rb-main", "rb-strip", "rb-cap", "s-grow", "g-stat", "n-copy", "rotor", "rphrase", "ARCS",
            "makeGlobe", "setCampuses", 'id="vcFlow"', "lifeimax", "lz-track", 'class="admit"',
            "aria-expanded", "s-reel", "vc-vid",
            "wire top", "wire foot", "concept5-rev", 'content="1"', "data-count", "newspost",
            "magnons-quantum-computing-research", 'href="#campuses"']:
    assert tok in page, tok
for gone in ["vtag", "s-scrub", "s-mask", "scrubVid", "s-bridge", "tk-cell", "s-sticky",
             "s-collage", "s-accordion", "lab-open", "data-drift", "o-name", "o-step", "nuinSub", "o-grid", "o-pin", "vc-clip", "vc-img", "o-tab", "gt-card", "gtc-", "oTabs"]:
    assert gone not in page, gone
for out in OUT:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(page)
print("built", len(page), "bytes ->", OUT[0])
