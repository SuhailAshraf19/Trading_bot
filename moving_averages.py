import pandas as pd

def calculate_ema(data, period):
    return data['close'].ewm(span=period, adjust=False).mean()


def get_ma_signal(data):
    """
    Returns:
        'bullish_crossover'
        'bearish_crossover'
        'bullish_continuation'
        'bearish_continuation'
        'no_signal'
    """

    data['ema_9'] = calculate_ema(data, 9)
    data['ema_21'] = calculate_ema(data, 21)

    latest = data.iloc[-1]
    prev = data.iloc[-2]

    # Crossover detection
    if prev['ema_9'] < prev['ema_21'] and latest['ema_9'] > latest['ema_21']:
        return "bullish_crossover"

    if prev['ema_9'] > prev['ema_21'] and latest['ema_9'] < latest['ema_21']:
        return "bearish_crossover"

    # Continuation signals
    if latest['ema_9'] > latest['ema_21'] and latest['close'] > latest['ema_9']:
        return "bullish_continuation"

    if latest['ema_9'] < latest['ema_21'] and latest['close'] < latest['ema_9']:
        return "bearish_continuation"

    return "no_signal"