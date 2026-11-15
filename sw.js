// Network-first for app files and guides so updates show up; falls back to cache offline.
const CACHE = "bsg-v7";
const CORE = ["./", "index.html", "css/style.css", "js/books.js", "js/app.js", "manifest.webmanifest", "icons/icon-192.png", "data/genesis.json", "data/exodus.json", "data/leviticus.json", "data/numbers.json", "data/deuteronomy.json", "data/joshua.json", "data/judges.json", "data/ruth.json", "data/1-samuel.json", "data/2-samuel.json", "data/1-kings.json", "data/2-kings.json", "data/1-chronicles.json", "data/2-chronicles.json", "data/ezra.json", "data/nehemiah.json", "data/esther.json"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE))); self.skipWaiting(); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))); self.clients.claim(); });
self.addEventListener("fetch", e => {
  const u = new URL(e.request.url);
  if (e.request.method !== "GET" || u.origin !== location.origin) return;
  e.respondWith(fetch(e.request).then(r => { const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); return r; })
    .catch(() => caches.match(e.request).then(r => r || caches.match("index.html"))));
});
