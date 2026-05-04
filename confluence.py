def get_trade_decision(
    trend,
    ma_signal,
    rsi_signal,
    volume_signal,
    sr_signal,
    breakout_signal,
    candle_signal,
    structure
):
    """
    Returns:
        'buy'
        'sell'
        'no_trade'
    """

    # ========================
    # 🔒 HARD FILTERS
    # ========================

    # 1. Sideways market
    if trend == "sideways" or structure == "sideways":
        return "no_trade"

    # 2. Fake breakout
    if "fake" in breakout_signal:
        return "no_trade"

    # 3. Indecision candle
    if candle_signal == "indecision":
        return "no_trade"

    # 4. Conflict filter (VERY IMPORTANT)
    if (trend in ["strong_bullish", "weak_bullish"] and structure == "downtrend") or \
       (trend in ["strong_bearish", "weak_bearish"] and structure == "uptrend"):
        return "no_trade"

    # 5. Overextended move (avoid chasing)
    if trend in ["strong_bullish", "weak_bullish"] and rsi_signal == "overbought":
        return "no_trade"

    if trend in ["strong_bearish", "weak_bearish"] and rsi_signal == "oversold":
        return "no_trade"

    # ========================
    # ⚖️ SCORING SYSTEM
    # ========================

    score = 0

    # TREND
    if trend == "strong_bullish":
        score += 3
    elif trend == "strong_bearish":
        score -= 3

    # MA
    if ma_signal in ["bullish_crossover", "bullish_continuation"]:
        score += 2
    elif ma_signal in ["bearish_crossover", "bearish_continuation"]:
        score -= 2

    # RSI
    if rsi_signal == "bullish":
        score += 1
    elif rsi_signal == "bearish":
        score -= 1

    # VOLUME (soft influence only)
    if volume_signal == "strong_bullish":
        score += 1
    elif volume_signal == "strong_bearish":
        score -= 1

    # SR
    if sr_signal == "near_support":
        score += 2
    elif sr_signal == "near_resistance":
        score -= 2

    # BREAKOUT
    if breakout_signal == "breakout_up":
        score += 3
    elif breakout_signal == "breakout_down":
        score -= 3

    # CANDLE
    if candle_signal == "bullish_reversal":
        score += 2
    elif candle_signal == "bearish_reversal":
        score -= 2
    elif candle_signal == "bullish_continuation":
        score += 1
    elif candle_signal == "bearish_continuation":
        score -= 1

    # STRUCTURE
    if structure == "uptrend":
        score += 2
    elif structure == "downtrend":
        score -= 2

    # ========================
    # 🧠 FINAL DECISION
    # ========================

    if score >= 6:
        return "buy"

    elif score <= -6:
        return "sell"

    else:
        return "no_trade"