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
  state.read = state.read || {}; state.notes = state.notes || {};
  function save() { localStorage.setItem(KEY, JSON.stringify(state)); }
  const isRead = (b, c) => !!(state.read[b] && state.read[b][c]);
  function setRead(b, c, v) { state.read[b] = state.read[b] || {}; if (v) state.read[b][c] = 1; else delete state.read[b][c]; save(); }
  const getNote = (b, c) => (state.notes[b] && state.notes[b][c]) || "";
  function setNote(b, c, t) { state.notes[b] = state.notes[b] || {}; if (t.trim()) state.notes[b][c] = t; else delete state.notes[b][c]; save(); }
  const readCount = b => Object.keys(state.read[b] || {}).length;

  // ---------- helpers ----------
  const esc = s => String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const pct = (a, b) => b ? Math.round(a / b * 100) : 0;
  const bar = p => `<div class="progress" role="progressbar" aria-valuenow="${p}" aria-valuemin="0" aria-valuemax="100"><i style="width:${p}%"></i></div>`;
  const esvUrl = (book, ch) => `https://www.esv.org/${encodeURIComponent(book.name).replace(/%20/g, "+")}+${ch}/`;
  const bgUrl = ref => `https://www.biblegateway.com/passage/?search=${encodeURIComponent(ref)}&version=ESV`;
  const refLink = (ref, book) => {
    const full = /^[0-9]+[:\u2013-]/.test(ref) && book ? `${book.name} ${ref}` : ref;
    return `<a href="${bgUrl(full)}" target="_blank" rel="noopener">${esc(ref)}</a>`;
  };
  async function getGuide(id) {
    if (cache[id]) return cache[id];
    const r = await fetch(`data/${id}.json`);
    if (!r.ok) throw new Error("Guide not found");
    return (cache[id] = await r.json());
  }

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
      <p class="muted small">Book-by-book guides based on the ESV: overview, outline, themes, key verses, chapter questions, and your own notes. ${ready} of 66 guides are ready, and more are coming.</p>
      <div class="stat"><b>Whole Bible progress</b><span class="muted small">${done} / ${total} chapters</span></div>${bar(pct(done, total))}
      <div class="btnrow"><a class="btn" href="#/search">🔍 Search guides</a><a class="btn" href="#/settings">⚙️ Backup &amp; settings</a></div>
    </div>`;
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
  }

  function comingSoon(b) {
    app.innerHTML = `<a class="back" href="#/">← All books</a><div class="card"><h1>${esc(b.name)}</h1>
      <p><span class="badge">Coming soon</span></p>
      <p class="muted">The study guide for ${esc(b.name)} (${b.testament === "OT" ? "Old" : "New"} Testament · ${esc(b.section)} · ${b.chapters} chapter${b.chapters > 1 ? "s" : ""}) hasn't been written yet.</p>
      <p>You can still read it now:</p>
      <div class="btnrow"><a class="btn primary" target="_blank" rel="noopener" href="${esvUrl(b, 1)}">Read ${esc(b.name)} on ESV.org ↗</a></div></div>`;
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
        ${g.readingPlan ? `<div class="card"><h3>Reading plan</h3><p>${esc(g.readingPlan)}</p><a class="btn primary" href="#/b/${id}/${firstUnread(b)}">${rc ? "Continue" : "Start"} with chapter ${firstUnread(b)} →</a></div>` : ""}`;
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
      body = `<div class="card">${g.keyVerses.map(v => `<blockquote>“${esc(v.quote)}”<cite>${refLink(v.ref)} (ESV)</cite></blockquote>`).join("")}
        <p class="muted small">Scripture quotations are from the ESV® Bible, © 2001 by Crossway. Used by permission. All rights reserved.</p></div>`;
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
      <div class="stat"><b>Progress</b><span class="muted small">${rc} / ${b.chapters} chapters read</span></div>${bar(pct(rc, b.chapters))}</div>
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
        <div class="btnrow"><a class="btn primary" target="_blank" rel="noopener" href="${esvUrl(b, n)}">📖 Read on ESV.org ↗</a>
        <a class="btn" target="_blank" rel="noopener" href="${bgUrl(b.name + " " + n)}">BibleGateway (ESV) ↗</a></div>
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
        g.keyVerses.forEach(v => add(`#/b/${g.id}/t/verses`, `Key verse: ${v.ref}`, v.quote));
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
      <p class="muted small">Your read checkmarks and notes are saved only on this device, in this browser. Export a backup now and then so you don't lose them.</p>
      <div class="btnrow"><button class="btn primary" id="exp">⬇️ Export backup</button><label class="btn">⬆️ Import backup<input type="file" id="imp" accept="application/json" hidden></label></div>
      <p class="saved" id="savedMsg"></p>
      <h3>Install on your phone</h3>
      <p class="small">In Chrome or Samsung Internet, open the menu (⋮ or ≡) and tap <b>Add to Home screen</b> or <b>Install app</b>. Once installed, it opens full screen and works offline.</p>
      <h3>Reset</h3><button class="btn" id="reset">Clear all progress &amp; notes</button></div>`;
    document.getElementById("exp").onclick = () => {
      const blob = new Blob([JSON.stringify(state, null, 1)], { type: "application/json" });
      const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = `bible-study-backup-${new Date().toISOString().slice(0, 10)}.json`; a.click();
    };
    document.getElementById("imp").onchange = async e => {
      try { const d = JSON.parse(await e.target.files[0].text()); state = { read: d.read || {}, notes: d.notes || {}, theme: state.theme }; save(); document.getElementById("savedMsg").textContent = "✓ Backup restored"; }
      catch (err) { alert("That file isn't a valid backup."); }
    };
    document.getElementById("reset").onclick = () => { if (confirm("Erase all read checkmarks and notes on this device?")) { state = { read: {}, notes: {}, theme: state.theme }; save(); location.hash = "#/"; } };
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
      else if (p[0] === "b" && p[2] === "t") await bookView(p[1], p[3]);
      else if (p[0] === "b" && p[2]) await chapterView(p[1], parseInt(p[2], 10));
      else if (p[0] === "b") await bookView(p[1]);
      else notFound();
    } catch (e) { app.innerHTML = `<div class="card"><h1>Couldn't load</h1><p class="muted">${esc(e.message)}. Check your connection and try again.</p><a href="#/">Go home</a></div>`; }
    if (!(p[0] === "b" && p[2] === "t")) window.scrollTo(0, 0);
  }
  window.addEventListener("hashchange", route);
  route();

  if ("serviceWorker" in navigator) window.addEventListener("load", () => navigator.serviceWorker.register("sw.js").catch(() => {}));
})();
