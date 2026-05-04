import ccxt
from config import API_KEY, API_SECRET, SYMBOL, TRADE_AMOUNT_USDT

def get_exchange():
    return ccxt.binance({
        "apiKey": API_KEY,
        "secret": API_SECRET,
        "enableRateLimit": True,
    })


def get_price(exchange):
    ticker = exchange.fetch_ticker(SYMBOL)
    return ticker['last']


def place_buy():
    exchange = get_exchange()

    try:
        price = get_price(exchange)
        amount = TRADE_AMOUNT_USDT / price

        order = exchange.create_market_buy_order(SYMBOL, amount)
        return order

    except Exception as e:
        return str(e)


def place_sell():
    exchange = get_exchange()

    try:
        balance = exchange.fetch_balance()
        base = SYMBOL.split('/')[0]

        amount = balance[base]['free']

        if amount <= 0:
            return "No asset to sell"

        order = exchange.create_market_sell_order(SYMBOL, amount)
        return order

    except Exception as e:
        return str(e)