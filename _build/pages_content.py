# Content pages: home, guides, research, glossary, videos, news, search, about and legal pages.
import json, os, re
from datetime import datetime
from common import *
from refdata import STUDIES, TIMELINE, GLOSSARY, VIDEOS, SITE_FAQ
from guides_a import GUIDES_A
from guides_b import GUIDES_B

GUIDES = GUIDES_A + GUIDES_B
GUIDE_MAP = {g["slug"]: g for g in GUIDES}
TOOLS = [
 ("risk-scanner.html", "scanner", "Glass Cliff Risk Scanner", "Twelve questions about a role you are weighing. Get a 0–100 risk score, the red flags and what to negotiate.", "4 minutes"),
 ("offer-protection.html", "offer", "Offer Protection Builder", "Tick the risks in your offer and get a prioritised list of protections to ask for, ready to copy or print.", "2 minutes"),
 ("100-day-plan.html", "plan", "Turnaround 100-Day Planner", "Choose your situation and get a three-phase plan with weekly checkpoints, dated from your start day.", "3 minutes"),
 ("readiness-quiz.html", "ready", "Crisis Leadership Readiness Check", "Fifteen statements across five dimensions. See where you are strong and what to build before you start.", "5 minutes"),
 ("board-check.html", "board", "Board Appointment Check", "For chairs and search committees: twelve checks that show whether you are setting your next leader up to succeed.", "3 minutes"),
]

def words(html_s):
    return len(strip_tags(html_s).split())

def guide_link(slug, p="{{p}}"):
    g = GUIDE_MAP[slug]
    return '%sguides/%s.html' % (p, slug)

def guide_list(guides, p="{{p}}"):
    out = []
    for g in guides:
        mins = max(4, round(words(g["body"]) / 230))
        out.append('<li><a href="%sguides/%s.html"><span class="g-title">%s</span><span class="g-desc">%s</span><span class="g-meta">%s<br>%d min read</span></a></li>' % (
            p, g["slug"], esc(g["title"]), esc(g["dek"]), esc(g["audience"]), mins))
    return '<ul class="guide-list">' + "".join(out) + '</ul>'

def instruments(p="{{p}}"):
    return '<div class="instruments">' + "".join(
        '<a class="instrument" href="%stools/%s">%s<div><h3>%s</h3><p>%s</p><span class="meta">Free, about %s</span></div></a>' % (p, f, ICONS[i], esc(t), esc(d), m)
        for f, i, t, d, m in TOOLS) + '<a class="instrument next" href="%sget-help.html"><div><h3>Want a person to look at it?</h3><p>Share your results with an experienced adviser through a confidential review.</p><span class="meta" style="color:var(--glass)">Confidential and free to request</span></div></a></div>' % p

def video_figure(v, p="{{p}}"):
    kind, vid, title, who, blurb = v
    if kind == "yt":
        poster = '<img src="https://i.ytimg.com/vi/%s/hqdefault.jpg" alt="" loading="lazy" width="480" height="360">' % vid
        btn = '<button type="button" data-yt="%s" aria-label="Play video: %s"><span></span></button>' % (vid, esc(title))
    else:
        poster = ('<svg viewBox="0 0 480 270" aria-hidden="true" style="width:100%%;height:100%%"><rect width="480" height="270" fill="#2B3447"/>'
                  '<path d="M0 200 L140 186 L250 198 L320 190 L320 270 L0 270Z" fill="#3A4459"/><rect x="300" y="182" width="150" height="8" fill="#9FD3D6" opacity=".7"/>'
                  '<text x="24" y="48" fill="#fff" font-family="Schibsted Grotesk, sans-serif" font-size="22" font-weight="700">%s</text>'
                  '<text x="24" y="76" fill="#BFC8C7" font-family="Schibsted Grotesk, sans-serif" font-size="15">%s</text></svg>') % (esc(title), esc(who))
        btn = '<button type="button" data-ted="%s" aria-label="Play video: %s"><span></span></button>' % (vid, esc(title))
    return '<figure class="video"><div class="video-frame">%s%s</div><figcaption><b>%s</b><span>%s. %s</span></figcaption></figure>' % (poster, btn, esc(title), esc(who), esc(blurb))

def load_news():
    path = os.path.join(ROOT_DIR, "data", "news.json")
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"updated": None, "items": []}

def news_items_html(items, limit):
    out = []
    for it in items[:limit]:
        try:
            when = datetime.fromisoformat(it["date"].replace("Z", "+00:00")).strftime("%b %d, %Y")
        except Exception:
            when = ""
        out.append('<li><a href="%s" target="_blank" rel="noopener nofollow">%s</a><span class="src">%s%s</span></li>' % (
            esc(it["link"]), esc(it["title"]), esc(it.get("source", "")), (", " + when) if when else ""))
    if not out:
        out.append('<li>Headlines load here each day. <a href="{{p}}news.html">Open the news page</a>.</li>')
    return "".join(out)

# ---------------- Home ----------------
def build_home():
    news = load_news()
    tl = [t for t in TIMELINE if t[0] in ("2005", "2010", "2013–14", "2020", "2025")]
    faqs = SITE_FAQ[:5]
    body = '''
<section class="hero"><div class="wrap hero-grid">
<div>
<h1>Is this role a glass cliff?</h1>
<p class="lede">Some leadership roles are offered when the odds are worst. Glasscliff helps you weigh a high-stakes role before you accept it, and helps boards appoint leaders without setting them up to fail.</p>
<div class="btn-row"><a class="btn btn-primary" href="{{p}}tools/risk-scanner.html">Scan a role for risk</a><a class="btn btn-line" href="{{p}}guides/what-is-the-glass-cliff.html">Read the guide</a></div>
<form id="edge-test" class="edge-test" aria-labelledby="edge-h">
<h2 id="edge-h">Quick edge test</h2>
<fieldset><legend class="sr">Three questions about the role</legend>
<div class="edge-q"><span>Is the organisation already in crisis?</span><span class="toggle"><input type="radio" id="c-y" name="crisis" value="yes"><label for="c-y">Yes</label><input type="radio" id="c-n" name="crisis" value="no" checked><label for="c-n">No</label></span></div>
<div class="edge-q"><span>Is your mandate in writing?</span><span class="toggle"><input type="radio" id="m-y" name="mandate" value="yes" checked><label for="m-y">Yes</label><input type="radio" id="m-n" name="mandate" value="no"><label for="m-n">No</label></span></div>
<div class="edge-q"><span>Do new resources come with the role?</span><span class="toggle"><input type="radio" id="r-y" name="resources" value="yes" checked><label for="r-y">Yes</label><input type="radio" id="r-n" name="resources" value="no"><label for="r-n">No</label></span></div>
</fieldset>
<div class="edge-read" aria-live="polite"><span class="edge-meter" aria-hidden="true"><i></i></span><span class="edge-label">Solid ground</span></div>
<p class="small" style="margin:.7rem 0 0"><a id="edge-link" href="{{p}}tools/risk-scanner.html">Run the full 12-question scan</a></p>
</form>
</div>
<div class="cliff-art">''' + HERO_ART + '''</div>
</div></section>
<div class="strata" aria-hidden="true"></div>

<section class="section"><div class="wrap">
<div class="section-head"><h2>Who Glasscliff is for</h2><p>The same risk looks different depending on which side of the table you sit.</p></div>
<div class="paths">
<div class="path"><h3>Leaders weighing a role</h3><p>You have been offered, or already hold, a senior role in an organisation that is struggling.</p><ul>
<li><a href="{{p}}guides/red-flags-in-a-leadership-offer.html">Twelve red flags in a leadership offer</a></li>
<li><a href="{{p}}guides/how-to-negotiate-a-turnaround-role.html">How to negotiate a turnaround role</a></li>
<li><a href="{{p}}tools/100-day-plan.html">Build your 100-day plan</a></li>
<li><a href="{{p}}get-help.html">Get a confidential review</a></li></ul></div>
<div class="path"><h3>Boards, CHROs and search panels</h3><p>You are appointing a leader in difficult conditions and want the appointment to work.</p><ul>
<li><a href="{{p}}guides/boards-appointing-a-crisis-leader.html">Appointing a crisis leader fairly</a></li>
<li><a href="{{p}}tools/board-check.html">Run the Board Appointment Check</a></li>
<li><a href="{{p}}guides/race-ethnicity-and-the-saviour-effect.html">The saviour effect</a></li>
<li><a href="{{p}}for-organizations.html">Request a Board Appointment Review</a></li></ul></div>
<div class="path"><h3>Students, researchers and journalists</h3><p>You need a clear, sourced account of what the evidence says, including where it disagrees.</p><ul>
<li><a href="{{p}}guides/glass-cliff-research-evidence.html">Twenty years of research</a></li>
<li><a href="{{p}}research.html">Research Library</a></li>
<li><a href="{{p}}glossary.html">Glossary</a></li>
<li><a href="{{p}}contests.html">Student Research Brief prize</a></li></ul></div>
</div></div></section>

<section class="section section-mist"><div class="wrap">
<div class="section-head"><h2>Free tools</h2><p>Each one runs in your browser. Nothing is sent anywhere unless you choose to.</p></div>
''' + instruments() + '''
</div></section>

<section class="section section-dark"><div class="wrap split">
<div><h2>Twenty years of evidence, in five moments</h2>
<p class="muted" style="color:#BFC8C7;font-family:var(--read)">The glass cliff is a research finding, not a slogan. It is also a live debate, and we cover both sides.</p>
<p><a href="{{p}}research.html">Explore the Research Library</a></p></div>
<ol class="timeline">''' + "".join('<li><time>%s</time><p>%s</p></li>' % (esc(y), esc(t)) for y, t in tl) + '''</ol>
</div></section>

<section class="section"><div class="wrap">
<div class="section-head"><h2>Guides</h2><p>Original, sourced and practical. Start with the first one if the term is new to you.</p></div>
''' + guide_list(GUIDES[:6]) + '''
<p style="margin-top:1.2rem"><a class="btn btn-line" href="{{p}}guides/">All ten guides</a></p>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap">
<div class="lead-band">
<div><h2>Weighing a role that could go either way?</h2>
<p>Tell us about the situation in confidence. We match you with an experienced executive coach, employment lawyer or turnaround adviser for an initial conversation.</p>
<a class="btn btn-primary" href="{{p}}get-help.html">Get a confidential review</a></div>
<ul class="promise"><li>Confidential. No names of organisations needed.</li><li>Reply <span data-reply-time>within two business days</span>.</li><li>Advisers vetted for crisis and turnaround experience.</li><li>Free to request. You agree any fees directly with the adviser.</li></ul>
</div></div></section>

<section class="section section-mist"><div class="wrap split">
<div><div class="section-head"><h2>Leadership news</h2></div>
<ul class="news-list" data-news="6">''' + news_items_html(news.get("items", []), 6) + '''</ul>
<p class="small" style="margin-top:1rem"><a href="{{p}}news.html">More headlines, updated daily</a></p></div>
<div><div style="background:var(--basalt);color:#E7ECEB;border-radius:var(--radius-l);padding:1.6rem">
<p class="note-of-day" data-note-of-day>The board sponsor matters more than the title. Name yours before you sign.<cite>Edge note of the day</cite></p></div>
<div style="margin-top:1.4rem">''' + video_figure(VIDEOS[0]) + '''</div>
<p class="small"><a href="{{p}}videos.html">Watch all eight videos</a></p></div>
</div></section>

<section class="section"><div class="wrap">
<div class="section-head"><h2>Take part</h2><p>Glasscliff is independent and reader-supported. Here is how to get involved.</p></div>
<div class="paths">
<div class="path"><h3>Win the Edge Prize</h3><p>Quarterly prizes for turnaround cases, student research and leadership stories. Current round closes in:</p><div class="countdown" data-countdown="0"></div><p style="margin-top:.8rem"><a href="{{p}}contests.html">See prizes and rules</a></p></div>
<div class="path"><h3>Join the Advisor Network</h3><p>Executive coaches, employment lawyers and interim leaders who help people through high-stakes roles.</p><p><a href="{{p}}advisors.html">Apply to join</a></p><h3 style="margin-top:1.2rem">Share your experience</h3><p>Ten anonymous questions for the Glass Cliff Pulse report.</p><p><a href="{{p}}survey.html">Take the survey</a></p></div>
<div class="path"><h3>Support the work</h3><p>Reader support funds research, tools, promotion, new contributors and prizes.</p><p><a class="btn btn-dark btn-sm" href="{{p}}support.html">Support Glasscliff</a></p><h3 style="margin-top:1.2rem">Work with us</h3><p><a href="{{p}}careers.html">Open roles</a> and <a href="{{p}}advertise.html">sponsorship packages</a>.</p></div>
</div></div></section>

<section class="section section-mist"><div class="wrap narrow">''' + faq_html(faqs) + '''<p style="margin-top:1rem"><a href="{{p}}faq.html">All questions</a></p></div></section>
'''
    schema = [
        {"@context": "https://schema.org", "@type": "Organization", "name": "Glasscliff", "url": SITE_URL, "logo": SITE_URL + "/assets/img/favicon.svg",
         "description": "Independent guide to high-stakes leadership roles and the glass cliff."},
        {"@context": "https://schema.org", "@type": "WebSite", "name": "Glasscliff", "url": SITE_URL,
         "potentialAction": {"@type": "SearchAction", "target": SITE_URL + "/search.html?q={search_term_string}", "query-input": "required name=search_term_string"}},
        faq_schema(faqs)]
    layout("index.html", "Glasscliff: is this leadership role a glass cliff?",
           "The independent guide to the glass cliff and high-stakes leadership roles. Free risk scanner, negotiation tools, research and confidential advice for leaders and boards.",
           body, schema=schema, keywords="glass cliff home leaders boards", priority="1.0", changefreq="daily")

# ---------------- Guides ----------------
def toc_from(body):
    return re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body)

def build_guides():
    groups = [("Start here", ["what-is-the-glass-cliff", "glass-ceiling-vs-glass-cliff", "glass-cliff-research-evidence"]),
              ("For leaders weighing or starting a role", ["red-flags-in-a-leadership-offer", "how-to-negotiate-a-turnaround-role", "first-100-days-turnaround-role", "is-a-crisis-role-a-career-accelerator"]),
              ("For boards and appointing panels", ["boards-appointing-a-crisis-leader", "race-ethnicity-and-the-saviour-effect"]),
              ("Beyond business", ["glass-cliff-in-politics"])]
    body = ('<div class="wrap page-head">' + crumbs([("{{p}}index.html", "Home"), (None, "Guides")]) +
            '<h1>Guides to the glass cliff</h1><p class="dek">Ten original guides for leaders, boards and researchers. Each one is sourced, practical and updated as new research appears.</p></div>'
            '<div class="wrap" style="padding-bottom:64px">')
    for title, slugs in groups:
        body += '<section style="margin-top:2rem"><h2 style="font-size:var(--step-2)">%s</h2>%s</section>' % (esc(title), guide_list([GUIDE_MAP[s] for s in slugs]))
    body += '<section style="margin-top:3rem"><h2 style="font-size:var(--step-2)">Put the guides to work</h2><ul class="pill-list">' + \
            "".join('<li><a href="{{p}}tools/%s">%s</a></li>' % (f, esc(t)) for f, i, t, d, m in TOOLS) + '</ul></section></div>'
    layout("guides/index.html", "Glass cliff guides for leaders and boards",
           "Ten in-depth guides on the glass cliff: definitions, evidence, red flags, negotiation, the first 100 days, board governance, race and politics.",
           body, active="guides/", schema=crumb_schema([("", "Home"), ("guides/", "Guides")]), keywords="guides articles", priority="0.9", changefreq="weekly")
    for g in GUIDES:
        build_guide(g)

def build_guide(g):
    mins = max(4, round(words(g["body"]) / 230))
    path = "guides/%s.html" % g["slug"]
    toc = toc_from(g["body"])
    tags = "".join('<span class="tag">%s</span>' % esc(t) for t in g["tags"])
    cta_leader = "board" not in g["slug"]
    cta = ('<div class="lead-band" style="margin:2.4rem 0"><div><h2>%s</h2><p>%s</p><a class="btn btn-primary" href="{{p}}%s">%s</a></div>'
           '<ul class="promise"><li>Confidential</li><li>Vetted advisers</li><li>Free to request</li></ul></div>') % (
        ("Weighing a role like this?" if cta_leader else "Appointing a leader in difficult conditions?"),
        ("Get an experienced second opinion on the offer, the risks and what to negotiate." if cta_leader else "Get an independent review of the appointment, the package and the support around it."),
        ("get-help.html" if cta_leader else "for-organizations.html"),
        ("Get a confidential review" if cta_leader else "Request a Board Appointment Review"))
    summary = '<div class="summary-box"><h2>In short</h2><ul>' + "".join("<li>%s</li>" % esc(s) for s in g["summary"]) + '</ul></div>'
    sources = '<section class="sources"><h2 style="font-size:1.1rem">Sources and further reading</h2><ol>' + \
              "".join('<li>%s <a href="%s" target="_blank" rel="noopener">%s</a></li>' % (esc(t), esc(link(u)), "Find the paper" if u.startswith("scholar:") else "Link") for t, u in g["sources"]) + '</ol></section>'
    related = '<section style="margin-top:2rem"><h2 style="font-size:1.25rem">Read next</h2>' + guide_list([GUIDE_MAP[s] for s in g["related"]]) + '</section>'
    toc_html = '<nav class="toc" aria-label="On this page"><h2>On this page</h2><ol>' + "".join('<li><a href="#%s">%s</a></li>' % (i, t) for i, t in toc) + '<li><a href="#faq-h">Questions</a></li></ol></nav>'
    aside = toc_html + ('<div class="aside-cta"><h2>Score a real offer</h2><p>Twelve questions, four minutes, a clear list of what to negotiate.</p><a class="btn btn-primary btn-sm" href="{{p}}tools/risk-scanner.html">Open the Risk Scanner</a></div>' if cta_leader else
                        '<div class="aside-cta"><h2>Check your appointment</h2><p>Twelve yes-or-no checks for boards and panels.</p><a class="btn btn-primary btn-sm" href="{{p}}tools/board-check.html">Open the Board Check</a></div>')
    body = ('<article><div class="wrap article-head">' + crumbs([("{{p}}index.html", "Home"), ("{{p}}guides/", "Guides"), (None, g["title"])]) +
            '<div>%s</div><h1>%s</h1><p class="dek">%s</p>' % (tags, esc(g["title"]), esc(g["dek"])) +
            '<div class="byline"><span>By the Glasscliff editorial team</span><span>Updated <time datetime="%s">%s</time></span><span>%d minute read</span><span>For: %s</span></div></div>' % (
                UPDATED, datetime.fromisoformat(UPDATED).strftime("%-d %B %Y"), mins, esc(g["audience"])) +
            '<div class="wrap article-grid" style="padding-bottom:64px"><div class="prose">' + summary + g["body"] + cta +
            faq_html(g["faq"], "Questions") + sources + related + '</div><aside class="article-aside">' + aside + '</aside></div></article>')
    schema = [{"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["desc"],
               "datePublished": PUBLISHED, "dateModified": UPDATED, "author": {"@type": "Organization", "name": "Glasscliff editorial team"},
               "publisher": {"@type": "Organization", "name": "Glasscliff", "logo": {"@type": "ImageObject", "url": SITE_URL + "/assets/img/favicon.svg"}},
               "mainEntityOfPage": SITE_URL + "/" + path, "image": SITE_URL + "/assets/img/og.png"},
              crumb_schema([("", "Home"), ("guides/", "Guides"), (path, g["title"])]), faq_schema(g["faq"])]
    layout(path, g["title"], g["desc"], body.replace('href="../', 'href="{{p}}').replace('href="{{p}}tools', 'href="{{p}}tools'),
           active="guides/", schema=schema, og_type="article", keywords=" ".join(g["tags"]) + " " + strip_tags(" ".join(g["summary"]))[:200], priority="0.8")

# ---------------- Research, glossary, videos, news ----------------
def build_research():
    vt = {"yes": ("v-yes", "Supports"), "mixed": ("v-mixed", "Mixed or nuanced"), "no": ("v-no", "No effect found")}
    studies = "".join('<article class="study"><h3>%s</h3><p class="cite">%s. <i>%s</i>.</p><p><span class="verdict %s">%s</span>%s</p><p class="small"><a href="%s" target="_blank" rel="noopener">%s</a></p></article>' % (
        esc(t), esc(a), esc(j), vt[v][0], vt[v][1], esc(s), esc(link(u)), "Find the paper" if u.startswith("scholar:") else "Read the source") for a, t, j, v, s, u in STUDIES)
    body = ('<div class="wrap page-head">' + crumbs([("{{p}}index.html", "Home"), (None, "Research Library")]) +
            '<h1>Research Library</h1><p class="dek">The key studies on the glass cliff, from the 2005 paper that named it to the newest work in 2025, including the studies that found no effect.</p></div>'
            '<div class="wrap split" style="padding-bottom:64px"><div><h2>Studies</h2><p class="muted">Each entry is summarised in our own words. Labels show whether a study supports the glass cliff, finds a nuanced result, or finds no effect.</p>' + studies +
            '</div><div><div style="position:sticky;top:88px"><h2>Timeline</h2><ol class="timeline">' + "".join('<li><time>%s</time><p>%s</p></li>' % (esc(y), esc(t)) for y, t in TIMELINE) +
            '</ol><div class="callout"><b>Reading the evidence</b>For a narrative account of what these studies add up to, read <a href="{{p}}guides/glass-cliff-research-evidence.html">Twenty years of glass cliff research</a>.</div>'
            '<div class="aside-cta"><h2>Researching the glass cliff?</h2><p>Students can win a prize and publication for a 1,500-word research brief.</p><a class="btn btn-primary btn-sm" href="{{p}}contests.html">See the Student Research Brief</a></div></div></div></div>')
    layout("research.html", "Glass cliff Research Library: key studies 2005–2025",
           "Annotated library of glass cliff research: Ryan & Haslam 2005, Cook & Glass, the 2020 meta-analysis, null findings and new 2025 studies, with a timeline.",
           body, active="research.html", schema=crumb_schema([("", "Home"), ("research.html", "Research Library")]), keywords="studies papers evidence meta-analysis timeline", priority="0.8")

def build_glossary():
    letters = sorted(set(t[0][0].upper() for t in GLOSSARY))
    az = '<nav class="az" aria-label="Jump to letter">' + "".join('<a href="#l-%s">%s</a>' % (l, l) for l in letters) + '</nav>'
    dl, seen = "", set()
    for term, d in sorted(GLOSSARY):
        L = term[0].upper()
        anchor = ' id="l-%s"' % L if L not in seen else ""
        seen.add(L)
        slug = re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")
        dl += '<dt%s><span id="%s"></span>%s</dt><dd>%s</dd>' % (anchor, slug, esc(term), esc(d))
    body = ('<div class="wrap page-head">' + crumbs([("{{p}}index.html", "Home"), (None, "Glossary")]) +
            '<h1>Glossary</h1><p class="dek">%d terms used in research and practice on leadership barriers, crisis roles and executive appointments.</p>%s</div>' % (len(GLOSSARY), az) +
            '<div class="wrap" style="padding-bottom:64px"><dl class="glossary">' + dl + '</dl>'
            '<p style="margin-top:2rem">For how these terms fit together, read <a href="{{p}}guides/glass-ceiling-vs-glass-cliff.html">Glass ceiling, glass cliff, glass escalator, broken rung</a>.</p></div>')
    schema = {"@context": "https://schema.org", "@type": "DefinedTermSet", "name": "Glasscliff glossary",
              "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d} for t, d in GLOSSARY]}
    layout("glossary.html", "Glossary of leadership barriers: glass cliff, ceiling, escalator and more",
           "Definitions of the glass cliff, glass ceiling, glass escalator, broken rung, saviour effect, mandate letter and other leadership terms.",
           body, schema=[schema, crumb_schema([("", "Home"), ("glossary.html", "Glossary")])], keywords=" ".join(t for t, d in GLOSSARY), priority="0.7")

def build_videos():
    body = ('<div class="wrap page-head">' + crumbs([("{{p}}index.html", "Home"), (None, "Videos")]) +
            '<h1>Video library</h1><p class="dek">Talks and short courses on the glass cliff and on leading through a crisis, chosen by our editors. Videos play from YouTube and TED; nothing loads until you press play.</p></div>'
            '<div class="wrap" style="padding-bottom:64px"><div class="videos">' + "".join(video_figure(v) for v in VIDEOS) + '</div>'
            '<p class="small muted" style="margin-top:2rem">Videos are embedded with each platform\'s own player and remain the property of their creators. YouTube videos use privacy-enhanced mode. Suggest a video through the <a href="{{p}}contact.html">contact form</a>.</p></div>')
    schema = [{"@context": "https://schema.org", "@type": "VideoObject", "name": t, "description": b, "thumbnailUrl": "https://i.ytimg.com/vi/%s/hqdefault.jpg" % i,
               "embedUrl": "https://www.youtube-nocookie.com/embed/%s" % i, "uploadDate": "2021-01-01"} for k, i, t, w, b in VIDEOS if k == "yt"][:3]
    layout("videos.html", "Videos on the glass cliff and crisis leadership",
           "Watch talks on the glass cliff by Sophie Williams, crisis leadership by Amy Edmondson, IMD and Stanford GSB, and why the glass ceiling metaphor misleads.",
           body, active="videos.html", keywords="video talk TED TEDx crisis leadership", priority="0.7")

def build_news():
    news = load_news()
    upd = news.get("updated")
    upd_txt = datetime.fromisoformat(upd.replace("Z", "+00:00")).strftime("%-d %B %Y, %H:%M UTC") if upd else "daily"
    body = ('<div class="wrap page-head">' + crumbs([("{{p}}index.html", "Home"), (None, "Leadership news")]) +
            '<h1>Leadership news</h1><p class="dek">Headlines on the glass cliff, crisis appointments, CEO turnover and board diversity, gathered automatically every day from Google News.</p>'
            '<p class="small muted">Last updated: <span data-news-updated>%s</span></p></div>' % esc(upd_txt) +
            '<div class="wrap split" style="padding-bottom:64px"><div><ul class="news-list" data-news="30">' + news_items_html(news.get("items", []), 30) + '</ul></div>'
            '<div><div class="callout"><b>How this page works</b>A scheduled job searches Google News each morning for a fixed set of leadership topics and lists the headlines with links to the original publishers. We do not copy or summarise articles, and a headline here is not an endorsement.</div>'
            '<div class="aside-cta"><h2>Make sense of the headlines</h2><p>Every crisis appointment raises the same questions. Our guides answer them.</p><a class="btn btn-primary btn-sm" href="{{p}}guides/">Read the guides</a></div></div></div>')
    layout("news.html", "Leadership news: crisis appointments and the glass cliff",
           "Daily headlines on the glass cliff, CEO and leader appointments in crisis, interim leaders and board diversity, with links to the original publishers.",
           body, keywords="news headlines appointments CEO", priority="0.6", changefreq="daily")

def build_search():
    body = ('<div class="wrap page-head">' + crumbs([("{{p}}index.html", "Home"), (None, "Search")]) +
            '<h1>Search</h1><p class="dek">Search guides, tools, the glossary and every page on Glasscliff.</p></div>'
            '<div class="wrap narrow" style="padding-bottom:64px"><form role="search" onsubmit="return false"><label class="sr" for="site-search">Search the site</label>'
            '<input id="site-search" type="search" placeholder="Try: negotiate, board, saviour effect" autocomplete="off"></form><ul id="search-results" class="search-results" aria-live="polite"></ul></div>')
    layout("search.html", "Search Glasscliff", "Search Glasscliff's guides, tools, research library and glossary.", body, keywords="search", priority="0.3", search=False)

def build_faq():
    body = ('<div class="wrap page-head">' + crumbs([("{{p}}index.html", "Home"), (None, "FAQ")]) +
            '<h1>Frequently asked questions</h1><p class="dek">About Glasscliff, our tools, advice, advertising and your data.</p></div>'
            '<div class="wrap narrow" style="padding-bottom:64px">' + faq_html(SITE_FAQ, "Questions and answers") +
            '<h2 style="margin-top:2.4rem;font-size:var(--step-2)">About the glass cliff itself</h2>' +
            "".join(faq_html(GUIDE_MAP["what-is-the-glass-cliff"]["faq"], "").replace('<h2 id="faq-h"></h2>', "").replace('aria-labelledby="faq-h"', 'aria-label="Glass cliff questions"')) +
            '<p style="margin-top:2rem">Still have a question? <a href="{{p}}contact.html">Contact us</a>.</p></div>')
    layout("faq.html", "FAQ", "Answers to common questions about Glasscliff, the glass cliff, our free tools, confidential reviews, advertising and privacy.",
           body, schema=faq_schema(SITE_FAQ + GUIDE_MAP["what-is-the-glass-cliff"]["faq"]), keywords="questions help", priority="0.6")

# ---------------- About & legal ----------------
def simple(path, title, desc, h1, dek, inner, *, kw="", pri="0.4", ads=True, active=None):
    body = ('<div class="wrap page-head">' + crumbs([("{{p}}index.html", "Home"), (None, h1)]) + '<h1>%s</h1>%s</div>' % (esc(h1), ('<p class="dek">%s</p>' % dek) if dek else "") +
            '<div class="wrap" style="padding-bottom:64px"><div class="prose">' + inner + '</div></div>')
    layout(path, title, desc, body, ads=ads, active=active, keywords=kw, priority=pri)

def build_about_legal():
    simple("about.html", "About Glasscliff", "Glasscliff is an independent publication and toolkit for leaders taking on high-stakes roles and the boards that appoint them.",
        "About Glasscliff", "An independent guide to high-stakes leadership roles, built on the research and on practical experience of crisis appointments.", '''
<h2 id="why">Why we exist</h2>
<p>In 2005, researchers Michelle Ryan and Alex Haslam gave a name to something many leaders had felt: the top job that arrives only when the organisation is already in trouble. Twenty years later, the glass cliff is widely discussed but rarely made practical. Most writing about it stops at the definition.</p>
<p>Glasscliff starts where the definition stops. We help leaders assess a specific role, negotiate the conditions they need, and plan their first 100 days. We help boards appoint leaders to difficult roles without setting them up to fail. And we keep an honest, sourced record of what the research does and does not show.</p>
<h2 id="what">What we do</h2>
<ul><li><b>Guides</b> written from the research and checked against primary sources.</li><li><b>Free tools</b> that run in your browser: the Risk Scanner, Offer Protection Builder, 100-Day Planner, Readiness Check and Board Appointment Check.</li><li><b>Confidential reviews</b> that connect leaders and organisations with vetted advisers.</li><li><b>The Edge Prize</b>, recognising turnaround cases, student research and leadership stories.</li><li><b>The Glass Cliff Pulse</b>, an anonymous survey of people who have held high-stakes roles.</li></ul>
<h2 id="independence">Independence and funding</h2>
<p>Glasscliff is funded by advertising (Google AdSense), labelled sponsorships, Advisor Network listings, referral fees from advisers, and reader support. Sponsors and advertisers never see or shape editorial content before publication. We are not affiliated with the researchers we cite, their universities, or any company or product with a similar name. Read our <a href="editorial-policy.html">editorial policy</a> and <a href="disclaimer.html">disclaimer</a>.</p>
<h2 id="principles">Our principles</h2>
<ul><li><b>Evidence first.</b> We link to sources and report studies that disagree.</li><li><b>Patterns, not people.</b> We do not label named individuals as glass cliff cases.</li><li><b>Useful over clever.</b> Every page should help someone make a better decision.</li><li><b>Your data stays yours.</b> Tools run locally; forms are used only to respond to you.</li></ul>
<h2 id="contact">Get in touch</h2>
<p>Use the <a href="contact.html">contact page</a> for questions and corrections. If you are interested in this website, the Glasscliff.com domain, sponsorship, advertising or a partnership, <a href="https://web.works/contact" target="_blank" rel="noopener">contact the owner</a>.</p>''', kw="mission independence funding", pri="0.5")

    simple("editorial-policy.html", "Editorial policy", "How Glasscliff researches, writes, sources, corrects and separates sponsored content from editorial.",
        "Editorial policy", "How we decide what to publish, and how you can hold us to it.", '''
<h2 id="sourcing">Sourcing</h2><p>Factual claims about research link to the original study, a publisher's page or a recognised summary. Where we could not verify a detail, we leave it out. We summarise studies in our own words and quote sparingly.</p>
<h2 id="balance">Balance</h2><p>The glass cliff is debated. When studies disagree, we say so, and we include null findings in the <a href="research.html">Research Library</a>.</p>
<h2 id="people">Named individuals</h2><p>We discuss patterns across many appointments. We do not describe any named living person as a "glass cliff case", because that judgement requires facts about their appointment that are rarely public.</p>
<h2 id="tools">Tools</h2><p>Our tools turn research findings and widely used governance practice into structured questions. Their scores are a starting point for a conversation, not a prediction.</p>
<h2 id="sponsors">Sponsored content and advertising</h2><p>Ads are served by Google AdSense and are clearly separate from our content. Sponsored placements are labelled "Sponsored" or "Supported by". Sponsors do not review editorial content before publication.</p>
<h2 id="corrections">Corrections</h2><p>Report an error through the <a href="contact.html">contact form</a> and choose "Correction". We review every report and note significant corrections on the page.</p>
<h2 id="ai">Use of software tools</h2><p>We may use software, including AI tools, to help research and draft. Every page is reviewed against its sources before publication, and editors are responsible for what we publish.</p>''', kw="sourcing corrections sponsors", pri="0.3")

    simple("privacy.html", "Privacy policy", "How Glasscliff collects, uses and protects information, including cookies and Google AdSense advertising.",
        "Privacy policy", "Last updated 12 November 2026.", '''
<h2 id="summary">Summary</h2><p>Our tools run in your browser and do not send your answers anywhere. When you submit a form, we receive what you typed so we can respond. We use cookies for basic site functions and Google uses cookies to serve and measure ads.</p>
<h2 id="collect">Information we collect</h2><ul><li><b>Form submissions</b> (name, email, and what you choose to tell us), delivered to our team by email through the FormSubmit service.</li><li><b>Basic attribution</b> attached to forms: the page you submitted from, the first page you visited, the referring site and any campaign (UTM) tags.</li><li><b>Tool answers</b> saved only in your own browser's local storage so you can return to them. You can clear them at any time by clearing your browser data.</li></ul>
<h2 id="use">How we use it</h2><p>Only to respond to you, provide the service you asked for (for example, a confidential review or a prize entry), and improve the site. With your consent, we may share the details of a review request with the adviser we match you with. We do not sell personal information.</p>
<h2 id="cookies">Cookies and advertising</h2><p>Third-party vendors, including Google, use cookies to serve ads based on your prior visits to this website or other websites. Google's use of advertising cookies enables it and its partners to serve ads to you based on your visits to this and/or other sites on the Internet.</p><p>You may opt out of personalised advertising by visiting <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener">Google Ads Settings</a>, or opt out of some third-party vendors' use of cookies for personalised advertising at <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener">www.aboutads.info</a>. Learn more about <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">how Google uses information from sites that use its services</a>.</p><p>Visitors in the European Economic Area, the United Kingdom and Switzerland are asked for consent through a Google-certified consent message before personalised ads are shown.</p>
<h2 id="third">Third-party services</h2><ul><li>Google AdSense (advertising) and Google Fonts (typefaces).</li><li>FormSubmit (form delivery).</li><li>YouTube and TED (video playback, only after you press play; YouTube runs in privacy-enhanced mode).</li><li>GitHub Pages (hosting).</li></ul>
<h2 id="rights">Your rights</h2><p>You can ask us to access, correct or delete information you have sent us. Use the <a href="contact.html">contact form</a> and choose "Privacy request". We keep form submissions only as long as needed to respond and for reasonable record-keeping, and no longer than 24 months.</p>
<h2 id="children">Children</h2><p>Glasscliff is intended for adults and is not directed at children under 16.</p>
<h2 id="changes">Changes</h2><p>We will update this page if our practices change and revise the date above.</p>''', kw="privacy cookies adsense data", pri="0.3")

    simple("terms.html", "Terms of use", "The terms that apply to using Glasscliff.com, its tools, forms, prizes and content.",
        "Terms of use", "Last updated 12 November 2026.", '''
<h2 id="use">Using the site</h2><p>You may read, share links to and use Glasscliff for personal and internal business purposes. Please do not copy substantial parts of our content without permission.</p>
<h2 id="advice">No professional advice</h2><p>Content and tools are educational. They are not legal, financial, employment or medical advice. Consult a qualified professional before making decisions about a contract or your career.</p>
<h2 id="tools">Tool results</h2><p>Scores and plans are generated from your answers by simple rules. They do not predict the outcome of any role or appointment.</p>
<h2 id="advisers">Advisers</h2><p>Advisers in the Advisor Network are independent. Any engagement and fees are agreed directly between you and the adviser. We are not a party to that agreement and are not responsible for advisers' services, although we act on complaints.</p>
<h2 id="submissions">Submissions and prizes</h2><p>By submitting an entry, story or survey response, you confirm it is your own and grant us a non-exclusive licence to publish it (anonymously where you ask). Prize rules on the Edge Prize page apply to entries.</p>
<h2 id="support">Support payments</h2><p>Support and pledges are voluntary contributions to running the site, not charitable donations, unless stated otherwise. They are non-refundable except where required by law or where a payment was made in error.</p>
<h2 id="links">Links</h2><p>We link to external sites for reference. We are not responsible for their content.</p>
<h2 id="liability">Liability</h2><p>To the extent permitted by law, Glasscliff is not liable for losses arising from use of the site or reliance on its content.</p>
<h2 id="changes">Changes</h2><p>We may update these terms. Continued use of the site means you accept the current version.</p>''', kw="terms conditions", pri="0.3")

    simple("disclaimer.html", "Disclaimer and trademark/copyright notice", "Glasscliff's disclaimer and trademark and copyright disclosure: independent publication, descriptive use of 'glass cliff', third-party marks and content.",
        "Disclaimer and trademark notice", "Please read this before relying on anything on Glasscliff.com.", '''
<h2 id="trademark">Trademark and name disclosure</h2>
<p>"Glass cliff" is a descriptive academic term coined by researchers Michelle K. Ryan and S. Alexander Haslam in 2005 to describe a pattern in leadership appointments. Glasscliff.com uses the term descriptively, as the subject of this publication and as the name of this website and domain.</p>
<p>Glasscliff.com is an independent publication. It is <b>not affiliated with, endorsed by or sponsored by</b> the researchers named above, their universities, any publisher, or any company, product, brand, film, book or person that uses the names "Glasscliff", "Glass Cliff", "Glass-Cliff" or any similar name. No such affiliation should be inferred.</p>
<p>All other names, logos, trademarks and brands mentioned on this site (including those of universities, journals, media organisations, video platforms and companies) are the property of their respective owners and are used only to identify and refer to them. Their mention does not imply endorsement.</p>
<h2 id="copyright">Copyright disclosure</h2>
<ul><li>All original text, tools, code, illustrations and design on Glasscliff.com are &copy; Glasscliff.com unless stated otherwise.</li><li>Research is cited and summarised in our own words; we link to original sources and do not reproduce papers.</li><li>Videos are embedded through YouTube's and TED's own players and remain the property of their creators and platforms.</li><li>News headlines link to the original publishers; we do not copy articles.</li><li>We use no third-party logos or photographs. Illustrations are original.</li></ul>
<p>If you believe content on this site infringes your rights, use the <a href="contact.html">contact form</a> and choose "Copyright or trademark". We respond promptly and remove material where appropriate.</p>
<h2 id="advice">Not professional advice</h2>
<p>Everything on Glasscliff is for general education. It is not legal, financial, employment, tax or medical advice, and it does not create a professional relationship. Tool scores are indicative only.</p>
<h2 id="accuracy">Accuracy</h2>
<p>We work hard to be accurate and to cite sources, but research evolves and errors happen. Check important points against the original sources and with qualified advisers.</p>
<h2 id="ads">Advertising and affiliate relationships</h2>
<p>The site displays ads served by Google AdSense. We may receive referral fees from advisers in the Advisor Network. Sponsored placements are labelled. None of these relationships affect our editorial judgement.</p>
<h2 id="owner">Ownership enquiries</h2>
<p>For enquiries about this website, the Glasscliff.com domain name, sponsorship, advertising or partnership, <a href="https://web.works/contact" target="_blank" rel="noopener">contact the owner</a>.</p>''', kw="disclaimer trademark copyright", pri="0.3")

def build_utility():
    # thank-you and 404: no ads (no publisher content), noindex
    def plain(path, title, inner):
        body = '<div class="wrap thanks"><div>' + inner + '</div></div>'
        layout(path, title, title, body, ads=False, noindex=True, sticky=False)
    plain("thank-you.html", "Thank you", '<h1 style="max-width:none">Received. Thank you.</h1><p class="dek" style="font-family:var(--read);font-size:1.2rem">We reply <span data-reply-time>within two business days</span>. Check your spam folder if you do not hear from us.</p>'
          '<div class="btn-row" style="justify-content:center;margin-top:1.4rem"><a class="btn btn-primary" href="{{p}}tools/">Explore the tools</a><a class="btn btn-line" href="{{p}}guides/">Read the guides</a></div>')
    base = "<script>document.write('<base href=\"'+(location.pathname.indexOf('/glasscliff-com/')===0?'/glasscliff-com/':'/')+'\">')</script>"
    body = ('<div class="wrap thanks"><div><h1 style="max-width:none">This page went over the edge.</h1><p class="dek" style="font-family:var(--read);font-size:1.2rem">The page you asked for does not exist or has moved.</p>'
            '<div class="btn-row" style="justify-content:center;margin-top:1.4rem"><a class="btn btn-primary" href="index.html">Go to the home page</a><a class="btn btn-line" href="search.html">Search the site</a></div></div></div>')
    layout("404.html", "Page not found", "Page not found", body, ads=False, noindex=True, sticky=False, extra_head=base)
