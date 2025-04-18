
# Базовий клас стратегії
from abc import ABC, abstractmethod
import pandas as pd

class StrategyBase(ABC):
    def __init__(self, price_data: pd.DataFrame):
        self.price_data = price_data.copy()
        self.entries_series = None
        self.exits_series = None
        self.backtest_results = None

    @abstractmethod
    def generate_signals(self):
        """Генерація сигналів для стратегії"""
        pass

    def entries(self):
        """Сигнали для входу в позицію"""
        if self.entries_series is None:
            raise ValueError("Entries не згенеровані. Спочатку виклич generate_signals().")
        return self.entries_series

    def exits(self):
        """Сигнали для виходу з позиції"""
        if self.exits_series is None:
            raise ValueError("Exits не згенеровані. Спочатку виклич generate_signals().")
        return self.exits_series

    @abstractmethod
    def run_backtest(self) -> pd.DataFrame:
        """Локальний бектест стратегії"""
        pass

    @abstractmethod
    def get_metrics(self) -> dict:
        """Метрики ефективності стратегії"""
        pass
    
