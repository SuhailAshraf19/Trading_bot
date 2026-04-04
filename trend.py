import pandas_ta as ta

def analyze_market_trend(df):
    # 1. INDICATORS
    df['ema_200'] = ta.ema(df['close'], length=200)
    df['ema_50'] = ta.ema(df['close'], length=50)
    
    # ADX for Strength
    adx_df = ta.adx(df['high'], df['low'], df['close'], length=14)
    current_adx = adx_df['ADX_14'].iloc[-1]
    
    # Volume SMA to check if current volume is "High" or "Low"
    df['vol_sma'] = ta.sma(df['volume'], length=20)
    
    # Current Values
    price = df['close'].iloc[-1]
    ema_200 = df['ema_200'].iloc[-1]
    vol_now = df['volume'].iloc[-1]
    vol_avg = df['vol_sma'].iloc[-1]

    # 2. THE MULTI-STEP FILTER
    
    # A. TREND DIRECTION (Price vs EMA)
    is_bullish = price > ema_200
    is_bearish = price < ema_200
    
    # B. TREND STRENGTH (ADX)
    # 25+ is a strong trend, 20-25 is developing, < 20 is weak
    is_strong_adx = current_adx > 25 
    
    # C. VOLUME CONVICTION
    # Is current volume at least 10% higher than average?
    has_volume_support = vol_now > (vol_avg * 1.1)

    # 3. FINAL CLASSIFICATION
    if is_bullish and is_strong_adx and has_volume_support:
        return "STRONG_BULLISH"
    elif is_bullish:
        return "WEAK_BULLISH (Wait for Volume/ADX)"
    
    if is_bearish and is_strong_adx and has_volume_support:
        return "STRONG_BEARISH"
    elif is_bearish:
        return "WEAK_BEARISH (Wait for Volume/ADX)"

    return "SIDEWAYS"