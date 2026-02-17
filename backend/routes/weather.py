"""
Mangifera Shield — Weather Alert Route
Disease risk alerts based on environmental conditions.
"""

from fastapi import APIRouter
from ..services.weather_service import fetch_weather, calculate_disease_risk, MALIHABAD_FACTORS

router = APIRouter(prefix="/api/weather", tags=["Weather Alerts"])


@router.get("/current")
async def get_current_weather():
    """Get current weather for Malihabad with disease risk assessment."""
    weather = await fetch_weather()
    risks = calculate_disease_risk(weather["temp"], weather["humidity"])

    return {
        "weather": weather,
        "disease_risks": risks,
        "local_factors": MALIHABAD_FACTORS,
        "overall_risk": risks[0]["risk_level"] if risks else "LOW"
    }


@router.get("/alerts")
async def get_disease_alerts():
    """Get disease risk alerts specifically for Dasheri mangoes."""
    weather = await fetch_weather()
    risks = calculate_disease_risk(weather["temp"], weather["humidity"])

    critical_alerts = [r for r in risks if r["risk_level"] in ("CRITICAL", "HIGH")]

    return {
        "alerts": critical_alerts,
        "total_alerts": len(critical_alerts),
        "current_conditions": {
            "temp": weather["temp"],
            "humidity": weather["humidity"],
            "location": weather["location"]
        },
        "advisory": MALIHABAD_FACTORS
    }
