/* Glasscliff.com — the five interactive tools. Everything runs in the browser; nothing is sent unless the user submits a form. */
(function () {
  "use strict";
  var G = window.GC || {}, $ = G.$, $$ = G.$$, esc = G.esc, store = G.store, ROOT = G.root || "";

  function save(key, form) { var o = {}; new FormData(form).forEach(function (v, k) { o[k] = v; }); store.set(key, JSON.stringify(o)); }
  function load(key, form) {
    var raw = store.get(key); if (!raw) return;
    try { var o = JSON.parse(raw); Object.keys(o).forEach(function (k) { $$('[name="' + k + '"]', form).forEach(function (el) { if (el.type === "radio" || el.type === "checkbox") el.checked = el.value === o[k] || (el.type === "checkbox" && o[k] === "on"); else el.value = o[k]; }); }); } catch (e) {}
  }
  function gauge(el, score) {
    var n = $(".needle", el); if (n) n.style.transform = "rotate(" + (-90 + score * 1.8) + "deg)";
  }
  $$("[data-print]").forEach(function (b) { b.addEventListener("click", function () { window.print(); }); });
  $$("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      var t = $(b.getAttribute("data-copy")); if (!t) return;
      var txt = t.innerText;
      (navigator.clipboard ? navigator.clipboard.writeText(txt) : Promise.reject()).then(function () { b.textContent = "Copied"; }, function () { b.textContent = "Select and copy manually"; });
      setTimeout(function () { b.textContent = "Copy list"; }, 2500);
    });
  });

  /* 1. Glass Cliff Risk Scanner */
  (function () {
    var f = $("#risk-scanner"); if (!f) return;
    var Q = {
      q1: { w: 1.2, flag: "The organisation is already in visible crisis.", ask: "Get the starting position documented and acknowledged by the board, so you are judged on the trend, not the level." },
      q2: { w: 1.1, flag: "Your mandate is not in writing.", ask: "Ask for a mandate letter: scope, decision rights, what success looks like at 100 days, 12 months and 3 years." },
      q3: { w: 1.1, flag: "Resources are missing or only promised verbally.", ask: "Put budget, headcount and investment commitments in the offer letter or board minute." },
      q4: { w: 1.0, flag: "The timeline to show results is very short.", ask: "Negotiate a realistic horizon and interim milestones that measure direction of travel." },
      q5: { w: 0.9, flag: "Your predecessor left under pressure, or the seat turns over fast.", ask: "Ask the board directly why the last leaders left, and what will be different for you." },
      q6: { w: 1.1, flag: "There is no named sponsor, or the board is divided.", ask: "Name a board sponsor with authority and agree a regular, private check-in." },
      q7: { w: 0.8, flag: "Others may have turned the role down first.", ask: "Find out who declined and why. Their reasons are your risk register." },
      q8: { w: 0.9, flag: "You cannot shape your own leadership team.", ask: "Secure the right to make a defined number of senior appointments in the first 6 months." },
      q9: { w: 0.9, flag: "You cannot see the real numbers before you sign.", ask: "Make access to finances, legal exposure and people data a condition of acceptance." },
      q10: { w: 0.8, flag: "Exit terms leave you exposed if it goes wrong.", ask: "Negotiate severance, change-of-control and indemnity (D&O) cover before you start." },
      q11: { w: 0.8, flag: "The crisis is not openly acknowledged.", ask: "Agree an internal (and if needed, public) statement of the situation you are inheriting." },
      q12: { w: 0.6, flag: "You would be a ‘first’ or atypical leader in this seat, which research links to extra scrutiny.", ask: "Build a visible support coalition early: sponsor, peer network, external coach." }
    };
    var hero = new URLSearchParams(location.search);
    if (hero.get("q1")) { var v1 = hero.get("q1") === "yes" ? "10" : "0"; var r1 = $('input[name="q1"][value="' + v1 + '"]', f); if (r1) r1.checked = true; }
    if (hero.get("q2")) { var v2 = hero.get("q2") === "yes" ? "0" : "10"; var r2 = $('input[name="q2"][value="' + v2 + '"]', f); if (r2) r2.checked = true; }
    if (hero.get("q3")) { var v3 = hero.get("q3") === "yes" ? "0" : "10"; var r3 = $('input[name="q3"][value="' + v3 + '"]', f); if (r3) r3.checked = true; }
    if (!hero.get("q1")) load("gc_scan", f);
    var out = $("#scan-result");
    function calc() {
      var num = 0, den = 0, answered = 0, items = [];
      Object.keys(Q).forEach(function (k) {
        var c = $('input[name="' + k + '"]:checked', f); if (!c) return;
        var v = parseFloat(c.value); answered++;
        num += v * Q[k].w; den += 10 * Q[k].w;
        if (v >= 6) items.push({ k: k, s: v * Q[k].w });
      });
      $("#scan-count").textContent = answered + " of 12 answered";
      if (answered < 6) { out.hidden = true; $("#scan-wait").hidden = false; return; }
      out.hidden = false; $("#scan-wait").hidden = true;
      var score = Math.round(num / den * 100);
      var b = score < 30 ? 0 : score < 50 ? 1 : score < 70 ? 2 : 3;
      var names = ["Solid ground", "Watch the edge", "Glass cliff", "Free fall"];
      var tips = [
        "The role looks well supported. Still get the mandate and exit terms in writing.",
        "Real risks, but negotiable. Fix the top items below before you sign.",
        "High risk of being set up to fail. Only accept with the protections below agreed in writing.",
        "The conditions for success are missing. Walk away, or rebuild the offer from scratch."
      ];
      gauge($("#scan-gauge"), score);
      $("#scan-score").textContent = score;
      var bandEl = $("#scan-band"); bandEl.textContent = names[b]; bandEl.className = "band b" + b;
      $("#scan-tip").textContent = tips[b];
      items.sort(function (a, c) { return c.s - a.s; });
      var top = items.slice(0, 5);
      $("#scan-flags").innerHTML = top.length ? top.map(function (i) { return "<li>" + esc(Q[i.k].flag) + "</li>"; }).join("") : "<li>No major red flags in your answers.</li>";
      $("#scan-asks").innerHTML = top.length ? top.map(function (i) { return "<li>" + esc(Q[i.k].ask) + "</li>"; }).join("") : "<li>Confirm your mandate, resources and exit terms in writing anyway.</li>";
      var cta = $("#scan-cta"); if (cta) cta.href = ROOT + "get-help.html?path=leader&tool=Risk%20Scanner&tool_score=" + score;
      var hidden = $("#scan-email-form");
      if (hidden) { hidden.elements.score.value = score + " (" + names[b] + ")"; hidden.elements.flags.value = top.map(function (i) { return Q[i.k].flag; }).join(" | "); hidden.elements.asks.value = top.map(function (i) { return Q[i.k].ask; }).join(" | "); }
      save("gc_scan", f);
    }
    f.addEventListener("change", calc);
    $("#scan-reset").addEventListener("click", function () { f.reset(); store.set("gc_scan", "{}"); calc(); });
    calc();
  })();

  /* 2. Offer Protection Builder */
  (function () {
    var f = $("#offer-builder"); if (!f) return;
    var P = {
      mandate: [1, "Mandate letter", "Scope, decision rights and success measures at 100 days, 12 months and 3 years, signed by the chair or appointing body."],
      baseline: [1, "Agreed baseline", "A written statement of the condition you inherit (finances, legal exposure, morale), minuted by the board."],
      resources: [1, "Resource commitments in writing", "Budget, headcount and investment named in the offer or a board resolution, not a conversation."],
      horizon: [1, "Realistic time horizon", "Milestones that measure direction of travel, with a review date no earlier than 12 to 18 months."],
      sponsor: [1, "Named board sponsor", "One person with authority who meets you privately every two weeks for the first 6 months."],
      severance: [1, "Severance and change-of-control terms", "Protection if you are removed without cause, the strategy changes, or the organisation is sold."],
      dando: [2, "Indemnity and D&O insurance", "Confirm cover for decisions taken in good faith, including for pre-existing liabilities you inherit."],
      team: [2, "Right to build your team", "Authority to make a defined number of senior appointments and exits in the first 6 months."],
      dataroom: [1, "Pre-signing information access", "Finances, litigation, regulatory findings, engagement data and the last two board evaluations."],
      comms: [2, "Communications plan", "Agreed messaging about the situation you inherit, and who speaks for the organisation when it gets hard."],
      coach: [2, "External coach and peer support", "A paid executive coach of your choosing for the first 12 months."],
      advisor: [3, "Independent advice on the contract", "An employment lawyer reviews the offer before you sign."],
      interim: [2, "Path from interim to permanent", "Written criteria and a date for the decision, plus a completion bonus if it ends."],
      chief: [2, "Chief of staff and communications support", "Dedicated support for public-facing roles where scrutiny is constant."],
      security: [3, "Personal and digital security", "Support for online abuse and safety risks that come with high-visibility roles."],
      review: [3, "Exit interview rights", "The right to a recorded, independent exit review if the appointment ends early."]
    };
    var MAP = {
      crisis: ["baseline", "horizon", "comms", "sponsor"], mandate: ["mandate", "sponsor", "review"], resources: ["resources", "horizon"],
      timeline: ["horizon", "baseline", "mandate"], board: ["sponsor", "mandate", "severance"], team: ["team", "resources"],
      info: ["dataroom", "dando", "advisor"], exit: ["severance", "dando", "advisor", "review"], first: ["coach", "sponsor", "comms", "security"],
      interim: ["interim", "severance", "mandate"]
    };
    var ROLE = { ceo: ["dando", "severance"], exec: ["coach"], interim: ["interim"], public: ["chief", "security", "comms"] };
    load("gc_offer", f);
    function build() {
      var picked = {};
      $$('input[name="risk"]:checked', f).forEach(function (c) { (MAP[c.value] || []).forEach(function (k) { picked[k] = 1; }); });
      var role = f.elements.role.value; (ROLE[role] || []).forEach(function (k) { picked[k] = 1; });
      if (Object.keys(picked).length) ["mandate", "advisor"].forEach(function (k) { picked[k] = 1; });
      var list = Object.keys(picked).map(function (k) { return P[k]; }).sort(function (a, b) { return a[0] - b[0]; });
      var out = $("#offer-list");
      $("#offer-empty").hidden = list.length > 0;
      $("#offer-actions").hidden = list.length === 0;
      out.innerHTML = list.map(function (p) { return '<li><span class="prio p' + p[0] + '">' + (p[0] === 1 ? "Must have" : p[0] === 2 ? "Strongly advised" : "Worth asking") + "</span><div><b>" + esc(p[1]) + "</b>" + esc(p[2]) + "</div></li>"; }).join("");
      $("#offer-count").textContent = list.length ? list.length + " protections to negotiate" : "";
      save("gc_offer", f);
    }
    f.addEventListener("change", build); build();
  })();

  /* 3. Turnaround 100-Day Planner */
  (function () {
    var f = $("#planner"); if (!f) return;
    var BASE = {
      p1: ["Hold 1:1s with every direct report and 20+ people two levels down; ask what they would fix first and what they are afraid to say.", "Get the real numbers: cash runway, top 10 customers, open legal and regulatory issues.", "Write and circulate a ‘state of play’ memo that records the position you inherited.", "Agree with your sponsor how and when you will report progress."],
      p2: ["Pick no more than three priorities and say no to the rest, publicly.", "Make the people decisions you have evidence for; delay the ones you do not.", "Stop the bleeding: freeze or end the activities that destroy the most value.", "Set up a weekly operating rhythm with clear owners and one dashboard."],
      p3: ["Present a 12-month plan to the board with milestones that measure direction of travel.", "Lock in resources against the plan in writing.", "Share early wins with the whole organisation and credit the people who delivered them.", "Run a private 100-day review with your sponsor: what changed, what you need next."]
    };
    var SIT = {
      finance: { name: "financial distress", p1: ["Build a 13-week cash-flow forecast and review it weekly.", "Meet lenders and the largest creditors before they hear rumours."], p2: ["Cut or pause discretionary spend with a clear rule everyone can understand.", "Prioritise the customers and products that generate cash now."], p3: ["Agree a refinancing or funding plan with the board.", "Report liquidity headroom alongside every update."] },
      reputation: { name: "reputational crisis", p1: ["Map every stakeholder affected and what they have been told so far.", "Appoint one accountable spokesperson and a single source of truth."], p2: ["Fix the underlying failure before relaunching the message.", "Commission an independent review if trust in internal findings is low."], p3: ["Publish what you changed, with evidence, not adjectives.", "Track trust indicators monthly: complaints, sentiment, retention."] },
      culture: { name: "toxic or broken culture", p1: ["Run confidential listening sessions; read every exit interview from the last two years.", "Identify the behaviours that are rewarded today, not the values on the wall."], p2: ["Act visibly on one serious behaviour case to show the rules have changed.", "Rewrite promotion and reward criteria around the behaviours you need."], p3: ["Launch a short pulse survey and commit to sharing results.", "Put culture measures into the leadership team's objectives."] },
      scandal: { name: "post-scandal clean-up", p1: ["Confirm every legal, regulatory and disclosure obligation with counsel.", "Secure documents and stop any ongoing harm immediately."], p2: ["Cooperate fully with investigators and keep the board informed in writing.", "Separate people implicated from decision-making while facts are established."], p3: ["Implement governance fixes: controls, whistleblowing, board oversight.", "Close the matter publicly only when the remediation is real."] },
      growth: { name: "growth that is breaking the organisation", p1: ["Find the bottlenecks: hiring, systems, quality and cash conversion.", "Talk to customers who left in the last six months."], p2: ["Slow down the activities growth is breaking; protect quality first.", "Bring in senior hires for the functions that are under-built."], p3: ["Set a sustainable growth target with the board.", "Invest in systems and processes that will scale for 18 months."] }
    };
    var SIZE = { small: "Keep the plan on one page and review it in person every Monday.", medium: "Cascade the three priorities to every team lead in week 5, with one owner per priority.", large: "Appoint a transformation office of 2 to 4 people by day 30 to track delivery." };
    var HIRE = { internal: "As an internal hire, name what you will do differently from your predecessor in week 1, or people will assume nothing changes.", external: "As an external hire, find two trusted insiders by day 15 who will tell you what you are missing." };
    load("gc_plan", f);
    function li(a) { return a.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join(""); }
    function render() {
      var s = SIT[f.elements.situation.value] || SIT.finance;
      var size = f.elements.size.value, hire = f.elements.hire.value;
      var start = f.elements.start.value ? new Date(f.elements.start.value + "T00:00:00") : null;
      function d(n) { if (!start || isNaN(start)) return "Day " + n; var x = new Date(start); x.setDate(x.getDate() + n - 1); return "Day " + n + ", " + x.toLocaleDateString(undefined, { month: "short", day: "numeric" }); }
      var html = "<p class=\"muted\">A plan for <b>" + esc(s.name) + "</b>. " + esc(HIRE[hire] || "") + "</p>";
      html += '<section class="plan-phase"><h3>Days 1 to 30: diagnose</h3><p class="small muted">' + d(1) + " to " + d(30) + "</p><ul>" + li(s.p1.concat(BASE.p1)) + "</ul></section>";
      html += '<section class="plan-phase"><h3>Days 31 to 60: stabilise</h3><p class="small muted">' + d(31) + " to " + d(60) + "</p><ul>" + li(s.p2.concat(BASE.p2, [SIZE[size] || ""])) + "</ul></section>";
      html += '<section class="plan-phase"><h3>Days 61 to 100: commit</h3><p class="small muted">' + d(61) + " to " + d(100) + "</p><ul>" + li(s.p3.concat(BASE.p3)) + "</ul></section>";
      html += "<h3>Weekly checkpoints</h3><ul class=\"small\"><li>Weeks 1 to 4: what did I learn that changes my view?</li><li>Weeks 5 to 9: are the three priorities moving? What did I stop?</li><li>Weeks 10 to 14: is the board seeing the same picture I am?</li></ul>";
      $("#plan-out").innerHTML = html;
      save("gc_plan", f);
    }
    f.addEventListener("change", render); f.addEventListener("input", render); render();
  })();

  /* 4. Crisis Leadership Readiness Check */
  (function () {
    var f = $("#readiness"); if (!f) return;
    var DIM = {
      diag: ["Diagnosis", "Spend your first weeks asking, not telling: structured listening, a written state-of-play memo, and one trusted outsider to test your read."],
      dec: ["Decisions under pressure", "Practise ‘good enough’ decisions with explicit review dates. Pre-agree which decisions you will make alone and which need the board."],
      comm: ["Communication", "Say what you know, what you do not, and when you will update. Rehearse hard conversations with a coach before you have them for real."],
      coal: ["Coalition building", "Map your sponsors, allies, neutrals and blockers. Invest in two allies outside your reporting line every month."],
      resil: ["Personal resilience", "Protect sleep, keep one non-work commitment, and agree with someone close what ‘too much’ looks like for you."]
    };
    var out = $("#ready-out");
    load("gc_ready", f);
    function calc() {
      var tot = {}, cnt = {}, n = 0;
      $$("fieldset[data-dim]", f).forEach(function (fs) {
        var dim = fs.getAttribute("data-dim"), c = $("input:checked", fs);
        if (!c) return; n++;
        tot[dim] = (tot[dim] || 0) + parseInt(c.value, 10); cnt[dim] = (cnt[dim] || 0) + 1;
      });
      $("#ready-count").textContent = n + " of 15 answered";
      if (n < 15) { out.hidden = true; $("#ready-wait").hidden = false; save("gc_ready", f); return; }
      out.hidden = false; $("#ready-wait").hidden = true;
      var rows = Object.keys(DIM).map(function (k) { return [k, Math.round(((tot[k] / cnt[k]) - 1) / 4 * 100)]; });
      var overall = Math.round(rows.reduce(function (a, r) { return a + r[1]; }, 0) / rows.length);
      $("#ready-score").textContent = overall;
      $("#ready-bars").innerHTML = rows.map(function (r) { return '<div class="bar"><span>' + DIM[r[0]][0] + '</span><span class="track"><span class="fill" style="width:' + r[1] + '%"></span></span><b>' + r[1] + "</b></div>"; }).join("");
      var sorted = rows.slice().sort(function (a, b) { return a[1] - b[1]; });
      $("#ready-strong").textContent = DIM[sorted[sorted.length - 1][0]][0];
      $("#ready-tips").innerHTML = sorted.slice(0, 2).map(function (r) { return "<li><b>" + DIM[r[0]][0] + ".</b> " + esc(DIM[r[0]][1]) + "</li>"; }).join("");
      var cta = $("#ready-cta"); if (cta) cta.href = ROOT + "get-help.html?path=leader&tool=Readiness%20Check&tool_score=" + (100 - overall);
      save("gc_ready", f);
    }
    f.addEventListener("change", calc); calc();
  })();

  /* 5. Board Appointment Check */
  (function () {
    var f = $("#board-check"); if (!f) return;
    load("gc_board", f);
    function calc() {
      var qs = $$("fieldset.q", f), yes = 0, ans = 0, gaps = [];
      qs.forEach(function (q) { var c = $("input:checked", q); if (!c) return; ans++; if (c.value === "yes") yes++; else gaps.push(q.getAttribute("data-gap")); });
      $("#board-count").textContent = ans + " of " + qs.length + " answered";
      if (ans < qs.length) { $("#board-out").hidden = true; $("#board-wait").hidden = false; save("gc_board", f); return; }
      $("#board-out").hidden = false; $("#board-wait").hidden = true;
      var score = Math.round(yes / qs.length * 100);
      gauge($("#board-gauge"), score);
      $("#board-score").textContent = score;
      var b = score >= 80 ? 0 : score >= 60 ? 1 : score >= 40 ? 2 : 3;
      var bandEl = $("#board-band"); bandEl.className = "band b" + b;
      bandEl.textContent = ["Well supported appointment", "Some gaps to close", "Likely glass cliff", "Set up to fail"][b];
      $("#board-gaps").innerHTML = gaps.length ? gaps.map(function (g) { return "<li>" + esc(g) + "</li>"; }).join("") : "<li>No gaps in your answers. Re-run the check at 6 months.</li>";
      var cta = $("#board-cta"); if (cta) cta.href = ROOT + "get-help.html?path=organisation&tool=Board%20Appointment%20Check&tool_score=" + (100 - score);
      save("gc_board", f);
    }
    f.addEventListener("change", calc); calc();
  })();
})();
