from SmartAPI import AngelAPIWrapper
from SmartWebSockets import SmartWebSockets
from config import CLIENT_ID, PASSWORD, TOTP
import asyncio




async def main():
    # Create an instance of the wrapper
    api = AngelAPIWrapper()
    
    try:
        # Call the get_profile method
        profile = await api.get_historical_data()
        print("Profile:", profile)
    except Exception as e:
        print(f"Error occurred: {e}")
    
    # api = SmartWebSockets()
    
    # try:
    #     result = await api.connect()
    #     print(result)
        
    #     while True:
    #         await asyncio.sleep(1)
            
    # except Exception as e:
    #     print("Something went wrong:", e)
    #     await api.disconnect()

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())