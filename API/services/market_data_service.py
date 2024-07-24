import aiohttp
import asyncio

class MarketDataService:
    def __init__(self):
        self.base_url = 'https://www.alphavantage.co/query'
        self.api_key = ''

    async def get_market_data(self, ticker):
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': ticker,
            'apikey': self.api_key
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params) as response:
                data = await response.json()

        if 'Global Quote' not in data or not data['Global Quote']:
            return None
        
        price = data['Global Quote']['05. price']
        return {'instrument': ticker, 'price': price}
