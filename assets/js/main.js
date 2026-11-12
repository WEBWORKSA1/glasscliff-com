/* Glasscliff.com — site behaviour: navigation, forms, lead scoring, self-updating widgets. No dependencies. */
(function () {
  "use strict";
  var CFG = window.GC_CONFIG || {};
  var ROOT = document.body.getAttribute("data-root") || "";
  var store = {
    get: function (k, s) { try { return (s ? sessionStorage : localStorage).getItem(k); } catch (e) { return null; } },
    set: function (k, v, s) { try { (s ? sessionStorage : localStorage).setItem(k, v); } catch (e) {} }
  };
  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }
  function esc(t) { return String(t == null ? "" : t).replace(/[&<>"']/g, function (m) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m]; }); }
  window.GC = { $: $, $$: $$, esc: esc, store: store, root: ROOT };

  /* Inbox, assembled only at the moment it is needed */
  function inbox() {
    if (CFG.formAlias) return CFG.formAlias;
    try { return atob((CFG.relay || []).join("")).split("").reverse().join(""); } catch (e) { return ""; }
  }

  /* Year */
  $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* Mobile navigation */
  var menuBtn = $(".menu-btn"), nav = $("#site-nav");
  if (menuBtn && nav) {
    menuBtn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) { nav.classList.remove("open"); menuBtn.setAttribute("aria-expanded", "false"); menuBtn.focus(); }
    });
  }

  /* "Write to us" links: mailto is built on click, never present in the page */
  $$("[data-mail]").forEach(function (a) {
    a.addEventListener("click", function (e) {
      var to = inbox(); if (!to || to.indexOf("@") < 0) return;
      e.preventDefault();
      var subj = a.getAttribute("data-mail") || "Glasscliff enquiry";
      window.location.href = "mailto:" + to + "?subject=" + encodeURIComponent(subj);
    });
  });

  /* First-touch attribution */
  (function () {
    var p = new URLSearchParams(location.search);
    if (!store.get("gc_landing")) store.set("gc_landing", location.pathname + location.search);
    if (!store.get("gc_ref") && document.referrer && document.referrer.indexOf(location.host) < 0) store.set("gc_ref", document.referrer);
    ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content"].forEach(function (k) { if (p.get(k)) store.set("gc_" + k, p.get(k)); });
  })();

  /* Cookie notice */
  (function () {
    if (store.get("gc_cookie_ok")) return;
    var box = document.createElement("div");
    box.className = "cookie"; box.setAttribute("role", "region"); box.setAttribute("aria-label", "Cookie notice");
    box.innerHTML = '<p>We use cookies for essential site features and, through Google AdSense, to show and measure ads. See our <a href="' + ROOT + 'privacy.html">privacy policy</a>.</p><button class="btn btn-dark btn-sm" type="button">OK, got it</button>';
    document.body.appendChild(box);
    box.querySelector("button").addEventListener("click", function () { store.set("gc_cookie_ok", "1"); box.remove(); });
  })();

  /* Hero edge test */
  (function () {
    var f = $("#edge-test"); if (!f) return;
    var mark = $(".edge-meter i", f), label = $(".edge-label", f), link = $("#edge-link");
    var weights = { crisis: 35, mandate: 30, resources: 25 };
    function band(s) { return s < 30 ? "Solid ground" : s < 55 ? "Watch the edge" : s < 80 ? "Glass cliff" : "Free fall"; }
    function update() {
      var s = 10;
      if ((f.crisis || {}).value === "yes") s += weights.crisis;
      if ((f.mandate || {}).value === "no") s += weights.mandate;
      if ((f.resources || {}).value === "no") s += weights.resources;
      mark.style.left = Math.min(96, Math.max(4, s)) + "%";
      label.textContent = band(s);
      if (link) link.href = ROOT + "tools/risk-scanner.html?q1=" + ((f.crisis || {}).value || "") + "&q2=" + ((f.mandate || {}).value || "") + "&q3=" + ((f.resources || {}).value || "");
    }
    f.addEventListener("change", update); update();
  })();

  /* Edge note of the day — rotates by date */
  (function () {
    var el = $("[data-note-of-day]"); if (!el) return;
    var notes = [
      ["Ask who said no to this role before you. Their reasons are your risk register.", "Offer due diligence"],
      ["A mandate that is not written down is a mandate that can be rewritten after you fail.", "Negotiation"],
      ["Crisis roles are judged on the trend, not the level. Agree the baseline on day one.", "Success metrics"],
      ["The board sponsor matters more than the title. Name yours before you sign.", "Support"],
      ["Resources promised verbally have a half-life of about one quarter.", "Resourcing"],
      ["If the timeline to turn it around is shorter than the timeline to hire your team, it is a trap.", "Timelines"],
      ["Visibility of the crisis protects you. Make the starting position public, internally at least.", "Communication"],
      ["Severance is cheapest to negotiate when they need you most: before you start.", "Exit terms"],
      ["The first 30 days are for diagnosis. Announcing a plan in week one is a gift to your critics.", "First 100 days"],
      ["A turnaround that needs a culture change needs more than one budget cycle.", "Timelines"],
      ["Boards: if you would not offer this package to the last leader, ask why you are offering it to this one.", "For boards"],
      ["Measure the support around a leader, not just the leader.", "For boards"],
      ["Being first is a story. Being set up to succeed is a strategy.", "Career strategy"],
      ["Write down what ‘done’ looks like at 100 days, 12 months and 3 years. Then get it agreed.", "Mandate"]
    ];
    var d = new Date(), start = new Date(d.getFullYear(), 0, 0);
    var day = Math.floor((d - start) / 864e5);
    var n = notes[day % notes.length];
    el.innerHTML = esc(n[0]) + "<cite>Edge note of the day, on " + esc(n[1].toLowerCase()) + "</cite>";
  })();

  /* Quarterly countdowns (contests roll over automatically) */
  function quarterEnd(offset) {
    var d = new Date(); var q = Math.floor(d.getUTCMonth() / 3) + (offset || 0);
    return new Date(Date.UTC(d.getUTCFullYear(), q * 3 + 3, 0, 23, 59, 59));
  }
  window.GC.quarterEnd = quarterEnd;
  $$("[data-countdown]").forEach(function (el) {
    var end = quarterEnd(parseInt(el.getAttribute("data-countdown"), 10) || 0);
    var out = $("[data-deadline]", el.parentNode) || null;
    if (out) out.textContent = end.toLocaleDateString(undefined, { year: "numeric", month: "long", day: "numeric", timeZone: "UTC" });
    function tick() {
      var ms = Math.max(0, end - new Date());
      var dd = Math.floor(ms / 864e5), hh = Math.floor(ms / 36e5) % 24, mm = Math.floor(ms / 6e4) % 60;
      el.innerHTML = "<div><b>" + dd + "</b><small>days</small></div><div><b>" + hh + "</b><small>hours</small></div><div><b>" + mm + "</b><small>minutes</small></div>";
    }
    tick(); setInterval(tick, 30000);
  });
  $$("[data-quarter-label]").forEach(function (el) {
    var d = new Date(); el.textContent = "Q" + (Math.floor(d.getUTCMonth() / 3) + 1) + " " + d.getUTCFullYear();
  });

  /* Leadership news — refreshes from data/news.json (updated daily by the site's automation) */
  $$("[data-news]").forEach(function (list) {
    var limit = parseInt(list.getAttribute("data-news"), 10) || 8;
    fetch(ROOT + "data/news.json", { cache: "no-cache" }).then(function (r) { return r.ok ? r.json() : null; }).then(function (data) {
      if (!data || !data.items || !data.items.length) return;
      list.innerHTML = data.items.slice(0, limit).map(function (it) {
        var dt = it.date ? new Date(it.date) : null;
        var when = dt && !isNaN(dt) ? dt.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" }) : "";
        return '<li><a href="' + esc(it.link) + '" target="_blank" rel="noopener nofollow">' + esc(it.title) + '</a><span class="src">' + esc(it.source || "") + (when ? ", " + when : "") + "</span></li>";
      }).join("");
      $$("[data-news-updated]").forEach(function (u) { if (data.updated) u.textContent = new Date(data.updated).toLocaleString(undefined, { dateStyle: "medium", timeStyle: "short" }); });
    }).catch(function () {});
  });

  /* Video facades: load the player only when asked */
  $$("[data-yt],[data-ted]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var frame = btn.parentNode, src;
      if (btn.hasAttribute("data-yt")) src = "https://www.youtube-nocookie.com/embed/" + btn.getAttribute("data-yt") + "?autoplay=1&rel=0";
      else src = "https://embed.ted.com/talks/" + btn.getAttribute("data-ted");
      var ifr = document.createElement("iframe");
      ifr.src = src; ifr.title = btn.getAttribute("aria-label") || "Video";
      ifr.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
      ifr.allowFullscreen = true; ifr.loading = "lazy";
      frame.innerHTML = ""; frame.appendChild(ifr);
    });
  });

  /* Prefill any form field from the URL (tool → lead form hand-off) */
  (function () {
    var p = new URLSearchParams(location.search);
    $$("form[data-gc-form]").forEach(function (f) {
      p.forEach(function (v, k) {
        var el = f.elements[k]; if (!el) return;
        if (el.length && el[0] && el[0].type === "radio") { $$('input[name="' + k + '"]', f).forEach(function (r) { r.checked = r.value === v; }); }
        else if (el.type !== "file") el.value = v;
      });
    });
  })();

  /* Lead score: 0–100 from urgency, seniority, budget, timeline and any tool score */
  function leadScore(fd) {
    var s = 0;
    var sen = { "Board / chair": 20, "CEO / president / head of organisation": 20, "C-suite / executive": 17, "VP / director": 12, "Senior manager": 8, "Elected or public office": 15, "Other": 4 };
    var time = { "Offer on the table now": 25, "Starting within 3 months": 20, "Already in the role": 18, "Exploring options": 8 };
    var bud = { "US$10,000+": 25, "US$3,000 – 10,000": 20, "US$1,000 – 3,000": 14, "Under US$1,000": 6, "Organisation is paying": 22, "Not sure yet": 6 };
    s += sen[fd.get("seniority")] || 0;
    s += time[fd.get("timeline")] || 0;
    s += bud[fd.get("budget")] || 0;
    var ts = parseInt(fd.get("tool_score") || "0", 10); if (ts) s += Math.round(ts / 100 * 20);
    if ((fd.get("situation") || "").length > 140) s += 5;
    if (fd.get("phone")) s += 5;
    return Math.min(100, s);
  }

  /* Field validation */
  function validate(scope) {
    var ok = true, first = null;
    $$("input,select,textarea", scope).forEach(function (el) {
      if (el.disabled || el.type === "hidden" || el.classList.contains("hp")) return;
      var wrap = el.closest(".field") || el.parentNode;
      var errEl = wrap && $(".err", wrap);
      var bad = !el.checkValidity();
      if (el.type === "radio" && el.required) bad = !$$('input[name="' + el.name + '"]', scope).some(function (r) { return r.checked; });
      if (wrap && wrap.classList) wrap.classList.toggle("invalid", bad);
      if (errEl) errEl.textContent = bad ? (el.type === "email" ? "Enter an email address like name@example.com." : el.type === "checkbox" ? "Tick this box to continue." : "This field is required.") : "";
      if (bad) { ok = false; if (!first) first = el; }
    });
    if (first) first.focus();
    return ok;
  }
  window.GC.validate = validate;

  /* Multi-step forms */
  $$("form[data-steps]").forEach(function (f) {
    var steps = $$(".step", f), bar = $$(".steps-bar li", f), i = 0;
    function show(n, user) {
      steps.forEach(function (s, k) { s.hidden = k !== n; });
      bar.forEach(function (b, k) { b.className = k < n ? "done" : k === n ? "now" : ""; if (k === n) b.setAttribute("aria-current", "step"); else b.removeAttribute("aria-current"); });
      i = n;
      if (!user) return;
      var h = $("h2,h3,legend", steps[n]); if (h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); }
      f.scrollIntoView({ behavior: "smooth", block: "start" });
    }
    $$("[data-next]", f).forEach(function (b) { b.addEventListener("click", function () { if (validate(steps[i])) show(Math.min(steps.length - 1, i + 1), true); }); });
    $$("[data-back]", f).forEach(function (b) { b.addEventListener("click", function () { show(Math.max(0, i - 1), true); }); });
    show(0);
  });

  /* Form delivery through FormSubmit (AJAX). */
  $$("form[data-gc-form]").forEach(function (f) {
    f.setAttribute("novalidate", "");
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = $(".form-msg", f), btn = $('[type="submit"]', f);
      if (!validate(f)) { if (msg) { msg.className = "form-msg bad"; msg.textContent = "Check the highlighted fields."; } return; }
      if (f.elements._honey && f.elements._honey.value) return;
      var name = f.getAttribute("data-gc-form");
      var fd = new FormData(f);
      fd.append("_subject", "Glasscliff.com: " + (f.getAttribute("data-subject") || name) + (fd.get("name") ? " from " + fd.get("name") : ""));
      fd.append("_template", "table");
      fd.append("_captcha", "false");
      fd.append("form", name);
      fd.append("page", location.href);
      fd.append("first_landing", store.get("gc_landing") || "");
      fd.append("referrer", store.get("gc_ref") || "");
      ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content"].forEach(function (k) { var v = store.get("gc_" + k); if (v) fd.append(k, v); });
      if (f.hasAttribute("data-score")) fd.append("lead_score", leadScore(fd));
      if (fd.get("email")) fd.append("_replyto", fd.get("email"));
      var to = inbox();
      if (!to) { if (msg) { msg.className = "form-msg bad"; msg.textContent = "The form is not configured yet. Please use the contact page."; } return; }
      if (btn) { btn.disabled = true; btn.setAttribute("data-label", btn.textContent); btn.textContent = "Sending…"; }
      if (msg) { msg.className = "form-msg"; msg.textContent = ""; }
      var payload = {};
      fd.forEach(function (v, k) { if (typeof v !== "string") return; payload[k] = payload[k] ? payload[k] + ", " + v : v; });
      fetch("https://formsubmit.co/ajax/" + encodeURIComponent(to), { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" }, body: JSON.stringify(payload) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, j: j }; }); })
        .then(function (res) {
          if (!res.ok || res.j.success === "false" || res.j.success === false) throw new Error(res.j.message || "Delivery failed");
          store.set("gc_last_form", name);
          var go = f.getAttribute("data-redirect");
          if (go) { location.href = ROOT + go; return; }
          if (msg) { msg.className = "form-msg ok"; msg.textContent = f.getAttribute("data-ok") || "Thanks. You are on the list."; }
          f.reset();
        })
        .catch(function () {
          if (msg) { msg.className = "form-msg bad"; msg.textContent = "Your message did not send. Check your connection and press the button again."; }
        })
        .then(function () { if (btn) { btn.disabled = false; btn.textContent = btn.getAttribute("data-label") || "Send"; } });
    });
  });

  /* Support page: payment links (pledge mode until links are configured) */
  (function () {
    var box = $("#pay-links"); if (!box) return;
    var p = CFG.payments || {}, names = { paypal: "PayPal", stripe: "Card (Stripe)", buymeacoffee: "Buy Me a Coffee", kofi: "Ko-fi" };
    var html = Object.keys(names).filter(function (k) { return p[k]; }).map(function (k) {
      return '<a class="btn btn-primary" href="' + esc(p[k]) + '" target="_blank" rel="noopener">Give with ' + names[k] + "</a>";
    }).join("");
    if (html) { box.innerHTML = html; box.hidden = false; var pm = $("#pledge-mode-note"); if (pm) pm.hidden = true; }
  })();
  $$("[data-amount]").forEach(function (b) {
    b.addEventListener("click", function () {
      var f = $("#pledge-form"); if (!f) return;
      f.elements.amount.value = b.getAttribute("data-amount");
      if (b.getAttribute("data-frequency") && f.elements.frequency) f.elements.frequency.value = b.getAttribute("data-frequency");
      f.scrollIntoView({ behavior: "smooth" }); f.elements.amount.focus();
    });
  });
  $$("[data-prize]").forEach(function (el) { var i = parseInt(el.getAttribute("data-prize"), 10); if ((CFG.prizes || [])[i]) el.textContent = CFG.prizes[i]; });
  $$("[data-plan]").forEach(function (el) { var k = el.getAttribute("data-plan"); if ((CFG.advisorPlans || {})[k]) el.textContent = CFG.advisorPlans[k]; });
  $$("[data-reply-time]").forEach(function (el) { if (CFG.replyTime) el.textContent = CFG.replyTime; });

  /* Site search */
  (function () {
    var box = $("#site-search"), out = $("#search-results"); if (!box || !out) return;
    var idx = [];
    function run() {
      var q = box.value.trim().toLowerCase();
      if (q.length < 2) { out.innerHTML = ""; return; }
      var terms = q.split(/\s+/);
      var hits = idx.map(function (d) {
        var hay = (d.t + " " + d.d + " " + d.k).toLowerCase(), sc = 0;
        terms.forEach(function (t) { if (hay.indexOf(t) > -1) sc += d.t.toLowerCase().indexOf(t) > -1 ? 3 : 1; });
        return [sc, d];
      }).filter(function (x) { return x[0] > 0; }).sort(function (a, b) { return b[0] - a[0]; }).slice(0, 20);
      out.innerHTML = hits.length ? hits.map(function (h) { return '<li><a href="' + ROOT + esc(h[1].u) + '">' + esc(h[1].t) + "</a><p>" + esc(h[1].d) + "</p></li>"; }).join("") : '<li>No matches for "' + esc(q) + '". Try a broader word such as "offer", "board" or "negotiate".</li>';
    }
    fetch(ROOT + "data/search.json").then(function (r) { return r.json(); }).then(function (j) {
      idx = j; var q = new URLSearchParams(location.search).get("q"); if (q) { box.value = q; } run();
    }).catch(function () {});
    box.addEventListener("input", run);
  })();
})();
