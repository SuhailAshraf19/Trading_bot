import os

# ========================
# 🔐 API (Railway ENV)
# ========================
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# ========================
# 📊 MARKET SETTINGS
# ========================
SYMBOL = "BTC/USDT"
TIMEFRAME = "5m"

# ========================
# 💰 TRADING SETTINGS
# ========================
TRADE_AMOUNT_USDT = 3.0   # ⚠️ Full balance (risky)
MIN_TRADE_USDT = 3.0      # Binance usually requires ~5 USDT minimum

# ========================
# ⏱️ BOT SETTINGS
# ========================
LOOP_INTERVAL = 300   # 5 minutes
COOLDOWN = 300        # avoid overtrading

# ========================
# 🧠 STRATEGY SETTINGS
# ========================
BUY_THRESHOLD = 7
SELL_THRESHOLD = -7

# ========================
# 🛑 RISK MANAGEMENT
# ========================
STOP_LOSS_PCT = 0.02     # 2% loss
TAKE_PROFIT_PCT = 0.03   # 3% profit

# ========================
# 🧪 MODES
# ========================
PAPER_TRADING = False
LOG_TO_FILE = True