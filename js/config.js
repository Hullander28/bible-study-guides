// Build flags.
//
// ESV_ENABLED: ESV quotations (data/verses-esv.json, 310 verses) are offered
// on the website and in the App Store / Google Play builds, under Crossway's
// standard-use rule (≤500 verses, under half of any book, under 25% of the
// app's text, with the copyright notice). `python3 tools/set_esv.py --off`
// can still turn ESV off (drops data/verses-esv.json and its sw.js entry);
// the picker then shows the other 14 translations, BSB default.
//
// PDF_ENABLED: the printable PDFs in pdf/ are website-only. Store builds
// (tools/build_store_www.py) omit pdf/ and set this to false, which hides the
// Download PDF button.
window.BSG_CONFIG = { ESV_ENABLED: true, PDF_ENABLED: true };
