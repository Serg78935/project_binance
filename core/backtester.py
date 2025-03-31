
# Бектестинг стратегій
import os
#os.system("pip install vectorbt")
from strategies.base import StrategyBase
import pandas as pd
import vectorbt as vbt
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


class Backtester:
    def __init__(self, strategy: StrategyBase):
        self.strategy = strategy
        self.results = None
        self.metrics = None
    
    def run(self):
        self.strategy.generate_signals()
        self.strategy.run_backtest()
        price_data = self.strategy.price_data
        signals = self.strategy.signals
        returns = price_data['close'].pct_change()
        pf = vbt.IndicatorFactory.from_pandas_ta(signals).run()
        portfolio = vbt.IndicatorFactory.from_pandas_ta(returns * signals.shift(1)).run()

        self.metrics = {
            'Total Return': portfolio.total_return().values[0],
            'Sharpe Ratio': portfolio.sharpe_ratio().values[0],
            'Max Drawdown': portfolio.max_drawdown().values[0],
            'Win Rate': (portfolio.returns > 0).mean(),
            'Expectancy': portfolio.expectancy().values[0],
            'Exposure Time': portfolio.exposure().values[0]
        }
        self.results = portfolio
        
    def save_results(self, filename='backtest_results.csv', plot_filename='backtest_plot.png'):
        metrics_df = pd.DataFrame([self.metrics])
        metrics_df.to_csv(filename, index=False)
        
        plt.figure(figsize=(10, 5))
        self.strategy.price_data['Close'].plot(label='Price')
        plt.title('Backtest Performance')
        plt.legend()
        plt.savefig(plot_filename)
        plt.close()
    
    def plot_equity_curve(self):
        plt.figure(figsize=(12, 6))
        self.results['cumulative_returns'].plot(title='Equity Curve', label='Strategy')
        plt.legend()
        plt.show()
    
    def plot_performance_heatmap(self, pairs_returns: pd.DataFrame):
        plt.figure(figsize=(12, 8))
        sns.heatmap(pairs_returns, annot=False, cmap='coolwarm', center=0)
        plt.title('Performance Heatmap')
        plt.show()
    
    def compare_strategies(self, strategies_metrics: pd.DataFrame):
        fig = px.bar(strategies_metrics, x='Strategy', y=['Total Return', 'Sharpe Ratio', 'Max Drawdown', 'Win Rate'],
                     barmode='group', title='Comparison of Strategies')
        fig.show()
    
    def generate_html_report(self, filename='backtest_report.html'):
        fig = px.line(self.results, y='cumulative_returns', title='Equity Curve')
        fig.write_html(filename)

