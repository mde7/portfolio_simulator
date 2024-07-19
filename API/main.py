from fastapi import FastAPI
from contextlib import asynccontextmanager
from services.portfolio_service import PortfolioService
from routers import market_data, portfolio, notification
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.notification_service import NotificationService

notification_service = NotificationService()
portfolio_service = PortfolioService(notification_service)

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(portfolio_service.check_and_execute_limit_orders, 'interval', minutes=2)
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

app.include_router(market_data.router, prefix="/market_data")
app.include_router(portfolio.get_portfolio_router(portfolio_service), prefix="/portfolio")
app.include_router(notification.get_notification_router(notification_service), prefix="/notifications")
