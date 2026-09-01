"""Concept 3: research-first, with the globe folded into the co-op rail.
Page order: hero > live NGN wire > RESEARCH platform (breadth: five fields in
the accordion, counters, an also-in-the-lab list) > the journey rail (spinning
globe + campuses stat + N.U.in + co-op photos/stats > CTA) > portrait quotes >
life > closer > wire > footer. Copy written so no section repeats another.
Deploys to concept-3/ alongside the untouched concept-2 and v1."""
import re, os

V1 = "/Users/z.christensen/environment/prototypes/northeastern-homepage-v2.html"
OUT = ["/Users/z.christensen/Projects/nu-homepage-prototype/concept-3/index.html",
       "/Users/z.christensen/environment/prototypes/concept-3/index.html"]
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
sheet_mk    = cut('<div class="sheet">', '<section class="quotes"')
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
xrow_js     = cut("/* ============ research expanding row ============ */", "/* ============ quote carousel (scroll-snap cards) ============ */")
tail_js     = cut("/* ============ subtle scroll movement ============ */", "/* ============ boot ============ */")

# engine: slow idle spin for the panel; dots always lit; counter never triggers (no #coopcount here)
assert engine.count("tgt.lon += 0.03;") == 1
engine = engine.replace("tgt.lon += 0.03;", "tgt.lon += 0.02;")
old_ign = "      ignite = reduceMotion ? 1 : easeOut(p);\n"
assert engine.count(old_ign) == 1
engine = engine.replace(old_ign, "")

# wrap the singleton engine into a per-canvas factory
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
          "}\n")

head = head.replace('<meta name="prototype-rev" content="53">',
                    '<meta name="concept3-rev" content="2">')
assert 'concept3-rev' in head

old_h = "<h2>Class is only half of it.</h2>"
assert rest_mk.count(old_h) == 1
rest_mk = rest_mk.replace(old_h, "<h2>And then there’s everything else.</h2>")

for name in ("header_mk", "hero_mk", "sheet_mk", "rest_mk", "footer_mk"):
    v = (globals()[name].replace('src="img/', 'src="../img/')
         .replace("url('img/", "url('../img/").replace('src="hero.mp4"', 'src="../hero.mp4"'))
    globals()[name] = v

NGN = "https://news.northeastern.edu"
U = NGN + "/wp-content/uploads"

# ---- research breadth: five fields in the accordion (all featured images are the stories' own)
XCARDS = [
 (U+"/2025/09/093025_MM_Field_Robotos_Lab_033.jpg",
  "A Boston Dynamics Spot robot walks alongside student researchers near ISEC.",
  "Robots walk to class here. Researchers are teaching them how",
  "/2025/10/01/walking-the-future/", "Walking the future", "Field robotics", True),
 (U+"/2026/07/072226_AS_-Calina_Copos_010.jpg",
  "A researcher in the Copos lab studies axolotl regeneration.",
  "Cracking the axolotl code: how to regrow limbs and stay young",
  "/2026/07/27/axolotl-regeneration-anti-aging/", "Regeneration research", "Biology", False),
 (U+"/2026/08/Biofuel1400.jpg",
  "Algae cultures used in AI-monitored biofuel research.",
  "Scientists put algae to work making fuel. AI keeps watch",
  "/2026/08/28/algae-biofuel-ai-research/", "Algae to energy", "Climate & energy", False),
 (U+"/2026/08/quantumsystem1400.jpg",
  "A modular quantum computing system in the lab.",
  "Quieting 'the noise' in quantum computing",
  "/2026/08/07/modular-quantum-computing-research/", "Modular quantum", "Quantum", False),
 (U+"/2026/08/TextingVote1400.jpg",
  "A phone showing a get-out-the-vote text message.",
  "Can a text message sway a voter? New research puts it to the test",
  "/2026/08/11/text-messages-get-out-the-vote/", "Get-out-the-vote study", "Social science", False),
]

ALSO_ROWS = [
 ("Graduate student studies oyster genomics to preserve biodiversity","Aug 2026","/2026/08/26/oyster-restoration-genetics-research/"),
 ("This engineer sees AI and its power constraints in a new light","Aug 2026","/2026/08/19/photonics-ai-energy/"),
 ("Helping fend off quantum computing security risks","Aug 2026","/2026/08/18/post-quantum-cryptography-cyberattacks/"),
 ("Launching satellites to unlock faster data speeds","Jul 2026","/2026/07/29/satellite-internet-6g-speeds-research/"),
 ("Aerobic fitness may be a teller of some brain health","Aug 2026","/2026/08/04/physical-activity-brain-health-impulse-control/"),
 ("A parasite is running rampant in Michigan. Will it spread?","Jul 2026","/2026/07/08/parasite-outbreak-michigan/"),
]

RAIL = [
 ("globe", 0), ("globe", 1), ("globe", 2), ("globe", 3),
 ("photo", "oyster-dock", "Harvesting oysters on Maine's Nonesuch River", "/2022/11/01/oyster-harvesting-maine/"),
 ("stat", "500,000+", "co‑op placements, all time"),
 ("photo", "apple-coop", "Developing cameras for Apple products", "/2025/01/15/apple-co-op-camera-process-engineer/"),
 ("stat", "10,000+", "employer partners"),
 ("photo", "microscopy-coop", "Microscopy, from diabetes research to EV batteries", "/2025/01/24/microscopy-skills-transfer-industries/"),
 ("stat", "250+", "countries and territories"),
 ("photo", "satellite-testbed", "A student-built satellite testbed", "/2024/10/16/high-speed-satellite-network-research/"),
 ("outro", None),
]

GLOBES = [
 ('{"set":"core","layers":{"campus":1,"labelC":1,"coops":0,"nuin":0,"labelN":0},"lon":-55,"lat":35}',
  "Four undergraduate campuses",
  "Slowly spinning globe showing the four undergraduate campuses labeled in white. Drag to spin."),
 ('{"set":"grad","layers":{"campus":1,"labelC":1,"coops":0,"nuin":0,"labelN":0},"lon":-100,"lat":42}',
  "Ten campuses with graduate programs",
  "Slowly spinning globe showing ten graduate-program campuses labeled in white. Drag to spin."),
 ('{"set":"nuin","layers":{"nuin":1,"labelN":1,"campus":0,"coops":0,"labelC":0},"lon":8,"lat":48}',
  "Eight N.U.in launch cities",
  "Slowly spinning globe showing the eight N.U.in launch cities in Europe. Drag to spin."),
 ('{"layers":{"coops":0.95,"campus":0,"nuin":0,"labelC":0,"labelN":0},"lon":-40,"lat":25}',
  "Co‑ops this fall",
  "Slowly spinning globe showing this fall's co-op cities as red dots. Drag to spin, hover a dot for details."),
]

NUIN_CITIES = ["Prague","Berlin","Thessaloniki","Dublin","Rome","Belfast","Glasgow","Madrid"]

TICKER = [
 ("Aug 28","This student toiled in aviaries, barns and pens for his co-op","/2026/08/28/wildlife-sanctuary-co-op-experience/"),
 ("Aug 28","Samantha Johnson '21, robotics CEO, to speak at Boston Convocation","/2026/08/28/samantha-johnson-convocation-alumni-speaker/"),
 ("Aug 28","Scientists put algae to work making fuel. AI keeps watch.","/2026/08/28/algae-biofuel-ai-research/"),
 ("Aug 28","Why Massachusetts banned this addictive Asian plant","/2026/08/28/kratom-ban-massachusetts/"),
 ("Aug 27","Many causes for floods, many causes for their devastation","/2026/08/27/nepal-tibet-flood/"),
 ("Aug 27","Boston convocation welcomes new Huskies to Northeastern","/2026/08/27/boston-convocation-guide-2026/"),
 ("Aug 20","Slow down and zoom in: the case for microfilm research","/2026/08/20/microfilm-research-archivist/"),
 ("Aug 12","These racing club students were given nine months to make their 'EV baby'","/2026/08/12/northeastern-electric-racing-club-2/"),
 ("Jul 29","This researcher is launching satellites to unlock faster data speeds","/2026/07/29/satellite-internet-6g-speeds-research/"),
 ("Jul 22","Northeastern graduate finds success and comfort in computer codes","/2026/07/22/ai-career-amazon-graduate/"),
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

# ---- sheet surgery: new accordion cards, giant counters, also-rows, NGN link
def xcard(img, alt, h3, url, linktext, tag, active):
    cls = "xcard active" if active else "xcard"
    return (f'''        <article class="{cls}" tabindex="0">
          <img src="{img}" alt="{alt}" loading="lazy">
          <div class="xshade"></div>
          <div class="xbody">
            <h3>{h3}</h3>
            <a class="storylink" href="{NGN}{url}">{linktext}</a>
          </div>
          <span class="xtag">{tag}</span>
        </article>\n''')

x_i0 = sheet_mk.find('<div class="xrow rv" id="xrow">')
x_i1 = sheet_mk.find("</div>\n\n      <div class=\"counters\"")
if x_i1 < 0:
    x_i1 = sheet_mk.find('</div>\n\n      <div class="counters"')
assert 0 < x_i0 < x_i1, "xrow bounds"
sheet_mk = (sheet_mk[:x_i0] + '<div class="xrow rv" id="xrow">\n'
            + "".join(xcard(*c) for c in XCARDS) + "      " + sheet_mk[x_i1:])

c_i0 = sheet_mk.find('<div class="counters" id="counters">')
c_i1 = sheet_mk.find('</div>\n      <a class="storylink', c_i0)
assert 0 < c_i0 < c_i1, "counters bounds"
RC = """<div class="rc-grid" id="counters">
        <div class="rc"><div class="n">$<span data-count="296">0</span>M</div><div class="l">external research awards last year</div></div>
        <div class="rc"><div class="n"><span data-count="50">0</span>+</div><div class="l">federally funded centers and institutes</div></div>
        <div class="rc"><div class="n"><span data-count="510">0</span></div><div class="l">patents and counting</div></div>
      """
sheet_mk = sheet_mk[:c_i0] + RC + sheet_mk[c_i1:]

also = "".join(f'<a class="n-row" href="{NGN}{u}"><span>{t}</span><span class="n-d">{d}</span></a>\n'
               for t, d, u in ALSO_ROWS)
cv = '<a class="storylink rv" style="margin-top:34px" href="https://news.northeastern.edu/2023/09/06/convocation-2023/">How our president talks about AI and being human</a>'
assert sheet_mk.count(cv) == 1
sheet_mk = sheet_mk.replace(cv, f'''<div class="also rv"><h3>Also in the lab right now</h3>
{also}</div>
      <a class="storylink rv" style="margin-top:34px" href="https://news.northeastern.edu/category/research/">Research coverage on NGN</a>''')

def ticker_items(rows):
    return "".join(f'<a class="w-item" href="{NGN}{u}"><span class="w-d">{d}</span>{t}</a>'
                   for d, t, u in rows)

def rail_panels():
    out = ""
    for p in RAIL:
        k = p[0]
        if k == "globe":
            cfg, cap, aria = GLOBES[p[1]]
            out += (f'<div class="j-panel j-globe"><div class="stage" data-cfg=\'{cfg}\'>'
                    f'<canvas aria-label="{aria}"></canvas>'
                    f'</div><span class="j-caption">{cap}</span></div>\n')
        elif k == "nuin":
            cities = "".join(f"<span>{c}</span>" for c in NUIN_CITIES)
            out += ('<div class="j-panel j-nuin"><span class="j-kick">N.U.in launch cities</span>'
                    f'<div class="j-cities">{cities}</div>'
                    '<span class="j-sub">Begin the degree at one of eight partner institutions across Europe.</span></div>\n')
        elif k == "stat":
            out += (f'<div class="j-panel j-stat"><div><span class="g-n">{p[1]}</span>'
                    f'<span class="g-l">{p[2]}</span></div></div>\n')
        elif k == "photo":
            _, img, t, u = p
            out += (f'<a class="j-panel j-photo" href="{NGN}{u}">'
                    f'<img src="../img/{img}.jpg" alt="" loading="lazy">'
                    f'<span class="j-cap"><span class="j-cap-t">{t}</span>'
                    f'<span class="j-cap-r">Read on NGN &#8594;</span></span></a>\n')
        elif k == "outro":
            out += ('<div class="j-panel j-outro"><div>'
                    '<span class="j-big">Where will yours be?</span>'
                    '<a class="pill ghostw" style="margin-top:26px" href="#admit">Start at Northeastern</a>'
                    '</div></div>\n')
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

NEW_CSS = """  /* ---------- concept-3 layer ---------- */
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
  .wire.top{border-bottom:0;margin-top:-28px;border-radius:28px 28px 0 0;padding-bottom:28px}
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

  /* ---------- research add-ons ---------- */
  .rc-grid{display:grid;grid-template-columns:repeat(3,1fr);
    gap:clamp(28px,4vw,64px);border-top:1px solid #E5E5E5;padding-top:48px;margin-top:70px}
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
  .also{margin-top:90px}
  .also h3{font-size:clamp(22px,2.4vw,32px);font-weight:300;letter-spacing:-.02em;color:var(--ink);margin-bottom:14px}
  .also .n-row{display:flex;justify-content:space-between;gap:18px;align-items:baseline;
    padding:16px 2px;border-top:1px solid #E5E5E5;font-size:15.5px;color:#404040;line-height:1.35}
  .also .n-row:hover{color:var(--ink);text-decoration:underline;text-underline-offset:3px}
  .also .n-d{flex:0 0 auto;font-size:12px;color:#737373}
  .xcard img{object-position:50% 32%}

  /* ---------- the journey rail ---------- */
  .journey{position:relative;z-index:5;background:var(--dark);color:#fff}
  .j-track{height:460svh}
  .j-stage{position:sticky;top:0;height:100svh;overflow:hidden;display:flex;flex-direction:column;justify-content:center}
  .j-head{padding-bottom:40px;text-align:center}
  .j-head h2{font-size:clamp(40px,5.6vw,86px);font-weight:200;letter-spacing:-.03em;line-height:1;color:#fff}
  .j-head .j-lede{margin-top:14px;font-size:14.5px;color:#A9A9B2}
  .j-rail{display:flex;gap:clamp(18px,2.4vw,36px);align-items:center;will-change:transform;
    width:max-content;padding-left:calc(50vw - min(42vw, 350px))}
  .j-panel{flex:0 0 auto;height:min(54svh,540px);border-radius:16px;overflow:hidden;
    display:flex;flex-direction:column;align-items:flex-start;justify-content:center}
  .j-stat{padding:0 clamp(20px,3vw,56px);justify-content:center}
  .g-n{display:block;font-size:clamp(56px,8vw,132px);font-weight:200;letter-spacing:-.035em;line-height:.95;color:#fff;white-space:nowrap}
  .g-l{display:block;margin-top:10px;font-size:15px;color:#A9A9B2;max-width:24ch}
  .j-photo{position:relative;background:#141419}
  .j-photo img{height:100%;width:auto;display:block}
  .j-cap{position:absolute;left:0;right:0;bottom:0;padding:44px 16px 14px;font-size:13.5px;color:#fff;
    background:linear-gradient(to top,rgba(5,5,8,.85),rgba(5,5,8,0));
    opacity:0;transform:translateY(10px);
    transition:opacity .35s var(--ease),transform .35s var(--ease)}
  .j-photo:hover .j-cap{opacity:1;transform:none}
  .j-cap-t{display:block;line-height:1.35}
  .j-cap-r{display:block;margin-top:6px;font-size:12.5px;font-weight:600;color:#fff}
  @media (hover: none){.j-cap{opacity:1;transform:none}}
  .j-globe{position:relative;width:min(84vw,700px);background:transparent;overflow:visible;
    align-items:stretch;justify-content:flex-end}
  .j-globe .stage{position:absolute;inset:0}
  .j-globe canvas{position:absolute;inset:0;width:100%;height:100%;touch-action:none;cursor:grab}
  .j-globe canvas.dragging{cursor:grabbing}
  .j-caption{position:relative;padding:0 4px;font-size:13.5px;color:#C9C9CF;z-index:2;width:100%;text-align:center}
  .j-nuin{padding:0 clamp(24px,3vw,64px)}
  .j-kick{font-size:13.5px;color:#A9A9B2}
  .j-cities{display:grid;grid-template-columns:repeat(4,auto);gap:8px 28px;margin-top:14px}
  .j-cities span{font-size:clamp(22px,2.6vw,40px);font-weight:250;letter-spacing:-.02em;color:#fff}
  .j-sub{margin-top:18px;font-size:14.5px;color:#A9A9B2;max-width:44ch}
  .j-outro{padding:0 clamp(24px,4vw,72px);justify-content:center}
  .j-big{display:block;font-size:clamp(44px,6vw,92px);font-weight:200;letter-spacing:-.03em;line-height:1;color:#fff}
  .j-bar{margin-top:40px;height:1px;background:rgba(255,255,255,.14);position:relative}
  .j-bar i{position:absolute;left:0;top:-1px;height:3px;width:0;background:var(--red)}
  @media (prefers-reduced-motion: reduce){
    .j-track{height:auto}
    .j-stage{position:static;height:auto;display:block;padding:60px 0}
    .j-rail{width:auto;overflow-x:auto;padding-left:0;transform:none !important}
    .j-bar{display:none}
  }

  /* ---------- portrait quotes ---------- */
  .voices-c{position:relative;z-index:6;background:var(--dark);color:#fff;padding:100px 0}
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

NGN_LOGO = (
 '<svg class="w-logo" viewBox="0 0 380 102" fill="none" xmlns="http://www.w3.org/2000/svg" '
 'role="img" aria-label="Northeastern Global News">'
 '<path d="M330.519 1.38965V11.2966H362.874L334.034 40.1918L341.025 47.2092L370.112 18.0525V50.9655H380V1.38965H330.519Z" fill="#C8102E"></path>'
 '<path d="M0 100.541V1.4585H17.8395L72.5255 69.4585V1.4585H92.1915V100.541H74.0636L19.6661 33.2707V100.541H0Z" fill="white"></path>'
 '<path d="M107.751 50.9931C107.751 22.0291 129.587 0 158.496 0C175.607 0 191.414 8.17321 201.824 23.2675L186.319 34.3577C178.601 22.6896 168.548 18.2315 158.496 18.2315C140.505 18.2315 127.912 31.7985 127.912 50.9931C127.912 70.1878 141.013 83.7548 159.004 83.7548C175.456 83.7548 184.712 74.0542 186.965 63.5419H157.04V46.5488H206.85C207.139 49.1081 207.207 52.0251 207.207 54.5018C207.207 79.9709 189.299 102 159.004 102C128.708 102 107.737 79.9709 107.737 51.0069L107.751 50.9931Z" fill="white"></path>'
 '<path d="M222.781 100.541V1.4585H240.621L295.307 69.4585V1.4585H314.973V100.541H296.845L242.447 33.2707V100.541H222.781V100.541Z" fill="white"></path>'
 '</svg>')

_vc_imgs, _vc_blocks = portrait_stack()

NEW_BODY = f"""
<div class="grain" aria-hidden="true"></div>

<section class="wire top" aria-label="Latest from Northeastern Global News">
  <div class="wire-in">
    <span class="w-label">{NGN_LOGO}</span>
    <div class="w-belt"><div class="w-track">{ticker_items(TICKER)}{ticker_items(TICKER)}</div></div>
  </div>
</section>

{sheet_mk}

<section class="journey" id="experience">
  <div class="j-track" id="jTrack">
    <div class="j-stage">
      <div class="wrap j-head rv">
        <h2><span class="line"><span>The world is our campus.</span></span></h2>
        <p class="j-lede">Campuses in white. Co‑op cities in red.</p>
      </div>
      <div class="j-rail" id="jRail">
{rail_panels()}      </div>
      <div class="wrap"><div class="j-bar"><i id="jBar"></i></div>
        <a class="storylink" style="color:#fff;margin-top:24px" href="https://www.northeastern.edu/co-op">Explore co&#8209;op</a>
      </div>
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

/* ============ the journey rail ============ */
const jTrack = $("#jTrack"), jRail = $("#jRail"), jBar = $("#jBar");
if (jTrack && jRail && !reduceMotion) {
  const jUpd = () => {
    const r = jTrack.getBoundingClientRect();
    const p = clamp01(-r.top / (r.height - innerHeight));
    jRail.style.transform = `translateX(${(-p * Math.max(0, jRail.scrollWidth - innerWidth)).toFixed(1)}px)`;
    if (jBar) jBar.style.width = (p * 100).toFixed(2) + "%";
  };
  addEventListener("scroll", () => requestAnimationFrame(jUpd), { passive: true });
  addEventListener("resize", jUpd);
  jUpd();
}

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
/* four themed globes on the rail */
const CORE4 = CAMPUSES.filter(c => ["Boston","Oakland","New York City","London"].includes(c[2]));
const GRAD10 = CAMPUSES.filter(c => !["Boston","Oakland","New York City","London"].includes(c[2]));
$$(".j-globe .stage").forEach(st => {
  const cfg = JSON.parse(st.dataset.cfg);
  if (cfg.set === "core") cfg.campuses = CORE4;
  if (cfg.set === "grad") cfg.campuses = GRAD10;
  makeGlobe(st, cfg);
});
"""

page = (head + nav_css + hero_css + overlay_css + sheet_css + NEW_CSS + "\n" + tailcss
        + "</style>\n\n<body>\n\n"
        + header_mk + hero_mk + NEW_BODY + rest_mk + WIRE_FOOT + footer_mk + "\n"
        + lenis + "\n<script>\n" + land + "\n" + coops + "\n" + helpers + globedata + engine
        + counters_js + xrow_js + NEW_JS + "\n" + tail_js + NEW_BOOT + "</script>\n")

assert page.count("<header") == 1 and page.count("<footer>") == 1
for tok in ['id="srch"', 'id="tkv"', 'id="xrow"', "Axolotl".lower() and "axolotl", "Modular quantum",
            "Also in the lab right now", "rc-grid", "makeGlobe", "j-cap-r",
            "The world is our campus", 'id="vcFlow"', "wire top", "wire foot", "lifeimax",
            'class="admit"', "concept3-rev", 'content="2"', "data-count", "newspost"]:
    assert tok in page, tok
for gone in ['class="scrolly"', 'id="coopcount"', "One university. Fourteen campuses."]:
    assert gone not in page, gone
seq = re.findall(r'class="j-panel (j-\w+)', page)
assert seq == ["j-globe"]*4 + ["j-photo","j-stat","j-photo","j-stat","j-photo","j-stat","j-photo","j-outro"], seq
for out in OUT:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(page)
print("built", len(page), "bytes ->", OUT[0])
print("rail:", " > ".join(seq))
