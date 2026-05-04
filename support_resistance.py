import pandas as pd

def find_levels(data, window=5):
    """
    Detects multiple support and resistance levels
    """

    supports = []
    resistances = []

    for i in range(window, len(data) - window):

        low = data['low'].iloc[i]
        high = data['high'].iloc[i]

        # Support: local minimum
        if low == min(data['low'].iloc[i-window:i+window]):
            supports.append(low)

        # Resistance: local maximum
        if high == max(data['high'].iloc[i-window:i+window]):
            resistances.append(high)

    return supports, resistances


def get_sr_signal(data, threshold=0.003):
    """
    Returns:
        'near_support'
        'near_resistance'
        'breakout_up'
        'breakout_down'
        'middle'
    """

    supports, resistances = find_levels(data)

    latest_price = data['close'].iloc[-1]

    # Check proximity
    for s in supports:
        if abs(latest_price - s) / latest_price < threshold:
            return "near_support"

    for r in resistances:
        if abs(latest_price - r) / latest_price < threshold:
            return "near_resistance"

    # Breakouts
    if latest_price > max(resistances, default=latest_price):
        return "breakout_up"

    if latest_price < min(supports, default=latest_price):
        return "breakout_down"

    return "middle"