
from core.backtester import Backtester
from strategies.sma_cross import SMACrossover  # або іншу стратегію
from core.data_loader import DataLoader

# Завантаження даних
data = DataLoader.load("data/btc_1m_2025-02.parquet")

# Запуск бектесту
strategy = SMACrossover()
backtester = Backtester(data, strategy)
results = backtester.run()

# Збереження результатів
results.to_csv("results/metrics.csv")
print("Backtest завершено, результати збережено у results/metrics.csv")
