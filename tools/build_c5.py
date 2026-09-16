"""Concept 4: the video-first pivot. Full-bleed video carries each pillar
(campus network, co-op, research), the globe survives as a broadcast-style
inset, and five personas are addressed by name: students and families, faculty
candidates, employer talent teams, school counselors, media. Three videos
total; the hero montage is deliberately reused for research. Every persona
link verified 200 on 2026-09-01. Deploys to concept-4/."""
import re, os

V1 = "/Users/z.christensen/environment/prototypes/northeastern-homepage-v2.html"
OUT = ["/Users/z.christensen/Projects/nu-homepage-prototype/concept-4/index.html",
       "/Users/z.christensen/environment/prototypes/concept-4/index.html"]
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
engine = engine.replace("tgt.lon += 0.03;", "tgt.lon += 0.006;")
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
counters_js = cut("/* ============ research counters ============ */", "/* ============ research expanding row ============ */")
tail_js     = cut("/* ============ subtle scroll movement ============ */", "/* ============ boot ============ */")


head = head.replace('<meta name="prototype-rev" content="53">',
                    '<meta name="concept4-rev" content="12">')
assert 'concept4-rev' in head


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
  .rb{display:grid;grid-template-columns:minmax(0,7fr) repeat(4,minmax(0,2fr));gap:10px;
    height:min(72svh,640px)}
  .rb a{position:relative;display:block;border-radius:14px;overflow:hidden;background:#141419}
  .rb img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
    transition:transform .8s var(--ease),filter .8s var(--ease)}
  .rb-strip img{filter:brightness(.72) saturate(.9)}
  .rb a:hover img{transform:scale(1.045);filter:none}
  .rb-cap{position:absolute;left:0;right:0;bottom:0;z-index:2;margin:0;padding:26px 24px 20px;
    font-size:clamp(16px,1.5vw,21px);font-weight:500;line-height:1.3;color:#fff;
    background:linear-gradient(to top,rgba(0,0,0,.72),transparent)}
  @media(max-width:820px){
    .rb{grid-template-columns:1fr 1fr;height:auto}
    .rb-main{grid-column:1/-1;aspect-ratio:16/10}
    .rb-strip{aspect-ratio:3/4}
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
  .s-orbit{position:relative;z-index:2;color:#fff}
  .o-grid{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr)}
  .o-steps{position:relative;z-index:2;padding-left:clamp(20px,6vw,90px)}
  .o-step{min-height:88svh;display:flex;flex-direction:column;justify-content:center;
    opacity:.32;transition:opacity .5s var(--ease)}
  .o-step.on{opacity:1}
  .o-step h3{margin:0;font-size:clamp(38px,4.4vw,80px);font-weight:250;
    letter-spacing:-.03em;line-height:1.05}
  .o-sub{list-style:none;margin:0;padding:0;max-height:0;opacity:0;overflow:hidden;
    transition:max-height .7s var(--ease),opacity .7s var(--ease)}
  .o-step.on .o-sub{max-height:420px;opacity:1}
  .o-sub li{margin-top:10px;font-size:15px;color:#D4D4D4}
  .o-sub li:first-child{margin-top:18px}
  .o-side{position:relative;z-index:1}
  .o-pin{position:sticky;top:0;height:100svh;display:flex;align-items:center;justify-content:center}
  .o-globe{position:relative;width:min(46vw,76svh);aspect-ratio:1;touch-action:none;cursor:grab}
  .o-globe canvas{position:absolute;inset:0;width:100%;height:100%}
  @media (max-width:820px){
    .o-grid{display:block}
    .o-side{position:sticky;top:0;z-index:1}
    .o-pin{position:static;height:auto;padding:12px 0}
    .o-globe{width:min(72vw,38svh);margin:0 auto}
    .o-steps{padding:0 18px}
    .o-step{min-height:46svh}
    .o-step h3{font-size:clamp(32px,9vw,52px)}
  }

  /* ---------- portrait quotes ---------- */
  .voices-c{position:relative;z-index:6;background:var(--dark);color:#fff;
    padding:clamp(90px,13vh,190px) 0 100px}
  .vc{display:grid;grid-template-columns:5fr 7fr;gap:clamp(28px,5vw,84px);align-items:start}
  .vc-media{position:sticky;top:calc(50svh - min(33svh,320px));height:min(66svh,640px);
    border-radius:16px;overflow:hidden}
  .vc-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;
    transition:opacity .6s var(--ease)}
  .vc-img.on{opacity:1}
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
    out = (f'<a class="rb-main bl" href="{NGN}{u}"><img src="{img}" alt="{alt}">'
           f'<p class="rb-cap">{cap}</p></a>\n')
    for i, (img, alt, cap, u) in enumerate(RB_STRIPS):
        out += (f'      <a class="rb-strip bl d{i+1}" href="{NGN}{u}" title="{cap}" '
                f'aria-label="{cap}"><img src="{img}" alt="{alt}"></a>\n')
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
    imgs = "".join(
        f'<img class="vc-img{" on" if i == 0 else ""}" data-i="{i}" src="{q[0]}" alt="" style="object-position:{q[1]}">'
        for i, q in enumerate(QUOTES))
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
    <div class="rb">
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
  <div class="o-grid">
    <div class="o-steps" id="oSteps">
      <div class="o-step on"><h3>Undergrad</h3>
        <ul class="o-sub"><li>Boston</li><li>New York City</li><li>Oakland</li><li>London</li></ul></div>
      <div class="o-step"><h3>Graduate</h3>
        <ul class="o-sub" id="gradSub"></ul></div>
      <div class="o-step"><h3>N.U.in</h3>
        <ul class="o-sub" id="nuinSub"></ul></div>
      <div class="o-step"><h3>Global Co&#8209;op</h3></div>
    </div>
    <div class="o-side">
      <div class="o-pin"><div class="o-globe" id="oGlobe"><canvas></canvas></div></div>
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
    v.play().catch(() => {});
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
    const p = clamp01(-r.top / (r.height - innerHeight));
    const e = easeIO2(clamp01(p / .5));
    gMedia.style.width = (62 + 38 * e) + "vw";
    gMedia.style.height = (60 + 40 * e) + "svh";
    gMedia.style.borderRadius = (18 * (1 - e)) + "px";
    gStage.classList.toggle("dim", p > .52);
    [.56, .70, .84].forEach((t, i) => gStats[i].classList.toggle("in", p > t));
  };
  addEventListener("scroll", () => requestAnimationFrame(gUpd), { passive: true });
  addEventListener("resize", gUpd);
  gUpd();
} else if (gTrack) {
  $$(".g-stats .g-stat").forEach(el => el.classList.add("in"));
  gStage.classList.add("dim");
}

/* ============ the network: categories left, globe layers right ============ */
const oSteps = $("#oSteps"), oGlobeEl = $("#oGlobe");
if (oSteps && oGlobeEl) {
  const CORE = ["Boston", "New York City", "Oakland", "London"];
  const CORE4 = CAMPUSES.filter(c => CORE.includes(c[2]));
  const GRAD10 = CAMPUSES.filter(c => !CORE.includes(c[2]));
  const gradSub = $("#gradSub"), nuinSub = $("#nuinSub");
  if (gradSub) gradSub.innerHTML = GRAD10.map(c => `<li>${c[2]}</li>`).join("");
  if (nuinSub) nuinSub.innerHTML = NUIN.map(c => `<li>${c[2]}</li>`).join("");
  const CATS = [
    { arr: CORE4,  layers: { campus: 1, labelC: 1, nuin: 0, labelN: 0, coops: 0 }, lat: 45, lon: -45, k: 1.06 },
    { arr: GRAD10, layers: { campus: 1, labelC: 1, nuin: 0, labelN: 0, coops: 0 }, lat: 40, lon: -95, k: 1.04 },
    { layers: { campus: 0, labelC: 0, nuin: 1, labelN: 1, coops: 0 }, lat: 47, lon: 10, k: 1.05 },
    { layers: { campus: 0, labelC: 0, nuin: 0, labelN: 0, coops: 1 }, lat: 25, lon: -30, k: 0.98 },
  ];
  const g = makeGlobe(oGlobeEl, {
    campuses: CORE4,
    layers: { campus: 1, labelC: 1, coops: 0, nuin: 0, labelN: 0 },
    k: CATS[0].k, lat: CATS[0].lat, lon: CATS[0].lon
  });
  const els = $$("#oSteps .o-step");
  let oCur = 0;
  const oUpd = () => {
    const mid = innerHeight / 2;
    let best = 0, bestD = Infinity;
    els.forEach((el, i) => {
      const r = el.getBoundingClientRect();
      const d = Math.abs(r.top + r.height / 2 - mid);
      if (d < bestD) { bestD = d; best = i; }
    });
    if (best !== oCur) {
      oCur = best;
      els.forEach((el, i) => el.classList.toggle("on", i === best));
      const ct = CATS[best];
      if (ct.arr) g.setCampuses(ct.arr);
      g.layers(ct.layers);
      g.fly({ lat: ct.lat, lon: ct.lon, k: ct.k });
    }
  };
  addEventListener("scroll", () => requestAnimationFrame(oUpd), { passive: true });
  addEventListener("resize", oUpd);
  oUpd();
}

/* ============ portrait quotes follow the reader ============ */
const vcFlow = $("#vcFlow");
if (vcFlow) {
  const vcQs = $$(".vc-q"), vcImgs = $$(".vc-img");
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
assert page.count("<video") == 2  # hero background + the growing co-op film
for tok in ['id="srch"', 'id="tkv"', "rb-main", "rb-strip", "s-grow", "g-stat", "o-step", "o-sub",
            "makeGlobe", "setCampuses", 'id="vcFlow"', "lifeimax", "lz-track", 'class="admit"',
            "wire top", "wire foot", "concept4-rev", 'content="12"', "data-count", "newspost",
            "magnons-quantum-computing-research", 'href="#campuses"']:
    assert tok in page, tok
for gone in ["vtag", "s-scrub", "s-mask", "scrubVid", "s-bridge", "tk-cell", "s-sticky",
             "s-collage", "s-accordion", "lab-open", "data-drift", "o-name"]:
    assert gone not in page, gone
for out in OUT:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(page)
print("built", len(page), "bytes ->", OUT[0])
