// Minimal service worker: cache the shell so the UI loads offline.
// API calls still need the local server.
const CACHE = "wjournal-v1";
self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(["/", "/manifest.json"])));
});
self.addEventListener("fetch", e => {
  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request)));
});
