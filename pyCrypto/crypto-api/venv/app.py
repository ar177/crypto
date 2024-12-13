import os
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv

# Load env var from .env
load_dotenv()

# Flask app setup
app = Flask(__name__)

# Get base URL for CoinGecko-API from the env
COIN_GECKO_API_URL = os.getenv('COIN_GECKO_API_URL')

@app.route('/crypto-prices', methods=['GET'])
def get_crypto_prices():
    # Get coin symbols from the query parameter
    coins = request.args.get('coins')
    
    if not coins:
        return jsonify({"error": "Missing 'coins' parameter"}), 400

    coin_list = coins.split(',')
    coin_symbols = ','.join([coin.strip().lower() for coin in coin_list])
    
    # Prepare API request to fetch live prices
    url = f"{COIN_GECKO_API_URL}?ids={coin_symbols}&vs_currencies=usd&include_market_cap=true&include_24hr_change=true"
    response = requests.get(url)
    
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from CoinGecko"}), 500

    data = response.json()

    result = {}
    for coin in coin_list:
        coin = coin.strip().lower()
        if coin in data:
            result[coin] = {
                "price": data[coin].get('usd'),
                "market_cap": data[coin].get('usd_market_cap'),
                "24h_change": data[coin].get('usd_24h_change')
            }
        else:
            result[coin] = {"error": "Coin not found"}

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
# this is the api
# https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,litecoin&vs_currencies=usd&include_market_cap=true&include_24hr_change=true
# {"bitcoin":
#  {"usd":101615,
#   "usd_market_cap":2012555426397.491,
#   "usd_24h_change":0.9615945480150373},
#  "ethereum":
#  {"usd":3931.95,
#   "usd_market_cap":473764983736.9503,
#   "usd_24h_change":3.472108211746944},
#  "litecoin":
#  {"usd":121.57,
#   "usd_market_cap":9155241278.068254,
#   "usd_24h_change":3.7761919799642474}}