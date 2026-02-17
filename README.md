# 🛡️ Mangifera Shield — *Protecting Malihabad's Mango Heritage*

> **Edge AI × Offline-First × Voice-Enabled** AgriTech platform that empowers mango farmers in Malihabad, Lucknow with disease detection, market intelligence, and digital quality verification.

---

## 🎯 The Problem

Malihabad produces **60% of India's Dasheri mangoes**, yet farmers face:

| Challenge | Impact |
|-----------|--------|
| 🦠 Powdery Mildew outbreaks (Feb-March) | 30-40% crop loss during flowering |
| 🚫 Middleman exploitation | Farmers get only ₹3,000/quintal vs ₹6,500 market rate |
| 📴 No internet in orchards | Can't access government advisories in real-time |
| 📝 Paper-based records | Lost harvest data, no negotiation proof |
| 🏗️ Construction dust stress | Malihabad highway expansion weakens trees |

## 💡 Our Solution

**Mangifera Shield** is a Progressive Web App (PWA) that works **100% offline** in the orchard and provides:

### 🔬 AI Disease Scanner
- **ResNet50-based** deep learning model detecting **8 mango diseases**
- Works offline using **TensorFlow.js in-browser inference**
- Treatment recommendations in **Hindi & English** with specific dosages
- **99.21% accuracy** on MLD24/MangoLeafBD datasets

### 📒 Khet-Khata (Digital Ledger)
- **Offline-first** inventory management using IndexedDB
- Auto-syncs to cloud when connectivity returns
- Track variety, quantity, grade, and estimated prices
- Replaces paper notebooks with searchable digital records

### 🏪 Mandi Price Intelligence
- **Real-time prices** from 8+ UP mandis via data.gov.in/AGMARKNET
- **Middleman analysis**: Shows farmers they lose ~20% to intermediaries
- Price trends and peak season predictions
- Best market recommendations (Mumbai Vashi vs Delhi Azadpur)

### 🌤️ Disease Prediction Engine
- Malihabad-specific **temperature/humidity thresholds**
- Powdery Mildew risk: 11°C-31°C, 64%-72% humidity
- Spray advisories with exact chemical concentrations
- Construction dust impact warnings (Malihabad highway)

### 📜 AI Quality Certificates
- PDF certificates with **QR code verification**
- Proves disease-free status to premium buyers
- Bilingual (Hindi + English) for market compliance
- Eliminates need for costly manual inspections

### 🎤 Voice Navigation (Hinglish)
- **Web Speech API** — no API key, works instantly
- 40+ voice commands: "Mandi ka rate", "Mausam", "Bimari jaanch"
- Text-to-speech feedback in Hindi
- Designed for low-literacy farmers

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────┐
│                  PWA Frontend                     │
│  HTML/CSS/JS • IndexedDB • Service Worker • TF.js │
├──────────────────────────────────────────────────┤
│               FastAPI Backend                     │
│  Disease API • Ledger API • Mandi API • Weather   │
├──────────────────────────────────────────────────┤
│           SQLite + External APIs                  │
│  data.gov.in • OpenWeatherMap • AGMARKNET         │
└──────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Quick Start
1.  **Install Dependencies:** `pip install -r backend/requirements.txt`
2.  **Start the App:** `python run_app.py`
3.  **Open in Browser:** http://localhost:8000
- **ReDoc**: http://localhost:8000/api/redoc

---

## 📂 Project Structure

```
Dasheri-Sentinal/
├── backend/
│   ├── main.py                 # FastAPI server
│   ├── database.py             # SQLAlchemy models
│   ├── routes/
│   │   ├── disease.py          # AI disease detection
│   │   ├── ledger.py           # Khet-Khata CRUD + sync
│   │   ├── mandi.py            # Mandi price fetching
│   │   ├── weather.py          # Weather & disease alerts
│   │   └── certificate.py      # Quality certificate PDF
│   └── training/
│       ├── train_model.py      # ResNet50 Trainer + Imbalance Handling
│       └── eda.py              # Exploratory Data Analysis (Graphs)
│   └── services/
│       ├── treatment_engine.py # 8-disease knowledge base
│       ├── weather_service.py  # OpenWeatherMap + risk calc
│       ├── mandi_service.py    # AGMARKNET + cached data
│       └── certificate_service.py # PDF + QR generation
├── frontend/
│   ├── index.html              # SPA shell (6 pages)
│   ├── manifest.json           # PWA manifest
│   ├── sw.js                   # Service Worker
│   ├── css/styles.css          # Premium dark design system
│   └── js/
│       ├── app.js              # SPA router + orchestrator
│       ├── i18n.js             # Hindi/English (80+ keys)
│       ├── db.js               # IndexedDB wrapper
│       ├── scanner.js          # Image upload + inference
│       ├── ledger.js           # Offline CRUD + sync
│       ├── mandi.js            # Price table + trend chart
│       ├── weather.js          # Risk gauges + alerts
│       ├── certificate.js      # Certificate generation
│       └── voice.js            # Web Speech API (Hinglish)
├── .env.example
└── README.md
```

---

## 🧪 Technical Highlights

| Feature | Technology | Offline? |
|---------|-----------|----------|
| Disease Detection | ResNet50 / TF.js | ✅ Yes |
| Inventory Ledger | IndexedDB + SQLite | ✅ Yes |
| Mandi Prices | data.gov.in API + Cache | ✅ Yes (cached) |
| Weather Alerts | OpenWeatherMap + Thresholds | ✅ Yes (cached) |
| Quality Cert | ReportLab PDF + QR | ✅ Yes (preview) |
| Voice Commands | Web Speech API | ✅ Yes |
| UI Language | Hindi + English | ✅ Yes |

---

## 🏆 Why Mangifera Shield Wins

1. **Real Problem, Real Users**: Built for actual Malihabad farmers facing middlemen and crop disease
2. **Works Offline**: PWA + Service Worker + IndexedDB = orchard-ready
3. **Edge AI**: In-browser inference means zero latency, zero data cost
4. **Voice-First**: Low-literacy farmers navigate via Hinglish voice commands
5. **Data-Driven**: Integrates data.gov.in, OpenWeatherMap, and AGMARKNET
6. **Impact Metrics**: Could save farmers ₹900/quintal by bypassing middlemen

---

## 🤝 Team

Built with ❤️ for India's mango farmers at the Viveka 5.0 Hackathon at SRMU.

---

## 📄 License

MIT License — Use freely to help farmers everywhere.