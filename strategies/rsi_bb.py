
 # RSI + Bollinger Bands
import pandas as pd
from strategies.base import StrategyBase

class RSI_Bollinger(StrategyBase):
    def __init__(self, price_data: pd.DataFrame, rsi_period: int = 14, bb_period: int = 20, rsi_lower: int = 30):
        super().__init__(price_data)
        self.rsi_period = rsi_period
        self.bb_period = bb_period
        self.rsi_lower = rsi_lower
    
    def generate_signals(self) -> pd.DataFrame:
        self.price_data['RSI'] = self.price_data['Close'].rolling(window=self.rsi_period).mean()
        self.price_data['BB_Lower'] = self.price_data['Close'].rolling(window=self.bb_period).mean() - 2 * self.price_data['Close'].rolling(window=self.bb_period).std()
        self.price_data['Signal'] = ((self.price_data['RSI'] < self.rsi_lower) & (self.price_data['Close'] > self.price_data['BB_Lower'])).astype(int)
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
