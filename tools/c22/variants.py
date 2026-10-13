"""Concept 22 head tags (favicon, Open Graph) and its two story-row variants.

Concept 22 is hand-edited; rerun this after any edit to it:  python3 tools/c22/variants.py
  concept-22a: the "Latest" row removed; rows lead with University News, then Global Entrepreneurship; HIDE stories held out
  concept-22b: two stories kept out of every row (HIDE below)
"""
import os, re

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
PAGES = "https://zchristensen-nu.github.io/nu-homepage-prototype"
BRAND = "https://brand.northeastern.edu/global/assets/favicon"
TITLE = "Northeastern University"
DESC = "Founded in 1898, Northeastern is a global, experiential, research university built on a tradition of engagement with the world."
HIDE = ["https://news.northeastern.edu/2026/10/12/november-midterms-political-analysis/",
        "https://news.northeastern.edu/2026/10/09/boston-rats-ai-dictionary/"]

def head(folder):
    url = f"{PAGES}/{folder}/"
    return f"""<!-- head:start -->
<meta name="description" content="{DESC}">
<link rel="icon" type="image/png" sizes="32x32" href="{BRAND}/favicon-32x32.png?v=2">
<link rel="icon" type="image/png" sizes="16x16" href="{BRAND}/favicon-16x16.png?v=2">
<link rel="apple-touch-icon" sizes="152x152" href="{BRAND}/apple-touch-152x152.png?v=2">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{TITLE}">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{PAGES}/img/og-home.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Two Northeastern students unpacking on move-in day, with the Northeastern University logo">
<meta name="twitter:card" content="summary_large_image">
<!-- head:end -->"""

def with_head(page, folder):
    page = re.sub(r"<!-- head:start -->.*?<!-- head:end -->\n", "", page, flags=re.S)
    assert page.count("<title>Northeastern University</title>\n") == 1
    return page.replace("<title>Northeastern University</title>\n", "<title>Northeastern University</title>\n" + head(folder) + "\n", 1)

def hold_out(page):
    """the HIDE stories never reach a row; each row backfills from the rest of its 24 fetched stories"""
    old = '.filter(p => !/^Photos:/i.test(p.title.rendered) && !shown.has(p.link))'
    assert page.count(old) == 1
    page = page.replace(old, '.filter(p => !/^Photos:/i.test(p.title.rendered) && !shown.has(p.link) && !HIDE.has(p.link))')
    page = page.replace("(async () => {\n  const API", "const HIDE = new Set(%r);\n(async () => {\n  const API" % HIDE, 1)
    assert "const HIDE" in page
    return page

def write(folder, page):
    os.makedirs(os.path.join(ROOT, folder), exist_ok=True)
    open(os.path.join(ROOT, folder, "index.html"), "w").write(page)
    print("built", folder)

src = os.path.join(ROOT, "concept-22", "index.html")
base = with_head(open(src).read(), "concept-22")
write("concept-22", base)

# 22a: no Latest row (the next row takes its place and its first-row fallback)
a, n = re.subn(r'<section class="crow" data-q="" id="ngnRow" aria-label="Latest".*?</section>\n', "", base, count=1, flags=re.S)
assert n == 1
# rows lead with University News, then Global Entrepreneurship; Human-Centered AI and Research follow
sec = {k: re.search(r'<section class="crow"[^>]* id="%s".*?</section>\n' % k, a, flags=re.S).group(0) for k in ("entRow", "aiRow", "uniRow", "researchRow")}
run = sec["entRow"] + sec["aiRow"] + sec["uniRow"] + sec["researchRow"]
assert a.count(run) == 1, "rows are no longer consecutive in concept 22"
a = a.replace(run, sec["uniRow"] + sec["entRow"] + sec["aiRow"] + sec["researchRow"])
write("concept-22a", with_head(hold_out(a), "concept-22a"))

# 22b: the HIDE stories held out of every row
write("concept-22b", with_head(hold_out(base), "concept-22b"))
