from config import BUY_THRESHOLD, SELL_THRESHOLD
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
    score = 0
    reasons = []

    # ========================
    # TREND (IMPORTANT)
    # ========================
    if trend in ["strong_bullish", "weak_bullish"]:
        score += 2
        reasons.append("Trend bullish")
    elif trend in ["strong_bearish", "weak_bearish"]:
        score -= 2
        reasons.append("Trend bearish")
    else:
        reasons.append("Trend sideways → no strong direction")

    # ========================
    # MARKET STRUCTURE (FILTER)
    # ========================
    if structure == "sideways":
        reasons.append("Market structure sideways → avoid trade")
        return "no_trade", reasons

    elif structure == "uptrend":
        score += 2
        reasons.append("Market structure uptrend")
    elif structure == "downtrend":
        score -= 2
        reasons.append("Market structure downtrend")

    # ========================
    # MOVING AVERAGE
    # ========================
    if ma_signal == "bullish_crossover":
        score += 2
        reasons.append("MA bullish crossover")
    elif ma_signal == "bearish_crossover":
        score -= 2
        reasons.append("MA bearish crossover")

    # ========================
    # RSI
    # ========================
    if rsi_signal == "oversold":
        score += 1
        reasons.append("RSI oversold (buy signal)")
    elif rsi_signal == "overbought":
        score -= 1
        reasons.append("RSI overbought (sell signal)")

    # ========================
    # SUPPORT / RESISTANCE
    # ========================
    if sr_signal == "near_support":
        score += 2
        reasons.append("Near support")
    elif sr_signal == "near_resistance":
        score -= 2
        reasons.append("Near resistance")

    # ========================
    # BREAKOUT
    # ========================
    if breakout_signal == "bullish_breakout":
        score += 3
        reasons.append("Bullish breakout")
    elif breakout_signal == "bearish_breakout":
        score -= 3
        reasons.append("Bearish breakout")

    # ========================
    # CANDLESTICK
    # ========================
    if "bullish" in candle_signal:
        score += 2
        reasons.append(f"Bullish candle: {candle_signal}")
    elif "bearish" in candle_signal:
        score -= 2
        reasons.append(f"Bearish candle: {candle_signal}")
    else:
        reasons.append("No strong candlestick signal")

    # ========================
    # FINAL DECISION
    # ========================
    if score >= BUY_THRESHOLD:
        reasons.append(f"Score = {score} → BUY")
        return "buy", reasons

    elif score <= SELL_THRESHOLD:
        reasons.append(f"Score = {score} → SELL")
        return "sell", reasons

    else:
        reasons.append(f"Score = {score} → No trade")
        return "no_trade", reasons