# Shared engine for the Glasscliff.com static build: constants, chrome, layout, registry, form helpers.
import html, json, os, re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = os.environ.get("GC_SITE_URL", "https://glasscliff.com")
NAME = "Glasscliff"
DOMAIN = "Glasscliff.com"
TAGLINE = "See the edge before you step onto it."
ADS_CLIENT = "ca-pub-6620975821265271"
OWNER_CONTACT = "https://web.works/contact"
PUBLISHED = "2026-11-12"
UPDATED = "2026-11-12"
ADSENSE_TAG = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>'
FONTS = "https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;600;700;800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap"

PAGES = []  # registry: dicts with path, title, desc, keywords, priority, changefreq, index, search

def esc(t):
    return html.escape(str(t), quote=True)

def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()

def link(src):
    """Turn 'scholar:<title>' into a Google Scholar search URL; pass other URLs through."""
    if src.startswith("scholar:"):
        from urllib.parse import quote_plus
        return "https://scholar.google.com/scholar?q=" + quote_plus('"' + src[8:] + '"')
    return src

# ---------- SVG assets ----------
LOGO = ('<svg viewBox="0 0 32 32" aria-hidden="true" focusable="false">'
        '<path d="M2 30V12l7-3 5 2 4-2v21z" fill="#1D2433"/>'
        '<path d="M2 17l7-2 5 1.5 4-1.5" fill="none" stroke="#B9A58A" stroke-width="1.2"/>'
        '<path d="M2 23l7-1.5 5 1 4-1" fill="none" stroke="#B9A58A" stroke-width="1"/>'
        '<rect x="18" y="8.2" width="12.5" height="2.6" rx=".6" fill="#9FD3D6" stroke="#2E7C83" stroke-width=".8"/>'
        '<circle cx="25.5" cy="5.6" r="1.6" fill="#B3264A"/></svg>')

ICONS = {
 "scanner": '<svg viewBox="0 0 52 52" aria-hidden="true"><path d="M6 36a20 20 0 0 1 40 0" fill="none" stroke="#1D2433" stroke-width="3"/><path d="M6 36a20 20 0 0 1 9-16.7" fill="none" stroke="#3F7D4E" stroke-width="3"/><path d="M37 19.3A20 20 0 0 1 46 36" fill="none" stroke="#B3264A" stroke-width="3"/><path d="M26 36l9-12" stroke="#1D2433" stroke-width="3" stroke-linecap="round"/><circle cx="26" cy="36" r="3" fill="#1D2433"/></svg>',
 "offer": '<svg viewBox="0 0 52 52" aria-hidden="true"><rect x="11" y="6" width="30" height="40" rx="3" fill="#F7F9F8" stroke="#1D2433" stroke-width="2.5"/><path d="M17 17h18M17 24h18M17 31h11" stroke="#B9A58A" stroke-width="2.5" stroke-linecap="round"/><path d="M30 38l4 4 8-9" fill="none" stroke="#2E7C83" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 "plan": '<svg viewBox="0 0 52 52" aria-hidden="true"><path d="M6 40h40" stroke="#1D2433" stroke-width="2.5"/><path d="M8 40V30h10v10M21 40V22h10v18M34 40V12h10v28" fill="#9FD3D6" stroke="#1D2433" stroke-width="2.5"/></svg>',
 "ready": '<svg viewBox="0 0 52 52" aria-hidden="true"><polygon points="26,6 45,20 38,43 14,43 7,20" fill="none" stroke="#B9A58A" stroke-width="2"/><polygon points="26,13 38,22 34,37 17,35 13,22" fill="#9FD3D6" stroke="#2E7C83" stroke-width="2.5"/></svg>',
 "board": '<svg viewBox="0 0 52 52" aria-hidden="true"><rect x="8" y="22" width="36" height="8" rx="2" fill="#1D2433"/><circle cx="14" cy="15" r="4" fill="#B9A58A"/><circle cx="26" cy="13" r="4" fill="#2E7C83"/><circle cx="38" cy="15" r="4" fill="#B9A58A"/><circle cx="14" cy="38" r="4" fill="#B9A58A"/><circle cx="38" cy="38" r="4" fill="#B9A58A"/></svg>',
}

HERO_ART = '''<svg viewBox="0 0 640 460" role="img" aria-labelledby="cliff-t">
<title id="cliff-t">Cross-section of a cliff in rock strata, with a glass ledge extending over the drop and a figure standing near its edge</title>
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EEF2F1"/><stop offset="1" stop-color="#DDE7E6"/></linearGradient>
<linearGradient id="glassg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9FD3D6" stop-opacity=".85"/><stop offset="1" stop-color="#9FD3D6" stop-opacity=".25"/></linearGradient>
</defs>
<g fill="none" stroke="#B9A58A" stroke-width="1" opacity=".55">
<path d="M330 70c60-14 140-8 300 6"/><path d="M360 96c70-10 160-6 270 4"/><path d="M400 122c60-6 140-4 230 2"/>
</g>
<path d="M0 132 L120 116 L210 124 L318 108 L318 460 L0 460Z" fill="#2B3447"/>
<path d="M0 178 L130 166 L230 176 L318 168 L318 214 L210 222 L110 214 L0 222Z" fill="#3A4459"/>
<path d="M0 262 L120 252 L240 264 L318 256 L318 300 L230 306 L120 298 L0 304Z" fill="#46516A"/>
<path d="M0 346 L140 336 L250 348 L318 342 L318 384 L240 390 L120 382 L0 390Z" fill="#3A4459"/>
<g fill="none" stroke="#B9A58A" stroke-width="1.3" opacity=".9">
<path d="M0 150 L130 140 L230 150 L318 140"/><path d="M0 238 L120 230 L240 240 L318 232"/><path d="M0 324 L130 316 L240 326 L318 320"/><path d="M0 410 L120 402 L250 412 L318 406"/>
</g>
<path d="M318 108 L330 150 L322 210 L336 270 L326 340 L340 400 L332 460 L318 460Z" fill="#1D2433"/>
<rect x="300" y="100" width="250" height="12" rx="2" fill="url(#glassg)" stroke="#2E7C83" stroke-width="1.5"/>
<path d="M310 103h230" stroke="#fff" stroke-width="1.2" opacity=".8"/>
<g stroke="#2E7C83" stroke-width="1" opacity=".6"><path d="M380 112v8M450 112v8M520 112v8"/></g>
<g transform="translate(486 58)"><circle cx="0" cy="0" r="7" fill="#B3264A"/><path d="M0 7v22M0 14l-9 9M0 14l9 7M0 29l-7 13M0 29l7 13" stroke="#1D2433" stroke-width="3.2" stroke-linecap="round"/></g>
<g stroke="#4F5A6D" stroke-width="1.2"><path d="M600 118V452" stroke-dasharray="4 6"/><path d="M592 118h16M594 200h12M594 280h12M594 360h12M592 452h16"/></g>
<text x="586" y="204" text-anchor="end" font-family="Schibsted Grotesk, sans-serif" font-size="12" fill="#4F5A6D">risk of failure</text>
</svg>'''

# ---------- chrome ----------
NAV = [("tools/", "Tools"), ("guides/", "Guides"), ("research.html", "Research"), ("videos.html", "Videos"), ("for-organizations.html", "For boards")]

def header(p, active):
    items = "".join('<a href="%s%s"%s>%s</a>' % (p, href, ' aria-current="page"' if active == href else "", label) for href, label in NAV)
    return ('<a class="skip" href="#main">Skip to content</a>'
            '<div class="owner-bar"><a href="%s" target="_blank" rel="noopener">Contact, if you are interested in this website/domain name/Sponsorship/Advertisement/Partnership</a></div>'
            '<header class="site-header"><div class="wrap">'
            '<a class="brand" href="%sindex.html" aria-label="Glasscliff home">%s<span>Glasscliff</span></a>'
            '<button class="menu-btn" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>'
            '<nav id="site-nav" class="nav" aria-label="Main">%s<a class="btn btn-primary btn-sm" href="%sget-help.html">Get a confidential review</a></nav>'
            '</div></header>') % (OWNER_CONTACT, p, LOGO, items, p)

def footer(p):
    col = lambda title, links: '<div><h2>%s</h2><ul>%s</ul></div>' % (title, "".join('<li><a href="%s%s">%s</a></li>' % (p, h, t) for h, t in links))
    return ('<footer class="site-footer"><div class="wrap"><div class="foot-grid">'
            '<div class="foot-brand"><a class="brand" href="%sindex.html" style="color:#fff">%s<span>Glasscliff</span></a>'
            '<p>The independent guide to high-stakes leadership roles, for the people who take them and the boards that appoint them.</p>'
            '<form class="newsletter" data-gc-form="newsletter" data-subject="Newsletter sign-up" data-ok="You are subscribed. The next Edge Brief will reach you soon.">'
            '<label class="sr" for="nl-email">Email address</label><input id="nl-email" type="email" name="email" placeholder="Your email" required autocomplete="email">'
            '<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">'
            '<button class="btn btn-primary" type="submit">Get the Edge Brief</button><p class="form-msg" role="status" aria-live="polite"></p></form></div>'
            % (p, LOGO)) + \
        col("Tools", [("tools/risk-scanner.html", "Risk Scanner"), ("tools/offer-protection.html", "Offer Protection Builder"), ("tools/100-day-plan.html", "100-Day Planner"), ("tools/readiness-quiz.html", "Readiness Check"), ("tools/board-check.html", "Board Appointment Check")]) + \
        col("Learn", [("guides/", "Guides"), ("research.html", "Research Library"), ("glossary.html", "Glossary"), ("videos.html", "Videos"), ("news.html", "Leadership news"), ("survey.html", "Pulse Survey")]) + \
        col("Get involved", [("get-help.html", "Confidential review"), ("for-organizations.html", "For organisations"), ("advisors.html", "Advisor Network"), ("support.html", "Support us"), ("contests.html", "Edge Prize"), ("careers.html", "Careers"), ("advertise.html", "Advertise and sponsor")]) + \
        col("About", [("about.html", "About"), ("contact.html", "Contact"), ("faq.html", "FAQ"), ("editorial-policy.html", "Editorial policy"), ("privacy.html", "Privacy"), ("terms.html", "Terms"), ("disclaimer.html", "Disclaimer and trademarks"), ("sitemap.html", "Sitemap"), ("search.html", "Search")]) + \
        ('</div><div class="foot-legal"><p>&copy; <span data-year>2026</span> Glasscliff.com. Independent publication. "Glass cliff" is a descriptive research term; we are not affiliated with any company, product or person using that or a similar name. '
         'Educational content, not legal, financial or employment advice. <a href="%sdisclaimer.html">Disclaimer and trademark notice</a>.</p>'
         '<p><a href="%s" target="_blank" rel="noopener">Interested in this website or domain? Contact the owner</a></p></div></div></footer>') % (p, OWNER_CONTACT)

def head(path, title, desc, *, ads=True, schema=None, og_type="website", noindex=False, extra_head=""):
    canon = SITE_URL + "/" + ("" if path == "index.html" else path.replace("index.html", ""))
    full_title = title if title.startswith(NAME) else title + " | " + NAME
    depth = path.count("/")
    p = "../" * depth
    out = ['<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">' + extra_head,
           '<meta name="viewport" content="width=device-width, initial-scale=1">',
           '<title>%s</title>' % esc(full_title),
           '<meta name="description" content="%s">' % esc(desc),
           '<link rel="canonical" href="%s">' % esc(canon)]
    if noindex: out.append('<meta name="robots" content="noindex, follow">')
    out += ['<meta name="google-adsense-account" content="%s">' % ADS_CLIENT,
            '<meta name="theme-color" content="#1D2433">',
            '<meta property="og:site_name" content="Glasscliff">',
            '<meta property="og:type" content="%s">' % og_type,
            '<meta property="og:title" content="%s">' % esc(title),
            '<meta property="og:description" content="%s">' % esc(desc),
            '<meta property="og:url" content="%s">' % esc(canon),
            '<meta property="og:image" content="%s/assets/img/og.png">' % SITE_URL,
            '<meta name="twitter:card" content="summary_large_image">',
            '<link rel="icon" href="%sassets/img/favicon.svg" type="image/svg+xml">' % p,
            '<link rel="manifest" href="%ssite.webmanifest">' % p,
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
            '<link rel="stylesheet" href="%s">' % FONTS,
            '<link rel="stylesheet" href="%sassets/css/site.css">' % p]
    if ads: out.append(ADSENSE_TAG)
    if schema:
        for s in (schema if isinstance(schema, list) else [schema]):
            out.append('<script type="application/ld+json">%s</script>' % json.dumps(s, ensure_ascii=False))
    out.append('</head>')
    return "".join(out)

def layout(path, title, desc, body, *, active=None, ads=True, schema=None, og_type="website", noindex=False,
           sticky=True, scripts=(), keywords="", priority="0.6", changefreq="monthly", search=True, extra_head=""):
    depth = path.count("/")
    p = "../" * depth
    page = head(path, title, desc, ads=ads, schema=schema, og_type=og_type, noindex=noindex, extra_head=extra_head)
    page += '<body data-root="%s"%s>' % (p, ' class="has-sticky"' if sticky else "")
    page += header(p, active)
    page += '<main id="main">' + body.replace("{{p}}", p) + '</main>'
    page += footer(p)
    if sticky:
        page += '<a class="btn btn-risk sticky-cta" href="%sget-help.html">Get a confidential review</a>' % p
    page += '<script src="%sassets/js/config.js"></script><script src="%sassets/js/main.js"></script>' % (p, p)
    for s in scripts:
        page += '<script src="%sassets/js/%s"></script>' % (p, s)
    page += '</body></html>'
    if not noindex:
        PAGES.append(dict(path=path, title=title, desc=desc, keywords=keywords, priority=priority, changefreq=changefreq, search=search))
    write(path, page)

def write(path, content):
    full = os.path.join(ROOT_DIR, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

# ---------- small components ----------
def crumbs(items):
    """items: list of (href or None, label). hrefs are relative with {{p}}."""
    parts = []
    for href, label in items:
        parts.append('<a href="%s">%s</a>' % (href, esc(label)) if href else '<span aria-current="page">%s</span>' % esc(label))
    return '<nav class="crumbs" aria-label="Breadcrumb">' + '<span aria-hidden="true">/</span>'.join(parts) + '</nav>'

def crumb_schema(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE_URL + "/" + u} for i, (u, n) in enumerate(items)]}

def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

def faq_html(faqs, heading="Frequently asked questions"):
    return ('<section class="faq" aria-labelledby="faq-h"><h2 id="faq-h">%s</h2>' % heading +
            "".join('<details><summary>%s</summary><div><p>%s</p></div></details>' % (esc(q), esc(a)) for q, a in faqs) + '</section>')

def field(name, label, kind="text", required=True, opt_label=False, placeholder="", autocomplete="", attrs=""):
    req = " required" if required else ""
    lab = esc(label) + (' <span class="opt">(optional)</span>' if not required else "")
    ac = ' autocomplete="%s"' % autocomplete if autocomplete else ""
    ph = ' placeholder="%s"' % esc(placeholder) if placeholder else ""
    fid = "f-" + name.replace("[]", "")
    if kind == "textarea":
        ctl = '<textarea id="%s" name="%s"%s%s %s></textarea>' % (fid, name, req, ph, attrs)
    else:
        ctl = '<input id="%s" type="%s" name="%s"%s%s%s %s>' % (fid, kind, name, req, ac, ph, attrs)
    return '<div class="field"><label for="%s">%s</label>%s<span class="err" aria-live="polite"></span></div>' % (fid, lab, ctl)

def select(name, label, options, required=True):
    req = " required" if required else ""
    fid = "f-" + name
    lab = esc(label) + (' <span class="opt">(optional)</span>' if not required else "")
    opts = '<option value="">Choose one</option>' + "".join('<option>%s</option>' % esc(o) for o in options)
    return '<div class="field"><label for="%s">%s</label><select id="%s" name="%s"%s>%s</select><span class="err" aria-live="polite"></span></div>' % (fid, lab, fid, name, req, opts)

def choices(name, legend, options, kind="radio", required=True):
    req = " required" if required and kind == "radio" else ""
    items = "".join('<label class="choice"><input type="%s" name="%s" value="%s"%s><span>%s%s</span></label>' % (
        kind, name, esc(v), req, esc(t), ('<small>%s</small>' % esc(s)) if s else "") for v, t, s in options)
    return '<fieldset class="field" style="border:0;padding:0;margin:0 0 1rem"><legend class="legend">%s</legend><div class="choices">%s</div><span class="err" aria-live="polite"></span></fieldset>' % (esc(legend), items)

def consent(text="I agree that Glasscliff may use these details to respond to me, as described in the privacy policy."):
    return ('<div class="field"><label class="check"><input type="checkbox" name="consent" value="yes" required> <span>%s</span></label><span class="err" aria-live="polite"></span></div>' % esc(text) +
            '<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">')
