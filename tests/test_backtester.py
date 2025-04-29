
# Тестування бектестера
import pytest
import pandas as pd
from core.backtester import Backtester  
from strategies.sma_cross import SMACrossover 

# Тестові дані
#dummy_data = pd.DataFrame({
 #   'time': pd.date_range(start='2025-02-01', periods=10, freq='min'),
 #   'close': [100 + i for i in range(10)]})
def test_backtester_runs():
    data = pd.DataFrame({
        'time': pd.date_range(start='2025-02-01', periods=10, freq='min'),
        'open': [100 + i for i in range(10)],
        'high': [101 + i for i in range(10)],
        'low': [99 + i for i in range(10)],
        'close': [100 + i for i in range(10)],
        'volume': [10] * 10
    })
    data['symbol'] = 'TEST'

    strategy_name = "sma_cross"
    strategy_func = SMACrossover
    strategy = SMACrossover(price_data=data)
    backtester = Backtester(data, strategy_func, strategy_name)
    results = backtester.run()
    assert 'equity_curve' in results, "Backtester should return results with equity_curve"

