from client import AngelClient
from config import LOGIN_PAYLOAD, PLACE_ORDER_PAYLOAD, MARKET_DATA_PAYLOAD, HISTORICAL_DATA_PAYLOAD, TOP_GAINERS_LOSERS_PAYLOAD
from endpoints import PLACE_ORDER, GET_ORDER_BOOK, GET_PROFILE, AUTHENTICATE, GET_MARKET_DATA, GET_GAINERS_LOSERS, GET_HISTORICAL_DATA

class AngelAPIWrapper:
    def __init__(self):
        self.client = AngelClient()

    # User APIs
    async def login(self):
            payload = LOGIN_PAYLOAD
            data = await self.client.post(AUTHENTICATE, payload)
            if data:
                print("Login successful")
            return data

    async def get_profile(self):
        return await self.client.get(GET_PROFILE)
    


    # Order APIs
    async def place_order(self):
        payload = PLACE_ORDER_PAYLOAD
        return await self.client.post(PLACE_ORDER, payload)
    
    async def get_order_book(self):
        payload = LOGIN_PAYLOAD
        return await self.client.post(GET_ORDER_BOOK, payload)
    


    # Market Data APIs
    async def get_market_data(self):
        payload = MARKET_DATA_PAYLOAD
        return await self.client.post(GET_MARKET_DATA, payload)
    
    # Historical Data APIs
    async def get_historical_data(self):
        payload = HISTORICAL_DATA_PAYLOAD
        return await self.client.post(GET_HISTORICAL_DATA, payload)
    

    # Get Gainers and Losers
    async def get_gainers_losers(self):
        payload = TOP_GAINERS_LOSERS_PAYLOAD
        return await self.client.post(GET_GAINERS_LOSERS, payload)
    

    
    