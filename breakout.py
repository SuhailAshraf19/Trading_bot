from support_resistance import find_levels

def get_breakout_signal(data, volume_signal, threshold=0.002):
    """
    Returns:
        'breakout_up'
        'breakout_down'
        'fake_breakout_up'
        'fake_breakout_down'
        'no_breakout'
    """

    supports, resistances = find_levels(data)

    latest = data.iloc[-1]
    prev = data.iloc[-2]

    price = latest['close']
    prev_price = prev['close']

    # Safety
    if not supports or not resistances:
        return "no_breakout"

    max_resistance = max(resistances)
    min_support = min(supports)

    # 🔥 BREAKOUT UP
    if price > max_resistance * (1 + threshold):

        if volume_signal in ["strong_bullish", "volume_spike"]:
            return "breakout_up"
        else:
            return "fake_breakout_up"

    # 🔻 BREAKOUT DOWN
    if price < min_support * (1 - threshold):

        if volume_signal in ["strong_bearish", "volume_spike"]:
            return "breakout_down"
        else:
            return "fake_breakout_down"

    return "no_breakout"