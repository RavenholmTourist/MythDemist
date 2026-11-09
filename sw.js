// Project Mythos service worker.
// Cache-first app shell plus stale-while-revalidate for content. Bump
// MYTHOS_CACHE on every release: the new worker installs alongside the old,
// activates, revalidates cached URLs, and drops the previous cache. That is
// the update-push channel for packaged installs.
const MYTHOS_CACHE = "mythos-v1";
const APP_SHELL = ["./", "./index.html", "./styles.css", "./manifest.webmanifest", "./src/app.js", "./src/progression.js", "./icons/icon-192.png", "./icons/icon-512.png"];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(MYTHOS_CACHE).then((cache) => cache.addAll(APP_SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((names) => Promise.all(names.filter((name) => name !== MYTHOS_CACHE).map((name) => caches.delete(name))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return;
  event.respondWith(
    caches.match(event.request).then((cached) => {
      const network = fetch(event.request)
        .then((response) => {
          if (response.ok) {
            const copy = response.clone();
            caches.open(MYTHOS_CACHE).then((cache) => cache.put(event.request, copy));
          }
          return response;
        })
        .catch(() => cached);
      // Stale-while-revalidate: serve cache instantly, refresh in background.
      return cached || network;
    })
  );
});
