/**
 * 🛡️ Mangifera Shield — IndexedDB Wrapper
 * Offline-first data storage with sync queue management
 */

const DB_NAME = 'MangiferaShieldDB';
const DB_VERSION = 1;

let db = null;

function openDatabase() {
    return new Promise((resolve, reject) => {
        if (db) { resolve(db); return; }

        const request = indexedDB.open(DB_NAME, DB_VERSION);

        request.onerror = () => reject(request.error);

        request.onupgradeneeded = (event) => {
            const database = event.target.result;

            // Ledger entries store
            if (!database.objectStoreNames.contains('ledger')) {
                const ledgerStore = database.createObjectStore('ledger', { keyPath: 'clientId' });
                ledgerStore.createIndex('farmerPhone', 'farmerPhone', { unique: false });
                ledgerStore.createIndex('synced', 'synced', { unique: false });
                ledgerStore.createIndex('createdAt', 'createdAt', { unique: false });
            }

            // Scan results store
            if (!database.objectStoreNames.contains('scans')) {
                const scanStore = database.createObjectStore('scans', { keyPath: 'scanId' });
                scanStore.createIndex('createdAt', 'createdAt', { unique: false });
            }

            // Cached mandi prices
            if (!database.objectStoreNames.contains('mandiPrices')) {
                database.createObjectStore('mandiPrices', { keyPath: 'id' });
            }

            // Cached weather data
            if (!database.objectStoreNames.contains('weather')) {
                database.createObjectStore('weather', { keyPath: 'id' });
            }

            // Sync queue
            if (!database.objectStoreNames.contains('syncQueue')) {
                const syncStore = database.createObjectStore('syncQueue', { keyPath: 'id', autoIncrement: true });
                syncStore.createIndex('type', 'type', { unique: false });
                syncStore.createIndex('status', 'status', { unique: false });
            }

            // Certificates
            if (!database.objectStoreNames.contains('certificates')) {
                database.createObjectStore('certificates', { keyPath: 'certId' });
            }
        };

        request.onsuccess = (event) => {
            db = event.target.result;
            resolve(db);
        };
    });
}

// === LEDGER OPERATIONS ===

async function saveLedgerEntryDB(entry) {
    const database = await openDatabase();
    return new Promise((resolve, reject) => {
        const tx = database.transaction('ledger', 'readwrite');
        const store = tx.objectStore('ledger');
        entry.synced = false;
        entry.createdAt = entry.createdAt || new Date().toISOString();
        entry.updatedAt = new Date().toISOString();
        store.put(entry);
        tx.oncomplete = () => resolve(entry);
        tx.onerror = () => reject(tx.error);
    });
}

async function getLedgerEntries() {
    const database = await openDatabase();
    return new Promise((resolve, reject) => {
        const tx = database.transaction('ledger', 'readonly');
        const store = tx.objectStore('ledger');
        const request = store.getAll();
        request.onsuccess = () => {
            const entries = request.result.sort((a, b) =>
                new Date(b.createdAt) - new Date(a.createdAt)
            );
            resolve(entries);
        };
        request.onerror = () => reject(request.error);
    });
}

async function deleteLedgerEntryDB(clientId) {
    const database = await openDatabase();
    return new Promise((resolve, reject) => {
        const tx = database.transaction('ledger', 'readwrite');
        tx.objectStore('ledger').delete(clientId);
        tx.oncomplete = () => resolve();
        tx.onerror = () => reject(tx.error);
    });
}

async function getUnsyncedLedgerEntries() {
    const database = await openDatabase();
    return new Promise((resolve, reject) => {
        const tx = database.transaction('ledger', 'readonly');
        const store = tx.objectStore('ledger');
        const index = store.index('synced');
        const request = index.getAll(false);
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
    });
}

async function markLedgerSynced(clientId) {
    const database = await openDatabase();
    return new Promise((resolve, reject) => {
        const tx = database.transaction('ledger', 'readwrite');
        const store = tx.objectStore('ledger');
        const getReq = store.get(clientId);
        getReq.onsuccess = () => {
            const entry = getReq.result;
            if (entry) {
                entry.synced = true;
                store.put(entry);
            }
            resolve();
        };
        tx.onerror = () => reject(tx.error);
    });
}

// === SCAN OPERATIONS ===

async function saveScanResult(scan) {
    const database = await openDatabase();
    return new Promise((resolve, reject) => {
        const tx = database.transaction('scans', 'readwrite');
        tx.objectStore('scans').put(scan);
        tx.oncomplete = () => resolve(scan);
        tx.onerror = () => reject(tx.error);
    });
}

async function getScanResults() {
    const database = await openDatabase();
    return new Promise((resolve, reject) => {
        const tx = database.transaction('scans', 'readonly');
        const request = tx.objectStore('scans').getAll();
        request.onsuccess = () => {
            const results = request.result.sort((a, b) =>
                new Date(b.createdAt) - new Date(a.createdAt)
            );
            resolve(results);
        };
        request.onerror = () => reject(request.error);
    });
}

// === CACHE OPERATIONS ===

async function cacheMandiPrices(data) {
    const database = await openDatabase();
    return new Promise((resolve, reject) => {
        const tx = database.transaction('mandiPrices', 'readwrite');
        tx.objectStore('mandiPrices').put({ id: 'latest', ...data, cachedAt: new Date().toISOString() });
        tx.oncomplete = () => resolve();
        tx.onerror = () => reject(tx.error);
    });
}

async function getCachedMandiPrices() {
    const database = await openDatabase();
    return new Promise((resolve, reject) => {
        const tx = database.transaction('mandiPrices', 'readonly');
        const request = tx.objectStore('mandiPrices').get('latest');
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
    });
}

async function cacheWeatherData(data) {
    const database = await openDatabase();
    return new Promise((resolve, reject) => {
        const tx = database.transaction('weather', 'readwrite');
        tx.objectStore('weather').put({ id: 'latest', ...data, cachedAt: new Date().toISOString() });
        tx.oncomplete = () => resolve();
        tx.onerror = () => reject(tx.error);
    });
}

async function getCachedWeather() {
    const database = await openDatabase();
    return new Promise((resolve, reject) => {
        const tx = database.transaction('weather', 'readonly');
        const request = tx.objectStore('weather').get('latest');
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
    });
}

// === CERTIFICATE OPERATIONS ===

async function saveCertificate(cert) {
    const database = await openDatabase();
    return new Promise((resolve, reject) => {
        const tx = database.transaction('certificates', 'readwrite');
        tx.objectStore('certificates').put(cert);
        tx.oncomplete = () => resolve();
        tx.onerror = () => reject(tx.error);
    });
}

async function getCertificates() {
    const database = await openDatabase();
    return new Promise((resolve, reject) => {
        const tx = database.transaction('certificates', 'readonly');
        const request = tx.objectStore('certificates').getAll();
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
    });
}

// Initialize DB on load
openDatabase().then(() => {
    console.log('📦 IndexedDB initialized');
}).catch(err => {
    console.error('❌ IndexedDB error:', err);
});
