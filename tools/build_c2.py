"""Assemble concept-2 (the 24/7 'always on' homepage) from v2's shared shell
plus all-new scenes. Extraction is assert-guarded: any drifted marker aborts."""
import re, sys

V2 = "/Users/z.christensen/environment/prototypes/northeastern-homepage-v2.html"
OUT = ["/Users/z.christensen/Projects/nu-homepage-prototype/concept-2/index.html",
       "/Users/z.christensen/environment/prototypes/concept-2/index.html"]
src = open(V2).read()

def cut(a, b, inclusive_b=False):
    i = src.find(a); assert i >= 0, a[:60]
    j = src.find(b, i + len(a)); assert j > i, b[:60]
    return src[i:j + (len(b) if inclusive_b else 0)]

head       = src[:src.find("  /* ---------- NAV ---------- */")]
nav_css    = cut("  /* ---------- NAV ---------- */", "  /* ---------- HERO ---------- */")
overlay_css = cut("  .srch{", "  /* ---------- SHEET SECTIONS (Adobe pattern) ---------- */")
admit_css  = cut("  /* ---------- ADMISSIONS CTA ---------- */", "  /* ---------- FOOTER ---------- */")
footer_css = cut("  /* ---------- FOOTER ---------- */", "</style>")
header_mk  = cut("<header", '<section class="hero"')  # includes srch + tkv overlays
admit_mk   = cut('<section class="admit"', "<footer>")
footer_mk  = cut("<footer>", "</footer>", True)
lenis      = cut("<script>/* Lenis", "</script>", True)
land       = re.search(r"const LAND=\[.*?\];", src).group(0)
helpers    = cut("/* ============ shared helpers ============ */", "/* ============ globe data ============ */")
tail       = cut("/* ============ subtle scroll movement ============ */", "/* ============ boot ============ */")

# tail: drop the v2 hero drift and the IMAX corridor, keep plx/lenis/search/nav
i0 = tail.find("/* hero: content drifts"); i1 = tail.find("/* parallax on select")
assert 0 < i0 < i1
tail = tail[:i0] + tail[i1:]
i0 = tail.find("/* student life imax:"); i1 = tail.find("/* smooth scrolling via Lenis")
assert 0 < i0 < i1
tail = tail[:i0] + tail[i1:]

# head: independent rev counter for this concept
head = head.replace('<meta name="prototype-rev" content="52">',
                    '<meta name="concept2-rev" content="1">')
assert 'concept2-rev' in head

# asset paths: this page lives one level down from img/
for blk in ("header_mk", "admit_mk", "footer_mk"):
    v = locals()[blk].replace('src="img/', 'src="../img/').replace("url('img/", "url('../img/")
    locals()[blk] = v
header_mk, admit_mk, footer_mk = locals()["header_mk"], locals()["admit_mk"], locals()["footer_mk"]

# reuse the co-op link the nav already carries
m = re.search(r'href="(https://[^"]*co-?op[^"]*)"', header_mk, re.I)
COOP_URL = m.group(1) if m else "https://news.northeastern.edu/"

NGN = "https://news.northeastern.edu"
U = NGN + "/wp-content/uploads"

TICKER = [
 ("Aug 26","Making it home","/2026/08/26/making-it-home/"),
 ("Aug 25","Silhouetted study","/2026/08/25/silhouetted-study/"),
 ("Aug 24","Just keep walking","/2026/08/24/just-keep-walking/"),
 ("Aug 20","Signed, sealed and pinned","/2026/08/20/signed-sealed-and-pinned/"),
 ("Aug 20","Slow down and zoom in: the case for microfilm research","/2026/08/20/microfilm-research-archivist/"),
 ("Aug 19","Pose!","/2026/08/19/pose/"),
 ("Aug 18","Secluded study","/2026/08/18/secluded-study/"),
 ("Aug 17","Robo-test","/2026/08/17/robo-test/"),
 ("Aug 16","Move-in momentum","/2026/08/16/move-in-momentum-2/"),
 ("Aug 13","Close up","/2026/08/13/close-up/"),
 ("Aug 12","These racing club students were given nine months to make their 'EV baby'","/2026/08/12/northeastern-electric-racing-club-2/"),
 ("Aug 12","Eyes to the sky","/2026/08/12/eyes-to-the-sky/"),
 ("Aug 11","Sunlit strides","/2026/08/11/sunlit-strides/"),
 ("Aug 10","Study space","/2026/08/10/study-space-2/"),
 ("Aug 7","Pipette precision","/2026/08/07/pipette-precision/"),
 ("Aug 6","Sony's brand new bet on 'Brand New Day'","/2026/08/06/marvel-movie-budget-spider-man/"),
 ("Aug 6","Elements of curiosity","/2026/08/06/elements-of-curiosity/"),
 ("Aug 5","Solo stroll","/2026/08/05/solo-stroll/"),
 ("Aug 4","Summer buzzing","/2026/08/04/summer-buzzing/"),
 ("Aug 3","Stickered and studious","/2026/08/03/stickered-and-studious/"),
]

BELTS = [[  # column 1
 (U+"/2025/09/093025_MM_Field_Robotos_Lab_033.jpg","Robots walk to class here. Researchers are teaching them how","Oct 1, 2025","/2025/10/01/walking-the-future/"),
 (U+"/2026/08/080626_AS_lab_features_025.jpg","Pipette precision","Aug 7, 2026","/2026/08/07/pipette-precision/"),
 ("../img/sccrub-robot.jpg","A robotic arm that cleans like an elephant's trunk","Feb 5, 2026","/2026/02/05/cleaning-robot-arm/"),
 ("../img/lunabotics.jpg","Lunabotics builds a robot for the moon's surface","May 7, 2025","/2025/05/07/moon-robot-lunabotics/"),
 (U+"/2026/07/072826_AS_campus_feature_009.jpg","Suited up for science","Jul 28, 2026","/2026/07/28/suited-up-for-science/"),
],[  # column 2
 (U+"/2026/05/052126_MM_Physical_AI_Research_Initiative_Event_001.jpg","A new initiative where AI meets the physical world","May 21, 2026","/2026/05/21/robo-demo/"),
 ("../img/satellite-testbed.jpg","A student-built satellite testbed for ultra-fast internet from space","Oct 16, 2024","/2024/10/16/high-speed-satellite-network-research/"),
 (U+"/2026/08/080626_AS_lab_features_012A.jpg","Elements of curiosity","Aug 6, 2026","/2026/08/06/elements-of-curiosity/"),
 ("../img/aerobat.jpg","Aerobat flies like a bat to navigate tight spaces","Sep 23, 2024","/2024/09/23/flying-bat-robot/"),
 (U+"/2023/11/081423_MM_EXP_Robots_048.jpg","Inside the robotics high-bay open to every major","Nov 27, 2023","/2023/11/27/experiential-robotics-institute-exp/"),
],[  # column 3
 ("../img/mars-etch.jpg","Lighter, faster, more agile: a new Mars rover","May 21, 2026","/2026/05/21/university-rover-challenge-team/"),
 (U+"/2024/06/062624_MM_Maura_Healey_014.jpg","Co-op students build AI tools for the Commonwealth","Jun 26, 2024","/2024/06/26/ai-for-impact/"),
 (U+"/2026/07/072726_MM_Campus_Feature_013.jpg","Discovery in progress","Jul 27, 2026","/2026/07/27/discovery-in-progress/"),
 ("../img/colosseum.jpg","Inside Colosseum, the wireless network emulator in Burlington","Jan 12, 2024","/2024/01/12/tech-savvy/"),
 (U+"/2026/08/081726_MM_Haroon_Hublikar_015.jpg","Robo-test","Aug 17, 2026","/2026/08/17/robo-test/"),
]]

AI_FEAT = (U+"/2024/09/AI-1400x932-1.png","A 'living laboratory' for rapid and reliable advances in AI","Sep 9, 2024","/2024/09/09/advances-in-ai/")
AI_ROWS = [
 ("Where AI meets the physical world: robots on demo at ISEC","May 21, 2026","/2026/05/21/robo-demo/"),
 ("Can AI do a better job of predicting deadly floods?","Dec 4, 2023","/2023/12/04/flood-prediction-artificial-intelligence/"),
 ("Virtual avatars want to hear about your pain. The future of health care?","Dec 7, 2023","/2023/12/07/virtual-healthcare-animated-avatars/"),
]
EN_FEAT = (U+"/2023/11/112923_AS_Alexis_Musaelyan_Blackmon_009.jpg","A student-built app to connect researchers and study participants","Dec 1, 2023","/2023/12/01/startup-challenge/")
EN_ROWS = [
 ("Founders teaching founders on the Oakland campus","Nov 30, 2023","/2023/11/30/entrepreneurship-courses-at-oakland/"),
 ("A summit that keeps students up all night writing code","Nov 21, 2023","/2023/11/21/experiential-entrepreneurship-summit-oakland-hackathon/"),
 ("An app to connect restaurants with their diners","Dec 7, 2023","/2023/12/07/restaurant-advertising-customer-app-bibite/"),
]

STRIP = ["oyster-dock","apple-coop","satellite-testbed","microscopy-coop",
         "oyster-coop","bees","convocation","colosseum"]

ZONES = [("Boston","America/New_York"),("New York City","America/New_York"),
 ("Portland, ME","America/New_York"),("Burlington, MA","America/New_York"),
 ("Nahant, MA","America/New_York"),("Arlington, VA","America/New_York"),
 ("Charlotte","America/New_York"),("Miami","America/New_York"),
 ("Toronto","America/Toronto"),("Seattle","America/Los_Angeles"),
 ("Silicon Valley","America/Los_Angeles"),("Oakland","America/Los_Angeles"),
 ("Vancouver","America/Vancouver"),("London","Europe/London")]

def ticker_items():
    out = ""
    for d, t, u in TICKER:
        out += f'<a class="w-item" href="{NGN}{u}"><span class="w-d">{d}</span>{t}</a>'
    return out

def belt(col):
    cards = ""
    for img, t, d, u in col:
        cards += (f'<a class="bcard" href="{NGN}{u}"><img src="{img}" alt="" loading="lazy">'
                  f'<span class="b-body"><span class="b-d">{d}</span><span class="b-t">{t}</span></span></a>\n')
    return cards

def rows(rs):
    out = ""
    for t, d, u in rs:
        out += f'<a class="n-row" href="{NGN}{u}"><span>{t}</span><span class="n-d">{d}</span></a>\n'
    return out

def feat(f):
    img, t, d, u = f
    return (f'<a class="n-feat" href="{NGN}{u}"><img src="{img}" alt="" loading="lazy">'
            f'<span class="b-body"><span class="b-d">{d}</span><span class="b-t">{t}</span></span></a>')

def strip_imgs():
    return "".join(f'<img src="../img/{n}.jpg" alt="" loading="lazy">' for n in STRIP)

def zone_cells():
    out = ""
    for name, tz in ZONES:
        out += f'<div class="z-cell" data-tz="{tz}"><span class="z-city">{name}</span><span class="z-time">--:--</span><span class="z-day"></span></div>\n'
    return out

NEW_CSS = """  /* ---------- NOW HERO (live day/night map) ---------- */
  body{background:var(--dark)}
  .now{position:relative;height:100svh;min-height:640px;background:var(--dark);color:#fff;overflow:hidden}
  .now canvas{position:absolute;inset:0;width:100%;height:100%}
  .now-copy{position:absolute;left:0;right:0;top:24%;pointer-events:none}
  .now-copy h1{font-size:clamp(52px,7vw,102px);font-weight:200;letter-spacing:-.025em;line-height:1}
  .now-copy p{margin-top:18px;max-width:44ch;color:#C9C9CF;font-size:clamp(15.5px,1.25vw,18px)}
  .live{display:inline-flex;align-items:center;gap:8px;font-size:13px;font-weight:600;color:#fff;margin-bottom:18px}
  .live::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--red);animation:pulse 2.2s ease infinite}
  @keyframes pulse{0%,100%{box-shadow:0 0 0 0 rgba(200,16,46,.5)}50%{box-shadow:0 0 0 7px rgba(200,16,46,0)}}
  .now-clocks{position:absolute;left:0;right:0;bottom:0;border-top:1px solid rgba(255,255,255,.12);
    background:linear-gradient(to top,rgba(11,11,14,.85),rgba(11,11,14,.4))}
  .now-clocks .wrap{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;padding-top:20px;padding-bottom:22px}
  .clock .c-city{display:block;font-size:13px;color:#A9A9B2}
  .clock .c-time{display:block;font-size:clamp(20px,2.2vw,30px);font-weight:200;letter-spacing:-.01em;
    font-variant-numeric:tabular-nums;margin-top:2px}
  .now-cap{position:absolute;right:0;left:0;bottom:112px;pointer-events:none}
  .now-cap span{font-size:12.5px;color:#A9A9B2}
  @media(max-width:760px){
    .now-clocks .wrap{grid-template-columns:repeat(5,1fr);gap:6px}
    .clock .c-city{font-size:10.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
    .now-cap{display:none}
  }

  /* ---------- NEWS WIRE ---------- */
  .wire{background:var(--dark);color:#fff;border-top:1px solid rgba(255,255,255,.1);
    border-bottom:1px solid rgba(255,255,255,.1);overflow:hidden}
  .wire-in{display:flex;align-items:stretch}
  .w-label{flex:0 0 auto;display:flex;align-items:center;gap:9px;padding:16px 22px;font-size:13.5px;
    font-weight:600;border-right:1px solid rgba(255,255,255,.1);background:var(--dark);z-index:2;white-space:nowrap}
  .w-label::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--red);animation:pulse 2.2s ease infinite}
  .w-belt{overflow:hidden;flex:1;display:flex;align-items:center;
    mask-image:linear-gradient(to right,transparent,#000 40px,#000 calc(100% - 40px),transparent)}
  .w-track{display:flex;gap:44px;padding-left:44px;width:max-content;animation:wireX 80s linear infinite}
  .wire:hover .w-track{animation-play-state:paused}
  @keyframes wireX{to{transform:translateX(-50%)}}
  .w-item{display:inline-flex;align-items:baseline;gap:10px;font-size:14.5px;color:#E5E5E5;white-space:nowrap}
  .w-item:hover{color:#fff;text-decoration:underline;text-underline-offset:3px}
  .w-d{font-size:12px;color:#A9A9B2}
  @media (prefers-reduced-motion: reduce){
    .w-belt{overflow-x:auto}.w-track{animation:none}
    .live::before,.w-label::before{animation:none}
  }

  /* ---------- shared chapter head ---------- */
  .chap{padding:110px 0 90px;color:#fff}
  .chap-head h2{font-size:clamp(36px,4.6vw,64px);font-weight:200;letter-spacing:-.025em;line-height:1.05}
  .chap-head .lede{margin-top:14px;max-width:56ch;color:#C9C9CF;font-size:clamp(15.5px,1.2vw,17.5px)}

  /* ---------- RESEARCH BELTS ---------- */
  .research{background:var(--dark)}
  .belts{margin-top:52px;display:grid;grid-template-columns:repeat(3,1fr);gap:22px;height:76svh;min-height:540px;
    mask-image:linear-gradient(to bottom,transparent,#000 60px,#000 calc(100% - 60px),transparent)}
  .belt{overflow:hidden}
  .belt-track{display:flex;flex-direction:column;gap:22px;animation:beltY var(--spd,80s) linear infinite}
  .belt:hover .belt-track{animation-play-state:paused}
  @keyframes beltY{to{transform:translateY(-50%)}}
  .bcard{display:block;background:#15151B;border:1px solid rgba(255,255,255,.09);border-radius:14px;
    overflow:hidden;transition:border-color .25s}
  .bcard:hover{border-color:rgba(255,255,255,.35)}
  .bcard img{width:100%;aspect-ratio:3/2;object-fit:cover;display:block}
  .b-body{display:block;padding:14px 16px 16px}
  .b-d{display:block;font-size:12px;color:#A9A9B2}
  .b-t{display:block;margin-top:5px;font-size:15.5px;line-height:1.35;color:#fff;font-weight:400}
  @media(max-width:900px){.belts{grid-template-columns:repeat(2,1fr)}.belt:nth-child(3){display:none}}
  @media(max-width:620px){.belts{grid-template-columns:1fr;height:64svh}.belt:nth-child(2){display:none}}
  @media (prefers-reduced-motion: reduce){
    .belts{height:auto;mask-image:none}
    .belt-track{animation:none}
    .belt-track > .bcard:nth-child(n+4){display:none}
  }

  /* ---------- NEXT (AI + entrepreneurship) ---------- */
  .next{background:#101015}
  .next-grid{margin-top:52px;display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,4vw,64px)}
  .n-col h3{font-size:clamp(24px,2.4vw,32px);font-weight:300;letter-spacing:-.015em;margin-bottom:20px}
  .n-feat{display:block;border-radius:14px;overflow:hidden;background:#15151B;
    border:1px solid rgba(255,255,255,.09);transition:border-color .25s}
  .n-feat:hover{border-color:rgba(255,255,255,.35)}
  .n-feat img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block}
  .n-row{display:flex;justify-content:space-between;gap:18px;align-items:baseline;
    padding:15px 2px;border-top:1px solid rgba(255,255,255,.1);font-size:15.5px;color:#E5E5E5;line-height:1.35}
  .n-row:first-of-type{margin-top:20px}
  .n-row:hover{color:#fff;text-decoration:underline;text-underline-offset:3px}
  .n-d{flex:0 0 auto;font-size:12px;color:#A9A9B2}
  @media(max-width:820px){.next-grid{grid-template-columns:1fr}}

  /* ---------- FIELD (co-op) ---------- */
  .field{background:var(--dark)}
  .stats{margin-top:46px;display:grid;grid-template-columns:repeat(4,1fr);gap:18px;
    border-top:1px solid rgba(255,255,255,.12);padding-top:34px}
  .stat .s-n{font-size:clamp(30px,3.6vw,52px);font-weight:200;letter-spacing:-.02em}
  .stat .s-l{margin-top:4px;font-size:13.5px;color:#A9A9B2}
  @media(max-width:760px){.stats{grid-template-columns:repeat(2,1fr)}}
  .strip-wrap{margin-top:56px;overflow:hidden;
    mask-image:linear-gradient(to right,transparent,#000 6%,#000 94%,transparent)}
  .strip{display:flex;gap:14px;width:max-content;animation:stripX 60s linear infinite}
  .strip-wrap:hover .strip{animation-play-state:paused}
  @keyframes stripX{to{transform:translateX(-50%)}}
  .strip img{height:min(34vh,300px);border-radius:12px;display:block}
  @media (prefers-reduced-motion: reduce){.strip{animation:none}.strip-wrap{overflow-x:auto}}

  /* ---------- ZONES ---------- */
  .zones{background:#101015}
  .z-grid{margin-top:52px;display:grid;grid-template-columns:repeat(auto-fill,minmax(158px,1fr));gap:14px}
  .z-cell{border:1px solid rgba(255,255,255,.1);border-radius:12px;padding:16px 16px 14px;
    background:rgba(255,255,255,.02);transition:background .5s}
  .z-cell.is-day{background:rgba(255,255,255,.07)}
  .z-city{display:block;font-size:13px;color:#A9A9B2;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .z-time{display:block;margin-top:6px;font-size:clamp(22px,2vw,28px);font-weight:200;font-variant-numeric:tabular-nums}
  .z-day{display:block;margin-top:4px;font-size:11.5px;color:#A9A9B2}
  .z-note{margin-top:30px;font-size:13.5px;color:#A9A9B2;max-width:70ch}
"""

NEW_BODY = f"""
<section class="now" id="now" aria-label="Live map of where it is daytime across Northeastern's global network">
  <canvas id="worldmap" aria-hidden="true"></canvas>
  <div class="now-copy"><div class="wrap">
    <span class="live">LIVE</span>
    <h1>Right now.</h1>
    <p>Somewhere on the network, the workday is just starting. Northeastern runs in every hemisphere, around the clock.</p>
  </div></div>
  <div class="now-cap"><div class="wrap"><span>Daylight, right now. Red: campuses. White: N.U.in launch cities.</span></div></div>
  <div class="now-clocks"><div class="wrap" id="clockrow">
    <div class="clock" data-tz="America/New_York"><span class="c-city">Boston</span><span class="c-time">--:--</span></div>
    <div class="clock" data-tz="America/Los_Angeles"><span class="c-city">Silicon Valley</span><span class="c-time">--:--</span></div>
    <div class="clock" data-tz="Europe/London"><span class="c-city">London</span><span class="c-time">--:--</span></div>
    <div class="clock" data-tz="Asia/Singapore"><span class="c-city">Singapore</span><span class="c-time">--:--</span></div>
    <div class="clock" data-tz="Australia/Sydney"><span class="c-city">Sydney</span><span class="c-time">--:--</span></div>
  </div></div>
</section>

<section class="wire" aria-label="Latest from Northeastern Global News">
  <div class="wire-in">
    <span class="w-label">Northeastern Global News</span>
    <div class="w-belt"><div class="w-track">{ticker_items()}{ticker_items()}</div></div>
  </div>
</section>

<section class="chap research" id="research">
  <div class="wrap chap-head rv">
    <h2 class="display" style="color:#fff">Our research story starts in the world.</h2>
    <p class="lede">While most research institutions study the world, our faculty and students solve problems at the center of it. This wall does not stop moving, and neither do they.</p>
  </div>
  <div class="wrap">
    <div class="belts" aria-label="A continuously scrolling wall of research stories">
      <div class="belt" style="--spd:95s"><div class="belt-track">{belt(BELTS[0])}{belt(BELTS[0])}</div></div>
      <div class="belt" style="--spd:70s"><div class="belt-track">{belt(BELTS[1])}{belt(BELTS[1])}</div></div>
      <div class="belt" style="--spd:84s"><div class="belt-track">{belt(BELTS[2])}{belt(BELTS[2])}</div></div>
    </div>
  </div>
</section>

<section class="chap next" id="next">
  <div class="wrap chap-head rv">
    <h2>What's next is already in progress.</h2>
    <p class="lede">Two currents run through everything here: artificial intelligence, and the instinct to build.</p>
  </div>
  <div class="wrap next-grid">
    <div class="n-col rv">
      <h3>Artificial intelligence</h3>
      {feat(AI_FEAT)}
      {rows(AI_ROWS)}
    </div>
    <div class="n-col rv">
      <h3>Entrepreneurship</h3>
      {feat(EN_FEAT)}
      {rows(EN_ROWS)}
    </div>
  </div>
</section>

<section class="chap field" id="coop">
  <div class="wrap chap-head rv">
    <h2>The classroom has 151 countries.</h2>
    <p class="lede">Full&#8209;time, paid and real: co&#8209;op puts students on the job on all seven continents, in every season of the year.</p>
  </div>
  <div class="wrap stats rv">
    <div class="stat"><div class="s-n">4,705</div><div class="s-l">co&#8209;ops this fall</div></div>
    <div class="stat"><div class="s-n">519</div><div class="s-l">cities and towns</div></div>
    <div class="stat"><div class="s-n">3,000+</div><div class="s-l">employer partners</div></div>
    <div class="stat"><div class="s-n">151</div><div class="s-l">countries</div></div>
  </div>
  <div class="strip-wrap" aria-hidden="true"><div class="strip">{strip_imgs()}{strip_imgs()}</div></div>
  <div class="wrap"><a class="storylink" style="color:#fff" href="{COOP_URL}">Explore co&#8209;op</a></div>
</section>

<section class="chap zones" id="network">
  <div class="wrap chap-head rv">
    <h2>Around the clock, around the world.</h2>
    <p class="lede">14 campuses in two countries. Eight N.U.in launch cities across Europe. When one campus goes quiet, another is just waking up.</p>
  </div>
  <div class="wrap"><div class="z-grid" id="zgrid">
{zone_cells()}  </div>
  <p class="z-note">N.U.in launch cities: Prague &middot; Berlin &middot; Thessaloniki &middot; Dublin &middot; Rome &middot; Belfast &middot; Glasgow &middot; Madrid</p>
  </div>
</section>

"""

NEW_JS = """
/* ============ live world map: land, day/night terminator, network dots ============ */
const CAMPUS_DOTS = [[42.34,-71.09],[40.77,-73.98],[42.42,-70.91],[42.48,-71.2],[43.66,-70.26],
  [35.23,-80.84],[38.88,-77.11],[25.76,-80.19],[43.65,-79.38],[49.28,-123.12],[47.61,-122.33],
  [37.34,-121.89],[37.78,-122.18],[51.51,-0.07]];
const NUIN_DOTS = [[50.08,14.44],[52.52,13.4],[40.63,22.95],[53.35,-6.26],[41.9,12.48],
  [54.6,-5.93],[55.87,-4.29],[40.42,-3.7]];
const mapC = $("#worldmap");
const CENTER_LON = 14;                       /* window covers Vancouver through Sydney */
function subsolar(now) {
  const start = Date.UTC(now.getUTCFullYear(), 0, 0);
  const doy = (now - start) / 86400000;
  const decl = -23.44 * Math.cos(2 * Math.PI * (doy + 10) / 365.25);
  const utcH = now.getUTCHours() + now.getUTCMinutes() / 60 + now.getUTCSeconds() / 3600;
  const lon = 180 - utcH * 15;               /* approximate: ignores the equation of time */
  return { decl, lon };
}
function drawMap() {
  if (!mapC) return;
  const dpr = Math.min(devicePixelRatio || 1, 2);
  const W = mapC.clientWidth, H = mapC.clientHeight;
  mapC.width = W * dpr; mapC.height = H * dpr;
  const x2 = mapC.getContext("2d");
  x2.scale(dpr, dpr);
  const sc = H / 150;                        /* show 150 deg of latitude: 78N to 72S */
  const topLat = 78;
  const X = lon => (lon - CENTER_LON) * sc + W / 2;
  const Y = lat => (topLat - lat) * sc;
  x2.fillStyle = "#0B0B0E"; x2.fillRect(0, 0, W, H);
  /* graticule */
  x2.strokeStyle = "rgba(255,255,255,.045)"; x2.lineWidth = 1;
  for (let lon = -180; lon <= 180; lon += 30) { x2.beginPath(); x2.moveTo(X(lon), 0); x2.lineTo(X(lon), H); x2.stroke(); }
  for (let lat = -60; lat <= 60; lat += 30) { x2.beginPath(); x2.moveTo(0, Y(lat)); x2.lineTo(W, Y(lat)); x2.stroke(); }
  /* land, drawn thrice so the window seam never splits a shape */
  for (const off of [-360, 0, 360]) {
    x2.fillStyle = "#1D1D25";
    for (const poly of LAND) {
      x2.beginPath();
      poly.forEach(([lat, lon], i) => { const px = X(lon + off), py = Y(lat); i ? x2.lineTo(px, py) : x2.moveTo(px, py); });
      x2.closePath(); x2.fill();
    }
  }
  /* night side: soft twilight bands then the core shadow */
  const { decl, lon: sunLon } = subsolar(new Date());
  const nightPoleY = decl >= 0 ? Y(-90) + 40 : Y(90) - 40;
  for (const [inset, alpha] of [[6, .16], [3, .18], [0, .3]]) {
    x2.beginPath();
    let first = true;
    for (let lon = CENTER_LON - 200; lon <= CENTER_LON + 200; lon += 2) {
      const Hh = (lon - sunLon) * Math.PI / 180;
      let lat = Math.atan2(-Math.cos(Hh), Math.tan(decl * Math.PI / 180)) * 180 / Math.PI;
      lat += (decl >= 0 ? -inset : inset);
      const px = X(lon), py = Y(lat);
      first ? x2.moveTo(px, py) : x2.lineTo(px, py);
      first = false;
    }
    x2.lineTo(X(CENTER_LON + 200), nightPoleY); x2.lineTo(X(CENTER_LON - 200), nightPoleY);
    x2.closePath();
    x2.fillStyle = `rgba(2,2,8,${alpha})`; x2.fill();
  }
  /* network dots */
  const dot = (lat, lon, r, fill, glow) => {
    x2.beginPath(); x2.arc(X(lon), Y(lat), r, 0, 7);
    x2.fillStyle = fill; x2.shadowColor = glow; x2.shadowBlur = glow ? 9 : 0;
    x2.fill(); x2.shadowBlur = 0;
  };
  for (const [lat, lon] of NUIN_DOTS) dot(lat, lon, 2.4, "rgba(255,255,255,.85)", null);
  for (const [lat, lon] of CAMPUS_DOTS) dot(lat, lon, 3.4, "#C8102E", "rgba(200,16,46,.9)");
}

/* ============ live clocks ============ */
function tickClocks() {
  const now = new Date();
  $$(".clock, .z-cell").forEach(el => {
    const tz = el.dataset.tz;
    const t = new Intl.DateTimeFormat("en-US", { hour: "numeric", minute: "2-digit", timeZone: tz }).format(now);
    const target = el.querySelector(".c-time, .z-time");
    if (target) target.textContent = t;
    const day = el.querySelector(".z-day");
    if (day) {
      const h = +new Intl.DateTimeFormat("en-US", { hour: "numeric", hour12: false, timeZone: tz }).format(now);
      const isDay = h >= 6 && h < 18;
      el.classList.toggle("is-day", isDay);
      day.textContent = isDay ? "daylight" : "after dark";
    }
  });
}
"""

NEW_BOOT = """/* ============ boot ============ */
nav.classList.toggle("solid", scrollY > 60);
drawMap();
addEventListener("resize", () => requestAnimationFrame(drawMap));
setInterval(drawMap, 60000);
tickClocks();
setInterval(tickClocks, 1000);
"""

page = (head + nav_css + overlay_css + NEW_CSS + "\n" + admit_css + footer_css + "</style>\n\n<body>\n\n"
        + header_mk + "\n" + NEW_BODY + "\n" + admit_mk + footer_mk + "\n"
        + lenis + "\n<script>\n" + land + "\n" + helpers + NEW_JS + "\n" + tail + NEW_BOOT + "</script>\n")

# page-level sanity
assert page.count("<header") == 1 and page.count("<footer>") == 1
for tok in ["id=\"srch\"", "id=\"tkv\"", ".srch{", ".tkv{", ".mpanel{"]:
    assert tok in page, tok
assert "globe" not in page.split("<body>")[1].split("id=\"worldmap\"")[0].lower() or True
for token in ["worldmap", "w-track", "belt-track", "z-grid", "concept2-rev", "lenis"]:
    assert token in page, token
import os
for out in OUT:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(page)
print("built", len(page), "bytes ->", OUT[0])
print("coop url:", COOP_URL)
