/* 股市操练笔记 · Service Worker
 * 作用域：根路径 /，提供离线缓存与资源更新。
 * 策略：
 *   - 页面导航（HTML）：网络优先，失败回退缓存，再回退首页
 *   - 静态资源（css/js/img/font/xml）：缓存优先 + 后台静默更新
 *   - 仅缓存同源资源，第三方 CDN 资源透传
 */
const CACHE = 'gpsl-blog-v1';
const CORE = [
  '/',
  '/manifest.json',
  '/img/pwa-192.png',
  '/img/pwa-512.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE)
      .then((cache) => cache.addAll(CORE))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  // 只缓存同源资源，跨域（如第三方 CDN）直接透传
  if (url.origin !== self.location.origin) return;

  // 页面导航：网络优先，离线时回退缓存，最终回退首页
  if (req.mode === 'navigate') {
    event.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE).then((cache) => cache.put(req, copy));
          return res;
        })
        .catch(() =>
          caches.match(req).then((hit) => hit || caches.match('/'))
        )
    );
    return;
  }

  // 静态资源：缓存优先 + 后台刷新
  if (/\.(css|js|png|jpg|jpeg|gif|svg|ico|webp|woff2?|eot|ttf|map|xml)$/.test(url.pathname)) {
    event.respondWith(
      caches.match(req).then((hit) => {
        const fetchPromise = fetch(req).then((res) => {
          if (res && res.ok) {
            const copy = res.clone();
            caches.open(CACHE).then((cache) => cache.put(req, copy));
          }
          return res;
        });
        return hit || fetchPromise;
      })
    );
  }
});
