
# Розрахунок метрик

import pandas as pd
import numpy as np

class Metrics:
    def __init__(self, results):
        self.results = results
        self.metrics = {}

    def calculate(self):
        returns = self.results['returns']
        equity_curve = self.results['equity_curve']
        trades = self.results['trades']

        self.metrics['total_return'] = equity_curve.iloc[-1] / equity_curve.iloc[0] - 1
        self.metrics['sharpe_ratio'] = self._sharpe_ratio(returns)
        self.metrics['max_drawdown'] = self._max_drawdown(equity_curve)
        self.metrics['winrate'] = self._winrate(trades)
        self.metrics['expectancy'] = self._expectancy(trades)
        self.metrics['exposure_time'] = self._exposure_time(trades)

    def save(self, filepath):
        df = pd.DataFrame([self.metrics])
        df.to_csv(filepath, index=False)

    def _sharpe_ratio(self, returns, risk_free_rate=0.0):
        return np.mean(returns - risk_free_rate) / np.std(returns) * np.sqrt(252)

    def _max_drawdown(self, equity_curve):
        peak = equity_curve.cummax()
        drawdown = (equity_curve - peak) / peak
        return drawdown.min()

    def _winrate(self, trades):
        return trades['profit'].gt(0).sum() / len(trades)

    def _expectancy(self, trades):
        return trades['profit'].mean()

    def _exposure_time(self, trades):
        return trades['duration'].sum() / (trades['exit_time'].max() - trades['entry_time'].min())
