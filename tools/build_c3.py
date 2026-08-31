"""Concept 2 rev 7: the elevated v1, second pass on Zach's notes.
- Rail reframed around the real campus hierarchy (flagship + 3 more undergrad
  campuses, 10 with grad programs, N.U.in), heading no longer Boston-first.
- The constellation panel becomes the v1 globe engine, slow-spinning: white
  campus labels, red co-op dots, hover tooltips, drag preserved.
- Co-op stats switch to all-time figures (labeled clearly; VERIFY before
  anyone external sees them).
- Research counters respaced; drag hint removed.
- Quote carousel rebuilt as a full-bleed cinema with line reveals.
- Student life headline replaced.
- Ticker reads the `newspost` editorial feed (photo features live in the
  separate seen-around type, which is exactly what Zach didn't want)."""
import re, os

V1 = "/Users/z.christensen/environment/prototypes/northeastern-homepage-v2.html"
OUT = ["/Users/z.christensen/Projects/nu-homepage-prototype/concept-2/index.html",
       "/Users/z.christensen/environment/prototypes/concept-2/index.html"]
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
tailcss     = cut("  /* ---------- STUDENT LIFE IMAX ---------- */", "</style>")   # imax+admit+footer

header_mk   = cut("<header", '<section class="hero"')
hero_mk     = cut('<section class="hero"', '<div class="scrolly"')
rest_mk     = cut('<section class="lifezoom lifeimax"', "<footer>")                # life + closer
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

# slow the idle spin for the panel setting
assert engine.count("tgt.lon += 0.03;") == 1
engine = engine.replace("tgt.lon += 0.03;", "tgt.lon += 0.02;")

head = head.replace('<meta name="prototype-rev" content="52">',
                    '<meta name="concept2-rev" content="7">')
assert 'concept2-rev' in head

# student life headline: students are sometimes on co-op, not in class
old_h = "<h2>Class is only half of it.</h2>"
assert rest_mk.count(old_h) == 1
rest_mk = rest_mk.replace(old_h, "<h2>Some of this you can’t major in.</h2>")

for name in ("header_mk", "hero_mk", "rest_mk", "footer_mk"):
    v = (globals()[name].replace('src="img/', 'src="../img/')
         .replace("url('img/", "url('../img/").replace('src="hero.mp4"', 'src="../hero.mp4"'))
    globals()[name] = v

NGN = "https://news.northeastern.edu"

# baked fallback for the wire: real newsposts harvested 2026-08-31
TICKER = [
 ("Aug 28","This student toiled in aviaries, barns and pens for his co-op","/2026/08/28/wildlife-sanctuary-co-op-experience/"),
 ("Aug 28","Samantha Johnson '21, robotics CEO, to speak at Boston Convocation","/2026/08/28/samantha-johnson-convocation-alumni-speaker/"),
 ("Aug 28","Scientists put algae to work making fuel. AI keeps watch.","/2026/08/28/algae-biofuel-ai-research/"),
 ("Aug 28","Why Massachusetts banned this addictive Asian plant","/2026/08/28/kratom-ban-massachusetts/"),
 ("Aug 27","Many causes for floods, many causes for their devastation","/2026/08/27/nepal-tibet-flood/"),
 ("Aug 27","Boston convocation welcomes new Huskies to Northeastern","/2026/08/27/boston-convocation-guide-2026/"),
 ("Aug 27","Everything to know about convocation 2026 at Northeastern Oakland","/2026/08/27/oakland-convocation-guide-2026/"),
 ("Aug 20","Slow down and zoom in: the case for microfilm research","/2026/08/20/microfilm-research-archivist/"),
 ("Aug 12","These racing club students were given nine months to make their 'EV baby'","/2026/08/12/northeastern-electric-racing-club-2/"),
 ("Jul 29","This researcher is launching satellites to unlock faster data speeds","/2026/07/29/satellite-internet-6g-speeds-research/"),
 ("Jul 22","Northeastern graduate finds success and comfort in computer codes","/2026/07/22/ai-career-amazon-graduate/"),
 ("Jul 16","Can network science predict the World Cup?","/2026/07/16/world-cup-final-prediction/"),
]

SHELF = [
 (NGN+"/wp-content/uploads/2025/09/093025_MM_Field_Robotos_Lab_033.jpg","Robots walk to class here. Researchers are teaching them how","Oct 2025","/2025/10/01/walking-the-future/"),
 (NGN+"/wp-content/uploads/2026/05/052126_MM_Physical_AI_Research_Initiative_Event_001.jpg","A new initiative where AI meets the physical world","May 2026","/2026/05/21/robo-demo/"),
 ("../img/sccrub-robot.jpg","A robotic arm that cleans like an elephant's trunk","Feb 2026","/2026/02/05/cleaning-robot-arm/"),
 ("../img/mars-etch.jpg","Lighter, faster, more agile: a new Mars rover","May 2026","/2026/05/21/university-rover-challenge-team/"),
 ("../img/lunabotics.jpg","Lunabotics builds a robot for the moon's surface","May 2025","/2025/05/07/moon-robot-lunabotics/"),
 ("../img/aerobat.jpg","Aerobat flies like a bat to navigate tight spaces","Sep 2024","/2024/09/23/flying-bat-robot/"),
 ("../img/colosseum.jpg","Inside Colosseum, the wireless network emulator","Jan 2024","/2024/01/12/tech-savvy/"),
 (NGN+"/wp-content/uploads/2023/11/081423_MM_EXP_Robots_048.jpg","The robotics high-bay open to every major","Nov 2023","/2023/11/27/experiential-robotics-institute-exp/"),
]

# rail: campus hierarchy, then the globe, then the all-time co-op arc
RAIL = [
 ("city", "Boston", "The flagship", "America/New_York"),
 ("city", "Oakland", "Undergraduate campus", "America/Los_Angeles"),
 ("city", "New York City", "Undergraduate campus", "America/New_York"),
 ("city", "London", "Undergraduate campus", "Europe/London"),
 ("stat", "10", "more campuses with graduate programs"),
 ("nuin", None),
 ("globe", None),
 ("photo", "oyster-dock", "Harvesting oysters on Maine's Nonesuch River", "/2022/11/01/oyster-harvesting-maine/"),
 ("stat", "500K+", "co‑ops placed, all time"),
 ("photo", "apple-coop", "Developing cameras for Apple products", "/2025/01/15/apple-co-op-camera-process-engineer/"),
 ("stat", "5,000+", "cities and towns"),
 ("photo", "microscopy-coop", "Microscopy, from diabetes research to EV batteries", "/2025/01/24/microscopy-skills-transfer-industries/"),
 ("stat", "10,000+", "employer partners"),
 ("photo", "satellite-testbed", "A student-built satellite testbed", "/2024/10/16/high-speed-satellite-network-research/"),
 ("stat", "250+", "countries and territories"),
 ("photo", "oyster-coop", None, None),
 ("outro", None),
]

NUIN_CITIES = ["Prague","Berlin","Thessaloniki","Dublin","Rome","Belfast","Glasgow","Madrid"]

def ticker_items(rows):
    return "".join(f'<a class="w-item" href="{NGN}{u}"><span class="w-d">{d}</span>{t}</a>'
                   for d, t, u in rows)

def rail_panels():
    out = ""
    for p in RAIL:
        k = p[0]
        if k == "city":
            _, name, role, tz = p
            out += (f'<div class="j-panel j-city"><span class="j-country">{role}</span>'
                    f'<span class="j-name">{name}</span>'
                    f'<span class="j-time" data-tz="{tz}">--:--</span></div>\n')
        elif k == "stat":
            out += (f'<div class="j-panel j-stat"><div><span class="g-n">{p[1]}</span>'
                    f'<span class="g-l">{p[2]}</span></div></div>\n')
        elif k == "nuin":
            cities = "".join(f"<span>{c}</span>" for c in NUIN_CITIES)
            out += ('<div class="j-panel j-nuin"><span class="j-country">N.U.in launch cities</span>'
                    f'<div class="j-cities">{cities}</div>'
                    '<span class="j-sub">First semester, first stamp in the passport.</span></div>\n')
        elif k == "globe":
            out += ('<div class="j-panel j-globe"><div class="stage" id="stage">'
                    '<canvas id="globe" aria-label="Slowly spinning globe: campuses labeled in white, co-op cities as red dots. Drag to spin, hover a dot for details."></canvas>'
                    '</div><span class="j-caption">Campuses in white. Every red dot: Huskies on co‑op this fall.</span></div>\n')
        elif k == "photo":
            _, img, t, u = p
            if t:
                out += (f'<a class="j-panel j-photo" href="{NGN}{u}" data-cursor="Read">'
                        f'<img src="../img/{img}.jpg" alt="" loading="lazy">'
                        f'<span class="j-cap">{t}</span></a>\n')
            else:
                out += (f'<div class="j-panel j-photo"><img src="../img/{img}.jpg" alt="" loading="lazy"></div>\n')
        elif k == "outro":
            out += ('<div class="j-panel j-outro"><div>'
                    '<span class="j-big">Where will yours be?</span>'
                    '<a class="pill ghostw" style="margin-top:26px" href="#admit">Start at Northeastern</a>'
                    '</div></div>\n')
    return out

def shelf_cards():
    return "".join(
        f'<a class="shcard" href="{NGN}{u}" data-cursor="Read"><img src="{img}" alt="" loading="lazy">'
        f'<span class="b-body"><span class="b-d">{d}</span><span class="b-t">{t}</span></span></a>\n'
        for img, t, d, u in SHELF)

NEW_CSS = """  /* ---------- award layer ---------- */
  ::selection{background:var(--red);color:#fff}
  html.has-cursor, html.has-cursor a, html.has-cursor button{cursor:none}
  html.has-cursor input, html.has-cursor textarea{cursor:text}
  .grain{position:fixed;inset:-50%;z-index:400;pointer-events:none;opacity:.045;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
    animation:grain 900ms steps(3) infinite}
  @keyframes grain{0%{transform:translate(0,0)}34%{transform:translate(-2%,1%)}67%{transform:translate(1%,-2%)}100%{transform:translate(0,0)}}
  .cursor{position:fixed;left:0;top:0;z-index:500;pointer-events:none;display:none}
  html.has-cursor .cursor{display:block}
  .cursor .c-dot{position:absolute;width:6px;height:6px;border-radius:50%;background:#fff;
    transform:translate(-50%,-50%);mix-blend-mode:difference}
  .cursor .c-ring{position:absolute;width:36px;height:36px;border-radius:50%;
    border:1px solid rgba(255,255,255,.55);transform:translate(-50%,-50%) scale(1);
    transition:transform .3s var(--ease),background .3s var(--ease);mix-blend-mode:difference;
    display:flex;align-items:center;justify-content:center}
  .cursor .c-label{font-size:9px;font-weight:600;color:#000;opacity:0;transition:opacity .2s}
  .cursor.is-link .c-ring{transform:translate(-50%,-50%) scale(2.1);background:#fff}
  .cursor.is-link .c-label{opacity:1}
  .loader{position:fixed;inset:0;z-index:600;background:#050507;display:flex;
    align-items:flex-end;justify-content:space-between;padding:26px 32px;color:#fff;
    transition:transform .9s cubic-bezier(.76,0,.24,1)}
  .loader.done{transform:translateY(-101%)}
  .loader .l-n{font-size:clamp(60px,10vw,140px);font-weight:200;letter-spacing:-.03em;
    line-height:.9;font-variant-numeric:tabular-nums}
  .loader .l-t{font-size:13px;color:#A9A9B2;max-width:22ch}
  html.is-loading{overflow:hidden}
  html.is-loading .hero h1 .w{animation-play-state:paused}
  .line{display:block;overflow:hidden}
  .line > span{display:block;transform:translateY(115%);transition:transform 1s var(--ease)}
  .line.in > span, .in .line > span{transform:none}
  @media (prefers-reduced-motion: reduce){
    .grain{animation:none}
    .line > span{transform:none;transition:none}
    .loader{display:none}
  }

  /* ---------- NGN wire ---------- */
  .wire{background:var(--dark);color:#fff;overflow:hidden;position:relative;z-index:6}
  .wire.top{border-bottom:1px solid rgba(255,255,255,.1);margin-top:-28px;border-radius:28px 28px 0 0;padding-top:14px}
  .wire.foot{border-top:1px solid rgba(255,255,255,.1)}
  .wire-in{display:flex;align-items:stretch}
  .w-label{flex:0 0 auto;display:flex;align-items:center;gap:9px;padding:15px 22px;font-size:13px;
    font-weight:600;white-space:nowrap}
  .w-label::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--red);animation:wpulse 2.2s ease infinite}
  @keyframes wpulse{0%,100%{box-shadow:0 0 0 0 rgba(200,16,46,.5)}50%{box-shadow:0 0 0 7px rgba(200,16,46,0)}}
  .w-belt{overflow:hidden;flex:1;display:flex;align-items:center;
    mask-image:linear-gradient(to right,transparent,#000 40px,#000 calc(100% - 40px),transparent)}
  .w-track{display:flex;gap:44px;padding-left:44px;width:max-content;animation:wireX 80s linear infinite}
  .wire:hover .w-track{animation-play-state:paused}
  @keyframes wireX{to{transform:translateX(-50%)}}
  .w-item{display:inline-flex;align-items:baseline;gap:10px;font-size:14px;color:#E5E5E5;white-space:nowrap}
  .w-item:hover{color:#fff}
  .w-d{font-size:11.5px;color:#A9A9B2}
  @media (prefers-reduced-motion: reduce){
    .w-track{animation:none}.w-belt{overflow-x:auto}
    .w-label::before{animation:none}
  }

  /* ---------- the network journey ---------- */
  .journey{position:relative;z-index:5;background:var(--dark);color:#fff}
  .j-track{height:640svh}
  .j-stage{position:sticky;top:0;height:100svh;overflow:hidden;display:flex;flex-direction:column;justify-content:center}
  .j-head{padding-bottom:40px;text-align:center}
  .j-head h2{font-size:clamp(40px,5.6vw,86px);font-weight:200;letter-spacing:-.03em;line-height:1;color:#fff}
  .j-rail{display:flex;gap:clamp(18px,2.4vw,36px);align-items:center;will-change:transform;
    width:max-content;padding-left:100vw}
  .j-panel{flex:0 0 auto;height:min(54svh,540px);border-radius:16px;overflow:hidden;
    display:flex;flex-direction:column;align-items:flex-start;justify-content:center}
  .j-city,.j-nuin{padding:0 clamp(24px,3vw,64px)}
  .j-country{font-size:13.5px;color:#A9A9B2}
  .j-name{font-size:clamp(56px,8vw,132px);font-weight:200;letter-spacing:-.035em;line-height:1;color:#fff;margin-top:6px;white-space:nowrap}
  .j-time{font-size:clamp(20px,2vw,28px);font-weight:200;color:#C9C9CF;margin-top:12px;font-variant-numeric:tabular-nums}
  .j-cities{display:grid;grid-template-columns:repeat(4,auto);gap:8px 28px;margin-top:14px}
  .j-cities span{font-size:clamp(22px,2.6vw,40px);font-weight:250;letter-spacing:-.02em;color:#fff}
  .j-sub{margin-top:18px;font-size:14.5px;color:#A9A9B2}
  .j-stat{padding:0 clamp(20px,3vw,56px);justify-content:center}
  .g-n{display:block;font-size:clamp(56px,8vw,132px);font-weight:200;letter-spacing:-.035em;line-height:.95;color:#fff;white-space:nowrap}
  .g-l{display:block;margin-top:10px;font-size:15px;color:#A9A9B2}
  .j-photo{position:relative;background:#141419}
  .j-photo img{height:100%;width:auto;display:block}
  .j-cap{position:absolute;left:16px;bottom:14px;right:16px;font-size:13.5px;color:#fff;
    text-shadow:0 1px 14px rgba(0,0,0,.7)}
  .j-globe{position:relative;width:min(88vw,860px);background:transparent;overflow:visible;
    align-items:stretch;justify-content:flex-end}
  .j-globe .stage{position:absolute;inset:0}
  .j-globe canvas{position:absolute;inset:0;width:100%;height:100%;touch-action:none;cursor:grab}
  .j-globe canvas.dragging{cursor:grabbing}
  .j-caption{position:relative;padding:0 4px;font-size:13.5px;color:#C9C9CF;z-index:2}
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

  /* ---------- research platform ---------- */
  .research2{position:relative;z-index:6;background:#FAFAFA;padding:120px 0 110px}
  .rc-grid{margin-top:70px;display:grid;grid-template-columns:repeat(3,1fr);
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
  .shelf-head{margin-top:110px}
  .shelf-head h3{font-size:clamp(24px,2.6vw,36px);font-weight:300;letter-spacing:-.02em;color:var(--ink)}
  .shelf{margin-top:28px;display:flex;gap:20px;overflow-x:auto;padding-bottom:16px;
    scroll-snap-type:x proximity;scrollbar-width:none;cursor:grab}
  .shelf::-webkit-scrollbar{display:none}
  .shelf.dragging{cursor:grabbing;scroll-snap-type:none}
  .shcard{flex:0 0 min(340px,78vw);scroll-snap-align:start;background:#fff;border:1px solid #E5E5E5;
    border-radius:14px;overflow:hidden;transition:border-color .25s}
  .shcard:hover{border-color:#A3A3A3}
  .shcard img{width:100%;aspect-ratio:3/2;object-fit:cover;display:block}
  .b-body{display:block;padding:14px 16px 16px}
  .b-d{display:block;font-size:12px;color:#737373}
  .b-t{display:block;margin-top:5px;font-size:15.5px;line-height:1.35;color:var(--ink);font-weight:400}

  /* ---------- voices cinema ---------- */
  .voices{position:relative;z-index:6;height:92svh;min-height:620px;background:var(--dark);
    color:#fff;overflow:hidden}
  .v-slide{position:absolute;inset:0;opacity:0;transition:opacity 1s var(--ease);pointer-events:none}
  .v-slide.is-active{opacity:1;pointer-events:auto}
  .v-bg{position:absolute;inset:0;background-size:cover;background-position:center;
    filter:brightness(.52);transform:scale(1.09)}
  .v-slide.is-active .v-bg{transform:scale(1);transition:transform 8s var(--ease)}
  .v-slide::after{content:"";position:absolute;inset:0;z-index:1;pointer-events:none;
    background:linear-gradient(to top right,rgba(5,5,8,.82) 0%,rgba(5,5,8,.38) 45%,rgba(5,5,8,0) 75%)}
  .v-in{position:relative;z-index:2;display:flex;flex-direction:column;justify-content:flex-end;
    height:100%;padding-bottom:120px}
  .v-in blockquote{font-size:clamp(24px,3.3vw,46px);font-weight:300;letter-spacing:-.015em;
    line-height:1.18;max-width:24ch;text-wrap:balance}
  .v-who{margin-top:26px;font-size:15px;color:#D4D4D4}
  .v-who b{display:block;font-weight:600;color:#fff;font-size:16.5px}
  .v-in .storylink{color:#fff;font-weight:500}
  .v-ui{position:absolute;left:0;right:0;bottom:0;z-index:3;
    border-top:1px solid rgba(255,255,255,.16)}
  .v-ui .wrap{display:flex;align-items:center;gap:22px;padding-top:16px;padding-bottom:18px}
  .v-ix{font-size:13px;color:#C9C9CF;font-variant-numeric:tabular-nums;flex:0 0 auto}
  .v-bars{display:flex;gap:8px;flex:1;max-width:300px}
  .v-bars i{position:relative;height:2px;flex:1;background:rgba(255,255,255,.22);overflow:hidden}
  .v-bars i::after{content:"";position:absolute;inset:0;background:#fff;transform:scaleX(0);transform-origin:left}
  .v-bars i.done::after{transform:scaleX(1)}
  .v-bars i.run::after{animation:vfill 8s linear forwards}
  @keyframes vfill{to{transform:scaleX(1)}}
  .v-nav{margin-left:auto;display:flex;gap:10px}
  .v-btn{width:42px;height:42px;border-radius:50%;border:1px solid rgba(255,255,255,.35);
    background:transparent;color:#fff;font-size:16px;cursor:pointer;transition:.2s;
    display:flex;align-items:center;justify-content:center}
  .v-btn:hover{background:#fff;color:var(--ink);border-color:#fff}
  @media (prefers-reduced-motion: reduce){
    .v-bg{transform:none}
    .v-bars i.run::after{animation:none;transform:scaleX(1)}
  }
"""

VOICES = f"""
<section class="voices" id="voices" aria-roledescription="carousel" aria-label="Student voices">
  <div class="v-slide is-active">
    <div class="v-bg" style="background-image:url('../img/microscopy-coop.jpg');background-position:center 30%"></div>
    <div class="wrap v-in">
      <blockquote><span class="line in"><span>&ldquo;I really enjoyed the process of research from my previous co‑op.</span></span><span class="line in"><span>But taking a step further and working with a physical product was an evolution that I wanted to achieve.&rdquo;</span></span></blockquote>
      <div class="v-who"><b>Cameron D’Mello</b> Bioengineering &middot; Co‑ops at Beth Israel Medical Center and QuantumScape</div>
      <a class="storylink" href="{NGN}/2025/01/24/microscopy-skills-transfer-industries/" data-cursor="Read">Read Cameron’s story</a>
    </div>
  </div>
  <div class="v-slide">
    <div class="v-bg" style="background-image:url('../img/oyster-dock.jpg');background-position:20% 35%"></div>
    <div class="wrap v-in">
      <blockquote><span class="line"><span>&ldquo;I wanted to do this job and test myself and see</span></span><span class="line"><span>if I like working outdoors as much as I hoped. So far, so good.&rdquo;</span></span></blockquote>
      <div class="v-who"><b>Maddy Russell</b> Environmental &amp; sustainability science &middot; Co‑op at Nonesuch Oyster Farm, Maine</div>
      <a class="storylink" href="{NGN}/2022/11/01/oyster-harvesting-maine/" data-cursor="Read">Read Maddy’s story</a>
    </div>
  </div>
  <div class="v-slide">
    <div class="v-bg" style="background-image:url('https://news.northeastern.edu/wp-content/uploads/2023/04/CAMBODIA_coop1400.jpg')"></div>
    <div class="wrap v-in">
      <blockquote><span class="line"><span>&ldquo;I really wanted the chance to go out into the field.</span></span><span class="line"><span>You just have to push past it, and that’s something I’ve gotten pretty good at.&rdquo;</span></span></blockquote>
      <div class="v-who"><b>Paris Graff</b> International affairs &middot; Co‑op with the Landmine Relief Fund, Cambodia</div>
      <a class="storylink" href="{NGN}/2023/04/25/landmine-relief-fund-cambodia-co-op/" data-cursor="Read">Read Paris’s story</a>
    </div>
  </div>
  <div class="v-ui"><div class="wrap">
    <span class="v-ix" id="vIx">01 / 03</span>
    <div class="v-bars" id="vBars"><i class="run"></i><i></i><i></i></div>
    <div class="v-nav">
      <button class="v-btn" id="vPrev" aria-label="Previous quote">&#8592;</button>
      <button class="v-btn" id="vNext" aria-label="Next quote">&#8594;</button>
    </div>
  </div></div>
</section>

"""

NEW_BODY = f"""
<div class="loader" id="loader" aria-hidden="true">
  <span class="l-t">Northeastern University</span>
  <span class="l-n" id="loadn">0</span>
</div>
<div class="grain" aria-hidden="true"></div>
<div class="cursor" id="cursor" aria-hidden="true"><span class="c-ring"><span class="c-label" id="clabel">Read</span></span><span class="c-dot"></span></div>

<section class="wire top" aria-label="Latest from Northeastern Global News">
  <div class="wire-in">
    <span class="w-label">Northeastern Global News</span>
    <div class="w-belt"><div class="w-track">{ticker_items(TICKER)}{ticker_items(TICKER)}</div></div>
  </div>
</section>

<section class="journey" id="experience">
  <div class="j-track" id="jTrack">
    <div class="j-stage">
      <div class="wrap j-head rv">
        <h2><span class="line"><span>One university.</span></span><span class="line"><span>Fourteen campuses.</span></span></h2>
      </div>
      <div class="j-rail" id="jRail">
{rail_panels()}      </div>
      <div class="wrap"><div class="j-bar"><i id="jBar"></i></div>
        <a class="storylink" style="color:#fff;margin-top:24px" href="https://www.northeastern.edu/co-op" data-cursor="Visit">Explore co&#8209;op</a>
      </div>
    </div>
  </div>
</section>

<section class="research2" id="research">
  <div class="wrap">
    <div class="sechead rv">
      <h2 class="display"><span class="line"><span>Our research story</span></span><span class="line"><span>starts in the world.</span></span></h2>
      <p class="lede">Students and professors choose Northeastern because the investment is real. The numbers are one year's worth.</p>
    </div>
    <div class="rc-grid" id="counters">
      <div class="rc"><div class="n">$<span data-count="296">0</span>M</div><div class="l">external research awards last year</div></div>
      <div class="rc"><div class="n"><span data-count="50">0</span>+</div><div class="l">federally funded centers and institutes</div></div>
      <div class="rc"><div class="n"><span data-count="510">0</span></div><div class="l">patents and counting</div></div>
    </div>
    <div class="shelf-head rv"><h3>In progress right now</h3></div>
    <div class="shelf" id="shelf">
{shelf_cards()}    </div>
    <a class="storylink rv" style="margin-top:26px" href="https://news.northeastern.edu/category/research/" data-cursor="Visit">Research coverage on NGN</a>
  </div>
</section>

"""

WIRE_FOOT = f"""
<section class="wire foot" aria-label="Latest from Northeastern Global News">
  <div class="wire-in">
    <span class="w-label">Northeastern Global News</span>
    <div class="w-belt"><div class="w-track">{ticker_items(TICKER)}{ticker_items(TICKER)}</div></div>
  </div>
</section>

"""

NEW_JS = """
/* ============ preloader ============ */
const loader = $("#loader"), loadN = $("#loadn");
document.documentElement.classList.add("is-loading");
let loaderDone = false;
function finishLoader() {
  if (loaderDone) return;
  loaderDone = true;
  if (loader) { loadN.textContent = 100; loader.classList.add("done"); }
  document.documentElement.classList.remove("is-loading");
}
function runLoader() {
  if (reduceMotion || !loader) { finishLoader(); return; }
  const t0 = performance.now();
  (function step() {
    const el = (performance.now() - t0) / 1100;
    loadN.textContent = Math.min(99, Math.floor(easeOut(Math.min(1, el)) * 99));
    if ((document.readyState === "complete" || el > 2.6) && el >= 1) { setTimeout(finishLoader, 120); }
    else requestAnimationFrame(step);
  })();
}
addEventListener("load", () => setTimeout(finishLoader, 700));
setTimeout(finishLoader, 4200);
document.addEventListener("visibilitychange", () => { if (!document.hidden) setTimeout(finishLoader, 1200); });

/* ============ custom cursor ============ */
if (matchMedia("(pointer: fine)").matches && !reduceMotion) {
  document.documentElement.classList.add("has-cursor");
  const cw = $("#cursor"), clabel = $("#clabel");
  const dotEl = cw.querySelector(".c-dot"), ringEl = cw.querySelector(".c-ring");
  let cx = innerWidth / 2, cy = innerHeight / 2, rx = cx, ry = cy;
  addEventListener("mousemove", e => { cx = e.clientX; cy = e.clientY; });
  (function cloop() {
    rx += (cx - rx) * .18; ry += (cy - ry) * .18;
    dotEl.style.left = cx + "px"; dotEl.style.top = cy + "px";
    ringEl.style.left = rx + "px"; ringEl.style.top = ry + "px";
    requestAnimationFrame(cloop);
  })();
  document.addEventListener("mouseover", e => {
    const t = e.target.closest("a, button, [data-cursor]");
    cw.classList.toggle("is-link", !!t);
    if (t) clabel.textContent = t.dataset.cursor || "";
  });
}

/* ============ live NGN wire: the newspost editorial feed ============ */
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

/* ============ the network journey ============ */
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
function tickCityClocks() {
  const now = new Date();
  $$(".j-time").forEach(el => {
    el.textContent = new Intl.DateTimeFormat("en-US",
      { hour: "numeric", minute: "2-digit", timeZone: el.dataset.tz }).format(now);
  });
}

/* ============ voices cinema ============ */
const vSlides = $$(".v-slide"), vBarsEl = $("#vBars"), vIx = $("#vIx");
if (vSlides.length) {
  let vi = 0, vTimer = null;
  const bars = [...vBarsEl.children];
  function vGo(i) {
    vSlides[vi].classList.remove("is-active");
    vi = (i + vSlides.length) % vSlides.length;
    const s = vSlides[vi];
    s.classList.add("is-active");
    vIx.textContent = `0${vi + 1} / 0${vSlides.length}`;
    bars.forEach((b, j) => {
      b.classList.remove("run", "done");
      if (j < vi) b.classList.add("done");
    });
    void vBarsEl.offsetWidth;
    bars[vi].classList.add("run");
    s.querySelectorAll(".line").forEach((ln, k) => {
      ln.classList.remove("in");
      void ln.offsetWidth;
      setTimeout(() => ln.classList.add("in"), 120 + k * 130);
    });
  }
  function vRestart() { clearInterval(vTimer); if (!reduceMotion) vTimer = setInterval(() => vGo(vi + 1), 8000); }
  $("#vPrev").addEventListener("click", () => { vGo(vi - 1); vRestart(); });
  $("#vNext").addEventListener("click", () => { vGo(vi + 1); vRestart(); });
  vRestart();
}

/* ============ shelf drag ============ */
const shelf = $("#shelf");
if (shelf) {
  let down = false, sx = 0, sl = 0;
  shelf.addEventListener("pointerdown", e => { down = true; sx = e.clientX; sl = shelf.scrollLeft; shelf.classList.add("dragging"); });
  addEventListener("pointermove", e => { if (down) shelf.scrollLeft = sl - (e.clientX - sx); });
  addEventListener("pointerup", () => { down = false; shelf.classList.remove("dragging"); });
}

/* ============ clip-reveal lines (voices slides manage their own) ============ */
const lineIO = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add("in"); lineIO.unobserve(e.target); }
}), { threshold: 0.3 });
$$(".line").forEach(el => { if (!el.closest(".v-slide")) lineIO.observe(el); });
"""

NEW_BOOT = """/* ============ boot ============ */
nav.classList.toggle("solid", scrollY > 60);
runLoader();
tickCityClocks();
setInterval(tickCityClocks, 1000);
/* globe panel: slow idle spin, campuses labeled, co-op dots on */
Object.assign(tgt, { coops: .9, campus: 1, nuin: .5, labelC: 1, labelN: 0 });
Object.assign(cur, { coops: .9, campus: 1, nuin: .5, labelC: 1, labelN: 0 });
tgt.k = 1.02; cur.k = 1.02;
resize();
requestAnimationFrame(frame);
"""

page = (head + nav_css + hero_css + overlay_css + sheet_css + NEW_CSS + "\n" + tailcss
        + "</style>\n\n<body>\n\n"
        + header_mk + hero_mk + NEW_BODY + VOICES + rest_mk + WIRE_FOOT + footer_mk + "\n"
        + lenis + "\n<script>\n" + land + "\n" + coops + "\n" + helpers + globedata + engine
        + counters_js + NEW_JS + "\n" + tail_js + NEW_BOOT + "</script>\n")

assert page.count("<header") == 1 and page.count("<footer>") == 1
for tok in ['id="srch"', 'id="tkv"', "j-rail", 'id="globe"', 'id="stage"', "v-slide", 'id="shelf"',
            "wire top", "wire foot", "lifeimax", 'class="admit"', "loader", "concept2-rev",
            'content="7"', "data-count", "newspost", "500K+", "major in"]:
    assert tok in page, tok
assert "Drag to explore" not in page
assert "qtrack" not in page and "qslide" not in page
for out in OUT:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(page)
print("built", len(page), "bytes ->", OUT[0])
