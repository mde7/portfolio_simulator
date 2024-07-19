import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from services.portfolio_service import PortfolioService
from services.notification_service import NotificationService

async def trigger_notification():
    notification_service = NotificationService()
    
    # from fastapi import WebSocket

    # class DummyWebSocket:
    #     async def accept(self):
    #         pass

    #     async def send_text(self, message: str):
    #         print(f"Sent message: {message}")

    #     async def receive_text(self):
    #         return "test message"

    #     async def close(self):
    #         pass

    # websocket = DummyWebSocket()
    # await notification_service.connect("testuser", websocket)
    
    portfolio_service = PortfolioService(notification_service)
    res=await portfolio_service.create_portfolio('testuser')
    print(res)
    # client = AsyncIOMotorClient("mongodb://localhost:27017")
    # db = client["portfolio_simulation"]

    # try:
    #     await client.admin.command('ping')
    #     print("MongoDB is connected")
    # except Exception as e:
    #     print(f"Error connecting to MongoDB: {e}")
    #     return

    # await db.limit_orders.insert_one({
    #     "instrument": "AAPL",
    #     "price": 100,
    #     "action": "buy",
    #     "username": "testuser",
    #     "shares": 10,
    #     "status": "pending"
    # })

    # await portfolio_service.check_and_execute_limit_orders()

    # notification_service.disconnect("testuser")

if __name__ == "__main__":
    asyncio.run(trigger_notification())
