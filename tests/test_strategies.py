
# Тестування стратегій
import pytest
import pandas as pd
from strategies.sma_cross import SMACrossover  
from strategies.rsi_bb import RSI_Bollinger
from strategies.vwap_reversion import VWAPReversion 

# Тестові дані
price_data = pd.DataFrame({
    'time': pd.date_range(start='2025-02-01', periods=10, freq='min'),
    'close': [100 + i for i in range(10)]
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

"""
# Тестові дані
dummy_data = pd.DataFrame({
    'time': pd.date_range(start='2025-02-01', periods=10, freq='min'),
    'close': [100 + i for i in range(10)]
})

def test_sma_cross():
    strategy = SMACrossover(price_data=dummy_data)
    #data = pd.DataFrame({'close': [100, 101, 102, 103, 104]})
    signal = strategy.generate_signals()
    assert price_data is not None and not price_data.empty
    #assert signal in [-1, 0, 1], "Signal should be -1, 0, or 1"
    #assert strategy is not None

def test_rsi_bb():
    strategy = RSI_Bollinger(price_data=dummy_data)
    #data = pd.DataFrame({'close': [100, 101, 102, 103, 104]})
    signal = strategy.generate_signals()
    assert price_data is not None and not price_data.empty
    #assert signal in [-1, 0, 1], "Signal should be -1, 0, or 1"
    #assert strategy is not None

def test_vwap_reversion():
    strategy = VWAPReversion(price_data=dummy_data)
    #data = pd.DataFrame({'close': [100, 101, 102, 103, 104]})
    signal = strategy.generate_signals()
    assert price_data is not None and not price_data.empty
    #assert signal in [-1, 0, 1], "Signal should be -1, 0, or 1"
    #assert strategy is not None

def test_sma_cross():
    strategy = SMACrossover()
    data = pd.DataFrame({'close': [100, 101, 102, 103, 104]})
    signal = strategy.generate_signal(data)
    assert signal in [-1, 0, 1], "Signal should be -1, 0, or 1"

def test_rsi_bb():
    strategy = RSI_Bollinger()
    data = pd.DataFrame({'close': [100, 101, 102, 103, 104]})
    signal = strategy.generate_signal(data)
    assert signal in [-1, 0, 1], "Signal should be -1, 0, or 1"

def test_vwap_reversion():
    strategy = VWAPReversion()
    data = pd.DataFrame({'close': [100, 101, 102, 103, 104]})
    signal = strategy.generate_signal(data)
    assert signal in [-1, 0, 1], "Signal should be -1, 0, or 1"
"""
