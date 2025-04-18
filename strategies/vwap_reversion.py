
# VWAP реверсія
import pandas as pd
from strategies.base import StrategyBase

class VWAPReversion(StrategyBase):
    def __init__(self, price_data: pd.DataFrame, dev_threshold: float = 0.01):
        super().__init__(price_data)
        self.dev_threshold = dev_threshold
        self.generate_signals()
    
    def generate_signals(self) -> pd.DataFrame:
        # Рахуємо VWAP як накопичене середнє по close (можна допрацювати, якщо потрібна справжня VWAP)
        #self.price_data['VWAP'] = self.price_data['close'].expanding().mean()
         # Правильний VWAP
        self.price_data['VWAP'] = (self.price_data['close'] * self.price_data['volume']).cumsum() / self.price_data['volume'].cumsum()

        # Формуємо сигнал: 1 — купити, -1 — продати, 0 — тримати
        self.price_data['Signal'] = 0
        self.price_data.loc[self.price_data['close'] < self.price_data['VWAP'] * (1 - self.dev_threshold), 'Signal'] = 1
        self.price_data.loc[self.price_data['close'] > self.price_data['VWAP'] * (1 + self.dev_threshold), 'Signal'] = -1

        # Визначаємо точки входу та виходу:
        self.price_data['Entry'] = (self.price_data['Signal'].shift(1) != 1) & (self.price_data['Signal'] == 1)
        self.price_data['Exit']  = (self.price_data['Signal'].shift(1) == 1) & (self.price_data['Signal'] != 1)

        # Зберігаємо серії
        self.entries_series = self.price_data['Entry']
        self.exits_series = self.price_data['Exit']

        # Друк результатів
        print("Total Entries:", self.entries_series.sum())
        print("Total Exits:", self.exits_series.sum())

    def run_backtest(self) -> pd.DataFrame:
        self.price_data['Returns'] = self.price_data['close'].pct_change()
        self.price_data['Strategy_Returns'] = self.price_data['Returns'] * self.price_data['Signal'].shift(1)
        self.backtest_results = self.price_data[['Strategy_Returns']]
        return self.backtest_results
    
    def get_metrics(self) -> dict:
        total_return = self.backtest_results['Strategy_Returns'].sum()
        win_rate = (self.backtest_results['Strategy_Returns'] > 0).mean()
        return {'Total Return': total_return, 'Win Rate': win_rate}
