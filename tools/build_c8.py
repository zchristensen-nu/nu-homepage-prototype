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
                    '<meta name="concept6-rev" content="3">')
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


assert helpers.count("admitIO.observe(admitEl);") == 1
helpers = helpers.replace("admitIO.observe(admitEl);", "if (admitEl) admitIO.observe(admitEl);")
i0 = tail_js.find("/* hero: content drifts"); i1 = tail_js.find("/* parallax on select backdrops")
assert 0 < i0 < i1
tail_js = tail_js[:i0] + tail_js[i1:]
mono = re.search(r'<img[^>]*src="(data:image/[^"]+)"', header_mk)
assert mono, "nav monogram"
MONO = mono.group(1)
import json
NGN = "https://news.northeastern.edu"
U = NGN + "/wp-content/uploads"

def ep(t, img, u): return {"t": t, "img": img, "u": u}

EP_COOP = [
 ep("Developing cameras for Apple products, on co‑op", "../img/apple-coop.jpg", NGN+"/2025/01/15/apple-co-op-camera-process-engineer/"),
 ep("Teacher, mentor, big sister: six months in a Cambodian dormitory", U+"/2023/11/Cecile-Doehrty_1400.jpg", NGN+"/2023/11/06/harpswell-foundation-co-op-cambodian-women/"),
 ep("Learning how global negotiation really works", U+"/2023/11/Dialogue-of-Civilization_1400.jpg", NGN+"/2023/11/27/dialogue-of-civilizations-geneva-anniversary/"),
 ep("Coffeehouses, Mozart and international finance, on co‑op", U+"/2023/09/Vienna1400.jpg", NGN+"/2023/10/13/unitcargo-finance-co-op-vienna-switzerland/"),
 ep("Harvesting oysters on Maine’s Nonesuch River, on co‑op", "../img/oyster-dock.jpg", NGN+"/2022/11/01/oyster-harvesting-maine/"),
]
EP_RESEARCH = [
 ep("This Northeastern researcher is making ‘waves’ with magnets", U+"/2026/09/Xufeng-Zhang_1400.jpg", NGN+"/2026/09/14/magnons-quantum-computing-research/"),
 ep("Robots walk to class here. Researchers are teaching them how", U+"/2025/09/093025_MM_Field_Robotos_Lab_033.jpg", NGN+"/2025/10/01/walking-the-future/"),
 ep("Cracking the axolotl code: how to regrow limbs and stay young", U+"/2026/07/072226_AS_-Calina_Copos_010.jpg", NGN+"/2026/07/27/axolotl-regeneration-anti-aging/"),
 ep("Scientists put algae to work making fuel. AI keeps watch", U+"/2026/08/Biofuel1400.jpg", NGN+"/2026/08/28/algae-biofuel-ai-research/"),
 ep("Quieting ‘the noise’ in quantum computing", U+"/2026/08/quantumsystem1400.jpg", NGN+"/2026/08/07/modular-quantum-computing-research/"),
]
EP_NETWORK = [
 ep("Northeastern students make a fast start to London life", U+"/2026/09/090726_CV_MoveIn_009.jpg", NGN+"/2026/09/08/move-in-week-london-campus/"),
 ep("Query, create or be curious at the new AI Makerspace in Boston", U+"/2026/09/AImakerspace1400.jpg", NGN+"/2026/09/23/ai-makerspace-boston-campus/"),
 ep("All-analog Oakland student government race brings record voter turnout", U+"/2026/09/092226_LC_Student_Government_Event_020.jpg", NGN+"/2026/09/25/northeastern-oakland-student-elections/"),
]
EP_LIFE = [
 ep("Photos: Convocation ceremonies, Fall Fest and the first day of fall semester", U+"/2026/09/090826_MM_convocation_147.jpg", NGN+"/2026/09/11/photos-convocation-ceremonies-fall-fest-and-the-first-day-of-fall-semester/"),
 ep("All-analog Oakland student government race brings record voter turnout", U+"/2026/09/092226_LC_Student_Government_Event_020.jpg", NGN+"/2026/09/25/northeastern-oakland-student-elections/"),
 ep("This graduate uses baking to cook up conversation about mental health", U+"/2026/08/Dayna-Altman1400.jpg", NGN+"/2026/09/15/bake-it-till-you-make-it-mental-health/"),
 ep("Northeastern students make a fast start to London life", U+"/2026/09/090726_CV_MoveIn_009.jpg", NGN+"/2026/09/08/move-in-week-london-campus/"),
]
EP_ATHLETICS = [
 ep("Former Husky Cam Schlittler stars as Yankees rout hometown Red Sox", U+"/2026/09/Cam-Schlittler-1400.jpg", NGN+"/2026/09/30/husky-cam-schlittler-yankees-red-sox-playoffs/"),
 ep("Northeastern women’s hockey team’s title run ends in semifinals", U+"/2026/03/JIM22137.jpg", NGN+"/2026/03/20/huskies-buckeyes-womens-hockey-frozen-four/"),
 ep("Meet the youngest members of Northeastern’s hockey teams", U+"/2026/02/021026_AS_Ella_Tapp_029.jpg", NGN+"/2026/03/04/northeastern-hockey-team-impact/"),
 ep("Huskies fall to BU in overtime Beanpot shootout", U+"/2026/02/020226_AS_M_Beapot_030.jpg", NGN+"/2026/02/03/beanpot-semis-huskies-terriers-td-garden/"),
]
EP_ADMIT = [
 ep("Apply to Northeastern", U+"/2023/09/Convocation1400.jpg", "https://admissions.northeastern.edu/"),
 ep("Visit a campus", U+"/2025/04/JIM28826.jpg", "https://admissions.northeastern.edu/visit/"),
 ep("Financial aid and scholarships", U+"/2026/09/090826_MM_convocation_147.jpg", "https://studentfinance.northeastern.edu/"),
 ep("Start your degree abroad with N.U.in", U+"/2025/07/070125_AS_RPS_orientation_004.jpg", "https://nuin.northeastern.edu/"),
]

SHOWS = [
 {"title": "Co‑op", "video": V_COOP, "thumb": "../img/apple-coop.jpg", "play": V_COOP,
  "meta": ["Experiential learning", "500,000+ placements", "10,000+ employers"],
  "syn": "Students alternate semesters in class with full‑time work at organizations around the world, then bring what they learned back to campus.",
  "eps": EP_COOP},
 {"title": "Research", "video": V_HERO, "thumb": U+"/2026/09/Xufeng-Zhang_1400.jpg", "play": V_HERO,
  "meta": ["$296M in external awards last year", "50+ federally funded centers"],
  "syn": "Our research story starts in the world. Faculty and students work on quantum systems, regenerative biology, robotics, and climate, and the work doesn’t stay in the lab.",
  "eps": EP_RESEARCH},
 {"title": "Global network", "video": V_LONDON, "thumb": U+"/2026/09/090726_CV_MoveIn_009.jpg", "play": V_LONDON,
  "meta": ["14 campuses", "U.S., U.K., and Canada", "N.U.in across Europe"],
  "syn": "Boston, London, New York City, Oakland, and ten more campuses across the U.S., U.K., and Canada. Every one opens doors to all the others.",
  "cta": {"label": "Explore the map", "href": "#campuses"},
  "eps": EP_NETWORK},
 {"title": "Student life", "video": V_CAMPUS, "thumb": U+"/2026/09/092226_LC_Student_Government_Event_020.jpg", "play": V_CAMPUS,
  "meta": ["Four undergraduate campuses", "Clubs, arts, and athletics"],
  "syn": "This place doesn’t slow down. Convocation, Fall Fest, student elections, and everything in between.",
  "eps": EP_LIFE},
 {"title": "Athletics", "still": U+"/2026/03/JIM22137.jpg", "thumb": U+"/2026/03/JIM22137.jpg",
  "meta": ["NCAA Division I", "Go Huskies"],
  "syn": "Division I Huskies, from Matthews Arena to the Charles River.",
  "cta": {"label": "Go to GoNU.com", "href": "https://gonu.com/"},
  "eps": EP_ATHLETICS},
 {"title": "Your turn.", "still": U+"/2026/09/090826_MM_convocation_147.jpg", "thumb": U+"/2023/09/Convocation1400.jpg",
  "meta": ["Apply", "Visit", "Financial aid"],
  "syn": "Four campuses to start from, and a world to work in after that. Here’s how to begin.",
  "cta": {"label": "Apply", "href": "https://admissions.northeastern.edu/"},
  "eps": EP_ADMIT},
]

def h(x): return x.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")

ICON_PLAY = '<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 1.5v13l11-6.5z" fill="currentColor"/></svg>'
ICON_INFO = '<svg width="18" height="18" viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="8.5" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M10 9v5M10 6.2v.1" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
ICON_ARROW = '<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h9M8.5 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_MUTED = '<svg class="i-muted" width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><path d="M3 7.5h3l4-3.5v12l-4-3.5H3z" fill="currentColor"/><path d="M13 7.5l4 5M17 7.5l-4 5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'
ICON_SOUND = '<svg class="i-sound" width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><path d="M3 7.5h3l4-3.5v12l-4-3.5H3z" fill="currentColor"/><path d="M13 7a4 4 0 010 6M15.2 5a7 7 0 010 10" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'

def layer(i, s):
    on = " on" if i == 0 else ""
    if "video" in s:
        return (f'<div class="bb-layer{on}"><video muted loop playsinline preload="none" '
                f'poster="{s["thumb"]}" src="{s["video"]}"></video></div>')
    return f'<div class="bb-layer kb{on}"><img src="{s["still"]}" alt="" loading="lazy"></div>'

def show_btn(i, s):
    return (f'<button class="show" aria-pressed="{"true" if i == 0 else "false"}" data-i="{i}">'
            f'<span class="th"><img src="{s["thumb"]}" alt="" loading="lazy"><i class="pb"></i></span>'
            f'<span class="st">{h(s["title"])}</span></button>')

S0 = SHOWS[0]
BILLBOARD = f'''<section class="bb" id="top" aria-label="Northeastern Originals">
  <div class="bb-media">{"".join(layer(i, s) for i, s in enumerate(SHOWS))}</div>
  <div class="bb-shade"></div>
  <div class="bb-in">
    <div class="wrap bb-row">
      <div class="bb-content" id="bbContent" aria-live="polite">
        <div class="bb-badge"><img src="{MONO}" alt=""><span>Northeastern Original</span></div>
        <h1 class="bb-title" id="bbTitle">{h(S0["title"])}</h1>
        <p class="bb-meta" id="bbMeta">{"".join(f"<span>{h(m)}</span>" for m in S0["meta"])}</p>
        <p class="bb-syn" id="bbSyn">{h(S0["syn"])}</p>
        <div class="bb-btns">
          <button class="bb-btn" id="bbPlay">{ICON_PLAY}<span>Play</span></button>
          <a class="bb-btn" id="bbCta" href="#" hidden><span id="bbCtaL"></span>{ICON_ARROW}</a>
          <button class="bb-btn ghost" id="bbInfo">{ICON_INFO}<span>More info</span></button>
        </div>
      </div>
      <button class="bb-mute" id="bbMute" aria-label="Unmute" aria-pressed="false">{ICON_MUTED}{ICON_SOUND}</button>
    </div>
    <div class="wrap"><div class="bb-shows" role="group" aria-label="Choose a show">{"".join(show_btn(i, s) for i, s in enumerate(SHOWS))}</div></div>
  </div>
</section>

<dialog class="dlg player" id="player" aria-label="Video player" data-lenis-prevent>
  <button class="dlg-x" data-close aria-label="Close">&#10005;</button>
  <video id="playerV" controls playsinline></video>
</dialog>

<dialog class="dlg info" id="info" aria-labelledby="infoT" data-lenis-prevent>
  <button class="dlg-x" data-close aria-label="Close">&#10005;</button>
  <div class="dlg-hero"><img id="infoImg" alt=""><h2 id="infoT"></h2></div>
  <div class="dlg-body">
    <p class="bb-meta" id="infoMeta"></p>
    <p class="dlg-syn" id="infoSyn"></p>
    <a class="bb-btn" id="infoCta" href="#" hidden><span id="infoCtaL"></span>{ICON_ARROW}</a>
    <h3 class="dlg-eps">Episodes</h3>
    <div id="infoEps"></div>
  </div>
</dialog>
'''

def card(e):
    return (f'<a class="card" href="{e["u"]}" data-ct="{h(e["t"])}" data-cimg="{e["img"]}">'
            f'<img src="{e["img"]}" alt="" loading="lazy"><p class="c-t">{h(e["t"])}</p></a>')

def row(rid, label, eps, hidden=False):
    hd = " hidden" if hidden else ""
    return (f'<section class="trow"{hd} id="{rid}" aria-label="{label}">\n'
            f'  <div class="wrap trow-head"><h2>{label}</h2>'
            f'<div class="tr-btns"><button class="tr-btn" data-dir="-1" aria-label="Scroll {label} back">&#8592;</button>'
            f'<button class="tr-btn" data-dir="1" aria-label="Scroll {label} forward">&#8594;</button></div></div>\n'
            f'  <div class="tr-strip">' + "".join(card(e) for e in eps) + "</div>\n</section>\n")

ROWS = ('<div class="shelves">\n'
        + row("continueRow", "Continue browsing", [], hidden=True)
        + row("ngnRow", "New on Northeastern Global News", EP_RESEARCH[:4])
        + row("coopRow", "Co&#8209;op stories", EP_COOP)
        + row("researchRow", "Research", EP_RESEARCH)
        + row("lifeRow", "Life at Northeastern", EP_LIFE + EP_NETWORK[1:2])
        + row("athleticsRow", "Athletics", EP_ATHLETICS)
        + '</div>\n')

GLOBE = '''<section class="s-orbit" id="campuses">
  <div class="o-globe" id="oGlobe" role="img" aria-label="Interactive globe showing the connected Northeastern network: campuses, N.U.in cities, and co&#8209;op locations"><canvas></canvas></div>
  <div class="o-overlay">
    <div class="n-copy">
      <h2>The world is our campus.</h2>
      <p class="n-legend">Campuses in white. Co&#8209;op cities in red.</p>
      <p class="n-lede">Every campus opens doors to all the others. Students move between them, and so does the work.</p>
    </div>
  </div>
</section>
'''

NEW_CSS = """  /* ---------- concept-6: Northeastern Originals ---------- */
  ::selection{background:var(--red);color:#fff}
  body{background:var(--dark)}

  /* billboard */
  .bb{position:relative;height:100svh;min-height:640px;overflow:hidden;color:#fff;background:#000}
  .bb-media{position:absolute;inset:0}
  .bb-layer{position:absolute;inset:0;opacity:0;transition:opacity .9s var(--ease)}
  .bb-layer.on{opacity:1}
  .bb-layer video,.bb-layer img{width:100%;height:100%;object-fit:cover;display:block}
  .bb-layer.kb.on img{animation:kb 24s ease-in-out infinite alternate}
  @keyframes kb{from{transform:scale(1)}to{transform:scale(1.12) translate(-1.5%,-1%)}}
  .bb-shade{position:absolute;inset:0;pointer-events:none;
    background:linear-gradient(to right,rgba(11,11,14,.82) 0%,rgba(11,11,14,.38) 36%,transparent 62%),
               linear-gradient(to top,var(--dark) 0%,rgba(11,11,14,.6) 24%,transparent 52%)}
  .bb-in{position:relative;z-index:2;height:100%;display:flex;flex-direction:column;justify-content:flex-end;
    padding-bottom:clamp(18px,3svh,34px)}
  .bb-row{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;
    margin-bottom:clamp(20px,3.5svh,40px)}
  .bb-content{max-width:min(640px,100%);transition:opacity .28s var(--ease),filter .28s var(--ease)}
  .bb-content.swap{opacity:0;filter:blur(10px)}
  .bb-badge{display:flex;align-items:center;gap:10px;font-size:15px;color:#E5E5E5}
  .bb-badge img{height:22px;width:auto}
  .bb-title{margin:12px 0 0;font-size:clamp(56px,8vw,128px);font-weight:200;letter-spacing:-.035em;
    line-height:.95;transform-origin:left bottom;transition:transform .9s var(--ease)}
  .bb-meta{margin:16px 0 0;display:flex;flex-wrap:wrap;gap:6px 0;font-size:15px;color:#E5E5E5}
  .bb-meta span+span::before{content:"\\00b7";margin:0 12px;color:#A9A9B2}
  .bb-syn{margin:14px 0 0;font-size:clamp(16px,1.3vw,19px);line-height:1.5;color:#E5E5E5;max-width:46ch;
    max-height:9em;overflow:hidden;
    transition:opacity .7s var(--ease),max-height .9s var(--ease),margin .9s var(--ease)}
  .bb-content.settled .bb-title{transform:scale(.78)}
  .bb-content.settled .bb-syn{opacity:0;max-height:0;margin-top:0}
  .bb-btns{display:flex;gap:12px;margin-top:22px;flex-wrap:wrap}
  .bb-btn{all:unset;box-sizing:border-box;display:inline-flex;align-items:center;gap:10px;height:48px;
    padding:0 24px;border-radius:999px;font-size:16px;font-weight:600;cursor:pointer;
    background:#fff;color:#0B0B0E;transition:background .2s}
  .bb-btn:hover{background:rgba(255,255,255,.82)}
  .bb-btn.ghost{background:rgba(255,255,255,.18);color:#fff;backdrop-filter:blur(10px)}
  .bb-btn.ghost:hover{background:rgba(255,255,255,.28)}
  .bb-btn:focus-visible,.bb-mute:focus-visible,.show:focus-visible .th{outline:2px solid #fff;outline-offset:3px}
  .bb-btn[hidden],.bb-mute[hidden]{display:none}
  .bb-mute{all:unset;box-sizing:border-box;flex:0 0 auto;width:44px;height:44px;border-radius:50%;
    border:1px solid rgba(255,255,255,.55);display:flex;align-items:center;justify-content:center;
    color:#fff;cursor:pointer;transition:background .2s}
  .bb-mute:hover{background:rgba(255,255,255,.14)}
  .bb-mute .i-sound{display:none}
  .bb-mute[aria-pressed="true"] .i-sound{display:block}
  .bb-mute[aria-pressed="true"] .i-muted{display:none}
  .bb-shows{display:flex;gap:12px;overflow-x:auto;scrollbar-width:none;padding:6px 3px 4px}
  .bb-shows::-webkit-scrollbar{display:none}
  .show{all:unset;box-sizing:border-box;cursor:pointer;flex:0 0 auto;width:clamp(160px,14.5vw,224px)}
  .show .th{position:relative;display:block;aspect-ratio:16/9;border-radius:10px;overflow:hidden;
    background:#141419;box-shadow:0 0 0 2px transparent;transition:box-shadow .3s var(--ease),transform .3s var(--ease)}
  .show img{width:100%;height:100%;object-fit:cover;display:block;filter:brightness(.62);transition:filter .3s}
  .show:hover .th{transform:translateY(-3px)}
  .show:hover img{filter:brightness(.85)}
  .show[aria-pressed="true"] .th{box-shadow:0 0 0 2px #fff}
  .show[aria-pressed="true"] img{filter:none}
  .show .st{display:block;margin-top:8px;font-size:14px;font-weight:500;color:#A9A9B2;transition:color .3s}
  .show[aria-pressed="true"] .st{color:#fff}
  .show .pb{position:absolute;left:0;bottom:0;height:3px;width:0;background:var(--red)}
  .show.timing .pb{animation:pbar var(--dur,14s) linear forwards}
  @keyframes pbar{to{width:100%}}
  @media (max-width:820px){
    .bb{min-height:560px}
    .bb-title{font-size:clamp(46px,13vw,72px)}
    .bb-syn{font-size:15.5px}
    .bb-btn{height:44px;padding:0 18px;font-size:15px}
    .show{width:150px}
  }
  @media (prefers-reduced-motion: reduce){
    .bb-layer,.bb-content,.bb-title,.bb-syn{transition:none}
    .bb-layer.kb.on img{animation:none}
  }

  /* dialogs */
  .dlg{border:0;padding:0;background:#141419;color:#fff;border-radius:16px;width:min(880px,94vw);
    max-height:90svh;overflow:auto;box-shadow:0 30px 80px rgba(0,0,0,.6)}
  .dlg::backdrop{background:rgba(0,0,0,.74);backdrop-filter:blur(4px)}
  .dlg.player{width:min(1200px,96vw);background:#000;overflow:hidden}
  .dlg.player video{display:block;width:100%;max-height:86svh;background:#000}
  .dlg-x{all:unset;position:absolute;top:14px;right:14px;z-index:3;width:38px;height:38px;border-radius:50%;
    background:rgba(20,20,25,.8);color:#fff;display:flex;align-items:center;justify-content:center;
    cursor:pointer;font-size:15px}
  .dlg-x:hover{background:#fff;color:#0B0B0E}
  .dlg-x:focus-visible{outline:2px solid #fff;outline-offset:2px}
  .dlg-hero{position:relative;aspect-ratio:16/7;background:#000}
  .dlg-hero img{width:100%;height:100%;object-fit:cover;display:block}
  .dlg-hero::after{content:"";position:absolute;inset:0;background:linear-gradient(to top,#141419 0%,transparent 60%)}
  .dlg-hero h2{position:absolute;left:28px;bottom:10px;z-index:2;margin:0;font-size:clamp(38px,5vw,64px);
    font-weight:200;letter-spacing:-.03em;line-height:1}
  .dlg-body{padding:6px 28px 30px}
  .dlg-syn{margin:14px 0 18px;font-size:16px;line-height:1.55;color:#D4D4D4;max-width:60ch}
  .dlg-eps{margin:26px 0 6px;font-size:20px;font-weight:600}
  .ep{display:grid;grid-template-columns:34px 170px 1fr;gap:18px;align-items:center;padding:14px 10px;
    border-top:1px solid rgba(255,255,255,.1);color:#fff;border-radius:8px;transition:background .2s}
  .ep:hover{background:rgba(255,255,255,.06)}
  .ep-n{font-size:24px;font-weight:300;color:#A9A9B2;text-align:center}
  .ep img{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:6px;display:block}
  .ep-t{font-size:15.5px;line-height:1.4}
  @media (max-width:640px){
    .ep{grid-template-columns:24px 110px 1fr;gap:12px}
    .dlg-body{padding:6px 18px 24px}
  }

  /* shelves */
  .shelves{position:relative;z-index:2;color:#fff;padding:clamp(10px,2svh,24px) 0 clamp(70px,10svh,130px)}
  .trow{margin-top:clamp(30px,4.5svh,54px)}
  .trow[hidden]{display:none}
  .trow-head{display:flex;align-items:baseline;justify-content:space-between;gap:16px}
  .trow-head h2{margin:0;font-size:clamp(19px,1.6vw,24px);font-weight:600;letter-spacing:-.01em}
  .tr-btns{display:flex;gap:8px}
  .tr-btn{width:36px;height:36px;border-radius:50%;border:1px solid rgba(255,255,255,.35);
    background:transparent;color:#fff;font-size:15px;cursor:pointer;transition:.2s;
    display:flex;align-items:center;justify-content:center}
  .tr-btn:hover{background:#fff;color:var(--ink);border-color:#fff}
  .tr-strip{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x proximity;
    scrollbar-width:none;margin-top:12px;padding:14px 0 18px;
    padding-inline:max(24px, calc((100vw - 1280px) / 2))}
  .tr-strip::-webkit-scrollbar{display:none}
  .card{position:relative;flex:0 0 auto;width:clamp(230px,22vw,340px);aspect-ratio:16/9;
    border-radius:10px;overflow:hidden;background:#141419;scroll-snap-align:start;
    transition:transform .35s var(--ease),box-shadow .35s var(--ease);display:block}
  .card:hover,.card:focus-visible{transform:scale(1.06);z-index:3;box-shadow:0 18px 44px rgba(0,0,0,.55)}
  .card:focus-visible{outline:2px solid #fff;outline-offset:3px}
  .card img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
  .card .c-t{position:absolute;left:0;right:0;bottom:0;z-index:2;margin:0;padding:34px 14px 12px;
    font-size:14px;font-weight:500;line-height:1.3;color:#fff;
    background:linear-gradient(to top,rgba(0,0,0,.8),transparent)}
  @media (prefers-reduced-motion: reduce){.card{transition:none}}

  /* network globe band */
  .s-orbit{position:relative;z-index:2;color:#fff;height:100svh;overflow:hidden}
  .o-globe{position:absolute;inset:0;touch-action:pan-y;cursor:grab;
    -webkit-mask-image:linear-gradient(to bottom,transparent,#000 12%,#000 88%,transparent);
    mask-image:linear-gradient(to bottom,transparent,#000 12%,#000 88%,transparent)}
  .o-globe canvas{position:absolute;inset:0;width:100%;height:100%}
  .o-overlay{position:relative;z-index:2;height:100%;display:flex;align-items:center;pointer-events:none}
  .n-copy{max-width:min(520px,44vw);padding-left:max(24px, calc((100vw - 1280px) / 2))}
  .n-copy h2{margin:0;font-size:clamp(40px,4.6vw,84px);font-weight:200;letter-spacing:-.03em;line-height:1.05}
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

NEW_JS = """
/* ============ Northeastern Originals: the billboard ============ */
const SHOWS = """ + json.dumps(SHOWS, ensure_ascii=False) + """;
const bbEl = $("#top"), bbContent = $("#bbContent");
const bbLayers = $$(".bb-layer"), showBtns = $$(".show");
const bbTitle = $("#bbTitle"), bbMeta = $("#bbMeta"), bbSyn = $("#bbSyn");
const bbPlay = $("#bbPlay"), bbCta = $("#bbCta"), bbCtaL = $("#bbCtaL"), bbMute = $("#bbMute");
const esc = s => String(s).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");
const SHOW_MS = 14000;
let bbCur = -1, bbMuted = true, bbAuto = !reduceMotion, bbAutoT = null, bbSettleT = null, bbVisible = true;
const layerVid = i => bbLayers[i].querySelector("video");
function bbText(s) {
  bbTitle.textContent = s.title;
  bbMeta.innerHTML = s.meta.map(m => `<span>${esc(m)}</span>`).join("");
  bbSyn.textContent = s.syn;
  bbPlay.hidden = !s.play;
  if (s.cta) { bbCta.hidden = false; bbCta.href = s.cta.href; bbCtaL.textContent = s.cta.label; }
  else bbCta.hidden = true;
  bbMute.hidden = !s.video;
}
function bbTimer() {
  showBtns.forEach(b => b.classList.remove("timing"));
  clearTimeout(bbAutoT);
  if (!bbAuto || !bbVisible) return;
  const b = showBtns[bbCur];
  b.style.setProperty("--dur", SHOW_MS + "ms");
  void b.offsetWidth;
  b.classList.add("timing");
  bbAutoT = setTimeout(() => bbSelect((bbCur + 1) % SHOWS.length), SHOW_MS);
}
function bbSelect(i) {
  if (i === bbCur) return;
  const prev = bbCur; bbCur = i;
  bbLayers.forEach((l, j) => l.classList.toggle("on", j === i));
  showBtns.forEach((b, j) => b.setAttribute("aria-pressed", j === i ? "true" : "false"));
  const v = layerVid(i);
  if (v) {
    if (!v.dataset.loaded) { v.dataset.loaded = "1"; v.load(); }
    v.muted = bbMuted;
    if (!reduceMotion && bbVisible) v.play().catch(() => {});
  }
  if (prev >= 0) {
    const pv = layerVid(prev);
    if (pv) setTimeout(() => { if (bbCur !== prev) pv.pause(); }, 950);
    bbContent.classList.add("swap");
    setTimeout(() => { bbText(SHOWS[i]); bbContent.classList.remove("swap", "settled"); }, 280);
  } else bbText(SHOWS[i]);
  clearTimeout(bbSettleT);
  if (!reduceMotion) bbSettleT = setTimeout(() => bbContent.classList.add("settled"), 7000);
  bbTimer();
}
showBtns.forEach((b, i) => b.addEventListener("click", () => {
  bbAuto = false;
  bbContent.classList.remove("settled");
  bbSelect(i);
  bbTimer();
}));
bbMute.addEventListener("click", () => {
  bbMuted = !bbMuted;
  bbMute.setAttribute("aria-pressed", bbMuted ? "false" : "true");
  bbMute.setAttribute("aria-label", bbMuted ? "Unmute" : "Mute");
  const v = layerVid(bbCur);
  if (v) v.muted = bbMuted;
});
new IntersectionObserver(es => es.forEach(e => {
  bbVisible = e.isIntersecting;
  const v = bbCur >= 0 ? layerVid(bbCur) : null;
  if (v) { if (bbVisible && !reduceMotion) v.play().catch(() => {}); else v.pause(); }
  bbTimer();
}), { threshold: 0.25 }).observe(bbEl);
bbSelect(0);

/* ============ player + more-info dialogs ============ */
const player = $("#player"), playerV = $("#playerV"), info = $("#info");
$$(".dlg").forEach(d => {
  d.addEventListener("click", e => { if (e.target === d || e.target.closest("[data-close]")) d.close(); });
});
bbPlay.addEventListener("click", () => {
  const s = SHOWS[bbCur];
  if (!s.play) return;
  const v = layerVid(bbCur); if (v) v.pause();
  clearTimeout(bbAutoT); bbAuto = false; bbTimer();
  playerV.src = s.play; playerV.muted = false;
  player.showModal();
  playerV.play().catch(() => {});
});
player.addEventListener("close", () => {
  playerV.pause(); playerV.removeAttribute("src"); playerV.load();
  const v = layerVid(bbCur); if (v && !reduceMotion) v.play().catch(() => {});
});
$("#bbInfo").addEventListener("click", () => {
  const s = SHOWS[bbCur];
  bbAuto = false; bbTimer();
  $("#infoImg").src = s.thumb;
  $("#infoT").textContent = s.title;
  $("#infoMeta").innerHTML = s.meta.map(m => `<span>${esc(m)}</span>`).join("");
  $("#infoSyn").textContent = s.syn;
  const ic = $("#infoCta");
  if (s.cta) { ic.hidden = false; ic.href = s.cta.href; $("#infoCtaL").textContent = s.cta.label; }
  else ic.hidden = true;
  $("#infoEps").innerHTML = s.eps.map((e, n) =>
    `<a class="ep" href="${esc(e.u)}" data-ct="${esc(e.t)}" data-cimg="${esc(e.img)}">` +
    `<span class="ep-n">${n + 1}</span><img src="${esc(e.img)}" alt="" loading="lazy">` +
    `<span class="ep-t">${esc(e.t)}</span></a>`).join("");
  info.showModal();
});
$("#infoCta").addEventListener("click", e => {
  const href = e.currentTarget.getAttribute("href");
  if (href && href.startsWith("#")) { e.preventDefault(); info.close(); document.querySelector(href).scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth" }); }
});

/* ============ shelves: arrows ============ */
$$(".trow").forEach(sec => {
  const strip = sec.querySelector(".tr-strip");
  sec.querySelectorAll(".tr-btn").forEach(b => b.addEventListener("click", () => {
    strip.scrollBy({ left: +b.dataset.dir * strip.clientWidth * 0.85, behavior: reduceMotion ? "auto" : "smooth" });
  }));
});

/* ============ continue browsing (this browser only) ============ */
const CB_KEY = "nu-continue";
const cbRead = () => { try { return JSON.parse(localStorage.getItem(CB_KEY)) || []; } catch (e) { return []; } };
const cbRow = $("#continueRow");
if (cbRow) {
  const seen = cbRead().slice(0, 8);
  if (seen.length) {
    cbRow.querySelector(".tr-strip").innerHTML = seen.map(c =>
      `<a class="card" href="${esc(c.u)}" data-ct="${esc(c.t)}" data-cimg="${esc(c.img)}">` +
      `<img src="${esc(c.img)}" alt="" loading="lazy"><p class="c-t">${esc(c.t)}</p></a>`).join("");
    cbRow.hidden = false;
  }
  document.addEventListener("click", e => {
    const a = e.target.closest("a[data-cimg]");
    if (!a) return;
    try {
      const list = cbRead().filter(c => c.u !== a.href);
      list.unshift({ t: a.dataset.ct, img: a.dataset.cimg, u: a.href });
      localStorage.setItem(CB_KEY, JSON.stringify(list.slice(0, 12)));
    } catch (e2) { /* storage unavailable */ }
  });
}

/* ============ live NGN shelf with real thumbnails ============ */
(async () => {
  try {
    const r = await fetch("https://news.northeastern.edu/wp-json/wp/v2/newspost?per_page=12&_embed=wp:featuredmedia");
    if (!r.ok) return;
    const tmp = document.createElement("div");
    const cards = (await r.json())
      .filter(p => !/^Photos:/i.test(p.title.rendered))
      .map(p => {
        const m = p._embedded && p._embedded["wp:featuredmedia"] && p._embedded["wp:featuredmedia"][0];
        if (!m) return null;
        const sz = m.media_details && m.media_details.sizes;
        const img = (sz && (sz.medium_large || sz.large || sz.medium) || m).source_url || m.source_url;
        tmp.innerHTML = p.title.rendered;
        const t = tmp.textContent;
        return `<a class="card" href="${esc(p.link)}" data-ct="${esc(t)}" data-cimg="${esc(img)}">` +
               `<img src="${esc(img)}" alt="" loading="lazy"><p class="c-t">${esc(t)}</p></a>`;
      })
      .filter(Boolean).slice(0, 10);
    if (cards.length >= 4) $("#ngnRow .tr-strip").innerHTML = cards.join("");
  } catch (e) { /* baked cards remain */ }
})();

/* ============ the network globe ============ */
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
"""

NEW_BOOT = """/* ============ boot ============ */
nav.classList.toggle("solid", scrollY > 60);
"""

page = (head + nav_css + overlay_css + sheet_css + NEW_CSS + "\n" + tailcss
        + "</style>\n\n<body>\n\n"
        + header_mk + BILLBOARD + ROWS + GLOBE + footer_mk + "\n"
        + lenis + "\n<script>\n" + land + "\n" + coops + "\n" + helpers + globedata + engine + NEW_JS + "\n" + tail_js + NEW_BOOT + "</script>\n")

assert page.count("<header") == 1 and page.count("<footer>") == 1
assert page.count('class="bb-layer') == 6 and page.count('class="show"') == 6
assert page.count("<video") == 5  # 4 billboard films + player
for tok in ['id="srch"', 'id="tkv"', "bbSelect", "showModal", "nu-continue", "ngnRow", "ARCS",
            "Northeastern Original", "concept6-rev", 'content="3"', "newspost", "data-lenis-prevent"]:
    assert tok in page, tok
for gone in ['class="hero"', "lifeimax", "rphrase", "s-grow", "wire top", 'class="admit"', "research counters"]:
    assert gone not in page, gone
for out in OUT:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(page)
print("built", len(page), "bytes ->", OUT[0])
