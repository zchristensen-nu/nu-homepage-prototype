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
tailcss     = cut("  /* ---------- STUDENT LIFE IMAX ---------- */", "</style>")

header_mk   = cut("<header", '<section class="hero"')
hero_mk     = cut('<section class="hero"', '<div class="scrolly"')
rest_mk     = cut('<section class="lifezoom lifeimax"', "<footer>")
footer_mk   = cut("<footer>", "</footer>", True)
assert '<section class="admit"' in rest_mk

lenis       = cut("<script>/* Lenis", "</script>", True)
land        = re.search(r"const LAND=\[.*?\];", src).group(0)
coops       = re.search(r"const COOPS=\[.*?\];", src).group(0)
helpers     = cut("/* ============ shared helpers ============ */", "/* ============ globe data ============ */")
globedata   = cut("/* ============ globe data ============ */", "/* ============ globe engine ============ */")
engine      = cut("/* ============ globe engine ============ */", "/* ============ scrollytelling ============ */")
counters_js = cut("/* ============ research counters ============ */", "/* ============ research expanding row ============ */")
tail_js     = cut("/* ============ subtle scroll movement ============ */", "/* ============ boot ============ */")

# engine: slow spin, dots always lit, factory-wrapped for the inset
assert engine.count("tgt.lon += 0.03;") == 1
engine = engine.replace("tgt.lon += 0.03;", "tgt.lon += 0.02;")
old_ign = "      ignite = reduceMotion ? 1 : easeOut(p);\n"
assert engine.count(old_ign) == 1
engine = engine.replace(old_ign, "")
assert engine.count('const canvas = $("#globe");') == 1
engine = engine.replace('const canvas = $("#globe");', 'const canvas = stageEl.querySelector("canvas");')
assert engine.count('.observe($("#stage"))') == 1
engine = engine.replace('.observe($("#stage"))', '.observe(stageEl)')
assert engine.count('$("#stage").appendChild(gtip)') == 1
engine = engine.replace('$("#stage").appendChild(gtip)', 'stageEl.appendChild(gtip)')
engine = ("function makeGlobe(stageEl, opts) {\n"
          + engine +
          "\nObject.assign(tgt, opts.layers); Object.assign(cur, opts.layers);\n"
          "tgt.k = opts.k || 1.02; cur.k = tgt.k;\n"
          "if (opts.lon !== undefined) cur.lon = tgt.lon = opts.lon;\n"
          "if (opts.lat !== undefined) cur.lat = tgt.lat = opts.lat;\n"
          "resize();\n"
          "requestAnimationFrame(frame);\n"
          "}\n")

head = head.replace('<meta name="prototype-rev" content="53">',
                    '<meta name="concept4-rev" content="1">')
assert 'concept4-rev' in head

old_h = "<h2>Class is only half of it.</h2>"
assert rest_mk.count(old_h) == 1
rest_mk = rest_mk.replace(old_h, "<h2>And then there’s everything else.</h2>")

for name in ("header_mk", "hero_mk", "rest_mk", "footer_mk"):
    v = (globals()[name].replace('src="img/', 'src="../img/')
         .replace("url('img/", "url('../img/").replace('src="hero.mp4"', 'src="../hero.mp4"'))
    globals()[name] = v

NGN = "https://news.northeastern.edu"
U = NGN + "/wp-content/uploads"
V_CAMPUS = "https://www.northeastern.edu/wp-content/uploads/Jamie-Wong-Video-Fade.mp4"
V_COOP   = "https://www.northeastern.edu/wp-content/uploads/The-Co-Op-Experience_Video-2-Fusion-v3.mp4"
V_HERO   = "../hero.mp4"

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

FACILITIES = [
 (U+"/2023/11/081423_MM_EXP_Robots_048.jpg", "EXP",
  "Eight floors of maker space and robotics, open to every major.",
  "/2023/11/27/experiential-robotics-institute-exp/"),
 (U+"/2026/05/052126_MM_Physical_AI_Research_Initiative_Event_001.jpg", "ISEC",
  "Home of the Physical AI initiative and interdisciplinary science.",
  "/2026/05/21/robo-demo/"),
 ("../img/colosseum.jpg", "Colosseum, Burlington",
  "The wireless network emulator where 6G research runs day and night.",
  "/2024/01/12/tech-savvy/"),
]

AUDIENCES = [
 ("Students and families",
  "See how a degree built around real work changes the first day of your career.",
  [("Undergraduate Admissions","https://admissions.northeastern.edu/"),
   ("Plan a visit","https://admissions.northeastern.edu/visit/"),
   ("Financial Services","https://studentfinance.northeastern.edu/")]),
 ("School counselors",
  "Help students weigh a research university where the degree includes professional experience on three continents.",
  [("Admissions overview","https://www.northeastern.edu/admissions/"),
   ("Campus visits","https://admissions.northeastern.edu/visit/")]),
 ("Faculty candidates",
  "$296M in external awards last year, 50+ federally funded centers, and facilities built for work that leaves the lab.",
  [("Research at Northeastern","https://research.northeastern.edu/"),
   ("Institutes and centers","https://research.northeastern.edu/institutes-and-centers/"),
   ("Office of the Provost","https://provost.northeastern.edu/")]),
 ("Employers and talent teams",
  "Co-op is a hiring engine: students join your team full time, and new cohorts arrive twice a year.",
  [("Hire co-op talent","https://careers.northeastern.edu/employers/"),
   ("How co-op works","https://www.northeastern.edu/co-op")]),
 ("Journalists and podcasters",
  "Our newsroom publishes daily and our faculty take calls.",
  [("Northeastern Global News","https://news.northeastern.edu/"),
   ("Faculty experts","https://news.northeastern.edu/faculty-experts/"),
   ("Media inquiries","https://news.northeastern.edu/media-inquiries/")]),
]

QUOTES = [
 ("../img/microscopy-coop.jpg", "center 30%",
  ["&ldquo;I really enjoyed the process of research from my previous co‑op.",
   "But taking a step further and working with a physical product was an evolution that I wanted to achieve.&rdquo;"],
  "Cameron D’Mello", "Bioengineering &middot; Co‑ops at Beth Israel Medical Center and QuantumScape",
  "/2025/01/24/microscopy-skills-transfer-industries/", "Read Cameron’s story"),
 ("../img/oyster-dock.jpg", "20% 35%",
  ["&ldquo;I wanted to do this job and test myself and see",
   "if I like working outdoors as much as I hoped. So far, so good.&rdquo;"],
  "Maddy Russell", "Environmental &amp; sustainability science &middot; Co‑op at Nonesuch Oyster Farm, Maine",
  "/2022/11/01/oyster-harvesting-maine/", "Read Maddy’s story"),
 ("https://news.northeastern.edu/wp-content/uploads/2023/04/CAMBODIA_coop1400.jpg", "center",
  ["&ldquo;I really wanted the chance to go out into the field.",
   "You just have to push past it, and that’s something I’ve gotten pretty good at.&rdquo;"],
  "Paris Graff", "International affairs &middot; Co‑op with the Landmine Relief Fund, Cambodia",
  "/2023/04/25/landmine-relief-fund-cambodia-co-op/", "Read Paris’s story"),
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

def facilities_cards():
    return "".join(
        f'<a class="fc" href="{NGN}{u}"><span class="fc-im"><img src="{img}" alt="" loading="lazy"></span>'
        f'<span class="fc-b"><b>{name}</b><span>{line}</span></span></a>\n'
        for img, name, line, u in FACILITIES)

def audience_rows():
    out = ""
    for name, line, links in AUDIENCES:
        ls = "".join(f'<a class="aud-l" href="{u}">{t} &#8594;</a>' for t, u in links)
        out += (f'<div class="aud rv"><div class="aud-h"><b>{name}</b><p>{line}</p></div>'
                f'<div class="aud-links">{ls}</div></div>\n')
    return out

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

  /* ---------- video pillar bands ---------- */
  .vband{position:relative;min-height:92svh;display:flex;align-items:flex-end;
    background:var(--dark);color:#fff;overflow:hidden}
  .vband video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.6)}
  .vband::after{content:"";position:absolute;inset:0;
    background:linear-gradient(to top,rgba(11,11,14,.86) 0%,rgba(11,11,14,.3) 45%,rgba(11,11,14,.12) 100%)}
  .vband .vb-in{position:relative;z-index:2;width:100%;padding:0 0 72px}
  .vb-in h2{font-size:clamp(42px,5.8vw,90px);font-weight:200;letter-spacing:-.03em;line-height:1.02}
  .vb-in .lede{margin-top:16px;max-width:52ch;color:#E5E5E5;font-size:clamp(15px,1.25vw,18px)}
  .vb-stats{margin-top:34px;display:flex;gap:clamp(24px,4vw,64px);flex-wrap:wrap}
  .vb-stat .n{font-size:clamp(30px,3.2vw,50px);font-weight:200;letter-spacing:-.02em;line-height:1}
  .vb-stat .l{margin-top:6px;font-size:13.5px;color:#C9C9CF;max-width:20ch}
  .g-inset{position:absolute;right:clamp(16px,4vw,64px);bottom:clamp(60px,9svh,110px);z-index:3;
    width:min(30vw,320px)}
  .g-inset .stage{position:relative;width:100%;aspect-ratio:1}
  .g-inset canvas{position:absolute;inset:0;width:100%;height:100%;touch-action:none;cursor:grab}
  .g-inset canvas.dragging{cursor:grabbing}
  .g-inset .gi-cap{display:block;margin-top:8px;text-align:center;font-size:12.5px;color:#C9C9CF}
  @media(max-width:900px){.g-inset{display:none}}

  /* ---------- persona duo (co-op) ---------- */
  .duo{position:relative;z-index:6;background:var(--dark);color:#fff;padding:0 0 110px}
  .duo-grid{display:grid;grid-template-columns:1fr 1fr;gap:clamp(20px,3vw,44px);margin-top:-40px;position:relative;z-index:3}
  .duo-card{background:#15151B;border:1px solid rgba(255,255,255,.1);border-radius:16px;
    padding:clamp(24px,3vw,44px)}
  .duo-card h3{font-size:clamp(21px,2vw,28px);font-weight:400;letter-spacing:-.015em}
  .duo-card p{margin-top:12px;font-size:15.5px;line-height:1.55;color:#C9C9CF;max-width:52ch}
  .duo-card .storylink{color:#fff}
  @media(max-width:820px){.duo-grid{grid-template-columns:1fr}}

  /* ---------- research landing ---------- */
  .rland{position:relative;z-index:6;background:var(--paper);padding:96px 0 120px;color:var(--ink)}
  .rc-grid{display:grid;grid-template-columns:repeat(3,1fr);
    gap:clamp(28px,4vw,64px);border-top:1px solid #E5E5E5;padding-top:48px}
  .rc{border-left:1px solid #E5E5E5;padding-left:clamp(18px,2vw,30px)}
  .rc:first-child{border-left:0;padding-left:0}
  .rc .n{font-size:clamp(48px,6vw,104px);font-weight:200;letter-spacing:-.03em;line-height:1;
    color:var(--ink);font-variant-numeric:tabular-nums;white-space:nowrap}
  .rc .l{margin-top:12px;font-size:14.5px;color:#737373;max-width:26ch}
  @media(max-width:760px){
    .rc-grid{grid-template-columns:1fr;gap:30px}
    .rc{border-left:0;padding-left:0;border-top:1px solid #E5E5E5;padding-top:22px}
    .rc:first-child{border-top:0;padding-top:0}
  }
  .fgrid{margin-top:90px;display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
  .fc{display:block;background:#fff;border:1px solid #E5E5E5;border-radius:14px;overflow:hidden;
    transition:border-color .25s}
  .fc:hover{border-color:#A3A3A3}
  .fc-im{display:block;overflow:hidden}
  .fc img{width:100%;aspect-ratio:3/2;object-fit:cover;display:block;transition:transform .8s var(--ease)}
  .fc:hover img{transform:scale(1.04)}
  .fc-b{display:block;padding:16px 18px 18px}
  .fc-b b{display:block;font-weight:600;font-size:16.5px;color:var(--ink)}
  .fc-b span{display:block;margin-top:6px;font-size:14.5px;line-height:1.5;color:#404040}
  @media(max-width:820px){.fgrid{grid-template-columns:1fr}}
  .fac-cta{margin-top:64px;border-top:1px solid #E5E5E5;padding-top:36px;
    display:flex;flex-wrap:wrap;gap:12px 36px;align-items:baseline}
  .fac-cta p{font-size:clamp(17px,1.5vw,21px);font-weight:300;color:var(--ink);max-width:44ch}

  /* ---------- audiences ---------- */
  .audience{position:relative;z-index:6;background:var(--dark);color:#fff;padding:120px 0}
  .audience .sechead h2{color:#fff}
  .aud{display:grid;grid-template-columns:7fr 5fr;gap:18px 44px;align-items:start;
    padding:34px 2px;border-top:1px solid rgba(255,255,255,.14)}
  .audlist .aud:first-of-type{margin-top:54px}
  .aud-h b{font-size:clamp(19px,1.8vw,25px);font-weight:500;letter-spacing:-.01em}
  .aud-h p{margin-top:8px;font-size:15.5px;line-height:1.55;color:#C9C9CF;max-width:52ch}
  .aud-links{display:flex;flex-direction:column;gap:10px;padding-top:6px}
  .aud-l{font-size:14.5px;font-weight:600;color:#fff}
  .aud-l:hover{color:#FFB3BE}
  @media(max-width:820px){.aud{grid-template-columns:1fr}}

  /* ---------- portrait quotes ---------- */
  .voices-c{position:relative;z-index:6;background:var(--dark);color:#fff;padding:0 0 100px}
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

NEW_BODY = f"""
<div class="grain" aria-hidden="true"></div>

<section class="wire top" aria-label="Latest from Northeastern Global News">
  <div class="wire-in">
    <span class="w-label">{NGN_LOGO}</span>
    <div class="w-belt"><div class="w-track">{ticker_items(TICKER)}{ticker_items(TICKER)}</div></div>
  </div>
</section>

<section class="vband" id="network" aria-label="The global campus network">
  <video src="{V_CAMPUS}" muted loop playsinline preload="none" data-vio></video>
  <div class="vb-in"><div class="wrap">
    <h2><span class="line"><span>The world is our campus.</span></span></h2>
    <p class="lede">Begin in Boston, Oakland, or London and move with your ambitions: fourteen campuses across the U.S., U.K., and Canada, connected as one university.</p>
    <div class="vb-stats">
      <div class="vb-stat"><div class="n">14</div><div class="l">campuses in three countries</div></div>
      <div class="vb-stat"><div class="n">4</div><div class="l">undergraduate campuses</div></div>
      <div class="vb-stat"><div class="n">8</div><div class="l">N.U.in launch cities in Europe</div></div>
    </div>
  </div></div>
  <div class="g-inset"><div class="stage">
    <canvas aria-label="Slowly spinning globe: campuses labeled in white, co-op cities as red dots. Drag to spin."></canvas>
  </div><span class="gi-cap">Campuses in white. Co‑op cities in red.</span></div>
</section>

<section class="vband" id="coop" aria-label="Experiential learning and co-op">
  <video src="{V_COOP}" muted loop playsinline preload="none" data-vio></video>
  <div class="vb-in"><div class="wrap">
    <h2><span class="line"><span>Put experience to work.</span></span></h2>
    <p class="lede">Co‑op places students in full-time, paid roles in every kind of workplace, and it has for generations.</p>
    <div class="vb-stats">
      <div class="vb-stat"><div class="n">500,000+</div><div class="l">co‑op placements, all time</div></div>
      <div class="vb-stat"><div class="n">10,000+</div><div class="l">employer partners</div></div>
      <div class="vb-stat"><div class="n">250+</div><div class="l">countries and territories</div></div>
    </div>
  </div></div>
</section>

<section class="duo">
  <div class="wrap duo-grid">
    <div class="duo-card rv">
      <h3>For students and families</h3>
      <p>Alternate semesters of classes with six months of real employment, and graduate with a résumé that already has chapters. Most co‑ops are paid; all of them count.</p>
      <a class="storylink" href="https://www.northeastern.edu/co-op">Explore co&#8209;op</a>
    </div>
    <div class="duo-card rv">
      <h3>For employers and talent teams</h3>
      <p>Co‑op is a hiring engine. Students join your team full time, contribute for six months, and new cohorts arrive twice a year, so the pipeline never sits empty. Ten thousand organizations already source talent this way.</p>
      <a class="storylink" href="https://careers.northeastern.edu/employers/">Hire co&#8209;op talent</a>
    </div>
  </div>
</section>

<section class="vband" id="research" aria-label="Research">
  <video src="{V_HERO}" muted loop playsinline preload="none" data-vio></video>
  <div class="vb-in"><div class="wrap">
    <h2><span class="line"><span>Our research story</span></span><span class="line"><span>starts in the world.</span></span></h2>
    <p class="lede">While most research institutions study the world, our faculty and students solve problems at the center of it.</p>
  </div></div>
</section>

<section class="rland">
  <div class="wrap">
    <div class="rc-grid" id="counters">
      <div class="rc"><div class="n">$<span data-count="296">0</span>M</div><div class="l">external research awards last year</div></div>
      <div class="rc"><div class="n"><span data-count="50">0</span>+</div><div class="l">federally funded centers and institutes</div></div>
      <div class="rc"><div class="n"><span data-count="510">0</span></div><div class="l">patents and counting</div></div>
    </div>
    <div class="fgrid rv">
{facilities_cards()}    </div>
    <div class="fac-cta rv">
      <p>Considering bringing your lab here? The facilities are ready and the investment is real.</p>
      <a class="storylink" href="https://research.northeastern.edu/">Research at Northeastern</a>
      <a class="storylink" href="https://provost.northeastern.edu/">Office of the Provost</a>
    </div>
  </div>
</section>

<section class="audience" id="foryou">
  <div class="wrap">
    <div class="sechead rv">
      <h2 class="display"><span class="line"><span>Come see what we mean.</span></span></h2>
    </div>
    <div class="audlist">
{audience_rows()}    </div>
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

/* ============ portrait quotes ============ */
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
/* the inset globe: every layer on, slow spin */
const gi = $(".g-inset .stage");
if (gi) makeGlobe(gi, { layers: { coops: .9, campus: 1, nuin: .5, labelC: 1, labelN: 0 }, k: 1.04, lon: -55, lat: 32 });
"""

page = (head + nav_css + hero_css + overlay_css + sheet_css + NEW_CSS + "\n" + tailcss
        + "</style>\n\n<body>\n\n"
        + header_mk + hero_mk + NEW_BODY + rest_mk + WIRE_FOOT + footer_mk + "\n"
        + lenis + "\n<script>\n" + land + "\n" + coops + "\n" + helpers + globedata + engine
        + counters_js + NEW_JS + "\n" + tail_js + NEW_BOOT + "</script>\n")

assert page.count("<header") == 1 and page.count("<footer>") == 1
assert page.count("<video") == 4  # hero + three pillar bands
for tok in ['id="srch"', 'id="tkv"', "vband", "g-inset", "makeGlobe", "duo-card",
            "For students and families", "For employers and talent teams", "Hire co",
            "fgrid", "Colosseum", "aud-l", "Journalists and podcasters", "media-inquiries",
            "faculty-experts", "careers.northeastern.edu/employers", 'id="vcFlow"',
            "wire top", "wire foot", "lifeimax", 'class="admit"', "concept4-rev",
            'content="1"', "data-count", "newspost", "The world is our campus"]:
    assert tok in page, tok
for gone in ['class="scrolly"', 'id="xrow"', "j-rail"]:
    assert gone not in page, gone
for out in OUT:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(page)
print("built", len(page), "bytes ->", OUT[0])
