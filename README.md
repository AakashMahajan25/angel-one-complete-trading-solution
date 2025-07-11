# Angel One Complete Trading Solution

A comprehensive Python wrapper for Angel One (Angel Broking) trading APIs that provides both REST API and WebSocket functionality for automated trading operations.

## 🚀 Features

### 📊 REST API Capabilities
- **User Management**: Authentication, profile retrieval, token generation
- **Order Management**: Place orders, get order book, trade book, cancel orders
- **Market Data**: Real-time quotes, historical data, market depth
- **Analytics**: Top gainers/losers, percentage changes, open interest data

### 🔴 Real-time WebSocket Streaming
- **Live Market Data**: LTP (Last Traded Price), Quote, Snap Quote, Depth data
- **Multiple Subscription Modes**: Support for different data granularities
- **Binary Data Parsing**: Efficient handling of Angel One's binary WebSocket protocol
- **Auto-reconnection**: Built-in connection management with heartbeat

### 🏗️ Architecture Features
- **Async/Await Support**: Full asynchronous implementation using `aiohttp`
- **Modular Design**: Clean separation of concerns with dedicated modules
- **Error Handling**: Comprehensive error management and logging
- **Type Safety**: Well-structured data models and response parsing

## 📋 Prerequisites

- Python 3.7 or higher
- Angel One Demat Account
- Angel One API credentials (API Key, Secret Key, Client ID)
- TOTP-enabled mobile app for MFA

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/AakashMahajan25/angel-one-complete-trading-solution.git
cd angel-one-complete-trading-solution
```

### 2. Create Virtual Environment (Optional)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the root directory with your Angel One credentials:

```env
# Angel One API Credentials
API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
CLIENT_ID=your_client_id_here
PASSWORD=your_password_here
MFA_TOKEN=your_totp_secret_key_here
```

#### How to Get Your Credentials:

1. **API Key & Secret Key**: 
   - Login to Angel One Dashboard
   - Go to API section and generate API credentials

2. **Client ID & Password**: 
   - Your Angel One login credentials

3. **MFA Token**: 
   - Your TOTP secret key from Angel One mobile app
   - This is used to generate time-based OTP for authentication

## 🚦 Quick Start

### Basic Usage Example

```python
import asyncio
from SmartAPI import AngelAPIWrapper
from SmartWebSockets import SmartWebSockets

async def main():
    # Initialize API wrapper
    api = AngelAPIWrapper()
    
    try:
        # Authenticate and get profile
        profile = await api.get_profile()
        print("Profile:", profile)
        
        # Get market data
        market_data = await api.get_market_data()
        print("Market Data:", market_data)
        
        # Get historical data
        historical = await api.get_historical_data()
        print("Historical Data:", historical)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

### WebSocket Real-time Data

```python
import asyncio
from SmartWebSockets import SmartWebSockets

async def websocket_example():
    ws = SmartWebSockets()
    
    try:
        # Connect to WebSocket
        await ws.connect()
        print("WebSocket connected!")
        
        # Keep connection alive and receive data
        while True:
            await asyncio.sleep(1)
            
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await ws.disconnect()

if __name__ == "__main__":
    asyncio.run(websocket_example())
```

## 📚 API Documentation

### SmartAPI Class Methods

#### User APIs
```python
api = AngelAPIWrapper()

# Authenticate user
await api.login()

# Get user profile
profile = await api.get_profile()
```

#### Order APIs
```python
# Place an order
order_response = await api.place_order()

# Get order book
orders = await api.get_order_book()
```

#### Market Data APIs
```python
# Get market data (OHLC/LTP/FULL)
market_data = await api.get_market_data()

# Get historical candle data
historical = await api.get_historical_data()

# Get top gainers/losers
gainers_losers = await api.get_gainers_losers()
```

### WebSocket Subscription Modes

| Mode | Value | Description |
|------|-------|-------------|
| LTP | 1 | Last Traded Price only |
| Quote | 2 | Basic quote data |
| Snap Quote | 3 | Detailed quote with best 5 buy/sell |
| Depth | 4 | Full market depth (20 levels) |

### Supported Exchanges

- **NSE**: National Stock Exchange
- **BSE**: Bombay Stock Exchange  
- **NFO**: NSE Futures & Options
- **BFO**: BSE Futures & Options
- **CDS**: Currency Derivatives
- **MCX**: Multi Commodity Exchange

## ⚙️ Configuration

### Order Payload Configuration

Customize order parameters in `config.py`:

```python
PLACE_ORDER_PAYLOAD = {
    "variety": "NORMAL",           # Order variety
    "tradingsymbol": "INFY",       # Trading symbol
    "symboltoken": "500209",       # Symbol token
    "transactiontype": "BUY",      # BUY/SELL
    "exchange": "NSE",             # Exchange
    "ordertype": "MARKET",         # MARKET/LIMIT/SL/SL-M
    "producttype": "INTRADAY",     # INTRADAY/DELIVERY/CARRYFORWARD
    "duration": "DAY",             # DAY/IOC
    "price": "0",                  # Price (0 for market orders)
    "quantity": "1"                # Quantity
}
```

### WebSocket Subscription Configuration

Configure symbols and modes in `config.py`:

```python
SUBSCRIBE_ACTION_PAYLOAD = {
    "correlationID": "unique_id",
    "action": 1,  # 1 for subscribe, 0 for unsubscribe
    "params": {
        "mode": 1,  # Subscription mode
        "tokenList": [
            {
                "exchangeType": 1,  # NSE
                "tokens": ["10626", "5290"]
            }
        ]
    }
}
```

## 🔧 Advanced Usage

### Custom Headers and Authentication

The system automatically handles:
- JWT token generation and refresh
- Required headers (IP addresses, MAC address, etc.)
- TOTP-based MFA authentication
- WebSocket authentication with feed tokens

### Error Handling Best Practices

```python
async def robust_trading_example():
    api = AngelAPIWrapper()
    
    try:
        # Always authenticate first
        await api.login()
        
        # Implement retry logic for critical operations
        max_retries = 3
        for attempt in range(max_retries):
            try:
                result = await api.place_order()
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                await asyncio.sleep(1)
                
    except Exception as e:
        print(f"Trading operation failed: {e}")
        # Implement your error notification system
```

## 📊 Data Structures

### Market Data Response
```json
{
    "subscription_mode": 1,
    "exchange_type": 1,
    "token": "99926000",
    "sequence_number": 1234567890,
    "exchange_timestamp": 1234567890,
    "last_traded_price": 125000,
    "last_traded_quantity": 100,
    "volume_trade_for_the_day": 1000000
}
```

### Order Response
```json
{
    "status": true,
    "message": "SUCCESS",
    "data": {
        "orderid": "220301000000001"
    }
}
```


## 🐛 Troubleshooting

### Common Issues

#### Authentication Errors
```bash
Error: Invalid credentials
Solution: Verify API_KEY, SECRET_KEY, CLIENT_ID, PASSWORD in .env file
```

#### TOTP Issues
```bash
Error: Invalid TOTP
Solution: Ensure MFA_TOKEN is correct and system time is synchronized
```

#### WebSocket Connection Issues
```bash
Error: WebSocket connection failed
Solution: Check network connectivity and API credentials
```

#### Module Import Errors
```bash
Error: No module named 'aiohttp'
Solution: Ensure virtual environment is activated and dependencies are installed
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This software is for educational and development purposes. Trading in financial markets involves substantial risk of loss. The authors and contributors are not responsible for any financial losses incurred through the use of this software. Always test thoroughly and understand the risks before using in live trading environments.

## 📞 Support

- Create an issue for bug reports
- Check Angel One API documentation for API-specific queries
- Ensure you have valid Angel One account and API access

## 🔗 Resources

- [Angel One API Documentation](https://smartapi.angelone.in/)
- [Angel One Developer Portal](https://smartapi.angelone.in/)
- [Python AsyncIO Documentation](https://docs.python.org/3/library/asyncio.html)

---

**Made with ❤️ for the trading community**