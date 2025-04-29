
# Тестування стратегій
import pytest
import pandas as pd
from strategies.sma_cross import SMACrossover  
from strategies.rsi_bb import RSI_Bollinger
from strategies.vwap_reversion import VWAPReversion 

# Тестові дані
price_data = pd.DataFrame({
    'time': pd.date_range(start='2025-02-01', periods=10, freq='min'),
    'close': [100 + i for i in range(10)],
    'volume': [10] * 10
})

def test_sma_cross():
    strategy = SMACrossover(price_data=price_data)
    assert strategy is not None

def test_rsi_bb():
    strategy = RSI_Bollinger(price_data=price_data)
    assert strategy is not None

def test_vwap_reversion():
    strategy = VWAPReversion(price_data=price_data)
    assert strategy is not None

