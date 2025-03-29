
# Тестування стратегій
import pytest
import pandas as pd
from strategies.sma_cross import SMACrossover  
from strategies.rsi_bb import RSI_Bollinger
from strategies.vwap_reversion import VWAPReversion  

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
