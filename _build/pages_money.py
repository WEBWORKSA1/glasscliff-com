# Lead generation and monetisation pages.
from common import *
from refdata import JOBS, AD_PACKAGES

COUNTRIES = ["United States", "Canada", "United Kingdom", "Ireland", "Australia", "New Zealand", "India", "Singapore", "United Arab Emirates", "Germany", "France", "Netherlands", "Nordics", "South Africa", "Nigeria", "Kenya", "Other"]
SECTORS = ["Corporate / listed company", "Private or PE-backed company", "Start-up or scale-up", "Non-profit or charity", "Public sector or government", "Politics", "Education or university", "Healthcare", "Sport", "Other"]

def page_head(h1, dek, crumb):
    return '<div class="wrap page-head">' + crumbs([("{{p}}index.html", "Home"), (None, crumb)]) + '<h1>%s</h1><p class="dek">%s</p></div>' % (esc(h1), dek)

def build_get_help():
    form = ('<form class="form-card" data-gc-form="confidential-review" data-subject="Confidential role review" data-steps data-score data-redirect="thank-you.html?f=review" id="review-form">'
            '<ol class="steps-bar"><li>Situation</li><li>The role</li><li>Help</li><li>Contact</li></ol>'
            '<input type="hidden" name="tool"><input type="hidden" name="tool_score">'
            '<section class="step"><h2 style="font-size:1.3rem">Your situation</h2>' +
            choices("path", "Which describes you?", [("leader", "I am weighing or holding a high-stakes role", ""), ("organisation", "We are appointing or supporting a leader", "Board, CHRO, search panel or sponsor")]) +
            choices("timeline", "Where are you in the process?", [("Offer on the table now", "Offer on the table now", ""), ("Starting within 3 months", "Starting within 3 months", ""), ("Already in the role", "Already in the role", ""), ("Exploring options", "Exploring options", "")]) +
            '<div class="step-nav"><span></span><button class="btn btn-primary" type="button" data-next>Continue</button></div></section>'
            '<section class="step" hidden><h2 style="font-size:1.3rem">The role</h2>' +
            select("seniority", "Level of the role", ["Board / chair", "CEO / president / head of organisation", "C-suite / executive", "VP / director", "Senior manager", "Elected or public office", "Other"]) +
            select("sector", "Sector", SECTORS) +
            select("org_size", "Organisation size", ["Under 50 people", "50 to 500", "500 to 5,000", "More than 5,000"], required=False) +
            field("situation", "What is happening? No names needed.", "textarea", placeholder="For example: offered the CEO role at a company that has missed its targets for two years; board split on strategy; no written mandate yet.", attrs='minlength="20"') +
            '<div class="step-nav"><button class="btn btn-line" type="button" data-back>Back</button><button class="btn btn-primary" type="button" data-next>Continue</button></div></section>'
            '<section class="step" hidden><h2 style="font-size:1.3rem">The help you want</h2>' +
            choices("help", "Choose any that apply", [("Contract and offer review (employment lawyer)", "Contract and offer review", "Employment lawyer"), ("Negotiation strategy", "Negotiation strategy", "What to ask for and how"),
                                                      ("Executive coach for the first year", "Executive coach", "For the first year in role"), ("Turnaround or interim specialist", "Turnaround or interim specialist", "Hands-on support"),
                                                      ("Board Appointment Review", "Board Appointment Review", "For organisations"), ("Leadership programme or workshop", "Leadership programme or workshop", "For teams and boards")], kind="checkbox", required=False) +
            select("budget", "Likely budget for outside help", ["Not sure yet", "Under US$1,000", "US$1,000 – 3,000", "US$3,000 – 10,000", "US$10,000+", "Organisation is paying"]) +
            select("contact_pref", "How should the adviser contact you?", ["Email", "Phone", "Video call"], required=False) +
            '<div class="step-nav"><button class="btn btn-line" type="button" data-back>Back</button><button class="btn btn-primary" type="button" data-next>Continue</button></div></section>'
            '<section class="step" hidden><h2 style="font-size:1.3rem">How we reach you</h2>' +
            '<div class="two">' + field("name", "Name", autocomplete="name") + field("email", "Work or personal email", "email", autocomplete="email") + '</div>' +
            '<div class="two">' + field("phone", "Phone", "tel", required=False, autocomplete="tel") + select("country", "Country", COUNTRIES) + '</div>' +
            consent("I agree that Glasscliff may use these details to respond to me and, with my agreement, share them with one matched adviser.") +
            '<label class="check"><input type="checkbox" name="newsletter" value="yes"> <span>Send me the Edge Brief, a short monthly email on high-stakes leadership.</span></label>'
            '<div class="step-nav"><button class="btn btn-line" type="button" data-back>Back</button><button class="btn btn-risk" type="submit">Request my confidential review</button></div>'
            '<p class="form-msg" role="status" aria-live="polite"></p></section></form>')
    body = (page_head("Get a confidential review", "Weighing a high-stakes role, or appointing someone to one? Tell us what is happening and we will match you with an experienced adviser for an initial conversation.", "Confidential review") +
            '<div class="wrap split" style="padding-bottom:48px"><div>' + form + '</div><div>'
            '<h2 style="font-size:var(--step-2)">How it works</h2><ol class="how" style="grid-template-columns:1fr"><li><b>Tell us the situation</b>Four short steps. No organisation names needed.</li>'
            '<li><b>We match you</b>With an executive coach, employment lawyer or turnaround adviser who has handled roles like yours.</li>'
            '<li><b>Talk it through</b>An initial conversation to decide whether and how they can help. Any fees are agreed directly with them.</li></ol>'
            '<div class="callout" style="margin-top:1.6rem"><b>Confidentiality</b>Your request is read only by the Glasscliff team. We share it with one matched adviser only after you agree. We never contact your organisation.</div>'
            '<div class="callout"><b>Reply time</b>We respond <span data-reply-time>within two business days</span>. If your offer has a deadline, mention it in the description.</div>'
            '<h2 style="font-size:1.2rem;margin-top:1.6rem">Before you send</h2><p>Running the <a href="{{p}}tools/risk-scanner.html">Risk Scanner</a> first gives your adviser a head start; your score is attached automatically when you come from the tool.</p></div></div>'
            '<section class="section section-mist"><div class="wrap narrow">' + faq_html([
                ("Is the review free?", "Requesting a review and the initial conversation are free. If you decide to work with an adviser, you agree their fees directly with them."),
                ("Who are the advisers?", "Independent executive coaches, employment lawyers, interim executives and turnaround specialists who apply to our Advisor Network and are vetted for relevant experience."),
                ("Will my employer find out?", "No. We never contact your organisation, and you do not need to name it."),
                ("Can an organisation request a review?", "Yes. Boards, CHROs and search panels can request a Board Appointment Review for a leader they are appointing or supporting."),
                ("Is this legal advice?", "Glasscliff does not give legal advice. If you need a contract review, we match you with a qualified employment lawyer.")]) + '</div></section>')
    layout("get-help.html", "Get a confidential review of a high-stakes leadership role",
           "Confidential review for leaders weighing a risky role and organisations appointing one. Get matched with an executive coach, employment lawyer or turnaround adviser.",
           body, active="get-help.html", sticky=False, keywords="confidential review coach lawyer adviser help", priority="0.9")

def build_orgs():
    body = (page_head("For boards and organisations", "Appointing a leader in difficult conditions is one of the highest-stakes decisions a board makes. We help you get it right, and help the leader succeed.", "For organisations") +
            '<div class="wrap" style="padding-bottom:24px"><div class="paths">'
            '<div class="path"><h3>Board Appointment Review</h3><p>An independent review of an appointment you are about to make or have just made: the baseline, the mandate, resources, timeline, sponsorship and protections, benchmarked against glass cliff research.</p></div>'
            '<div class="path"><h3>Leader transition support</h3><p>Coaching and advisory support for a newly appointed leader through the first 100 days and first year, matched from our Advisor Network.</p></div>'
            '<div class="path"><h3>Workshops and talks</h3><p>Sessions for boards, nomination committees, HR and leadership teams on the glass cliff, fair succession and supporting atypical leaders.</p></div>'
            '</div></div>'
            '<section class="section"><div class="wrap split"><div class="prose"><h2>Why boards ask for this</h2>'
            '<p>Research on the glass cliff shows that under-represented leaders are more likely to be appointed in difficult conditions in some contexts, and that what happens after appointment, the support, time and fairness of evaluation, shapes whether they succeed. A failed appointment costs a second search, lost momentum and reputational damage.</p>'
            '<p>An independent review gives the board a structured view before the offer is final, and a record that the appointment was made with care.</p>'
            '<h3>Start with the free check</h3><p>The <a href="{{p}}tools/board-check.html">Board Appointment Check</a> takes three minutes and shows the gaps a review would focus on.</p>'
            '<h3>Read first</h3><ul><li><a href="{{p}}guides/boards-appointing-a-crisis-leader.html">How to appoint a crisis leader without setting them up to fail</a></li><li><a href="{{p}}guides/race-ethnicity-and-the-saviour-effect.html">The saviour effect</a></li></ul></div>'
            '<div><form class="form-card" data-gc-form="organisation-enquiry" data-subject="Organisation enquiry" data-score data-redirect="thank-you.html?f=organisation">'
            '<h2 style="font-size:1.3rem">Talk to us</h2><input type="hidden" name="path" value="organisation"><input type="hidden" name="tool"><input type="hidden" name="tool_score">' +
            choices("service", "What are you interested in?", [("Board Appointment Review", "Board Appointment Review", ""), ("Leader transition support", "Leader transition support", ""), ("Workshop or talk", "Workshop or talk", ""), ("Not sure yet", "Not sure yet", "")]) +
            '<div class="two">' + field("name", "Name", autocomplete="name") + field("email", "Work email", "email", autocomplete="email") + '</div>' +
            '<div class="two">' + field("organisation", "Organisation", autocomplete="organization") + field("job_title", "Your role", autocomplete="organization-title") + '</div>' +
            select("seniority", "Level of the appointment", ["Board / chair", "CEO / president / head of organisation", "C-suite / executive", "VP / director", "Other"]) +
            select("timeline", "Timing", ["Offer on the table now", "Starting within 3 months", "Already in the role", "Exploring options"]) +
            select("budget", "Budget", ["Organisation is paying", "US$10,000+", "US$3,000 – 10,000", "Not sure yet"], required=False) +
            field("situation", "What would you like help with?", "textarea") + consent() +
            '<button class="btn btn-risk" type="submit">Send enquiry</button><p class="form-msg" role="status" aria-live="polite"></p></form></div></div></section>')
    layout("for-organizations.html", "For boards: Board Appointment Review and leader transition support",
           "Independent Board Appointment Reviews, leader transition coaching and workshops for boards, CHROs and search committees appointing leaders in a crisis.",
           body, active="for-organizations.html", keywords="board review CHRO succession workshop", priority="0.8")

def build_advisors():
    body = (page_head("Join the Advisor Network", "Glasscliff connects leaders in high-stakes roles with the people who can help them: executive coaches, employment lawyers, interim executives and turnaround specialists.", "Advisor Network") +
            '<div class="wrap" style="padding-bottom:24px"><div class="tiers">'
            '<div class="tier"><h3>Listed</h3><p class="price"><span data-plan="listed">US$49 / month</span></p><ul><li>Profile in the Advisor Network</li><li>Eligible for matched referrals</li><li>Cancel any time</li></ul><a class="btn btn-line" href="#apply">Apply</a></div>'
            '<div class="tier feature"><h3>Featured</h3><p class="price"><span data-plan="featured">US$149 / month</span></p><ul><li>Everything in Listed</li><li>Priority in matching</li><li>Featured on relevant guides and tools</li><li>Invitation to judge the Edge Prize</li></ul><a class="btn btn-primary" href="#apply">Apply for Featured</a></div>'
            '<div class="tier"><h3>Referral only</h3><p class="price"><span data-plan="referral">15% of first engagement</span></p><ul><li>No monthly fee</li><li>Pay only when a matched client engages you</li><li>Subject to capacity</li></ul><a class="btn btn-line" href="#apply">Apply</a></div>'
            '</div><p class="small muted" style="margin-top:.8rem">Launch rates. All advisers are vetted before listing. Glasscliff never shares a client\'s details without their agreement.</p></div>'
            '<section class="section" id="apply"><div class="wrap split"><div class="prose"><h2>Who we are looking for</h2><ul><li>Executive coaches with experience supporting leaders through turnarounds, crises or "first" appointments.</li>'
            '<li>Employment lawyers who negotiate senior executive contracts.</li><li>Interim executives and turnaround specialists.</li><li>Board advisers and search consultants focused on fair succession.</li></ul>'
            '<h2>How vetting works</h2><p>We review your experience, ask for two references from senior clients, and hold a short call. We publish clear standards and act on every client complaint.</p></div>'
            '<div><form class="form-card" data-gc-form="advisor-application" data-subject="Advisor Network application" data-redirect="thank-you.html?f=advisor">'
            '<h2 style="font-size:1.3rem">Apply to join</h2>' +
            '<div class="two">' + field("name", "Name", autocomplete="name") + field("email", "Email", "email", autocomplete="email") + '</div>' +
            select("specialism", "Main specialism", ["Executive coach", "Employment lawyer", "Interim executive", "Turnaround specialist", "Board adviser", "Search consultant", "Other"]) +
            select("plan", "Plan", ["Listed", "Featured", "Referral only", "Not sure yet"]) +
            '<div class="two">' + field("website", "Website or LinkedIn", "url", placeholder="https://") + select("country", "Country", COUNTRIES) + '</div>' +
            field("experience", "Relevant experience in two or three sentences", "textarea") + consent() +
            '<button class="btn btn-primary" type="submit">Send application</button><p class="form-msg" role="status" aria-live="polite"></p></form></div></div></section>')
    layout("advisors.html", "Join the Glasscliff Advisor Network for coaches, lawyers and turnaround experts",
           "Executive coaches, employment lawyers, interim executives and turnaround specialists: join the Glasscliff Advisor Network and receive matched referrals.",
           body, keywords="advisor network coach lawyer interim referral directory", priority="0.7")

def build_support():
    tiers = [("25", "one-time", "Keep a guide current", "Funds research and fact-checking for one guide update."),
             ("10", "monthly", "Monthly supporter", "Covers hosting, tools and the daily news service."),
             ("100", "one-time", "Fund a prize", "Goes straight into the Student Research Brief prize pool."),
             ("500", "one-time", "Commission a contributor", "Pays a new contributor for an in-depth guide.")]
    tier_html = "".join('<div class="tier%s"><h3>%s</h3><p class="price">US$%s <small>%s</small></p><p>%s</p><button class="btn %s" type="button" data-amount="%s" data-frequency="%s">Choose US$%s</button></div>' % (
        " feature" if f == "monthly" else "", esc(t), a, "per month" if f == "monthly" else "one time", esc(d), "btn-primary" if f == "monthly" else "btn-line", a, f, a) for a, f, t, d in tiers)
    alloc = [("Operations and hosting", 30), ("Promotion and marketing", 25), ("Hiring writers and researchers", 25), ("Contests and prizes", 20)]
    alloc_html = '<div class="alloc">' + "".join('<div class="bar"><span>%s</span><span class="track"><span class="fill" style="width:%d%%"></span></span><b>%d%%</b></div>' % (n, v, v) for n, v in alloc) + '</div>'
    body = (page_head("Support Glasscliff", "Glasscliff is independent and free to use. Reader support keeps the tools free, funds new research and contributors, and pays for the Edge Prize.", "Support us") +
            '<div class="wrap" style="padding-bottom:24px"><div class="tiers">' + tier_html + '</div></div>'
            '<section class="section"><div class="wrap split"><div><h2>Where the money goes</h2><p class="muted">Our planned split for every dollar of support. We will publish an annual summary.</p>' + alloc_html +
            '<div class="prose" style="margin-top:1.6rem"><h3>Other ways to help</h3><ul><li>Share a guide or tool with someone weighing a role.</li><li>Take the <a href="{{p}}survey.html">Glass Cliff Pulse Survey</a>.</li><li>Ask your employer about <a href="{{p}}advertise.html">sponsoring a prize</a>.</li><li>Corporate supporters: many employers match staff contributions. Ask your HR team.</li></ul></div></div>'
            '<div><div id="pay-links" class="btn-row" hidden style="margin-bottom:1rem"></div>'
            '<form id="pledge-form" class="form-card" data-gc-form="support-pledge" data-subject="Support pledge" data-redirect="thank-you.html?f=support">'
            '<h2 style="font-size:1.3rem">Make a pledge</h2><p id="pledge-mode-note" class="small muted">Choose an amount and we will email you a secure payment link (card, PayPal or bank transfer) <span data-reply-time>within two business days</span>.</p>' +
            '<div class="two">' + field("amount", "Amount (US$)", "number", attrs='min="1" step="1" inputmode="numeric"') + '<div class="field"><label for="f-frequency">Frequency</label><select id="f-frequency" name="frequency"><option value="one-time">One time</option><option value="monthly">Monthly</option><option value="yearly">Yearly</option></select></div></div>' +
            select("purpose", "Direct my support to", ["Wherever it is needed most", "Operations and hosting", "Promotion and marketing", "Hiring writers and researchers", "Contests and prizes"]) +
            '<div class="two">' + field("name", "Name", autocomplete="name") + field("email", "Email", "email", autocomplete="email") + '</div>' +
            '<label class="check"><input type="checkbox" name="public_thanks" value="yes"> <span>Thank me by name on the site (optional).</span></label>' + consent() +
            '<button class="btn btn-primary" type="submit">Send my pledge</button><p class="form-msg" role="status" aria-live="polite"></p></form>'
            '<p class="small muted" style="margin-top:.8rem">Support payments are contributions to running Glasscliff.com, not tax-deductible charitable donations.</p></div></div></section>')
    layout("support.html", "Support Glasscliff: keep the tools free and independent",
           "Support Glasscliff with a one-time or monthly contribution. Funds operations, promotion, new contributors and the Edge Prize.",
           body, keywords="donate support contribute fund", priority="0.6")

def build_contests():
    contests = [
        ("Turnaround Case Challenge", "For working professionals", "Write up a real turnaround or crisis role you led or witnessed, anonymised, in 1,200 to 2,000 words: the situation, the conditions you negotiated (or did not), what you did, and what you would do differently.",
         "Insight, honesty and usefulness to other leaders."),
        ("Student Research Brief", "For students and early-career researchers", "A 1,500-word brief on a question about the glass cliff, leadership succession or crisis leadership, using published evidence or your own data.",
         "Rigour, clarity and originality of the question."),
        ("Leadership Story", "Open to everyone", "A 600 to 1,000-word personal account of stepping into, or deciding against, a high-stakes role. Anonymous entries welcome.",
         "Candour, reflection and what others can learn."),
    ]
    blocks = ""
    for name, who, brief, judged in contests:
        blocks += ('<div class="contest"><span class="tag tag-stone">%s</span><h3>%s</h3><p style="font-family:var(--read);max-width:62ch">%s</p><p class="small"><b>Judged on:</b> %s</p></div>' % (esc(who), esc(name), esc(brief), esc(judged)))
    body = (page_head("The Edge Prize", "Quarterly prizes for the best writing on high-stakes leadership. Winners are published on Glasscliff and paid.", "Edge Prize") +
            '<div class="wrap split" style="padding-bottom:24px"><div>' + blocks + '</div><div>'
            '<div class="result" style="position:static"><h2 style="font-size:1.2rem">Current round: <span data-quarter-label>this quarter</span></h2><p class="small muted">Entries close <span data-deadline>at the end of the quarter</span> (23:59 UTC).</p><div class="countdown" data-countdown="0"></div>'
            '<table class="prize-table" style="margin-top:1rem"><thead><tr><th>Place</th><th>Prize (each category)</th></tr></thead><tbody>'
            '<tr><td>First</td><td data-prize="0">US$500 + featured publication</td></tr><tr><td>Second</td><td data-prize="1">US$250</td></tr><tr><td>Third</td><td data-prize="2">US$100</td></tr></tbody></table>'
            '<p class="small" style="margin-top:1rem">Want your organisation\'s name on a prize? <a href="{{p}}advertise.html">Sponsor the Edge Prize</a>.</p></div></div></div>'
            '<section class="section"><div class="wrap split"><div class="prose"><h2>Rules</h2><ol><li>Free to enter. One entry per person per category per round.</li><li>Entries must be your own, original and unpublished. Anonymise organisations and people.</li>'
            '<li>Open to adults worldwide, except where prohibited by law.</li><li>Entries are judged by the Glasscliff editorial team and, where a round is sponsored, one sponsor-nominated judge with relevant expertise.</li>'
            '<li>Winners are announced within 30 days of the close and paid by bank transfer or PayPal.</li><li>By entering you grant Glasscliff a non-exclusive licence to publish your entry with credit (or anonymously, if you ask).</li>'
            '<li>No purchase or payment is required, and supporting Glasscliff does not improve your chances.</li><li>We may withhold a prize if no entry meets the standard, and roll the prize into the next round.</li></ol></div>'
            '<div><form class="form-card" data-gc-form="edge-prize-entry" data-subject="Edge Prize entry" data-redirect="thank-you.html?f=prize"><h2 style="font-size:1.3rem">Enter this round</h2>' +
            select("category", "Category", [c[0] for c in contests]) +
            '<div class="two">' + field("name", "Name", autocomplete="name") + field("email", "Email", "email", autocomplete="email") + '</div>' +
            field("entry_title", "Title of your entry") +
            field("entry_link", "Link to your entry (Google Doc, Dropbox or similar, with view access)", "url", placeholder="https://") +
            field("summary", "Two-sentence summary", "textarea") +
            '<label class="check"><input type="checkbox" name="anonymous" value="yes"> <span>Publish anonymously if selected.</span></label>' +
            consent("I confirm this entry is my own original work and I accept the rules above.") +
            '<button class="btn btn-primary" type="submit">Submit my entry</button><p class="form-msg" role="status" aria-live="polite"></p></form></div></div></section>')
    layout("contests.html", "The Edge Prize: quarterly writing prizes on high-stakes leadership",
           "Win up to US$500 and publication: quarterly Edge Prize for turnaround case studies, student research briefs on the glass cliff, and leadership stories.",
           body, keywords="contest prize competition students essay award", priority="0.7", changefreq="weekly")

def build_careers():
    jobs = "".join('<li><div><h3>%s</h3><p><span class="tag">%s</span>%s</p></div><a class="btn btn-line btn-sm" href="#apply" data-role="%s">Apply</a></li>' % (esc(t), esc(w), esc(d), esc(t)) for t, w, d in JOBS)
    body = (page_head("Careers at Glasscliff", "We are a small, remote team building the best resource on high-stakes leadership. We hire writers, researchers, community builders and partners.", "Careers") +
            '<div class="wrap" style="padding-bottom:24px"><h2 style="font-size:var(--step-2)">Open roles</h2><ul class="jobs">' + jobs + '</ul></div>'
            '<section class="section" id="apply"><div class="wrap split"><div class="prose"><h2>How we work</h2><ul><li>Remote first, asynchronous by default.</li><li>Paid work is paid promptly; volunteer roles carry a stipend and credit.</li>'
            '<li>We value evidence, plain writing and kindness under pressure, the same things we write about.</li><li>We welcome applications from people under-represented in leadership.</li></ul>'
            '<h2>Not seeing your role?</h2><p>Join the talent pool with the form. We contact the pool first when new roles open.</p></div>'
            '<div><form class="form-card" data-gc-form="careers-application" data-subject="Careers application" data-redirect="thank-you.html?f=careers"><h2 style="font-size:1.3rem">Apply or join the talent pool</h2>' +
            select("role", "Role", [j[0] for j in JOBS] + ["Talent pool (any future role)"]) +
            '<div class="two">' + field("name", "Name", autocomplete="name") + field("email", "Email", "email", autocomplete="email") + '</div>' +
            field("portfolio", "Portfolio, LinkedIn or CV link", "url", placeholder="https://") +
            field("why", "Why you, in a few sentences", "textarea") + consent() +
            '<button class="btn btn-primary" type="submit">Send application</button><p class="form-msg" role="status" aria-live="polite"></p></form></div></div></section>'
            '<script>document.querySelectorAll("[data-role]").forEach(function(a){a.addEventListener("click",function(){var s=document.getElementById("f-role");if(s)s.value=a.getAttribute("data-role");});});</script>')
    jp = [{"@context": "https://schema.org", "@type": "JobPosting", "title": t, "description": d, "datePosted": PUBLISHED, "employmentType": "CONTRACTOR",
           "hiringOrganization": {"@type": "Organization", "name": "Glasscliff", "sameAs": SITE_URL}, "jobLocationType": "TELECOMMUTE",
           "applicantLocationRequirements": {"@type": "Country", "name": "Worldwide"}} for t, w, d in JOBS]
    layout("careers.html", "Careers at Glasscliff: writers, researchers, partnerships",
           "Remote roles at Glasscliff: contributing editors, research analysts, partnerships lead, community manager, video producer and campus ambassadors.",
           body, schema=jp, keywords="jobs careers hiring writer researcher remote", priority="0.6")

def build_advertise():
    tiers = "".join('<div class="tier%s"><h3>%s</h3><p class="price">%s <small>%s</small></p><ul>%s</ul><a class="btn %s" href="#enquire">Enquire</a></div>' % (
        " feature" if len(pk) > 4 else "", esc(pk[0]), pk[1], pk[2], "".join("<li>%s</li>" % esc(x) for x in pk[3]), "btn-primary" if len(pk) > 4 else "btn-line") for pk in AD_PACKAGES)
    body = (page_head("Advertise and sponsor", "Reach leaders weighing high-stakes roles, the boards that appoint them, and the people who study leadership. Every placement is labelled and editorially independent.", "Advertise") +
            '<div class="wrap" style="padding-bottom:24px"><div class="tiers">' + tiers + '</div><p class="small muted" style="margin-top:.8rem">Launch rates in US dollars. Custom packages available.</p></div>'
            '<section class="section" id="enquire"><div class="wrap split"><div class="prose"><h2>Who reads Glasscliff</h2><ul><li>Senior leaders considering turnaround, interim and "first" appointments.</li>'
            '<li>Chairs, directors, CHROs and search consultants.</li><li>Students, researchers and journalists covering leadership and equity.</li></ul>'
            '<h2>Good fits</h2><p>Executive education, coaching platforms, employment law firms, executive search, board-readiness programmes, HR technology and leadership publishers.</p>'
            '<h2>Our standards</h2><p>Sponsored placements are labelled. Sponsors do not review or shape editorial content. We decline advertisers whose products conflict with our readers\' interests.</p>'
            '<p>Interested in acquiring the site, the Glasscliff.com domain or a strategic partnership? <a href="https://web.works/contact" target="_blank" rel="noopener">Contact the owner directly</a>.</p></div>'
            '<div><form class="form-card" data-gc-form="advertising-enquiry" data-subject="Advertising or sponsorship enquiry" data-redirect="thank-you.html?f=advertise"><h2 style="font-size:1.3rem">Request the media kit</h2>' +
            select("package", "Interested in", [p[0] for p in AD_PACKAGES] + ["Partnership", "Something else"]) +
            '<div class="two">' + field("name", "Name", autocomplete="name") + field("email", "Work email", "email", autocomplete="email") + '</div>' +
            '<div class="two">' + field("company", "Company", autocomplete="organization") + field("website", "Website", "url", placeholder="https://") + '</div>' +
            select("budget", "Budget per quarter", ["Under US$1,000", "US$1,000 – 5,000", "US$5,000 – 15,000", "US$15,000+"], required=False) +
            field("message", "Goals and timing", "textarea", required=False) + consent() +
            '<button class="btn btn-primary" type="submit">Request the media kit</button><p class="form-msg" role="status" aria-live="polite"></p></form></div></div></section>')
    layout("advertise.html", "Advertise and sponsor on Glasscliff",
           "Sponsorship and advertising packages on Glasscliff: newsletter, tool, Edge Prize, report and directory placements for leadership and HR brands.",
           body, keywords="advertise sponsor media kit partnership", priority="0.6")

def build_survey():
    sc = lambda n, l, o: select(n, l, o, required=False)
    body = (page_head("The Glass Cliff Pulse Survey", "Have you been offered or held a leadership role in difficult conditions? Ten anonymous questions. Results feed the Glass Cliff Pulse report.", "Pulse Survey") +
            '<div class="wrap split" style="padding-bottom:48px"><div><form class="form-card" data-gc-form="pulse-survey" data-subject="Pulse Survey response" data-redirect="thank-you.html?f=survey">' +
            select("role_level", "1. The most senior high-stakes role you have been offered", ["Board / chair", "CEO / head of organisation", "C-suite / executive", "VP / director", "Senior manager", "Elected or public office"]) +
            select("accepted", "2. Did you accept it?", ["Yes", "No", "Still deciding"]) +
            select("condition", "3. The organisation's condition at the time", ["Stable", "Under pressure", "In visible crisis"]) +
            select("first", "4. Were you the first person of your gender, race or background in that role?", ["Yes", "No", "Prefer not to say"]) +
            sc("mandate", "5. Was your mandate written down?", ["Yes", "Partly", "No"]) +
            sc("resources", "6. Were resources committed in writing?", ["Yes", "Partly", "No"]) +
            sc("sponsor", "7. Did you have a named board sponsor?", ["Yes", "No"]) +
            sc("tenure", "8. How long did you stay?", ["Still in role", "Under 1 year", "1 to 2 years", "2 to 4 years", "More than 4 years"]) +
            field("lesson", "9. What do you wish you had negotiated?", "textarea", required=False) +
            sc("region", "10. Region", ["North America", "Europe", "UK and Ireland", "Asia", "Middle East", "Africa", "Latin America", "Oceania"]) +
            field("email", "Email, only if you want the report", "email", required=False, autocomplete="email") +
            '<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">'
            '<button class="btn btn-primary" type="submit">Send my answers</button><p class="form-msg" role="status" aria-live="polite"></p></form></div>'
            '<div class="prose"><h2>Why we run this survey</h2><p>Most glass cliff research uses company records or lab experiments. Far less captures what leaders themselves were offered, what they negotiated, and how it turned out. The Pulse fills that gap.</p>'
            '<h2>Your privacy</h2><ul><li>No name required. Email is optional and used only to send you the report.</li><li>Results are published only in aggregate.</li><li>Open-text answers may be quoted anonymously.</li></ul>'
            '<h2>Organisations</h2><p>Want to run the Pulse with your leadership community or alumni network? <a href="{{p}}contact.html">Contact us</a>.</p></div></div>')
    layout("survey.html", "The Glass Cliff Pulse Survey (anonymous)",
           "Share your experience of high-stakes leadership roles in ten anonymous questions. Results feed the Glass Cliff Pulse report.",
           body, keywords="survey research participate anonymous", priority="0.6")

def build_contact():
    body = (page_head("Contact Glasscliff", "Questions, corrections, partnerships, press and privacy requests. We reply <span data-reply-time>within two business days</span>.", "Contact") +
            '<div class="wrap split" style="padding-bottom:48px"><div><form class="form-card" data-gc-form="contact" data-subject="Contact form" data-redirect="thank-you.html?f=contact">' +
            select("topic", "Topic", ["General question", "Correction", "Confidential review question", "Advisor Network", "Edge Prize", "Advertising or sponsorship", "Website, domain or partnership enquiry", "Press", "Privacy request", "Copyright or trademark"]) +
            '<div class="two">' + field("name", "Name", autocomplete="name") + field("email", "Email", "email", autocomplete="email") + '</div>' +
            field("about_page", "Page you are writing about", "url", required=False, placeholder="https://") +
            field("message", "Message", "textarea") + consent() +
            '<button class="btn btn-primary" type="submit">Send message</button><p class="form-msg" role="status" aria-live="polite"></p></form></div>'
            '<div class="prose"><h2>Faster routes</h2><ul><li><b>Weighing a role?</b> The <a href="{{p}}get-help.html">confidential review form</a> goes straight to the right person.</li>'
            '<li><b>Board or HR?</b> See <a href="{{p}}for-organizations.html">For organisations</a>.</li><li><b>Coach or lawyer?</b> <a href="{{p}}advisors.html">Join the Advisor Network</a>.</li>'
            '<li><b>Brands:</b> <a href="{{p}}advertise.html">Advertise and sponsor</a>.</li></ul>'
            '<h2>Prefer email?</h2><p><a href="{{p}}contact.html" data-mail="Glasscliff enquiry">Write to us by email</a>. The link opens your email app.</p>'
            '<h2>Website, domain or partnership</h2><p>If you are interested in this website, the Glasscliff.com domain name, sponsorship, advertising or a partnership, <a href="https://web.works/contact" target="_blank" rel="noopener">contact the owner</a>.</p></div></div>')
    layout("contact.html", "Contact Glasscliff", "Contact Glasscliff with questions, corrections, partnership ideas, press or privacy requests.",
           body, keywords="contact email message", priority="0.5")
