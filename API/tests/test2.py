import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from services.portfolio_service import PortfolioService
from services.notification_service import NotificationService

class DummyMarketDataService:
    def get_market_data(self, instrument):
        return {"price": 100}

async def trigger_notification():
    # Initialize the NotificationService
    notification_service = NotificationService()
    
    # Simulate WebSocket connection (Normally handled by FastAPI server)
    from fastapi import WebSocket

    class DummyWebSocket:
        async def accept(self):
            pass

        async def send_text(self, message: str):
            print(f"Sent message: {message}")

        async def receive_text(self):
            return "test message"

        async def close(self):
            pass

    websocket = DummyWebSocket()
    await notification_service.connect("testuser", websocket)
    
    # Initialize PortfolioService with the same NotificationService instance
    portfolio_service = PortfolioService(notification_service)
    portfolio_service.mds = DummyMarketDataService()  # Use a dummy market data service
    await portfolio_service.create_portfolio(
        'testuser'
    )
    # Connect to MongoDB
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client["portfolio_simulation"]

    # Ensure MongoDB is accessible
    try:
        # Check MongoDB connection
        await client.admin.command('ping')
        print("MongoDB is connected")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return

    # Simulate inserting a pending order into the database
    await db.limit_orders.insert_one({
        "instrument": "AAPL",
        "price": 100,
        "action": "buy",
        "username": "testuser",
        "shares": 10,
        "status": "pending"
    })

    # Manually trigger the check_and_execute_limit_orders method
    await portfolio_service.check_and_execute_limit_orders()

    # Disconnect the WebSocket (clean up)
    notification_service.disconnect("testuser")

if __name__ == "__main__":
    asyncio.run(trigger_notification())
