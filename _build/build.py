#!/usr/bin/env python3
"""Build Glasscliff.com into plain static HTML at the repository root.

Usage:
  python3 _build/build.py          # rebuild every page from templates and data
  python3 _build/build.py --news   # also refresh data/news.json from Google News RSS first

The output is committed to the repo and served by GitHub Pages from the main branch.
"""
import json, os, re, sys, urllib.request, urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa
from refdata import GLOSSARY, NEWS_QUERIES
import pages_content as pc
import pages_tools as pt
import pages_money as pm

NEWS_PATH = os.path.join(ROOT_DIR, "data", "news.json")

def fetch_news():
    """Headlines only (title, source, date, link). No article text is stored."""
    items, seen = [], set()
    for q in NEWS_QUERIES:
        url = "https://news.google.com/rss/search?" + urllib.parse.urlencode({"q": q + " when:30d", "hl": "en-US", "gl": "US", "ceid": "US:en"})
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (GlasscliffBot; +https://glasscliff.com)"})
            with urllib.request.urlopen(req, timeout=20) as r:
                root = ET.fromstring(r.read())
        except Exception as e:
            print("news: skip query", q, "-", e)
            continue
        for it in root.iter("item"):
            title = (it.findtext("title") or "").strip()
            src_el = it.find("source")
            source = (src_el.text or "").strip() if src_el is not None else ""
            if source and title.endswith(" - " + source):
                title = title[: -len(" - " + source)]
            key = re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()
            if not title or key in seen:
                continue
            seen.add(key)
            try:
                dt = parsedate_to_datetime(it.findtext("pubDate")).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            except Exception:
                dt = ""
            items.append({"title": title, "source": source, "date": dt, "link": (it.findtext("link") or "").strip()})
    items.sort(key=lambda x: x["date"], reverse=True)
    items = items[:30]
    if not items:
        print("news: nothing fetched; keeping existing file")
        return
    try:
        old = json.load(open(NEWS_PATH, encoding="utf-8"))
    except Exception:
        old = {"items": []}
    if [i["link"] for i in old.get("items", [])] == [i["link"] for i in items]:
        print("news: unchanged")
        return
    data = {"updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "items": items}
    with open(NEWS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("news: wrote", len(items), "items")

def url_for(path):
    return SITE_URL + "/" + ("" if path == "index.html" else path.replace("index.html", ""))

def build_sitemaps():
    seen, pages = set(), []
    for pg in PAGES:
        if pg["path"] in seen:
            continue
        seen.add(pg["path"]); pages.append(pg)
    news = pc.load_news()
    lastmod_news = (news.get("updated") or UPDATED)[:10]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for pg in pages:
        lm = lastmod_news if pg["path"] in ("index.html", "news.html") else UPDATED
        xml.append("<url><loc>%s</loc><lastmod>%s</lastmod><changefreq>%s</changefreq><priority>%s</priority></url>" % (esc(url_for(pg["path"])), lm, pg["changefreq"], pg["priority"]))
    xml.append("</urlset>")
    write("sitemap.xml", "\n".join(xml) + "\n")
    # search index
    idx = [{"u": pg["path"].replace("index.html", ""), "t": pg["title"], "d": pg["desc"], "k": pg["keywords"]} for pg in pages if pg["search"]]
    for term, d in GLOSSARY:
        slug = re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")
        idx.append({"u": "glossary.html#" + slug, "t": term + " (glossary)", "d": d, "k": "definition glossary"})
    write("data/search.json", json.dumps(idx, ensure_ascii=False, separators=(",", ":")))
    # HTML sitemap
    groups = {"Guides": [], "Tools": [], "Learn": [], "Get involved": [], "About and legal": []}
    for pg in pages:
        p = pg["path"]
        g = ("Guides" if p.startswith("guides/") else "Tools" if p.startswith("tools/") else
             "Learn" if p in ("index.html", "research.html", "glossary.html", "videos.html", "news.html", "search.html", "faq.html") else
             "Get involved" if p in ("get-help.html", "for-organizations.html", "advisors.html", "support.html", "contests.html", "careers.html", "advertise.html", "survey.html") else "About and legal")
        groups[g].append(pg)
    body = ('<div class="wrap page-head">' + crumbs([("{{p}}index.html", "Home"), (None, "Sitemap")]) + '<h1>Sitemap</h1><p class="dek">Every page on Glasscliff.</p></div><div class="wrap" style="padding-bottom:64px"><div class="paths" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr))">')
    for g, items in groups.items():
        body += '<div class="path"><h2 style="font-size:1.2rem">%s</h2><ul>%s</ul></div>' % (g, "".join('<li><a href="{{p}}%s">%s</a></li>' % (pg["path"].replace("index.html", "") or "index.html", esc(pg["title"])) for pg in items))
    body += '</div></div>'
    layout("sitemap.html", "Sitemap", "A list of every page on Glasscliff.com.", body, keywords="sitemap", priority="0.2", search=False)

def social_svgs():
    """SVG sources for the social image and app icon; the site workflow converts them to PNG with rsvg-convert."""
    art = HERO_ART.replace('<svg viewBox="0 0 640 460" role="img" aria-labelledby="cliff-t">', '<svg x="600" y="150" width="680" height="489" viewBox="0 0 640 460">')
    art = re.sub(r"<title[^>]*>.*?</title>", "", art)
    art = re.sub(r"<text[^>]*>risk of failure</text>", "", art)
    logo = LOGO.replace('<svg viewBox="0 0 32 32" aria-hidden="true" focusable="false">', '<svg x="70" y="70" width="58" height="58" viewBox="0 0 32 32">')
    sans = "Liberation Sans, DejaVu Sans, Arial, sans-serif"
    og = ('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">'
          '<rect width="1200" height="630" fill="#EEF2F1"/>' + logo +
          '<text x="142" y="113" font-family="%s" font-size="40" font-weight="700" fill="#1D2433">Glasscliff</text>' % sans +
          '<text font-family="%s" font-size="74" font-weight="700" fill="#1D2433" letter-spacing="-2"><tspan x="68" y="270">Is this role a</tspan><tspan x="68" y="352">glass cliff?</tspan></text>' % sans +
          '<text font-family="Liberation Serif, DejaVu Serif, Georgia, serif" font-size="28" fill="#2B3447"><tspan x="70" y="440">Free tools, research and confidential</tspan><tspan x="70" y="478">advice for high-stakes leadership roles.</tspan></text>' +
          art + '<rect y="616" width="1200" height="14" fill="#1D2433"/></svg>')
    write("assets/img/og.svg", og)
    icon = LOGO.replace('<svg viewBox="0 0 32 32" aria-hidden="true" focusable="false">', '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="-4 -4 40 40"><rect x="-4" y="-4" width="40" height="40" fill="#EEF2F1"/>')
    write("assets/img/icon.svg", icon)

def build_root_files():
    write("ads.txt", "google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0\n")
    write("robots.txt", "User-agent: *\nAllow: /\nDisallow: /thank-you.html\n\nSitemap: %s/sitemap.xml\n" % SITE_URL)
    write("site.webmanifest", json.dumps({"name": "Glasscliff", "short_name": "Glasscliff", "start_url": "./", "display": "standalone",
                                          "background_color": "#EEF2F1", "theme_color": "#1D2433",
                                          "icons": [{"src": "assets/img/favicon.svg", "sizes": "any", "type": "image/svg+xml"},
                                                    {"src": "assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, indent=2) + "\n")
    write("assets/img/favicon.svg", LOGO.replace('aria-hidden="true" focusable="false"', 'xmlns="http://www.w3.org/2000/svg"'))

def main():
    if "--news" in sys.argv:
        fetch_news()
    PAGES.clear()
    pc.build_home()
    pc.build_guides()
    pt.build_tools()
    pc.build_research(); pc.build_glossary(); pc.build_videos(); pc.build_news(); pc.build_search(); pc.build_faq()
    pm.build_get_help(); pm.build_orgs(); pm.build_advisors(); pm.build_support(); pm.build_contests()
    pm.build_careers(); pm.build_advertise(); pm.build_survey(); pm.build_contact()
    pc.build_about_legal(); pc.build_utility()
    build_sitemaps()
    build_root_files()
    social_svgs()
    print("built", len(PAGES), "indexable pages")

if __name__ == "__main__":
    main()
