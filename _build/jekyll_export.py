#!/usr/bin/env python3
"""Export the built site as Jekyll pages that share one layout (_layouts/default.html).

GitHub Pages renders these natively on the free plan, with no Actions needed. Each page keeps
its own head tags, schema and main content; the owner bar, header, footer, AdSense tag and scripts
come from the layout, so they are identical on every page.

Usage: python3 _build/build.py && python3 _build/jekyll_export.py [OUT_DIR]
(OUT_DIR defaults to the repository root, replacing the full HTML files in place.)
--check renders every exported page back through a Liquid emulator and compares it with the build.
"""
import glob, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT_DIR, ADSENSE_TAG, NAV, OWNER_CONTACT, header, footer

def L(s):  # Liquid output tag
    return "{{ page.%s }}" % s

def layout():
    nav = "".join('<a href="{{ page.root }}%s"{%% if page.active == "%s" %%} aria-current="page"{%% endif %%}>%s</a>' % (h, h, t) for h, t in NAV)
    head_common = ('<meta name="twitter:card" content="summary_large_image">'
                   '<link rel="icon" href="{{ page.root }}assets/img/favicon.svg" type="image/svg+xml">'
                   '<link rel="manifest" href="{{ page.root }}site.webmanifest">'
                   '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
                   '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;600;700;800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap">'
                   '<link rel="stylesheet" href="{{ page.root }}assets/css/site.css">')
    hdr = header("{{ page.root }}", None)
    hdr = re.sub(r'<nav id="site-nav" class="nav" aria-label="Main">.*?<a class="btn', '<nav id="site-nav" class="nav" aria-label="Main">' + nav + '<a class="btn', hdr)
    return ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">{{ page.extra_head }}'
            '<meta name="viewport" content="width=device-width, initial-scale=1">{{ page.head }}' + head_common +
            '{% if page.ads %}' + ADSENSE_TAG + '{% endif %}{{ page.schema }}</head>'
            '<body data-root="{{ page.root }}"{% if page.sticky %} class="has-sticky"{% endif %}>' + hdr +
            '<main id="main">{{ content }}</main>' + footer("{{ page.root }}") +
            '{% if page.sticky %}<a class="btn btn-risk sticky-cta" href="{{ page.root }}get-help.html">Get a confidential review</a>{% endif %}'
            '<script src="{{ page.root }}assets/js/config.js"></script><script src="{{ page.root }}assets/js/main.js"></script>'
            '{% if page.tools %}<script src="{{ page.root }}assets/js/tools.js"></script>{% endif %}</body></html>')

def split(path, html):
    m = re.match(r'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">(.*?)<meta name="viewport" content="width=device-width, initial-scale=1">(.*?)<meta name="twitter:card"', html, re.S)
    extra_head, head = m.group(1), m.group(2)
    schema = "".join(re.findall(r'<script type="application/ld\+json">.*?</script>', html.split("</head>")[0], re.S))
    body_open = re.search(r'<body data-root="([^"]*)"( class="has-sticky")?>', html)
    active = re.search(r'<a href="[^"]*?((?:tools/|guides/|research\.html|videos\.html|for-organizations\.html))" aria-current="page">', html)
    main = re.search(r'<main id="main">(.*)</main>', html, re.S).group(1)
    fm = {"layout": "default", "root": body_open.group(1), "head": head, "extra_head": extra_head, "schema": schema,
          "ads": ADSENSE_TAG in html.split("</head>")[0], "sticky": bool(body_open.group(2)),
          "tools": "assets/js/tools.js" in html, "active": active.group(1) if active else ""}
    return fm, main

def to_page(fm, main):
    lines = ["---"] + ["%s: %s" % (k, json.dumps(v, ensure_ascii=False)) for k, v in fm.items()] + ["---"]
    return "\n".join(lines) + "\n{% raw %}" + main + "{% endraw %}"

def emulate(lay, page_src):
    """Minimal Liquid rendering for the tags used in the layout, to prove the export is lossless."""
    _, fm_txt, rest = page_src.split("---\n", 2)
    fm = {}
    for line in fm_txt.strip().split("\n"):
        k, v = line.split(": ", 1)
        fm[k] = json.loads(v)
    content = rest.lstrip("\n")
    content = content.replace("{% raw %}", "", 1)
    content = content[: content.rfind("{% endraw %}")]
    out = lay
    out = re.sub(r'\{% if page\.active == "([^"]+)" %\}(.*?)\{% endif %\}', lambda m: m.group(2) if fm.get("active") == m.group(1) else "", out)
    out = re.sub(r'\{% if page\.(\w+) %\}(.*?)\{% endif %\}', lambda m: m.group(2) if fm.get(m.group(1)) else "", out, flags=re.S)
    out = re.sub(r'\{\{ page\.(\w+) \}\}', lambda m: str(fm.get(m.group(1), "")), out)
    return out.replace("{{ content }}", content)

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out_dir = args[0] if args else ROOT_DIR
    lay = layout()
    files = sorted(f for f in glob.glob(os.path.join(ROOT_DIR, "**", "*.html"), recursive=True)
                   if "/_build/" not in f and "/_layouts/" not in f)
    bad = 0
    for full in files:
        rel = os.path.relpath(full, ROOT_DIR)
        html = open(full, encoding="utf-8").read()
        if html.startswith("---"):
            continue
        fm, main_html = split(rel, html)
        page = to_page(fm, main_html)
        if "--check" in sys.argv and emulate(lay, page) != html:
            bad += 1
            print("MISMATCH", rel)
        dest = os.path.join(out_dir, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "w", encoding="utf-8").write(page)
    os.makedirs(os.path.join(out_dir, "_layouts"), exist_ok=True)
    open(os.path.join(out_dir, "_layouts", "default.html"), "w", encoding="utf-8").write(lay)
    print("exported", len(files), "pages;", "mismatches:", bad)

if __name__ == "__main__":
    main()
