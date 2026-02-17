/**
 * 🛡️ Mangifera Shield — Khet-Khata Ledger Module
 * Offline-first harvest inventory management
 */

let ledgerFormVisible = false;

function toggleLedgerForm() {
    const form = document.getElementById('ledger-form');
    ledgerFormVisible = !ledgerFormVisible;

    if (ledgerFormVisible) {
        form.classList.remove('hidden');
        // Set default date to today
        document.getElementById('entry-date').value = new Date().toISOString().split('T')[0];
    } else {
        form.classList.add('hidden');
        clearLedgerForm();
    }
}

function clearLedgerForm() {
    document.getElementById('entry-variety').value = 'Dasheri';
    document.getElementById('entry-quantity').value = '';
    document.getElementById('entry-grade').value = 'A';
    document.getElementById('entry-date').value = '';
    document.getElementById('entry-price').value = '';
    document.getElementById('entry-notes').value = '';
}

async function saveLedgerEntry() {
    const variety = document.getElementById('entry-variety').value;
    const quantity = parseFloat(document.getElementById('entry-quantity').value);
    const grade = document.getElementById('entry-grade').value;
    const harvestDate = document.getElementById('entry-date').value;
    const price = parseFloat(document.getElementById('entry-price').value) || 0;
    const notes = document.getElementById('entry-notes').value;

    if (!quantity || quantity <= 0) {
        showToast('❌ Please enter a valid quantity');
        return;
    }

    if (!harvestDate) {
        showToast('❌ Please select a harvest date');
        return;
    }

    const entry = {
        clientId: generateUUID(),
        farmerPhone: '0000000000',
        variety: variety,
        quantityKg: quantity,
        qualityGrade: grade,
        harvestDate: harvestDate,
        estimatedPrice: price,
        notes: notes,
        synced: false,
        createdAt: new Date().toISOString()
    };

    try {
        // Save to IndexedDB first (offline-first)
        await saveLedgerEntryDB(entry);

        // Try to sync to server
        if (isOnline) {
            try {
                await fetch(`${API_BASE}/api/ledger/entries`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        client_id: entry.clientId,
                        farmer_phone: entry.farmerPhone,
                        variety: entry.variety,
                        quantity_kg: entry.quantityKg,
                        quality_grade: entry.qualityGrade,
                        harvest_date: entry.harvestDate,
                        estimated_price: entry.estimatedPrice,
                        notes: entry.notes
                    })
                });
                await markLedgerSynced(entry.clientId);
            } catch (e) {
                console.log('Will sync later:', e);
            }
        }

        showToast('✅ Entry saved!');
        toggleLedgerForm();
        loadLedgerEntries();
        loadDashboardData();
    } catch (err) {
        console.error('Save error:', err);
        showToast('❌ Error saving entry');
    }
}

async function loadLedgerEntries() {
    const entries = await getLedgerEntries();
    const container = document.getElementById('ledger-entries');

    // Update summary
    const totalKg = entries.reduce((sum, e) => sum + (e.quantityKg || 0), 0);
    const totalValue = entries.reduce((sum, e) => sum + ((e.estimatedPrice || 0) * (e.quantityKg || 0)), 0);

    document.getElementById('ledger-total-qty').textContent = `${totalKg.toFixed(1)} kg`;
    document.getElementById('ledger-total-value').textContent = formatCurrency(totalValue);
    document.getElementById('ledger-total-entries').textContent = entries.length;

    // Update sync status
    const unsynced = entries.filter(e => !e.synced).length;
    const syncStatus = document.getElementById('sync-status');
    const syncBar = document.getElementById('sync-bar');

    if (unsynced > 0) {
        syncStatus.textContent = `${unsynced} entries pending sync`;
        syncBar.classList.remove('synced');
    } else {
        syncStatus.textContent = t('sync_status');
        syncBar.classList.add('synced');
    }

    // Render entries
    if (entries.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <span class="empty-icon">📒</span>
                <p>${currentLang === 'hi' ? 'अभी कोई प्रविष्टि नहीं। "प्रविष्टि जोड़ें" पर टैप करें!' : 'No entries yet. Tap "Add Entry" to start!'}</p>
            </div>`;
        return;
    }

    container.innerHTML = entries.map(e => `
        <div class="ledger-entry-card">
            <div class="entry-icon">🥭</div>
            <div class="entry-info">
                <div class="entry-title">${e.variety} — Grade ${e.qualityGrade}</div>
                <div class="entry-meta">
                    ${formatDate(e.harvestDate)} • 
                    ${e.synced ? '☁️ Synced' : '📱 Local'}
                    ${e.notes ? ' • ' + e.notes.substring(0, 30) : ''}
                </div>
            </div>
            <div class="entry-qty">${e.quantityKg} kg</div>
            <div class="entry-actions">
                <button class="entry-action-btn whatsapp-sell-btn" onclick="sellOnWhatsApp('${e.variety}', ${e.quantityKg}, '${e.qualityGrade}', ${e.estimatedPrice || 0})" title="Sell on WhatsApp">
                    <i class="fab fa-whatsapp"></i>
                </button>
                <button class="entry-action-btn" onclick="deleteLedgerEntry('${e.clientId}')" title="Delete">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `).join('');
}

async function deleteLedgerEntry(clientId) {
    if (!confirm(currentLang === 'hi' ? 'क्या आप वाकई हटाना चाहते हैं?' : 'Are you sure you want to delete?')) return;

    try {
        await deleteLedgerEntryDB(clientId);
        showToast('🗑️ Entry deleted');
        loadLedgerEntries();
        loadDashboardData();
    } catch (err) {
        showToast('❌ Error deleting');
    }
}

async function syncLedger() {
    if (!isOnline) {
        showToast('📴 No internet. Will sync when online.');
        return;
    }

    const unsynced = await getUnsyncedLedgerEntries();
    if (unsynced.length === 0) {
        showToast('✅ All entries are synced!');
        return;
    }

    showToast(`⏳ Syncing ${unsynced.length} entries...`);

    try {
        const entries = unsynced.map(e => ({
            client_id: e.clientId,
            farmer_phone: e.farmerPhone,
            variety: e.variety,
            quantity_kg: e.quantityKg,
            quality_grade: e.qualityGrade,
            harvest_date: e.harvestDate,
            estimated_price: e.estimatedPrice,
            notes: e.notes
        }));

        const res = await fetch(`${API_BASE}/api/ledger/sync`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ entries })
        });

        const data = await res.json();

        if (data.success) {
            for (const e of unsynced) {
                await markLedgerSynced(e.clientId);
            }
            showToast(`✅ ${data.synced} entries synced!`);
            loadLedgerEntries();
        }
    } catch (err) {
        console.error('Sync error:', err);
        showToast('❌ Sync failed. Will retry later.');
    }
}

// ===============================
// SELL ON WHATSAPP
// ===============================
function sellOnWhatsApp(variety, quantity, grade, price) {
    const lang = typeof currentLang !== 'undefined' ? currentLang : 'en';

    const message = lang === 'hi'
        ? `🥭 *मैंगीफेरा शील्ड — स्टॉक बिक्री*\n\n` +
        `📍 स्थान: मलिहाबाद, लखनऊ\n` +
        `🥭 किस्म: ${variety}\n` +
        `⚖️ मात्रा: ${quantity} kg\n` +
        `⭐ ग्रेड: ${grade}\n` +
        `💰 अपेक्षित मूल्य: ₹${price}/kg\n` +
        `📜 AI गुणवत्ता प्रमाणपत्र उपलब्ध\n\n` +
        `🛡️ मैंगीफेरा शील्ड — AI-सत्यापित गुणवत्ता`
        : `🥭 *Mangifera Shield — Stock for Sale*\n\n` +
        `📍 Location: Malihabad, Lucknow\n` +
        `🥭 Variety: ${variety}\n` +
        `⚖️ Quantity: ${quantity} kg\n` +
        `⭐ Grade: ${grade}\n` +
        `💰 Expected Price: ₹${price}/kg\n` +
        `📜 AI Quality Certificate Available\n\n` +
        `🛡️ Mangifera Shield — AI-Verified Quality`;

    const encoded = encodeURIComponent(message);
    window.open(`https://wa.me/?text=${encoded}`, '_blank');
    showToast('📱 WhatsApp opened!');
}

async function sellAllOnWhatsApp() {
    const entries = await getLedgerEntries();
    if (entries.length === 0) {
        showToast('📒 No stock to sell. Add entries first!');
        return;
    }

    const lang = typeof currentLang !== 'undefined' ? currentLang : 'en';
    const totalKg = entries.reduce((sum, e) => sum + (e.quantityKg || 0), 0);

    // Group by variety
    const byVariety = {};
    entries.forEach(e => {
        if (!byVariety[e.variety]) byVariety[e.variety] = { qty: 0, grade: e.qualityGrade, price: e.estimatedPrice };
        byVariety[e.variety].qty += e.quantityKg || 0;
    });

    const stockLines = Object.entries(byVariety).map(([v, d]) =>
        `  🥭 ${v}: ${d.qty} kg (Grade ${d.grade}) @ ₹${d.price || '—'}/kg`
    ).join('\n');

    const message = lang === 'hi'
        ? `🥭 *मैंगीफेरा शील्ड — बल्क स्टॉक बिक्री*\n\n` +
        `📍 स्थान: मलिहाबाद, लखनऊ\n` +
        `⚖️ कुल स्टॉक: ${totalKg} kg\n\n` +
        `📦 स्टॉक विवरण:\n${stockLines}\n\n` +
        `📜 AI गुणवत्ता प्रमाणपत्र उपलब्ध\n` +
        `☎️ संपर्क करें — सीधी बिक्री, बिचौलिया नहीं!\n\n` +
        `🛡️ मैंगीफेरा शील्ड — AI-सत्यापित गुणवत्ता`
        : `🥭 *Mangifera Shield — Bulk Stock for Sale*\n\n` +
        `📍 Location: Malihabad, Lucknow\n` +
        `⚖️ Total Stock: ${totalKg} kg\n\n` +
        `📦 Stock Details:\n${stockLines}\n\n` +
        `📜 AI Quality Certificate Available\n` +
        `☎️ Contact for Direct Purchase — No Middlemen!\n\n` +
        `🛡️ Mangifera Shield — AI-Verified Quality`;

    const encoded = encodeURIComponent(message);
    window.open(`https://wa.me/?text=${encoded}`, '_blank');
    showToast('📱 WhatsApp opened with full stock!');
}

