import time
import ccxt
import pandas as pd

from config import *
from logger import log
from excecuter import place_buy, place_sell

# Indicators
from trend import get_trend
from moving_averages import get_ma_signal
from rsi import get_rsi_signal
from volume import get_volume_signal
from support_resistance import get_sr_signal
from breakout import get_breakout_signal
from candlestick import get_candlestick_signal
from market_structure import get_market_structure
from confluence import get_trade_decision


# ========================
# 📡 FETCH DATA
# ========================
def get_data():
    exchange = ccxt.binance()

    bars = exchange.fetch_ohlcv(
        SYMBOL,
        timeframe=TIMEFRAME,
        limit=200
    )

    df = pd.DataFrame(bars, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume'
    ])

    df[['open','high','low','close','volume']] = df[
        ['open','high','low','close','volume']
    ].astype(float)

    return df


# ========================
# 🤖 MAIN BOT
# ========================
def run_bot():

    position = None
    entry_price = 0
    last_trade_time = 0

    log("🚀 Bot Started...")

    while True:
        try:
            data = get_data()
            current_price = data['close'].iloc[-1]

            # ========================
            # COOLDOWN
            # ========================
            if time.time() - last_trade_time < COOLDOWN:
                time.sleep(5)
                continue

            # ========================
            # INDICATORS
            # ========================
            trend = get_trend(data)
            ma_signal = get_ma_signal(data)
            rsi_signal = get_rsi_signal(data)
            volume_signal = get_volume_signal(data)
            sr_signal = get_sr_signal(data)
            structure = get_market_structure(data)

            candle_signal = get_candlestick_signal(data, trend)
            breakout_signal = get_breakout_signal(data, volume_signal)

            # ========================
            # DECISION
            # ========================
            decision = get_trade_decision(
                trend,
                ma_signal,
                rsi_signal,
                volume_signal,
                sr_signal,
                breakout_signal,
                candle_signal,
                structure
            )

            # ========================
            # LOG STATE
            # ========================
            log("-" * 50)
            log(f"Price: {current_price}")
            log(f"Trend: {trend} | Structure: {structure}")
            log(f"Decision: {decision}")
            log(f"Position: {position}")

            # ========================
            # RISK MANAGEMENT
            # ========================
            if position == "long":

                if current_price <= entry_price * (1 - STOP_LOSS_PCT):
                    log("🛑 STOP LOSS HIT")
                    log(place_sell())
                    position = None
                    last_trade_time = time.time()
                    continue

                elif current_price >= entry_price * (1 + TAKE_PROFIT_PCT):
                    log("🎯 TAKE PROFIT HIT")
                    log(place_sell())
                    position = None
                    last_trade_time = time.time()
                    continue

            # ========================
            # ENTRY / EXIT
            # ========================
            if decision == "buy" and position is None:
                log("🟢 BUY")
                result = place_buy()
                log(result)

                position = "long"
                entry_price = current_price
                last_trade_time = time.time()

            elif decision == "sell" and position == "long":
                log("🔴 SELL")
                result = place_sell()
                log(result)

                position = None
                last_trade_time = time.time()

            else:
                log("⚪ NO ACTION")

        except Exception as e:
            log(f"⚠️ ERROR: {e}")

        # ========================
        # LOOP WAIT
        # ========================
        time.sleep(LOOP_INTERVAL)


# ========================
# START
# ========================
if __name__ == "__main__":
    run_bot()