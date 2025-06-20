import aiohttp
from config import get_headers, generate_token

class AngelClient:
    def __init__(self):
        self.headers = get_headers()
        self.token = generate_token()
        self.headers["Authorization"] = f"Bearer {self.token}"
        
    
    async def get(self, url, params=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers, params=params) as response:
                return await response.json()
    

    async def post(self, url, payload):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=payload) as response:
                return await response.json()