// 홈 화면 추가(PWA)용 서비스 워커. 오프라인 지원은 필요 없어서 앱 화면 파일만 가볍게 캐시하고, 나머지는 항상 인터넷에서 받는다.
const CACHE = 'sieun-shell-v9';
const SHELL = ['./', './index.html', './css/style.css', './js/app.js', './js/gen.js', './js/draw.js', './manifest.webmanifest', './icons/icon-192.png'];
self.addEventListener('install', (e) => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener('activate', (e) => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return; // 외부 사진은 브라우저가 직접
  // 네트워크 먼저, 실패하면 캐시
  e.respondWith(fetch(e.request).then(r => { if (SHELL.some(s => url.pathname.endsWith(s.replace('./', '/')))) { const cp = r.clone(); caches.open(CACHE).then(c => c.put(e.request, cp)); } return r; }).catch(() => caches.match(e.request)));
});
