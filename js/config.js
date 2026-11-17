// ESV_ENABLED is true for the web / GitHub Pages build.
//
// For App Store and Google Play builds, Crossway has not granted permission
// yet, so ESV must stay off. Run:
//   python3 tools/set_esv.py --off
// That sets this flag to false, drops data/verses-esv.json from the
// service-worker cache list, and deletes data/verses-esv.json so no ESV
// text is shipped. The translation picker then matches Hidden Word's 13
// bundled versions, with BSB as the default.
//
// Turn it back on for the web build with:
//   python3 tools/set_esv.py --on
window.BSG_CONFIG = { ESV_ENABLED: true };
