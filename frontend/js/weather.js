/**
 * 🛡️ Mangifera Shield — Weather & Disease Alert Module
 * ✅ PROACTIVE: Auto-checks weather → Voice alert if disease risk detected
 * Fetches weather data and displays disease-risk gauges
 */

let lastAutoAlertTime = 0;
const AUTO_ALERT_COOLDOWN = 10 * 60 * 1000; // 10 min cooldown (demo-friendly)

async function loadWeatherData() {
    let data = null;

    try {
        if (isOnline) {
            const res = await fetch(`${API_BASE}/api/weather/current`);
            data = await res.json();
            await cacheWeatherData(data);
        } else {
            data = await getCachedWeather();
        }
    } catch (err) {
        data = await getCachedWeather();
    }

    if (!data) {
        data = getDemoWeatherData();
    }

    renderWeather(data);
    return data;
}

// ===============================
// AUTOMATIC WEATHER ALERTS (PROACTIVE)
// ===============================
async function checkAutoAlerts() {
    const now = Date.now();
    const lastAlert = parseInt(localStorage.getItem('lastAutoAlert') || '0');

    // Don't repeat within cooldown period
    if (now - lastAlert < AUTO_ALERT_COOLDOWN) {
        console.log('⏰ Auto-alert cooldown active, skipping.');
        return;
    }

    let data = null;
    try {
        if (typeof isOnline !== 'undefined' && isOnline) {
            const res = await fetch(`${API_BASE}/api/weather/current`);
            data = await res.json();
        } else {
            data = typeof getCachedWeather !== 'undefined' ? await getCachedWeather() : null;
        }
    } catch (e) {
        data = null;
    }

    if (!data) data = getDemoWeatherData();

    const risks = data.disease_risks || [];
    const criticalAlerts = risks.filter(r => r.risk_level === 'CRITICAL' || r.risk_level === 'HIGH');

    if (criticalAlerts.length === 0) return;

    // Show dashboard alert banner
    showDashboardAlert(criticalAlerts[0]);

    // Update alert count on dashboard
    const alertStat = document.getElementById('stat-alerts');
    if (alertStat) alertStat.textContent = criticalAlerts.length;

    // 🚨 HERO FEATURE: Show dramatic proactive modal
    const topAlert = criticalAlerts[0];
    showProactiveModal(topAlert);

    // Save timestamp
    localStorage.setItem('lastAutoAlert', now.toString());
}

function showDashboardAlert(alert) {
    const banner = document.getElementById('dashboard-alert');
    const alertMsg = document.getElementById('alert-message');

    if (banner && alertMsg) {
        const isHi = typeof currentLang !== 'undefined' && currentLang === 'hi';
        banner.classList.remove('hidden');
        alertMsg.textContent = isHi
            ? (alert.spray_advisory_hi || alert.description_hi || alert.description_en)
            : (alert.spray_advisory_en || alert.description_en);
    }
}

function fireVoiceAlert(alert) {
    if (!('speechSynthesis' in window)) return;

    const isHi = typeof currentLang !== 'undefined' && currentLang === 'hi';

    let message;
    if (alert.risk_level === 'CRITICAL') {
        message = isHi
            ? `⚠️ खतरा! ${alert.disease_hi || alert.disease} का गंभीर खतरा है! ${alert.spray_advisory_hi || ''} तुरंत छिड़काव करें!`
            : `⚠️ DANGER! Critical ${alert.disease} risk detected! ${alert.spray_advisory_en || ''} Spray immediately!`;
    } else {
        message = isHi
            ? `⚠️ सावधान! ${alert.disease_hi || alert.disease} का खतरा बढ़ रहा है। ${alert.spray_advisory_hi || ''}`
            : `⚠️ Warning! ${alert.disease} risk is high. ${alert.spray_advisory_en || ''}`;
    }

    // Show toast
    if (typeof showToast !== 'undefined') {
        showToast(`🚨 ${isHi ? (alert.disease_hi || alert.disease) : alert.disease}: ${isHi ? alert.spray_advisory_hi : alert.spray_advisory_en}`);
    }

    // Speak alert
    setTimeout(() => {
        const utterance = new SpeechSynthesisUtterance(message);
        utterance.lang = isHi ? 'hi-IN' : 'en-IN';
        utterance.rate = 0.9;
        utterance.volume = 1.0;
        utterance.pitch = 1.1;

        // Try to find Hindi voice
        const voices = speechSynthesis.getVoices();
        if (isHi) {
            const hindiVoice = voices.find(v => v.lang.includes('hi'));
            if (hindiVoice) utterance.voice = hindiVoice;
        }

        speechSynthesis.speak(utterance);
        console.log('🔊 Voice alert fired:', message);
    }, 1000);
}

// 🚨 HERO: Dramatic proactive alert modal
function showProactiveModal(alert) {
    const modal = document.getElementById('proactive-alert-modal');
    if (!modal) return;

    const isHi = typeof currentLang !== 'undefined' && currentLang === 'hi';

    document.getElementById('proactive-title').textContent = isHi
        ? '⚠️ बीमारी का खतरा!' : '⚠️ Disease Risk Detected!';
    document.getElementById('proactive-disease').textContent = isHi
        ? (alert.disease_hi || alert.disease) : alert.disease;
    document.getElementById('proactive-risk').textContent = alert.risk_level;
    document.getElementById('proactive-risk').className = `proactive-risk risk-${alert.risk_level}`;
    document.getElementById('proactive-message').textContent = isHi
        ? (alert.spray_advisory_hi || alert.description_hi) : (alert.spray_advisory_en || alert.description_en);

    modal.classList.remove('hidden');

    // Fire voice alert after a short delay (dramatic effect)
    setTimeout(() => fireVoiceAlert(alert), 1500);
}

function closeProactiveAlert() {
    const modal = document.getElementById('proactive-alert-modal');
    if (modal) modal.classList.add('hidden');
}

// ===============================
// DEMO WEATHER DATA
// ===============================
function getDemoWeatherData() {
    return {
        weather: {
            temp: 22,
            humidity: 68,
            wind_speed: 3.2,
            description: "Partly cloudy",
            location: "Malihabad, Lucknow"
        },
        disease_risks: [
            {
                disease: "Powdery Mildew",
                disease_hi: "छाछ्या/खर्रा",
                risk_level: "CRITICAL",
                risk_score: 85,
                description_en: "Temp 22°C & Humidity 68% within danger zone (11-31°C, 64-72%). Immediate action needed during Dasheri flowering.",
                description_hi: "तापमान 22°C और नमी 68% खतरे के क्षेत्र में (11-31°C, 64-72%)। दशहरी बौर के दौरान तत्काल कार्रवाई ज़रूरी।",
                spray_advisory_en: "Spray Sulfur (0.2%) or Karathane (0.1%) immediately",
                spray_advisory_hi: "तुरंत सल्फर (0.2%) या कैराथेन (0.1%) का छिड़काव करें"
            },
            {
                disease: "Anthracnose",
                disease_hi: "एन्थ्रेक्नोज",
                risk_level: "HIGH",
                risk_score: 72,
                description_en: "Humidity 68% favors Anthracnose development. Monitor fruit and leaves for dark spots.",
                description_hi: "68% नमी एन्थ्रेक्नोज के विकास के अनुकूल। फलों और पत्तियों पर काले धब्बों की निगरानी करें।",
                spray_advisory_en: "Apply Carbendazim (0.1%) preventive spray",
                spray_advisory_hi: "कार्बेन्डाजिम (0.1%) का रोकथाम छिड़काव करें"
            },
            {
                disease: "Sooty Mould",
                disease_hi: "कालिका/काला फफूंद",
                risk_level: "MODERATE",
                risk_score: 45,
                description_en: "Moderate humidity may support sooty mould with hopper infestation.",
                description_hi: "मध्यम नमी हॉपर संक्रमण के साथ सूटी मोल्ड को बढ़ावा दे सकती है।",
                spray_advisory_en: "Monitor for hoppers. Spray Imidacloprid if needed.",
                spray_advisory_hi: "हॉपर की निगरानी करें। ज़रूरत पर इमिडाक्लोप्रिड का छिड़काव करें।"
            },
            {
                disease: "Gall Midge",
                disease_hi: "गॉल मिज",
                risk_level: "LOW",
                risk_score: 20,
                description_en: "Current conditions do not strongly favor gall midge infestation.",
                description_hi: "वर्तमान परिस्थितियाँ गॉल मिज संक्रमण के लिए बहुत अनुकूल नहीं हैं।",
                spray_advisory_en: "Routine monitoring is sufficient.",
                spray_advisory_hi: "नियमित निगरानी पर्याप्त है।"
            }
        ],
        local_factors: {
            construction_dust: "Malihabad highway construction increases dust stress on mango trees.",
            construction_dust_hi: "मलिहाबाद हाईवे निर्माण से आम के पेड़ों पर धूल का तनाव बढ़ता है।",
            irrigation: "Groundwater levels low in Feb — ensure drip irrigation for young orchards.",
            irrigation_hi: "फरवरी में भूजल स्तर कम — युवा बागों में ड्रिप सिंचाई सुनिश्चित करें।",
            market_timing: "Peak Dasheri season June-July. Plan spray schedule accordingly.",
            market_timing_hi: "दशहरी का मौसम जून-जुलाई। छिड़काव अनुसूची की योजना बनाएं।"
        }
    };
}

// ===============================
// RENDER WEATHER UI
// ===============================
function renderWeather(data) {
    const weather = data.weather || {};
    const risks = data.disease_risks || [];
    const factors = data.local_factors || {};

    // Current weather
    document.getElementById('weather-temp').textContent = `${weather.temp || 22}°C`;
    document.getElementById('weather-humidity').textContent = `${weather.humidity || 68}%`;
    document.getElementById('weather-wind').textContent = `${weather.wind_speed || 3.2} km/h`;

    // Risk gauges
    const gaugeContainer = document.getElementById('risk-gauges');
    gaugeContainer.innerHTML = risks.map(risk => {
        const riskColor = getRiskColor(risk.risk_level);
        const isHi = currentLang === 'hi';
        return `
            <div class="risk-gauge">
                <div class="risk-header">
                    <span class="risk-disease">${isHi ? (risk.disease_hi || risk.disease) : risk.disease}</span>
                    <span class="risk-badge risk-${risk.risk_level}">${risk.risk_level}</span>
                </div>
                <div class="risk-bar">
                    <div class="risk-fill" style="width: ${risk.risk_score}%; background: ${riskColor}"></div>
                </div>
                <div class="risk-info">${isHi ? (risk.description_hi || risk.description_en) : risk.description_en}</div>
                <div class="risk-info" style="color: ${riskColor}; margin-top: 4px; font-weight: 500;">
                    💊 ${isHi ? (risk.spray_advisory_hi || risk.spray_advisory_en) : risk.spray_advisory_en}
                </div>
            </div>
        `;
    }).join('');

    // Alerts (critical/high only)
    const alertContainer = document.getElementById('weather-alerts');
    const criticalAlerts = risks.filter(r => r.risk_level === 'CRITICAL' || r.risk_level === 'HIGH');

    if (criticalAlerts.length === 0) {
        alertContainer.innerHTML = `
            <div class="empty-state">
                <span class="empty-icon">✅</span>
                <p>${currentLang === 'hi' ? 'कोई गंभीर अलर्ट नहीं' : 'No critical alerts'}</p>
            </div>`;
    } else {
        alertContainer.innerHTML = criticalAlerts.map(alert => `
            <div class="alert-card ${alert.risk_level.toLowerCase()}">
                <div class="alert-card-icon">${alert.risk_level === 'CRITICAL' ? '🚨' : '⚠️'}</div>
                <div>
                    <div class="alert-card-title">${currentLang === 'hi' ? (alert.disease_hi || alert.disease) : alert.disease}</div>
                    <div class="alert-card-text">${currentLang === 'hi' ? (alert.description_hi || alert.description_en) : alert.description_en}</div>
                </div>
            </div>
        `).join('');
    }

    // Local advisory
    const advisoryContent = document.getElementById('advisory-content');
    const isHi = currentLang === 'hi';

    advisoryContent.innerHTML = `
        <div class="advisory-item">🏗️ ${isHi ? (factors.construction_dust_hi || factors.construction_dust || '') : (factors.construction_dust || '')}</div>
        <div class="advisory-item">💧 ${isHi ? (factors.irrigation_hi || factors.irrigation || '') : (factors.irrigation || '')}</div>
        <div class="advisory-item">📅 ${isHi ? (factors.market_timing_hi || factors.market_timing || '') : (factors.market_timing || '')}</div>
    `;
}

function getRiskColor(level) {
    const colors = {
        'CRITICAL': '#ef4444',
        'HIGH': '#f97316',
        'MODERATE': '#f59e0b',
        'LOW': '#22c55e'
    };
    return colors[level] || '#6b7280';
}
