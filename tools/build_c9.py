"""Concept 10: immersive streaming. The page opens on a full-bleed billboard
(per-feature film, synopsis, stories panel) over a
row of portrait feature cards; then live NGN rows (a static featured card,
then portrait posters, Netflix-style edge paddles); concept 2's scroll-driven
globe tour, research sheet and co-op rail; concept 4's portrait video reel;
concept 2's portrait quotes; and v1's "Your turn." closer. Keeps the v1 nav,
footer and brand. Deploys to concept-10/ (concept-7 belongs to the streaming concepts 7-9 build)."""
import math, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = [os.path.join(ROOT, "concept-10/index.html")]

# ponytail: reuse build_c8's extraction (nav, footer, show data) by running its prefix;
# if build_c8 is restructured, lift the extraction into a shared module then.
_c8 = open(os.path.join(HERE, "build_c8.py")).read()
_pre = _c8.split("S0 = SHOWS[0]")[0]
assert "def cut(" in _pre and "SHOWS = [" in _pre
g = {}
exec(_pre, g)
head, nav_css, overlay_css, tailcss = (g[k] for k in ("head", "nav_css", "overlay_css", "tailcss"))
header_mk, footer_mk, lenis_js, rest_mk = g["header_mk"], g["footer_mk"], g["lenis"], g["rest_mk"]
land, coops, helpers, tail_js = (g[k] for k in ("land", "coops", "helpers", "tail_js"))
SHOWS, MONO, NGN_LOGO, h, NGN, U, ep = g["SHOWS"], g["MONO"], g["NGN_LOGO"], g["h"], g["NGN"], g["U"], g["ep"]

# navigation: Admissions + Academics become one deduplicated dropdown; Global & Campuses becomes
# Global Network; Global Entrepreneurship and AI become top-level links (out of the dead # link and More)
ENT_URL, AI_URL = "https://entrepreneurship.northeastern.edu/", "https://www.northeastern.edu/ai/"
def nav_edit(src, a, b, n=1):
    assert src.count(a) == n, (src.count(a), a[:70]); return src.replace(a, b)
header_mk = nav_edit(header_mk, """      <button class="mnav-btn" data-panel="mp-admissions" aria-expanded="false">Admissions</button>
      <button class="mnav-btn" data-panel="mp-academics" aria-expanded="false">Academics</button>""",
    """      <button class="mnav-btn" data-panel="mp-admissions" aria-expanded="false">Academics</button>""")
header_mk = nav_edit(header_mk, """      <button class="mnav-btn" data-panel="mp-global" aria-expanded="false">Global &amp; Campuses</button>""",
    f"""      <button class="mnav-btn" data-panel="mp-global" aria-expanded="false">Global Network</button>
      <a class="mnav-a" href="{ENT_URL}">Global Entrepreneurship</a>
      <a class="mnav-a" href="{AI_URL}">AI</a>""")
_a0 = header_mk.index('<div class="mpanel" id="mp-admissions"'); _a1 = header_mk.index('<div class="mpanel" id="mp-experiential"')
_feat = header_mk[_a0:_a1]
_feat = _feat[_feat.index('<a class="mp-feat"'):]
_feat = _feat[:_feat.index("</a>") + 4]
header_mk = header_mk[:_a0] + f"""<div class="mpanel" id="mp-admissions" hidden><div class="wrap mp-in">
      <div class="mp-lead mp-lead-wide"><div class="mp-title">Academics</div><p>However you learn best, there is a path here.</p>
        <a class="storylink" href="https://www.northeastern.edu/admissions/">Admissions</a>
        <a class="storylink" href="https://www.northeastern.edu/academics/">Academics</a></div>
      <div class="mp-col"><div class="mp-h">Apply</div><div class="mp-links">
        <a href="https://admissions.northeastern.edu/">Undergraduate admissions</a>
        <a href="https://graduate.northeastern.edu/admissions-information/how-to-apply/the-process">Graduate admissions</a>
        <a href="https://law.northeastern.edu/admissions/">Law school admissions</a>
        <a href="https://admissions.northeastern.edu/visit/">Visit a campus</a>
      </div></div>
      <div class="mp-col"><div class="mp-h">Programs</div><div class="mp-links">
        <a href="https://www.northeastern.edu/academics/colleges-and-schools/">Colleges and schools</a>
        <a href="https://phd.northeastern.edu/">Doctoral programs</a>
        <a href="https://online.northeastern.edu/">Online education</a>
        <a href="https://bachelors-completion.northeastern.edu/">Bachelor's degree completion</a>
      </div></div>
      <div class="mp-col"><div class="mp-h">Get started</div><div class="mp-links">
        <a href="https://studentfinance.northeastern.edu/">Financial aid</a>
        <a href="https://www.northeastern.edu/orientation/">Orientation and family programs</a>
        <a href="https://academicplan.northeastern.edu/">Academic plan</a>
      </div></div>
  </div></div>
  """ + header_mk[_a1:]
header_mk = nav_edit(header_mk, """        <a href="#">Entrepreneurship</a>
""", "", 2)            # Experiential panel + mobile menu
header_mk = nav_edit(header_mk, f"""        <a href="{AI_URL}">Artificial Intelligence</a>
""", "", 2)  # More panel + mobile menu
header_mk = nav_edit(header_mk, '<button class="tkv-open mobilemenu" id="tkv-open" aria-expanded="false">Menu</button>',
    '<button class="tkv-open mobilemenu" id="tkv-open" aria-expanded="false"><svg class="tko-i" width="22" height="22" viewBox="0 0 22 22" aria-hidden="true"><path d="M3 7h16M3 15h16" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg><span class="tko-l">Menu</span></button>')
# mobile menu: one merged group, renamed Global, and the two new direct links
_t0 = header_mk.index('<button class="tkv-g" data-sub="tsub-0"'); _t0 = header_mk.rindex('<div class="tkv-grp">', 0, _t0)
_t1 = header_mk.index('<button class="tkv-g" data-sub="tsub-2"'); _t1 = header_mk.rindex('<div class="tkv-grp">', 0, _t1)
header_mk = header_mk[:_t0] + """<div class="tkv-grp">
      <button class="tkv-g" data-sub="tsub-0" aria-expanded="false">Academics<span class="tkv-c" aria-hidden="true">+</span></button>
      <div class="tkv-sub" id="tsub-0">
        <a href="https://www.northeastern.edu/admissions/">Admissions overview</a>
        <a href="https://www.northeastern.edu/academics/">Academics overview</a>
        <a href="https://admissions.northeastern.edu/">Undergraduate admissions</a>
        <a href="https://graduate.northeastern.edu/admissions-information/how-to-apply/the-process">Graduate admissions</a>
        <a href="https://law.northeastern.edu/admissions/">Law school admissions</a>
        <a href="https://admissions.northeastern.edu/visit/">Visit a campus</a>
        <a href="https://www.northeastern.edu/academics/colleges-and-schools/">Colleges and schools</a>
        <a href="https://phd.northeastern.edu/">Doctoral programs</a>
        <a href="https://online.northeastern.edu/">Online education</a>
        <a href="https://bachelors-completion.northeastern.edu/">Bachelor's degree completion</a>
        <a href="https://studentfinance.northeastern.edu/">Financial aid</a>
        <a href="https://www.northeastern.edu/orientation/">Orientation and family programs</a>
        <a href="https://academicplan.northeastern.edu/">Academic plan</a>
      </div>
    </div>
    """ + header_mk[_t1:]
header_mk = nav_edit(header_mk, 'aria-expanded="false">Global<span class="tkv-c"', 'aria-expanded="false">Global Network<span class="tkv-c"')
_t2 = header_mk.index('<button class="tkv-g" data-sub="tsub-5"'); _t2 = header_mk.rindex('<div class="tkv-grp">', 0, _t2)
header_mk = header_mk[:_t2] + f"""<a class="tkv-l" href="{ENT_URL}">Global Entrepreneurship<span aria-hidden="true">&#8594;</span></a>
    <a class="tkv-l" href="{AI_URL}">AI<span aria-hidden="true">&#8594;</span></a>
    """ + header_mk[_t2:]
header_mk = nav_edit(header_mk, '<span class="apply"><a class="pill" href="#admit">Apply</a></span>', '')
# social links as the live site's icons (WordPress core social-link SVGs), text kept as the accessible name
_SOC = json.load(open(os.path.join(os.path.dirname(__file__), "social-icons.json")))
for _k, _name, _url in (("facebook", "Facebook", "https://www.facebook.com/northeastern"), ("twitter", "X", "https://x.com/northeastern"),
                        ("youtube", "YouTube", "https://www.youtube.com/user/Northeastern"), ("linkedin", "LinkedIn", "https://www.linkedin.com/school/northeastern-university/"),
                        ("instagram", "Instagram", "https://www.instagram.com/northeastern"), ("tiktok", "TikTok", "https://www.tiktok.com/@northeastern")):
    _a = f'<a href="{_url}">{_name}</a>'
    assert footer_mk.count(_a) == 1, _a
    footer_mk = footer_mk.replace(_a, f'<a href="{_url.replace("@northeastern", "@northeasternu")}" aria-label="{_name}">{_SOC[_k]}</a>')
footer_mk = nav_edit(footer_mk, """<a href="#">Entrepreneurship</a>""", f"""<a href="{ENT_URL}">Entrepreneurship</a>""")

assert head.count('<meta name="concept6-rev" content="4">') == 1
head = head.replace('<meta name="concept6-rev" content="4">', '<meta name="concept10-rev" content="56">')

# expose Lenis (handy for scripted checks; anchors already route through it)
assert tail_js.count("const lenis = new Lenis({ lerp: 0.12 });") == 1
tail_js = tail_js.replace("const lenis = new Lenis({ lerp: 0.12 });", "const lenis = window.lenis = new Lenis({ lerp: 0.12 });")

def cut_from(src, a, b, inclusive_b=False):
    i = src.find(a); assert i >= 0, a[:60]
    j = src.find(b, i + len(a)); assert j > i, b[:60]
    return src[i:j + (len(b) if inclusive_b else 0)]

# concept 2 (built page): globe tour, research sheet, co-op rail, portrait quotes
C2 = open(os.path.join(ROOT, "concept-2/index.html")).read()
c2_css = (cut_from(C2, "  /* ---------- GLOBE SCROLLY ---------- */", "  .srch{")
          + cut_from(C2, "  /* ---------- SHEET SECTIONS (Adobe pattern) ---------- */", "  /* ---------- award layer ---------- */")
          + cut_from(C2, "  .line{display:block;overflow:hidden}", "  /* ---------- NGN wire ---------- */").replace(".grain{animation:none}", "")
          + cut_from(C2, "  /* ---------- co-op rail ---------- */", "  /* ---------- STUDENT LIFE IMAX ---------- */"))
globe_mk  = cut_from(C2, '<div class="scrolly" id="experience">', '<div class="sheet">')
globe_mk  = globe_mk.replace('<div class="scrolly" id="experience">', '<div class="scrolly" id="campuses">')
sheet_mk  = cut_from(C2, '<div class="sheet">', '<section class="voices-c"')
c2_js = (cut_from(C2, "/* ============ globe data ============ */", "/* ============ research counters ============ */")
         + cut_from(C2, "/* ============ research counters ============ */", "/* ============ live NGN wire")
         + cut_from(C2, "/* ============ co-op rail ============ */", "/* ============ subtle scroll movement ============ */"))
assert 'id="coop"' in sheet_mk and 'id="research"' in sheet_mk
COPY = [
 (globe_mk, "Northeastern's 14 campuses, 8 N.U.in locations, and 4,705 Fall 2026 co‑op placements. Scroll for the tour, click a red pin for a story, drag to rotate.",
            "Northeastern’s 14 campuses, eight N.U.in locations, and this fall’s co‑op locations. Scroll for the tour, select a red pin for a story, drag to rotate."),
 (globe_mk, '<div class="big"><b>14</b> campuses</div>\n        <p>A connected network of campuses across the U.S., U.K., and Canada, where each one opens doors to all the others.</p>',
            '<div class="big">One network across the world.</div>\n        <p>14 campuses across the U.S., U.K., and Canada.</p>'),
 (globe_mk, "<p>Through N.U.in, new students begin their Northeastern degree at one of eight partner institutions across Europe.</p>",
            "<p>Through N.U.in, new students begin their Northeastern degree at a partner institution in Europe.</p>"),
 (globe_mk, "</b> co‑op placements</div>", "</b> co‑ops</div>"),
 (globe_mk, "<p>Full-time, paid positions in every kind of workplace.</p>",
            "<p>More than a century of students working with employer partners around the world.</p>"),
 (sheet_mk, "patents and counting", "patents"),
 (sheet_mk, "Our research story starts in the world.", "Where removing barriers ignites collaboration, innovation, and results"),
 (sheet_mk, "While most research institutions study the world, our faculty and students solve problems at the center of it.",
            "We offer leading-edge labs, tools, and technologies for our researchers and partners to tackle large-scale problems from all angles."),
 (sheet_mk, '<span class="g-n">5,000+</span><span class="g-l">cities and towns</span>', '<span class="g-n">3,900+</span><span class="g-l">employer partners worldwide</span>'),
 (sheet_mk, '<span class="g-n">10,000+</span><span class="g-l">employer partners</span>', '<span class="g-n">100+</span><span class="g-l">years of co‑op</span>'),
 (sheet_mk, '<span class="g-n">250+</span><span class="g-l">countries and territories</span>', '<span class="g-n">350K+</span><span class="g-l">alumni around the world</span>'),
 (sheet_mk, ">Research coverage on NGN<", ">More research on NGN<"),
]
fixed = {}
for src_name, a, b in [("globe_mk" if blk is globe_mk else "sheet_mk", a, b) for blk, a, b in COPY]:
    blk = globals()[src_name]
    assert blk.count(a) == 1, a[:70]
    globals()[src_name] = blk.replace(a, b)
# the globe tour ends on the co-op beat (the outro step is cut)
_i = globe_mk.index('    <div class="step" data-step="outro">'); _j = globe_mk.index("\n  </div>\n</div>", _i)
globe_mk = globe_mk[:_i].rstrip() + "\n" + globe_mk[_j:]
# 2. the co-op story card never covers the pin: while it's open the globe eases left of it
assert c2_js.count("W > 900 ? W * 0.62 : W * 0.5") == 3  # render, dot hover, pin click
c2_js = c2_js.replace("W > 900 ? W * 0.62 : W * 0.5", "globeCX()")
_n = c2_js.count("const cy = H * 0.52;"); assert _n >= 2, _n
c2_js = c2_js.replace("const cy = H * 0.52;", "const cy = H * ((W > 720 && !window.GLOBE_ALL) ? 0.52 : (window.GLOBE_CY || 0.6));  /* phones: position set by the mobile treatment */")
_n = c2_js.count("Math.min(W, H) * 0.42"); assert _n == 4, _n
c2_js = c2_js.replace("Math.min(W, H) * 0.42", "Math.min(W, H) * ((W > 720 && !window.GLOBE_ALL) ? 0.42 : (window.GLOBE_R || 0.42))")
assert c2_js.count('$("#coopcount").textContent = ') == 1
c2_js = c2_js.replace('$("#coopcount").textContent = ', '($("#coopcount") || {}).textContent = ')
_l = """  let bx = cand[0][0], by = cand[0][1];
  for (const [tx, ty] of cand) {
    const hit = labelBoxes.some(b =>
      tx < b.x + b.w && b.x < tx + w + 12 && ty < b.y + b.h && b.y < ty + 18);
    if (!hit) { bx = tx; by = ty; break; }
  }"""
assert c2_js.count(_l) == 1
c2_js = c2_js.replace(_l, """  let bx = cand[0][0], by = cand[0][1], placed = false;
  for (const [tx, ty] of cand) {
    const hit = labelBoxes.some(b =>
      tx < b.x + b.w && b.x < tx + w + 12 && ty < b.y + b.h && b.y < ty + 18);
    if (!hit) { bx = tx; by = ty; placed = true; break; }
  }
  if (!placed && W <= 720) return;  /* phones: a label that can't sit clear of the others is dropped, its dot stays */""")
_f = "ctx.font = \"500 11px 'FF Real Head','Lato',sans-serif\";"
assert c2_js.count(_f) == 1
c2_js = c2_js.replace(_f, "ctx.font = (W <= 720 ? \"500 10.5px\" : \"500 11px\") + \" 'FF Real Head','Lato',sans-serif\";")
_d = 'canvas.addEventListener("pointerdown", e => {\n  dragging = true;'
assert c2_js.count(_d) == 1
c2_js = c2_js.replace(_d, 'canvas.addEventListener("pointerdown", e => {\n  if (W <= 720 || window.GLOBE_LOCK) return;  /* phones: the globe is locked; the page scrolls freely */\n  dragging = true;')
_pa = "  /* story pins: pulsing markers that open the docked story card */"
assert c2_js.count(_pa) == 1
c2_js = c2_js.replace(_pa, r"""  /* path arcs: thin great-circle arcs that draw themselves in, led by a soft point; fade as a group */
  if (window.PATH_ARCS && window.PATH_ARCS.length) {
    const slerp = (a, b, t) => {
      const V = (la, lo) => { const p = la * RAD, l = lo * RAD; return [Math.cos(p) * Math.cos(l), Math.cos(p) * Math.sin(l), Math.sin(p)]; };
      const u = V(a[0], a[1]), w = V(b[0], b[1]);
      const om = Math.acos(Math.max(-1, Math.min(1, u[0] * w[0] + u[1] * w[1] + u[2] * w[2])));
      if (om < 1e-6) return [a[0], a[1], 0];
      const sa = Math.sin((1 - t) * om) / Math.sin(om), sb = Math.sin(t * om) / Math.sin(om);
      const x = sa * u[0] + sb * w[0], y = sa * u[1] + sb * w[1], z = sa * u[2] + sb * w[2];
      return [Math.asin(Math.max(-1, Math.min(1, z))) / RAD, Math.atan2(y, x) / RAD, om];
    };
    const fadeA = window.PATH_FADE ?? 1;  /* ?? so a finished fade (0) stays at 0 */
    for (const arc of window.PATH_ARCS) {
      const f = reduceMotion ? 1 : Math.min(1, (now - arc.t0) / 900), ease = 1 - Math.pow(1 - f, 3);
      const om = slerp(arc.a, arc.b, .5)[2] || 0, lift = Math.min(.22, .05 + om * .12) * (window.PATH_LIFT || 1), N = 48;
      let started = false, head = null;
      ctx.beginPath();
      for (let i = 0; i <= N * ease; i++) {
        const t = i / N, q = slerp(arc.a, arc.b, t), pr = project(q[0], q[1], R, cx, cy, Math.sin(Math.PI * t) * lift);
        if (pr[2] > 0.02) { if (!started) { ctx.moveTo(pr[0], pr[1]); started = true; } else ctx.lineTo(pr[0], pr[1]); head = pr; }
        else started = false;
      }
      ctx.lineCap = "round";
      ctx.strokeStyle = `rgba(238,85,102,${.16 * fadeA})`; ctx.lineWidth = 5; ctx.stroke();
      ctx.strokeStyle = `rgba(255,190,200,${.75 * fadeA})`; ctx.lineWidth = 1.3; ctx.stroke();
      if (head && f < 1) { ctx.beginPath(); ctx.arc(head[0], head[1], 3, 0, 7); ctx.fillStyle = `rgba(255,255,255,${.95 * fadeA})`; ctx.fill(); }
    }
  }
  if (window.PATH_LABEL) {
    const L = window.PATH_LABEL, pr = project(L.ll[0], L.ll[1], R, cx, cy);
    const nb = labelBoxes.length, la = L.at ? Math.max(0, Math.min(1, (now - L.at) / 300)) : 1;
    if (pr[2] > 0 && la > 0) label(L.text, pr[0], pr[1], la, W <= 720 ? 16 : 18);
    window.PATH_LABEL_BOX = labelBoxes.length > nb ? labelBoxes[labelBoxes.length - 1] : null;
  } else window.PATH_LABEL_BOX = null;
""" + _pa)
_e = "const entryUpd = () => {\n  const r = scEl.getBoundingClientRect();"
assert c2_js.count(_e) == 1
c2_js = c2_js.replace(_e, "const entryUpd = () => {\n  if (window.GV_NOENTRY) return;\n  const r = scEl.getBoundingClientRect();")
for _a, _b in (("const dip = dist < 12 ? 0 :", "const dip = window.FLY_NODIP || dist < 12 ? 0 :"),
               ("dur: 800 + Math.min(1000, dist * 7) }", "dur: (800 + Math.min(1000, dist * 7)) * (window.FLY_SLOW || 1) }"),
               ("const e = easeIO(t);", "const e = (window.FLY_EASE || easeIO)(t);"),
               ("function label(text, x, y, a) {\n", """function label(text, x, y, a, px) {
  if (px) {  /* the paths treatment's single, larger label */
    /* unboxed: a soft shadow carries it over the map */
    ctx.font = "600 " + px + "px 'FF Real Head','Lato',sans-serif"; ctx.textAlign = "left"; ctx.textBaseline = "middle";
    const w = ctx.measureText(text).width, h = Math.round(px * 1.3), bx = x + 14, by = y - h / 2;
    labelBoxes.push({ x: bx, y: by, w, h });
    ctx.save(); ctx.shadowColor = `rgba(0,0,0,${.85 * a})`; ctx.shadowBlur = 10;
    ctx.fillStyle = `rgba(255,255,255,${a})`; ctx.fillText(text, bx, y + .5); ctx.restore();
    return;
  }
""")):
    assert c2_js.count(_a) == 1, _a
    c2_js = c2_js.replace(_a, _b)
assert c2_js.count("function render(now) {") == 1
c2_js = c2_js.replace("function render(now) {", """let globeShift = 0;
const globeCX = () => window.GLOBE_ALL ? W * 0.5 : (W > 900 ? W * 0.62 - globeShift : W * 0.5);
function render(now) {""")
assert c2_js.count("function frame(now) {\n  if (stageVisible) {") == 1
c2_js = c2_js.replace("function frame(now) {\n  if (stageVisible) {", """function frame(now) {
  if (stageVisible) {
    const gc = W > 900 && !gtCard.hidden ? gtCard.getBoundingClientRect() : null;
    globeShift += ((gc ? Math.max(0, W * 0.62 - (gc.left - 240)) : 0) - globeShift) * (reduceMotion ? 1 : .06);""")
assert c2_js.count("const COOP_DISPLAY_TOTAL = 500000;") == 1
_t = '<b>${fmt(best[2])}</b> co‑op placement${best[2] === 1 ? "" : "s"}`'
assert c2_js.count(_t) == 1
c2_js = c2_js.replace(_t, '<b>${fmt(best[2])}</b> co‑op${best[2] === 1 ? "" : "s"} this fall`')
# the co-op beat counts concept 2's all-time figure (500,000): an unverified placeholder, VERIFY before external use
c2_js = c2_js.replace("/* all-time placements, VERIFY before external use */", "/* all-time co-ops, VERIFY before external use */")

# the portrait reel (concept 4's idea): b-roll clips from seven university films, each card
# looping its own segment. Segments picked from sampled frames on 2026-09-30; the co-op
# and Jamie Wong films are mostly interviews, so they contribute at most one clip.
FILM = {
 "adm":  "https://admissions.northeastern.edu/wp-content/uploads/2023/08/07.21.26_UG-Website-Hero-Video.mp4",
 "dmsb": "https://damore-mckim.northeastern.edu/wp-content/uploads/2026/03/dmsb-hero-noaudio.webm",
 "res":  "https://research.northeastern.edu/wp-content/uploads/2024/06/VID_Homepage-Hero_Small.mp4",
 "lon":  "https://www.nulondon.ac.uk/wp-content/uploads/2026/02/Discover-your-path-at-Northeastern-University-London.mp4",
 "nyc":  "https://nyc.northeastern.edu/wp-content/uploads/NYC-Home_SLOW.mp4",
 "roux": "https://roux.northeastern.edu/wp-content/uploads/MAGGIE-VIDEO-4-2.mp4",
 "coop": "https://www.northeastern.edu/wp-content/uploads/The-Co-Op-Experience_Video-2-Fusion-v3.mp4",
 "hero": "../hero.mp4",
}
CLIPS = [("adm", .5, 6), ("res", .5, 6), ("lon", 24, 29.5), ("dmsb", 8.5, 14), ("hero", 0, 9), ("adm", 7, 11.5),
         ("nyc", 0, 9), ("res", 6.5, 9.5), ("lon", 55, 62), ("dmsb", 31, 36), ("adm", 30, 36), ("coop", 7.5, 9.5),
         ("res", 16, 19.5), ("lon", 3, 9), ("adm", 13, 18), ("roux", 1, 7)]
reel_mk = ('<section class="reel" aria-hidden="true"><div class="reel-track" id="reelTrack">'
           + "".join(f'<div class="vidcard"><video muted playsinline preload="none" data-src="{FILM[f]}" data-s="{a}" data-e="{b}"></video></div>' for f, a, b in CLIPS)
           + "</div></section>\n")

# closer slideshow photos (NGN, 1400px)
CLOSER_PHOTOS = [U + "/" + f for f in (
 "2024/07/Convocation1400.jpg",                        # 1 phone lights, convocation arena
 "2026/08/LondonConvocation1400.jpg",                  # 2 London convocation, overhead on confetti
 "2026/09/091026_CV_London_Convocation_041.jpg",       # 3 London convocation, confetti on stage
 "2026/09/090826_RW_NUOAK_TasteConvocation_022.jpg",   # 4 Oakland convocation
 "2026/09/090826_AS_NYC_convocation_072.jpg",          # 5 NYC convocation
 "2026/09/091626_MMU_Parade_of_Flags_007.jpg",         # 6 Parade of Flags
 "2026/09/Fenway1400.jpg",                             # 7 graduates with home-country flags
 "2026/09/1400_1a30c6.jpg")]                           # 8 students in motion on a campus path
admit_mk = rest_mk[:rest_mk.index("</section>") + len("</section>")]
_a = "<p>First-year, transfer, graduate, online, or start abroad with N.U.in. However you get here, experience starts on day one.</p>"
assert admit_mk.count(_a) == 1
admit_mk = admit_mk.replace("<h2>Your turn.</h2>", "<h2>Your turn.</h2>").replace(_a,
    "<p>The world doesn’t wait. Neither do you. Undergraduate, graduate, transfer, and online programs across our campus network.</p>")
for a, b in (('<a class="pill red" href="#">Apply</a>', '<a class="pill red" href="https://admissions.northeastern.edu/">Apply</a>'),
             ('<a class="pill ghostw" href="#">Visit</a>', '<a class="pill ghostw" href="https://admissions.northeastern.edu/visit/">Visit</a>'),
             ('<a class="pill ghostw" href="#">Request info</a>', '<a class="pill ghostw" href="https://studentfinance.northeastern.edu/">Financial aid</a>')):
    assert admit_mk.count(a) == 1, a
    admit_mk = admit_mk.replace(a, b)
_bg = """<div class="bg" data-plx="34" style="background-image:url('https://news.northeastern.edu/wp-content/uploads/2025/05/1400-thumbnail-v2.png')"></div>"""
assert admit_mk.count(_bg) == 1
# London stage, Oakland, NYC, phone lights, London overhead, Parade of Flags, campus path, Fenway flags
_order = [2, 3, 4, 0, 1, 5, 7, 6]
admit_mk = admit_mk.replace(_bg, '<div class="bg" data-plx="34">' + "".join(
    '<img%s data-src="%s" alt="" decoding="async">' % (' class="on"' if k == 0 else "", CLOSER_PHOTOS[n]) for k, n in enumerate(_order)) + "</div>")

# features: Co-op, Research, Global network, Admissions (student life + athletics), Entrepreneurship
S = {s["title"]: s for s in SHOWS}
EP_ENT = [
 ep("Student startup develops hands-on learning toy for future engineers", U+"/2026/07/072426_MM_NextTile_002.jpg", NGN+"/2026/07/31/nexttile-startup-stem-northeastern/"),
 ep("Founders pitch startups in Dragons’ Den-style event for funding", U+"/2026/06/060426_CV_GLS_day1_048.jpg", NGN+"/2026/06/05/startup-pitch-competition-london-summit/"),
 ep("Revolutionizing dental hygiene, starting with your toothbrush", U+"/2025/08/NOOK_1400.jpg", NGN+"/2026/07/15/how-to-keep-toothbrush-clean-nook/"),
 ep("Is this healthy energy drink coming to a store near you?", U+"/2026/03/033126_MM_The_Market_031.jpg", NGN+"/2026/04/10/healthy-energy-drink-journee/"),
]
def feat(t, src, v=None, still=None, card=None, **kw):
    s = S[src] if src else {}
    return {"t": t, "v": v, "img": still or s.get("still") or s.get("thumb"), "card": card or s.get("thumb"),
            "syn": kw["syn"],
            "cta": kw.get("cta", s.get("cta")), "eps": kw.get("eps", s.get("eps", []))[:4], "h": kw["h"]}
# every feature plays a full 1920x1080 film (the 640x360 proxies looked blown up full-bleed)
HD = {"coop": "https://www.northeastern.edu/wp-content/uploads/The-Co-Op-Experience_Video-2-Fusion-v3.mp4",
      "research": "https://research.northeastern.edu/wp-content/uploads/2024/06/VID_Homepage-Hero_Small.mp4",
      "global": "https://admissions.northeastern.edu/wp-content/uploads/2023/08/07.21.26_UG-Website-Hero-Video.mp4",
      "ai": "https://roux.northeastern.edu/wp-content/uploads/MAGGIE-VIDEO-4-2.mp4",
      "ent": "https://damore-mckim.northeastern.edu/wp-content/uploads/2026/03/dmsb-hero-noaudio.webm"}
# copy: brand voice (trusted, empowering, confident), brand facts only. Co-op numbers from the
# key-terms entry; network numbers from the boilerplate; research line from the research messaging page.
FEATS = [
 feat("Co‑op", "Co‑op", v=HD["coop"], h="Learn by doing", card="../img/aquarium-dive.jpg",
      syn="Every part of your journey at Northeastern is built for immersive learning, innovation, and integrating emerging technologies, like AI, to enhance creativity and career readiness.",
      cta={"label": "Explore co‑op", "href": "https://www.northeastern.edu/co-op"}),
 feat("Research", "Research", v=HD["research"], h="Breakthroughs begin here",
      syn="Northeastern is an R1 research enterprise that advances work in health, security, and sustainability with partners in industry, government, and communities.",
      cta={"label": "Explore research", "href": "https://research.northeastern.edu/"}),
 feat("Global network", "Global network", v=HD["global"], h="Learn and innovate without boundaries", card="../img/global-london.jpg",
      syn="Our dynamic network of campuses, alumni, and partners is designed to maximize opportunities for powerful educational experiences, influential research, and compelling collaborations in every part of the world.",
      cta={"label": "See the network", "href": "#campuses"}),
 feat("AI", None, v=HD["ai"], h="Responsible, human-centered AI", still=U+"/2026/09/AImakerspace1400.jpg",
      card=U+"/2026/09/Francesco_Restuccia_1400.jpg",
      syn="We bring together researchers, applied AI experts, educators, and industry partners to advance AI in health, life sciences, responsible AI, climate and sustainability, and real-world organizational practice.",
      cta={"label": "Explore AI at Northeastern", "href": "https://www.northeastern.edu/ai/"},
      eps=[ep("Query, create or be curious at new AI Makerspace in Boston", U+"/2026/09/AImakerspace1400.jpg", NGN+"/2026/09/23/ai-makerspace-boston-campus/"),
           ep("The student refining AI at one of the largest real estate firms", U+"/2026/08/Co-op_AI_1400.jpg", NGN+"/2026/09/09/real-estate-ai-co-op/"),
           ep("In Serbia, she helped build an AI to give activists worldwide a leg up", U+"/2026/08/081426_MM_Ayla_DiBattista_006.jpg", NGN+"/2026/09/03/ayla-dibattista-co-op-northeastern/"),
           ep("This professor is making AI systems more aware of their ignorance", U+"/2026/09/Francesco_Restuccia_1400.jpg", NGN+"/2026/09/21/northeastern-pecase-award-2026/")]),
 feat("Entrepreneurship", None, v=HD["ent"], h="Built to move ideas forward. Faster.", still=U+"/2026/06/060426_CV_GLS_day1_048.jpg", card=U+"/2026/07/072426_MM_NextTile_002.jpg",
      syn="Learn, create, launch, and scale with one of the most extensive entrepreneurship support systems in the world.",
      cta={"label": "Read founder stories", "href": NGN + "/tag/entrepreneurship/"}, eps=EP_ENT),
]
assert len(FEATS) == 5 and all(f["eps"] and f["img"] and f["card"] and f["cta"] and f["v"] in HD.values() for f in FEATS)

def layer(i, f):
    on = " on" if i == 0 else ""
    if f["v"]:
        return (f'<div class="hl{on}"><video muted loop playsinline preload="{"auto" if i == 0 else "none"}" '
                f'poster="{f["img"]}" src="{f["v"]}"></video></div>')
    return f'<div class="hl kb{on}"><img src="{f["img"]}" alt="" loading="lazy"></div>'

def show_card(i, f):
    return (f'<button class="ln" data-i="{i}" aria-pressed="{"true" if i == 0 else "false"}">'
            f'<img src="{f["card"]}" alt="" loading="lazy">'
            f'<span class="ln-t">{h(f["t"])}</span><i class="ln-pb"></i></button>')

F0 = FEATS[0]
HERO = f'''<script>if (/[?&]hero=b\\b/.test(location.search)) document.documentElement.classList.add("hero-b")</script>
<section class="hx" id="top" aria-label="Featured">
  <div class="hx-media" id="hxMedia">{"".join(layer(i, f) for i, f in enumerate(FEATS))}</div>
  <div class="hx-shade"></div>
  <h1 class="vh">Northeastern University</h1>
  <div class="hx-in" id="hxIn">
    <div class="hx-copy" aria-live="polite">
      <h2 class="hx-title" id="hxTitle">{h(F0["h"])}</h2>
      <p class="hx-syn" id="hxSyn">{h(F0["syn"])}</p>
      <a class="hx-btn" id="hxCta" href="#" hidden><span id="hxCtaL"></span>{g["ICON_ARROW"]}</a>
    </div>
    <aside class="hx-eps" id="hxEps" aria-label="Stories from this feature"></aside>
  </div>
  <div class="hx-shows" id="hxShows">
    <div class="hx-lineup" role="group" aria-label="Choose a feature">{"".join(show_card(i, f) for i, f in enumerate(FEATS))}</div>
  </div>
</section>
'''

CHEV = '<svg width="30" height="30" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
def row(rid, label, q=None, hidden=True):
    dq = f' data-q="{q}"' if q is not None else ""
    return (f'<section class="crow"{" hidden" if hidden else ""}{dq} id="{rid}" aria-label="{label}">'
            f'<div class="wrap"><h3>{label}</h3></div><div class="crow-body">'
            f'<button class="pad prev" aria-label="Scroll {label} back" disabled>{CHEV}</button>'
            f'<div class="crow-strip"></div>'
            f'<button class="pad next" aria-label="Scroll {label} forward">{CHEV}</button></div></section>\n')

NGN_LOCKUP = open(os.path.join(HERE, "ngn-lockup.svg")).read().replace('<svg class="ngn-lockup"', '<svg class="ngn-lockup" aria-hidden="true" focusable="false"')
_m0 = NGN_LOCKUP.index('<g class="ngn-lockup__monogram">'); _m1 = NGN_LOCKUP.index("</g>", _m0) + 4
NGN_LOCKUP = NGN_LOCKUP[:_m0] + NGN_LOCKUP[_m1:]
assert NGN_LOCKUP.count('viewBox="0 0 573 48"') == 1 and "ngn-lockup__monogram-block" not in NGN_LOCKUP.split("</style>")[1]
NGN_LOCKUP = NGN_LOCKUP.replace('viewBox="0 0 573 48"', 'viewBox="64 0 509 48"')
ROWS = ('<section class="rows" aria-labelledby="rowsT">\n'
        '  <div class="wrap rows-head"><h2 id="rowsT"><a href="https://news.northeastern.edu/"><span class="vh">Northeastern Global News</span>'
        + NGN_LOCKUP + '</a></h2><p class="rows-tag">Stories from the university and the world.</p></div>\n'
        + row("ngnRow", "Latest", "", hidden=False)
        + row("entRow", "Entrepreneurship", "tags=9287")
        + row("aiRow", "Human-Centered AI", "tags=9865,9843")
        + row("uniRow", "University News", "categories=7")
        + row("researchRow", "Research", "categories=21443")
        + "</section>\n")

NEW_CSS = r'''
  /* ---------- concept-7: immersive streaming ---------- */
  body{background:var(--dark)}
  /* the .wrap content edge; % resolves against each full-width element's own box */
  :root{--edge:max(clamp(20px,4vw,48px), calc((100% - 1280px) / 2 + clamp(20px,4vw,48px)))}
  ::selection{background:var(--red);color:#fff}
  .vh{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
  .vidcard{position:relative;border-radius:14px;overflow:hidden;background:#141419}
  .vidcard video{width:100%;height:100%;object-fit:cover;display:block}

  /* billboard */
  .hx{position:relative;height:100svh;min-height:760px;overflow:hidden;color:#fff;background:#000}
  .hx-media{position:absolute;inset:0;will-change:transform}
  .hl{position:absolute;inset:0;opacity:0;transition:opacity 1s var(--ease)}
  .hl.on{opacity:1}
  .hl video,.hl img{width:100%;height:100%;object-fit:cover;display:block}
  .hl.kb.on img{animation:kb 24s ease-in-out infinite alternate}
  @keyframes kb{from{transform:scale(1)}to{transform:scale(1.1) translate(-1.5%,-1%)}}
  .hx-shade{position:absolute;inset:0;pointer-events:none;
    background:linear-gradient(to right,rgba(11,11,14,.78) 0%,rgba(11,11,14,.3) 38%,transparent 62%),
               linear-gradient(to top,var(--dark) 0%,rgba(11,11,14,.72) 34%,transparent 62%)}
  /* the copy and the stories panel sit a full breath above the feature row */
  .hx-in{position:absolute;z-index:2;left:0;right:0;bottom:calc(var(--shh,280px) + clamp(56px,9svh,110px));
    display:flex;align-items:flex-end;justify-content:space-between;gap:48px;padding:0 var(--edge)}
  .hx-copy,.hx-eps{transition:opacity .35s var(--ease)}
  .hx-in.swap .hx-copy,.hx-in.swap .hx-eps{opacity:0}
  .hx-copy{flex:1 1 auto;min-width:0;max-width:760px}
  .hx-title{margin:0;font-size:clamp(48px,6.2vw,104px);font-weight:200;letter-spacing:-.035em;line-height:.98;text-wrap:balance;
    min-height:calc(2 * .98em);display:flex;align-items:flex-end}
  .hx-syn{margin:18px 0 0;font-size:clamp(16px,1.25vw,19px);line-height:1.5;color:#E5E5E5;max-width:44ch}
  .hx-btn{all:unset;box-sizing:border-box;display:inline-flex;align-items:center;gap:10px;height:48px;padding:0 24px;margin-top:22px;
    border-radius:999px;font-size:16px;font-weight:600;cursor:pointer;background:#fff;color:#0B0B0E;transition:background .2s}
  .hx-btn:hover{background:rgba(255,255,255,.84)}
  .hx-btn[hidden]{display:none}
  .hx-btn:focus-visible,.ln:focus-visible,.cc:focus-visible,.pad:focus-visible{outline:2px solid #fff;outline-offset:3px}
  .hx-eps{width:min(360px,32%);flex:0 0 auto}
  .hx-eps h3{margin:0 0 4px;font-size:17px;font-weight:600}
  .ep{display:grid;grid-template-columns:104px 1fr;gap:14px;align-items:center;padding:7px;border-radius:12px;color:#fff;
    background:rgba(20,20,26,.55);backdrop-filter:blur(14px);margin-top:8px;transition:background .2s}
  .ep:hover{background:rgba(255,255,255,.14)}
  .ep img{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:7px}
  .ep span{font-size:14px;line-height:1.35}

  /* closer slideshow */
  .admit .bg img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 45%;opacity:0;
    transition:opacity 1.8s ease-in-out;will-change:opacity}
  .admit .bg img.on{opacity:1}
  .admit .bg img.pre{opacity:.001}
  @media (prefers-reduced-motion: reduce){.admit .bg img{transition:none}}

  /* hero variant B (?hero=b) */
  .hero-b .hx-eps{display:none}
  .hero-b #hxCta{position:absolute;right:var(--edge);bottom:0;margin:0}
  .hero-b .hx-syn{max-width:52ch}
  @media (max-width:899px){.hero-b #hxCta{position:static;margin-top:22px}}

  /* feature cards under the hero */
  .hx-shows{position:absolute;z-index:3;left:0;right:0;bottom:clamp(18px,3svh,36px)}
  .hx-lineup{display:flex;gap:12px;overflow-x:auto;scrollbar-width:none;padding:10px var(--edge) 6px}
  .hx-lineup::-webkit-scrollbar{display:none}
  .ln{all:unset;box-sizing:border-box;cursor:pointer;position:relative;flex:1 1 0;min-width:0;height:clamp(130px,17svh,180px);
    border-radius:8px;overflow:hidden;background:#141419;transition:transform .35s var(--ease),box-shadow .35s var(--ease)}
  .ln img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.62) saturate(.85);transition:filter .35s}
  .ln::after{content:"";position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,.72) 0%,transparent 48%)}
  .ln-t{position:absolute;z-index:2;left:10px;right:10px;bottom:11px;font-size:clamp(19px,1.6vw,25px);font-weight:400;line-height:1;
    letter-spacing:-.02em;color:#fff;text-shadow:0 2px 12px rgba(0,0,0,.45)}
  .ln:hover{transform:translateY(-4px)}
  .ln:hover img{filter:brightness(.9)}
  .ln[aria-pressed="true"]{transform:translateY(-8px);box-shadow:0 0 0 2px #fff,0 18px 40px rgba(0,0,0,.6)}
  .ln[aria-pressed="true"] img{filter:none}
  .ln-pb{position:absolute;z-index:3;left:10px;right:10px;top:10px;height:3px;border-radius:3px;overflow:hidden;
    background:rgba(255,255,255,.28);opacity:0;transition:opacity .3s}
  .ln[aria-pressed="true"] .ln-pb{opacity:1}
  .ln-pb::after{content:"";display:block;height:100%;width:calc(var(--pb,0) * 100%);background:#fff;border-radius:inherit}
  @media (max-width:899px){.hx-eps{display:none}}
  @media (max-width:640px){.hx{min-height:700px}.hx-btn{height:44px;padding:0 18px;font-size:15px}.ln{flex:0 0 158px;height:104px}.ln-t{font-size:17px}}
  @media (prefers-reduced-motion: reduce){.hl,.hx-copy,.hx-eps,.ln{transition:none}.hl.kb.on img{animation:none}}

  /* rows: a featured card, then portrait posters; edge paddles scroll */
  .rows{position:relative;z-index:2;color:#fff;padding:clamp(40px,7svh,80px) 0 clamp(60px,9svh,110px)}
  .rows-head h2{margin:0;line-height:0}
  .rows-head h2 a{display:inline-block;--wp--custom--color--emphasize:#fff;--wp--custom--color--background:var(--dark)}
  .rows-head .ngn-lockup{height:clamp(22px,2.2vw,30px);width:auto;display:block}
  .rows-tag{margin:12px 0 0;font-size:clamp(15px,1.2vw,17px);color:#A9A9B2}
  .crow{margin-top:clamp(28px,4.4svh,50px);--ch:clamp(280px,23vw,360px);--pw:calc(var(--ch) * 2 / 3)}
  .crow[hidden]{display:none}
  .crow h3{margin:0;font-size:clamp(17px,1.4vw,21px);font-weight:600;color:#E5E5E5}
  .crow-body{position:relative}
  .crow-strip{display:flex;gap:12px;overflow-x:auto;scrollbar-width:none;padding:14px var(--edge) 14px;scroll-padding-inline:var(--edge)}
  .crow-strip::-webkit-scrollbar{display:none}
  .cc{position:relative;flex:0 0 auto;width:var(--pw);height:var(--ch);border-radius:10px;overflow:hidden;background:#141419;color:#fff}
  .cc img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .6s var(--ease),filter .4s}
  .cc:hover img{transform:scale(1.04);filter:brightness(1.08)}
  .cc::after{content:"";position:absolute;inset:0;pointer-events:none;
    background:linear-gradient(to top,rgba(0,0,0,.94) 0%,rgba(0,0,0,.72) 28%,rgba(0,0,0,.2) 55%,transparent 72%)}
  .cc-t{position:absolute;z-index:2;left:0;right:0;bottom:0;padding:0 16px 18px;font-size:clamp(15px,1.12vw,18px);font-weight:600;
    line-height:1.2;letter-spacing:-.005em;text-wrap:balance;text-shadow:0 1px 10px rgba(0,0,0,.6)}
  .pad{position:absolute;z-index:3;top:14px;bottom:14px;width:max(52px, calc(var(--edge) - 8px));border:0;padding:0;cursor:pointer;color:#fff;
    display:flex;align-items:center;justify-content:center;opacity:0;transition:opacity .25s}
  .pad.prev{left:0;background:linear-gradient(to right,rgba(11,11,14,.92),rgba(11,11,14,.5) 70%,transparent)}
  .pad.next{right:0;background:linear-gradient(to left,rgba(11,11,14,.92),rgba(11,11,14,.5) 70%,transparent)}
  .pad.prev svg{transform:scaleX(-1)}
  .pad svg{transition:transform .25s var(--ease)}
  .pad.next:hover svg{transform:scale(1.25)}
  .pad.prev:hover svg{transform:scaleX(-1) scale(1.25)}
  .crow-body:hover .pad:not(:disabled),.pad:focus-visible{opacity:1}
  .pad:disabled{visibility:hidden}
  @media (hover:none){.pad{display:none}}

  /* the reel: portrait b-roll drifting left to right */
  .reel{position:relative;z-index:2;padding:clamp(90px,13svh,180px) 0;overflow-x:auto;overflow-y:hidden;scrollbar-width:none;
    overscroll-behavior-x:contain;cursor:grab}
  .reel::-webkit-scrollbar{display:none}
  .reel.drag{cursor:grabbing}
  .reel-track{display:flex;gap:16px;width:max-content}
  .reel .vidcard{flex:0 0 auto;height:min(66svh,740px);aspect-ratio:9/16}
  @media (max-width:820px){.reel{padding:clamp(56px,8svh,90px) 0}.reel .vidcard{height:70svh}}
  @media (prefers-reduced-motion: reduce){.reel{overflow-x:auto}}

  /* row mockup A · Preview */
  .pv{position:absolute;z-index:40;display:block;border-radius:12px;overflow:hidden;background:#18181D;color:#fff;
    box-shadow:0 30px 70px rgba(0,0,0,.65),0 0 0 1px rgba(255,255,255,.08);opacity:0;pointer-events:none;
    transition:transform .34s cubic-bezier(.2,.8,.2,1),opacity .2s}
  .pv.on{opacity:1;pointer-events:auto}
  .pv-img{display:block;width:100%;aspect-ratio:16/9;object-fit:cover}
  .pv-b{display:block;padding:16px 18px 18px;opacity:0;transition:opacity .25s .14s}
  .pv.on .pv-b{opacity:1}
  .pv-meta{display:block;font-size:13px;color:#A9A9B2}
  .pv-t{display:block;margin-top:6px;font-size:18px;font-weight:600;line-height:1.25;text-wrap:balance}
  .pv-x{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;margin-top:8px;font-size:14.5px;line-height:1.45;color:#D4D4D4}
  .pv-cta{display:inline-flex;align-items:center;gap:8px;margin-top:14px;height:38px;padding:0 16px;border-radius:999px;background:#fff;color:#0B0B0E;font-size:14px;font-weight:600}

  /* row mockup B · Spotlight (quiet): caption over the strip, faint color wash, focused poster lifts */
  .rows-b .crow{position:relative;display:flex;flex-direction:column;--ch:clamp(250px,21vw,320px)}
  .rows-b .crow > .wrap{position:relative;z-index:1;width:100%}
  .sp-bg{position:absolute;left:0;right:0;top:-12%;bottom:-12%;pointer-events:none;
    -webkit-mask-image:radial-gradient(70% 60% at 35% 55%,#000,transparent);mask-image:radial-gradient(70% 60% at 35% 55%,#000,transparent)}
  .sp-bg i{position:absolute;inset:0;background-size:cover;background-position:center;opacity:0;filter:blur(70px) saturate(1.3);transition:opacity 1.1s var(--ease)}
  .sp-bg i.on{opacity:.32}
  .sp-in{position:relative;z-index:1;order:1;padding:0 var(--edge);margin-top:12px}
  .sp-copy{max-width:720px;min-height:calc(13px * 1.5 + 2 * 1.2em * 1 + 2 * 15.5px * 1.45 + 56px);transition:opacity .22s}
  .sp-copy.swap{opacity:0}
  .sp-meta,.cf-meta{margin:0;font-size:13.5px;color:#A9A9B2}
  .sp-t{margin:0;font-size:clamp(20px,1.7vw,26px);font-weight:400;letter-spacing:-.012em;line-height:1.2;
    display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
  .sp-x,.cf-x{margin:8px 0 0;font-size:15.5px;line-height:1.45;color:#C9C9CF;max-width:62ch;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
  .sp-btn{margin-top:10px;color:#fff}
  .rows-b .crow-body{order:2;z-index:1}
  .rows-b .cc{transition:transform .35s var(--ease),box-shadow .35s var(--ease)}
  .rows-b .cc img{transition:filter .35s,transform .6s var(--ease)}
  .rows-b .crow-strip:hover .cc:not(.on) img,.rows-b .cc:not(.on) img{filter:brightness(.55)}
  .rows-b .cc.on{transform:translateY(-6px);box-shadow:0 18px 40px rgba(0,0,0,.55)}
  @media (prefers-reduced-motion: reduce){.sp-bg i{transition:none}}

  /* B · full-bleed stage: the focused story's 1400px original fills the row (no zoom), text on a left gradient */
  .rows-bfull .crow{margin-top:clamp(12px,2svh,24px);min-height:clamp(600px,84svh,820px);overflow:hidden;
    padding-top:clamp(28px,5svh,56px);--ch:clamp(190px,15vw,232px)}
  .rows-bfull .crow > .wrap{margin-bottom:auto}
  .rows-bfull .crow + .crow{margin-top:clamp(36px,6svh,72px)}
  .rows-bfull .crow + .crow::before{content:"";position:absolute;z-index:2;top:0;left:var(--edge);right:var(--edge);height:1px;background:rgba(255,255,255,.14)}
  /* the photo is never drawn wider than its 1400px source: edge-to-edge up to 1400px viewports,
     centered with soft side fades beyond that (keeps it 1:1 or smaller, so it never upscales) */
  .rows-bfull .sp-bg{inset:0;left:50%;right:auto;width:min(100%,1400px);transform:translateX(-50%);-webkit-mask-image:none;mask-image:none}
  @media (min-width:1401px){
    .rows-bfull .sp-bg{-webkit-mask-image:linear-gradient(to right,transparent,#000 14%,#000 86%,transparent);
                       mask-image:linear-gradient(to right,transparent,#000 14%,#000 86%,transparent)}
  }
  .rows-bfull .sp-bg i{filter:none;background-position:center 35%;transition:opacity .8s var(--ease)}
  .rows-bfull .sp-bg i.on{opacity:1}
  .rows-bfull .sp-bg::after{content:"";position:absolute;inset:0;
    background:linear-gradient(to right,rgba(11,11,14,.94) 0%,rgba(11,11,14,.6) 38%,rgba(11,11,14,.08) 70%),
               linear-gradient(to top,var(--dark) 0%,rgba(11,11,14,.55) 32%,transparent 58%),linear-gradient(to bottom,var(--dark) 0%,transparent 16%)}
  .rows-bfull .sp-in{margin:0 0 clamp(14px,2.4svh,26px)}
  .rows-bfull .sp-copy{max-width:580px;min-height:0}
  .rows-bfull .sp-t{margin-top:0;font-size:clamp(30px,3.2vw,50px);font-weight:300;letter-spacing:-.025em;line-height:1.06;text-wrap:balance;-webkit-line-clamp:3}
  .rows-bfull .sp-x{margin-top:14px;font-size:16.5px;line-height:1.5;color:#D4D4D4;max-width:50ch;-webkit-line-clamp:3}
  .rows-bfull .sp-btn{display:inline-flex;align-items:center;height:44px;padding:0 22px;margin-top:20px;border:0;border-radius:999px;
    background:#fff;color:#0B0B0E;font-size:15px;font-weight:600}
  .rows-bfull .sp-btn:hover{background:rgba(255,255,255,.84);color:#0B0B0E}
  .rows-bfull .cc-t{font-size:14px;padding:0 12px 14px}
  .rows-bfull .cc.on{box-shadow:0 0 0 2px #fff,0 18px 40px rgba(0,0,0,.55)}

  .cc-pb{display:none}
  .rows-b .cc-pb{display:block;position:absolute;z-index:3;left:10px;right:10px;top:10px;height:3px;border-radius:3px;overflow:hidden;
    background:rgba(255,255,255,.28);opacity:0;transition:opacity .3s}
  .rows-b .cc.on .cc-pb{opacity:1}
  .rows-b .cc-pb::after{content:"";display:block;height:100%;width:calc(var(--pb,0) * 100%);background:#fff;border-radius:inherit}

  /* B3 (framed photo) vs B2 (quiet) */
  .sp-fig{display:none}
  .rows-bimg .sp-bg{display:none}
  .rows-bimg .crow{--ch:clamp(200px,16vw,250px)}
  .rows-bimg .sp-in{display:flex;align-items:center;justify-content:space-between;gap:clamp(28px,4vw,64px);margin:14px 0 6px}
  .rows-bimg .sp-copy{flex:1 1 0;max-width:560px;min-height:0}
  .rows-bimg .sp-t{font-size:clamp(24px,2.3vw,36px);font-weight:300;letter-spacing:-.02em;line-height:1.12;-webkit-line-clamp:3}
  .rows-bimg .sp-x{-webkit-line-clamp:3}
  .rows-bimg .sp-fig{display:block;position:relative;flex:0 0 min(52%,720px);aspect-ratio:16/9;border-radius:14px;overflow:hidden;background:#141419;
    box-shadow:0 24px 60px rgba(0,0,0,.5)}
  .sp-fig img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .6s var(--ease)}
  .sp-fig img.on{opacity:1}
  @media (max-width:820px){.rows-bimg .sp-in{flex-direction:column-reverse;align-items:stretch}.rows-bimg .sp-fig{flex:none;width:100%}}

  /* row mockup C · Coverflow */
  .cf{margin-top:clamp(24px,4svh,44px);overflow-x:clip;--chh:clamp(320px,44svh,470px);--cw:calc(var(--chh) * 2 / 3)}
  .cf-tabs{display:flex;gap:8px;flex-wrap:wrap}
  .cf-tab{all:unset;cursor:pointer;padding:10px 18px;border-radius:999px;font-size:15px;font-weight:500;color:#D4D4D4;border:1px solid rgba(255,255,255,.22);transition:.2s}
  .cf-tab:hover{border-color:#fff;color:#fff}
  .cf-tab[aria-selected="true"]{background:#fff;color:#0B0B0E;border-color:#fff}
  .cf-tab:focus-visible,.cf-nav:focus-visible,.cf-stage:focus-visible{outline:2px solid #fff;outline-offset:3px}
  .cf-stage{position:relative;height:var(--chh);margin:clamp(32px,5svh,56px) 0 clamp(60px,8svh,96px);perspective:1500px;transition:opacity .22s}
  .cf-stage.swap,.cf-copy.swap{opacity:0}
  .cf-card{position:absolute;left:50%;top:0;width:var(--cw);height:100%;margin-left:calc(var(--cw) / -2);border-radius:14px;overflow:hidden;
    transition:transform .7s cubic-bezier(.2,.8,.2,1),opacity .4s,filter .5s;filter:brightness(.5);box-shadow:0 30px 60px rgba(0,0,0,.55);
    -webkit-box-reflect:below 8px linear-gradient(transparent 72%,rgba(255,255,255,.16))}
  .cf-card.on{filter:none}
  .cf-card img{width:100%;height:100%;object-fit:cover;display:block;pointer-events:none}
  .cf-info{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:24px}
  .cf-copy{text-align:center;max-width:640px;margin:0 auto;transition:opacity .2s}
  .cf-t{margin:8px 0 0;font-size:clamp(24px,2.2vw,32px);font-weight:400;letter-spacing:-.015em;line-height:1.15;text-wrap:balance}
  .cf-x{margin-left:auto;margin-right:auto;-webkit-line-clamp:2}
  .cf-nav{all:unset;box-sizing:border-box;cursor:pointer;width:56px;height:56px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;
    background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.2);transition:background .2s,color .2s}
  .cf-nav:hover{background:#fff;color:#0B0B0E}
  .cf-nav svg{width:24px;height:24px}
  .cf-nav.prev svg{transform:scaleX(-1)}
  @media (max-width:720px){.cf-info{grid-template-columns:1fr}.cf-nav{display:none}}

  /* nav: top-level links beside the dropdowns, and the mobile menu's direct links */
  .mnav-a{font-size:14px;color:#fff;opacity:.85;padding:6px 2px;border-bottom:2px solid transparent;transition:.2s;white-space:nowrap}
  .mnav-a:hover{opacity:1}
  .mnav-btn{white-space:nowrap}
  .tkv-l{display:flex;justify-content:space-between;align-items:center;font-size:clamp(21px,2.4vw,28px);font-weight:300;color:#fff;
    border-bottom:1px solid rgba(255,255,255,.14);padding:18px 0}
  .tkv-l:hover{color:#FFB3BE}
  .mp-lead .storylink+.storylink{margin-top:6px}
  .mp-lead-wide{max-width:none;flex:0 0 300px}
  .mp-lead-wide .storylink{display:flex}

  /* phone menu hierarchy */
  .tkv-sub.open{columns:auto;padding:18px 0 30px}
  .tkv-ov{display:flex;flex-wrap:wrap;gap:8px;margin:2px 0 20px}
  .tkv-sub .tkv-ov a{padding:8px 16px;border:1px solid rgba(255,255,255,.3);border-radius:999px;font-size:14px;font-weight:500;color:#fff}
  .tkv-sub .tkv-ov a:hover{background:#fff;color:#0B0B0E}
  .tkv-sec+.tkv-sec{margin-top:20px}
  .tkv-h{margin:0 0 4px;font-size:13px;color:#8a8a92}
  .tkv-sub .tkv-sec a{display:block;padding:7px 0;font-size:16px;color:#E5E5E5}
  #tsub-5.open{display:grid;grid-template-columns:1fr 1fr;column-gap:16px}
  .tkv-g[aria-expanded="true"]{color:#fff}

  /* globe on phones: beat text rides high, the co-op story card is a compact strip docked at the bottom */
  @media (max-width:720px){
    /* every step's text shares one caption slot under the nav; the step at mid-screen is "current" */
    .gv-cap .step{min-height:95svh}
    .gv-cap .steps .step .card{position:fixed;z-index:6;top:84px;left:20px;right:20px;max-width:none;pointer-events:none;
      opacity:0;transform:translateY(16px);transition:opacity .28s ease,transform .28s ease;text-shadow:0 2px 18px rgba(0,0,0,.6)}
    .gv-cap .steps .step.past .card{transform:translateY(-14px)}
    .gv-cap .steps .step.cur .card{opacity:1;transform:none;pointer-events:auto;
      transition:opacity .55s .22s cubic-bezier(.2,.8,.2,1),transform .55s .22s cubic-bezier(.2,.8,.2,1)}
    .gv-cap .step .big{font-size:clamp(32px,9.5vw,46px)}
    .gv-cap .step p{margin-top:10px;font-size:15px}
    /* the caption reads over the planet: a deeper wash at the top of the stage */
    .gv-cap .stage::before{height:42svh;background:linear-gradient(var(--dark) 0%,var(--dark) 34%,rgba(11,11,14,.6) 70%,transparent)}
    .gt-card{display:grid;grid-template-columns:96px 1fr;left:16px;right:16px;bottom:12px}
    .gt-card img{width:96px;height:100%;min-height:96px;aspect-ratio:auto}
    .gtc-body{padding:10px 12px}
    .gtc-body h3{font-size:15px;margin-top:4px}
    .gtc-body .storylink{margin-top:6px;font-size:13px}
    .gt-step{grid-column:1/-1;padding:6px 10px}
    .gt-arrow{width:32px;height:32px}
  }

  /* nav legibility: a soft dark wash behind the transparent bar */
  .nav::before{content:"";position:absolute;left:0;right:0;top:0;height:170%;z-index:-1;pointer-events:none;
    background:linear-gradient(to bottom,rgba(0,0,0,.6) 0%,rgba(0,0,0,.28) 55%,transparent 100%);transition:opacity .35s}
  .nav.solid::before{opacity:0}
  .f-soc{gap:18px;align-items:center}
  .f-soc a{display:grid;place-items:center;width:40px;height:40px;margin:-8px;transition:color .2s}
  .f-soc svg{width:22px;height:22px;fill:currentColor}
  /* lockup is 486x180 with the N spanning x 35-192: the link clips to the N's width and the negative margin
     puts the N's left edge on the page gutter */
  .nav .wordmark{--lh:64px;height:var(--lh);width:calc(var(--lh) * 2.7);margin-left:calc(var(--lh) * -.194);overflow:hidden;flex:none;
    transition:width .5s,height .5s,margin .5s;transition-timing-function:cubic-bezier(.2,.7,.2,1)}
  .lockup{height:100%;width:auto;display:block;flex:none}
  .lockup .lk-word{fill:#fff;transition:opacity .3s,transform .5s cubic-bezier(.2,.7,.2,1)}
  .nav.scrolled .wordmark{--lh:46px;width:calc(var(--lh) * 1.12)}
  .nav.scrolled .lockup .lk-word{opacity:0;transform:translateX(-24px)}
  @media (max-width:720px){ .nav .wordmark{--lh:50px} .nav.scrolled .wordmark{--lh:40px} }
  /* links centred on the page, so they also hold still while the logo peels */
  @media (min-width:961px){ .nav .row{display:grid;grid-template-columns:1fr auto 1fr}
    .nav .wordmark{justify-self:start} .nav .nvright{justify-self:end;margin-left:0} }

  /* phone nav: compact icon controls, one primary button */
  .tkv-open .tko-i{display:none}
  @media (max-width:960px){
    .nav .row{gap:12px;height:64px}
    .nav .wordmark img{height:24px}
    .nvright{gap:2px}
    .nvicon{width:44px;height:44px}
    .navx .tkv-open{width:44px;height:44px;padding:0;border:0;border-radius:50%;align-items:center;justify-content:center}
    .tkv-open .tko-i{display:block}
    .tkv-open .tko-l{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
    .nav .apply{margin-left:8px}
    .nav .apply .pill{padding:0 18px;height:38px;display:inline-flex;align-items:center;font-size:14px;font-weight:600;
      background:#fff;color:#0B0B0E;border-color:#fff}
  }

  /* Spotlight on phones: photo on top fading into the text, fixed-height caption, snapping posters */
  @media (max-width:720px){
    .rows-bfull .crow{min-height:0;padding-top:0;--ch:172px;--pw:150px}
    .rows-bfull .crow > .wrap{order:-2;margin-bottom:12px}
    .rows-bfull .crow + .crow{margin-top:44px;padding-top:32px}
    .rows-bfull .sp-bg{position:relative;order:-1;inset:auto;left:auto;transform:none;width:100%;aspect-ratio:16/10;flex:none}
    .rows-bfull .sp-bg::after{background:linear-gradient(to bottom,transparent 50%,rgba(11,11,14,.7) 80%,var(--dark) 100%)}
    .rows-bfull .sp-in{margin:-44px 0 16px}
    .rows-bfull .sp-copy{min-height:224px}
    .rows-bfull .sp-t{font-size:26px;line-height:1.12}
    .rows-bfull .sp-x{margin-top:10px;font-size:15.5px}
    .rows-bfull .sp-btn{height:42px;margin-top:16px}
    .rows-bfull .cc-t{font-size:13px;line-height:1.2;padding:0 10px 12px}
    .rows-b .crow-strip{scroll-snap-type:x mandatory}
    .rows-b .cc{scroll-snap-align:start}
    /* globe: room after the last beat so its text and card clear out before the next section */
    .gv-cap .steps{padding-bottom:70svh}
  }

  /* ===== globe treatments on phones (?globe=a..e) ===== */
  .gv-a #gt-card,.gv-b #gt-card,.gv-c #gt-card,.gv-d #gt-card,.gv-e #gt-card{display:none!important}
  /* shared story card */
  .gvc{flex:0 0 84%;scroll-snap-align:center;display:grid;grid-template-columns:84px 1fr;gap:12px;align-items:center;padding:10px;border-radius:16px;
    background:rgba(20,20,26,.86);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.1);
    transition:border-color .3s,background .3s}
  .gvc.on{border-color:rgba(255,255,255,.5)}
  .gvc img{width:84px;height:84px;object-fit:cover;border-radius:10px}
  .gvc-loc,.gvl-loc,.gve-loc{margin:0;font-size:12.5px;color:#A9A9B2}
  .gvc-t{margin:3px 0 0;font-size:14.5px;line-height:1.3;color:#fff;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
  .gvc-a,.gvl-a,.gve-a{display:inline-block;margin-top:6px;font-size:13px;font-weight:600;color:#fff}
  .gv-places{margin:12px 0 0!important;font-size:13px!important;line-height:1.6;color:#8A8A93;max-width:none}
  /* A · Stage */
  .gv-a .stage canvas{cursor:default}
  .gva-prog{position:fixed;z-index:7;top:80px;left:20px;display:flex;gap:6px;opacity:0;transition:opacity .4s}
  .gva-prog.on{opacity:1}
  .gva-prog i{width:22px;height:3px;border-radius:2px;background:rgba(255,255,255,.25);transition:background .4s}
  .gva-prog i.on{background:#fff}
  .gv-a.gv-cap .steps .step .card{top:98px}
  .gva-dock{position:fixed;z-index:7;left:0;right:0;bottom:14px;display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;
    padding:0 20px;scrollbar-width:none;opacity:0;transform:translateY(20px);pointer-events:none;transition:opacity .4s,transform .4s}
  .gva-dock::-webkit-scrollbar{display:none}
  .gv-coop .gva-dock{opacity:1;transform:none;pointer-events:auto}
  .gv-a .stage::after{height:30svh}
  /* B · Tabs */
  .gv-b .scrolly{padding:84px 0 56px}
  .gv-b .steps{display:none}
  .gv-b .stage{position:relative;height:min(100vw,58svh)}
  .gv-b .stage::before,.gv-b .stage::after{display:none}
  .gvb{padding:0 20px 8px}
  .gvb-tabs{display:flex;gap:4px;padding:4px;border-radius:999px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.1)}
  .gvb-tabs button{all:unset;flex:1;text-align:center;padding:10px 0;border-radius:999px;font-size:14.5px;font-weight:600;color:#C9C9CF;cursor:pointer;transition:.25s}
  .gvb-tabs button[aria-selected="true"]{background:#fff;color:#0B0B0E}
  .gvb-panes{padding:0 20px}
  .gvb-pane{display:none}
  .gvb-pane.on{display:block;animation:gvin .5s cubic-bezier(.2,.8,.2,1)}
  @keyframes gvin{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
  .gvb-pane .card{opacity:1!important;transform:none!important;max-width:none}
  .gvb-pane .big{font-size:clamp(32px,9vw,44px)}
  .gvb-pane p{font-size:15.5px}
  .gvb-list{margin-top:22px;display:grid;gap:8px}
  .gvl{display:grid;grid-template-columns:64px 1fr;gap:12px;align-items:center;padding:8px;border-radius:14px;background:rgba(255,255,255,.05);border:1px solid transparent;cursor:pointer}
  .gvl.on{border-color:rgba(255,255,255,.45);background:rgba(255,255,255,.09)}
  .gvl img{width:64px;height:64px;object-fit:cover;border-radius:10px}
  .gvl-t{margin:2px 0 0;font-size:14.5px;line-height:1.3;color:#fff}
  .gvl .gvl-a{display:none}
  .gvl.on .gvl-a{display:inline-block}
  /* C · Horizon */
  .gv-c .stage::before{height:56svh;background:linear-gradient(var(--dark) 0%,var(--dark) 30%,rgba(11,11,14,.35) 80%,transparent)}
  .gv-c.gv-cap .step .big{font-size:clamp(38px,11vw,54px)}
  .gv-c.gv-cap .steps .step .card{top:110px}
  .gvc-dock{bottom:18px}
  /* D · Stories */
  .gv-d .steps{display:none}
  .gv-d .stage{position:relative;height:100svh}
  .gv-d .stage::before{height:44svh}
  .gvd{position:absolute;inset:0;z-index:6;pointer-events:none}
  .gvd-bars{position:absolute;top:80px;left:20px;right:20px;display:flex;gap:4px}
  .gvd-bars i{flex:1;height:3px;border-radius:2px;background:rgba(255,255,255,.25);overflow:hidden}
  .gvd-bars b{display:block;height:100%;width:0;background:#fff}
  .gvd-cap{position:absolute;top:100px;left:20px;right:20px;z-index:2;pointer-events:auto;transition:opacity .22s}
  .gvd-cap.swap{opacity:0}
  .gvd-cap .card{opacity:1!important;transform:none!important;max-width:none}
  .gvd-cap .big{font-size:clamp(32px,9.5vw,46px)}
  .gvd-kick{margin:0;font-size:13.5px;color:#A9A9B2}
  .gvd-t{margin:8px 0 0;font-size:clamp(26px,7.4vw,34px);font-weight:300;letter-spacing:-.02em;line-height:1.12}
  .gvd-a{display:inline-flex;align-items:center;height:42px;padding:0 20px;margin-top:16px;border-radius:999px;background:#fff;color:#0B0B0E;font-size:15px;font-weight:600}
  .gvd-prev,.gvd-next{all:unset;position:absolute;top:96px;bottom:0;pointer-events:auto;cursor:pointer}
  .gvd-prev{left:0;width:30%}.gvd-next{right:0;width:70%}
  .gvd-hint{position:absolute;bottom:22px;left:0;right:0;margin:0;text-align:center;font-size:13px;color:#8A8A93}
  /* E · Split */
  .gv-e .stage{position:sticky;top:64px;height:46svh;z-index:6;background:var(--dark)}
  .gv-e .stage::before{display:none}
  .gv-e .stage::after{height:14svh}
  .gv-e .steps{margin-top:0;padding:10svh 20px 30svh}
  .gv-e .step,.gv-e .gve-story{min-height:0;display:block;margin:0 0 34svh;padding:0}
  .gv-e .step .card,.gve{display:block;max-width:none;opacity:.4;transform:none;padding:20px;border-radius:16px;background:#141419;border:1px solid rgba(255,255,255,.08);transition:opacity .4s}
  .gv-e .step.on .card,.gv-e .gve-story.on .gve{opacity:1}
  .gv-e .step .big{font-size:clamp(30px,8.6vw,40px)}
  .gve img{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:10px}
  .gve-b{margin-top:12px}
  .gve-t{margin:4px 0 0;font-size:18px;line-height:1.3;color:#fff}
  /* PATHS */
  .gv-paths #gt-card,.gv-paths .stage .hint{display:none!important}
  .gv-paths .steps{height:170svh;padding:0}
  .gv-paths .steps > *{display:none}
  .gv-paths .stage::before{display:none}
  .pth{position:absolute;z-index:6;left:var(--edge);top:50%;transform:translateY(-50%);width:min(440px,36vw)}
  .pth-h{margin:0 0 22px;font-size:clamp(34px,3.6vw,56px);font-weight:200;letter-spacing:-.035em;line-height:1.04;color:#fff}
  .pth-card{padding:20px 22px 16px;border-radius:18px;background:rgba(20,20,26,.72);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);
    border:1px solid rgba(255,255,255,.1);transition:opacity .26s}
  .pth-card.swap{opacity:0}
  .pth-bars{display:flex;gap:4px;margin:0 0 14px}
  .pth-bars i{flex:1;height:3px;border-radius:2px;background:rgba(255,255,255,.18);overflow:hidden}
  .pth-bars b{display:block;height:100%;width:0;background:#fff}
  .pth-k{margin:0;font-size:13px;color:#A9A9B2}
  .pth-t{margin:4px 0 14px;font-size:clamp(18px,1.5vw,22px);font-weight:500;line-height:1.25;color:#fff}
  .pth-stops{list-style:none;margin:0;padding:0;counter-reset:s}
  .pth-stops li{position:relative;padding:8px 0 8px 26px;opacity:.35;transition:opacity .4s}
  .pth-stops li::before{content:"";position:absolute;left:4px;top:13px;width:9px;height:9px;border-radius:50%;background:#EE5566;
    box-shadow:0 0 0 0 rgba(238,85,102,.5)}
  .pth-stops li.past{opacity:.7}
  .pth-stops li.on{opacity:1}
  .pth-stops li.on::before{box-shadow:0 0 0 5px rgba(238,85,102,.22)}
  .pth-stops b{display:block;font-size:15.5px;font-weight:600;color:#fff}
  .pth-stops span{display:block;margin-top:1px;font-size:13.5px;color:#C9C9CF}
  .pth-foot{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-top:12px;padding-top:12px;border-top:1px solid rgba(255,255,255,.1)}
  .pth-a{font-size:14px;font-weight:600;color:#fff}
  .pth-a[hidden]{visibility:hidden;display:block}
  .pth-nav{display:flex;align-items:center;gap:8px}
  .pth-n{font-size:12.5px;color:#A9A9B2;min-width:34px;text-align:center;font-variant-numeric:tabular-nums}
  .pth-b{all:unset;cursor:pointer;width:34px;height:34px;border-radius:50%;border:1px solid rgba(255,255,255,.3);color:#fff;display:flex;align-items:center;justify-content:center;font-size:14px}
  .pth-b:hover{background:#fff;color:#0B0B0E}
  .pth-b:focus-visible,.pth-a:focus-visible{outline:2px solid #fff;outline-offset:3px}
  @media (max-width:720px){
    .pth{position:absolute;inset:84px 20px 18px;top:84px;transform:none;width:auto;display:flex;flex-direction:column;justify-content:space-between;pointer-events:none}
    .pth > *{pointer-events:auto}
    .pth-h{font-size:clamp(30px,8.6vw,40px);margin:0}
    .pth-card{padding:14px 16px 10px}
    .pth-t{margin-bottom:8px;font-size:16.5px}
    .pth-stops{display:flex;flex-wrap:wrap;gap:4px 14px}
    .pth-stops li{padding:4px 0 4px 16px}
    .pth-stops li::before{left:0;top:10px;width:8px;height:8px}
    .pth-stops b{font-size:14px}
    .pth-stops span{display:none}
    .pth-stops li.on span{display:block;flex-basis:100%}
  }

  /* HORIZON */
  .gv-horizon #gt-card,.gv-horizon .stage .hint{display:none!important}
  .gv-horizon .steps{height:170svh;padding:0}
  .gv-horizon .steps > *{display:none}
  .gv-horizon .stage::before{display:none}
  .gv-horizon .stage::after{height:10svh}
  .gv-horizon:not(.gv-side) .stage::before{display:block;height:46svh;z-index:4;background:linear-gradient(var(--dark) 0%,rgba(11,11,14,.85) 55%,transparent)}
  .hz{position:absolute;z-index:6;top:clamp(96px,13svh,130px);left:var(--edge);right:var(--edge)}
  .hz-head{display:flex;align-items:flex-end;justify-content:space-between;gap:20px}
  .hz.swap .hz-stops{opacity:0;transform:translateY(6px)}
  .hz-stops{transition:opacity .42s ease,transform .42s ease}
  .hz-h{margin:0;font-size:clamp(34px,4vw,64px);font-weight:200;letter-spacing:-.035em;line-height:1.04;color:#fff}
  .hz-nav{display:flex;align-items:center;gap:8px;flex:none;padding-bottom:6px}
  .hz-b{all:unset;cursor:pointer;width:38px;height:38px;border-radius:50%;border:1px solid rgba(255,255,255,.3);color:#fff;display:flex;align-items:center;justify-content:center;font-size:15px;transition:background .2s,color .2s}
  .hz-b:hover{background:#fff;color:#0B0B0E}
  .hz-b:focus-visible,.hz-stops li:focus-visible{outline:2px solid #fff;outline-offset:4px;border-radius:6px}
  .hz-stops{list-style:none;margin:clamp(20px,3svh,30px) 0 0;padding:0;display:grid;grid-template-columns:repeat(var(--n,3),minmax(0,1fr));gap:12px;scrollbar-width:none}
  .hz-stops::-webkit-scrollbar{display:none}
  .hz-stops li{cursor:pointer;opacity:.34;transition:opacity .45s;min-width:0}
  .hz-stops li:hover{opacity:.8}
  .hz-stops li.past{opacity:.62}
  .hz-stops li.on{opacity:1}
  .hz-stops i{display:block;height:3px;border-radius:2px;background:rgba(255,255,255,.22);overflow:hidden}
  .hz-stops b{display:block;height:100%;width:0;background:#fff}
  .hz-stops li.past b{width:100%}
  @keyframes hzfill{from{width:0}to{width:100%}}
  .hz.held .hz-stops b,.hz.off .hz-stops b{animation-play-state:paused!important}
  .hz-p{display:block;margin-top:10px;font-size:clamp(15px,1.25vw,18px);font-weight:600;color:#fff;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .hz-x{display:block;margin-top:2px;font-size:13.5px;line-height:1.35;color:#C9C9CF;opacity:0;transition:opacity .2s}
  .hz-stops li.past .hz-x{opacity:1;transition:opacity .5s .3s}  /* after the map note has faded */
  .hz-call{position:absolute;left:0;top:0;z-index:5;font-size:14px;line-height:1.4;color:#D4D4DA;
    text-shadow:0 1px 10px rgba(0,0,0,.9),0 0 2px rgba(0,0,0,.6);pointer-events:none;opacity:0;transition:opacity .35s}
  .hz-call.on{opacity:1}
  @media (max-width:720px){ .hz-call{font-size:13px} }
  @media (max-width:1100px) and (min-width:721px){ .hz-x{font-size:12.5px} }
  @media (max-width:720px){
    .hz{top:80px;left:20px;right:20px}
    .hz-head{align-items:center}
    .hz-h{font-size:clamp(26px,7.6vw,34px)}
    .hz-nav{padding-bottom:0}
    .hz-b{width:34px;height:34px}
    .hz-stops{display:flex;gap:8px;overflow-x:auto;margin:16px -20px 0;padding:0 20px;scroll-padding-inline:20px}
    .hz-stops li{flex:1 0 calc((100% - 8px * (min(var(--n), 3) - 1)) / min(var(--n), 3))}
    .hz-p{font-size:13.5px;margin-top:8px}
    .hz-x{font-size:12px}
  }
  @media (prefers-reduced-motion: reduce){.hz-stops,.hz-stops li{transition:none}}
  /* SIDE: the horizon idea with content on the left and the globe on the right */
  .gv-side .hz{top:clamp(96px,16svh,200px);right:auto;width:min(440px,36vw)}  /* anchored at the top: controls never move */
  .gv-side .hz-head{flex-direction:column;align-items:flex-start;gap:18px}
  .gv-side .hz-stops{grid-template-columns:1fr;gap:clamp(6px,1.6svh,16px);margin-top:clamp(12px,2.4svh,22px)}
  .gv-side .hz-p{margin-top:8px}
  .gv-side .stage::before{display:block;top:0;bottom:0;right:auto;left:0;width:56%;height:auto;z-index:4;
    background:linear-gradient(to right,rgba(11,11,14,.9) 0%,rgba(11,11,14,.72) 55%,transparent)}
  @media (min-width:721px) and (max-height:820px){ .gv-side .hz-stops li:not(.on) .hz-x{display:none} }  /* short laptops: only the current stop keeps its note */
  @media (max-width:720px){
    .gv-side .hz{top:80px;transform:none;left:20px;right:20px;width:auto}
    .gv-side .hz-head{flex-direction:row;align-items:center}
    .gv-side .stage::before{width:auto;right:0;height:52svh;bottom:auto;background:linear-gradient(var(--dark) 0%,rgba(11,11,14,.85) 60%,transparent)}
  }

  /* GUS */
  .gv-gus #gt-card,.gv-gus .stage .hint{display:none!important}
  .gv-gus .steps{height:460svh;padding:0}
  .gv-gus .steps > *{display:none}
  .gv-gus .stage::before{display:none}
  .gus{position:absolute;z-index:6;left:var(--edge);top:50%;transform:translateY(-50%);max-width:min(560px,40vw);pointer-events:none}
  .gus-l{margin:0;font-size:clamp(34px,4.6vw,72px);font-weight:200;letter-spacing:-.035em;line-height:1.05;color:#fff;
    opacity:0;transform:translateY(18px);transition:opacity .7s cubic-bezier(.2,.8,.2,1),transform .7s cubic-bezier(.2,.8,.2,1)}
  .gus-l.past{opacity:.32;transform:none}
  .gus-l.on{opacity:1;transform:none}
  .gus-l:last-child.on{font-weight:300}
  @media (max-width:720px){
    .gus{top:84px;left:20px;right:20px;max-width:none;transform:none}
    .gus-l{font-size:clamp(28px,8.4vw,38px)}
  }
  @media (prefers-reduced-motion: reduce){.gus-l{transition:none}}
  /* switcher */
  .gvswitch{position:fixed;z-index:300;left:8px;right:8px;bottom:10px;display:flex;justify-content:space-between;gap:2px;padding:5px;border-radius:999px;
    background:rgba(20,20,26,.94);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.15);font-size:12.5px}
  .gvswitch a{padding:8px 10px;border-radius:999px;color:#C9C9CF;white-space:nowrap}
  .gvswitch a.on{background:#fff;color:#0B0B0E;font-weight:600}

  @media (max-width:720px){ #research{padding-top:48px} }

  /* mockup switcher */
  .vswitch{position:fixed;left:16px;bottom:16px;z-index:300;display:flex;gap:4px;padding:6px;border-radius:999px;background:rgba(20,20,26,.92);
    backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.15);font-size:13px}
  .vswitch a{padding:8px 14px;border-radius:999px;color:#C9C9CF;white-space:nowrap}
  .vswitch a.on{background:#fff;color:#0B0B0E;font-weight:600}

  /* co-op rail: full-height panels, no dead space */
  .j-stage{justify-content:flex-start;padding:clamp(84px,11svh,104px) 0 clamp(18px,3svh,30px)}
  .j-head{padding-bottom:clamp(16px,2.6svh,28px)}
  .j-rail{flex:1 1 auto;min-height:0;align-items:stretch;padding-left:max(var(--edge), calc(50vw - (100svh - 280px) * .75))}
  .j-panel{height:auto}
  .j-photo img{height:100%;width:auto}
  .j-stage > .wrap:last-child{flex:none}
  .j-stat{aspect-ratio:3/4;max-width:82vw;background:#141419;border:1px solid rgba(255,255,255,.08);
    align-items:flex-start;justify-content:flex-end;padding:clamp(24px,3vw,44px)}
  .j-stat .g-n{font-size:clamp(72px,13svh,170px)}
  .j-stat .g-l{margin-top:14px;font-size:clamp(16px,1.4vw,20px);color:#C9C9CF}
  .j-outro{aspect-ratio:3/4;max-width:82vw;justify-content:flex-end;padding:clamp(24px,3vw,44px)}
  .j-stage > .wrap:last-child{width:100%;box-sizing:border-box;display:flex;align-items:center;gap:clamp(16px,3vw,32px);margin-top:clamp(16px,2.6svh,28px)}
  .j-bar{flex:1 1 auto;margin:0}
  .j-stage > .wrap:last-child .storylink{flex:none;margin:0 !important;height:44px;padding:0 22px;border:1.5px solid rgba(255,255,255,.6);
    border-radius:999px;font-size:15px;font-weight:600;color:#fff !important;align-items:center}
  .j-stage > .wrap:last-child .storylink:hover{background:#fff;color:#0B0B0E !important;border-color:#fff}

  /* concept 2's globe: flush on this page, dissolving into its neighbors */
  .scrolly{border-radius:0;margin-top:0}
  .gt-card{right:var(--edge)}
  .stage::before,.stage::after{content:"";position:absolute;left:0;right:0;z-index:4;pointer-events:none}
  .stage::before{top:0;height:16svh;background:linear-gradient(var(--dark),transparent)}
  .stage::after{bottom:0;height:24svh;background:linear-gradient(transparent,var(--dark))}

'''

GLOBE_VARIANTS = r'''
/* ============ globe on phones: five treatments to compare (?globe=a..e), "now" is the default ============ */
const GVM = matchMedia("(max-width:720px)").matches;
const GVP = (new URLSearchParams(location.search).get("globe") || "").toLowerCase();
const GV = ["gus", "paths", "horizon", "side"].includes(GVP) ? GVP : (GVM ? (GVP || "a") : null);
const GVS = ["now", "a", "b", "c", "d", "e", "gus", "paths", "horizon", "side"];
if (GV && GVS.includes(GV)) {
  const root = document.documentElement, scrolly = $(".scrolly"), stage = $("#stage");
  root.classList.add("gv-" + GV);
  if (["now", "a", "c"].includes(GV)) root.classList.add("gv-cap");
  const el = (tag, cls, html) => { const n = document.createElement(tag); if (cls) n.className = cls; if (html != null) n.innerHTML = html; return n; };
  const escH = t => String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;");
  const stepEls = $$(".step"), stepName = s => s.dataset.step;
  const LABEL = { campuses: "Campuses", nuin: "N.U.in", coops: "Co‑op" };
  /* drive the camera directly (what a scroll step does, without needing the step) */
  const view = name => {
    const v = VIEWS[name];
    startFly({ lon: v.lon !== undefined ? v.lon : cur.lon, lat: v.lat !== undefined ? v.lat : cur.lat, k: v.k });
    for (const key of LAYER_KEYS) tgt[key] = v[key];
    focus = null; autorotate = !!v.auto; storySel = -1;
    if (v.count && !counted) { counted = true; ignite = 1; igniteT0 = performance.now() + 500; }
  };
  const story = (i, opts = {}) => {
    storySel = i; const st = TOUR_STORIES[i];
    startFly({ lon: st.view.lon, lat: opts.lat !== undefined ? opts.lat : st.view.lat, k: opts.k !== undefined ? opts.k : st.view.k * (window.GV_STORYK || 1) });
    Object.assign(tgt, { coops: .5, campus: .1, nuin: 0, labelC: 0, labelN: 0, spins: 1 });
    autorotate = false;
  };
  const storyCard = (st, i, cls) => `<div class="${cls}" data-i="${i}"><img src="${escH(st.img)}" alt="" loading="lazy">` +
    `<div class="${cls}-b"><p class="${cls}-loc">${escH(st.loc)}</p><p class="${cls}-t">${escH(st.t)}</p>` +
    `<a class="${cls}-a" href="${escH(st.url)}">Read the story<span aria-hidden="true"> →</span></a></div></div>`;
  const relayout = () => { if (typeof resize === "function") resize(); };
  /* phone zoom levels: the whole network stays in frame instead of overflowing the sides */
  if (!["now", "gus", "paths", "horizon", "side"].includes(GV)) { Object.assign(VIEWS.campuses, { lon: -92, lat: 40, k: 1.08 }); Object.assign(VIEWS.nuin, { lon: 6, lat: 46, k: 1.3 }); }
  /* one tracker: the step under mid-screen is current; it alone moves the camera */
  const trackSteps = fn => {
    let curS;
    const f = () => {
      const mid = innerHeight * .5;
      const now = stepEls.find(s => { const r = s.getBoundingClientRect(); return r.top <= mid && r.bottom > mid; }) || null;
      if (now !== curS) { curS = now; fn(now); }
    };
    addEventListener("scroll", () => requestAnimationFrame(f), { passive: true }); f();
  };

  /* phones: no names on the globe (they can't sit cleanly beside a dense cluster); the caption lists them */
  if (!["now", "gus", "paths", "horizon", "side"].includes(GV)) {
    VIEWS.campuses.labelC = 0; VIEWS.nuin.labelN = 0;
    const list = (step, names) => { const c = $(`.step[data-step="${step}"] .card`); if (c) c.append(el("p", "gv-places", names.map(escH).join('<span aria-hidden="true"> \u00b7 </span>'))); };
    const order = ["Boston", "London", "New York City", "Oakland"];
    list("campuses", [...order, ...CAMPUSES.map(c => c[2]).filter(n => !order.includes(n))]);
    list("nuin", NUIN.map(c => c[2]));
  }

  /* A · Stage: pinned; progress above the caption; globe centred between caption and a swipeable story dock */
  if (GV === "a") {
    const prog = el("div", "gva-prog", stepEls.map(() => "<i></i>").join(""));
    const dock = el("div", "gva-dock", TOUR_STORIES.map((st, i) => storyCard(st, i, "gvc")).join(""));
    stage.append(prog, dock);
    const place = () => {
      const H = innerHeight, top = 270, bottom = H - 170;
      window.GLOBE_CY = ((top + bottom) / 2) / H;
      window.GLOBE_R = Math.min((bottom - top) / 2 - 8, innerWidth / 2 - 14) / Math.min(innerWidth, H) / 1.0;
    };
    place(); addEventListener("resize", place);
    window.GV_STORYK = .62;
    const marks = [...prog.children];
    stepIO.disconnect();
    trackSteps(st => {
      const k = stepEls.indexOf(st);
      prog.classList.toggle("on", k >= 0);
      marks.forEach((m, i) => m.classList.toggle("on", i <= k));
      if (!st) return;
      view(st.dataset.step);
      if (st.dataset.step === "coops") { const on = [...dock.children].findIndex(n => n.classList.contains("on")); story(Math.max(0, on)); }
    });
    let t;
    dock.addEventListener("scroll", () => { clearTimeout(t); t = setTimeout(() => {
      const c = [...dock.children], mid = dock.scrollLeft + dock.clientWidth / 2;
      const i = c.reduce((b, n, k) => Math.abs(n.offsetLeft + n.offsetWidth / 2 - mid) < Math.abs(c[b].offsetLeft + c[b].offsetWidth / 2 - mid) ? k : b, 0);
      c.forEach((n, k) => n.classList.toggle("on", k === i));
      if (dock.dataset.touched) story(i);
    }, 120); }, { passive: true });
    dock.addEventListener("touchstart", () => dock.dataset.touched = "1", { passive: true });
    dock.firstElementChild.classList.add("on");
  }

  /* B · Tabs: unpinned; a segmented control over a square globe; co-op tab lists the stories */
  if (GV === "b") {
    window.GV_NOENTRY = true; window.GLOBE_CY = .5; window.GLOBE_R = .38; window.GV_STORYK = .7;
    const wrap = el("div", "gvb");
    const tabs = el("div", "gvb-tabs", stepEls.map((s, i) => `<button role="tab" aria-selected="${i ? "false" : "true"}" data-i="${i}">${LABEL[stepName(s)]}</button>`).join(""));
    tabs.setAttribute("role", "tablist");
    const panes = el("div", "gvb-panes");
    stepEls.forEach((s, i) => {
      const pane = el("div", "gvb-pane" + (i ? "" : " on")); pane.append(s.querySelector(".card"));
      if (stepName(s) === "coops") pane.append(el("div", "gvb-list", TOUR_STORIES.map((st, k) => storyCard(st, k, "gvl")).join("")));
      panes.append(pane);
    });
    scrolly.insertBefore(wrap, stage); wrap.append(tabs); stage.after(panes);
    const go = i => {
      [...tabs.children].forEach((b, k) => b.setAttribute("aria-selected", k === i ? "true" : "false"));
      [...panes.children].forEach((p, k) => p.classList.toggle("on", k === i));
      panes.querySelectorAll(".gvl").forEach(n => n.classList.remove("on"));
      view(stepName(stepEls[i]));
    };
    tabs.addEventListener("click", e => { const b = e.target.closest("button"); if (b) go(+b.dataset.i); });
    panes.addEventListener("click", e => {
      const row = e.target.closest(".gvl"); if (!row || e.target.closest("a")) return;
      panes.querySelectorAll(".gvl").forEach(n => n.classList.toggle("on", n === row));
      story(+row.dataset.i); stage.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
    });
    let first = true;
    new IntersectionObserver(es => { if (es[0].isIntersecting && first) { first = false; go(0); } }, { threshold: .3 }).observe(stage);
    relayout();
  }

  /* C · Horizon: pinned; a huge planet rising from the bottom; scroll turns it continuously */
  if (GV === "c") {
    window.GV_NOENTRY = true;
    const placeC = () => { const H = innerHeight, W = innerWidth, R = W * 1.18; window.GLOBE_R = R / Math.min(W, H); window.GLOBE_CY = (H * .44 + R) / H; };
    placeC(); addEventListener("resize", placeC);
    for (const k in VIEWS) { delete VIEWS[k].lon; delete VIEWS[k].lat; VIEWS[k].k = 1; VIEWS[k].auto = false; }
    stepIO.disconnect();
    trackSteps(st => { if (st) view(st.dataset.step); });
    const dock = el("div", "gva-dock gvc-dock", TOUR_STORIES.map((st, i) => storyCard(st, i, "gvc")).join(""));
    stage.append(dock);
    const steps = $(".steps");
    let pauseAt = null;
    const scrub = () => {
      const r = steps.getBoundingClientRect(); if (r.bottom < 0 || r.top > innerHeight) return;
      if (pauseAt !== null) { if (Math.abs(scrollY - pauseAt) < 60) return; pauseAt = null; storySel = -1; }
      const p = clamp01((innerHeight * .5 - r.top) / Math.max(1, r.height - innerHeight * .7));
      fly = null; tgt.lon = -112 + 135 * p; tgt.lat = 8 - 4 * p; tgt.k = 1;
    };
    addEventListener("scroll", () => requestAnimationFrame(scrub), { passive: true }); scrub();
    let t;
    dock.addEventListener("scroll", () => { clearTimeout(t); t = setTimeout(() => {
      const c = [...dock.children], mid = dock.scrollLeft + dock.clientWidth / 2;
      const i = c.reduce((b, n, k) => Math.abs(n.offsetLeft + n.offsetWidth / 2 - mid) < Math.abs(c[b].offsetLeft + c[b].offsetWidth / 2 - mid) ? k : b, 0);
      c.forEach((n, k) => n.classList.toggle("on", k === i));
      if (dock.dataset.touched) { pauseAt = scrollY; story(i, { k: 1, lat: TOUR_STORIES[i].view.lat - 34 }); }
    }, 120); }, { passive: true });
    dock.addEventListener("touchstart", () => dock.dataset.touched = "1", { passive: true });
    dock.firstElementChild.classList.add("on");
  }

  /* D · Stories: one full-screen panel you tap through, Instagram-stories style */
  if (GV === "d") {
    window.GV_NOENTRY = true; window.GV_STORYK = .7;
    const segs = [...stepEls.map(s => ({ kind: "beat", name: stepName(s), card: s.querySelector(".card") })),
                  ...TOUR_STORIES.map((st, i) => ({ kind: "story", i, st }))];
    const ui = el("div", "gvd");
    ui.innerHTML = `<div class="gvd-bars">${segs.map(() => "<i><b></b></i>").join("")}</div><div class="gvd-cap"></div>` +
      `<button class="gvd-prev" aria-label="Previous"></button><button class="gvd-next" aria-label="Next"></button><p class="gvd-hint">Tap to continue</p>`;
    stage.append(ui);
    const cap = ui.querySelector(".gvd-cap"), bars = [...ui.querySelectorAll(".gvd-bars b")];
    const keep = el("div", "gvd-keep"); keep.hidden = true; ui.append(keep);
    segs.forEach(sg => { if (sg.card) keep.append(sg.card); });
    const place = () => { const H = innerHeight; window.GLOBE_CY = .6; window.GLOBE_R = Math.min(.44, (H * .5) / Math.min(innerWidth, H) / 2.1); };
    place();
    let k = -1, t0 = 0, vis = false, paused = false, DUR = 6500;
    const show = n => {
      k = Math.max(0, Math.min(segs.length - 1, n)); t0 = performance.now();
      bars.forEach((b, i) => b.style.width = i < k ? "100%" : "0%");
      const sg = segs[k];
      cap.classList.add("swap");
      setTimeout(() => {
        [...cap.children].forEach(n => n.classList.contains("card") ? keep.append(n) : n.remove());
        if (sg.kind === "beat") { cap.append(sg.card); view(sg.name); }
        else { cap.innerHTML = `<p class="gvd-kick">Co‑op story · ${escH(sg.st.loc)}</p><p class="gvd-t">${escH(sg.st.t)}</p><a class="gvd-a" href="${escH(sg.st.url)}">Read the story<span aria-hidden="true"> →</span></a>`; story(sg.i); }
        cap.classList.remove("swap");
      }, k === 0 && !cap.children.length ? 0 : 220);
    };
    ui.querySelector(".gvd-next").onclick = () => show(k + 1 >= segs.length ? 0 : k + 1);
    ui.querySelector(".gvd-prev").onclick = () => show(k - 1);
    let holdT;
    ui.addEventListener("pointerdown", () => { holdT = setTimeout(() => paused = true, 250); });
    addEventListener("pointerup", () => { clearTimeout(holdT); if (paused) setTimeout(() => paused = false, 0); });
    new IntersectionObserver(es => { vis = es[0].intersectionRatio > .6; if (vis && k < 0) show(0); }, { threshold: [0, .6, 1] }).observe(stage);
    const loop = now => {
      if (vis && !paused && !document.hidden && k >= 0) {
        if (reduceMotion) { t0 = now; } else {
          const f = Math.min(1, (now - t0) / DUR); bars[k].style.width = (f * 100).toFixed(1) + "%";
          if (f >= 1 && k < segs.length - 1) show(k + 1);
        }
      } else if (k >= 0) t0 = now - (parseFloat(bars[k].style.width) || 0) / 100 * DUR;
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
    relayout();
  }

  /* E · Split: the globe pins in the top half; cards scroll up beneath it and steer it */
  if (GV === "e") {
    window.GV_NOENTRY = true; window.GLOBE_CY = .54; window.GLOBE_R = .44; window.GV_STORYK = .8;
    const steps = $(".steps");
    TOUR_STORIES.forEach((st, i) => steps.append(el("div", "gve-story", storyCard(st, i, "gve"))));
    const cards = [...steps.children];
    const io = new IntersectionObserver(es => es.forEach(e => {
      if (!e.isIntersecting) return;
      cards.forEach(c => c.classList.toggle("on", c === e.target));
      if (e.target.classList.contains("step")) view(e.target.dataset.step);
      else story(+e.target.querySelector(".gve").dataset.i);
    }), { rootMargin: "-58% 0px -30% 0px" });
    cards.forEach(c => io.observe(c));
    relayout();
  }

  /* GUS · one sentence builds as you scroll; each phrase lights its own layer. No flights, no labels. */
  if (GV === "gus") {
    window.GV_NOENTRY = true;
    stepIO.disconnect();
    const LINES = ["One university.", "14 campuses.", "8 places to begin.", "Co‑op on every continent.", "All of it, yours."];
    const box = el("div", "gus", LINES.map(t => `<p class="gus-l">${escH(t)}</p>`).join(""));
    box.setAttribute("aria-live", "polite");
    stage.append(box);
    const ls = [...box.children];
    /* no starting campus: "One university" is the whole globe, then every campus lights at once */
    const place = () => {
      if (innerWidth > 720) { window.GLOBE_CY = undefined; window.GLOBE_R = undefined; return; }
      const H = innerHeight, top = 84 + box.offsetHeight + 24, bottom = H - 30;
      window.GLOBE_CY = ((top + bottom) / 2) / H; window.GLOBE_R = Math.max(.2, Math.min((bottom - top) / 2 - 6, innerWidth / 2 - 18) / Math.min(innerWidth, H));
    };
    const STATES = [
      { campus: 0, nuin: 0, coops: 0, spins: 0, k: 1 },
      { campus: 1, nuin: 0, coops: 0, spins: 0, k: 1 },
      { campus: 1, nuin: 1, coops: 0, spins: 0, k: 1 },
      { campus: 1, nuin: 1, coops: 1, spins: 0, k: .96 },
      { campus: 1, nuin: 1, coops: 1, spins: 0, k: .9 },
    ];
    cur.lon = tgt.lon = -42; cur.lat = tgt.lat = 30; cur.k = tgt.k = 1;
    Object.assign(cur, STATES[0]); Object.assign(tgt, STATES[0]); cur.labelC = tgt.labelC = 0; cur.labelN = tgt.labelN = 0;
    fly = null; autorotate = true;
    let beat = -1;
    const TH = [0, .17, .36, .55, .74];
    const upd = () => {
      const r = scrolly.getBoundingClientRect(), p = clamp01(-r.top / Math.max(1, r.height - innerHeight));
      let b = 0; TH.forEach((t, i) => { if (p >= t) b = i; });
      if (b === beat) return; beat = b;
      ls.forEach((l, i) => { l.classList.toggle("on", i === b); l.classList.toggle("past", i < b); });
      const st = STATES[b]; for (const k of ["campus", "nuin", "coops", "spins"]) tgt[k] = st[k]; tgt.k = st.k;
      labelOff();
    };
    const labelOff = () => { tgt.labelC = 0; tgt.labelN = 0; };
    /* a slow, steady turn (the engine's idle spin is quickened by a third) */
    const drift = () => { if (!fly) tgt.lon -= .02; requestAnimationFrame(drift); };
    if (!reduceMotion) requestAnimationFrame(drift);
    addEventListener("scroll", () => requestAnimationFrame(upd), { passive: true });
    addEventListener("resize", () => { place(); relayout(); });
    requestAnimationFrame(() => { place(); relayout(); upd(); });
  }

  /* PATHS · real journeys across the network, drawn one stop at a time (no connecting lines) */
  if (GV === "paths") {
    window.GV_NOENTRY = true; window.GLOBE_LOCK = true;
    stepIO.disconnect();
    window.PATH_ARCS = [];
    const P = __PATHS__;
    const ui = el("div", "pth");
    ui.innerHTML = `<h2 class="pth-h">Where a Northeastern path can go.</h2>` +
      `<div class="pth-card" aria-live="polite"><div class="pth-bars" aria-hidden="true">${P.map(() => "<i><b></b></i>").join("")}</div><p class="pth-k"></p><p class="pth-t"></p><ol class="pth-stops"></ol>` +
      `<div class="pth-foot"><a class="pth-a" href="#">Read the story<span aria-hidden="true"> →</span></a>` +
      `<div class="pth-nav"><button class="pth-b" data-d="-1" aria-label="Previous path">←</button><span class="pth-n"></span>` +
      `<button class="pth-b" data-d="1" aria-label="Next path">→</button></div></div></div>`;
    stage.append(ui);
    const card = ui.querySelector(".pth-card"), list = ui.querySelector(".pth-stops"), link = ui.querySelector(".pth-a");
    /* the planet is a quiet backdrop; the path's stops are the only bright points */
    const BACK = { campus: .1, nuin: .08, coops: .1, labelC: 0, labelN: 0, spins: 1 };
    Object.assign(cur, BACK); Object.assign(tgt, BACK);
    autorotate = false; fly = null;
    $("#globe").addEventListener("click", e => e.stopImmediatePropagation(), true);
    const place = () => {
      if (innerWidth > 720) { window.GLOBE_CY = undefined; window.GLOBE_R = undefined; return; }
      const H = innerHeight, top = 84 + ui.querySelector(".pth-h").offsetHeight + 12, bottom = H - card.offsetHeight - 22;
      window.GLOBE_CY = ((top + bottom) / 2) / H;
      window.GLOBE_R = Math.max(.2, Math.min((bottom - top) / 2 - 4, innerWidth / 2 - 18) / Math.min(innerWidth, H));
    };
    let pi = 0, si = -1, t0 = 0, vis = false;
    const DWELL = 1500, HOLD = 2000;
    const bars = [...ui.querySelectorAll(".pth-bars b")];
    const total = i => P[i].stops.length * DWELL + HOLD - DWELL;
    let pathT0 = 0;
    const stopAt = j => {
      si = j; t0 = performance.now();
      const st = P[pi].stops[j];
      if (j > 0) window.PATH_ARCS.push({ a: P[pi].stops[j - 1].ll, b: st.ll, t0 });
      window.PATH_LABEL = { ll: st.ll, text: st.place };
      STORY_PINS.push(st.ll); storySel = j;
      startFly({ lon: st.ll[1], lat: st.ll[0] - 6, k: P[pi].k || 1.2 });
      [...list.children].forEach((li, k) => { li.classList.toggle("on", k === j); li.classList.toggle("past", k < j); });
    };
    const showPath = i => {
      pi = (i + P.length) % P.length; si = -1; STORY_PINS.length = 0; window.PATH_ARCS = []; window.PATH_LABEL = null;
      pathT0 = performance.now();
      bars.forEach((b, k) => b.style.width = k < pi ? "100%" : "0%");
      const pth = P[pi];
      card.classList.add("swap");
      setTimeout(() => {
        card.querySelector(".pth-k").textContent = pth.kind;
        card.querySelector(".pth-t").textContent = pth.title;
        list.innerHTML = pth.stops.map(st => `<li><b>${escH(st.place)}</b><span>${escH(st.note)}</span></li>`).join("");
        link.hidden = !pth.url; if (pth.url) link.href = pth.url;
        ui.querySelector(".pth-n").textContent = `${pi + 1} / ${P.length}`;
        card.classList.remove("swap");
        place(); relayout();
        stopAt(0);
      }, reduceMotion ? 0 : 260);
    };
    ui.querySelectorAll(".pth-b").forEach(b => b.addEventListener("click", () => showPath(pi + +b.dataset.d)));
    new IntersectionObserver(es => { vis = es[0].intersectionRatio > .5; }, { threshold: [0, .5, 1] }).observe(stage);
    const loop = now => {
      if (vis && !document.hidden && si >= 0 && !reduceMotion) {
        bars[pi].style.width = Math.min(100, (now - pathT0) / total(pi) * 100).toFixed(1) + "%";
        const last = si >= P[pi].stops.length - 1;
        if (!last && now - t0 > DWELL) stopAt(si + 1);
        else if (last && now - t0 > HOLD) showPath(pi + 1);
      } else if (si >= 0) { const d = now - (loop.last || now); t0 += d; pathT0 += d; }
      loop.last = now;
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
    addEventListener("resize", () => { place(); relayout(); });
    showPath(0);
  }

  /* HORIZON / SIDE · a path's stops sit in a row like stories, dim until reached; each fills as the globe
     flies to it (co-op tour camera). Tap a stop to jump; hover or focus pauses; the globe is locked. */
  if (GV === "horizon" || GV === "side") {
    const SIDE = GV === "side";
    if (SIDE) root.classList.add("gv-horizon");
    window.GV_NOENTRY = true; window.GLOBE_LOCK = true; window.GLOBE_ALL = !SIDE; window.PATH_LIFT = SIDE ? .8 : .45;
    window.FLY_NODIP = true; window.FLY_SLOW = 1.35;  /* no zoom bounce, calmer flights */
    stepIO.disconnect();
    window.PATH_ARCS = [];
    const P = __PATHS__;
    const ui = el("div", "hz");
    ui.innerHTML = `<div class="hz-head"><h2 class="hz-h">Where a Northeastern path can go.</h2>` +
      `<div class="hz-nav"><button class="hz-b" data-d="-1" aria-label="Previous path">←</button><button class="hz-b" data-d="1" aria-label="Next path">→</button></div></div>` +
      `<ol class="hz-stops" aria-live="polite"></ol>`;
    stage.append(ui);
    const list = ui.querySelector(".hz-stops");
    const BACK = { campus: .1, nuin: .08, coops: .1, labelC: 0, labelN: 0, spins: 1 };
    Object.assign(cur, BACK); Object.assign(tgt, BACK);
    autorotate = false; fly = null;
    $("#globe").addEventListener("click", e => e.stopImmediatePropagation(), true);
    let crest = { R: 1000, cap: 400 };
    const place = () => {
      const W = innerWidth, H = innerHeight, phone = W <= 720;
      const below = ui.getBoundingClientRect().bottom - stage.getBoundingClientRect().top;
      if (SIDE) {
        if (!phone) { window.GLOBE_CY = undefined; window.GLOBE_R = undefined; return; }
        const top = below + 18, bottom = H - 24;
        window.GLOBE_CY = ((top + bottom) / 2) / H; window.GLOBE_R = Math.max(.2, Math.min((bottom - top) / 2 - 4, W / 2 - 18) / Math.min(W, H));
        return;
      }
      const R = phone ? W * 1.15 : Math.max(W * .62, H * 1.0);
      const topOfDisk = Math.min(H - 120, Math.max(below + 30, H * (phone ? .5 : .46)));
      window.GLOBE_R = R / Math.min(W, H); window.GLOBE_CY = (topOfDisk + R) / H;
      crest = { R, cap: H - topOfDisk };
    };
    let pi = 0, si = -1, t0 = 0, vis = false, held = false;
    const DWELL = 2400, HOLD = 3000;
    const angDeg = (a, b) => { const p1 = a[0] * RAD, p2 = b[0] * RAD, dl = (b[1] - a[1]) * RAD;
      return Math.acos(Math.max(-1, Math.min(1, Math.sin(p1) * Math.sin(p2) + Math.cos(p1) * Math.cos(p2) * Math.cos(dl)))) / RAD; };
    const zoomFor = (pth, j) => {
      const nb = pth.stops[j - 1] || pth.stops[j + 1]; if (!nb) return SIDE ? 1.95 : 1.45;
      const d = angDeg(nb.ll, pth.stops[j].ll), near = d < 6 ? 1 : d < 25 ? .45 : 0;
      return SIDE ? 1.75 + near * .35 : 1.3 + near * .3;  /* pulled back from the co-op tour's camera: less sweep per move */
    };
    const dur = j => j >= P[pi].stops.length - 1 ? HOLD : DWELL;
    const paint = j => [...list.children].forEach((li, k) => {
      li.classList.toggle("on", k === j); li.classList.toggle("past", k < j);
      li.setAttribute("aria-current", k === j ? "step" : "false");
      const b = li.querySelector("b");
      b.style.animation = k === j ? "none" : "";  /* the bar starts filling when the camera lands */
    });
    const bar = j => {
      const b = list.children[j] && list.children[j].querySelector("b");
      if (!b || reduceMotion) return;
      b.style.animation = "none"; void b.offsetWidth; b.style.animation = `hzfill ${dur(j)}ms linear forwards`;
    };
    const flyTo = (pth, j) => {
      const st = pth.stops[j], kk = zoomFor(pth, j);
      /* horizon: the stop sits a third of the way down the visible cap at this zoom */
      const tilt = SIDE ? 1 : Math.asin(Math.max(-.95, Math.min(.95, (crest.R - crest.cap * .38) / (crest.R * kk)))) / RAD;
      startFly({ lon: st.ll[1], lat: st.ll[0] - tilt, k: kk });
    };
    /* the current stop's note sits on the map under its city label; when the camera moves on,
       it fades out there and fades in under that city in the row (row notes show for past stops only) */
    const call = el("div", "hz-call"); call.setAttribute("aria-hidden", "true"); stage.append(call);
    let callWait = false, landed = false;  /* dwell time counts from landing, so slower flights don't eat it */
    const callOff = () => { call.classList.remove("on"); callWait = false; };
    const callPos = () => {
      const b = window.PATH_LABEL_BOX;
      if (!b) { call.style.visibility = "hidden"; return; }
      const g = $("#globe").getBoundingClientRect(), sr = stage.getBoundingClientRect();
      const x = g.left - sr.left + b.x, room = innerWidth - (g.left + b.x) - 16;
      call.style.visibility = "";
      call.style.maxWidth = Math.max(140, Math.min(260, room)) + "px";
      call.style.transform = `translate(${Math.round(x)}px,${Math.round(g.top - sr.top + b.y + b.h + 2)}px)`;
    };
    const callTick = () => {
      if (!landed && si >= 0 && !fly && !swapping) { landed = true; t0 = performance.now(); bar(si); }
      if (callWait && !fly && !swapping && window.PATH_LABEL_BOX) { call.classList.add("on"); callWait = false; }
      if (call.classList.contains("on") || callWait) callPos();
      requestAnimationFrame(callTick);
    };
    requestAnimationFrame(callTick);
    const stopAt = (j, jump, noFly) => {
      callOff();
      si = j; t0 = performance.now();
      const pth = P[pi], st = pth.stops[j];
      call.textContent = st.note; callWait = true; landed = false;
      if (jump) {  /* rebuild the trail up to this stop, already drawn */
        STORY_PINS.length = 0; window.PATH_ARCS = [];
        for (let k = 0; k < j; k++) { STORY_PINS.push(pth.stops[k].ll); if (k) window.PATH_ARCS.push({ a: pth.stops[k - 1].ll, b: pth.stops[k].ll, t0: -1e9 }); }
      }
      if (j > 0) window.PATH_ARCS.push({ a: pth.stops[j - 1].ll, b: st.ll, t0 });
      /* a new stop's pin and label wait for the line to arrive (the arc draws in 900ms) */
      const arrive = j > 0 && !jump && !reduceMotion ? t0 + 900 : 0;
      window.PATH_LABEL = { ll: st.ll, text: st.place, at: arrive };
      clearTimeout(stopAt.pinT);
      const pin = () => { STORY_PINS.push(st.ll); storySel = j; };
      if (arrive) { const key = pi + ":" + j; stopAt.pinT = setTimeout(() => { if (pi + ":" + si === key) pin(); }, 900); } else pin();
      if (!noFly) flyTo(pth, j);
      paint(j);
      const li = list.children[j];
      if (li && list.scrollWidth > list.clientWidth) list.scrollTo({ left: li.offsetLeft - 20, behavior: reduceMotion ? "auto" : "smooth" });
    };
    /* path hand-off: the old trail fades while the camera is already flying to the next first stop,
       the stop row crossfades, and the new trail fades in where the camera lands */
    let swapT = 0, swapping = false, pending = 0;
    const fill = pth => {
      list.style.setProperty("--n", pth.stops.length);
      list.innerHTML = pth.stops.map((st, k) => `<li tabindex="0" data-k="${k}"><i aria-hidden="true"><b></b></i>` +
        `<span class="hz-p">${escH(st.place)}</span><span class="hz-x">${escH(st.note)}</span></li>`).join("");
      list.scrollLeft = 0;
    };
    const showPath = (i, instant) => {
      const ni = (i + P.length) % P.length;
      pending = ni;
      clearTimeout(swapT);
      const land = () => {
        swapping = false; pi = ni; si = -1;
        STORY_PINS.length = 0; window.PATH_ARCS = []; window.PATH_LABEL = null; window.PATH_FADE = 1; tgt.spins = 1;
        fill(P[pi]); place(); relayout();
        ui.classList.remove("swap");
        stopAt(0, false, !instant);
      };
      if (instant || reduceMotion) { land(); if (!instant) flyTo(P[ni], 0); return; }
      swapping = true;
      ui.classList.add("swap"); window.PATH_LABEL = null; tgt.spins = 0; callOff();
      flyTo(P[ni], 0);
      const f0 = performance.now();
      const fade = now => { if (!swapping) return; window.PATH_FADE = Math.max(0, 1 - (now - f0) / 420); if (window.PATH_FADE > 0) requestAnimationFrame(fade); };
      requestAnimationFrame(fade);
      swapT = setTimeout(land, 520);
    };
    ui.querySelectorAll(".hz-b").forEach(b => b.addEventListener("click", () => showPath((swapping ? pending : pi) + +b.dataset.d)));
    list.addEventListener("click", e => { const li = e.target.closest("li"); if (li) stopAt(+li.dataset.k, true); });
    list.addEventListener("keydown", e => { if ((e.key === "Enter" || e.key === " ") && e.target.matches("li")) { e.preventDefault(); stopAt(+e.target.dataset.k, true); } });
    /* hover or keyboard focus on the content holds the path (and its bar) in place */
    const hold = on => { held = on; ui.classList.toggle("held", on); };
    if (matchMedia("(hover: hover)").matches) { ui.addEventListener("pointerenter", () => hold(true)); ui.addEventListener("pointerleave", () => hold(false)); }
    ui.addEventListener("focusin", () => hold(true)); ui.addEventListener("focusout", e => { if (!ui.contains(e.relatedTarget)) hold(false); });
    new IntersectionObserver(es => { vis = es[0].intersectionRatio > .5; ui.classList.toggle("off", !vis); }, { threshold: [0, .5, 1] }).observe(stage);
    const loop = now => {
      if (vis && !held && !document.hidden && si >= 0 && !reduceMotion) {
        const last = si >= P[pi].stops.length - 1;
        if (!swapping && landed && now - t0 > dur(si)) { if (!last) stopAt(si + 1); else showPath(pi + 1); }
      } else if (si >= 0) { t0 += now - (loop.last || now); }
      loop.last = now;
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
    let rt; addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(() => { place(); relayout(); if (si >= 0 && !swapping) stopAt(si, true); }, 150); });
    showPath(0, true);
  }

  /* treatment switcher (only when ?globe= is in the URL) */
  if (new URLSearchParams(location.search).has("globe")) {
    const NAMES = { now: "Now", a: "A · Stage", b: "B · Tabs", c: "C · Horizon", d: "D · Stories", e: "E · Split", gus: "GUS", paths: "Paths", horizon: "Horizon", side: "Side" };
    const bar = el("nav", "gvswitch", GVS.map(x => `<a href="?globe=${x}#campuses" class="${x === GV ? "on" : ""}">${x === GV ? NAMES[x] : (x === "now" ? "Now" : x.toUpperCase())}</a>`).join(""));
    bar.setAttribute("aria-label", "Globe treatments"); document.body.append(bar);
  }
}
'''
GLOBE_PINCH = r'''/* globe: a two-finger pinch zooms the planet, never the page (page zoom elsewhere is untouched) */
{
  const cv = $("#globe");
  if (cv) {
    ["gesturestart", "gesturechange", "gestureend"].forEach(ev => cv.addEventListener(ev, e => e.preventDefault()));
    let pinch = null;
    const dist = t => Math.hypot(t[0].clientX - t[1].clientX, t[0].clientY - t[1].clientY);
    cv.addEventListener("touchstart", e => {
      if (e.touches.length === 2) { e.preventDefault(); pinch = { d: dist(e.touches), k: cur.k }; dragging = false; }
    }, { passive: false });
    cv.addEventListener("touchmove", e => {
      if (!pinch || e.touches.length !== 2) return;
      e.preventDefault();
      fly = null; dragging = false;
      if (innerWidth > 720 && !window.GLOBE_LOCK) cur.k = tgt.k = Math.max(.8, Math.min(4, pinch.k * dist(e.touches) / pinch.d));
    }, { passive: false });
    cv.addEventListener("touchend", e => { if (e.touches.length < 2) pinch = null; });
  }
}
'''
NEW_JS = r'''{
/* ============ concept-7 ============ */
/* globe on phones: exactly one current step (the one at mid-screen) owns the caption slot;
   steps above it are "past" so they leave upward; the co-op card only shows on its step */
{
  const steps = $$(".step"), coopsStep = $('.step[data-step="coops"]');
  let curStep = null;
  const upd = () => {
    if (innerWidth > 720 || !document.documentElement.classList.contains("gv-cap")) { steps.forEach(s => s.classList.remove("cur", "past")); return; }
    const mid = innerHeight * .5;
    const pinned = $(".scrolly").getBoundingClientRect().top <= 70;
    const now = pinned ? (steps.find(s => { const r = s.getBoundingClientRect(); return r.top <= mid && r.bottom > mid; }) || null) : null;
    if (now !== curStep) {
      curStep = now;
      const k = steps.indexOf(now), lastPast = steps.every(s => s.getBoundingClientRect().bottom <= mid);
      steps.forEach((s, i) => { s.classList.toggle("cur", s === now); s.classList.toggle("past", lastPast || (k >= 0 && i < k)); });
    }
    document.documentElement.classList.toggle("gv-coop", curStep === coopsStep);
    if (document.documentElement.classList.contains("gv-now")) { const want = curStep === coopsStep; if (gtCard.hidden === want) gtCard.hidden = !want; }
  };
  addEventListener("scroll", () => requestAnimationFrame(upd), { passive: true });
  addEventListener("resize", upd); upd();
}
/* phone menu: each section mirrors its desktop dropdown (overview pills, then labeled link groups) */
{
  const MAP = { "tsub-0": "mp-admissions", "tsub-2": "mp-experiential", "tsub-3": "mp-research", "tsub-4": "mp-global", "tsub-6": "mp-more" };
  const ah = a => `<a href="${a.getAttribute("href")}">${a.textContent.trim()}</a>`;
  for (const [sub, panel] of Object.entries(MAP)) {
    const sEl = document.getElementById(sub), pEl = document.getElementById(panel);
    if (!sEl || !pEl) continue;
    const ov = [...pEl.querySelectorAll(".mp-lead .storylink")];
    const secs = [...pEl.querySelectorAll(".mp-col")].map(c => ({ h: (c.querySelector(".mp-h") || {}).textContent || "", links: [...c.querySelectorAll(".mp-links a")] }))
      .filter(x => x.links.length && x.h.trim() !== "Campuses");
    sEl.innerHTML = (ov.length ? `<div class="tkv-ov">${ov.map(ah).join("")}</div>` : "") +
      secs.map(x => `<div class="tkv-sec">${x.h ? `<p class="tkv-h">${x.h}</p>` : ""}${x.links.map(ah).join("")}</div>`).join("");
  }
}
/* nav: hovering anything in the bar that isn't a dropdown trigger (Global Entrepreneurship, AI,
   logo, search, Apply) closes an open panel; moving down into the panel itself keeps it open */
$$("#nav .row a, #nav .row .nvicon, #nav .row .tkv-open").forEach(el => el.addEventListener("mouseenter", () => {
  clearTimeout(mHoverT); mCloseAll();
}));
const esc = s => String(s).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");
const FEATS = __FEATS__;

/* ============ billboard ============ */
const hx = $(".hx"), hxIn = $("#hxIn"), layers = $$(".hl"), lnBtns = $$(".ln");
let cur = 0, elapsed = 0, hxVisible = true, hoverShows = false;
const vidOf = i => layers[i].querySelector("video");
const playI = i => { const v = vidOf(i); if (v && !reduceMotion) v.play().catch(() => {}); };
function fillHero(f) {
  $("#hxTitle").textContent = f.h;
  $("#hxSyn").textContent = f.syn;
  const cta = $("#hxCta");
  cta.hidden = !f.cta;
  if (f.cta) { cta.href = f.cta.href; $("#hxCtaL").textContent = f.cta.label; }
  $("#hxEps").innerHTML = f.eps.slice(0, 3).map(e =>
    `<a class="ep" href="${esc(e.u)}"><img src="${esc(e.img)}" alt="" loading="lazy"><span>${esc(e.t)}</span></a>`).join("");
}
/* one title size for every feature: the largest at which the longest title fits the copy column,
   so switching features never changes the type size and Entrepreneurship never meets the panel */
function fitHeroTitle() {
  const t = $("#hxTitle"), keep = t.textContent;
  t.style.fontSize = ""; t.style.minHeight = "0";
  let fs = parseFloat(getComputedStyle(t).fontSize);
  const fits = () => t.scrollWidth <= t.clientWidth && t.offsetHeight <= fs * .98 * 2 + 2;
  for (const f of FEATS) {
    t.textContent = f.h;
    while (fs > 32 && !fits()) { fs -= 2; t.style.fontSize = fs + "px"; }
  }
  t.textContent = keep; t.style.minHeight = "";
}
function selectF(i) {
  elapsed = 0;
  lnBtns.forEach((b, k) => { b.setAttribute("aria-pressed", k === i ? "true" : "false"); b.style.setProperty("--pb", 0); });
  if (i === cur) return;
  const from = cur; cur = i;
  layers[from].classList.remove("on"); layers[i].classList.add("on");
  playI(i);
  setTimeout(() => { const v = vidOf(from); if (v && from !== cur) v.pause(); }, 1000);
  hxIn.classList.add("swap");
  setTimeout(() => { fillHero(FEATS[i]); hxIn.classList.remove("swap"); }, reduceMotion ? 0 : 350);
}
lnBtns.forEach(b => b.addEventListener("click", () => selectF(+b.dataset.i)));
/* auto-rotate every 12s; the loader fills per frame on the active card */
const ROTATE_MS = 12000;
$("#hxShows").addEventListener("pointerenter", () => hoverShows = true);
$("#hxShows").addEventListener("pointerleave", () => hoverShows = false);
if (!reduceMotion) {
  let lastT = 0;
  const tick = now => {
    const dt = lastT ? Math.min(100, now - lastT) : 0; lastT = now;
    if (hxVisible && !hoverShows && !document.hidden && scrollY < innerHeight * .3) {
      elapsed += dt;
      lnBtns[cur].style.setProperty("--pb", Math.min(1, elapsed / ROTATE_MS).toFixed(4));
      if (elapsed >= ROTATE_MS) selectF((cur + 1) % FEATS.length);
    }
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}
new IntersectionObserver(es => es.forEach(e => {
  hxVisible = e.isIntersecting;
  const v = vidOf(cur);
  if (v) { if (hxVisible) playI(cur); else v.pause(); }
})).observe(hx);
/* card titles wrap by word; shrink only when a single word is wider than the card */
/* every card label shares one size: the largest at which the longest single word fits */
function fitTitles() {
  const ts = $$(".ln-t");
  ts.forEach(t => t.style.fontSize = "");
  let fs = parseFloat(getComputedStyle(ts[0]).fontSize);
  for (const t of ts) { t.style.fontSize = fs + "px"; while (fs > 11 && t.scrollWidth > t.clientWidth) { fs -= .5; t.style.fontSize = fs + "px"; } }
  ts.forEach(t => t.style.fontSize = fs + "px");
}
const shows = $("#hxShows");
const layout = () => { fitTitles(); fitHeroTitle(); hx.style.setProperty("--shh", shows.offsetHeight + "px"); };
addEventListener("resize", layout);
document.fonts.ready.then(layout); layout();
/* leaving the billboard: the film eases back and the copy lets go */
if (!reduceMotion) {
  const media = $("#hxMedia");
  addEventListener("scroll", () => requestAnimationFrame(() => {
    const p = clamp01(scrollY / innerHeight);
    media.style.transform = `translateY(${(p * 90).toFixed(1)}px) scale(${(1 + p * .06).toFixed(4)})`;
    hxIn.style.opacity = (1 - p * 1.5).toFixed(3);
  }), { passive: true });
}
fillHero(FEATS[0]);
playI(0);

/* ============ closer: photos crossfade every 5s while it's on screen ============ */
{
  const admit = $(".admit"), shots = $$(".admit .bg img");
  let k = 0, vis = false, started = false;
  /* each photo is fully decoded before it fades in, so nothing decodes mid-fade */
  const ready = img => { if (!img.src) img.src = img.dataset.src; return img.decode().catch(() => {}); };
  /* the upcoming photo is decoded and kept painted at near-zero opacity, so its fade-in never stalls */
  const prime = img => ready(img).then(() => img.classList.add("pre"));
  const step = async () => {
    const next = shots[(k + 1) % shots.length];
    await prime(next);
    if (vis && !document.hidden) {
      shots[k].classList.remove("on"); k = (k + 1) % shots.length;
      next.classList.remove("pre"); next.classList.add("on");
      setTimeout(() => prime(shots[(k + 1) % shots.length]), 2000);
    }
    setTimeout(step, 5000);
  };
  new IntersectionObserver(es => es.forEach(e => {
    vis = e.isIntersecting;
    if (vis && !started) { started = true; ready(shots[0]); prime(shots[1]); if (!reduceMotion) setTimeout(step, 5000); }
  }), { rootMargin: "800px 0px" }).observe(admit);
}

/* ============ rows: a featured card, then portrait posters ============ */
const card = c => `<a class="cc" href="${esc(c.u)}">` +
  `<img src="${esc(c.img)}" alt="" loading="lazy"><span class="cc-t">${esc(c.t)}</span></a>`;
function mountRow(sec, items) {
  const strip = sec.querySelector(".crow-strip"), prev = sec.querySelector(".pad.prev"), next = sec.querySelector(".pad.next");
  strip.innerHTML = items.map(card).join("");
  const sync = () => {
    prev.disabled = strip.scrollLeft < 4;
    next.disabled = strip.scrollLeft + strip.clientWidth >= strip.scrollWidth - 4;
  };
  const by = d => strip.scrollBy({ left: d * (strip.clientWidth - 2 * parseFloat(getComputedStyle(strip).paddingLeft)), behavior: reduceMotion ? "auto" : "smooth" });
  prev.onclick = () => by(-1); next.onclick = () => by(1);
  strip.addEventListener("scroll", () => requestAnimationFrame(sync), { passive: true });
  addEventListener("resize", sync);
  sec.hidden = false;
  sync();
}

/* ============ the reel: each card loops its own clip; the strip drifts rightward ============ */
if ($(".reel")) {
  const reel = $(".reel"), track = $("#reelTrack"), GAP = 16;
  const vio = new IntersectionObserver(es => es.forEach(e => {
    const v = e.target;
    if (!e.isIntersecting) { v.pause(); return; }
    if (!v.src) {
      v.addEventListener("loadedmetadata", () => { v.currentTime = +v.dataset.s; }, { once: true });
      v.src = v.dataset.src;
    }
    if (!reduceMotion) v.play().catch(() => {});
  }), { rootMargin: "300px" });
  track.querySelectorAll("video").forEach(v => {
    v.addEventListener("timeupdate", () => { if (v.currentTime >= +v.dataset.e) v.currentTime = +v.dataset.s; });
    v.addEventListener("ended", () => { v.currentTime = +v.dataset.s; v.play().catch(() => {}); });
    vio.observe(v);
  });
  /* the strip is a real scroller (swipe, trackpad, mouse drag) holding three copies of the clips.
     It drifts rightward on its own; after the user scrolls it re-centres by exactly one copy, but only
     once they've let go, so a fling in either direction never gets interrupted. */
  let pos, last = 0, on = false, holdUntil = 0, drag = null, touching = false, userAt = 0;
  const N = track.children.length;
  for (let r = 0; r < 2; r++) [...track.children].slice(0, N).forEach(c => {
    const k = c.cloneNode(true), v = k.querySelector("video");
    v.addEventListener("timeupdate", () => { if (v.currentTime >= +v.dataset.e) v.currentTime = +v.dataset.s; });
    vio.observe(v); track.append(k);
  });
  const SET = () => track.children[N].offsetLeft - track.children[0].offsetLeft;
  const recentre = () => {
    const w = SET();
    if (reel.scrollLeft < w * .5) reel.scrollLeft += w; else if (reel.scrollLeft > w * 1.5) reel.scrollLeft -= w;
    pos = reel.scrollLeft;
  };
  reel.scrollLeft = SET(); pos = reel.scrollLeft;
  new IntersectionObserver(es => { on = es[0].isIntersecting; }).observe(reel);
  const hold = () => { holdUntil = performance.now() + 1800; };
  reel.addEventListener("touchstart", () => { touching = true; hold(); }, { passive: true });
  reel.addEventListener("touchend", () => { touching = false; hold(); }, { passive: true });
  reel.addEventListener("wheel", hold, { passive: true });
  reel.addEventListener("scroll", () => { if (Math.abs(reel.scrollLeft - pos) > 2) { userAt = performance.now(); hold(); } pos = reel.scrollLeft; }, { passive: true });
  reel.addEventListener("pointerdown", e => { if (e.pointerType !== "mouse") return; drag = { x: e.clientX, s: reel.scrollLeft }; reel.classList.add("drag"); hold(); });
  addEventListener("pointermove", e => { if (!drag) return; reel.scrollLeft = drag.s - (e.clientX - drag.x); pos = reel.scrollLeft; hold(); });
  addEventListener("pointerup", () => { if (drag) { drag = null; reel.classList.remove("drag"); } });
  const step = now => {
    const dt = last ? Math.min(50, now - last) : 0; last = now;
    const idle = !touching && !drag && now - userAt > 300;
    if (on && idle) {
      if (!reduceMotion && now > holdUntil) { pos -= dt * .045; reel.scrollLeft = pos; pos = reel.scrollLeft; }
      recentre();
    }
    requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

/* live NGN: news posts only (no "Photos:" galleries), no story repeated across rows */
const FALLBACK = FEATS.flatMap(f => f.eps).slice(0, 10).map(e => ({ t: e.t, u: e.u, img: e.img, wide: e.img }));
const RV = (new URLSearchParams(location.search).get("rows") || "").toLowerCase();
const RVK = ["a", "b", "b2", "b3", "c"].includes(RV) ? RV : "current";
document.documentElement.classList.add("rows-" + RVK, ...({ b: ["rows-b", "rows-bfull"], b2: ["rows-b"], b3: ["rows-b", "rows-bimg"] }[RV] || []));
const fmtDate = d => d ? new Date(d).toLocaleDateString("en-US", { month: "long", day: "numeric" }) : "";
const ARROW = `__ARROW__`, CHEV = `__CHEV__`;
(async () => {
  const API = "https://news.northeastern.edu/wp-json/wp/v2/newspost?per_page=24&_embed=wp:featuredmedia&_fields=link,title,excerpt,date,_links,_embedded&";
  const rows = $$(".crow[data-q]");
  const data = await Promise.all(rows.map(sec => fetch(API + sec.dataset.q).then(r => r.ok ? r.json() : []).catch(() => [])));
  const shown = new Set(), tmp = document.createElement("div"), topics = [];
  const text = html => { tmp.innerHTML = html; return tmp.textContent.trim(); };
  rows.forEach((sec, k) => {
    const items = data[k].filter(p => !/^Photos:/i.test(p.title.rendered) && !shown.has(p.link)).map(p => {
      const m = p._embedded && p._embedded["wp:featuredmedia"] && p._embedded["wp:featuredmedia"][0];
      if (!m) return null;
      const sz = (m.media_details && m.media_details.sizes) || {};
      const img = (sz["newspack-article-block-portrait-medium"] || sz.large || sz.medium_large || m).source_url;
      if (!img) return null;
      return { t: text(p.title.rendered), u: p.link, img, wide: (sz.large || sz.medium_large || m).source_url, full: m.source_url,
               x: text((p.excerpt && p.excerpt.rendered) || ""), d: p.date };
    }).filter(Boolean).slice(0, 14);
    const label = sec.getAttribute("aria-label");
    if (items.length < 4) { if (!k) topics.push({ sec, label, items: FALLBACK }); return; }
    items.forEach(c => shown.add(c.u));
    topics.push({ sec, label, items });
  });
  if (["b", "b2", "b3"].includes(RV)) topics.forEach(spotlight);
  else if (RV === "c") coverflow(topics);
  else { topics.forEach(tp => mountRow(tp.sec, tp.items)); if (RV === "a") previews(topics); }
})();

/* A · Preview: hovering a poster grows a floating story card out of it (it overlays, nothing reflows) */
function previews(topics) {
  if (!matchMedia("(hover: hover)").matches) return;
  const pv = document.createElement("a");
  pv.className = "pv";
  pv.innerHTML = `<img class="pv-img" alt=""><span class="pv-b"><span class="pv-meta"></span><span class="pv-t"></span><span class="pv-x"></span><span class="pv-cta">Read story ${ARROW}</span></span>`;
  document.body.appendChild(pv);
  let showT, hideT;
  const hide = () => { clearTimeout(showT); pv.classList.remove("on"); };
  const show = (el, it, label) => {
    pv.href = it.u;
    pv.querySelector(".pv-img").src = it.wide || it.img;
    pv.querySelector(".pv-meta").textContent = label;
    pv.querySelector(".pv-t").textContent = it.t;
    pv.querySelector(".pv-x").textContent = it.x || "";
    const r = el.getBoundingClientRect(), vw = document.documentElement.clientWidth;
    const pad = parseFloat(getComputedStyle(el.parentElement).paddingLeft);
    const w = Math.min(460, Math.max(r.width * 1.9, 340));
    pv.style.transition = "none"; pv.classList.remove("on"); pv.style.width = w + "px"; pv.style.transform = "none";
    const h = pv.offsetHeight;
    const left = Math.max(pad, Math.min(vw - pad - w, r.left + r.width / 2 - w / 2));
    const top = Math.max(scrollY + 84, r.top + scrollY + r.height / 2 - h / 2);
    pv.style.left = left + "px"; pv.style.top = top + "px";
    const dx = r.left + r.width / 2 - (left + w / 2), dy = r.top + scrollY + r.height / 2 - (top + h / 2);
    pv.style.transform = `translate(${dx}px, ${dy}px) scale(${r.width / w}, ${r.height / h})`;
    void pv.offsetWidth;
    pv.style.transition = ""; pv.classList.add("on"); pv.style.transform = "none";
  };
  topics.forEach(tp => tp.sec.querySelectorAll(".cc").forEach((el, i) => {
    el.addEventListener("pointerenter", () => { clearTimeout(hideT); clearTimeout(showT); showT = setTimeout(() => show(el, tp.items[i], tp.label), 380); });
    el.addEventListener("pointerleave", () => { clearTimeout(showT); hideT = setTimeout(hide, 160); });
  }));
  pv.addEventListener("pointerenter", () => clearTimeout(hideT));
  pv.addEventListener("pointerleave", () => { hideT = setTimeout(hide, 160); });
  addEventListener("scroll", hide, { passive: true });
}

/* B · Spotlight: each topic is a stage; the focused story fills it, the posters run along the bottom */
function spotlight(tp) {
  const sec = tp.sec, items = tp.items;
  sec.classList.add("sp");
  sec.insertAdjacentHTML("afterbegin", `<div class="sp-bg" aria-hidden="true"><i></i><i></i></div>` +
    `<div class="sp-in"><div class="sp-copy" aria-live="polite"><p class="sp-t"></p><p class="sp-x"></p>` +
    `<a class="storylink sp-btn" href="#">Read story</a></div><div class="sp-fig" aria-hidden="true"><img alt=""><img alt=""></div></div>`);
  mountRow(sec, items);
  const bgs = sec.querySelectorAll(".sp-bg i"), figs = sec.querySelectorAll(".sp-fig img"), copy = sec.querySelector(".sp-copy"), cards = [...sec.querySelectorAll(".cc")];
  let cur = -1, layer = 0, t;
  const set = i => {
    if (i === cur) return;
    cards.forEach(c => c.style.setProperty("--pb", 0));
    cur = i; const it = items[i];
    layer ^= 1;
    const stage = bgs[layer], prev = bgs[layer ^ 1], pic = new Image();
    pic.src = it.full || it.wide || it.img;
    pic.decode().catch(() => {}).then(() => {
      if (items[cur] !== it) return;
      stage.style.backgroundImage = `url('${pic.src}')`; stage.classList.add("on"); prev.classList.remove("on");
    });
    /* the framed photo: full-size original, swapped in only once decoded */
    const f = figs[layer], other = figs[layer ^ 1], want = it.full || it.wide || it.img;
    f.src = want;
    f.decode().catch(() => {}).then(() => { if (items[cur] === it) { f.classList.add("on"); other.classList.remove("on"); } });
    cards.forEach((c, k) => c.classList.toggle("on", k === i));
    copy.classList.add("swap");
    setTimeout(() => {
      copy.querySelector(".sp-t").textContent = it.t;
      copy.querySelector(".sp-x").textContent = it.x || "";
      copy.querySelector(".sp-btn").href = it.u;
      copy.classList.remove("swap");
    }, reduceMotion ? 0 : 220);
  };
  /* a focused poster never sits half under a paddle: the row slides it into the clear lane,
     and hover is ignored briefly so the poster that slides under the pointer doesn't steal focus */
  const strip = sec.querySelector(".crow-strip");
  let quietUntil = 0;
  const reveal = c => {
    const s = strip.getBoundingClientRect(), pl = parseFloat(getComputedStyle(strip).paddingLeft), r = c.getBoundingClientRect();
    const d = r.right > s.right - pl ? r.right - (s.right - pl) : r.left < s.left + pl ? r.left - (s.left + pl) : 0;
    if (Math.abs(d) < 2) return;
    quietUntil = performance.now() + 700;
    strip.scrollBy({ left: d, behavior: reduceMotion ? "auto" : "smooth" });
  };
  const canHover = matchMedia("(hover: hover)").matches;
  cards.forEach((c, k) => {
    if (canHover) c.addEventListener("pointerenter", () => {
      clearTimeout(t);
      if (performance.now() < quietUntil) return;
      t = setTimeout(() => { set(k); reveal(c); }, 140);
    });
    c.addEventListener("click", e => { e.preventDefault(); set(k); reveal(c); hold(); });
    c.addEventListener("focus", () => { set(k); reveal(c); });
  });
  set(0);
  /* auto-advance every 8s with a loader on the focused poster; pauses on hover, after a touch,
     off screen, in a hidden tab, and under reduced motion; loops after the first ten stories */
  cards.forEach(c => c.insertAdjacentHTML("beforeend", '<i class="cc-pb" aria-hidden="true"></i>'));
  const SPOT_MS = 8000, LOOP = Math.min(cards.length, 10);
  let elapsedS = 0, lastS = 0, visS = false, hoverS = false, holdS = 0;
  function hold() { holdS = performance.now() + 6000; elapsedS = 0; }
  new IntersectionObserver(es => { visS = es[0].isIntersecting; }, { threshold: .45 }).observe(sec);
  if (canHover) { sec.addEventListener("pointerenter", () => hoverS = true); sec.addEventListener("pointerleave", () => { hoverS = false; elapsedS = 0; }); }
  strip.addEventListener("touchstart", hold, { passive: true });
  if (!reduceMotion) {
    const tickS = now => {
      const dt = lastS ? Math.min(100, now - lastS) : 0; lastS = now;
      if (visS && !hoverS && !document.hidden && now > holdS) {
        elapsedS += dt;
        cards[cur].style.setProperty("--pb", Math.min(1, elapsedS / SPOT_MS).toFixed(4));
        if (elapsedS >= SPOT_MS) {
          cards[cur].style.setProperty("--pb", 0); elapsedS = 0;
          const n = (cur + 1) % LOOP; set(n); reveal(cards[n]);
        }
      }
      requestAnimationFrame(tickS);
    };
    requestAnimationFrame(tickS);
  }
}

/* C · Coverflow: one module, topic tabs over a 3D coverflow; the centered story carries the details */
function coverflow(topics) {
  topics.forEach(tp => tp.sec.hidden = true);
  const host = document.createElement("div");
  host.className = "cf";
  host.innerHTML = `<div class="wrap cf-tabs" role="tablist" aria-label="Topics">` +
    topics.map((tp, n) => `<button role="tab" class="cf-tab" aria-selected="${n ? "false" : "true"}" data-i="${n}">${esc(tp.label)}</button>`).join("") +
    `</div><div class="cf-stage" tabindex="0" aria-label="Stories, use the arrow keys to browse"></div>` +
    `<div class="wrap cf-info"><button class="cf-nav prev" aria-label="Previous story">${CHEV}</button>` +
    `<div class="cf-copy" aria-live="polite"><p class="cf-meta"></p><p class="cf-t"></p><p class="cf-x"></p><a class="hx-btn cf-btn" href="#">Read story ${ARROW}</a></div>` +
    `<button class="cf-nav next" aria-label="Next story">${CHEV}</button></div>`;
  $(".rows").appendChild(host);
  const stage = host.querySelector(".cf-stage"), copy = host.querySelector(".cf-copy");
  let items = [], cards = [], i = 0, topic = 0;
  const layout = () => {
    const cw = cards[0] ? cards[0].offsetWidth : 240;
    cards.forEach((c, k) => {
      const o = k - i, a = Math.abs(o), sg = Math.sign(o);
      const x = o === 0 ? 0 : sg * (cw * .74 + (a - 1) * cw * .3);
      c.style.transform = `translateX(${x.toFixed(1)}px) translateZ(${a ? -150 - a * 30 : 0}px) rotateY(${a ? -sg * 50 : 0}deg)`;
      c.style.zIndex = 100 - a; c.style.opacity = a > 5 ? 0 : 1;
      c.classList.toggle("on", !o); c.tabIndex = o ? -1 : 0;
    });
  };
  const info = () => {
    const it = items[i]; copy.classList.add("swap");
    setTimeout(() => {
      copy.querySelector(".cf-meta").textContent = topics[topic].label;
      copy.querySelector(".cf-t").textContent = it.t;
      copy.querySelector(".cf-x").textContent = it.x || "";
      copy.querySelector(".cf-btn").href = it.u;
      copy.classList.remove("swap");
    }, reduceMotion ? 0 : 180);
  };
  const go = n => { const m = Math.max(0, Math.min(items.length - 1, n)); if (m === i && cards.length) return; i = m; layout(); info(); };
  const load = n => {
    topic = n; items = topics[n].items; i = 0;
    stage.innerHTML = items.map(it => `<a class="cf-card" href="${esc(it.u)}"><img src="${esc(it.img)}" alt="" loading="lazy"></a>`).join("");
    cards = [...stage.children];
    cards.forEach((c, k) => c.addEventListener("click", e => { if (k !== i) { e.preventDefault(); go(k); } }));
    layout(); info();
  };
  host.querySelectorAll(".cf-tab").forEach(b => b.addEventListener("click", () => {
    host.querySelectorAll(".cf-tab").forEach(x => x.setAttribute("aria-selected", x === b ? "true" : "false"));
    stage.classList.add("swap");
    setTimeout(() => { load(+b.dataset.i); stage.classList.remove("swap"); }, reduceMotion ? 0 : 220);
  }));
  host.querySelector(".cf-nav.prev").onclick = () => go(i - 1);
  host.querySelector(".cf-nav.next").onclick = () => go(i + 1);
  stage.addEventListener("keydown", e => { if (e.key === "ArrowRight") go(i + 1); if (e.key === "ArrowLeft") go(i - 1); });
  let x0 = null;
  stage.addEventListener("pointerdown", e => { x0 = e.clientX; });
  stage.addEventListener("pointerup", e => { if (x0 !== null && Math.abs(e.clientX - x0) > 40) go(i + (e.clientX < x0 ? 1 : -1)); x0 = null; });
  addEventListener("resize", layout);
  load(0);
}

/* switcher for the row mockups (only when ?rows= is in the URL) */
if (new URLSearchParams(location.search).has("rows")) {
  const bar = document.createElement("nav");
  bar.className = "vswitch"; bar.setAttribute("aria-label", "Story row mockups");
  bar.innerHTML = [["current", "Current"], ["a", "A · Preview"], ["b", "B · Spotlight"], ["b2", "B2 · Quiet"], ["b3", "B3 · Framed"], ["c", "C · Coverflow"]]
    .map(([k, l]) => `<a href="?rows=${k}" class="${RVK === k ? "on" : ""}">${l}</a>`).join("");
  document.body.appendChild(bar);
}
}
'''
# real cross-campus paths, each from an NGN story (researched 2026-10-06); one illustrative path, labeled
BOS, OAK, LON, NYC, POR, BUR = [42.34, -71.09], [37.78, -122.18], [51.51, -0.07], [40.77, -73.98], [43.66, -70.26], [42.48, -71.2]
# ponytail: places beyond the campus constants above; illustrative paths, any hop under 1,000 km fails the build
MIA, NAH, SEA, VAN, SV, ARL, CLT, TOR = [25.76, -80.19], [42.42, -70.91], [47.61, -122.33], [49.28, -123.12], [37.34, -121.89], [38.88, -77.11], [35.23, -80.84], [43.65, -79.38]
KGL, SYD, DEL = [-1.94, 30.06], [-33.87, 151.21], [28.61, 77.21]
MEX, SJU, SIN, BOC, REY, NBO, SAO, TYO, SEL, TLL = [19.43, -99.13], [18.47, -66.11], [1.35, 103.82], [9.34, -82.24], [64.15, -21.94], [-1.29, 36.82], [-23.55, -46.63], [35.68, 139.69], [37.57, 126.98], [59.44, 24.75]
PATHS = [
 {"kind": "Student", "title": "Start abroad, then Boston",
  "url": NGN + "/2026/01/16/nu-in-students-boston-transition/",
  "stops": [{"place": "Greece", "note": "First semester through N.U.in", "ll": [40.64, 22.94]},
            {"place": "Boston", "note": "Spring semester on the Boston campus", "ll": BOS}]},
 {"kind": "One possible path", "k": 1.0, "url": "", "title": "Engineering, by way of Mexico City",
  "stops": [{"place": "Boston", "note": "Civil engineering on the Boston campus", "ll": BOS},
            {"place": "Mexico City", "note": "A co‑op designing water systems", "ll": MEX},
            {"place": "Miami", "note": "A master's on the Miami campus", "ll": MIA}]},
 {"kind": "One possible path", "k": 1.0, "url": "", "title": "Three seas",
  "stops": [{"place": "Nahant", "note": "A semester of marine biology at the Marine Science Center", "ll": NAH},
            {"place": "Panama", "note": "Coral reef surveys in Bocas del Toro", "ll": BOC},
            {"place": "Seattle", "note": "Kelp forest research in the Pacific Northwest", "ll": SEA}]},
 {"kind": "Research", "title": "One institute, three campuses", "k": 1.05,
  "url": NGN + "/2026/05/04/network-science-institute-global-presence/",
  "stops": [{"place": "Boston", "note": "The Network Science Institute, which maps how ideas and diseases spread", "ll": BOS},
            {"place": "London", "note": "A second hub on the London campus, with European partners", "ll": LON},
            {"place": "Portland, Maine", "note": "A third at the Roux Institute, working with companies in Maine", "ll": POR}]},
 {"kind": "One possible path", "k": 1.0, "url": "", "title": "Across the Pacific",
  "stops": [{"place": "Vancouver", "note": "Computer science on the Vancouver campus", "ll": VAN},
            {"place": "Singapore", "note": "A co‑op with a fintech startup", "ll": SIN},
            {"place": "Silicon Valley", "note": "A final semester on the Silicon Valley campus", "ll": SV}]},
 {"kind": "One possible path", "k": 1.0, "url": "", "title": "Diagnostics for clinics",
  "stops": [{"place": "Boston", "note": "A bioengineering lab designing low‑cost blood tests", "ll": BOS},
            {"place": "Kigali", "note": "Field trials with rural clinics in Rwanda", "ll": KGL},
            {"place": "London", "note": "Results published with London campus colleagues", "ll": LON}]},
 {"kind": "One possible path", "k": 1.0, "url": "", "title": "Environmental health",
  "stops": [{"place": "Boston", "note": "A Boston lab studying chemical exposure during pregnancy", "ll": BOS},
            {"place": "Puerto Rico", "note": "Tap water samples from homes across Puerto Rico", "ll": SJU},
            {"place": "Arlington", "note": "Findings briefed to federal environmental agencies", "ll": ARL}]},
 {"kind": "One possible path", "k": 1.0, "url": "", "title": "Arctic to equator",
  "stops": [{"place": "Portland, Maine", "note": "Models of warming in the Gulf of Maine, built at the Roux Institute", "ll": POR},
            {"place": "Reykjavík", "note": "Sensors tracking glacier melt, placed with Icelandic scientists", "ll": REY},
            {"place": "London", "note": "The data turned into climate policy on the London campus", "ll": LON},
            {"place": "Nairobi", "note": "Drought forecasts built with Kenyan farmers and researchers", "ll": NBO}]},
 {"kind": "Student", "title": "London, Oakland, then Boston", "k": .95,
  "url": NGN + "/2024/09/12/enrollment-statistics-2024/",
  "stops": [{"place": "London", "note": "One semester on the London campus", "ll": LON},
            {"place": "Oakland", "note": "One semester on the Oakland campus", "ll": OAK},
            {"place": "Boston", "note": "The rest of the degree", "ll": BOS}]},
 {"kind": "One possible path", "k": 1.0, "url": "", "title": "Wildfire data",
  "stops": [{"place": "Seattle", "note": "A faculty lab using AI to predict how wildfires spread", "ll": SEA},
            {"place": "Sydney", "note": "Fire‑season data shared by Australian researchers", "ll": SYD},
            {"place": "Oakland", "note": "Students join the project from the Oakland campus", "ll": OAK}]},
 {"kind": "One possible path", "k": 1.0, "url": "", "title": "A startup on three continents",
  "stops": [{"place": "Oakland", "note": "A water‑filter startup that began in an Oakland class", "ll": OAK},
            {"place": "São Paulo", "note": "First customers in São Paulo", "ll": SAO},
            {"place": "London", "note": "Investors on the London campus", "ll": LON}]},
 {"kind": "One possible path", "k": 1.0, "url": "", "title": "Robotics in Asia",
  "stops": [{"place": "Charlotte", "note": "A data science master's on the Charlotte campus", "ll": CLT},
            {"place": "Tokyo", "note": "A co‑op writing robotics software", "ll": TYO},
            {"place": "Seoul", "note": "Summer research on robots that help older adults at home", "ll": SEL},
            {"place": "Toronto", "note": "A semester on the Toronto campus", "ll": TOR}]},
 {"kind": "One possible path", "k": 1.0, "url": "", "title": "Heat in cities",
  "stops": [{"place": "New York City", "note": "A professor studying urban heat at the New York campus", "ll": NYC},
            {"place": "Delhi", "note": "Rooftop sensors measuring heat in Delhi neighborhoods", "ll": DEL},
            {"place": "Miami", "note": "Cooling plans tested with the city of Miami", "ll": MIA}]},
 {"kind": "One possible path", "k": 1.0, "url": "", "title": "Security without borders",
  "stops": [{"place": "Arlington", "note": "Research on securing power grids, outside Washington, D.C.", "ll": ARL},
            {"place": "Tallinn", "note": "Cyber defense exercises with NATO partners in Estonia", "ll": TLL},
            {"place": "London", "note": "A cybersecurity master's on the London campus", "ll": LON}]},
]
def _km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, a + b)
    return 6371 * 2 * math.asin(math.sqrt(math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2))
for _p in PATHS:
    for _a, _b in zip(_p["stops"], _p["stops"][1:]):
        assert _km(_a["ll"], _b["ll"]) >= 1000, (_p["title"], _a["place"], _b["place"])
GLOBE_VARIANTS = GLOBE_VARIANTS.replace("__PATHS__", json.dumps(PATHS, ensure_ascii=False))
NEW_JS = NEW_JS.replace("__ARROW__", g["ICON_ARROW"]).replace("__CHEV__", CHEV)
NEW_JS = NEW_JS.replace("__FEATS__", json.dumps(FEATS, ensure_ascii=False).replace("</", "<\\/"))

# the co-op rail is cut (2026-10-06); research stays
_j0 = sheet_mk.index('<section class="journey"'); _j1 = sheet_mk.index("</section>", _j0) + len("</section>")
sheet_mk = sheet_mk[:_j0] + sheet_mk[_j1:]
# the live site's lockup (www.northeastern.edu header); the wordmark peels away to the N on scroll only (dropdowns also set .solid)
_w0 = header_mk.index('<a class="wordmark"'); _w1 = header_mk.index("</a>", _w0)
header_mk = (header_mk[:_w0] + '<a class="wordmark" href="#" aria-label="Northeastern University home">'
             + open(os.path.join(os.path.dirname(__file__), "nu-lockup.svg")).read() + header_mk[_w1:])
page = (head + nav_css + overlay_css + c2_css + NEW_CSS + "\n" + tailcss
        + "</style>\n\n<body>\n\n"
        + header_mk + HERO + "<main>\n" + ROWS + globe_mk + sheet_mk + admit_mk + "\n</main>\n" + footer_mk + "\n"
        + lenis_js + "\n<script>\n" + land + "\n" + coops + "\n" + helpers + c2_js + GLOBE_PINCH + GLOBE_VARIANTS + NEW_JS
        + "\n" + tail_js + "/* ============ boot ============ */\nconst navScrolled = () => nav.classList.toggle(\"scrolled\", scrollY > 60);\naddEventListener(\"scroll\", navScrolled, { passive: true });\nnavScrolled();\nnav.classList.toggle(\"solid\", scrollY > 60);\nresize();\nrequestAnimationFrame(frame);\n</script>\n")

GERUNDS = [
 ("Developing cameras for Apple products", "Camera development for Apple products"),
 ("Harvesting oysters on Maine's Nonesuch River", "Oyster harvests on Maine's Nonesuch River"),
 ("Harvesting oysters on Maine’s Nonesuch River", "Oyster harvests on Maine’s Nonesuch River"),
 ("Learning how global negotiation really works", "How global negotiation really works"),
 ("Learning that happens on the job, in the field, everywhere.", "Education on the job, in the field, everywhere."),
 (">Walking the future<", ">Robots on campus<"),
]
for a, b in GERUNDS:
    assert a in page or "’" in a, a
    page = page.replace(a, b)
assert page.count("<header") == 1 and page.count("<footer>") == 1
assert HERO.count('class="ln"') == 5 and page.count('class="crow"') == 5 and page.count('class="vidcard"') == 0 and 'class="journey"' not in page
assert 'class="voices-c"' not in page and "SMEET" not in page
for tok in ['id="srch"', 'concept10-rev" content="56"', 'id="stage"', "TOUR_STORIES", "stepIO", 'class="admit"', 'id="xrow"', "lineIO"]:
    assert tok in page, tok
for gone in ['data-panel="mp-academics"', "Learning by doing", "Shaping responsible", "Developing cameras", "Harvesting oysters", "Learning how global", "Walking the future", 'href="#">Entrepreneurship', "Global &amp; Campuses", "Ideas into ventures", "kbs ", "Only at Northeastern", "tabs-1", "placement", "one way in", "one part.", 'data-step="outro"', "and counting", "Continue browsing", "hx-meta", "opens doors", "Now showing", "hxSound", "makeGlobe", "qtrack", 'class="hero"', 'class="grain"', "—"]:
    assert gone not in page, gone
for out in OUT:
    open(out, "w").write(page)
print("built", len(page), "bytes ->", OUT[0])

# concept 11: the same page as a standalone concept, with the image Spotlight as its story rows
p11 = page
for x, y in (('<meta name="concept10-rev" content="56">', '<meta name="concept11-rev" content="45">'),
             ('const RV = (new URLSearchParams(location.search).get("rows") || "").toLowerCase();',
              'const RV = (new URLSearchParams(location.search).get("rows") || "b").toLowerCase();')):
    assert p11.count(x) == 1, x
    p11 = p11.replace(x, y)
os.makedirs(os.path.join(ROOT, "concept-11"), exist_ok=True)
open(os.path.join(ROOT, "concept-11/index.html"), "w").write(p11)
print("built", len(p11), "bytes -> concept-11/index.html")

# concept 12: concept 11 with the Horizon globe as the only treatment (no switcher, since ?globe= is absent)
p12 = p11
for x, y in (('<meta name="concept11-rev" content="45">', '<meta name="concept12-rev" content="15">'),
             ('get("globe") || "").toLowerCase();', 'get("globe") || "horizon").toLowerCase();')):
    assert p12.count(x) == 1, x
    p12 = p12.replace(x, y)
os.makedirs(os.path.join(ROOT, "concept-12"), exist_ok=True)
open(os.path.join(ROOT, "concept-12/index.html"), "w").write(p12)
print("built", len(p12), "bytes -> concept-12/index.html")
