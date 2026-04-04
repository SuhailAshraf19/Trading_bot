import pandas_ta as ta

def get_comprehensive_candle_score(df):
    # 1. Detect ALL major TA-Lib patterns via pandas-ta
    # These return 100 for Bullish, -100 for Bearish, or 0
    patterns = df.ta.cdl_pattern(name="all")
    
    curr = patterns.iloc[-1]
    bull_score = 0.0
    bear_score = 0.0
    active_reasons = []

    # --- WEIGHTED SCORING SYSTEM ---
    # High Reliability Patterns (3-Candle) - Weight: 0.40
    high_rel = {
        'CDLMORNINGSTAR': 0.40, 'CDLEVENINGSTAR': 0.40, 
        'CDL3WHITESOLDIERS': 0.40, 'CDL3BLACKCROWS': 0.40,
        'CDLABANDONEDBABY': 0.45, 'CDL3INSIDE': 0.35, 'CDL3OUTSIDE': 0.35
    }
    
    # Medium Reliability (2-Candle) - Weight: 0.25
    med_rel = {
        'CDLENGULFING': 0.25, 'CDLHARAMI': 0.20, 
        'CDLPIERCING': 0.25, 'CDLDARKCLOUDCOVER': 0.25,
        'CDLKICKING': 0.30, 'CDLMATCHINGLOW': 0.20
    }
    
    # Single Candle / Contextual - Weight: 0.15
    low_rel = {
        'CDLHAMMER': 0.15, 'CDLINVERTEDHAMMER': 0.10, 
        'CDLSHOOTINGSTAR': 0.15, 'CDLHANGINGMAN': 0.15,
        'CDLDRAGONFLYDOJI': 0.10, 'CDLGRAVESTONEDOJI': 0.10,
        'CDLMARUBOZU': 0.15, 'CDLBELTHOLD': 0.10
    }

    # 2. TALLY THE VOTES
    all_weights = {**high_rel, **med_rel, **low_rel}
    
    for pattern, weight in all_weights.items():
        if pattern in curr and curr[pattern] != 0:
            if curr[pattern] > 0: # Bullish
                bull_score += weight
                active_reasons.append(f"Bullish {pattern[3:]} (+{weight})")
            else: # Bearish
                bear_score += weight
                active_reasons.append(f"Bearish {pattern[3:]} (-{weight})")

    # 3. NORMALIZE (Final Score between -1 and 1)
    final_score = max(-1.0, min(1.0, bull_score - bear_score))
    
    return final_score, active_reasons