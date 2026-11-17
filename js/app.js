(function () {
  "use strict";
  const KEY = "bsg:v1";
  const app = document.getElementById("app");
  const BOOKS = window.BOOKS;
  const byId = Object.fromEntries(BOOKS.map(b => [b.id, b]));
  const cache = {};

  // ---------- storage ----------
  function load() { try { return JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { return {}; } }
  let state = load();
  state.read = state.read || {}; state.notes = state.notes || {}; state.mem = state.mem || {};
  state.tr = window.BSG_TR.valid(state.tr);
  function save() { localStorage.setItem(KEY, JSON.stringify(state)); }
  const isRead = (b, c) => !!(state.read[b] && state.read[b][c]);
  function setRead(b, c, v) { state.read[b] = state.read[b] || {}; if (v) state.read[b][c] = 1; else delete state.read[b][c]; save(); }
  const getNote = (b, c) => (state.notes[b] && state.notes[b][c]) || "";
  function setNote(b, c, t) { state.notes[b] = state.notes[b] || {}; if (t.trim()) state.notes[b][c] = t; else delete state.notes[b][c]; save(); }
  const readCount = b => Object.keys(state.read[b] || {}).length;

  // ---------- helpers ----------
  function isNative() {
    try { if (window.BSGNative && window.BSGNative.isNative) return true; } catch (e) {}
    try { if (window.Capacitor && typeof window.Capacitor.isNativePlatform === "function") return window.Capacitor.isNativePlatform(); } catch (e) {}
    return false;
  }
  const esc = s => String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const pct = (a, b) => b ? Math.round(a / b * 100) : 0;
  const bar = p => `<div class="progress" role="progressbar" aria-valuenow="${p}" aria-valuemin="0" aria-valuemax="100"><i style="width:${p}%"></i></div>`;
  const tr = () => window.BSG_TR.valid(state.tr);
  const bgUrl = ref => window.BSG_TR.bgUrl(tr(), ref);
  const refLink = (ref, book) => {
    if (!/[0-9]/.test(ref)) return esc(ref);
    const full = /^[0-9]+[:\u2013-]/.test(ref) && book ? `${book.name} ${ref}` : ref;
    return `<a href="${bgUrl(full)}" target="_blank" rel="noopener">${esc(ref)}</a>`;
  };
  function setTr(t) {
    state.tr = window.BSG_TR.valid(t);
    save();
    paintTrPicks();
    updateFooter();
    route();
  }
  function paintTrPicks() {
    const cur = tr();
    const head = document.getElementById("trPick");
    if (head) head.innerHTML = window.BSG_TR.shortOptionHtml(cur);
    const sel = document.getElementById("trSel");
    if (sel) sel.innerHTML = window.BSG_TR.optionHtml(cur);
    const note = document.getElementById("trNote");
    if (note) note.innerHTML = window.BSG_TR.noteHtml(cur);
  }
  function updateFooter() {
    const el = document.querySelector(".foot");
    if (el) el.innerHTML = window.BSG_TR.footerHtml(tr());
  }
  function verseQuote(ref, occ) { return window.BSG_TR.text(tr(), ref, occ || 0); }
  function wireTrPicks() {
    const head = document.getElementById("trPick");
    if (head && !head.dataset.wired) {
      head.dataset.wired = "1";
      head.addEventListener("change", e => setTr(e.target.value));
    }
    const sel = document.getElementById("trSel");
    if (sel) sel.onchange = e => setTr(e.target.value);
  }
  async function getGuide(id) {
    if (cache[id]) return cache[id];
    const r = await fetch(`data/${id}.json`);
    if (!r.ok) throw new Error("Guide not found");
    return (cache[id] = await r.json());
  }

  // ---------- dates, plans, memory ----------
  const PLANS = window.PLANS || [], MEMORY = window.MEMORY || [];
  const planById = Object.fromEntries(PLANS.map(p => [p.id, p]));
  const ymd = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  const parseYmd = s => { const [y, m, d] = s.split("-").map(Number); return new Date(y, m - 1, d); };
  const todayYmd = () => ymd(new Date());
  const addDays = (s, n) => { const d = parseYmd(s); d.setDate(d.getDate() + n); return ymd(d); };
  const dayDiff = (a, b) => Math.round((parseYmd(b) - parseYmd(a)) / 86400000);
  const niceDate = s => parseYmd(s).toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric" });
  function activePlan() { const st = state.plan; if (!st || !planById[st.id]) return null; return { st, p: planById[st.id] }; }
  const dayChapters = (p, d) => p.schedule[d - 1] || [];
  const dayDone = (p, d) => { const cs = dayChapters(p, d); return cs.length > 0 && cs.every(([b, c]) => isRead(b, c)); };
  function setDayDone(p, d, v) { dayChapters(p, d).forEach(([b, c]) => { state.read[b] = state.read[b] || {}; if (v) state.read[b][c] = 1; else delete state.read[b][c]; }); save(); }
  function dayLabel(p, d) {
    const groups = [];
    for (const [b, c] of dayChapters(p, d)) { const g = groups[groups.length - 1]; if (g && g.b === b && g.to === c - 1) g.to = c; else groups.push({ b, from: c, to: c }); }
    return groups.map(g => `${byId[g.b].name} ${g.from}${g.to > g.from ? "–" + g.to : ""}`).join("; ");
  }
  function planStats(p, st) {
    const raw = dayDiff(st.start, todayYmd()) + 1, today = Math.min(Math.max(raw, 0), p.days);
    let doneDays = 0, firstUndone = 0, behind = 0;
    for (let d = 1; d <= p.days; d++) { const ok = dayDone(p, d); if (ok) doneDays++; else { if (!firstUndone) firstUndone = d; if (d < raw) behind++; } }
    let streak = 0, d = raw >= 1 && raw <= p.days && dayDone(p, raw) ? raw : Math.min(raw, p.days + 1) - 1;
    while (d >= 1 && dayDone(p, d)) { streak++; d--; }
    return { raw, today, doneDays, firstUndone, behind, streak };
  }
  const dayLinks = (p, d) => dayChapters(p, d).map(([b, c]) => `<a class="chip ${isRead(b, c) ? "done" : ""}" href="#/b/${b}/${c}">${isRead(b, c) ? "✓ " : ""}${esc(byId[b].name)} ${c}</a>`).join("");
  const memText = v => `“${esc(verseQuote(v.ref))}”`;
  function verseOfDay() { if (!MEMORY.length) return null; const n = Math.floor(parseYmd(todayYmd()) / 86400000); return MEMORY[((n * 37) % MEMORY.length + MEMORY.length) % MEMORY.length]; }
  const ATTR = () => window.BSG_TR.attrHtml(tr());

  // ---------- theme ----------
  const themeBtn = document.getElementById("themeBtn");
  function currentDark() {
    const t = document.documentElement.dataset.theme;
    return t ? t === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  }
  function paintThemeBtn() { themeBtn.textContent = currentDark() ? "☀️" : "🌙"; }
  themeBtn.onclick = () => {
    const t = currentDark() ? "light" : "dark";
    document.documentElement.dataset.theme = t; state.theme = t; save(); paintThemeBtn();
  };
  paintThemeBtn();

  // ---------- views ----------
  function home() {
    const total = BOOKS.reduce((a, b) => a + b.chapters, 0);
    const done = BOOKS.reduce((a, b) => a + readCount(b.id), 0);
    const ready = BOOKS.filter(b => b.ready).length;
    let html = `<div class="card">
      <h1>Bible Study Guides</h1>
      <p class="muted small">Book-by-book guides with a translation you choose: overview, outline, themes, key verses, chapter questions, and your own notes. ${ready === 66 ? "All 66 books are ready." : ready + " of 66 guides are ready, and more are coming."}</p>
      <div class="stat"><b>Whole Bible progress</b><span class="muted small">${done} / ${total} chapters</span></div>${bar(pct(done, total))}
      <div class="btnrow"><a class="btn" href="#/plan">📅 Reading plan</a><a class="btn" href="#/memory">🧠 Memory verses</a><a class="btn" href="#/search">🔍 Search</a><a class="btn" href="#/settings">⚙️ Backup &amp; settings</a></div>
    </div>`;
    html += todayCard() + votdCard();
    for (const [t, label] of [["OT", "Old Testament"], ["NT", "New Testament"]]) {
      html += `<section class="testament"><h2>${label}</h2>`;
      const sections = [...new Set(BOOKS.filter(b => b.testament === t).map(b => b.section))];
      for (const s of sections) {
        html += `<div class="section-title">${esc(s)}</div><div class="grid">`;
        for (const b of BOOKS.filter(x => x.testament === t && x.section === s)) {
          const rc = readCount(b.id);
          html += b.ready
            ? `<a class="book ready" href="#/b/${b.id}"><div class="bn">${esc(b.name)}</div><div class="bm">${rc}/${b.chapters} chapters read</div>${bar(pct(rc, b.chapters))}</a>`
            : `<a class="book soon" href="#/b/${b.id}"><div class="bn">${esc(b.name)}</div><div class="bm">${b.chapters} chapter${b.chapters > 1 ? "s" : ""}</div><span class="badge">Coming soon</span></a>`;
        }
        html += `</div>`;
      }
      html += `</section>`;
    }
    app.innerHTML = html;
    wireDayButtons(home);
    const vb = document.getElementById("votdReveal"); if (vb) vb.onclick = () => { vb.parentElement.classList.add("shown"); };
  }

  function todayCard() {
    const a = activePlan();
    if (!a) return `<div class="card today"><h2>📅 Today's reading</h2><p class="muted small">Pick a daily reading plan (a year through the whole Bible, 90 days in the New Testament, and more) and your reading for each day will show up here.</p><a class="btn primary" href="#/plan">Choose a reading plan →</a></div>`;
    const { st, p } = a, s = planStats(p, st);
    if (s.raw < 1) return `<div class="card today"><h2>📅 ${esc(p.name)}</h2><p>Your plan starts ${niceDate(st.start)} (in ${1 - s.raw} day${s.raw === 0 ? "" : "s"}). Day 1: ${esc(dayLabel(p, 1))}</p><a class="btn" href="#/plan">View plan</a></div>`;
    if (s.doneDays === p.days) return `<div class="card today"><h2>🎉 Plan complete!</h2><p>You finished <b>${esc(p.name)}</b>. Well done, good and faithful reader.</p><a class="btn" href="#/plan">Start another plan</a></div>`;
    const d = s.raw > p.days ? s.firstUndone : s.raw;
    const done = dayDone(p, d);
    return `<div class="card today"><div class="stat"><h2>📅 Today's reading</h2><span class="muted small">Day ${d} of ${p.days}</span></div>
      <p class="muted small">${esc(p.name)} · ${niceDate(addDays(st.start, d - 1))}</p>
      <p class="reading"><b>${esc(dayLabel(p, d))}</b></p><div class="chips">${dayLinks(p, d)}</div>
      <div class="btnrow"><button class="btn ${done ? "" : "primary"}" data-day="${d}" data-v="${done ? 0 : 1}">${done ? "✓ Done, undo" : "Mark today done"}</button><a class="btn" href="#/plan">Full plan</a></div>
      <div class="stat"><span class="small">🔥 ${s.streak}-day streak</span><span class="muted small">${s.doneDays}/${p.days} days</span></div>${bar(pct(s.doneDays, p.days))}
      ${s.behind ? `<p class="small behind">You're ${s.behind} day${s.behind > 1 ? "s" : ""} behind. <a href="#/plan">Catch up</a></p>` : ""}</div>`;
  }
  function votdCard() {
    const v = verseOfDay(); if (!v) return "";
    const m = !!state.mem[v.ref];
    return `<div class="card votd"><div class="stat"><h2>🧠 Verse of the day</h2>${m ? `<span class="badge go">Memorized</span>` : ""}</div>
      <blockquote>${memText(v)}<cite>${esc(v.ref)} (${esc(tr())})</cite></blockquote>
      <div class="btnrow"><a class="btn" href="#/memory/cards">Practice flashcards</a><a class="btn" href="#/memory">All memory verses</a></div>${ATTR()}</div>`;
  }
  function wireDayButtons(rerender) {
    const a = activePlan(); if (!a) return;
    app.querySelectorAll("button[data-day]").forEach(btn => btn.onclick = () => { setDayDone(a.p, +btn.dataset.day, btn.dataset.v === "1"); rerender(); });
  }

  function planView() {
    const a = activePlan();
    let html = `<a class="back" href="#/">← Home</a>`;
    if (!a) {
      html += `<div class="card"><h1>Reading plans</h1><p class="muted small">Choose a plan and a start date. Each day's chapters link into the study guides, and checking a day off also marks those chapters read in the guides.</p>
        <label class="field">Start date <input type="date" id="startDate" value="${todayYmd()}"></label></div>
        ${PLANS.map(p => `<div class="card"><h3>${esc(p.name)}</h3><p class="small">${esc(p.desc)}</p><p class="muted small">${p.total} chapters · ${p.days} days</p><button class="btn primary" data-start="${p.id}">Start this plan</button></div>`).join("")}`;
      app.innerHTML = html;
      app.querySelectorAll("button[data-start]").forEach(b => b.onclick = () => { state.plan = { id: b.dataset.start, start: document.getElementById("startDate").value || todayYmd() }; save(); planView(); });
      return;
    }
    const { st, p } = a, s = planStats(p, st);
    html += `<div class="card"><h1>${esc(p.name)}</h1><p class="muted small">Started ${niceDate(st.start)} · ${p.total} chapters over ${p.days} days</p>
      <div class="stat"><b>${s.doneDays} / ${p.days} days done</b><span class="small">🔥 ${s.streak}-day streak</span></div>${bar(pct(s.doneDays, p.days))}
      ${s.behind ? `<p class="small behind">You're ${s.behind} day${s.behind > 1 ? "s" : ""} behind schedule.</p><div class="btnrow"><a class="btn primary" href="#plan-day-${s.firstUndone}" id="jumpUndone">Go to day ${s.firstUndone}</a><button class="btn" id="resched">Reschedule so day ${s.firstUndone} is today</button></div>` : `<p class="small">You're on track. 👍</p>`}
      <label class="field">Start date <input type="date" id="startEdit" value="${st.start}"></label><div class="btnrow"><button class="btn" id="resetPlan">Stop / switch plan</button></div></div>
      <div class="card"><ul class="daylist">`;
    for (let d = 1; d <= p.days; d++) {
      const ok = dayDone(p, d), cls = d === s.raw ? "today" : (d < s.raw && !ok ? "late" : "");
      html += `<li id="plan-day-${d}" class="${cls}"><input type="checkbox" data-pday="${d}" ${ok ? "checked" : ""} aria-label="Day ${d} done">
        <div><div class="small muted">Day ${d} · ${niceDate(addDays(st.start, d - 1))}${d === s.raw ? " · <b>Today</b>" : ""}</div><div class="chips">${dayLinks(p, d)}</div></div></li>`;
    }
    html += `</ul></div>`;
    app.innerHTML = html;
    app.querySelectorAll("input[data-pday]").forEach(cb => cb.onchange = () => { const y = scrollY; setDayDone(p, +cb.dataset.pday, cb.checked); planView(); scrollTo(0, y); });
    const r = document.getElementById("resched");
    if (r) r.onclick = () => { state.plan.start = addDays(todayYmd(), -(s.firstUndone - 1)); save(); planView(); };
    const j = document.getElementById("jumpUndone");
    if (j) j.onclick = e => { e.preventDefault(); document.getElementById("plan-day-" + s.firstUndone).scrollIntoView({ block: "center" }); };
    document.getElementById("startEdit").onchange = e => { if (e.target.value) { state.plan.start = e.target.value; save(); planView(); } };
    document.getElementById("resetPlan").onclick = () => { if (confirm("Stop this plan? Your chapter checkmarks stay; only the plan schedule is removed.")) { delete state.plan; save(); planView(); } };
    const t = document.getElementById("plan-day-" + Math.max(1, Math.min(s.raw, p.days)));
    if (t && s.raw > 3) setTimeout(() => t.scrollIntoView({ block: "center" }), 0);
  }

  function memoryView(bookFilter) {
    const books = [...new Set(MEMORY.map(v => v.b))];
    const list = MEMORY.filter(v => !bookFilter || v.b === bookFilter);
    const mcount = MEMORY.filter(v => state.mem[v.ref]).length;
    app.innerHTML = `<a class="back" href="#/">← Home</a><div class="card"><h1>Memory verses</h1>
      <p class="muted small">${MEMORY.length} short verses chosen from across the Bible. Practice with flashcards and mark the ones you know by heart.</p>
      <div class="stat"><b>Memorized</b><span class="muted small">${mcount} / ${MEMORY.length}</span></div>${bar(pct(mcount, MEMORY.length))}
      <label class="field">Book <select id="memBook"><option value="">All books</option>${books.map(b => `<option value="${b}" ${b === bookFilter ? "selected" : ""}>${esc(byId[b].name)}</option>`).join("")}</select></label>
      <div class="btnrow"><a class="btn primary" href="#/memory/cards${bookFilter ? "?b=" + bookFilter : ""}">🃏 Flashcards${bookFilter ? ": " + esc(byId[bookFilter].name) : ""}</a></div></div>
      <div class="card">${list.map(v => `<div class="mv"><blockquote>${memText(v)}<cite><a href="#/b/${v.b}">${esc(v.ref)}</a> (${esc(tr())})</cite></blockquote>
        <button class="btn small-btn ${state.mem[v.ref] ? "primary" : ""}" data-mem="${esc(v.ref)}">${state.mem[v.ref] ? "✓ Memorized" : "Mark memorized"}</button></div>`).join("")}${ATTR()}</div>`;
    document.getElementById("memBook").onchange = e => { location.hash = "#/memory" + (e.target.value ? "?b=" + e.target.value : ""); };
    app.querySelectorAll("button[data-mem]").forEach(b => b.onclick = () => { const r = b.dataset.mem; if (state.mem[r]) delete state.mem[r]; else state.mem[r] = todayYmd(); save(); const y = scrollY; memoryView(bookFilter); scrollTo(0, y); });
  }

  let deck = null;
  function cardsView(bookFilter) {
    const key = bookFilter || "";
    if (!deck || deck.key !== key) deck = { key, onlyNew: false, shuffle: false, order: null, i: 0, shown: false };
    let list = MEMORY.filter(v => !bookFilter || v.b === bookFilter);
    if (deck.onlyNew) list = list.filter(v => !state.mem[v.ref]);
    if (deck.shuffle) { if (!deck.order || deck.order.length !== list.length) deck.order = list.map((_, i) => i).sort(() => Math.random() - .5); list = deck.order.map(i => list[i]); }
    if (deck.i >= list.length) deck.i = 0;
    const v = list[deck.i];
    const back = `#/memory${bookFilter ? "?b=" + bookFilter : ""}`;
    app.innerHTML = `<a class="back" href="${back}">← Memory verses</a>
      <div class="card"><div class="stat"><h1>Flashcards</h1><span class="muted small">${list.length ? deck.i + 1 + " / " + list.length : "0"}</span></div>
      <p class="muted small">${bookFilter ? esc(byId[bookFilter].name) : "All books"} · Tap the card to reveal the verse.</p>
      <div class="btnrow"><label class="toggle"><input type="checkbox" id="onlyNew" ${deck.onlyNew ? "checked" : ""}> Not yet memorized only</label><label class="toggle"><input type="checkbox" id="shuf" ${deck.shuffle ? "checked" : ""}> Shuffle</label></div></div>
      ${v ? `<button class="flash ${deck.shown ? "shown" : ""}" id="flash" aria-live="polite"><span class="fref">${esc(v.ref)}</span>
        ${deck.shown ? `<span class="ftext">${memText(v)}</span>` : `<span class="muted small">Say it from memory, then tap to check</span>`}</button>
      <div class="btnrow center"><button class="btn" id="prev">← Prev</button>
        <button class="btn ${state.mem[v.ref] ? "" : "primary"}" id="gotit">${state.mem[v.ref] ? "✓ Memorized (undo)" : "I know it ✓"}</button>
        <button class="btn" id="next">Next →</button></div>` : `<div class="card"><p>🎉 You've memorized every verse in this set. Uncheck “Not yet memorized only” to review them.</p></div>`}
      ${ATTR()}`;
    const rer = () => cardsView(bookFilter);
    document.getElementById("onlyNew").onchange = e => { deck.onlyNew = e.target.checked; deck.i = 0; deck.order = null; deck.shown = false; rer(); };
    document.getElementById("shuf").onchange = e => { deck.shuffle = e.target.checked; deck.order = null; deck.i = 0; deck.shown = false; rer(); };
    if (!v) return;
    document.getElementById("flash").onclick = () => { deck.shown = !deck.shown; rer(); };
    document.getElementById("prev").onclick = () => { deck.i = (deck.i - 1 + list.length) % list.length; deck.shown = false; rer(); };
    document.getElementById("next").onclick = () => { deck.i = (deck.i + 1) % list.length; deck.shown = false; rer(); };
    document.getElementById("gotit").onclick = () => {
      if (state.mem[v.ref]) { delete state.mem[v.ref]; save(); rer(); return; }
      state.mem[v.ref] = todayYmd(); save();
      if (!deck.onlyNew) deck.i = (deck.i + 1) % list.length; deck.order = deck.onlyNew ? null : deck.order; deck.shown = false; rer();
    };
  }

  function comingSoon(b) {
    app.innerHTML = `<a class="back" href="#/">← All books</a><div class="card"><h1>${esc(b.name)}</h1>
      <p><span class="badge">Coming soon</span></p>
      <p class="muted">The study guide for ${esc(b.name)} (${b.testament === "OT" ? "Old" : "New"} Testament · ${esc(b.section)} · ${b.chapters} chapter${b.chapters > 1 ? "s" : ""}) hasn't been written yet.</p>
      <p>You can still read it now:</p>
      <div class="btnrow">${window.BSG_TR.chapterButtons(tr(), b, 1)}</div></div>`;
  }

  const TABS = [["overview", "Overview"], ["chapters", "Chapters"], ["outline", "Outline"], ["themes", "Themes"], ["verses", "Key Verses"], ["christ", "Christ in " ], ["refs", "Cross-Refs"], ["reflect", "Reflect"]];

  async function bookView(id, tab) {
    const b = byId[id];
    if (!b) return notFound();
    if (!b.ready) return comingSoon(b);
    const g = await getGuide(id);
    tab = tab || "overview";
    const rc = readCount(id);
    const tabs = TABS.map(([k, l]) => `<a class="tab ${k === tab ? "on" : ""}" href="#/b/${id}/t/${k}">${k === "christ" ? l + esc(b.name) : l}</a>`).join("");
    let body = "";
    const o = g.overview;
    if (tab === "overview") {
      body = `<div class="card"><dl class="ov">
        <dt>Author</dt><dd>${esc(o.author)}</dd><dt>Date</dt><dd>${esc(o.date)}</dd>
        <dt>Audience</dt><dd>${esc(o.audience)}</dd><dt>Setting</dt><dd>${esc(o.setting)}</dd>
        <dt>Purpose</dt><dd>${esc(o.purpose)}</dd>${o.structure ? `<dt>Structure</dt><dd>${esc(o.structure)}</dd>` : ""}</dl></div>
        ${g.readingPlan ? `<div class="card"><h3>Reading plan</h3><p>${esc(window.BSG_TR.readingPlanText(g.readingPlan, tr()))}</p><a class="btn primary" href="#/b/${id}/${firstUnread(b)}">${rc ? "Continue" : "Start"} with chapter ${firstUnread(b)} →</a></div>` : ""}`;
    } else if (tab === "chapters") {
      body = `<div class="card"><ul class="chlist">${g.chapterList.map(c => `<li>
        <input type="checkbox" data-ch="${c.n}" ${isRead(id, c.n) ? "checked" : ""} aria-label="Mark chapter ${c.n} read">
        <a href="#/b/${id}/${c.n}" class="${getNote(id, c.n) ? "has-note" : ""}"><span class="num">${c.n}</span>${esc(c.title)}</a></li>`).join("")}</ul></div>`;
    } else if (tab === "outline") {
      body = `<div class="card">${g.outline.map(p => `<div class="outline-part"><h3>${esc(p.title)} <span class="range">${esc(p.range)}</span></h3>
        <ul>${p.items.map(i => `<li>${esc(i.title)} <span class="range">(${esc(i.range)})</span></li>`).join("")}</ul></div>`).join("")}</div>`;
    } else if (tab === "themes") {
      body = g.themes.map(t => `<div class="card"><div class="theme-title">${esc(t.title)}</div><p>${esc(t.text)}</p></div>`).join("");
    } else if (tab === "verses") {
      const seen = {};
      body = `<div class="card">${g.keyVerses.map(v => {
        const i = seen[v.ref] || 0; seen[v.ref] = i + 1;
        return `<blockquote>“${esc(verseQuote(v.ref, i))}”<cite>${refLink(v.ref)} (${esc(tr())})</cite></blockquote>`;
      }).join("")}${ATTR()}</div>`;
    } else if (tab === "christ") {
      body = `<div class="card"><p class="muted small">How ${esc(b.name)} points forward to Jesus:</p><ul class="refs">${g.christInBook.map(x => `<li><b>${refLink(x.ref, b)}</b>: ${esc(x.text)}</li>`).join("")}</ul></div>`;
    } else if (tab === "refs") {
      body = `<div class="card"><ul class="refs">${g.crossReferences.map(x => `<li><b>${refLink(x.ref)}</b>: ${esc(x.note)}</li>`).join("")}</ul></div>`;
    } else if (tab === "reflect") {
      body = `<div class="card"><h3>Reflection &amp; application</h3><ol class="q">${g.reflection.map(r => `<li>${esc(r)}</li>`).join("")}</ol></div>
        <div class="card"><h3>My notes on ${esc(b.name)}</h3><textarea id="bookNote" placeholder="Big-picture takeaways, prayers, questions…">${esc(getNote(id, "book"))}</textarea><div class="saved" id="savedMsg"></div></div>`;
    }
    app.innerHTML = `<a class="back" href="#/">← All books</a>
      <div class="card"><h1>${esc(b.name)}</h1><p class="muted">${esc(g.tagline)}</p>
      <div class="stat"><b>Progress</b><span class="muted small">${rc} / ${b.chapters} chapters read</span></div>${bar(pct(rc, b.chapters))}
      <div class="btnrow noprint"><a class="btn" href="pdf/${id}.pdf" target="_blank" rel="noopener" download="${esc(b.name)} Study Guide.pdf">⬇️ Download PDF</a><button class="btn" onclick="window.print()">🖨️ Print this page</button></div></div>
      <nav class="tabs">${tabs}</nav>${body}`;
    app.querySelectorAll("input[data-ch]").forEach(cb => cb.onchange = () => { setRead(id, +cb.dataset.ch, cb.checked); bookView(id, tab).then(keepTab); });
    const bn = document.getElementById("bookNote");
    if (bn) wireNote(bn, id, "book");
    keepTab();
  }
  function keepTab() { const on = app.querySelector(".tab.on"); if (on) on.scrollIntoView({ block: "nearest", inline: "center" }); }
  function firstUnread(b) { for (let i = 1; i <= b.chapters; i++) if (!isRead(b.id, i)) return i; return 1; }

  function wireNote(el, id, ch) {
    const msg = document.getElementById("savedMsg"); let t;
    el.addEventListener("input", () => { clearTimeout(t); t = setTimeout(() => { setNote(id, ch, el.value); if (msg) { msg.textContent = "✓ Saved on this device"; setTimeout(() => msg.textContent = "", 1500); } }, 400); });
  }

  async function chapterView(id, n) {
    const b = byId[id];
    if (!b) return notFound();
    if (!b.ready) return comingSoon(b);
    const g = await getGuide(id);
    const c = g.chapterList.find(x => x.n === n);
    if (!c) return notFound();
    app.innerHTML = `<a class="back" href="#/b/${id}/t/chapters">← ${esc(b.name)} chapters</a>
      <div class="card"><div class="muted small">${esc(b.name)} ${n} of ${b.chapters}</div><h1>${esc(c.title)}</h1>
        <div class="btnrow">${window.BSG_TR.chapterButtons(tr(), b, n)}</div>
        <h3>Summary</h3><p>${esc(c.summary)}</p></div>
      <div class="card"><h3>Discussion questions</h3><ol class="q">${c.questions.map(q => `<li>${esc(q)}</li>`).join("")}</ol></div>
      <div class="card"><h3>Cross-references</h3><div class="chips">${c.crossRefs.map(r => `<span class="chip">${refLink(r)}</span>`).join("")}</div></div>
      <div class="card"><label class="readbox"><input type="checkbox" id="readCb" ${isRead(id, n) ? "checked" : ""}> I've read ${esc(b.name)} ${n}</label>
        <h3 style="margin-top:14px">My notes</h3><textarea id="note" placeholder="What stood out? What is God showing you? Answers to the questions…">${esc(getNote(id, n))}</textarea><div class="saved" id="savedMsg"></div></div>
      <div class="pager">${n > 1 ? `<a class="btn" href="#/b/${id}/${n - 1}">← Ch ${n - 1}</a>` : `<span></span>`}${n < b.chapters ? `<a class="btn primary" href="#/b/${id}/${n + 1}">Ch ${n + 1} →</a>` : `<a class="btn primary" href="#/b/${id}/t/reflect">Finish: Reflect →</a>`}</div>`;
    document.getElementById("readCb").onchange = e => setRead(id, n, e.target.checked);
    wireNote(document.getElementById("note"), id, n);
  }

  async function searchView(q) {
    app.innerHTML = `<a class="back" href="#/">← All books</a><div class="card"><h1>Search</h1>
      <input class="search" id="q" type="search" placeholder="Book, topic, person, or verse (e.g. covenant, Joseph, 15:6)" value="${esc(q || "")}" autofocus>
      <p class="muted small">Searches book names and everything inside the finished guides.</p></div><div id="results"></div>`;
    const input = document.getElementById("q");
    const guides = await Promise.all(BOOKS.filter(b => b.ready).map(b => getGuide(b.id).catch(() => null)));
    const run = () => {
      const term = input.value.trim(); const out = document.getElementById("results");
      history.replaceState(null, "", "#/search" + (term ? "?q=" + encodeURIComponent(term) : ""));
      if (term.length < 2) { out.innerHTML = ""; return; }
      const re = new RegExp(term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "i");
      const hl = s => { const m = s.match(re); if (!m) return esc(s.slice(0, 140)); const i = Math.max(0, m.index - 60); const sn = (i ? "…" : "") + s.slice(i, m.index + m[0].length + 80) + "…"; return esc(sn).replace(new RegExp(re.source, "ig"), x => `<mark>${x}</mark>`); };
      const res = [];
      BOOKS.forEach(b => { if (re.test(b.name) || re.test(b.section)) res.push({ href: `#/b/${b.id}`, title: b.name, sub: `${b.section}${b.ready ? "" : " · coming soon"}` }); });
      guides.forEach(g => {
        if (!g) return; const b = byId[g.id];
        const add = (href, title, text) => { if (re.test(text) || re.test(title)) res.push({ href, title, sub: hl(text), raw: true }); };
        Object.entries(g.overview).forEach(([k, v]) => add(`#/b/${g.id}/t/overview`, `${b.name}: ${k[0].toUpperCase() + k.slice(1)}`, v));
        g.themes.forEach(t => add(`#/b/${g.id}/t/themes`, `${b.name} theme: ${t.title}`, t.text));
        { const seen = {}; g.keyVerses.forEach(v => { const i = seen[v.ref] || 0; seen[v.ref] = i + 1; add(`#/b/${g.id}/t/verses`, `Key verse: ${v.ref}`, verseQuote(v.ref, i)); }); }
        g.chapterList.forEach(c => add(`#/b/${g.id}/${c.n}`, `${b.name} ${c.n}: ${c.title}`, [c.summary, ...c.questions, ...c.crossRefs].join(" ")));
        g.reflection.forEach(r => add(`#/b/${g.id}/t/reflect`, `${b.name}: Reflection`, r));
      });
      out.innerHTML = res.length ? `<div class="card">${res.slice(0, 60).map(r => `<a class="result" href="${r.href}"><p><b>${esc(r.title)}</b><br><span class="small muted">${r.raw ? r.sub : esc(r.sub)}</span></p></a>`).join("")}</div>`
        : `<div class="card muted">No results for “${esc(term)}”.</div>`;
    };
    input.addEventListener("input", run); run();
  }

  function settingsView() {
    app.innerHTML = `<a class="back" href="#/">← All books</a><div class="card"><h1>Backup &amp; settings</h1>
      <h3>Bible translation</h3>
      <label class="field">Translation <select id="trSel" aria-label="Bible translation"></select></label>
      <p class="muted small" id="trNote"></p>
      <p class="muted small">Your read checkmarks, notes, reading plan, and memorized verses are saved only on this device, in this browser. Export a backup now and then so you don't lose them.</p>
      <div class="btnrow"><button class="btn primary" id="exp">⬇️ Export backup</button><label class="btn">⬆️ Import backup<input type="file" id="imp" accept="application/json" hidden></label></div>
      <p class="saved" id="savedMsg"></p>
      ${isNative() ? "" : `<h3>Install on your phone</h3>
      <p class="small">In Chrome or Samsung Internet, open the menu (⋮ or ≡) and tap <b>Add to Home screen</b> or <b>Install app</b>. Once installed, it opens full screen and works offline.</p>`}
      <h3>Reset</h3><button class="btn" id="reset">Clear all progress, notes, plan &amp; memory verses</button></div>`;
    paintTrPicks(); wireTrPicks();
    document.getElementById("exp").onclick = async () => {
      const name = `bible-study-backup-${new Date().toISOString().slice(0, 10)}.json`;
      const text = JSON.stringify(state, null, 1);
      if (window.BSGNative && window.BSGNative.shareFile) {
        try {
          await window.BSGNative.shareFile({ name, text, title: "Bible Study Guides backup", body: "Study Guides backup" });
          document.getElementById("savedMsg").textContent = "✓ Backup ready to share";
          return;
        } catch (err) { /* fall back to a download */ }
      }
      const blob = new Blob([text], { type: "application/json" });
      const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = name; a.click();
    };
    document.getElementById("imp").onchange = async e => {
      try { const d = JSON.parse(await e.target.files[0].text()); state = { read: d.read || {}, notes: d.notes || {}, mem: d.mem || {}, plan: d.plan, theme: state.theme, tr: window.BSG_TR.valid(d.tr || state.tr) }; save(); document.getElementById("savedMsg").textContent = "✓ Backup restored"; }
      catch (err) { alert("That file isn't a valid backup."); }
    };
    document.getElementById("reset").onclick = () => { if (confirm("Erase all read checkmarks, notes, reading plan, and memorized verses on this device?")) { state = { read: {}, notes: {}, mem: {}, theme: state.theme, tr: state.tr }; save(); location.hash = "#/"; } };
  }

  function notFound() { app.innerHTML = `<div class="card"><h1>Not found</h1><a href="#/">Go home</a></div>`; }

  // ---------- router ----------
  async function route() {
    const h = location.hash.replace(/^#\/?/, "");
    const [path, qs] = h.split("?");
    const p = path.split("/").filter(Boolean);
    try {
      if (!p.length) home();
      else if (p[0] === "search") await searchView(new URLSearchParams(qs || "").get("q"));
      else if (p[0] === "settings") settingsView();
      else if (p[0] === "plan") planView();
      else if (p[0] === "memory" && p[1] === "cards") cardsView(new URLSearchParams(qs || "").get("b"));
      else if (p[0] === "memory") memoryView(new URLSearchParams(qs || "").get("b"));
      else if (p[0] === "b" && p[2] === "t") await bookView(p[1], p[3]);
      else if (p[0] === "b" && p[2]) await chapterView(p[1], parseInt(p[2], 10));
      else if (p[0] === "b") await bookView(p[1]);
      else notFound();
    } catch (e) { app.innerHTML = `<div class="card"><h1>Couldn't load</h1><p class="muted">${esc(e.message)}. Check your connection and try again.</p><a href="#/">Go home</a></div>`; }
    if (!(p[0] === "b" && p[2] === "t")) window.scrollTo(0, 0);
  }
  window.addEventListener("hashchange", route);
  window.BSG_TR.load().then(() => {
    state.tr = window.BSG_TR.valid(state.tr);
    paintTrPicks();
    wireTrPicks();
    updateFooter();
    route();
  }).catch(e => {
    app.innerHTML = `<div class="card"><h1>Couldn't load</h1><p class="muted">${esc(e.message)}. Check your connection and try again.</p></div>`;
  });

  if ("serviceWorker" in navigator && !isNative()) window.addEventListener("load", () => navigator.serviceWorker.register("sw.js").catch(() => {}));
  if (window.BSGNative && window.BSGNative.hideSplash) window.BSGNative.hideSplash();
})();
