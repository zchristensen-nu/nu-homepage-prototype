"""Snapshot NGN stories per category (title, link, image, date, excerpt) for baking into the streaming concepts."""
import json, re, html, urllib.request
CATS = {"latest": None, "research": 21443, "science-technology": 3, "health": 612, "society-culture": 6,
        "business": 4, "arts-entertainment": 5, "sports": 8, "law": 19491, "world-news": 14565}
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 prototype-snapshot"})
    return json.load(urllib.request.urlopen(req, timeout=30))
def strip(s): return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()
out = {}
for slug, cid in CATS.items():
    q = "per_page=16&_embed=wp:featuredmedia" + (f"&categories={cid}" if cid else "")
    posts = get(f"https://news.northeastern.edu/wp-json/wp/v2/newspost?{q}")
    rows = []
    for p in posts:
        t = strip(p["title"]["rendered"])
        if t.lower().startswith("photos:") and slug != "latest": pass
        m = (p.get("_embedded") or {}).get("wp:featuredmedia") or [{}]
        m = m[0] if m else {}
        sz = (m.get("media_details") or {}).get("sizes") or {}
        img = (sz.get("medium_large") or sz.get("large") or sz.get("medium") or m).get("source_url") or m.get("source_url")
        if not img: continue
        ex = strip(p["excerpt"]["rendered"])
        ex = re.sub(r"\s+", " ", ex)
        if len(ex) > 180: ex = ex[:177].rsplit(" ", 1)[0] + "…"
        rows.append({"t": t, "u": p["link"], "img": img, "d": p["date"], "ex": ex})
    out[slug] = rows
    print(slug, len(rows))
json.dump(out, open("ngn_snapshot.json", "w"), ensure_ascii=False, indent=1)
