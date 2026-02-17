/**
 * 🛡️ Mangifera Shield — Internationalization Engine
 * Hindi/English translations with dynamic language switching
 */

const TRANSLATIONS = {
    en: {
        // Splash
        splash_subtitle: "Protecting Malihabad's Mango Heritage",
        splash_tagline: "Edge AI • Offline First • Voice Enabled",

        // Status
        status_online: "Online",
        status_offline: "Offline",

        // Navigation
        nav_home: "Home",
        nav_scan: "Scan",
        nav_khata: "Khata",
        nav_rate: "Rates",
        nav_alert: "Alerts",
        nav_scanner: "Scan Disease",
        nav_ledger: "Khet-Khata",
        nav_mandi: "Mandi Rates",
        nav_weather: "Weather Alerts",
        nav_certificate: "Quality Cert",
        nav_voice: "Voice Command",

        // Dashboard
        dashboard_title: "🏠 Dashboard",
        dashboard_desc: "Welcome to Mangifera Shield, Kisan!",
        stat_scans: "Scans Done",
        stat_stock: "Total Stock",
        stat_price: "Best Rate",
        stat_alerts: "Alerts",
        quick_actions: "⚡ Quick Actions",
        recent_scans: "🔬 Recent Scans",
        no_scans: "No scans yet. Tap \"Scan Disease\" to start!",
        alert_title: "Disease Risk Alert",

        // Scanner
        scanner_title: "📸 Disease Scanner",
        scanner_desc: "Capture or upload a mango leaf image for AI diagnosis",
        upload_text: "Tap to capture or upload leaf image",
        upload_hint: "JPG, PNG — Clear close-up of the leaf",
        retake: "Retake",
        scan_now: "Scan Now",
        scanning: "AI analyzing...",
        description: "📋 Description",
        symptoms: "🔍 Symptoms",
        treatment: "💊 Treatment",
        prevention: "🛡️ Prevention",
        gen_certificate: "Generate Certificate",
        share: "Share",
        disease_info: "📚 Disease Information",

        // Ledger
        ledger_title: "📒 Khet-Khata",
        ledger_desc: "Your offline inventory ledger — works without internet!",
        total_quantity: "Total Quantity",
        estimated_value: "Est. Value",
        total_entries: "Entries",
        sync_status: "All data saved locally",
        sync: "Sync",
        add_entry: "Add Entry",
        variety: "🥭 Variety",
        quantity_kg: "⚖️ Quantity (kg)",
        quality_grade: "⭐ Quality",
        harvest_date: "📅 Harvest Date",
        est_price: "💰 Est. Price (₹/kg)",
        notes: "📝 Notes",
        save: "Save Entry",
        cancel: "Cancel",

        // Mandi
        mandi_title: "🏪 Mandi Prices",
        mandi_desc: "Dasheri mango rates from UP mandis",
        best_rate: "Best Rate",
        vs_middleman: "vs Middleman: ",
        middleman_title: "Middleman Cut: ~20%",
        middleman_text: "Save ₹900/quintal by selling directly with verified quality certificates!",
        market: "Market",
        min_price: "Min ₹",
        max_price: "Max ₹",
        modal_price: "Modal ₹",
        price_trend: "📈 Price Trend",
        data_source: "Source: data.gov.in / AGMARKNET",

        // Weather
        weather_title: "🌤️ Weather & Disease Alerts",
        weather_desc: "Malihabad-specific weather monitoring for disease prediction",
        humidity: "Humidity:",
        wind: "Wind:",
        disease_risk: "🎯 Disease Risk Level",
        active_alerts: "🚨 Active Alerts",
        malihabad_advisory: "Malihabad Advisory",

        // Certificate
        cert_title: "📜 Quality Certificate",
        cert_desc: "AI-verified proof of quality for premium buyers",
        farmer_name: "👤 Farmer Name",
        select_scan: "🔬 Select Scan Result",
        generate_cert: "Generate Certificate",
        quality_cert: "Quality Certificate",
        past_certs: "📋 Past Certificates",
        no_certs: "No certificates generated yet.",

        // Voice
        voice_listening: "Listening...",
        voice_cmd_1: "\"Mandi ka rate\"",
        voice_cmd_2: "\"Mausam\"",
        voice_cmd_3: "\"Stock check\"",
        voice_cmd_4: "\"Bimari jaanch\"",

        // WhatsApp & Expert
        sell_whatsapp: "Sell on WhatsApp",
        ask_expert: "Ask Expert",
        ai_model_loading: "Loading AI model..."
    },

    hi: {
        // Splash
        splash_subtitle: "मलिहाबाद की आम की विरासत की रक्षा",
        splash_tagline: "एज AI • ऑफ़लाइन फ़र्स्ट • वॉयस एनेबल्ड",

        // Status
        status_online: "ऑनलाइन",
        status_offline: "ऑफ़लाइन",

        // Navigation
        nav_home: "होम",
        nav_scan: "स्कैन",
        nav_khata: "खाता",
        nav_rate: "भाव",
        nav_alert: "अलर्ट",
        nav_scanner: "रोग स्कैन करें",
        nav_ledger: "खेत-खाता",
        nav_mandi: "मंडी भाव",
        nav_weather: "मौसम अलर्ट",
        nav_certificate: "गुणवत्ता प्रमाणपत्र",
        nav_voice: "वॉयस कमांड",

        // Dashboard
        dashboard_title: "🏠 डैशबोर्ड",
        dashboard_desc: "मैंगीफेरा शील्ड में आपका स्वागत है, किसान!",
        stat_scans: "स्कैन किए",
        stat_stock: "कुल स्टॉक",
        stat_price: "बेस्ट भाव",
        stat_alerts: "अलर्ट",
        quick_actions: "⚡ त्वरित कार्य",
        recent_scans: "🔬 हाल के स्कैन",
        no_scans: "अभी तक कोई स्कैन नहीं। \"रोग स्कैन\" पर टैप करें!",
        alert_title: "रोग खतरा अलर्ट",

        // Scanner
        scanner_title: "📸 रोग स्कैनर",
        scanner_desc: "AI निदान के लिए आम की पत्ती की तस्वीर खींचें या अपलोड करें",
        upload_text: "पत्ती की तस्वीर खींचने या अपलोड करने के लिए टैप करें",
        upload_hint: "JPG, PNG — पत्ती का साफ नज़दीकी फ़ोटो",
        retake: "दोबारा खींचें",
        scan_now: "अभी स्कैन करें",
        scanning: "AI जाँच कर रहा है...",
        description: "📋 विवरण",
        symptoms: "🔍 लक्षण",
        treatment: "💊 उपचार",
        prevention: "🛡️ रोकथाम",
        gen_certificate: "प्रमाणपत्र बनाएं",
        share: "शेयर करें",
        disease_info: "📚 रोग जानकारी",

        // Ledger
        ledger_title: "📒 खेत-खाता",
        ledger_desc: "आपका ऑफ़लाइन इन्वेंटरी खाता — बिना इंटरनेट के काम करता है!",
        total_quantity: "कुल मात्रा",
        estimated_value: "अनुमानित मूल्य",
        total_entries: "प्रविष्टियाँ",
        sync_status: "सभी डेटा स्थानीय रूप से सहेजा गया",
        sync: "सिंक",
        add_entry: "प्रविष्टि जोड़ें",
        variety: "🥭 किस्म",
        quantity_kg: "⚖️ मात्रा (किलो)",
        quality_grade: "⭐ गुणवत्ता",
        harvest_date: "📅 तुड़ाई की तारीख",
        est_price: "💰 अनुमानित भाव (₹/किलो)",
        notes: "📝 नोट्स",
        save: "सहेजें",
        cancel: "रद्द करें",

        // Mandi
        mandi_title: "🏪 मंडी भाव",
        mandi_desc: "UP की मंडियों से दशहरी आम के भाव",
        best_rate: "सबसे अच्छा भाव",
        vs_middleman: "बिचौलिये से: ",
        middleman_title: "बिचौलिया कट: ~20%",
        middleman_text: "सत्यापित गुणवत्ता प्रमाणपत्र से सीधे बेचकर ₹900/क्विंटल बचाएं!",
        market: "मंडी",
        min_price: "न्यूनतम ₹",
        max_price: "अधिकतम ₹",
        modal_price: "मॉडल ₹",
        price_trend: "📈 भाव ट्रेंड",
        data_source: "स्रोत: data.gov.in / AGMARKNET",

        // Weather
        weather_title: "🌤️ मौसम और रोग अलर्ट",
        weather_desc: "मलिहाबाद के लिए विशेष मौसम निगरानी",
        humidity: "नमी:",
        wind: "हवा:",
        disease_risk: "🎯 रोग खतरा स्तर",
        active_alerts: "🚨 सक्रिय अलर्ट",
        malihabad_advisory: "मलिहाबाद सलाहकार",

        // Certificate
        cert_title: "📜 गुणवत्ता प्रमाणपत्र",
        cert_desc: "प्रीमियम खरीदारों के लिए AI-सत्यापित गुणवत्ता प्रमाण",
        farmer_name: "👤 किसान का नाम",
        select_scan: "🔬 स्कैन परिणाम चुनें",
        generate_cert: "प्रमाणपत्र बनाएं",
        quality_cert: "गुणवत्ता प्रमाणपत्र",
        past_certs: "📋 पिछले प्रमाणपत्र",
        no_certs: "अभी तक कोई प्रमाणपत्र नहीं बनाया गया।",

        // Voice
        voice_listening: "सुन रहे हैं...",
        voice_cmd_1: "\"मंडी का रेट\"",
        voice_cmd_2: "\"मौसम\"",
        voice_cmd_3: "\"स्टॉक चेक\"",
        voice_cmd_4: "\"बीमारी जाँच\"",

        // WhatsApp & Expert
        sell_whatsapp: "WhatsApp पर बेचें",
        ask_expert: "विशेषज्ञ से पूछें",
        ai_model_loading: "AI मॉडल लोड हो रहा है..."
    }
};

let currentLang = 'en';

function setLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('dasheri_lang', lang);
    document.documentElement.setAttribute('data-lang', lang);

    // Update all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (TRANSLATIONS[lang] && TRANSLATIONS[lang][key]) {
            el.textContent = TRANSLATIONS[lang][key];
        }
    });

    // Update lang label
    const langLabel = document.getElementById('lang-label');
    if (langLabel) langLabel.textContent = lang === 'en' ? 'EN' : 'हि';
}

function toggleLanguage() {
    const newLang = currentLang === 'en' ? 'hi' : 'en';
    setLanguage(newLang);
}

function t(key) {
    return (TRANSLATIONS[currentLang] && TRANSLATIONS[currentLang][key]) || key;
}

// Initialize language from localStorage
(function () {
    const saved = localStorage.getItem('dasheri_lang');
    if (saved) currentLang = saved;
})();
