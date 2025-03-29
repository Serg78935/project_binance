
# VWAP реверсія
import pandas as pd
from strategies.base import StrategyBase

class VWAPReversion(StrategyBase):
    def __init__(self, price_data: pd.DataFrame, dev_threshold: float = 0.01):
        super().__init__(price_data)
        self.dev_threshold = dev_threshold
    
    def generate_signals(self) -> pd.DataFrame:
        self.price_data['VWAP'] = self.price_data['Close'].expanding().mean()
        self.price_data['Signal'] = ((self.price_data['Close'] < self.price_data['VWAP'] * (1 - self.dev_threshold)).astype(int) - 
                             (self.price_data['Close'] > self.price_data['VWAP'] * (1 + self.dev_threshold)).astype(int))
        self.signals = self.price_data[['Signal']]
        return self.signals
    
    def run_backtest(self) -> pd.DataFrame:
        self.price_data['Returns'] = self.price_data['Close'].pct_change()
        self.price_data['Strategy_Returns'] = self.price_data['Returns'] * self.price_data['Signal'].shift(1)
        self.backtest_results = self.price_data[['Strategy_Returns']]
        return self.backtest_results
    
    def get_metrics(self) -> dict:
        total_return = self.backtest_results['Strategy_Returns'].sum()
        win_rate = (self.backtest_results['Strategy_Returns'] > 0).mean()
        return {'Total Return': total_return, 'Win Rate': win_rate}
