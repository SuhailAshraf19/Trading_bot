import ccxt
import pandas as pd

from market_structure import get_market_structure


def get_data(symbol='BTC/USDT', timeframe='5m', limit=200):
    exchange = ccxt.binance()

    bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)

    df = pd.DataFrame(bars, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume'
    ])

    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)

    return df


def run_test():
    print("🧠 Testing Market Structure (DEBUG MODE)\n")

    data = get_data()

    structure = get_market_structure(data, lookback=50)

    # ========================
    # EXTRA ANALYSIS (DEBUG)
    # ========================
    recent = data.tail(50)

    highs = recent['high'].values
    lows = recent['low'].values

    hh = lh = hl = ll = 0

    for i in range(1, len(highs)):

        if highs[i] > highs[i - 1]:
            hh += 1
        else:
            lh += 1

        if lows[i] > lows[i - 1]:
            hl += 1
        else:
            ll += 1

    total = len(highs) - 1

    bullish_strength = (hh + hl) / (2 * total)
    bearish_strength = (lh + ll) / (2 * total)

    print("-" * 50)
    print(f"Bullish Strength: {bullish_strength:.2f}")
    print(f"Bearish Strength: {bearish_strength:.2f}")
    print("-" * 50)

    # ========================
    # HUMAN READABLE OUTPUT
    # ========================
    if bullish_strength > 0.65:
        print("📈 Market Bias: STRONG UPTREND")

    elif bullish_strength > bearish_strength:
        print("📈 Market Bias: WEAK UPTREND")

    elif bearish_strength > 0.65:
        print("📉 Market Bias: STRONG DOWNTREND")

    elif bearish_strength > bullish_strength:
        print("📉 Market Bias: WEAK DOWNTREND")

    else:
        print("⚖️ Market Bias: SIDEWAYS / UNCERTAIN")

    print("\n🧾 Raw Structure Output:", structure)
    print("-" * 50)


if __name__ == "__main__":
    run_test()