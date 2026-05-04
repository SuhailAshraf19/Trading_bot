import pandas as pd

def get_volume_signal(data, lookback=20):
    """
    Returns:
        'strong_bullish'
        'strong_bearish'
        'weak_bullish'
        'weak_bearish'
        'volume_spike_reversal'
        'low_volume'
        'neutral'
    """

    # Rolling average volume
    data['avg_volume'] = data['volume'].rolling(window=lookback).mean()

    latest = data.iloc[-1]
    prev = data.iloc[-2]

    latest_volume = latest['volume']
    avg_volume = latest['avg_volume']

    # Price movement
    price_change = latest['close'] - prev['close']

    # 🚫 Low volume filter
    if latest_volume < avg_volume * 0.7:
        return "low_volume"

    # 🔥 Volume spike logic
    if latest_volume > avg_volume * 1.5:

        if price_change > 0:
            return "strong_bullish"

        elif price_change < 0:
            return "strong_bearish"

        else:
            return "volume_spike_reversal"

    # 📈 Normal high volume logic
    if latest_volume > avg_volume:

        if price_change > 0:
            return "weak_bullish"

        elif price_change < 0:
            return "weak_bearish"

    return "neutral"