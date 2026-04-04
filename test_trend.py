import ccxt
import pandas as pd
import pandas_ta as ta
# Import your actual function from trend.py
from trend import analyze_market_trend 

def run_test():
    print("🛰️ Connecting to Binance (Public)...")
    exchange = ccxt.binance()
    
    # 1. Fetch 300 candles (we need at least 200 for the EMA 200 to calculate)
    symbol = 'ETH/USDT'
    print(f"📥 Fetching latest 300 candles for {symbol}...")
    bars = exchange.fetch_ohlcv(symbol, timeframe='5m', limit=300)
    
    # 2. Prepare Data
    df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    
    # 3. Run Your Logic
    result = analyze_market_trend(df)
    
    # 4. Detailed Printout for Verification
    current_price = df['close'].iloc[-1]
    ema_200 = ta.ema(df['close'], length=200).iloc[-1]
    adx_df = ta.adx(df['high'], df['low'], df['close'], length=14)
    current_adx = adx_df['ADX_14'].iloc[-1]
    
    print("-" * 30)
    print(f"🔍 TEST RESULTS FOR {symbol}")
    print(f"Price: {current_price:.2f}")
    print(f"EMA 200: {ema_200:.2f}")
    print(f"ADX (Strength): {current_adx:.2f}")
    print("-" * 30)
    print(f"🤖 BOT SAYS THE TREND IS: **{result}**")
    print("-" * 30)

if __name__ == "__main__":
    run_test()