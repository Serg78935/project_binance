
# Перетин ковзних середніх
import pandas as pd
from strategies.base import StrategyBase
class SMACrossover(StrategyBase):
    def __init__(self, price_data: pd.DataFrame, fast: int = 10, slow: int = 50):
        super().__init__(price_data)
        self.fast = fast
        self.slow = slow
    
    def generate_signals(self) -> pd.DataFrame:
        self.price_data['SMA_Fast'] = self.price_data['close'].rolling(window=self.fast).mean()
        self.price_data['SMA_Slow'] = self.price_data['close'].rolling(window=self.slow).mean()
        self.price_data['Signal'] = (self.price_data['SMA_Fast'] > self.price_data['SMA_Slow']).astype(int)
        self.signals = self.price_data[['Signal']]
        return self.signals
    
    def run_backtest(self) -> pd.DataFrame:
        self.price_data['Returns'] = self.price_data['close'].pct_change()
        self.price_data['Strategy_Returns'] = self.price_data['Returns'] * self.price_data['Signal'].shift(1)
        self.backtest_results = self.price_data[['Strategy_Returns']]
        return self.backtest_results
    
    def get_metrics(self) -> dict:
        total_return = self.backtest_results['Strategy_Returns'].sum()
        win_rate = (self.backtest_results['Strategy_Returns'] > 0).mean()
        return {'Total Return': total_return, 'Win Rate': win_rate}
    
