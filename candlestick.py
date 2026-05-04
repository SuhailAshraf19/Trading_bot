def get_candle_type(candle):
    body = abs(candle['close'] - candle['open'])
    range_ = candle['high'] - candle['low']

    if range_ == 0:
        return "neutral"

    body_ratio = body / range_

    if body_ratio < 0.2:
        return "doji"
    elif candle['close'] > candle['open']:
        return "bullish"
    else:
        return "bearish"


def get_candlestick_signal(data, trend=None):
    """
    Returns:
        'bullish_reversal'
        'bearish_reversal'
        'bullish_continuation'
        'bearish_continuation'
        'indecision'
        'no_signal'
    """

    if len(data) < 3:
        return "no_signal"

    c1 = data.iloc[-3]
    c2 = data.iloc[-2]
    c3 = data.iloc[-1]

    type1 = get_candle_type(c1)
    type2 = get_candle_type(c2)
    type3 = get_candle_type(c3)

    # ========================
    # SINGLE CANDLE PATTERNS
    # ========================

    body = abs(c3['close'] - c3['open'])
    upper_wick = c3['high'] - max(c3['open'], c3['close'])
    lower_wick = min(c3['open'], c3['close']) - c3['low']

    # Hammer / Pin Bar (bullish reversal)
    if lower_wick > body * 2:
        if trend == "bearish":
            return "bullish_reversal"

    # Shooting Star / Pin Bar (bearish reversal)
    if upper_wick > body * 2:
        if trend == "bullish":
            return "bearish_reversal"

    # Doji
    if type3 == "doji":
        return "indecision"

    # Marubozu (strong momentum)
    if body > (c3['high'] - c3['low']) * 0.9:
        if c3['close'] > c3['open']:
            return "bullish_continuation"
        else:
            return "bearish_continuation"

    # ========================
    # DOUBLE CANDLE PATTERNS
    # ========================

    # Bullish Engulfing
    if type2 == "bearish" and type3 == "bullish":
        if c3['close'] > c2['open'] and c3['open'] < c2['close']:
            if trend == "bearish":
                return "bullish_reversal"

    # Bearish Engulfing
    if type2 == "bullish" and type3 == "bearish":
        if c3['open'] > c2['close'] and c3['close'] < c2['open']:
            if trend == "bullish":
                return "bearish_reversal"

    # Tweezer Top (bearish reversal)
    if abs(c2['high'] - c3['high']) / c3['high'] < 0.001:
        if trend == "bullish":
            return "bearish_reversal"

    # Tweezer Bottom (bullish reversal)
    if abs(c2['low'] - c3['low']) / c3['low'] < 0.001:
        if trend == "bearish":
            return "bullish_reversal"

    # Inside Bar (indecision / breakout setup)
    if c3['high'] < c2['high'] and c3['low'] > c2['low']:
        return "indecision"

    # ========================
    # TRIPLE CANDLE PATTERNS
    # ========================

    # Morning Star (bullish reversal)
    if type1 == "bearish" and type2 == "doji" and type3 == "bullish":
        if trend == "bearish":
            return "bullish_reversal"

    # Evening Star (bearish reversal)
    if type1 == "bullish" and type2 == "doji" and type3 == "bearish":
        if trend == "bullish":
            return "bearish_reversal"

    # Three White Soldiers (strong bullish)
    if type1 == type2 == type3 == "bullish":
        return "bullish_continuation"

    # Three Black Crows (strong bearish)
    if type1 == type2 == type3 == "bearish":
        return "bearish_continuation"

    return "no_signal"