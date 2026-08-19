/* N.O.U Digital Systems - service worker
 *
 * Strategy:
 * - App shell (/) and navigation requests: network-first, falling back to the
 *   cached shell so the installed PWA still opens offline.
 * - Same-origin static assets (/assets/*, icons, manifest): cache-first with
 *   runtime caching (stale-while-revalidate keeps it fast and fresh).
 * - API calls (/api/*) are NEVER cached - they carry private data.
 * - Cross-origin requests (fonts, etc.) are left to the network.
 */
// Bump VERSION whenever app code changes: 'activate' purges caches that do
// not start with the current VERSION, preventing stale shells/modules from
// being served (this caused HMR websocket 400s + blocked API calls in older
// installed browsers).
const VERSION = 'nou-v1.0.1'
const SHELL_CACHE = `${VERSION}-shell`
const ASSET_CACHE = `${VERSION}-assets`

const SHELL_URLS = ['/', '/index.html', '/favicon.svg', '/favicon1.png', '/favicon1-192.png', '/favicon1-180.png', '/favicon-maskable.png', '/manifest.webmanifest']

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(SHELL_CACHE).then((cache) => cache.addAll(SHELL_URLS)).catch(() => {})
  )
  self.skipWaiting()
})

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => !k.startsWith(VERSION)).map((k) => caches.delete(k)))
    )
  )
  self.clients.claim()
})

self.addEventListener('fetch', (event) => {
  const { request } = event
  if (request.method !== 'GET') return

  const url = new URL(request.url)
  if (url.origin !== self.location.origin) return

  // API: never cache (private data).
  if (url.pathname.startsWith('/api/')) return

  // Navigations: network-first with offline shell fallback.
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((response) => {
          const copy = response.clone()
          caches.open(SHELL_CACHE).then((cache) => cache.put('/index.html', copy))
          return response
        })
        .catch(() => caches.match('/index.html'))
    )
    return
  }

  // Static assets: cache-first, then network + populate cache.
  event.respondWith(
    caches.match(request).then(
      (cached) =>
        cached ||
        fetch(request).then((response) => {
          if (response && response.status === 200) {
            const copy = response.clone()
            caches.open(ASSET_CACHE).then((cache) => cache.put(request, copy))
          }
          return response
        })
    )
  )
})
