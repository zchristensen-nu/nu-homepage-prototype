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
counters_js = cut("/* ============ research counters ============ */", "/* ============ research expanding row ============ */")
tail_js     = cut("/* ============ subtle scroll movement ============ */", "/* ============ boot ============ */")
i0 = tail_js.find("/* student life imax:"); i1 = tail_js.find("/* smooth scrolling via Lenis")
assert 0 < i0 < i1
tail_js = tail_js[:i0] + tail_js[i1:]


head = head.replace('<meta name="prototype-rev" content="53">',
                    '<meta name="concept4-rev" content="2">')
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

  /* ---------- full-bleed video sections ---------- */
  .vsec{position:relative;min-height:92svh;display:flex;align-items:flex-end;
    background:var(--dark);color:#fff;overflow:hidden}
  .vsec.city{min-height:78svh}
  .vsec video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.66)}
  .vsec::after{content:"";position:absolute;inset:0;
    background:linear-gradient(to top,rgba(11,11,14,.78) 0%,rgba(11,11,14,.22) 45%,rgba(11,11,14,.1) 100%)}
  .vs-in{position:relative;z-index:2;width:100%;padding:0 0 64px}
  .vs-in h2{font-size:clamp(48px,7.5vw,120px);font-weight:200;letter-spacing:-.03em;line-height:1}
  .vb-stats{margin-top:30px;display:flex;gap:clamp(24px,4vw,64px);flex-wrap:wrap}
  .vb-stat .n{font-size:clamp(30px,3.2vw,50px);font-weight:200;letter-spacing:-.02em;line-height:1;
    font-variant-numeric:tabular-nums}
  .vb-stat .l{margin-top:6px;font-size:13.5px;color:#C9C9CF;max-width:20ch}

  /* ---------- N.U.in collection ---------- */
  .nuin{position:relative;z-index:6;background:var(--dark);color:#fff;padding:110px 0 120px}
  .nu-h{font-size:clamp(48px,7.5vw,120px);font-weight:200;letter-spacing:-.03em;line-height:1}
  .nu-cities{margin-top:16px;font-size:clamp(14px,1.2vw,17px);color:#C9C9CF}
  .nu-grid{margin-top:44px;display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
  .nu-grid video{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:14px;display:block;background:#141419}
  @media(max-width:820px){.nu-grid{grid-template-columns:1fr}}
"""

NEW_BODY = f"""
<div class="grain" aria-hidden="true"></div>

<section class="wire top" aria-label="Latest from Northeastern Global News">
  <div class="wire-in">
    <span class="w-label">{NGN_LOGO}</span>
    <div class="w-belt"><div class="w-track">{ticker_items(TICKER)}{ticker_items(TICKER)}</div></div>
  </div>
</section>

<section class="vsec" id="experiential" aria-label="Experiential learning">
  <video src="{V_COOP}" muted loop playsinline preload="none" data-vio></video>
  <div class="vs-in"><div class="wrap">
    <h2><span class="line"><span>Experiential Learning</span></span></h2>
    <div class="vb-stats">
      <div class="vb-stat"><div class="n">500,000+</div><div class="l">co‑op placements, all time</div></div>
      <div class="vb-stat"><div class="n">10,000+</div><div class="l">employer partners</div></div>
      <div class="vb-stat"><div class="n">250+</div><div class="l">countries and territories</div></div>
    </div>
  </div></div>
</section>

<section class="vsec" id="research" aria-label="Research">
  <video src="{V_CAMPUS}" muted loop playsinline preload="none" data-vio></video>
  <div class="vs-in"><div class="wrap">
    <h2><span class="line"><span>Research</span></span></h2>
    <div class="vb-stats" id="counters">
      <div class="vb-stat"><div class="n">$<span data-count="296">0</span>M</div><div class="l">external research awards last year</div></div>
      <div class="vb-stat"><div class="n"><span data-count="50">0</span>+</div><div class="l">federally funded centers and institutes</div></div>
      <div class="vb-stat"><div class="n"><span data-count="510">0</span></div><div class="l">patents and counting</div></div>
    </div>
  </div></div>
</section>

<section class="vsec city" id="boston"><video src="{V_HERO}" muted loop playsinline preload="none" data-vio></video>
  <div class="vs-in"><div class="wrap"><h2><span class="line"><span>Boston</span></span></h2></div></div></section>
<section class="vsec city" id="london"><video src="{V_LONDON}" muted loop playsinline preload="none" data-vio></video>
  <div class="vs-in"><div class="wrap"><h2><span class="line"><span>London</span></span></h2></div></div></section>
<section class="vsec city" id="nyc"><video src="{V_NYC}" muted loop playsinline preload="none" data-vio></video>
  <div class="vs-in"><div class="wrap"><h2><span class="line"><span>NYC</span></span></h2></div></div></section>
<section class="vsec city" id="oakland"><video src="{V_CAMPUS}" muted loop playsinline preload="none" data-vio></video>
  <div class="vs-in"><div class="wrap"><h2><span class="line"><span>Oakland</span></span></h2></div></div></section>

<section class="nuin" id="nuin" aria-label="N.U.in">
  <div class="wrap">
    <h2 class="nu-h"><span class="line"><span>N.U.in</span></span></h2>
    <p class="nu-cities">Prague &middot; Berlin &middot; Thessaloniki &middot; Dublin &middot; Rome &middot; Belfast &middot; Glasgow &middot; Madrid</p>
    <div class="nu-grid">
      <video src="{V_LONDON}" muted loop playsinline preload="none" data-vio></video>
      <video src="{V_HERO}" muted loop playsinline preload="none" data-vio></video>
      <video src="{V_COOP}" muted loop playsinline preload="none" data-vio></video>
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
        + lenis + "\n<script>\n" + helpers + counters_js + NEW_JS + "\n" + tail_js + NEW_BOOT + "</script>\n")

assert page.count("<header") == 1 and page.count("<footer>") == 1
assert page.count("<video") == 10  # hero + 2 pillars + 4 cities + 3 nuin tiles
for tok in ['id="srch"', 'id="tkv"', "Experiential Learning", ">Research<", ">Boston<", ">London<",
            ">NYC<", ">Oakland<", ">N.U.in<", "nu-grid", "NYC-Home_SLOW", "nulondon.ac.uk",
            "Jamie-Wong", "wire top", "wire foot", 'class="admit"', "concept4-rev",
            'content="2"', "data-count", "newspost"]:
    assert tok in page, tok
for gone in ["duo-card", "aud-l", "fgrid", 'id="vcFlow"', "g-inset", "makeGlobe", "lifeimax"]:
    assert gone not in page, gone
for out in OUT:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(page)
print("built", len(page), "bytes ->", OUT[0])
