"""Concept 2 rev 9, per Zach: rev 8 read as unpolished.
- The v1 globe scrolly returns WHOLE (camera flights, steps, staple story card,
  counter with dot ignition): campuses > N.U.in > co-op > outro. It replaces
  the static-globe campus section.
- The loved co-op photo/stat rail stays, after the scrolly (all-time numbers).
- Research: editorial collage that drifts around the canvas on scroll
  (asymmetric two-column flow, per-element parallax), counters kept above.
- Quotes: scroll-driven crossfade cinema (pinned stage, push-in, line reveals),
  no controls, no autoplay, no tabs.
- Keeps from rev 8: NGN-logo wire (centered, live newspost feed), loader,
  grain, clip reveals, life headline, closer, footer. No custom cursor.
"""
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
scrolly_css = cut("  /* ---------- GLOBE SCROLLY ---------- */", "  /* ---------- SHEET SECTIONS (Adobe pattern) ---------- */")  # includes srch/tkv css
sheet_css   = cut("  /* ---------- SHEET SECTIONS (Adobe pattern) ---------- */", "  /* ---------- QUOTES (large-card carousel) ---------- */")
tailcss     = cut("  /* ---------- STUDENT LIFE IMAX ---------- */", "</style>")

header_mk   = cut("<header", '<section class="hero"')
hero_mk     = cut('<section class="hero"', '<div class="scrolly"')
scrolly_mk  = cut('<div class="scrolly"', '<div class="sheet">')
rest_mk     = cut('<section class="lifezoom lifeimax"', "<footer>")
footer_mk   = cut("<footer>", "</footer>", True)
assert '<section class="admit"' in rest_mk

lenis       = cut("<script>/* Lenis", "</script>", True)
land        = re.search(r"const LAND=\[.*?\];", src).group(0)
coops       = re.search(r"const COOPS=\[.*?\];", src).group(0)
helpers     = cut("/* ============ shared helpers ============ */", "/* ============ globe data ============ */")
globedata   = cut("/* ============ globe data ============ */", "/* ============ globe engine ============ */")
engine      = cut("/* ============ globe engine ============ */", "/* ============ scrollytelling ============ */")
scrolly_js  = cut("/* ============ scrollytelling ============ */", "/* ============ research counters ============ */")
counters_js = cut("/* ============ research counters ============ */", "/* ============ research expanding row ============ */")
tail_js     = cut("/* ============ subtle scroll movement ============ */", "/* ============ boot ============ */")

head = head.replace('<meta name="prototype-rev" content="53">',
                    '<meta name="concept2-rev" content="10">')
assert 'concept2-rev' in head

old_h = "<h2>Class is only half of it.</h2>"
assert rest_mk.count(old_h) == 1
rest_mk = rest_mk.replace(old_h, "<h2>Some of this you can’t major in.</h2>")

for name in ("header_mk", "hero_mk", "scrolly_mk", "rest_mk", "footer_mk"):
    v = (globals()[name].replace('src="img/', 'src="../img/')
         .replace("url('img/", "url('../img/").replace('src="hero.mp4"', 'src="../hero.mp4"'))
    globals()[name] = v

NGN = "https://news.northeastern.edu"

NGN_LOGO = (
 '<svg class="w-logo" viewBox="0 0 380 102" fill="none" xmlns="http://www.w3.org/2000/svg" '
 'role="img" aria-label="Northeastern Global News">'
 '<path d="M330.519 1.38965V11.2966H362.874L334.034 40.1918L341.025 47.2092L370.112 18.0525V50.9655H380V1.38965H330.519Z" fill="#C8102E"></path>'
 '<path d="M0 100.541V1.4585H17.8395L72.5255 69.4585V1.4585H92.1915V100.541H74.0636L19.6661 33.2707V100.541H0Z" fill="white"></path>'
 '<path d="M107.751 50.9931C107.751 22.0291 129.587 0 158.496 0C175.607 0 191.414 8.17321 201.824 23.2675L186.319 34.3577C178.601 22.6896 168.548 18.2315 158.496 18.2315C140.505 18.2315 127.912 31.7985 127.912 50.9931C127.912 70.1878 141.013 83.7548 159.004 83.7548C175.456 83.7548 184.712 74.0542 186.965 63.5419H157.04V46.5488H206.85C207.139 49.1081 207.207 52.0251 207.207 54.5018C207.207 79.9709 189.299 102 159.004 102C128.708 102 107.737 79.9709 107.737 51.0069L107.751 50.9931Z" fill="white"></path>'
 '<path d="M222.781 100.541V1.4585H240.621L295.307 69.4585V1.4585H314.973V100.541H296.845L242.447 33.2707V100.541H222.781V100.541Z" fill="white"></path>'
 '</svg>')

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

# editorial collage: (img, title, date, url, column 1|2, width%, drift px)
RE_ITEMS = [
 (NGN+"/wp-content/uploads/2025/09/093025_MM_Field_Robotos_Lab_033.jpg","Robots walk to class here. Researchers are teaching them how","Oct 2025","/2025/10/01/walking-the-future/", 1, 100, -26, True),
 (NGN+"/wp-content/uploads/2026/05/052126_MM_Physical_AI_Research_Initiative_Event_001.jpg","A new initiative where AI meets the physical world","May 2026","/2026/05/21/robo-demo/", 2, 78, 34, False),
 ("../img/sccrub-robot.jpg","A robotic arm that cleans like an elephant's trunk","Feb 2026","/2026/02/05/cleaning-robot-arm/", 2, 88, -18, False),
 ("../img/mars-etch.jpg","Lighter, faster, more agile: a new Mars rover","May 2026","/2026/05/21/university-rover-challenge-team/", 1, 68, 42, False),
 ("../img/lunabotics.jpg","Lunabotics builds a robot for the moon's surface","May 2025","/2025/05/07/moon-robot-lunabotics/", 2, 100, -30, False),
 ("../img/aerobat.jpg","Aerobat flies like a bat to navigate tight spaces","Sep 2024","/2024/09/23/flying-bat-robot/", 1, 84, 22, False),
 ("../img/colosseum.jpg","Inside Colosseum, the wireless network emulator","Jan 2024","/2024/01/12/tech-savvy/", 2, 72, 40, False),
 (NGN+"/wp-content/uploads/2023/11/081423_MM_EXP_Robots_048.jpg","The robotics high-bay open to every major","Nov 2023","/2023/11/27/experiential-robotics-institute-exp/", 1, 76, -14, False),
]

RAIL = [
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

def ticker_items(rows):
    return "".join(f'<a class="w-item" href="{NGN}{u}"><span class="w-d">{d}</span>{t}</a>'
                   for d, t, u in rows)

def rail_panels():
    out = ""
    for p in RAIL:
        k = p[0]
        if k == "stat":
            out += (f'<div class="j-panel j-stat"><div><span class="g-n">{p[1]}</span>'
                    f'<span class="g-l">{p[2]}</span></div></div>\n')
        elif k == "photo":
            _, img, t, u = p
            if t:
                out += (f'<a class="j-panel j-photo" href="{NGN}{u}">'
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

def re_items(col):
    out = ""
    for img, t, d, u, c, w, drift, feature in RE_ITEMS:
        if c != col: continue
        cls = "re-item feature" if feature else "re-item"
        out += (f'<a class="{cls}" href="{NGN}{u}" style="width:{w}%" data-drift="{drift}">'
                f'<span class="re-im"><img src="{img}" alt="" loading="lazy"></span>'
                f'<span class="b-body"><span class="b-d">{d}</span><span class="b-t">{t}</span></span></a>\n')
    return out

def quote_slides():
    out = ""
    for i, (img, pos, lines, name, who, u, cta) in enumerate(QUOTES):
        ls = "".join(f'<span class="line"><span>{l}</span></span>' for l in lines)
        act = " is-active" if i == 0 else ""
        out += (f'<div class="v-slide{act}"><div class="v-bg" style="background-image:url(\'{img}\');background-position:{pos}"></div>'
                f'<div class="wrap v-in"><blockquote>{ls}</blockquote>'
                f'<div class="v-who"><b>{name}</b> {who}</div>'
                f'<a class="storylink" href="{NGN}{u}">{cta}</a></div></div>\n')
    return out

NEW_CSS = """  /* ---------- award layer ---------- */
  ::selection{background:var(--red);color:#fff}
  .grain{position:fixed;inset:-50%;z-index:400;pointer-events:none;opacity:.045;
    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
    animation:grain 900ms steps(3) infinite}
  @keyframes grain{0%{transform:translate(0,0)}34%{transform:translate(-2%,1%)}67%{transform:translate(1%,-2%)}100%{transform:translate(0,0)}}
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

  /* ---------- co-op rail ---------- */
  .journey{position:relative;z-index:5;background:var(--dark);color:#fff}
  .j-track{height:420svh}
  .j-stage{position:sticky;top:0;height:100svh;overflow:hidden;display:flex;flex-direction:column;justify-content:center}
  .j-head{padding-bottom:40px;text-align:center}
  .j-head h2{font-size:clamp(40px,5.6vw,86px);font-weight:200;letter-spacing:-.03em;line-height:1;color:#fff}
  .j-rail{display:flex;gap:clamp(18px,2.4vw,36px);align-items:center;will-change:transform;
    width:max-content;padding-left:100vw}
  .j-panel{flex:0 0 auto;height:min(54svh,540px);border-radius:16px;overflow:hidden;
    display:flex;flex-direction:column;align-items:flex-start;justify-content:center}
  .j-stat{padding:0 clamp(20px,3vw,56px);justify-content:center}
  .g-n{display:block;font-size:clamp(56px,8vw,132px);font-weight:200;letter-spacing:-.035em;line-height:.95;color:#fff;white-space:nowrap}
  .g-l{display:block;margin-top:10px;font-size:15px;color:#A9A9B2}
  .j-photo{position:relative;background:#141419}
  .j-photo img{height:100%;width:auto;display:block}
  .j-cap{position:absolute;left:16px;bottom:14px;right:16px;font-size:13.5px;color:#fff;
    text-shadow:0 1px 14px rgba(0,0,0,.7)}
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

  /* ---------- research: counters + editorial drift collage ---------- */
  .research2{position:relative;z-index:6;background:#FAFAFA;padding:120px 0 130px;overflow:hidden}
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
  .rghead{margin-top:120px}
  .rghead h3{font-size:clamp(24px,2.6vw,36px);font-weight:300;letter-spacing:-.02em;color:var(--ink)}
  .re-flow{margin-top:44px;display:grid;grid-template-columns:7fr 5fr;gap:clamp(24px,4vw,72px);align-items:start}
  .re-col{display:flex;flex-direction:column;gap:clamp(40px,6vw,96px)}
  .re-col.two{margin-top:clamp(60px,10vw,160px)}
  .re-item{display:block;will-change:transform}
  .re-col .re-item:nth-child(even){align-self:flex-end}
  .re-im{display:block;overflow:hidden;border-radius:14px}
  .re-item img{width:100%;aspect-ratio:3/2;object-fit:cover;display:block;transition:transform .8s var(--ease)}
  .re-item:hover img{transform:scale(1.04)}
  .re-item.feature img{aspect-ratio:16/10}
  .re-item.feature .b-t{font-size:clamp(19px,1.9vw,28px);font-weight:300;max-width:24ch}
  .b-body{display:block;padding:14px 2px 0}
  .b-d{display:block;font-size:12px;color:#737373}
  .b-t{display:block;margin-top:5px;font-size:16px;line-height:1.35;color:var(--ink);font-weight:400}
  @media(max-width:760px){
    .re-flow{grid-template-columns:1fr}
    .re-col.two{margin-top:0}
    .re-item{width:100% !important;transform:none !important}
  }

  /* ---------- voices: scroll-driven cinema ---------- */
  .voices{position:relative;z-index:6;background:var(--dark);color:#fff}
  .v-track{height:340svh}
  .v-stage{position:sticky;top:0;height:100svh;min-height:600px;overflow:hidden}
  .v-slide{position:absolute;inset:0;opacity:0;pointer-events:none;will-change:opacity}
  .v-slide.is-active{pointer-events:auto}
  .v-bg{position:absolute;inset:0;background-size:cover;filter:brightness(.52);will-change:transform}
  .v-slide::after{content:"";position:absolute;inset:0;z-index:1;pointer-events:none;
    background:linear-gradient(to top right,rgba(5,5,8,.82) 0%,rgba(5,5,8,.38) 45%,rgba(5,5,8,0) 75%)}
  .v-in{position:relative;z-index:2;display:flex;flex-direction:column;justify-content:flex-end;
    height:100%;padding-bottom:96px}
  .v-in blockquote{font-size:clamp(24px,3.3vw,46px);font-weight:300;letter-spacing:-.015em;
    line-height:1.18;max-width:24ch;text-wrap:balance}
  .v-who{margin-top:26px;font-size:15px;color:#D4D4D4}
  .v-who b{display:block;font-weight:600;color:#fff;font-size:16.5px}
  .v-in .storylink{color:#fff;font-weight:500}
  @media (prefers-reduced-motion: reduce){
    .v-track{height:auto}
    .v-stage{position:static;height:auto;overflow:visible}
    .v-slide{position:relative;opacity:1 !important;height:80svh;min-height:520px}
  }
"""

NEW_BODY = f"""
<div class="loader" id="loader" aria-hidden="true">
  <span class="l-t">Northeastern University</span>
  <span class="l-n" id="loadn">0</span>
</div>
<div class="grain" aria-hidden="true"></div>

<section class="wire" aria-label="Latest from Northeastern Global News">
  <div class="wire-in">
    <span class="w-label">{NGN_LOGO}</span>
    <div class="w-belt"><div class="w-track">{ticker_items(TICKER)}{ticker_items(TICKER)}</div></div>
  </div>
</section>
"""

AFTER_SCROLLY = f"""
<section class="journey" id="coop">
  <div class="j-track" id="jTrack">
    <div class="j-stage">
      <div class="wrap j-head rv">
        <h2><span class="line"><span>Full-time, paid and real.</span></span></h2>
      </div>
      <div class="j-rail" id="jRail">
{rail_panels()}      </div>
      <div class="wrap"><div class="j-bar"><i id="jBar"></i></div>
        <a class="storylink" style="color:#fff;margin-top:24px" href="https://www.northeastern.edu/co-op">Explore co&#8209;op</a>
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
    <div class="rghead rv"><h3>In progress right now</h3></div>
    <div class="re-flow">
      <div class="re-col one">
{re_items(1)}      </div>
      <div class="re-col two">
{re_items(2)}      </div>
    </div>
    <a class="storylink rv" style="margin-top:40px" href="https://news.northeastern.edu/category/research/">Research coverage on NGN</a>
  </div>
</section>

<section class="voices" id="voices" aria-label="Student voices">
  <div class="v-track" id="vTrack">
    <div class="v-stage">
{quote_slides()}    </div>
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

/* ============ co-op rail ============ */
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

/* ============ research collage: elements drift around the canvas ============ */
const driftEls = $$("[data-drift]").map(el => ({ el, d: +el.dataset.drift }));
if (driftEls.length && !reduceMotion) {
  const dUpd = () => {
    const mid = innerHeight / 2;
    for (const { el, d } of driftEls) {
      const r = el.getBoundingClientRect();
      const c = (r.top + r.height / 2 - mid) / innerHeight;   /* -0.5 top .. 0.5 bottom */
      el.style.transform = `translateY(${(c * d).toFixed(1)}px)`;
    }
  };
  addEventListener("scroll", () => requestAnimationFrame(dUpd), { passive: true });
  addEventListener("resize", dUpd);
  dUpd();
}

/* ============ voices: scroll-driven crossfade cinema ============ */
const vTrack = $("#vTrack"), vSlides = $$(".v-slide");
if (vTrack && vSlides.length && !reduceMotion) {
  const N = vSlides.length;
  let vActive = 0;
  const vUpd = () => {
    const r = vTrack.getBoundingClientRect();
    const p = clamp01(-r.top / (r.height - innerHeight));
    vSlides.forEach((sl, i) => {
      const t = clamp01((p - i / N) * N);
      const fadeIn = clamp01(t / 0.16);
      const fadeOut = i === N - 1 ? 1 : clamp01((1 - t) / 0.16);
      sl.style.opacity = (t <= 0 && i !== 0 ? 0 : Math.min(fadeIn, fadeOut)).toFixed(2);
      sl.querySelector(".v-bg").style.transform = `scale(${(1.05 + t * 0.05).toFixed(3)})`;
    });
    const idx = Math.min(N - 1, Math.floor(p * N));
    if (idx !== vActive) {
      vActive = idx;
      vSlides.forEach((sl, i) => sl.classList.toggle("is-active", i === idx));
      vSlides[idx].querySelectorAll(".line").forEach((ln, k) => {
        ln.classList.remove("in");
        void ln.offsetWidth;
        setTimeout(() => ln.classList.add("in"), 90 + k * 120);
      });
    }
  };
  addEventListener("scroll", () => requestAnimationFrame(vUpd), { passive: true });
  addEventListener("resize", vUpd);
  vSlides[0].querySelectorAll(".line").forEach(ln => ln.classList.add("in"));
  vUpd();
}

/* ============ clip-reveal lines (voices manage their own) ============ */
const lineIO = new IntersectionObserver(es => es.forEach(e => {
  if (e.isIntersecting) { e.target.classList.add("in"); lineIO.unobserve(e.target); }
}), { threshold: 0.3 });
$$(".line").forEach(el => { if (!el.closest(".v-slide")) lineIO.observe(el); });
"""

NEW_BOOT = """/* ============ boot ============ */
nav.classList.toggle("solid", scrollY > 60);
runLoader();
resize();
requestAnimationFrame(frame);
"""

page = (head + nav_css + hero_css + scrolly_css + sheet_css + NEW_CSS + "\n" + tailcss
        + "</style>\n\n<body>\n\n"
        + header_mk + hero_mk + NEW_BODY + scrolly_mk + AFTER_SCROLLY + rest_mk + WIRE_FOOT + footer_mk + "\n"
        + lenis + "\n<script>\n" + land + "\n" + coops + "\n" + helpers + globedata + engine
        + scrolly_js + counters_js + NEW_JS + "\n" + tail_js + NEW_BOOT + "</script>\n")

assert page.count("<header") == 1 and page.count("<footer>") == 1
for tok in ['id="srch"', 'id="tkv"', 'class="scrolly"', 'id="globe"', "gt-card", "coopcount",
            "j-rail", "w-logo", "re-flow", "data-drift", 'id="vTrack"', "v-slide",
            "wire foot", "lifeimax", 'class="admit"', "loader", "concept2-rev", 'content="10"',
            "data-count", "newspost", "500K+", "major in"]:
    assert tok in page, tok
for gone in ["Drag to explore", "g-wrap", "g-clock", "rgcard", "One university. Fourteen campuses."]:
    assert gone not in page, gone
for out in OUT:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(page)
print("built", len(page), "bytes ->", OUT[0])
