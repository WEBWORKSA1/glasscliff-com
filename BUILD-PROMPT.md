# Glasscliff.com — Phase-wise Build Prompt

A copy-paste prompt set for building (or rebuilding, or extending) Glasscliff.com with any capable AI coding assistant. Run the phases in order. Each phase lists the prompt, the deliverables and the acceptance checks that must pass before moving on.

> Owner inbox rule: every form on the site delivers to the single owner inbox. That address is supplied privately to the builder and must only ever be stored encoded (see Phase 6). It is deliberately not written in this file.

---

## Phase 0 — Concept and business model

**Prompt**

> You are the founding product lead for Glasscliff.com. "Glass cliff" is the research term (Ryan & Haslam, University of Exeter, 2005) for the pattern where women and other under-represented leaders are more likely to be appointed to leadership roles during a crisis, when the risk of failure is highest. Build Glasscliff.com as the independent leadership-risk guide for three audiences:
> 1. **Leaders** weighing a high-stakes role (turnaround CEO, interim executive, first female or first minority leader of a struggling unit, politician taking over after a defeat).
> 2. **Boards, CHROs and search committees** who appoint those leaders and want to avoid setting them up to fail.
> 3. **Students, researchers and journalists** who need a clear, sourced explanation of the evidence and the debate.
>
> Positioning line: "See the edge before you step onto it." Tone: calm, evidence-led, practical, never sensational. Do not name living individuals as "glass cliff victims"; discuss research patterns, not people.

**Revenue engines (in order of expected value)**
1. Lead generation — Confidential Role Review (leaders) and Board Appointment Review (organisations), referred to vetted executive coaches, employment lawyers and interim-leadership advisers. Monetised per qualified lead or as referral fees.
2. Advisor Network listings — paid directory/referral plans for coaches and advisers.
3. Google AdSense (publisher ID `ca-pub-6620975821265271`) on content pages. Leadership-development, executive-coaching and executive-education keywords carry US CPCs in the $10–$22 range.
4. Sponsorship and advertising — newsletter, report, tool and contest sponsorships.
5. Donations and memberships — one-time and monthly support.

**Acceptance:** a one-page positioning brief exists; every later phase traces back to one of the three audiences and one of the five revenue engines.

---

## Phase 1 — Competitive research synthesis

**Prompt**

> Visit at least 35 leading sites in the leadership, women-in-leadership, executive search, coaching, board-diversity and career-data space (e.g. Lean In, Catalyst, Women in the Workplace, HBR, CCL, Chief, Ellevate, The Muse, Levels.fyi, Korn Ferry, Spencer Stuart, Russell Reynolds, Heidrick & Struggles, Egon Zehnder, 30% Club, 50/50 Women on Boards, Women on Boards, SHRM, BetterUp, CoachHub, Torch, MindTools, Harvard PON, AnitaB.org, PowerToFly, Ladders, ExecuNet, NACD, Equileap, Great Place To Work, Built In, The Glass Hammer, The Female Lead, Forbes Leadership, McKinsey Leadership, TED, Wikipedia "Glass cliff", Idealist). For each, record navigation, lead-capture forms and CTAs, interactive tools, content formats, monetisation and design. Output RESEARCH.md with a feature matrix and a "steal list" of patterns to adopt.

**Acceptance:** RESEARCH.md lists 35+ sites and at least 25 concrete patterns mapped to Glasscliff pages.

---

## Phase 2 — Information architecture

**Prompt**

> Design the sitemap for a static site hosted on GitHub Pages (free plan, `main` branch, root folder). Use relative links everywhere so the site works both at `https://<user>.github.io/glasscliff-com/` and at `https://glasscliff.com/`. Required pages:
> - Home
> - Tools hub + 5 tools: Glass Cliff Risk Scanner, Offer Protection Builder, Turnaround 100-Day Planner, Crisis Leadership Readiness Check, Board Appointment Check
> - Guides hub + 10 long-form guides
> - Research Library (annotated studies + timeline), Glossary, Video Library, Leadership News (auto-updated), Pulse Survey (anonymous)
> - Get Help (Confidential Role Review — the dedicated lead-generation section), For Organisations, Join the Advisor Network
> - Support (donations), Prizes and Contests, Careers, Advertise and Sponsor
> - About, Contact, FAQ, Search, Editorial Policy, Privacy, Terms, Disclaimer and Trademark/Copyright notice, HTML sitemap, Thank-you, 404
> - Root files: `ads.txt`, `robots.txt`, `sitemap.xml`, `site.webmanifest`, favicon

**Acceptance:** every page is reachable within two clicks from the header or footer; no orphan pages.

---

## Phase 3 — Design system

**Prompt**

> Create a distinctive design system rooted in the subject: geology, strata, survey instruments, glass. Avoid generic AI-site tells (cream + terracotta, neon-on-black, identical rounded cards, ALL-CAPS eyebrows, arrows appended to buttons).
> - Palette: Basalt `#1D2433` (text), Fog `#EEF2F1` (background), Glacier `#2E7C83` (actions/links) with pale Glacier `#9FD3D6` (glass), Strata `#B9A58A` (structure lines), Garnet `#B3264A` (risk/alerts).
> - Type: Schibsted Grotesk for display/UI, Source Serif 4 for reading text (18px, 1.7 line height, max 68ch).
> - Signature element: the cliff cross-section — layered strata with a glass ledge — used in the hero and as section dividers. Glass treatment (translucency + blur) only on the header and the hero "edge test" panel.
> - Components: owner bar, header with mobile drawer, buttons, form fields with visible focus, gauge, callout, accordion FAQ, video facade, news list, pricing tiers, progress steps, toast/status.
> - Quality floor: responsive to 320px, WCAG AA contrast, visible keyboard focus, `prefers-reduced-motion` respected, no layout shift from ads (reserve space).

**Acceptance:** one CSS file; Lighthouse accessibility ≥ 95 on Home and a guide.

---

## Phase 4 — Content (AdSense-grade original writing)

**Prompt**

> Write original, sourced, people-first content. Minimum: 10 guides of 900–1,500 words each, every guide with a summary box, table of contents, practical takeaways, FAQ (with FAQPage schema), and a sources list linking to primary research. Topics:
> 1. What is the glass cliff? The complete guide
> 2. Twenty years of glass cliff research: what the evidence says (and where it disagrees)
> 3. Glass ceiling, glass cliff, glass escalator, broken rung and the labyrinth — the terms explained
> 4. Twelve red flags in a leadership offer
> 5. How to negotiate a turnaround role: the protections to ask for
> 6. The first 100 days of a turnaround leadership role
> 7. For boards: how to appoint a crisis leader without setting them up to fail
> 8. Race, ethnicity and the "saviour effect"
> 9. The glass cliff in politics and the public sector
> 10. Is a crisis role a career accelerator? When to say yes
>
> Also: Research Library with full citations (Ryan & Haslam 2005, 2007; Haslam & Ryan 2008; Ryan, Haslam & Kulich 2010; Bruckmüller & Branscombe 2010; Ryan et al. 2011; Adams, Gupta & Leeth 2009; Cook & Glass 2014; Sabharwal 2015; Ryan et al. 2016; Morgenroth et al. 2020; newer 2025 work), a 30-term glossary, FAQ, About, Editorial Policy. Present the scientific debate honestly, including null findings.

**Acceptance:** no thin pages; every factual claim about research links to a source; no named living person is labelled a glass-cliff case.

---

## Phase 5 — Interactive tools

**Prompt**

> Build five client-side tools in vanilla JavaScript (no backend):
> 1. **Glass Cliff Risk Scanner** — 12 weighted questions about the organisation's condition, the mandate, resources, support and exit terms. Output: 0–100 risk score, band (Solid ground / Watch the edge / Glass cliff / Free fall), the top red flags and matching negotiation asks. Offer "Email me a copy" and "Get a confidential review" which pre-fills the lead form with the score.
> 2. **Offer Protection Builder** — pick the risks you see; generate a prioritised list of protections (mandate letter, resource commitments, board sponsor, severance and change-of-control terms, D&O cover, success metrics with a realistic horizon, communications plan). Copy and print.
> 3. **Turnaround 100-Day Planner** — choose situation type (financial distress, reputational crisis, toxic culture, post-scandal, broken growth) and team size; output a three-phase plan (Days 1–30 diagnose, 31–60 stabilise, 61–100 commit) with weekly checkpoints. Print-ready.
> 4. **Crisis Leadership Readiness Check** — 15 statements on a 5-point scale across five dimensions; radar-style bar output and development suggestions.
> 5. **Board Appointment Check** — 12 yes/no checks for appointing committees; output a support score and the gaps to close; CTA to Board Appointment Review.
>
> Tools save progress to `localStorage` (wrapped in try/catch) and never send data unless the user submits a form.

**Acceptance:** all tools work with keyboard only, on mobile, and with JavaScript errors = 0 in the console.

---

## Phase 6 — Lead generation engine and forms

**Prompt**

> Build a dedicated lead-generation section (`get-help.html`) — the highest-converting page on the site:
> - Two paths side by side: "I'm weighing or holding a high-risk role" and "We're appointing or supporting a leader".
> - Multi-step form (4 steps, progress bar): situation, role and timeline, help needed and budget band, contact and consent. Pre-fill from tool results and UTM parameters.
> - Lead score 0–100 (urgency, seniority, budget, timeline, tool score), first landing page, referrer, UTM tags attached as hidden fields.
> - Trust elements: confidentiality promise, response-time promise, how it works in three steps, FAQ, what happens to your data.
> - Exit points: every guide ends with a contextual CTA; every tool result has a CTA; sticky mobile "Get a confidential review" button.
>
> Form delivery: all forms POST via `fetch` to FormSubmit's AJAX endpoint. The owner inbox is assembled at runtime from an encoded key in `assets/js/config.js` (reverse the address, base64-encode it, split into two parts). The plain address must never appear in HTML, page text, JSON, README or this prompt. After FormSubmit's one-time activation, replace the encoded key with the random alias FormSubmit issues. A "Write to us" link builds its `mailto:` only on click. Include a honeypot field and disable FormSubmit captcha only if the honeypot is present.

**Acceptance:** `grep` for the owner address across the repo returns zero matches; each form shows inline validation, a sending state, success redirect to `thank-you.html`, and an error message with a retry.

---

## Phase 7 — Monetisation surfaces

**Prompt**

> 1. **AdSense:** place the exact tag `<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>` in the `<head>` of every content page, plus `<meta name="google-adsense-account" content="ca-pub-6620975821265271">`. Leave it off `thank-you.html` and `404.html` (no publisher content). Root `ads.txt`: `google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0`. Use Auto ads; never place ads inside forms or next to buttons.
> 2. **Owner bar:** at the very top of every page: "Contact, if you are interested in this website/domain name/Sponsorship/Advertisement/Partnership" linking to `https://web.works/contact`.
> 3. **Support page:** one-time and monthly tiers, a custom amount, and a clear "where the money goes" split (operations, promotion and marketing, hiring talent, contests and prizes). Pledge mode until payment links (PayPal.me, Stripe Payment Link, Buy Me a Coffee, Ko-fi) are pasted into `config.js`.
> 4. **Contests and prizes:** quarterly "Edge Prize" challenges (Turnaround Case Challenge, Student Research Brief, Leadership Story) with live countdowns, rules, judging criteria, prize table and entry form. Sponsor slot for each contest.
> 5. **Careers:** open roles (contributing editor, research analyst, community moderator, partnerships lead, video producer, campus ambassadors), talent-pool form.
> 6. **Advertise and sponsor:** packages with launch rates (newsletter, tool sponsorship, contest sponsorship, report sponsorship, directory featured listing), no invented audience numbers, enquiry form.
> 7. **Video library:** YouTube embeds via privacy-enhanced `youtube-nocookie.com` behind click-to-load facades; only verified video IDs.

**Acceptance:** owner bar visible on every page at 320px width; AdSense tag present in every content page head; `ads.txt` resolves at the root.

---

## Phase 8 — Automation and self-updating content

**Prompt**

> - Generate the site from a Python build script (`_build/build.py`) so header, footer, owner bar, AdSense tag and SEO tags come from one template.
> - `python3 _build/build.py --news` fetches Google News RSS for a set of leadership queries, keeps headline, source, date and link only (no article text), writes `data/news.json` and re-renders the News page and home feed.
> - GitHub Actions workflow `.github/workflows/site.yml` rebuilds on every source push and runs daily; it commits only if something changed and requests a Pages build.
> - In the browser: "Edge note of the day" rotates by date, contest countdowns roll to the next quarter automatically, news refreshes from `data/news.json`, copyright year updates itself.

**Acceptance:** running the build twice with no new news produces no diff; the workflow uses only `GITHUB_TOKEN`.

---

## Phase 9 — Compliance

**Prompt**

> - AdSense programme policies: original content, clear navigation, About/Contact/Privacy present, no prohibited content, no incentivised clicks, no ads on non-content pages, cookie notice, Privacy Policy that names Google's use of cookies and links to Google's ad-settings and partner-sites pages.
> - Trademark/copyright disclosure: "glass cliff" is a descriptive academic term; Glasscliff.com is an independent publication not affiliated with any company, product or person using "Glasscliff", "Glass Cliff" or similar names; all third-party names and marks belong to their owners; videos are embedded through YouTube's own player; research is cited, not reproduced.
> - Content disclaimers: educational information, not legal, financial or employment advice.
> - Privacy: forms collect only what is needed; consent checkbox; data used only to respond; retention and deletion request route.

**Acceptance:** Disclaimer page carries the trademark/copyright disclosure; footer links to it from every page.

---

## Phase 10 — SEO and performance

**Prompt**

> Unique title and meta description per page; canonical URLs on `https://glasscliff.com`; Open Graph and Twitter cards with a 1200×630 image; JSON-LD (Organization, WebSite with SearchAction, Article for guides, FAQPage, BreadcrumbList); XML and HTML sitemaps; internal linking between guides, tools and the lead form; lazy-loaded video; fonts with `display=swap`; total CSS < 40 KB, JS < 60 KB.

**Acceptance:** every page has exactly one `<h1>`; no broken internal links; sitemap lists every indexable page.

---

## Phase 11 — Deploy and launch

**Prompt**

> Push to `github.com/WEBWORKSA1/glasscliff-com` on `main`. Enable Pages: Settings → Pages → Deploy from a branch → `main` / root. When ready to apply for AdSense, point glasscliff.com at GitHub Pages (A records 185.199.108.153, .109.153, .110.153, .111.153; `www` CNAME to `webworksa1.github.io`), set the custom domain in Pages, enforce HTTPS, confirm `https://glasscliff.com/ads.txt` resolves, then apply in AdSense and enable the Google-certified consent message for EEA/UK/CH.

**Acceptance:** live URL loads; forms deliver after FormSubmit activation; AdSense site status moves to "Getting ready".

---

## Phase 12 — First 90 days of growth

1. Weeks 1–2: submit sitemap to Google Search Console and Bing; activate FormSubmit; paste payment links.
2. Weeks 3–6: publish one new guide per week (targets: "glass cliff examples", "glass cliff vs glass ceiling", "how to negotiate an executive offer", "interim CEO", "turnaround CEO first 100 days"); launch the Pulse Survey on LinkedIn.
3. Weeks 7–10: recruit 10 founding advisers into the Advisor Network; open the first Edge Prize with a sponsor.
4. Weeks 11–13: publish the first "Glass Cliff Pulse" report from survey data (gated PDF = lead magnet); pitch it to HR and business press.
