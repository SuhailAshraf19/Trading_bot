def get_market_structure(data, lookback=50):
    """
    Returns:
        'uptrend'
        'downtrend'
        'sideways'
    """

    if len(data) < lookback:
        return "sideways"

    # Use only recent candles
    recent = data.tail(lookback)

    highs = recent['high'].values
    lows = recent['low'].values

    hh = 0  # rising highs
    lh = 0  # falling highs
    hl = 0  # rising lows
    ll = 0  # falling lows

    # ========================
    # COUNT MOVES
    # ========================
    for i in range(1, len(highs)):

        # High structure
        if highs[i] > highs[i - 1]:
            hh += 1
        else:
            lh += 1

        # Low structure
        if lows[i] > lows[i - 1]:
            hl += 1
        else:
            ll += 1

    total = len(highs) - 1

    if total == 0:
        return "sideways"

    # ========================
    # STRENGTH CALCULATION
    # ========================
    bullish_strength = (hh + hl) / (2 * total)
    bearish_strength = (lh + ll) / (2 * total)

    # ========================
    # FINAL DECISION
    # ========================
    if bullish_strength > 0.6:
        return "uptrend"

    elif bearish_strength > 0.6:
        return "downtrend"

    else:
        return "sideways"