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
          "const CAMPUSES_ = opts.campuses || CAMPUSES;\n"
          "const NUIN_ = opts.nuin || NUIN;\n"
          + engine +
          "\nObject.assign(tgt, opts.layers); Object.assign(cur, opts.layers);\n"
          "tgt.k = opts.k || 1.02; cur.k = tgt.k;\n"
          "if (opts.lon !== undefined) cur.lon = tgt.lon = opts.lon;\n"
          "if (opts.lat !== undefined) cur.lat = tgt.lat = opts.lat;\n"
          "resize();\n"
          "requestAnimationFrame(frame);\n"
          "return { fly: startFly, layers: function(o){ Object.assign(tgt, o); } };\n"
          "}\n")
counters_js = cut("/* ============ research counters ============ */", "/* ============ research expanding row ============ */")
tail_js     = cut("/* ============ subtle scroll movement ============ */", "/* ============ boot ============ */")
i0 = tail_js.find("/* student life imax:"); i1 = tail_js.find("/* smooth scrolling via Lenis")
assert 0 < i0 < i1
tail_js = tail_js[:i0] + tail_js[i1:]


head = head.replace('<meta name="prototype-rev" content="53">',
                    '<meta name="concept4-rev" content="11">')
assert 'concept4-rev' in head


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
  @media (prefers-reduced-motion: reduce){
    .grain{animation:none}
    .line > span{transform:none;transition:none}
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

  /* ---------- the stream: one dark continuum ---------- */
  body{background:var(--dark)}
  .vidcard{position:relative;border-radius:14px;overflow:hidden;background:#141419}
  .vidcard video{width:100%;height:100%;object-fit:cover;display:block}

  /* streams: text / video / text / video conveyor rows */
  .streams{position:relative;z-index:2;color:#fff;padding:clamp(72px,9vh,120px) 0;overflow:hidden}
  .tk-row{display:flex;gap:22px;width:max-content;align-items:center;margin-top:26px;
    animation:stripX 46s linear infinite}
  .streams:hover .tk-row{animation-play-state:paused}
  @keyframes stripX{to{transform:translateX(-50%)}}
  .tk-cell{flex:0 0 auto}
  .tk-cell .vidcard{width:clamp(260px,30vw,460px);aspect-ratio:16/10}
  @media (prefers-reduced-motion: reduce){.tk-row{animation:none;overflow-x:auto;width:auto}}

  /* sticky video, stats pass by, ghost word behind */
  .s-sticky{position:relative;z-index:1;color:#fff;padding:clamp(100px,14vh,200px) 0 clamp(80px,12vh,160px)}
  .stk{position:relative;z-index:2;display:grid;grid-template-columns:6fr 6fr;gap:clamp(28px,5vw,84px);align-items:start}
  .stk-media{position:sticky;top:18svh}
  .stk-media .vidcard{aspect-ratio:4/5;max-height:62svh}
  .stk-flow .beat{min-height:62svh;display:flex;flex-direction:column;justify-content:center}
  .beat .n{font-size:clamp(64px,9vw,150px);font-weight:200;letter-spacing:-.035em;line-height:.95;
    font-variant-numeric:tabular-nums;white-space:nowrap}
  .beat .l{margin-top:10px;font-size:15px;color:#A9A9B2}
  @media(max-width:820px){.stk{grid-template-columns:1fr}.stk-media{position:static}.stk-flow .beat{min-height:0;padding:30px 0}}

  /* the tunnel: names and films alternate on the rail */
  .s-orbit{position:relative;z-index:2;color:#fff}
  .o-grid{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr)}
  .o-steps{position:relative;z-index:2;padding-left:clamp(20px,6vw,90px)}
  .o-step{min-height:100svh;display:flex;flex-direction:column;justify-content:center;
    gap:clamp(18px,3svh,30px)}
  .o-step h2{margin:0;font-size:clamp(52px,6.5vw,110px);font-weight:200;
    letter-spacing:-.035em;line-height:1}
  .o-step .vidcard{width:114%;max-width:none;aspect-ratio:16/10}
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
    .o-step{min-height:52svh}
    .o-step h2{font-size:clamp(40px,10vw,60px)}
    .o-step .vidcard{width:100%}
  }
  /* collage: drifting films over the same dark ground, counters between */
  .s-collage{position:relative;z-index:1;color:#fff;padding:clamp(90px,12svh,180px) 0 clamp(110px,14svh,200px);overflow:visible}
  .col-grid{position:relative;z-index:2;display:grid;grid-template-columns:7fr 5fr;gap:clamp(28px,5vw,80px);align-items:start}
  .col-a .vidcard{aspect-ratio:16/10}
  .col-b{margin-top:clamp(90px,16vw,260px)}
  .col-b .vidcard{aspect-ratio:4/5;width:82%}
  .col-cap{margin-top:12px;font-size:13.5px;color:#A9A9B2}
  .col-side{margin:0;font-weight:200;font-size:clamp(34px,4.6vw,68px);line-height:1.02;letter-spacing:-.01em;color:#EDEDF2;max-width:7em}
  .rc-grid{position:relative;z-index:2;display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(24px,3vw,48px);
    border-top:1px solid rgba(255,255,255,.14);padding-top:40px;margin-top:64px}
  .rc{border-left:1px solid rgba(255,255,255,.14);padding-left:clamp(18px,2vw,30px)}
  .rc:first-child{border-left:0;padding-left:0}
  .rc .n{font-size:clamp(40px,4.6vw,76px);font-weight:200;letter-spacing:-.03em;line-height:1;
    color:#fff;font-variant-numeric:tabular-nums;white-space:nowrap}
  .rc .l{margin-top:10px;font-size:14px;color:#A9A9B2;max-width:26ch}
  @media(max-width:820px){
    .col-grid{grid-template-columns:1fr}.col-b{margin-top:0}.col-b .vidcard{width:100%}
    .rc-grid{grid-template-columns:1fr;gap:26px}
    .rc{border-left:0;padding-left:0;border-top:1px solid rgba(255,255,255,.14);padding-top:20px}
    .rc:first-child{border-top:0;padding-top:0}
    [data-drift]{transform:none !important}
  }

  /* accordion: labels run along the slat edge, not on pills */
  .s-accordion{position:relative;z-index:2;color:#fff;padding:12svh 0 16svh}
  .acc{display:flex;gap:14px;height:min(64svh,620px)}
  .acc .cell{position:relative;flex:1;border-radius:16px;overflow:hidden;cursor:pointer;
    transition:flex .55s var(--ease);background:#141419}
  .acc .cell video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
    filter:brightness(.7);transition:filter .5s}
  .acc .cell:hover{flex:3.2}
  .acc .cell:hover video{filter:none}
  .acc .lab{position:absolute;left:16px;top:16px;z-index:2;writing-mode:vertical-rl;
    font-size:15.5px;font-weight:600;color:#fff;letter-spacing:.01em;
    text-shadow:0 1px 12px rgba(0,0,0,.65);transition:opacity .3s}
  .acc .lab-open{position:absolute;left:18px;bottom:16px;z-index:2;font-size:clamp(22px,2.2vw,34px);
    font-weight:300;letter-spacing:-.015em;color:#fff;opacity:0;transform:translateY(8px);
    transition:opacity .4s var(--ease),transform .4s var(--ease);text-shadow:0 1px 14px rgba(0,0,0,.6)}
  .acc .cell:hover .lab{opacity:0}
  .acc .cell:hover .lab-open{opacity:1;transform:none}
  @media(max-width:820px){.acc{flex-direction:column;height:auto}
    .acc .cell{aspect-ratio:16/9;flex:none !important}
    .acc .lab{writing-mode:horizontal-tb}}
"""

NEW_BODY = f"""
<div class="grain" aria-hidden="true"></div>

<section class="wire top" aria-label="Latest from Northeastern Global News">
  <div class="wire-in">
    <span class="w-label">{NGN_LOGO}</span>
    <div class="w-belt"><div class="w-track">{ticker_items(TICKER)}{ticker_items(TICKER)}</div></div>
  </div>
</section>

<section class="streams" id="stream" aria-label="The university in motion">
  <div class="tk-row">
    <div class="tk-cell"><div class="vidcard"><video src="{V_HEROSM}" muted loop playsinline preload="none" data-vio></video></div><p class="col-cap">Boston</p></div>
    <div class="tk-cell"><div class="vidcard"><video src="{V_COOPSM}" muted loop playsinline preload="none" data-vio></video></div><p class="col-cap">On co&#8209;op</p></div>
    <div class="tk-cell"><div class="vidcard"><video src="{V_JAMIESM}" muted loop playsinline preload="none" data-vio></video></div><p class="col-cap">Oakland</p></div>
    <div class="tk-cell"><div class="vidcard"><video src="{V_HEROSM}" muted loop playsinline preload="none" data-vio></video></div><p class="col-cap">Boston</p></div>
    <div class="tk-cell"><div class="vidcard"><video src="{V_COOPSM}" muted loop playsinline preload="none" data-vio></video></div><p class="col-cap">On co&#8209;op</p></div>
    <div class="tk-cell"><div class="vidcard"><video src="{V_JAMIESM}" muted loop playsinline preload="none" data-vio></video></div><p class="col-cap">Oakland</p></div>
  </div>
</section>

<section class="s-sticky" id="coop">
  <div class="wrap">
    <div class="stk">
      <div class="stk-media"><div class="vidcard"><video src="{V_COOP}" muted loop playsinline preload="none" data-vio></video></div></div>
      <div class="stk-flow">
        <div class="beat"><div class="n">500,000+</div><div class="l">co&#8209;op placements, all time</div></div>
        <div class="beat"><div class="n">10,000+</div><div class="l">employer partners</div></div>
        <div class="beat"><div class="n">250+</div><div class="l">countries and territories</div></div>
      </div>
    </div>
  </div>
</section>

<section class="s-orbit" id="campuses">
  <div class="o-grid">
    <div class="o-steps" id="oSteps">
      <div class="o-step"><h2>Boston</h2>
        <div class="vidcard"><video src="{V_HERO}" muted loop playsinline preload="none" data-vio></video></div></div>
      <div class="o-step"><h2>London</h2>
        <div class="vidcard"><video src="{V_LONDON}" muted loop playsinline preload="none" data-vio></video></div></div>
      <div class="o-step"><h2>NYC</h2>
        <div class="vidcard"><video src="{V_NYC}" muted loop playsinline preload="none" data-vio></video></div></div>
      <div class="o-step"><h2>Oakland</h2>
        <div class="vidcard"><video src="{V_CAMPUS}" muted loop playsinline preload="none" data-vio></video></div></div>
      <div class="o-step"><h2>N.U.in</h2></div>
    </div>
    <div class="o-side">
      <div class="o-pin"><div class="o-globe" id="oGlobe"><canvas></canvas></div></div>
    </div>
  </div>
</section>

<section class="s-collage" id="research">
  <div class="wrap">
    <div class="col-grid">
      <div class="col-a" data-drift="-70"><div class="vidcard"><video src="{V_CAMPUS}" muted loop playsinline preload="none" data-vio></video></div>
        <p class="col-cap">Inside the labs and institutes</p></div>
      <div class="col-b" data-drift="110"><p class="col-side">Work that leaves the building.</p></div>
    </div>
    <div class="rc-grid" id="counters">
      <div class="rc"><div class="n">$<span data-count="296">0</span>M</div><div class="l">external research awards last year</div></div>
      <div class="rc"><div class="n"><span data-count="50">0</span>+</div><div class="l">federally funded centers and institutes</div></div>
      <div class="rc"><div class="n"><span data-count="510">0</span></div><div class="l">patents and counting</div></div>
    </div>
  </div>
</section>

<section class="s-accordion" id="lanes">
  <div class="wrap">
    <div class="acc">
      <div class="cell"><video src="{V_COOP}" muted loop playsinline preload="none" data-vio></video>
        <span class="lab">Co&#8209;op</span><span class="lab-open">Co&#8209;op</span></div>
      <div class="cell"><video src="{V_HERO}" muted loop playsinline preload="none" data-vio></video>
        <span class="lab">Research</span><span class="lab-open">Research</span></div>
      <div class="cell"><video src="{V_CAMPUS}" muted loop playsinline preload="none" data-vio></video>
        <span class="lab">Campuses</span><span class="lab-open">Campuses</span></div>
      <div class="cell"><video src="{V_NYC}" muted loop playsinline preload="none" data-vio></video>
        <span class="lab">Student life</span><span class="lab-open">Student life</span></div>
    </div>
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

/* ============ 04: the scrolly returns — steps left, globe right, film over the rim ============ */
const oSteps = $("#oSteps"), oGlobeEl = $("#oGlobe");
if (oSteps && oGlobeEl) {
  const pick = n => CAMPUSES.find(c => c[2] === n);
  const CITY = [["Boston", "Boston"], ["London", "London"],
                ["NYC", "New York City"], ["Oakland", "Oakland"]]
    .map(([label, name]) => {
      const c = pick(name);
      return { lat: c[0], lon: c[1], layers: { campus: 1, nuin: 0 } };
    });
  CITY.push({ lat: 47, lon: 8, k: 1.0, layers: { campus: .25, nuin: 1 } });
  const g = makeGlobe(oGlobeEl, {
    layers: { campus: 1, labelC: 0, coops: 0, nuin: 0, labelN: 0 },
    k: 1.12, lat: CITY[0].lat, lon: CITY[0].lon
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
      const st = CITY[oCur];
      g.layers(st.layers);
      g.fly({ lat: st.lat, lon: st.lon, k: st.k || 1.12 });
    }
  };
  addEventListener("scroll", () => requestAnimationFrame(oUpd), { passive: true });
  addEventListener("resize", oUpd);
  oUpd();
}

/* ============ 05: collage drift (feedback-safe) ============ */
const driftEls = $$("[data-drift]").map(el => ({ el, d: +el.dataset.drift, ty: 0 }));
if (driftEls.length && !reduceMotion) {
  const dUpd = () => {
    const mid = innerHeight / 2;
    for (const o of driftEls) {
      const r = o.el.getBoundingClientRect();
      const c = (r.top - o.ty + r.height / 2 - mid) / innerHeight;
      o.ty = c * o.d;
      o.el.style.transform = `translateY(${o.ty.toFixed(1)}px)`;
    }
  };
  addEventListener("scroll", () => requestAnimationFrame(dUpd), { passive: true });
  addEventListener("resize", dUpd);
  dUpd();
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
        + header_mk + hero_mk + NEW_BODY + rest_mk + WIRE_FOOT + footer_mk + "\n"
        + lenis + "\n<script>\n" + land + "\n" + coops + "\n" + helpers + globedata + engine + counters_js + NEW_JS + "\n" + tail_js + NEW_BOOT + "</script>\n")

assert page.count("<header") == 1 and page.count("<footer>") == 1
assert page.count("<video") == 17  # hero + stream composition
for tok in ['id="srch"', 'id="tkv"', "tk-row", "o-step", "makeGlobe", "lab-open", "col-cap",
            "data-drift", "wire top", "wire foot", 'class="admit"',
            "concept4-rev", 'content="11"', "data-count", "newspost"]:
    assert tok in page, tok
for gone in ["vtag", "s-scrub", "s-mask", "opt\"", "scrubVid", "s-bridge", "tk-city", "o-col", "o-name"]:
    assert gone not in page, gone
for out in OUT:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(page)
print("built", len(page), "bytes ->", OUT[0])
