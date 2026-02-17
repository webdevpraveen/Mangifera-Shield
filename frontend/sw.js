/**
 * 🛡️ Mangifera Shield — Service Worker
 * Caches all assets for offline-first PWA functionality
 */

const CACHE_NAME = 'mangifera-shield-v2';
const STATIC_ASSETS = [
    '/',
    '/index.html',
    '/css/styles.css',
    '/js/i18n.js',
    '/js/db.js',
    '/js/app.js',
    '/js/scanner.js',
    '/js/ledger.js',
    '/js/mandi.js',
    '/js/weather.js',
    '/js/certificate.js',
    '/js/voice.js',
    '/manifest.json',
    '/assets/icon-192.png',
    '/assets/icon-512.png'
];

const API_CACHE = 'mangifera-api-v1';

// Install — cache static assets
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            console.log('📦 Caching static assets');
            // Use addAll but don't fail on missing optional assets
            return Promise.allSettled(
                STATIC_ASSETS.map(url => cache.add(url).catch(e => {
                    console.warn(`⚠️ Could not cache: ${url}`, e);
                }))
            );
        })
    );
    self.skipWaiting();
});

// Activate — clean old caches
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(
                keys.filter(key => key !== CACHE_NAME && key !== API_CACHE)
                    .map(key => caches.delete(key))
            )
        )
    );
    self.clients.claim();
});

// Fetch — cache-first for static, network-first for API
self.addEventListener('fetch', event => {
    const url = new URL(event.request.url);

    // API requests: network-first with cache fallback
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(
            fetch(event.request)
                .then(response => {
                    // Cache GET responses
                    if (event.request.method === 'GET' && response.ok) {
                        const clone = response.clone();
                        caches.open(API_CACHE).then(cache => cache.put(event.request, clone));
                    }
                    return response;
                })
                .catch(() => caches.match(event.request))
        );
        return;
    }

    // Static assets: cache-first
    event.respondWith(
        caches.match(event.request).then(cached => {
            if (cached) return cached;
            return fetch(event.request).then(response => {
                if (response.ok) {
                    const clone = response.clone();
                    caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
                }
                return response;
            });
        })
    );
});

// Background sync for ledger — triggers when device comes back online
self.addEventListener('sync', event => {
    if (event.tag === 'sync-ledger') {
        event.waitUntil(doBackgroundSync());
    }
});

// Listen for online events to trigger background sync
self.addEventListener('message', event => {
    if (event.data && event.data.type === 'REGISTER_SYNC') {
        self.registration.sync.register('sync-ledger').catch(err => {
            console.warn('Background sync registration failed:', err);
        });
    }
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});

async function doBackgroundSync() {
    try {
        // Notify all open clients to trigger their sync logic
        const clients = await self.clients.matchAll();
        clients.forEach(client => client.postMessage({ type: 'SYNC_LEDGER' }));

        // Also attempt direct sync fetch for unsynced entries
        const response = await fetch('/api/health');
        if (response.ok) {
            console.log('✅ Background sync: server reachable, clients notified');
        }
    } catch (e) {
        console.error('Background sync error:', e);
        throw e; // Rethrow so the sync event retries
    }
}
