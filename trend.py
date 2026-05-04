import pandas as pd

def calculate_ema(data, period):
    return data['close'].ewm(span=period, adjust=False).mean()


def get_trend(data):
    data['ema_20'] = calculate_ema(data, 20)
    data['ema_50'] = calculate_ema(data, 50)

    latest = data.iloc[-1]

    # Difference between EMAs
    ema_diff = abs(latest['ema_20'] - latest['ema_50'])

    # Threshold (tune this later)
    threshold = latest['close'] * 0.001  # 0.1%

    # SIDEWAYS CONDITION
    if ema_diff < threshold:
        return "sideways"

    # TREND CONDITIONS
    if latest['ema_20'] > latest['ema_50']:
        if latest['close'] > latest['ema_20']:
            return "strong_bullish"
        else:
            return "weak_bullish"
    else:
        if latest['close'] < latest['ema_20']:
            return "strong_bearish"
        else:
            return "weak_bearish"