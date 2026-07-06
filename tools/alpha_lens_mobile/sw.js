const CACHE_NAME = 'alpha-lens-ultra4-20260706';
const ASSETS = ['./index.html?v=ultra4','./styles.css?v=ultra4','./app.js?v=ultra4','./manifest.webmanifest?v=ultra4'];
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
  if (url.pathname.endsWith('/') || url.pathname.endsWith('/index.html') || url.pathname.endsWith('/styles.css') || url.pathname.endsWith('/app.js')) {
    event.respondWith(fetch(event.request).then(res => {
      const copy = res.clone(); caches.open(CACHE_NAME).then(cache => cache.put(event.request, copy)); return res;
    }).catch(() => caches.match(event.request).then(cached => cached || caches.match('./index.html?v=ultra4'))));
    return;
  }
  event.respondWith(caches.match(event.request).then(cached => cached || fetch(event.request)));
});
