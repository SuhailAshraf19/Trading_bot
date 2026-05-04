import pandas as pd

def calculate_rsi(data, period=14):
    delta = data['close'].diff()

    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def get_rsi_signal(data):
    """
    Returns:
        'overbought'
        'oversold'
        'bullish'
        'bearish'
        'neutral'
    """

    data['rsi'] = calculate_rsi(data)

    latest = data.iloc[-1]
    rsi = latest['rsi']

    if rsi > 70:
        return "overbought"

    elif rsi < 30:
        return "oversold"

    elif rsi > 50:
        return "bullish"

    elif rsi < 50:
        return "bearish"

    else:
        return "neutral"