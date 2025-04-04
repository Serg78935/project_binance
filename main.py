
from core.backtester import Backtester
from strategies.sma_cross import SMACrossover  # або іншу стратегію
from core.data_loader import DataLoader
  

loader = DataLoader()
df = loader.load()
print(df.head())  # Переконайтесь, що дані є

"""
# Завантаження даних
import pandas as pd
file_path = "data/btc_1m_2025-02.parquet"
df = pd.read_parquet(file_path)
"""
# Запуск бектесту
strategy = SMACrossover(df)
backtester = Backtester(strategy)
results = backtester.run()

# Збереження результатів
results.to_csv("results/metrics.csv")
print("Backtest завершено, результати збережено у results/metrics.csv")

