// Translation catalog: Hidden Word's public-domain / CC BY-SA texts, plus NIV
// (2011) and ESV for the 310 quoted verses, under Biblica's and Crossway's
// general-use quotation rules (each with its required copyright notice).
// ESV is offered when BSG_CONFIG.ESV_ENABLED is true (web and store builds).
(function () {
  "use strict";

  const TRANSLATIONS = {
    BSB: { n: "Berean Standard Bible", l: "Modern • public domain" },
    NIV: {
      n: "New International Version",
      l: "2011 • used by permission",
      a: "Scripture quotations taken from The Holy Bible, New International Version® NIV® Copyright © 1973, 1978, 1984, 2011 by Biblica, Inc.™ Used by permission. All rights reserved worldwide."
    },
    KJV: { n: "King James Version", l: "1611/1769 • public domain" },
    WEB: { n: "World English Bible", l: "Modern • public domain" },
    MSB: { n: "Majority Standard Bible", l: "Modern • public domain" },
    LSV: {
      n: "Literal Standard Version",
      l: "Modern literal • CC BY-SA 4.0",
      a: "Literal Standard Version (LSV) © 2020 Covenant Press. Used under the Creative Commons Attribution-ShareAlike 4.0 license (creativecommons.org/licenses/by-sa/4.0). Text unmodified; source: eBible.org."
    },
    FBV: {
      n: "Free Bible Version",
      l: "Modern • CC BY-SA 4.0",
      a: "Free Bible Version (FBV) © 2018 Dr. Jonathan Gallagher. Used under the Creative Commons Attribution-ShareAlike 4.0 license (creativecommons.org/licenses/by-sa/4.0). Text unmodified; source: eBible.org."
    },
    ASV: { n: "American Standard Version (1901)", l: "public domain" },
    RV: { n: "Revised Version (1885)", l: "public domain" },
    YLT: { n: "Young's Literal Translation", l: "1898 • public domain" },
    DBY: { n: "Darby Translation", l: "1890 • public domain" },
    WBS: { n: "Noah Webster Bible", l: "1833 • public domain" },
    BBE: { n: "Bible in Basic English", l: "1965 • public domain (US)" },
    GNV: { n: "Geneva Bible (1599)", l: "Original spelling • public domain" }
  };

  const ESV_META = {
    n: "English Standard Version",
    l: "© Crossway • used by permission",
    a: "Scripture quotations marked (ESV) are from the ESV® Bible (The Holy Bible, English Standard Version®), © 2001 by Crossway, a publishing ministry of Good News Publishers. ESV Text Edition: 2025. The ESV text may not be quoted in any publication made available to the public by a Creative Commons license. The ESV may not be translated in whole or in part into any other language. Used by permission. All rights reserved."
  };

  // BibleGateway version parameters. DBY and WBS use this site's codes.
  const BG_VERSION = {
    BSB: "BSB", NIV: "NIV", KJV: "KJV", WEB: "WEB", MSB: "MSB", LSV: "LSV", FBV: "FBV",
    ASV: "ASV", RV: "RV", YLT: "YLT", DBY: "DARBY", WBS: "WBT", BBE: "BBE",
    GNV: "GNV", ESV: "ESV"
  };

  const esc = s => String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  let verses = {};
  let esv = {};

  const esvEnabled = () => !!(window.BSG_CONFIG && window.BSG_CONFIG.ESV_ENABLED);

  function available() {
    const keys = Object.keys(TRANSLATIONS);
    return esvEnabled() ? ["ESV", ...keys] : keys;
  }

  function meta(tr) {
    if (tr === "ESV") return ESV_META;
    return TRANSLATIONS[tr] || TRANSLATIONS.BSB;
  }

  function valid(tr) {
    if (tr === "ESV" && esvEnabled()) return "ESV";
    if (tr && TRANSLATIONS[tr]) return tr;
    return "BSB";
  }

  function text(tr, ref, occ) {
    tr = valid(tr);
    if (tr === "ESV") {
      const v = esv[ref];
      if (Array.isArray(v)) return v[occ || 0] || v[0] || "";
      return v || "";
    }
    const row = verses[ref];
    if (!row) return "";
    return row[tr] || row.BSB || "";
  }

  function attrHtml(tr) {
    tr = valid(tr);
    const T = meta(tr);
    if (T.a) return `<p class="muted small attr">${esc(T.a)}</p>`;
    const extra = T.l && /public domain/i.test(T.l) ? "" : "";
    return `<p class="muted small attr">Scripture quotations are from the ${esc(T.n)} (${esc(tr)}), ${esc(T.l)}.</p>${extra}`;
  }

  function footerHtml(tr) {
    tr = valid(tr);
    const T = meta(tr);
    const notice = T.a
      ? esc(T.a)
      : `Scripture quotations are from the ${esc(T.n)} (${esc(tr)}), ${esc(T.l)}.`;
    const dest = tr === "ESV" ? "ESV.org or BibleGateway" : "BibleGateway";
    return `<p>${notice}</p><p>Study notes, summaries and questions are original to this app. Chapter links open the full text on ${dest}.</p>`;
  }

  function bgUrl(tr, ref) {
    tr = valid(tr);
    const ver = BG_VERSION[tr] || tr;
    return `https://www.biblegateway.com/passage/?search=${encodeURIComponent(ref)}&version=${encodeURIComponent(ver)}`;
  }

  function esvOrgUrl(book, ch) {
    return `https://www.esv.org/${encodeURIComponent(book.name).replace(/%20/g, "+")}+${ch}/`;
  }

  function chapterUrl(tr, book, ch) {
    tr = valid(tr);
    if (tr === "ESV") return esvOrgUrl(book, ch);
    return bgUrl(tr, `${book.name} ${ch}`);
  }

  function chapterButtons(tr, book, ch) {
    tr = valid(tr);
    if (tr === "ESV") {
      return `<a class="btn primary" target="_blank" rel="noopener" href="${esvOrgUrl(book, ch)}">📖 Read on ESV.org ↗</a>`
        + `<a class="btn" target="_blank" rel="noopener" href="${bgUrl("ESV", book.name + " " + ch)}">BibleGateway (ESV) ↗</a>`;
    }
    return `<a class="btn primary" target="_blank" rel="noopener" href="${chapterUrl(tr, book, ch)}">📖 Read on BibleGateway (${esc(tr)}) ↗</a>`;
  }

  function readingPlanText(s, tr) {
    s = String(s || "");
    if (valid(tr) === "ESV") return s;
    return s.replace(/ESV\.org/g, "BibleGateway");
  }

  function optionHtml(selected) {
    selected = valid(selected);
    return available().map(k => {
      const T = meta(k);
      return `<option value="${k}" ${k === selected ? "selected" : ""}>${k} — ${esc(T.n)}</option>`;
    }).join("");
  }

  function shortOptionHtml(selected) {
    selected = valid(selected);
    return available().map(k => `<option value="${k}" ${k === selected ? "selected" : ""}>${k}</option>`).join("");
  }

  function noteHtml(tr) {
    tr = valid(tr);
    const T = meta(tr);
    const bits = [`<b>${esc(tr)}</b> — ${esc(T.n)} (${esc(T.l)}), available offline.`];
    if (T.a) bits.push(esc(T.a));
    return bits.join(" ");
  }

  async function load() {
    const r = await fetch("data/verses.json");
    if (!r.ok) throw new Error("Couldn't load Bible translations");
    verses = await r.json();
    if (esvEnabled()) {
      try {
        const e = await fetch("data/verses-esv.json");
        if (e.ok) esv = await e.json();
      } catch (err) { esv = {}; }
    } else {
      esv = {};
    }
    return true;
  }

  window.BSG_TR = {
    TRANSLATIONS,
    DEFAULT: "BSB",
    esvEnabled,
    available,
    meta,
    valid,
    text,
    attrHtml,
    footerHtml,
    bgUrl,
    chapterUrl,
    chapterButtons,
    readingPlanText,
    optionHtml,
    shortOptionHtml,
    noteHtml,
    load
  };
})();
