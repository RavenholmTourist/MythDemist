const CACHE = 'sor4-survival-tracker-v7'

self.addEventListener('install', () => self.skipWaiting())
self.addEventListener('activate', (e) => e.waitUntil(clients.claim()))

// Cache-first for same-origin GETs; fills the cache from the network as it goes.
self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url)
  if (e.request.method !== 'GET' || url.origin !== location.origin) return
  e.respondWith(
    caches.open(CACHE).then(async (cache) => {
      const hit = await cache.match(e.request, { ignoreSearch: true })
      const fetched = fetch(e.request)
        .then((res) => {
          if (res.ok) cache.put(e.request, res.clone())
          return res
        })
        .catch(() => hit)
      return hit ?? fetched
    }),
  )
})
