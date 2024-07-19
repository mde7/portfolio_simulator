from models.models import OrderModel
from services.portfolio_service import PortfolioService

from fastapi import APIRouter, HTTPException

router = APIRouter()

def get_portfolio_router(portfolio_service: PortfolioService):
    @router.post("/create_portfolio/{username}")
    async def create_portfolio(username: str):
        return await portfolio_service.create_portfolio(username)


    @router.get("/get_portfolio/{username}")
    async def get_portfolio(username: str):
        portfolio = await portfolio_service.get_portfolio(username)
        if not portfolio:
            raise HTTPException(status_code=404, detail="Portfolio not found")
        return portfolio


    @router.get("/place_order/")
    async def place_order(order: OrderModel):
        return await portfolio_service.place_order(order)
    
    return router