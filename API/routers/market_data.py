from services.market_data_service import MarketDataService

from fastapi import APIRouter, HTTPException

router = APIRouter()
market_data_service = MarketDataService()

@router.get("/{ticker}")
async def get_portfolio(ticker: str):
    market_data = await market_data_service.get_market_data(ticker)
    if not market_data:
        raise HTTPException(status_code=404, detail=f"Market Data for instrument: {ticker} not found.")
    return market_data
