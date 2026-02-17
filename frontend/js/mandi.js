/**
 * 🛡️ Mangifera Shield — Mandi Price Module
 * Price fetching, display, and simple trend visualization
 */

async function loadMandiPrices() {
    let data = null;

    try {
        if (isOnline) {
            const res = await fetch(`${API_BASE}/api/mandi/prices`);
            data = await res.json();
            await cacheMandiPrices(data);
        } else {
            data = await getCachedMandiPrices();
        }
    } catch (err) {
        data = await getCachedMandiPrices();
    }

    if (!data) {
        // Use hardcoded fallback
        data = getHardcodedMandiData();
    }

    renderMandiPrices(data);
}

function getHardcodedMandiData() {
    return {
        prices: [
            { market: "Lucknow (Aminabad)", min_price: 3500, max_price: 5500, modal_price: 4500 },
            { market: "Delhi (Azadpur)", min_price: 4500, max_price: 6500, modal_price: 5500 },
            { market: "Malihabad Local", min_price: 3000, max_price: 4200, modal_price: 3600 },
            { market: "Kanpur", min_price: 3200, max_price: 5000, modal_price: 4100 },
            { market: "Varanasi", min_price: 3300, max_price: 4800, modal_price: 4000 },
            { market: "Agra", min_price: 3400, max_price: 5200, modal_price: 4300 },
            { market: "Allahabad", min_price: 3100, max_price: 4600, modal_price: 3800 },
            { market: "Mumbai (Vashi)", min_price: 5000, max_price: 7500, modal_price: 6200 }
        ],
        statistics: {
            best_price: 7500,
            best_market: "Mumbai (Vashi)",
            average_price: 4500,
            min_price: 3000
        },
        trends: {
            last_week: "+5%",
            last_month: "+12%",
            peak_month: "June"
        },
        middleman_analysis: {
            avg_middleman_cut: "18-22%",
            direct_selling_savings: "₹800-1200 per quintal"
        },
        source: "Cached Data"
    };
}

function renderMandiPrices(data) {
    const prices = data.prices || [];
    const stats = data.statistics || {};

    // Best price card
    document.getElementById('best-market').textContent = stats.best_market || 'Delhi (Azadpur Mandi)';
    document.getElementById('best-amount').textContent = `₹${(stats.best_price || 6500).toLocaleString()}/Quintal`;

    // Calculate middleman difference
    const middlemanCut = stats.best_price ? Math.round(stats.best_price * 0.2) : 1300;
    document.getElementById('best-diff').innerHTML = `
        <span>${t('vs_middleman')}</span>
        <span class="diff-value">+₹${middlemanCut.toLocaleString()}</span>
    `;

    // Price table
    const tbody = document.getElementById('price-tbody');
    tbody.innerHTML = prices.map(p => `
        <tr>
            <td>${p.market}</td>
            <td>₹${(p.min_price || 0).toLocaleString()}</td>
            <td>₹${(p.max_price || 0).toLocaleString()}</td>
            <td class="price-highlight">₹${(p.modal_price || 0).toLocaleString()}</td>
        </tr>
    `).join('');

    // Trend insight
    const trends = data.trends || {};
    const insight = document.getElementById('trend-insight');
    if (currentLang === 'hi') {
        insight.textContent = `पिछले हफ्ते: ${trends.last_week || '+5%'} | पिछले महीने: ${trends.last_month || '+12%'} | पीक महीना: ${trends.peak_month || 'जून'}`;
    } else {
        insight.textContent = `Last Week: ${trends.last_week || '+5%'} | Last Month: ${trends.last_month || '+12%'} | Peak Month: ${trends.peak_month || 'June'}`;
    }

    // Updated time
    document.getElementById('price-updated').textContent = ` • ${new Date().toLocaleTimeString()}`;

    // Draw simple trend chart
    drawTrendChart(prices);
}

function drawTrendChart(prices) {
    const canvas = document.getElementById('trend-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const container = canvas.parentElement;

    // Set canvas size
    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;

    const w = canvas.width;
    const h = canvas.height;
    const pad = 40;

    // Clear
    ctx.clearRect(0, 0, w, h);

    if (prices.length < 2) return;

    const modalPrices = prices.map(p => p.modal_price || 0);
    const maxPrice = Math.max(...modalPrices) * 1.1;
    const minPrice = Math.min(...modalPrices) * 0.9;
    const range = maxPrice - minPrice || 1;

    // Grid lines
    ctx.strokeStyle = 'rgba(34, 197, 94, 0.1)';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
        const y = pad + (h - pad * 2) * (i / 4);
        ctx.beginPath();
        ctx.moveTo(pad, y);
        ctx.lineTo(w - pad, y);
        ctx.stroke();

        // Price labels
        const price = Math.round(maxPrice - (range * i / 4));
        ctx.fillStyle = 'rgba(255,255,255,0.3)';
        ctx.font = '10px Inter';
        ctx.textAlign = 'right';
        ctx.fillText(`₹${price}`, pad - 5, y + 4);
    }

    // Draw line
    const stepX = (w - pad * 2) / (modalPrices.length - 1);

    // Gradient fill
    const gradient = ctx.createLinearGradient(0, pad, 0, h - pad);
    gradient.addColorStop(0, 'rgba(34, 197, 94, 0.3)');
    gradient.addColorStop(1, 'rgba(34, 197, 94, 0.01)');

    // Fill area
    ctx.beginPath();
    ctx.moveTo(pad, h - pad);
    modalPrices.forEach((price, i) => {
        const x = pad + stepX * i;
        const y = pad + (h - pad * 2) * (1 - (price - minPrice) / range);
        if (i === 0) ctx.lineTo(x, y);
        else ctx.lineTo(x, y);
    });
    ctx.lineTo(pad + stepX * (modalPrices.length - 1), h - pad);
    ctx.closePath();
    ctx.fillStyle = gradient;
    ctx.fill();

    // Draw line on top
    ctx.beginPath();
    ctx.strokeStyle = '#22c55e';
    ctx.lineWidth = 2;
    modalPrices.forEach((price, i) => {
        const x = pad + stepX * i;
        const y = pad + (h - pad * 2) * (1 - (price - minPrice) / range);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    });
    ctx.stroke();

    // Draw dots
    modalPrices.forEach((price, i) => {
        const x = pad + stepX * i;
        const y = pad + (h - pad * 2) * (1 - (price - minPrice) / range);

        ctx.beginPath();
        ctx.arc(x, y, 4, 0, Math.PI * 2);
        ctx.fillStyle = '#22c55e';
        ctx.fill();
        ctx.strokeStyle = '#0a0f0d';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Market labels
        const shortName = prices[i].market.split('(')[0].trim().substring(0, 8);
        ctx.fillStyle = 'rgba(255,255,255,0.4)';
        ctx.font = '9px Inter';
        ctx.textAlign = 'center';
        ctx.fillText(shortName, x, h - pad + 14);
    });
}
