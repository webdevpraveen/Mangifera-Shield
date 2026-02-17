"""
Mangifera Shield — Mandi Price Route
Fetch and serve Dasheri mango mandi prices.
"""

from fastapi import APIRouter
from ..services.mandi_service import fetch_mandi_prices

router = APIRouter(prefix="/api/mandi", tags=["Mandi Prices"])


@router.get("/prices")
async def get_mandi_prices(commodity: str = "Mango"):
    """Get current mandi prices for Dasheri mangoes across UP mandis."""
    data = await fetch_mandi_prices(commodity=commodity)
    return data


@router.get("/trends")
async def get_price_trends():
    """Get historical price trends for Dasheri mangoes."""
    data = await fetch_mandi_prices()
    return {
        "trends": data.get("trends", {}),
        "middleman_analysis": data.get("middleman_analysis", {})
    }
