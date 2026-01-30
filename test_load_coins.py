#!/usr/bin/env python3
# Test loading coins from Binance
import requests

try:
    url = "https://api.binance.com/api/v3/exchangeInfo"
    print("Fetching from Binance API...")
    response = requests.get(url, timeout=10)
    data = response.json()

    usdt_pairs = []
    for symbol_info in data['symbols']:
        if (symbol_info['symbol'].endswith('USDT') and
            symbol_info['status'] == 'TRADING' and
            symbol_info['quoteAsset'] == 'USDT'):

            base_asset = symbol_info['baseAsset']

            if any(x in base_asset for x in ['UP', 'DOWN', 'BULL', 'BEAR']):
                continue

            usdt_pairs.append(base_asset)

    print(f"Found {len(usdt_pairs)} coins")
    print("First 10:", usdt_pairs[:10])

except Exception as e:
    print(f"Error: {e}")
