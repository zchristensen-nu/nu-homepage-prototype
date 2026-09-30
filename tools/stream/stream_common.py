"""Shared chrome for the streaming concepts (7, 8, 9): v1 nav, overlays, footer, and
scripts, with the v1-only script blocks guarded or cut so a page without those
sections can't throw and kill everything after it."""
import re, os, json

V1 = "/Users/z.christensen/environment/prototypes/northeastern-homepage-v2.html"
ROOT = "/Users/z.christensen/Projects/nu-homepage-prototype"
MIRROR = "/Users/z.christensen/environment/prototypes"
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(V1).read()

def cut(a, b, inclusive_b=False):
    i = src.find(a); assert i >= 0, a[:60]
    j = src.find(b, i + len(a)); assert j > i, b[:60]
    return src[i:j + (len(b) if inclusive_b else 0)]

head0       = src[:src.find("  /* ---------- NAV ---------- */")]
nav_css     = cut("  /* ---------- NAV ---------- */", "  /* ---------- HERO ---------- */")
overlay_css = cut("  .srch{", "  /* ---------- SHEET SECTIONS (Adobe pattern) ---------- */")
tailcss     = cut("  /* ---------- ADMISSIONS CTA ---------- */", "</style>")
header_mk   = cut("<header", '<section class="hero"')
footer_mk   = cut("<footer>", "</footer>", True)
lenis       = cut("<script>/* Lenis", "</script>", True)
helpers     = cut("/* ============ shared helpers ============ */", "/* ============ globe data ============ */")
tail_js     = cut("/* ============ subtle scroll movement ============ */", "/* ============ boot ============ */")

assert helpers.count("admitIO.observe(admitEl);") == 1
helpers = helpers.replace("admitIO.observe(admitEl);", "if (admitEl) admitIO.observe(admitEl);")
for a, b in [("/* hero: content drifts", "/* parallax on select backdrops"),
             ("/* student life imax:", "/* smooth scrolling via Lenis")]:
    i0 = tail_js.find(a); i1 = tail_js.find(b)
    assert 0 < i0 < i1, a
    tail_js = tail_js[:i0] + tail_js[i1:]
for name in ("header_mk", "footer_mk"):
    globals()[name] = globals()[name].replace('src="img/', 'src="../img/')
MONO = re.search(r'<img[^>]*src="(data:image/[^"]+)"', header_mk).group(1)

SNAP = json.load(open(os.path.join(HERE, "ngn_snapshot.json")))
NGN = "https://news.northeastern.edu"
U = NGN + "/wp-content/uploads"
IMG = "../img/"

def page(name, rev, css, body, js):
    meta = '<meta name="prototype-rev" content="53">'
    assert head0.count(meta) == 1
    head = head0.replace(meta, f'<meta name="{name}-rev" content="{rev}">')
    return (head + nav_css + overlay_css + css + "\n" + tailcss
            + "</style>\n\n<body>\n\n" + header_mk + body + footer_mk + "\n"
            + lenis + "\n<script>\n" + helpers + js + "\n" + tail_js
            + "/* ============ boot ============ */\nnav.classList.toggle(\"solid\", scrollY > 60);\n</script>\n")

def write(dirname, html):
    assert html.count("<header") == 1 and html.count("<footer>") == 1
    for base in (ROOT, MIRROR):
        out = os.path.join(base, dirname, "index.html")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w").write(html)
    print("built", len(html), "bytes ->", os.path.join(ROOT, dirname))

def jsdata(obj):
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")

# ---------- shared content (every link verified 200 on 2026-09-30) ----------
def item(t, img, u, ex="", tag=""):
    return {"t": t, "img": img, "u": u, "ex": ex, "tag": tag}

PILLARS = [
 {"key": "coop", "t": "Co‑op", "img": IMG + "aquarium-dive.jpg", "u": "https://www.northeastern.edu/experiential-learning/",
  "film": "../coop-sm.mp4", "big": "https://www.northeastern.edu/wp-content/uploads/The-Co-Op-Experience_Video-2-Fusion-v3.mp4",
  "line": "Semesters of full‑time work, all over the map.",
  "ex": "Students alternate semesters in class with full‑time work at organizations around the world, then bring what they learned back to campus.",
  "tags": ["Experiential learning", "Every major", "Worldwide"]},
 {"key": "research", "t": "Research", "img": IMG + "satellite-testbed.jpg", "u": "https://research.northeastern.edu/",
  "big": "../hero.mp4",
  "line": "Our research story starts in the world.",
  "ex": "Faculty and students work on quantum systems, regenerative biology, robotics, and climate, and the work doesn’t stay in the lab.",
  "tags": ["Labs and institutes", "Undergraduate research", "Industry partners"]},
 {"key": "campuses", "t": "Global campuses", "img": U + "/2026/09/090726_CV_MoveIn_009.jpg", "u": "https://www.northeastern.edu/campuses/",
  "film": "../jamie-sm.mp4", "big": "https://www.nulondon.ac.uk/wp-content/uploads/2026/02/Discover-your-path-at-Northeastern-University-London.mp4",
  "line": "Fourteen campuses. One university.",
  "ex": "Boston, London, New York City, Oakland, and ten more campuses across the U.S., U.K., and Canada. Every one opens doors to all the others.",
  "tags": ["U.S., U.K., and Canada", "14 campuses"]},
 {"key": "life", "t": "Student life", "img": IMG + "convocation.jpg", "u": "https://studentlife.northeastern.edu/",
  "film": "../jamie-sm.mp4", "big": "https://www.northeastern.edu/wp-content/uploads/Jamie-Wong-Video-Fade.mp4",
  "line": "This place doesn’t slow down.",
  "ex": "Convocation, Fall Fest, club fairs, student elections, and everything in between, on every campus.",
  "tags": ["Clubs and organizations", "Arts", "Community"]},
 {"key": "athletics", "t": "Athletics", "img": U + "/2025/04/JIM28826.jpg", "u": "https://gonu.com/",
  "line": "Division I Huskies.",
  "ex": "From Matthews Arena to the Charles River, Huskies compete at the NCAA Division I level.",
  "tags": ["NCAA Division I", "Go Huskies"]},
 {"key": "admissions", "t": "Admissions", "img": U + "/2025/07/070125_AS_RPS_orientation_004.jpg", "u": "https://admissions.northeastern.edu/",
  "line": "Your turn.",
  "ex": "Four campuses to start from, and a world to work in after that. Here’s how to begin.",
  "tags": ["Apply", "Visit", "Financial aid"]},
 {"key": "graduate", "t": "Graduate programs", "img": IMG + "aerobat.jpg", "u": "https://graduate.northeastern.edu/",
  "line": "Advanced degrees, built around experience.",
  "ex": "Master’s, doctoral, and certificate programs across Northeastern’s colleges and campuses.",
  "tags": ["Master’s", "Doctoral", "Certificates"]},
 {"key": "nuin", "t": "N.U.in", "img": None, "u": "https://nuin.northeastern.edu/",
  "line": "Start your degree abroad.",
  "ex": "New students begin their Northeastern degree at one of eight partner institutions across Europe.",
  "tags": ["First year abroad", "Eight cities"],
  "cities": ["Dublin", "Belfast", "Glasgow", "Madrid", "Rome", "Prague", "Berlin", "Thessaloniki"]},
]
PBYKEY = {p["key"]: p for p in PILLARS}

COLLEGES = [
 ("Khoury", "Khoury College of Computer Sciences", "https://www.khoury.northeastern.edu/"),
 ("D’Amore-McKim", "D’Amore-McKim School of Business", "https://damore-mckim.northeastern.edu/"),
 ("Engineering", "College of Engineering", "https://coe.northeastern.edu/"),
 ("Science", "College of Science", "https://cos.northeastern.edu/"),
 ("CAMD", "College of Arts, Media and Design", "https://camd.northeastern.edu/"),
 ("CSSH", "College of Social Sciences and Humanities", "https://cssh.northeastern.edu/"),
 ("Bouvé", "Bouvé College of Health Sciences", "https://bouve.northeastern.edu/"),
 ("Law", "School of Law", "https://law.northeastern.edu/"),
 ("CPS", "College of Professional Studies", "https://cps.northeastern.edu/"),
]

CAMPUS_SITES = [
 ("Boston", U + "/2026/09/AImakerspace1400.jpg", "https://www.northeastern.edu/campuses/"),
 ("London", U + "/2026/09/090726_CV_MoveIn_009.jpg", "https://www.nulondon.ac.uk/"),
 ("Oakland", U + "/2026/09/092226_LC_Student_Government_Event_020.jpg", "https://oakland.northeastern.edu/"),
 ("New York City", None, "https://nyc.northeastern.edu/"),
 ("Portland, Maine", None, "https://roux.northeastern.edu/"),
 ("And nine more", None, "https://www.northeastern.edu/campuses/"),
]

COOP_STORIES = [
 item("Developing cameras for Apple products, on co‑op", IMG + "apple-coop.jpg", NGN + "/2025/01/15/apple-co-op-camera-process-engineer/", tag="Cupertino, California"),
 item("Teacher, mentor, big sister: six months in a Cambodian dormitory", U + "/2023/11/Cecile-Doehrty_1400.jpg", NGN + "/2023/11/06/harpswell-foundation-co-op-cambodian-women/", tag="Phnom Penh, Cambodia"),
 item("Learning how global negotiation really works", U + "/2023/11/Dialogue-of-Civilization_1400.jpg", NGN + "/2023/11/27/dialogue-of-civilizations-geneva-anniversary/", tag="Geneva, Switzerland"),
 item("Coffeehouses, Mozart and international finance, on co‑op", U + "/2023/09/Vienna1400.jpg", NGN + "/2023/10/13/unitcargo-finance-co-op-vienna-switzerland/", tag="Vienna, Austria"),
 item("Harvesting oysters on Maine’s Nonesuch River, on co‑op", IMG + "oyster-dock.jpg", NGN + "/2022/11/01/oyster-harvesting-maine/", tag="Scarborough, Maine"),
]
RESEARCH_STORIES = [
 item("This Northeastern researcher is making ‘waves’ with magnets", U + "/2026/09/Xufeng-Zhang_1400.jpg", NGN + "/2026/09/14/magnons-quantum-computing-research/", tag="Quantum"),
 item("Robots walk to class here. Researchers are teaching them how", U + "/2025/09/093025_MM_Field_Robotos_Lab_033.jpg", NGN + "/2025/10/01/walking-the-future/", tag="Robotics"),
 item("Cracking the axolotl code: how to regrow limbs and stay young", U + "/2026/07/072226_AS_-Calina_Copos_010.jpg", NGN + "/2026/07/27/axolotl-regeneration-anti-aging/", tag="Biology"),
 item("Scientists put algae to work making fuel. AI keeps watch", U + "/2026/08/Biofuel1400.jpg", NGN + "/2026/08/28/algae-biofuel-ai-research/", tag="Climate and energy"),
 item("Quieting ‘the noise’ in quantum computing", U + "/2026/08/quantumsystem1400.jpg", NGN + "/2026/08/07/modular-quantum-computing-research/", tag="Quantum"),
]
LIFE_STORIES = [
 item("Photos: Convocation ceremonies, Fall Fest and the first day of fall semester", U + "/2026/09/090826_MM_convocation_147.jpg", NGN + "/2026/09/11/photos-convocation-ceremonies-fall-fest-and-the-first-day-of-fall-semester/", tag="Boston"),
 item("All-analog Oakland student government race brings record voter turnout", U + "/2026/09/092226_LC_Student_Government_Event_020.jpg", NGN + "/2026/09/25/northeastern-oakland-student-elections/", tag="Oakland"),
 item("Northeastern students make a fast start to London life", U + "/2026/09/090726_CV_MoveIn_009.jpg", NGN + "/2026/09/08/move-in-week-london-campus/", tag="London"),
 item("Query, create or be curious at the new AI Makerspace in Boston", U + "/2026/09/AImakerspace1400.jpg", NGN + "/2026/09/23/ai-makerspace-boston-campus/", tag="Boston"),
 item("This graduate uses baking to cook up conversation about mental health", U + "/2026/08/Dayna-Altman1400.jpg", NGN + "/2026/09/15/bake-it-till-you-make-it-mental-health/", tag="Alumni"),
]
ATHLETICS_STORIES = [
 item("Former Husky Cam Schlittler stars as Yankees rout hometown Red Sox", U + "/2026/09/Cam-Schlittler-1400.jpg", NGN + "/2026/09/30/husky-cam-schlittler-yankees-red-sox-playoffs/", tag="Baseball"),
 item("Northeastern women’s hockey team’s title run ends in semifinals", U + "/2026/03/JIM22137.jpg", NGN + "/2026/03/20/huskies-buckeyes-womens-hockey-frozen-four/", tag="Women’s hockey"),
 item("Meet the youngest members of Northeastern’s hockey teams", U + "/2026/02/021026_AS_Ella_Tapp_029.jpg", NGN + "/2026/03/04/northeastern-hockey-team-impact/", tag="Hockey"),
 item("Huskies fall to BU in overtime Beanpot shootout", U + "/2026/02/020226_AS_M_Beapot_030.jpg", NGN + "/2026/02/03/beanpot-semis-huskies-terriers-td-garden/", tag="Beanpot"),
]
ADMIT_PATHS = [
 item("Apply to Northeastern", U + "/2025/07/070125_AS_RPS_orientation_004.jpg", "https://admissions.northeastern.edu/", "Start an application for any of our four undergraduate campuses.", "Admissions"),
 item("Visit a campus", U + "/2026/09/AImakerspace1400.jpg", "https://admissions.northeastern.edu/visit/", "Tours, information sessions, and virtual visits.", "Admissions"),
 item("Financial aid and scholarships", IMG + "convocation.jpg", "https://studentfinance.northeastern.edu/", "Grants, scholarships, and aid for undergraduate and graduate students.", "Student finance"),
 item("Start abroad with N.U.in", None, "https://nuin.northeastern.edu/", "Begin your degree at a partner institution in Europe.", "N.U.in"),
 item("Explore academics", IMG + "lunabotics.jpg", "https://www.northeastern.edu/academics/", "Majors, minors, and combined majors across nine colleges.", "Academics"),
 item("Graduate programs", IMG + "aerobat.jpg", "https://graduate.northeastern.edu/", "Master’s, doctoral, and certificate programs.", "Graduate"),
]
CATS = [  # NGN category slug, display name
 ("science-technology", "Science & Technology"), ("health", "Health"), ("society-culture", "Society & Culture"),
 ("business", "Business"), ("arts-entertainment", "Arts & Entertainment"), ("sports", "Sports"),
 ("law", "Law"), ("world-news", "World & National News"), ("research", "Research"),
]
CAT_IDS = {"latest": None, "research": 21443, "science-technology": 3, "health": 612, "society-culture": 6,
           "business": 4, "arts-entertainment": 5, "sports": 8, "law": 19491, "world-news": 14565}

SHARED_JS = r"""
/* ============ streaming concepts: shared ============ */
const esc = s => String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;");
const NGN_API = "https://news.northeastern.edu/wp-json/wp/v2/newspost";
async function ngnFetch(catId, n) {
  const q = `per_page=${n || 16}&_embed=wp:featuredmedia` + (catId ? `&categories=${catId}` : "");
  const r = await fetch(`${NGN_API}?${q}`);
  if (!r.ok) throw new Error(r.status);
  const tmp = document.createElement("div");
  const txt = h => { tmp.innerHTML = h || ""; return tmp.textContent.trim(); };
  return (await r.json()).map(p => {
    const m = p._embedded && p._embedded["wp:featuredmedia"] && p._embedded["wp:featuredmedia"][0];
    if (!m) return null;
    const sz = m.media_details && m.media_details.sizes;
    const img = ((sz && (sz.medium_large || sz.large || sz.medium)) || m).source_url || m.source_url;
    let ex = txt(p.excerpt && p.excerpt.rendered).replace(/\s+/g, " ");
    if (ex.length > 180) ex = ex.slice(0, 177).replace(/\s+\S*$/, "") + "…";
    return { t: txt(p.title.rendered), u: p.link, img, d: p.date, ex };
  }).filter(Boolean);
}
const fmtDate = iso => { try { return new Date(iso).toLocaleDateString("en-US", { month: "short", day: "numeric" }); } catch (e) { return ""; } };

/* continue browsing: this browser only */
const CB_KEY = "nu-stream-continue";
const cbRead = () => { try { return JSON.parse(localStorage.getItem(CB_KEY)) || []; } catch (e) { return []; } };
document.addEventListener("click", e => {
  const a = e.target.closest("a[data-cb]");
  if (!a) return;
  try {
    const rec = JSON.parse(a.dataset.cb);
    const list = cbRead().filter(c => c.u !== rec.u);
    list.unshift(rec);
    localStorage.setItem(CB_KEY, JSON.stringify(list.slice(0, 14)));
  } catch (err) { /* storage unavailable */ }
});
const cbAttr = it => esc(JSON.stringify({ t: it.t, img: it.img || "", u: it.u, tag: it.tag || "" }));
"""
