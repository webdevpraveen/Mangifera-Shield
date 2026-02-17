/**
 * 🛡️ Mangifera Shield — Main Application Controller
 * Routing, navigation, online/offline detection, splash screen
 */

const API_BASE = window.location.origin;
let isOnline = navigator.onLine;
let currentPage = 'dashboard';
let lastScanResult = null;
let deferredInstallPrompt = null;

// === PWA INSTALL PROMPT ===
window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredInstallPrompt = e;
    // Show install banner after 5 seconds
    setTimeout(() => {
        const banner = document.getElementById('install-banner');
        if (banner) banner.classList.remove('hidden');
    }, 5000);
});

function installPWA() {
    if (!deferredInstallPrompt) return;
    deferredInstallPrompt.prompt();
    deferredInstallPrompt.userChoice.then(choice => {
        if (choice.outcome === 'accepted') {
            showToast('✅ App installed!');
        }
        deferredInstallPrompt = null;
        document.getElementById('install-banner').classList.add('hidden');
    });
}

// === INITIALIZATION ===
document.addEventListener('DOMContentLoaded', async () => {
    // Show splash for 2.5 seconds
    setTimeout(() => {
        const splash = document.getElementById('splash-screen');
        const app = document.getElementById('app');
        splash.style.opacity = '0';
        splash.style.transition = 'opacity 0.5s ease';
        setTimeout(() => {
            splash.style.display = 'none';
            app.classList.remove('hidden');
            initApp();
        }, 500);
    }, 2500);
});

async function initApp() {
    // Set saved language
    setLanguage(currentLang);

    // Setup online/offline detection
    setupNetworkDetection();

    // Setup language toggle
    document.getElementById('lang-toggle').addEventListener('click', toggleLanguage);

    // Initialize all modules
    await loadDashboardData();
    initScanner();
    loadLedgerEntries();
    loadMandiPrices();
    loadWeatherData();
    updateSavingsCard();

    // Bind install button
    const installBtn = document.getElementById('install-btn');
    if (installBtn) installBtn.addEventListener('click', installPWA);

    // Register service worker
    registerSW();

    // 🚨 Auto-check weather alerts (proactive voice alert after 3s)
    setTimeout(() => {
        if (typeof checkAutoAlerts === 'function') checkAutoAlerts();
    }, 3000);

    console.log('🛡️ Mangifera Shield initialized!');
}

// === NAVIGATION ===
function navigateTo(page) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));

    // Show target page
    const targetPage = document.getElementById(`page-${page}`);
    if (targetPage) {
        targetPage.classList.add('active');
        currentPage = page;
    }

    // Update nav items
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.toggle('active', item.getAttribute('data-page') === page);
    });

    // Page-specific loading
    if (page === 'mandi') loadMandiPrices();
    if (page === 'weather') loadWeatherData();
    if (page === 'ledger') loadLedgerEntries();
    if (page === 'certificate') loadCertificateScanOptions();

    // Scroll to top
    window.scrollTo(0, 0);
}

// === NETWORK DETECTION ===
function setupNetworkDetection() {
    updateOnlineStatus();

    window.addEventListener('online', () => {
        isOnline = true;
        updateOnlineStatus();
        showToast('✅ Back online! Syncing data...');
        trySyncAll();

        // Register background sync with service worker
        if ('serviceWorker' in navigator && navigator.serviceWorker.controller) {
            navigator.serviceWorker.controller.postMessage({ type: 'REGISTER_SYNC' });
        }
    });

    window.addEventListener('offline', () => {
        isOnline = false;
        updateOnlineStatus();
        showToast('📴 Offline mode — all features still work!');
    });
}

function updateOnlineStatus() {
    const indicator = document.getElementById('online-indicator');
    const statusText = indicator.querySelector('.status-text');

    if (isOnline) {
        indicator.classList.remove('offline');
        statusText.setAttribute('data-i18n', 'status_online');
        statusText.textContent = t('status_online');
    } else {
        indicator.classList.add('offline');
        statusText.setAttribute('data-i18n', 'status_offline');
        statusText.textContent = t('status_offline');
    }
}

// === DASHBOARD DATA ===
async function loadDashboardData() {
    try {
        // Load scan count
        const scans = await getScanResults();
        document.getElementById('stat-scans').textContent = scans.length;

        // Update recent scans
        updateRecentScans(scans.slice(0, 5));

        // Load stock
        const entries = await getLedgerEntries();
        const totalKg = entries.reduce((sum, e) => sum + (e.quantityKg || 0), 0);
        document.getElementById('stat-stock').textContent = `${totalKg} kg`;

        // Load mandi prices
        if (isOnline) {
            try {
                const res = await fetch(`${API_BASE}/api/mandi/prices`);
                const data = await res.json();
                if (data.statistics) {
                    document.getElementById('stat-price').textContent = `₹${data.statistics.best_price}`;
                }
                await cacheMandiPrices(data);
            } catch (e) {
                const cached = await getCachedMandiPrices();
                if (cached && cached.statistics) {
                    document.getElementById('stat-price').textContent = `₹${cached.statistics.best_price}`;
                }
            }
        } else {
            const cached = await getCachedMandiPrices();
            if (cached && cached.statistics) {
                document.getElementById('stat-price').textContent = `₹${cached.statistics.best_price}`;
            }
        }

        // Load weather alerts
        if (isOnline) {
            try {
                const res = await fetch(`${API_BASE}/api/weather/alerts`);
                const data = await res.json();
                document.getElementById('stat-alerts').textContent = data.total_alerts || 0;
                await cacheWeatherData(data);

                if (data.alerts && data.alerts.length > 0) {
                    const banner = document.getElementById('dashboard-alert');
                    const msg = document.getElementById('alert-message');
                    banner.classList.remove('hidden');
                    msg.textContent = `${data.alerts[0].disease}: ${currentLang === 'hi' ? data.alerts[0].description_hi : data.alerts[0].description_en}`;
                }
            } catch (e) {
                // Use cached
            }
        }
    } catch (err) {
        console.error('Dashboard load error:', err);
    }
}

function updateRecentScans(scans) {
    const list = document.getElementById('recent-scans-list');
    if (!scans || scans.length === 0) {
        list.innerHTML = `
            <div class="empty-state">
                <span class="empty-icon">📷</span>
                <p data-i18n="no_scans">${t('no_scans')}</p>
            </div>`;
        return;
    }

    list.innerHTML = scans.map(scan => `
        <div class="ledger-entry-card">
            <div class="entry-icon">${scan.isHealthy ? '✅' : '⚠️'}</div>
            <div class="entry-info">
                <div class="entry-title">${scan.disease}</div>
                <div class="entry-meta">${new Date(scan.createdAt).toLocaleDateString()} • ${(scan.confidence * 100).toFixed(1)}%</div>
            </div>
            <div class="entry-qty" style="color: ${scan.isHealthy ? 'var(--success)' : 'var(--danger)'}">
                ${scan.isHealthy ? 'Healthy' : scan.disease}
            </div>
        </div>
    `).join('');
}

// === DISEASE INFO CARDS ===
async function loadDiseaseCards() {
    const grid = document.getElementById('disease-cards');
    if (!grid) return;

    try {
        let classes;
        if (isOnline) {
            const res = await fetch(`${API_BASE}/api/disease/classes`);
            const data = await res.json();
            classes = data.classes;
        }

        if (!classes) {
            classes = [
                { name: "Anthracnose", name_hi: "एन्थ्रेक्नोज", severity: "High" },
                { name: "Bacterial Canker", name_hi: "बैक्टीरियल कैंकर", severity: "High" },
                { name: "Cutting Weevil", name_hi: "कटिंग वीविल", severity: "Medium" },
                { name: "Die Back", name_hi: "डाई-बैक", severity: "High" },
                { name: "Gall Midge", name_hi: "गॉल मिज", severity: "Medium" },
                { name: "Healthy", name_hi: "स्वस्थ", severity: "None" },
                { name: "Powdery Mildew", name_hi: "पाउडरी मिल्ड्यू", severity: "Critical" },
                { name: "Sooty Mould", name_hi: "सूटी मोल्ड", severity: "Medium" }
            ];
        }

        grid.innerHTML = classes.map(cls => `
            <div class="disease-card" onclick="showDiseaseDetail('${cls.name}')">
                <div class="disease-card-name">${currentLang === 'hi' ? cls.name_hi : cls.name}</div>
                <span class="disease-card-severity severity-${cls.severity}">${cls.severity}</span>
            </div>
        `).join('');
    } catch (e) {
        console.error('Disease cards error:', e);
    }
}

function showDiseaseDetail(name) {
    // Navigate to scanner page where disease details are shown
    navigateTo('scanner');
    showToast(`ℹ️ ${name}`);
}

// === SYNC ===
async function trySyncAll() {
    if (!isOnline) return;
    try {
        await syncLedger();
    } catch (e) {
        console.error('Sync error:', e);
    }
}

// === TOAST ===
function showToast(message, duration = 3000) {
    const toast = document.getElementById('toast');
    const toastMsg = document.getElementById('toast-message');
    toastMsg.textContent = message;
    toast.classList.remove('hidden');
    setTimeout(() => toast.classList.add('hidden'), duration);
}

// === SERVICE WORKER ===
function registerSW() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js')
            .then(reg => console.log('✅ Service Worker registered:', reg.scope))
            .catch(err => console.log('⚠️ SW registration failed:', err));
    }
}

// === UTILITY ===
function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

function formatCurrency(amount) {
    return '₹' + Number(amount).toLocaleString('en-IN');
}

function formatDate(dateStr) {
    try {
        return new Date(dateStr).toLocaleDateString(currentLang === 'hi' ? 'hi-IN' : 'en-IN', {
            day: 'numeric',
            month: 'short',
            year: 'numeric'
        });
    } catch {
        return dateStr;
    }
}

// === MIDDLEMAN SAVINGS CALCULATOR ===
async function updateSavingsCard() {
    try {
        let bestPrice = 6500;
        let localPrice = 3600;

        // Try to get real mandi data
        if (isOnline) {
            try {
                const res = await fetch(`${API_BASE}/api/mandi/prices`);
                const data = await res.json();
                if (data.statistics) {
                    bestPrice = data.statistics.best_price || bestPrice;
                    localPrice = data.statistics.min_price || localPrice;
                }
            } catch (e) { /* use defaults */ }
        }

        const middlemanCut = Math.round(bestPrice * 0.20); // ~20%
        const savings = bestPrice - localPrice;

        const amountEl = document.getElementById('savings-amount');
        const detailEl = document.getElementById('savings-detail');

        if (amountEl) {
            amountEl.textContent = `₹${savings.toLocaleString()}/quintal`;
        }
        if (detailEl) {
            const isHi = currentLang === 'hi';
            detailEl.textContent = isHi
                ? `बिचौलिये का कट ~₹${middlemanCut.toLocaleString()}/क्विंटल। सीधे बेचें और बचाएं!`
                : `Middleman takes ~₹${middlemanCut.toLocaleString()}/quintal. Sell directly & save!`;
        }
    } catch (e) {
        console.log('Savings calc error:', e);
    }
}
