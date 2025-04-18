
 # RSI + Bollinger Bands
import pandas as pd
import numpy as np
import ta
from strategies.base import StrategyBase

class RSI_Bollinger(StrategyBase):
    def __init__(self, price_data: pd.DataFrame, rsi_period: int = 14, bb_period: int = 20, 
                 rsi_lower: int = 40, rsi_upper: int = 70, max_holding_period: int = 200, stop_loss_pct: float = -0.03):
        super().__init__(price_data)
        self.rsi_period = rsi_period
        self.bb_period = bb_period
        self.rsi_lower = rsi_lower
        self.rsi_upper = rsi_upper
        self.max_holding_period = max_holding_period
        self.stop_loss_pct = stop_loss_pct
        self._prepare_indicators()
        self.generate_signals()

    def _prepare_indicators(self):
        # Правильний RSI
        self.price_data['RSI'] = ta.momentum.RSIIndicator(
            self.price_data['close'], window=self.rsi_period
        ).rsi()

        # Нижня межа Боллінджера
        self.price_data['BB_Lower'] = (
            self.price_data['close'].rolling(window=self.bb_period).mean() 
            - 2 * self.price_data['close'].rolling(window=self.bb_period).std()
        )
    def generate_signals(self) -> pd.DataFrame:
        entries = np.zeros(len(self.price_data), dtype=bool)
        exits = np.zeros(len(self.price_data), dtype=bool)

        in_position = False
        entry_price = 0.0
        holding_period = 0

        for i in range(1, len(self.price_data)):
            row = self.price_data.iloc[i]
            prev_row = self.price_data.iloc[i-1]

            # Вхід: RSI нижче порога та ціна в зоні 0-5% вище нижньої межі Боллінджера
            if not in_position:
                if (row['RSI'] < self.rsi_lower) and (0 < (row['close'] - row['BB_Lower']) / row['BB_Lower'] < 0.05):
                    entries[i] = True
                    in_position = True
                    entry_price = row['close']
                    holding_period = 0

            else:
                holding_period += 1

                # Вихід:
                exit_conditions = [
                    row['RSI'] > self.rsi_upper,                                         # RSI вище верхнього порогу
                    (row['close'] - entry_price) / entry_price <= self.stop_loss_pct,   # Стоп-лосс
                    holding_period >= self.max_holding_period                           # Максимальний час утримання
                ]

                if any(exit_conditions):
                    exits[i] = True
                    in_position = False

        # Закриваємо на останньому барі, якщо треба
        if in_position:
            exits[-1] = True

        self.entries_series = pd.Series(entries, index=self.price_data.index)
        self.exits_series = pd.Series(exits, index=self.price_data.index)

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


