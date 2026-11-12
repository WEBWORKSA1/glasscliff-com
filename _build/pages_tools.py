# Tool pages: hub + five interactive tools.
from common import *
from pages_content import TOOLS, guide_list, GUIDE_MAP, instruments

GAUGE = '''<svg class="gauge" id="%s" viewBox="0 0 300 170" aria-hidden="true">
<path d="M20 150a130 130 0 0 1 260 0" fill="none" stroke="#dfe6e4" stroke-width="22"/>
<path d="M20 150a130 130 0 0 1 58-108" fill="none" stroke="#3F7D4E" stroke-width="22"/>
<path d="M78 42a130 130 0 0 1 144 0" fill="none" stroke="#B7791F" stroke-width="22"/>
<path d="M222 42a130 130 0 0 1 58 108" fill="none" stroke="#B3264A" stroke-width="22"/>
<g class="needle" style="transform:rotate(-90deg)"><path d="M150 150V40" stroke="#1D2433" stroke-width="5" stroke-linecap="round"/></g>
<circle cx="150" cy="150" r="10" fill="#1D2433"/></svg>'''

def q(name, legend, opts, hint=""):
    h = '<span class="hint">%s</span>' % esc(hint) if hint else ""
    items = "".join('<label><input type="radio" name="%s" value="%s"><span>%s</span></label>' % (name, v, esc(t)) for v, t in opts)
    return '<fieldset class="q"><legend>%s%s</legend><div class="scale">%s</div></fieldset>' % (esc(legend), h, items)

def tool_page(path, title, desc, h1, dek, shell, method, faqs, related, kw):
    body = ('<div class="wrap page-head">' + crumbs([("{{p}}index.html", "Home"), ("{{p}}tools/", "Tools"), (None, h1)]) +
            '<h1>%s</h1><p class="dek">%s</p></div>' % (esc(h1), dek) +
            '<div class="wrap" style="padding-bottom:40px">' + shell + '</div>' +
            '<section class="section section-mist"><div class="wrap split"><div class="prose">' + method + '</div><div>' + faq_html(faqs, "Questions") + '</div></div></section>' +
            '<section class="section"><div class="wrap"><h2 style="font-size:var(--step-2)">Related guides</h2>' + guide_list([GUIDE_MAP[s] for s in related]) + '</div></section>')
    schema = [{"@context": "https://schema.org", "@type": "WebApplication", "name": h1, "applicationCategory": "BusinessApplication", "operatingSystem": "Any",
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}, "url": SITE_URL + "/" + path, "description": desc},
              faq_schema(faqs), crumb_schema([("", "Home"), ("tools/", "Tools"), (path, h1)])]
    layout(path, title, desc, body, active="tools/", schema=schema, scripts=("tools.js",), keywords=kw, priority="0.9")

def build_tools():
    # hub
    body = ('<div class="wrap page-head">' + crumbs([("{{p}}index.html", "Home"), (None, "Tools")]) +
            '<h1>Free tools for high-stakes roles</h1><p class="dek">Five tools built on glass cliff research and governance practice. They run entirely in your browser, save your progress on your device, and send nothing unless you choose to.</p></div>'
            '<div class="wrap" style="padding-bottom:40px">' + instruments() + '</div>'
            '<section class="section section-mist"><div class="wrap split"><div class="prose"><h2>Which tool should I use?</h2>'
            '<ul><li><b>Offered a role?</b> Start with the <a href="risk-scanner.html">Risk Scanner</a>, then build your negotiation list with the <a href="offer-protection.html">Offer Protection Builder</a>.</li>'
            '<li><b>Starting soon?</b> Generate a plan with the <a href="100-day-plan.html">100-Day Planner</a> and check yourself with the <a href="readiness-quiz.html">Readiness Check</a>.</li>'
            '<li><b>On a board or panel?</b> Run the <a href="board-check.html">Board Appointment Check</a> before you make the offer.</li></ul>'
            '<h2>How the tools were built</h2><p>Each tool turns findings from the research on the glass cliff (see our <a href="{{p}}research.html">Research Library</a>) and common governance practice into structured questions. The scores are indicators to guide a conversation, not predictions about any role or person.</p></div>'
            '<div class="lead-band" style="grid-template-columns:1fr"><div><h2>Want a human to look at it?</h2><p>Share your tool results with an experienced adviser through a confidential review.</p><a class="btn btn-primary" href="{{p}}get-help.html">Get a confidential review</a></div></div></div></section>')
    layout("tools/index.html", "Free glass cliff tools: risk scanner, negotiation and 100-day planner",
           "Free tools for leaders and boards: Glass Cliff Risk Scanner, Offer Protection Builder, Turnaround 100-Day Planner, Readiness Check and Board Appointment Check.",
           body, active="tools/", schema=crumb_schema([("", "Home"), ("tools/", "Tools")]), keywords="tools calculator scanner quiz checklist", priority="0.9", changefreq="weekly")

    # 1. Risk Scanner
    qs = (q("q1", "Is the organisation, or the unit you would lead, already in a visible crisis?", [("0", "No, it is stable"), ("5", "Under pressure"), ("10", "Yes, a visible crisis")]) +
          q("q2", "Is your mandate in writing?", [("0", "Yes, signed"), ("6", "Discussed, not written"), ("10", "Vague or contested")], "Scope, decision rights and how success will be judged.") +
          q("q3", "Do new resources come with the role?", [("0", "Committed in writing"), ("6", "Promised verbally"), ("10", "None: do more with less")]) +
          q("q4", "How long do you have to show results?", [("0", "18 months or more"), ("5", "6 to 18 months"), ("10", "Under 6 months")]) +
          q("q5", "How did your predecessor leave?", [("0", "Planned succession"), ("6", "Resigned under pressure"), ("10", "Dismissed, or several leaders in 3 years")]) +
          q("q6", "How strong is board or sponsor support?", [("0", "Named sponsor with authority"), ("5", "Generally supportive"), ("10", "Divided, or no sponsor")]) +
          q("q7", "Were you the first choice?", [("0", "Yes"), ("4", "Not sure"), ("10", "Others declined first")]) +
          q("q8", "Can you shape your own leadership team?", [("0", "Yes, freely"), ("5", "Some changes allowed"), ("10", "Must keep the inherited team")]) +
          q("q9", "Can you see the real numbers before you sign?", [("0", "Full access"), ("5", "Partial access"), ("10", "Refused, or 'after you start'")]) +
          q("q10", "What happens to you if it goes wrong?", [("0", "Severance and change-of-control cover"), ("5", "Standard terms"), ("10", "Little or no protection")]) +
          q("q11", "Is the crisis openly acknowledged?", [("0", "Yes, openly"), ("4", "Partly"), ("10", "Hidden: you would be blamed for it")]) +
          q("q12", "Would you be a 'first' or atypical leader in this seat?", [("0", "No"), ("4", "Yes, with visible peers"), ("8", "Yes, and the only one")], "For example the first woman or first person of colour in the role."))
    shell = ('<div class="tool-shell"><form id="risk-scanner" aria-describedby="scan-count"><p class="small muted" id="scan-count" aria-live="polite">0 of 12 answered</p>' + qs +
             '<div class="btn-row" style="margin-top:1rem"><button class="btn btn-line btn-sm" type="button" id="scan-reset">Start again</button></div></form>'
             '<aside class="result" aria-live="polite"><h2 style="font-size:1.2rem">Your result</h2><p id="scan-wait" class="muted">Answer at least six questions to see a score. Answer all twelve for the most reliable result.</p>'
             '<div id="scan-result" hidden>' + GAUGE % "scan-gauge" + '<p class="score-big"><span id="scan-score">0</span><span class="sr"> out of 100</span></p><p id="scan-band" class="band"></p><p id="scan-tip" class="small"></p>'
             '<h3 style="font-size:1rem;margin-top:1rem">Top red flags</h3><ul class="flag-list" id="scan-flags"></ul>'
             '<h3 style="font-size:1rem">What to negotiate</h3><ul class="flag-list asks" id="scan-asks"></ul>'
             '<div class="btn-row no-print"><a class="btn btn-risk" id="scan-cta" href="{{p}}get-help.html">Get a confidential review</a><button class="btn btn-line btn-sm" type="button" data-print>Print</button></div>'
             '<form id="scan-email-form" class="no-print" data-gc-form="scan-results" data-subject="Risk Scanner results" data-ok="Sent. Check your inbox shortly." style="margin-top:1.2rem;border-top:1px solid var(--line);padding-top:1rem">'
             '<p class="small" style="margin:0 0 .5rem"><b>Email me a copy</b> and occasional Edge Brief updates.</p>'
             '<input type="hidden" name="score"><input type="hidden" name="flags"><input type="hidden" name="asks">'
             '<div class="field"><label class="sr" for="se-email">Email</label><input id="se-email" type="email" name="email" placeholder="Your email" required autocomplete="email"><span class="err"></span></div>'
             '<input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true"><button class="btn btn-dark btn-sm" type="submit">Email my results</button><p class="form-msg" role="status" aria-live="polite"></p></form>'
             '</div></aside></div>')
    method = ('<h2>How the score works</h2><p>Each answer is scored from 0 (no risk) to 10 (high risk) and weighted by how strongly it relates to the conditions that research and practice link to failed crisis appointments. The weights are highest for the organisation\'s condition, a written mandate, resources and sponsorship. The total is scaled to 0–100.</p>'
              '<table><thead><tr><th>Score</th><th>Band</th><th>What it means</th></tr></thead><tbody>'
              '<tr><td>0–29</td><td>Solid ground</td><td>Well supported. Confirm the essentials in writing.</td></tr>'
              '<tr><td>30–49</td><td>Watch the edge</td><td>Real but negotiable risks.</td></tr>'
              '<tr><td>50–69</td><td>Glass cliff</td><td>High risk of being set up to fail without changes.</td></tr>'
              '<tr><td>70–100</td><td>Free fall</td><td>The conditions for success are missing.</td></tr></tbody></table>'
              '<p>The score describes the role, not you. A high score does not mean you would fail; it means the role, as offered, makes success harder than it needs to be. Read <a href="{{p}}guides/red-flags-in-a-leadership-offer.html">twelve red flags in a leadership offer</a> for the reasoning behind each question.</p>')
    tool_page("tools/risk-scanner.html", "Glass Cliff Risk Scanner: is this leadership role set up to fail?",
              "Free 12-question risk scanner for leadership offers. Get a 0–100 glass cliff risk score, your top red flags and what to negotiate before you accept.",
              "Glass Cliff Risk Scanner", "Twelve questions about the role you are weighing. You get a risk score, the red flags that drive it, and what to negotiate. About four minutes.",
              shell, method,
              [("Is my data stored?", "Your answers are saved only in your own browser so you can come back to them. Nothing is sent unless you use the email form."),
               ("Can I use this for a role I already hold?", "Yes. Answer as things stand today. A high score suggests what to renegotiate with your board or sponsor."),
               ("What should I do with a high score?", "Use the 'What to negotiate' list as the agenda for your next conversation, build a full list with the Offer Protection Builder, or request a confidential review.")],
              ["red-flags-in-a-leadership-offer", "how-to-negotiate-a-turnaround-role", "is-a-crisis-role-a-career-accelerator"], "risk score calculator glass cliff offer red flags")

    # 2. Offer Protection Builder
    risks = [("crisis", "The organisation is in visible crisis"), ("mandate", "The mandate is not written down"), ("resources", "Resources are thin or unconfirmed"),
             ("timeline", "The timeline to show results is short"), ("board", "The board is divided or there is no sponsor"), ("team", "I must keep the inherited team"),
             ("info", "I cannot see the full picture before signing"), ("exit", "Exit terms are weak"), ("first", "I would be a visible 'first' or atypical leader"), ("interim", "The role is interim or acting")]
    shell = ('<div class="tool-shell"><form id="offer-builder">'
             '<div class="field"><label for="f-role">Type of role</label><select id="f-role" name="role"><option value="exec">Executive or senior leader</option><option value="ceo">CEO, president or head of organisation</option><option value="interim">Interim or acting leader</option><option value="public">Elected or public-sector role</option></select></div>'
             '<fieldset class="field" style="border:0;padding:0"><legend class="legend">Which risks do you see in this offer?</legend><div class="choices">' +
             "".join('<label class="choice"><input type="checkbox" name="risk" value="%s"><span>%s</span></label>' % (v, esc(t)) for v, t in risks) +
             '</div></fieldset></form>'
             '<aside class="result" aria-live="polite"><h2 style="font-size:1.2rem">Protections to negotiate</h2><p class="small muted" id="offer-count"></p><p id="offer-empty" class="muted">Tick at least one risk to build your list.</p>'
             '<ul class="check-out" id="offer-list"></ul><div class="btn-row no-print" id="offer-actions" hidden style="margin-top:1rem"><button class="btn btn-dark btn-sm" type="button" data-copy="#offer-list">Copy list</button>'
             '<button class="btn btn-line btn-sm" type="button" data-print>Print</button><a class="btn btn-risk btn-sm" href="{{p}}get-help.html?path=leader&amp;tool=Offer%20Protection%20Builder">Get help negotiating</a></div></aside></div>')
    method = ('<h2>How to use your list</h2><ol><li><b>Start with the "Must have" items.</b> They are the conditions for success: mandate, baseline, resources, time, sponsor.</li>'
              '<li><b>Bundle the protections.</b> Present severance, indemnity and coaching as a standard package for a high-risk role.</li>'
              '<li><b>Put agreements in writing.</b> Follow each conversation with an email summary, and ask for the key points in the offer letter or a board minute.</li>'
              '<li><b>Get the contract reviewed.</b> An employment lawyer should check severance, change-of-control and indemnity terms.</li></ol>'
              '<p>The reasoning behind each protection is in <a href="{{p}}guides/how-to-negotiate-a-turnaround-role.html">How to negotiate a turnaround role</a>.</p>')
    tool_page("tools/offer-protection.html", "Offer Protection Builder: what to negotiate in a turnaround role",
              "Tick the risks in your leadership offer and get a prioritised checklist of protections to negotiate: mandate letter, resources, sponsor, severance, D&O and more.",
              "Offer Protection Builder", "Tick the risks you see in your offer. Get a prioritised list of protections to negotiate, ready to copy or print.",
              shell, method,
              [("Is this legal advice?", "No. It is a checklist of commonly negotiated terms. Have an employment lawyer review any contract before you sign."),
               ("Will asking for all of these cost me the offer?", "Prioritise the 'Must have' items. Serious organisations expect senior candidates to negotiate the conditions for success."),
               ("What is a mandate letter?", "A short document signed by the appointing body setting out your scope, decision rights and how success will be judged.")],
              ["how-to-negotiate-a-turnaround-role", "red-flags-in-a-leadership-offer", "glass-cliff-in-politics"], "negotiate offer checklist severance mandate letter")

    # 3. 100-Day Planner
    shell = ('<div class="tool-shell"><form id="planner">'
             '<div class="field"><label for="f-situation">What kind of situation are you walking into?</label><select id="f-situation" name="situation">'
             '<option value="finance">Financial distress</option><option value="reputation">Reputational crisis</option><option value="culture">Toxic or broken culture</option><option value="scandal">Post-scandal clean-up</option><option value="growth">Growth that is breaking the organisation</option></select></div>'
             '<div class="field"><label for="f-size">How large is the organisation or unit?</label><select id="f-size" name="size"><option value="small">Under 100 people</option><option value="medium">100 to 2,000 people</option><option value="large">More than 2,000 people</option></select></div>'
             '<div class="field"><label for="f-hire">Are you an internal or external hire?</label><select id="f-hire" name="hire"><option value="external">External</option><option value="internal">Internal</option></select></div>'
             '<div class="field"><label for="f-start">Start date <span class="opt">(optional, to date the plan)</span></label><input id="f-start" type="date" name="start"></div>'
             '<div class="btn-row no-print"><button class="btn btn-dark btn-sm" type="button" data-print>Print or save as PDF</button></div></form>'
             '<aside class="result" style="position:static" aria-live="polite"><h2 style="font-size:1.2rem">Your 100-day plan</h2><div id="plan-out"></div></aside></div>')
    method = ('<h2>Why three phases</h2><p>Crisis roles reward leaders who resist the urge to announce a plan in week one. Diagnosing first protects you from committing to the wrong priorities, and recording the position you inherited means you will be judged on progress rather than the starting point.</p>'
              '<p>The plan combines actions that apply to almost every turnaround with actions specific to the situation you chose. Adapt it; it is a scaffold, not a script. The full reasoning is in <a href="{{p}}guides/first-100-days-turnaround-role.html">The first 100 days of a turnaround role</a>.</p>')
    tool_page("tools/100-day-plan.html", "Turnaround 100-Day Planner for new leaders",
              "Generate a free three-phase 100-day plan for a turnaround or crisis leadership role: diagnose, stabilise, commit, tailored to your situation.",
              "Turnaround 100-Day Planner", "Choose your situation and get a three-phase plan, dated from your start day, with weekly checkpoints. Print it or save it as a PDF.",
              shell, method,
              [("Can I edit the plan?", "Print or save it as a PDF, then edit your copy. Your choices are remembered on this device."),
               ("Does this work for a role I already started?", "Yes. Start from the phase you are in and use the earlier phases as a checklist of anything you skipped."),
               ("What if my situation is a mix of types?", "Pick the dominant one, then run the planner again for the second and merge the lists.")],
              ["first-100-days-turnaround-role", "how-to-negotiate-a-turnaround-role", "is-a-crisis-role-a-career-accelerator"], "100 day plan first 90 days turnaround new leader")

    # 4. Readiness Check
    stm = [("diag", "I can tell the difference between the symptoms of a problem and its causes within a few weeks."), ("diag", "I seek out people who will tell me bad news."), ("diag", "I write down what I find before deciding what to do about it."),
           ("dec", "I can make a good-enough decision without complete information."), ("dec", "I set review dates for big decisions instead of treating them as final."), ("dec", "I can stop a project I started when the evidence changes."),
           ("comm", "I explain hard decisions clearly, including what I do not yet know."), ("comm", "I stay calm and consistent when I am being criticised in public."), ("comm", "I communicate more, not less, when things are going badly."),
           ("coal", "I have a sponsor or ally with real authority in my organisation."), ("coal", "I build relationships with people outside my reporting line."), ("coal", "I can bring sceptics on board without giving away the plan."),
           ("resil", "I have people outside work I can talk to honestly."), ("resil", "I protect my sleep and recovery during intense periods."), ("resil", "I know my early warning signs of being overstretched.")]
    scale = [("1", "Strongly disagree"), ("2", "Disagree"), ("3", "Neutral"), ("4", "Agree"), ("5", "Strongly agree")]
    qs = "".join('<fieldset class="q" data-dim="%s"><legend>%d. %s</legend><div class="scale">%s</div></fieldset>' % (
        d, i + 1, esc(t), "".join('<label><input type="radio" name="r%d" value="%s"><span>%s</span></label>' % (i, v, l) for v, l in scale)) for i, (d, t) in enumerate(stm))
    shell = ('<div class="tool-shell"><form id="readiness"><p class="small muted" id="ready-count" aria-live="polite">0 of 15 answered</p>' + qs + '</form>'
             '<aside class="result" aria-live="polite"><h2 style="font-size:1.2rem">Your profile</h2><p id="ready-wait" class="muted">Answer all fifteen statements to see your profile.</p>'
             '<div id="ready-out" hidden><p class="score-big"><span id="ready-score">0</span><span class="sr"> out of 100</span></p><p class="band b0">Overall readiness</p>'
             '<div class="bars" id="ready-bars"></div><p class="small">Strongest: <b id="ready-strong"></b></p><h3 style="font-size:1rem">Build these first</h3><ul class="flag-list asks" id="ready-tips"></ul>'
             '<div class="btn-row no-print"><a class="btn btn-risk" id="ready-cta" href="{{p}}get-help.html">Find a coach for a crisis role</a><button class="btn btn-line btn-sm" type="button" data-print>Print</button></div></div></aside></div>')
    method = ('<h2>The five dimensions</h2><ul><li><b>Diagnosis:</b> seeing the real problem quickly.</li><li><b>Decisions under pressure:</b> acting without complete information, and correcting course.</li>'
              '<li><b>Communication:</b> candour, consistency and calm under scrutiny.</li><li><b>Coalition building:</b> sponsors, allies and the ability to win over sceptics.</li><li><b>Personal resilience:</b> the support and habits that sustain you through a long, hard role.</li></ul>'
              '<p>This is a self-reflection tool, not a validated psychometric test. Use it to decide where to invest before you start, ideally with a coach or trusted colleague.</p>')
    tool_page("tools/readiness-quiz.html", "Crisis Leadership Readiness Check (free self-assessment)",
              "A free 15-statement self-assessment of your readiness for a crisis or turnaround leadership role across five dimensions, with development suggestions.",
              "Crisis Leadership Readiness Check", "Fifteen statements across five dimensions. See where you are strong and what to build before you take on a high-stakes role.",
              shell, method,
              [("Is this a psychometric test?", "No. It is a structured self-reflection based on common themes in crisis leadership. It is not validated as a psychological assessment."),
               ("What is a good score?", "There is no pass mark. Look at the spread: your two lowest dimensions are where support or preparation will help most."),
               ("Can my team use it?", "Yes. Many leaders find it useful to compare their own answers with how a trusted colleague would rate them.")],
              ["first-100-days-turnaround-role", "is-a-crisis-role-a-career-accelerator", "what-is-the-glass-cliff"], "readiness quiz self assessment crisis leadership")

    # 5. Board Appointment Check
    checks = [("We have written an honest summary of the organisation's condition and shared it with shortlisted candidates.", "Write and share an honest baseline with candidates."),
              ("We would offer this role on the same terms to the candidate we would have chosen in good times.", "Test the offer against what you would give a conventional candidate."),
              ("We know why previous candidates declined, if any did.", "Find out why candidates declined and fix those issues."),
              ("The mandate (scope, decision rights, success measures) is written and signed by the chair.", "Put the mandate in a signed letter."),
              ("The resources the plan needs are committed in a board minute.", "Commit resources in a board minute, not a conversation."),
              ("The leader can make senior team changes in the first six months.", "Give the leader authority over the senior team."),
              ("The first formal review is at least 12 months away.", "Set a realistic review date, typically 12 to 18 months."),
              ("A named director will meet the leader privately at least every two weeks for six months.", "Name a board sponsor with authority and a meeting rhythm."),
              ("Severance, indemnity and D&O cover match what we offer other senior leaders.", "Match protections to what other senior leaders receive."),
              ("Progress will be judged against the agreed baseline, not the starting level.", "Agree to judge the trend against the baseline."),
              ("The board agrees on what success looks like in the first year.", "Resolve board disagreement about success before the appointment."),
              ("If the appointment ends early, we will review why before choosing a successor.", "Commit to a review before any replacement decision.")]
    qs = "".join('<fieldset class="q" data-gap="%s"><legend>%d. %s</legend><div class="scale"><label><input type="radio" name="b%d" value="yes"><span>Yes</span></label><label><input type="radio" name="b%d" value="no"><span>No or not sure</span></label></div></fieldset>' % (
        esc(g), i + 1, esc(t), i, i) for i, (t, g) in enumerate(checks))
    shell = ('<div class="tool-shell"><form id="board-check"><p class="small muted" id="board-count" aria-live="polite">0 of 12 answered</p>' + qs + '</form>'
             '<aside class="result" aria-live="polite"><h2 style="font-size:1.2rem">Support score</h2><p id="board-wait" class="muted">Answer all twelve checks to see your score.</p>'
             '<div id="board-out" hidden>' + GAUGE % "board-gauge" + '<p class="score-big"><span id="board-score">0</span><span class="sr"> out of 100</span></p><p id="board-band" class="band"></p>'
             '<h3 style="font-size:1rem">Gaps to close before the offer</h3><ul class="flag-list" id="board-gaps"></ul>'
             '<div class="btn-row no-print"><a class="btn btn-risk" id="board-cta" href="{{p}}for-organizations.html">Request a Board Appointment Review</a><button class="btn btn-line btn-sm" type="button" data-print>Print</button></div></div></aside></div>')
    method = ('<h2>Read the gauge the right way round</h2><p>On this tool a <b>higher score is better</b>: it measures the support you are building around the appointment. The gauge colours show where the appointment sits, from well supported to set up to fail.</p>'
              '<p>The twelve checks come from research on the glass cliff and the saviour effect and from common governance practice. They are explained in <a href="{{p}}guides/boards-appointing-a-crisis-leader.html">How to appoint a crisis leader without setting them up to fail</a>.</p>')
    tool_page("tools/board-check.html", "Board Appointment Check: avoid the glass cliff when appointing a leader",
              "A free 12-point check for boards, chairs and search committees appointing a leader in a crisis. Score your support and see the gaps to close.",
              "Board Appointment Check", "Twelve yes-or-no checks for chairs, nomination committees and search panels. See whether you are setting your next leader up to succeed.",
              shell, method,
              [("Who should complete the check?", "The chair or the nomination committee, ideally together, before the offer is made."),
               ("Our score is low. Should we delay the appointment?", "Not necessarily. Most gaps can be closed quickly: a mandate letter, a board minute on resources and a named sponsor."),
               ("Can Glasscliff review our appointment?", "Yes. Request a Board Appointment Review and we will connect you with an independent adviser.")],
              ["boards-appointing-a-crisis-leader", "race-ethnicity-and-the-saviour-effect", "glass-cliff-research-evidence"], "board check governance nomination committee appointment")
