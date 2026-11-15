// Network-first for app files and guides so updates show up; falls back to cache offline.
const CACHE = "bsg-v32";
const CORE = ["./", "index.html", "css/style.css", "js/books.js", "js/app.js", "manifest.webmanifest", "icons/icon-192.png", "data/genesis.json", "data/exodus.json", "data/leviticus.json", "data/numbers.json", "data/deuteronomy.json", "data/joshua.json", "data/judges.json", "data/ruth.json", "data/1-samuel.json", "data/2-samuel.json", "data/1-kings.json", "data/2-kings.json", "data/1-chronicles.json", "data/2-chronicles.json", "data/ezra.json", "data/nehemiah.json", "data/esther.json", "data/job.json", "data/psalms.json", "data/proverbs.json", "data/ecclesiastes.json", "data/song-of-solomon.json", "data/isaiah.json", "data/jeremiah.json", "data/lamentations.json", "data/ezekiel.json", "data/daniel.json", "data/hosea.json", "data/joel.json", "data/amos.json", "data/obadiah.json", "data/jonah.json", "data/micah.json", "data/nahum.json", "data/habakkuk.json", "data/zephaniah.json", "data/haggai.json", "data/zechariah.json", "data/malachi.json", "data/matthew.json", "data/mark.json", "data/luke.json", "data/john.json", "data/acts.json", "data/romans.json", "data/1-corinthians.json", "data/2-corinthians.json", "data/galatians.json", "data/ephesians.json", "data/philippians.json", "data/colossians.json", "data/1-thessalonians.json", "data/2-thessalonians.json", "data/1-timothy.json", "data/2-timothy.json", "data/titus.json", "data/philemon.json"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE))); self.skipWaiting(); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))); self.clients.claim(); });
self.addEventListener("fetch", e => {
  const u = new URL(e.request.url);
  if (e.request.method !== "GET" || u.origin !== location.origin) return;
  e.respondWith(fetch(e.request).then(r => { const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); return r; })
    .catch(() => caches.match(e.request).then(r => r || caches.match("index.html"))));
});
