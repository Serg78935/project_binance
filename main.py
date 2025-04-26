
import time
from core.backtester import Backtester
from strategies.sma_cross import SMACrossover  
from strategies.rsi_bb import RSI_Bollinger
from strategies.vwap_reversion import VWAPReversion
from core.data_loader import DataLoader

# Завантаження даних
loader = DataLoader()
df = loader.load()

print(df.head())  # Переконайтесь, що дані є

# Стратегії
backtesters = [
    Backtester(df, SMACrossover, "sma_cross"),
   # Backtester(df, RSI_Bollinger, "rsi_bb"),
   # Backtester(df, VWAPReversion, "vwap_reversion")
]

print("Starting backtest...")
start_time = time.time()

for bt in backtesters:
    bt.run()

# Запуск бектесту
backtester = Backtester( df, SMACrossover, "sma_cross") 

backtester.compare_strategies_full([
    "results/metrics_sma_cross.csv",
    "results/metrics_rsi_bb.csv",
    "results/metrics_vwap_reversion.csv"
])


end_time = time.time()
#print(f"Backtest completed for ETHBTC in {end_time - start_time} seconds.")

print("Backtest завершено, результати збережено у results/metrics.csv")



