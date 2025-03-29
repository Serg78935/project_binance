
# Тестування бектестера
import pytest
import pandas as pd
from core.backtester import Backtester  
from strategies.sma_cross import SMACrossover 

def test_backtester_runs():
    data = pd.DataFrame({
        'time': pd.date_range(start='2025-02-01', periods=10, freq='T'),
        'open': [100 + i for i in range(10)],
        'high': [101 + i for i in range(10)],
        'low': [99 + i for i in range(10)],
        'close': [100 + i for i in range(10)],
        'volume': [10] * 10
    })
    strategy = SMACrossover()
    backtester = Backtester(strategy, data)
    results = backtester.run()
    assert 'equity_curve' in results, "Backtester should return results with equity_curve"
