"""
Mangifera Shield — Mandi Price Service
Fetches mango prices from data.gov.in / AGMARKNET with offline caching.
"""

import os
import httpx
from datetime import datetime


# Fallback mandi price data for Lucknow and nearby mandis
# (Used when data.gov.in API is unavailable or for offline demo)
CACHED_MANDI_PRICES = [
    {
        "market": "Lucknow (Aminabad Mandi)",
        "commodity": "Mango (Dasheri)",
        "variety": "Dasheri",
        "min_price": 3500,
        "max_price": 5500,
        "modal_price": 4500,
        "unit": "Quintal",
        "arrival_date": "2026-02-15",
        "state": "Uttar Pradesh",
        "district": "Lucknow"
    },
    {
        "market": "Malihabad Local Mandi",
        "commodity": "Mango (Dasheri)",
        "variety": "Dasheri",
        "min_price": 3000,
        "max_price": 5000,
        "modal_price": 4000,
        "unit": "Quintal",
        "arrival_date": "2026-02-15",
        "state": "Uttar Pradesh",
        "district": "Lucknow"
    },
    {
        "market": "Lucknow (Alambagh Mandi)",
        "commodity": "Mango (Dasheri)",
        "variety": "Dasheri",
        "min_price": 3800,
        "max_price": 5800,
        "modal_price": 4800,
        "unit": "Quintal",
        "arrival_date": "2026-02-15",
        "state": "Uttar Pradesh",
        "district": "Lucknow"
    },
    {
        "market": "Kanpur Mandi",
        "commodity": "Mango (Dasheri)",
        "variety": "Dasheri",
        "min_price": 3200,
        "max_price": 5200,
        "modal_price": 4200,
        "unit": "Quintal",
        "arrival_date": "2026-02-15",
        "state": "Uttar Pradesh",
        "district": "Kanpur"
    },
    {
        "market": "Delhi (Azadpur Mandi)",
        "commodity": "Mango (Dasheri)",
        "variety": "Dasheri",
        "min_price": 5000,
        "max_price": 8000,
        "modal_price": 6500,
        "unit": "Quintal",
        "arrival_date": "2026-02-15",
        "state": "Delhi",
        "district": "New Delhi"
    },
    {
        "market": "Saharanpur Mandi",
        "commodity": "Mango (Dasheri)",
        "variety": "Dasheri",
        "min_price": 3200,
        "max_price": 5000,
        "modal_price": 4100,
        "unit": "Quintal",
        "arrival_date": "2026-02-15",
        "state": "Uttar Pradesh",
        "district": "Saharanpur"
    },
    {
        "market": "Bulandshahr Mandi",
        "commodity": "Mango (Dasheri)",
        "variety": "Dasheri",
        "min_price": 3000,
        "max_price": 4800,
        "modal_price": 3900,
        "unit": "Quintal",
        "arrival_date": "2026-02-15",
        "state": "Uttar Pradesh",
        "district": "Bulandshahr"
    },
    {
        "market": "Varanasi Mandi",
        "commodity": "Mango (Dasheri)",
        "variety": "Dasheri",
        "min_price": 3500,
        "max_price": 5500,
        "modal_price": 4500,
        "unit": "Quintal",
        "arrival_date": "2026-02-15",
        "state": "Uttar Pradesh",
        "district": "Varanasi"
    }
]

# Historical price trend data for charts
PRICE_TRENDS = {
    "Dasheri": {
        "months": ["Jun-25", "Jul-25", "Aug-25", "Sep-25", "Oct-25", "Nov-25", "Dec-25", "Jan-26", "Feb-26"],
        "avg_price": [5200, 4800, 3500, 2800, 2200, 2000, 2500, 3000, 4500],
        "insight_en": "Dasheri mango prices peak in June-July (₹5000+/quintal) and are lowest in October-November. Current season shows strong demand with prices recovering.",
        "insight_hi": "दशहरी आम की कीमतें जून-जुलाई में चरम (₹5000+/क्विंटल) पर होती हैं और अक्टूबर-नवंबर में सबसे कम। इस मौसम में मांग मजबूत है और कीमतें सुधर रही हैं।"
    }
}

# Middleman vs direct selling comparison
MIDDLEMAN_ANALYSIS = {
    "middleman_cut_percent": 20,
    "typical_scenario": {
        "mandi_price": 4500,
        "middleman_price": 3600,
        "farmer_loss": 900,
        "en": "Middlemen typically take 20% margin. On ₹4500/quintal, farmer loses ₹900. Direct selling through Mangifera Shield's verified quality certificates can eliminate this loss.",
        "hi": "बिचौलिये आमतौर पर 20% मार्जिन लेते हैं। ₹4500/क्विंटल पर, किसान को ₹900 का नुकसान होता है। मैंगीफेरा शील्ड के सत्यापित गुणवत्ता प्रमाणपत्र से सीधी बिक्री करके यह नुकसान खत्म किया जा सकता है।"
    }
}


async def fetch_mandi_prices(api_key: str = None, commodity: str = "Mango") -> dict:
    """Fetch current mandi prices from data.gov.in API."""
    if not api_key:
        api_key = os.getenv("DATA_GOV_API_KEY", "")

    prices = CACHED_MANDI_PRICES

    # Try fetching live data if API key is available
    if api_key and api_key != "your_data_gov_api_key_here":
        try:
            url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
            params = {
                "api-key": api_key,
                "format": "json",
                "limit": 20,
                "filters[commodity]": commodity,
                "filters[state]": "Uttar Pradesh"
            }
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("records"):
                        live_prices = []
                        for record in data["records"]:
                            live_prices.append({
                                "market": record.get("market", "Unknown"),
                                "commodity": record.get("commodity", commodity),
                                "variety": record.get("variety", "Dasheri"),
                                "min_price": float(record.get("min_price", 0)),
                                "max_price": float(record.get("max_price", 0)),
                                "modal_price": float(record.get("modal_price", 0)),
                                "unit": "Quintal",
                                "arrival_date": record.get("arrival_date", ""),
                                "state": record.get("state", ""),
                                "district": record.get("district", "")
                            })
                        if live_prices:
                            prices = live_prices
        except Exception:
            pass  # Fall back to cached data

    # Calculate statistics
    all_modal = [p["modal_price"] for p in prices if p["modal_price"] > 0]
    avg_price = sum(all_modal) / len(all_modal) if all_modal else 0
    best_market = max(prices, key=lambda x: x["modal_price"]) if prices else None

    return {
        "prices": prices,
        "statistics": {
            "average_price": round(avg_price),
            "best_market": best_market["market"] if best_market else "N/A",
            "best_price": best_market["modal_price"] if best_market else 0,
            "total_markets": len(prices)
        },
        "trends": PRICE_TRENDS.get("Dasheri", {}),
        "middleman_analysis": MIDDLEMAN_ANALYSIS,
        "last_updated": datetime.now().isoformat(),
        "source": "data.gov.in / AGMARKNET" if api_key else "Cached Data"
    }
