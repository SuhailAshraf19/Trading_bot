import ccxt

API_KEY = "OArZvxz6DYW8wSQ16omIiy5uT44gtqO8HH6gVIsDQWmJBmbUncTGGJSNKpHpxzPG"
API_SECRET = "ZxIdHafbXflIwUs34GeIAUjOmmhtCrr3KAOpGYxhFK6AgYmpEI6M0I4Tn8W7O5VG"


SYMBOL = "SHIB/USDT"
USDT_AMOUNT = 5   # spend 3 USDT


def test_buy():
    exchange = ccxt.binance({
        "apiKey": API_KEY,
        "secret": API_SECRET,
        "enableRateLimit": True,
    })

    try:
        # Get current price
        ticker = exchange.fetch_ticker(SYMBOL)
        price = ticker['last']

        print(f"Current Price: {price}")

        # Convert USDT to BTC amount
        amount = USDT_AMOUNT / price

        print(f"Buying amount: {amount}")

        # Place market buy
        order = exchange.create_market_sell_order(SYMBOL, amount)

        print("✅ BUY ORDER SUCCESS")
        print(order)

    except Exception as e:
        print("❌ ERROR:", e)


if __name__ == "__main__":
    test_buy()