from pymongo import MongoClient
from datetime import datetime
import random

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['crypto_db']

# Create collections
cryptocurrencies = db['cryptocurrencies']
historical_prices = db['historical_prices']

# Insert sample cryptocurrencies
cryptocurrencies.insert_one({
    "symbol": "BTC",
    "name": "Bitcoin",
    "market_cap_rank": 1,
    "created_at": datetime.now()
})

cryptocurrencies.insert_one({
    "symbol": "ETH",
    "name": "Ethereum",
    "market_cap_rank": 2,
    "created_at": datetime.now()
})

# Get cryptocurrency IDs
btc_id = cryptocurrencies.find_one({"symbol": "BTC"})["_id"]
eth_id = cryptocurrencies.find_one({"symbol": "ETH"})["_id"]

# Insert dummy data
for i in range(30): 
    historical_prices.insert_one({
        "crypto_id": btc_id,
        "timestamp": datetime.now(),
        "price_usd": random.uniform(30000, 60000),
        "market_cap": random.randint(500000000000, 1000000000000),
        "24h_change": random.uniform(-5, 5),
        "volume_24h": random.randint(1000000000, 5000000000)
    })
    
    historical_prices.insert_one({
        "crypto_id": eth_id,
        "timestamp": datetime.now(),
        "price_usd": random.uniform(1000, 4000),
        "market_cap": random.randint(200000000000, 500000000000),
        "24h_change": random.uniform(-5, 5),
        "volume_24h": random.randint(500000000, 2000000000)
    })

print("Sample data inserted successfully.")
