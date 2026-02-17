"""
Mangifera Shield — Weather Alert Service
OpenWeatherMap integration with Malihabad disease risk calculation.
Environmental thresholds for Powdery Mildew and Anthracnose.
"""

import os
import httpx
from datetime import datetime

# Malihabad coordinates (Lucknow district)
MALIHABAD_LAT = 26.9267
MALIHABAD_LON = 80.7178

# Disease risk thresholds based on agricultural research
DISEASE_THRESHOLDS = {
    "Powdery Mildew": {
        "temp_min": 11,
        "temp_max": 31,
        "humidity_min": 64,
        "humidity_max": 72,
        "season": "Feb-March (Flowering)",
        "risk_months": [1, 2, 3],
        "description_en": "Powdery Mildew thrives when temperature is 11°C–31°C and humidity is 64%–72%. Peak risk during Dasheri flowering season (Feb-March).",
        "description_hi": "छाछ्या रोग 11°C-31°C तापमान और 64%-72% नमी में पनपता है। दशहरी आम के बौर आने के मौसम (फरवरी-मार्च) में सबसे ज़्यादा खतरा।"
    },
    "Anthracnose": {
        "temp_min": 25,
        "temp_max": 35,
        "humidity_min": 80,
        "humidity_max": 100,
        "season": "Monsoon (July-September)",
        "risk_months": [6, 7, 8, 9],
        "description_en": "Anthracnose spreads rapidly in warm (25°C–35°C), humid (>80%) conditions. Peak during monsoon season.",
        "description_hi": "एन्थ्रेक्नोज गर्म (25°C-35°C) और नम (>80%) स्थितियों में तेजी से फैलता है। बरसात में सबसे ज़्यादा खतरा।"
    },
    "Die Back": {
        "temp_min": 30,
        "temp_max": 45,
        "humidity_min": 20,
        "humidity_max": 50,
        "season": "Summer (April-June)",
        "risk_months": [4, 5, 6],
        "description_en": "Die Back worsens in hot, dry summer conditions (30°C–45°C). Stress from heat makes trees vulnerable.",
        "description_hi": "डाई-बैक गर्मी में (30°C-45°C) बिगड़ता है। गर्मी के तनाव से पेड़ कमज़ोर होते हैं।"
    }
}

# Malihabad-specific factors
MALIHABAD_FACTORS = {
    "construction_dust": {
        "en": "⚠️ Lucknow Expressway construction dust can block leaf pores, weakening disease resistance. Regular water washing of leaves is recommended.",
        "hi": "⚠️ लखनऊ एक्सप्रेसवे निर्माण की धूल पत्तियों के छिद्रों को बंद कर सकती है, जिससे रोग प्रतिरोधक क्षमता कम होती है। पत्तियों को नियमित पानी से धोने की सलाह दी जाती है।"
    },
    "local_advisory": {
        "en": "Malihabad's dense mango orchards require extra vigilance for Powdery Mildew during the February flowering season.",
        "hi": "मलिहाबाद के घने आम के बागों में फरवरी में बौर आने के समय छाछ्या रोग के लिए अतिरिक्त सतर्कता ज़रूरी है।"
    }
}


def calculate_disease_risk(temp: float, humidity: float) -> list:
    """Calculate disease risk based on current weather conditions."""
    current_month = datetime.now().month
    risks = []

    # Spray advisories for each disease
    SPRAY_ADVISORIES = {
        "Powdery Mildew": {
            "spray_advisory_en": "Spray Sulfur (0.2%) or Karathane (0.1%) immediately",
            "spray_advisory_hi": "तुरंत सल्फर (0.2%) या कैराथेन (0.1%) का छिड़काव करें",
            "disease_hi": "छाछ्या/खर्रा"
        },
        "Anthracnose": {
            "spray_advisory_en": "Apply Carbendazim (0.1%) preventive spray",
            "spray_advisory_hi": "कार्बेन्डाजिम (0.1%) का रोकथाम छिड़काव करें",
            "disease_hi": "एन्थ्रेक्नोज"
        },
        "Die Back": {
            "spray_advisory_en": "Prune infected branches. Apply Bordeaux paste on cuts",
            "spray_advisory_hi": "संक्रमित शाखाएं काटें। कटे भाग पर बोर्डो पेस्ट लगाएं",
            "disease_hi": "शीर्ष मरण"
        }
    }

    for disease, thresholds in DISEASE_THRESHOLDS.items():
        # Check temperature range
        temp_in_range = thresholds["temp_min"] <= temp <= thresholds["temp_max"]
        # Check humidity range
        humidity_in_range = thresholds["humidity_min"] <= humidity <= thresholds["humidity_max"]
        # Check season
        in_season = current_month in thresholds["risk_months"]

        # Calculate risk level
        risk_score = 0
        if temp_in_range:
            risk_score += 35
        if humidity_in_range:
            risk_score += 35
        if in_season:
            risk_score += 30

        if risk_score > 0:
            if risk_score >= 70:
                risk_level = "CRITICAL"
            elif risk_score >= 50:
                risk_level = "HIGH"
            elif risk_score >= 30:
                risk_level = "MODERATE"
            else:
                risk_level = "LOW"

            advisory = SPRAY_ADVISORIES.get(disease, {})
            risks.append({
                "disease": disease,
                "disease_hi": advisory.get("disease_hi", disease),
                "risk_level": risk_level,
                "risk_score": risk_score,
                "temp_in_range": temp_in_range,
                "humidity_in_range": humidity_in_range,
                "in_season": in_season,
                "season": thresholds["season"],
                "description_en": thresholds["description_en"],
                "description_hi": thresholds["description_hi"],
                "spray_advisory_en": advisory.get("spray_advisory_en", "Monitor regularly. Consult local KVK if needed."),
                "spray_advisory_hi": advisory.get("spray_advisory_hi", "नियमित निगरानी करें। ज़रूरत पर स्थानीय KVK से सलाह लें।"),
                "threshold": {
                    "temp": f"{thresholds['temp_min']}°C – {thresholds['temp_max']}°C",
                    "humidity": f"{thresholds['humidity_min']}% – {thresholds['humidity_max']}%"
                }
            })

    # Sort by risk score descending
    risks.sort(key=lambda x: x["risk_score"], reverse=True)
    return risks


async def fetch_weather(api_key: str = None) -> dict:
    """Fetch current weather for Malihabad from OpenWeatherMap."""
    if not api_key:
        api_key = os.getenv("OPENWEATHER_API_KEY", "")

    if not api_key or api_key == "your_openweathermap_api_key_here":
        # Return demo data for Malihabad in February
        return get_demo_weather()

    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": MALIHABAD_LAT,
        "lon": MALIHABAD_LON,
        "appid": api_key,
        "units": "metric"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return {
                    "temp": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"],
                    "wind_speed": data.get("wind", {}).get("speed", 0),
                    "description": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"],
                    "location": "Malihabad, Lucknow",
                    "timestamp": datetime.now().isoformat(),
                    "source": "OpenWeatherMap"
                }
    except Exception:
        pass

    return get_demo_weather()


def get_demo_weather() -> dict:
    """Demo weather data for Malihabad in February (mango flowering season)."""
    return {
        "temp": 22.5,
        "feels_like": 21.8,
        "humidity": 68,
        "pressure": 1013,
        "wind_speed": 3.2,
        "description": "haze",
        "icon": "50d",
        "location": "Malihabad, Lucknow",
        "timestamp": datetime.now().isoformat(),
        "source": "Demo Data (February Avg)"
    }
