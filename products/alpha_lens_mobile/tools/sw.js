const CACHE_NAME = 'nds-lens-studio12-20260706';
const ASSETS = ['./index.html?v=studio12','./styles.css?v=studio12','./app.js?v=studio12','./manifest.webmanifest?v=studio12','./docs/UI_REFORM_V9.md','./docs/FONT_POLICY_V11.md','./docs/NDS_LENS_V12_CHANGES.md'];
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
    }).catch(() => caches.match(event.request).then(cached => cached || caches.match('./index.html?v=studio12'))));
    return;
  }
  event.respondWith(caches.match(event.request).then(cached => cached || fetch(event.request)));
});
