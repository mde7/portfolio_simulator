from models.models import LimitOrderModel, OrderModel
from motor.motor_asyncio import AsyncIOMotorClient
from services.market_data_service import MarketDataService

class PortfolioService:
    def __init__(self, notification_service):
        self.client = AsyncIOMotorClient("mongodb://localhost:27017")
        self.db = self.client["portfolio_simulation"]
        self.mds = MarketDataService()
        self.ns = notification_service

    async def create_portfolio(self, username):
        portfolio = {'user': username, 'stocks': []}
        exists = await self.db.portfolios.find_one({'user': username})

        if exists:
            return {'info': 'user portfolio already exists'}
        
        result = await self.db.portfolios.insert_one(portfolio)
        return {'status': result.inserted_id}
    
    async def get_portfolio(self, username):
        portfolio = await self.db.portfolios.find_one({'user': username})
        return portfolio

    async def place_order(self, order):     
        if order.type == "market":
            instrument = self.mds.get_market_data(order.instrument)
            await self.execute_order(order.username, order.instrument, order.position, order.action, instrument['price'])
            return {"status": "order executed", "execution_price": instrument['price']}
        else:
            limit_order = LimitOrderModel(**order.dict(), status='pending')
            result = await self.db.limit_orders.insert_one(limit_order.dict())
            return {'result': result.inserted_id, 'status': 'pending'}
    
    async def execute_order(self, username, instrument, position, action, price):
        portfolio = await self.db.portfolios.find_one({'user': username})

        if not portfolio:
            return {"error": "user portfolio not found"}
        
        if action == 'buy':
            for stock in portfolio['stocks']:
                if stock['instrument'] == instrument:
                    stock['cost_basis'] = (stock['cost_basis']*stock['position'] + price*position)/(stock['position'] + position)
                    stock['position'] += position
            else:
                portfolio['stocks'].append({
                    'instrument': instrument,
                    'cost_basis': price,
                    'position': position
                })
        elif action == 'sell':
            for stock in portfolio['stocks']:
                if stock['instrument'] == instrument:
                    if stock['position'] > position:
                        stock['position'] -= position
                        if stock['position'] == 0:
                            portfolio['stocks'].remove(stock)
                    else:
                        return {"error": "not enough positions to sell"}
        
        await self.db.portfolios.update_one({'user': username}, {'$set': portfolio})

    async def check_and_execute_limit_orders(self):
        pending_orders = await self.db.limit_orders.find({'status': 'pending'}).to_list(None)

        for order in pending_orders:
            instrument = order["instrument"]
            price = order["price"]
            action = order["action"]
            username = order["username"]
            position = order["shares"]

            current_data = self.mds.get_market_data(instrument)
            current_price = current_data['price']

            if (action=='buy' and price <= current_price) or (action=='sell' and price >= current_price):
                await self.execute_order(username, instrument, position, action, current_price)
                await self.db.limit_orders.delete_one({"_id": order["_id"]})

                message = f"{action.capitalize()} order for {position} shares of {instrument} at {current_price} has been executed."
                await self.ns.send_personal_message(message, username)