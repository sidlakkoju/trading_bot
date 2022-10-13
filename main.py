from alpaca.trading.client import TradingClient
from config import API_KEY, SECRET_KEY


# https://alpaca.markets/docs/trading/getting-started/


trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)

# Getting account information and printing it
account = trading_client.get_account()
for property_name, value in account:
    print(f"\"{property_name}\": {value}")
