const CACHE_NAME = 'alpha-lens-studio10-20260706';
const ASSETS = ['./index.html?v=studio10','./styles.css?v=studio10','./app.js?v=studio10','./manifest.webmanifest?v=studio10','./docs/UI_REFORM_V9.md'];
self.addEventListener('install', event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS)));
  self.skipWaiting();
});
self.addEventListener('activate', event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  const url = new URL(event.request.url);
  if (url.pathname.endsWith('/') || url.pathname.endsWith('/index.html') || url.pathname.endsWith('/styles.css') || url.pathname.endsWith('/app.js') || url.pathname.endsWith('/manifest.webmanifest') || url.pathname.endsWith('/UI_REFORM_V9.md')) {
    event.respondWith(fetch(event.request).then(res => {
      const copy = res.clone(); caches.open(CACHE_NAME).then(cache => cache.put(event.request, copy)); return res;
    }).catch(() => caches.match(event.request).then(cached => cached || caches.match('./index.html?v=studio10'))));
    return;
  }
  event.respondWith(caches.match(event.request).then(cached => cached || fetch(event.request)));
});
