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
scrolly_js  = cut("/* ============ scrollytelling ============ */", "/* ============ research counters ============ */")
counters_js = cut("/* ============ research counters ============ */", "/* ============ research expanding row ============ */")
xrow_js     = cut("/* ============ research expanding row ============ */", "/* ============ quote carousel (scroll-snap cards) ============ */")
tail_js     = cut("/* ============ subtle scroll movement ============ */", "/* ============ boot ============ */")

head = head.replace('<meta name="prototype-rev" content="53">',
                    '<meta name="concept2-rev" content="17">')
assert 'concept2-rev' in head

outro_old_h = '<div class="big">Where will yours be?</div>'
assert scrolly_mk.count(outro_old_h) == 1
scrolly_mk = scrolly_mk.replace(outro_old_h, '<div class="big">And that&#8217;s just this fall.</div>')
outro_old_p = "<p>3,000+ employers. 151 countries. One application.</p>"
assert scrolly_mk.count(outro_old_p) == 1
scrolly_mk = scrolly_mk.replace(outro_old_p, "")
outro_pill = scrolly_mk.find('class="pill ghostw"')
if outro_pill > 0:
    a0 = scrolly_mk.rfind("<a", 0, outro_pill); a1 = scrolly_mk.find("</a>", outro_pill) + 4
    scrolly_mk = scrolly_mk[:a0] + scrolly_mk[a1:]

old_h = "<h2>Class is only half of it.</h2>"
assert rest_mk.count(old_h) == 1
rest_mk = rest_mk.replace(old_h, "<h2>Some of this you can’t major in.</h2>")

for name in ("header_mk", "hero_mk", "scrolly_mk", "sheet_mk", "rest_mk", "footer_mk"):
    v = (globals()[name].replace('src="img/', 'src="../img/')
         .replace("url('img/", "url('../img/").replace('src="hero.mp4"', 'src="../hero.mp4"'))
    globals()[name] = v


# v1 sheet: upgrade counters to the c2 giant style, point the storylink at NGN research
c_i0 = sheet_mk.find('<div class="counters" id="counters">')
c_i1 = sheet_mk.find('</div>\n      <a class="storylink', c_i0)
assert 0 < c_i0 < c_i1, "counters block in sheet"
RC = """<div class="rc-grid" id="counters">
        <div class="rc"><div class="n">$<span data-count="296">0</span>M</div><div class="l">external research awards last year</div></div>
        <div class="rc"><div class="n"><span data-count="50">0</span>+</div><div class="l">federally funded centers and institutes</div></div>
        <div class="rc"><div class="n"><span data-count="510">0</span></div><div class="l">patents and counting</div></div>
      """
sheet_mk = sheet_mk[:c_i0] + RC + sheet_mk[c_i1:]
cv = 'href="https://news.northeastern.edu/2023/09/06/convocation-2023/">How our president talks about AI and being human</a>'
assert sheet_mk.count(cv) == 1
sheet_mk = sheet_mk.replace(cv, 'href="https://news.northeastern.edu/category/research/">Research coverage on NGN</a>')

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

HERO_QUOTE = {
 "img": "../img/oyster-dock.jpg", "pos": "20% 35%",
 "text": "I wanted to do this job and test myself and see if I like working outdoors as much as I hoped. So far, so good.",
 "name": "Maddy Russell",
 "who": "Environmental &amp; sustainability science &middot; Co‑op at Nonesuch Oyster Farm, Maine",
 "url": "/2022/11/01/oyster-harvesting-maine/", "cta": "Read Maddy’s story",
}

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

def quote_words():
    return "".join(f'<span class="qw">{w}</span> ' for w in HERO_QUOTE["text"].split(" "))

def voice_rows():
    out = ""
    for img, pos, lines, name, who, u, cta in QUOTES:
        if name == HERO_QUOTE["name"]: continue
        q = " ".join(lines)
        out += (f'<a class="vr" href="{NGN}{u}"><span class="vr-q">{q}</span>'
                f'<span class="vr-who"><b>{name}</b> {who}</span></a>\n')
    return out

def ledger_rows():
    out = ""
    for img, pos, lines, name, who, u, cta in QUOTES:
        q = " ".join(lines)
        out += (f'<article class="led rv"><span class="led-im"><img src="{img}" alt="" loading="lazy" style="object-position:{pos}"></span>'
                f'<div class="led-b"><blockquote>{q}</blockquote>'
                f'<div class="v-who"><b>{name}</b> {who}</div>'
                f'<a class="storylink" href="{NGN}{u}">{cta}</a></div></article>\n')
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

def verbar(cur):
    links = [("index.html", "Current", "cur"), ("quotes-a.html", "One voice", "a"),
             ("quotes-b.html", "Ledger", "b"), ("quotes-c.html", "Portraits", "c")]
    out = '<div class="verbar"><span class="lbl">Quotes:</span>'
    for href, label, key in links:
        cls = ' class="cur"' if key == cur else ''
        out += f'<a href="{href}"{cls}>{label}</a>'
    return out + "</div>\n"

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

  /* ---------- research counters (giant style, lives inside the v1 sheet) ---------- */
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

  /* ---------- variant A: one voice, lit word by word ---------- */
  .q-track{height:260svh}
  .q-stage{position:sticky;top:0;height:100svh;min-height:600px;display:flex;align-items:center;overflow:hidden}
  .q-grid{display:grid;grid-template-columns:5fr 7fr;gap:clamp(28px,5vw,84px);align-items:center;width:100%}
  .q-photo{border-radius:16px;overflow:hidden;height:min(66svh,640px)}
  .q-photo img{width:100%;height:100%;object-fit:cover;display:block}
  .q-quote{font-size:clamp(28px,3.6vw,56px);font-weight:300;letter-spacing:-.018em;line-height:1.22;
    max-width:22ch;text-wrap:balance}
  .q-quote .qw{opacity:.16;transition:opacity .35s var(--ease)}
  .q-quote .qw.on{opacity:1}
  .q-meta{margin-top:30px;opacity:0;transform:translateY(12px);
    transition:opacity .6s var(--ease),transform .6s var(--ease)}
  .q-meta.on{opacity:1;transform:none}
  .q-more{background:var(--dark);padding:10px 0 110px}
  .q-more .vr{display:grid;grid-template-columns:1fr auto;gap:8px 40px;align-items:end;
    padding:30px 2px;border-top:1px solid rgba(255,255,255,.14);color:#E5E5E5;transition:color .25s}
  .q-more .vr:hover{color:#fff}
  .vr-q{font-size:clamp(16px,1.4vw,19px);font-weight:300;line-height:1.5;max-width:64ch}
  .vr-who{font-size:13.5px;color:#A9A9B2;white-space:nowrap}
  .vr-who b{color:#fff;font-weight:600;display:block}
  @media(max-width:820px){
    .q-grid{grid-template-columns:1fr;gap:26px}
    .q-photo{height:38svh}
    .q-more .vr{grid-template-columns:1fr}
    .vr-who{white-space:normal}
  }
  @media (prefers-reduced-motion: reduce){
    .q-track{height:auto}
    .q-stage{position:static;height:auto;padding:90px 0}
    .q-quote .qw{opacity:1;transition:none}
    .q-meta{opacity:1;transform:none}
  }

  /* ---------- variant B: the ledger, all voices in flow ---------- */
  .voices-b{position:relative;z-index:6;background:var(--dark);color:#fff;padding:120px 0}
  .led{display:grid;grid-template-columns:4fr 8fr;gap:clamp(24px,4vw,72px);align-items:center;
    padding:clamp(48px,7vh,84px) 0;border-top:1px solid rgba(255,255,255,.14)}
  .led:first-of-type{border-top:0;padding-top:0}
  .led:nth-of-type(even){grid-template-columns:8fr 4fr}
  .led:nth-of-type(even) .led-im{order:2}
  .led-im{display:block;border-radius:14px;overflow:hidden}
  .led-im img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block}
  .led-b blockquote{font-size:clamp(22px,2.6vw,40px);font-weight:300;letter-spacing:-.015em;
    line-height:1.25;max-width:26ch;text-wrap:balance}
  .led-b .v-who{margin-top:20px}
  .led-b .storylink{color:#fff}
  @media(max-width:820px){
    .led,.led:nth-of-type(even){grid-template-columns:1fr}
    .led:nth-of-type(even) .led-im{order:0}
  }

  /* ---------- variant C: sticky portrait, flowing quotes ---------- */
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
  .vc-q .v-who{margin-top:20px}
  .vc-q .storylink{color:#fff}
  @media(max-width:820px){
    .vc{grid-template-columns:1fr}
    .vc-media{display:none}
    .vc-flow .vc-q{min-height:0;padding:34px 0;opacity:1}
  }

  /* ---------- variant switcher ---------- */
  .verbar{position:fixed;left:14px;bottom:14px;z-index:300;display:flex;gap:2px;align-items:center;
    background:rgba(16,16,20,.88);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.16);
    border-radius:999px;padding:5px 8px;font-size:12px}
  .verbar .lbl{padding:0 6px;color:#8a8a92}
  .verbar a{padding:5px 11px;border-radius:999px;color:#ddd}
  .verbar a:hover{background:rgba(255,255,255,.14)}
  .verbar a.cur{background:#fff;color:#111}
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
{{SHEET}}

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

{{VOICES_SECTION}}
"""
VOICES_CUR = f"""<section class="voices" id="voices" aria-label="Student voices">
  <div class="v-track" id="vTrack">
    <div class="v-stage">
{quote_slides()}    </div>
  </div>
</section>

"""

VOICES_A = f"""<section class="voices" id="voices" aria-label="Student voices">
  <div class="q-track" id="qTrack">
    <div class="q-stage"><div class="wrap q-grid">
      <div class="q-photo"><img src="{HERO_QUOTE['img']}" alt="" style="object-position:{HERO_QUOTE['pos']}"></div>
      <div>
        <blockquote class="q-quote" id="qQuote">&ldquo;{quote_words()}&rdquo;</blockquote>
        <div class="q-meta" id="qMeta">
          <div class="v-who"><b>{HERO_QUOTE['name']}</b> {HERO_QUOTE['who']}</div>
          <a class="storylink" href="{NGN}{HERO_QUOTE['url']}">{HERO_QUOTE['cta']}</a>
        </div>
      </div>
    </div></div>
  </div>
  <div class="q-more"><div class="wrap">
{voice_rows()}  </div></div>
</section>
"""

VOICES_B = f"""<section class="voices-b" id="voices" aria-label="Student voices">
  <div class="wrap">
{ledger_rows()}  </div>
</section>
"""

_vc_imgs, _vc_blocks = portrait_stack()
VOICES_C = f"""<section class="voices-c" id="voices" aria-label="Student voices">
  <div class="wrap vc">
    <div class="vc-media">{_vc_imgs}</div>
    <div class="vc-flow" id="vcFlow">
{_vc_blocks}    </div>
  </div>
</section>
"""

VOICES_MAP = {"cur": VOICES_CUR, "a": VOICES_A, "b": VOICES_B, "c": VOICES_C}

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

/* ============ variant A: words light as you scroll ============ */
const qTrack = $("#qTrack"), qQuote = $("#qQuote");
if (qTrack && qQuote && !reduceMotion) {
  const qws = [...qQuote.querySelectorAll(".qw")];
  const qMeta = $("#qMeta");
  const qUpd = () => {
    const r = qTrack.getBoundingClientRect();
    const p = clamp01(-r.top / (r.height - innerHeight));
    const lit = Math.floor(p * 1.18 * qws.length);
    qws.forEach((w, i) => w.classList.toggle("on", i < lit));
    if (qMeta) qMeta.classList.toggle("on", p > 0.82);
  };
  addEventListener("scroll", () => requestAnimationFrame(qUpd), { passive: true });
  addEventListener("resize", qUpd);
  qUpd();
}
if (qQuote && reduceMotion) $$("#qQuote .qw").forEach(w => w.classList.add("on"));

/* ============ variant C: flowing quotes drive the sticky portrait ============ */
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

body_mid = AFTER_SCROLLY.replace("{SHEET}", sheet_mk).replace("{VOICES_SECTION}", VOICES_MAP["c"])
page = (head + nav_css + hero_css + scrolly_css + sheet_css + NEW_CSS + "\n" + tailcss
        + "</style>\n\n<body>\n\n"
        + header_mk + hero_mk + NEW_BODY + scrolly_mk + body_mid + rest_mk + WIRE_FOOT + footer_mk + "\n"
        + lenis + "\n<script>\n" + land + "\n" + coops + "\n" + helpers + globedata + engine
        + scrolly_js + counters_js + xrow_js + NEW_JS + "\n" + tail_js + NEW_BOOT + "</script>\n")

assert page.count("<header") == 1 and page.count("<footer>") == 1
assert "{SHEET}" not in page and "{VOICES_SECTION}" not in page
for tok in ['id="srch"', 'class="scrolly"', 'id="xrow"', "xcard", "rc-grid", "j-rail",
            'id="vcFlow"', "vc-media", "wire foot", "lifeimax", 'class="admit"',
            "concept2-rev", 'content="17"', "data-count", "newspost"]:
    assert tok in page, tok
for gone in ["rr-reel", "verbar", 'id="vTrack"', 'id="qTrack"', "voices-b"]:
    assert gone not in page, gone
for out in OUT:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(page)
print("built", len(page), "bytes ->", OUT[0])
