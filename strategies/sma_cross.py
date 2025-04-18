
# Перетин ковзних середніх
import pandas as pd
from strategies.base import StrategyBase  # якщо є базовий клас
class SMACrossover(StrategyBase):
    def __init__(self, price_data: pd.DataFrame, fast: int = 10, slow: int = 50):
        super().__init__(price_data)
        self.fast = fast
        self.slow = slow
        self._prepare_indicators()
        self.generate_signals()

    def _prepare_indicators(self):
        self.price_data['SMA_Fast'] = self.price_data['close'].rolling(window=self.fast).mean()
        self.price_data['SMA_Slow'] = self.price_data['close'].rolling(window=self.slow).mean()

    def generate_signals(self):
        self.price_data['Signal'] = (self.price_data['SMA_Fast'] > self.price_data['SMA_Slow']).astype(int)
        #self.entries_series = (self.price_data['SMA_Fast'] > self.price_data['SMA_Slow'])
        #self.exits_series = ~self.entries_series

        # Визначаємо точки входу та виходу:
        self.price_data['Entry'] = (self.price_data['Signal'].shift(1) != 1) & (self.price_data['Signal'] == 1)
        self.price_data['Exit']  = (self.price_data['Signal'].shift(1) == 1) & (self.price_data['Signal'] != 1)

        # Зберігаємо серії
        self.entries_series = self.price_data['Entry']
        self.exits_series = self.price_data['Exit']
        
         # Друк результатів
        print("Total Entries:", self.entries_series.sum())
        print("Total Exits:", self.exits_series.sum())
       

    def run_backtest(self):
        self.price_data['Returns'] = self.price_data['close'].pct_change()
        self.price_data['Strategy_Returns'] = self.price_data['Returns'] * self.entries_series.shift(1)
        self.backtest_results = self.price_data[['Strategy_Returns']]
        return self.backtest_results

    def get_metrics(self):
        total_return = self.backtest_results['Strategy_Returns'].sum()
        win_rate = (self.backtest_results['Strategy_Returns'] > 0).mean()
        return {'Total Return': total_return, 'Win Rate': win_rate}

    
