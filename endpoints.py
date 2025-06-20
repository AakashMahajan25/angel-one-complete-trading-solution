ROOT_API_ENDPOINT = "https://apiconnect.angelone.in"

# User APIs
AUTHENTICATE = ROOT_API_ENDPOINT + "/rest/auth/angelbroking/user/v1/loginByPassword"
GENERATE_TOKEN = ROOT_API_ENDPOINT + "/rest/auth/angelbroking/jwt/v1/generateTokens"
GET_PROFILE = ROOT_API_ENDPOINT + "/rest/secure/angelbroking/user/v1/getProfile"

# Order APIs
PLACE_ORDER = ROOT_API_ENDPOINT + "/rest/secure/angelbroking/order/v1/placeOrder"
CANCEL_ORDER = ROOT_API_ENDPOINT + "/rest/secure/angelbroking/order/v1/cancelOrder"
GET_ORDER_BOOK = ROOT_API_ENDPOINT + "/rest/secure/angelbroking/order/v1/getOrderBook"
GET_TRADE_BOOK = ROOT_API_ENDPOINT + "/rest/secure/angelbroking/order/v1/getTradeBook"

# Data APIs
GET_MARKET_DATA = ROOT_API_ENDPOINT + "/rest/secure/angelbroking/market/v1/quote/"

# Top Gainer/Losers APIs
GET_GAINERS_LOSERS = ROOT_API_ENDPOINT + "/rest/secure/angelbroking/marketData/v1/gainersLosers"

# Historical API
GET_HISTORICAL_DATA = ROOT_API_ENDPOINT + "/rest/secure/angelbroking/historical/v1/getCandleData"

# All Instruments JSON
GET_ALL_INSTRUMENTS_JSON = "https://margincalculator.angelone.in/OpenAPI_File/files/OpenAPIScripMaster.json"
