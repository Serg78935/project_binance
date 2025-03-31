
# Backtesting Trading Strategies on Binance

## Project Overview
This project is designed to backtest various trading strategies using historical 1-minute OHLCV data for BTC pairs on Binance. It provides a modular architecture for loading data, executing backtests, calculating performance metrics, and visualizing results.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Serg78935/project_binance.git
   cd project_binance
   ```
2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running a Backtest
To execute a backtest with a specific strategy, run:
```bash
python main.py --strategy <strategy_name>
```
For example, to run the SMA Cross strategy:
```bash
python main.py --strategy sma_cross
```

Results, including performance metrics and equity curve plots, will be saved in the `results/` folder.

## Strategies Implemented

### 1. **SMA Cross** (Simple Moving Average Crossover)
   - Uses two SMAs (short and long period) to generate buy/sell signals.
   - Buy when the short SMA crosses above the long SMA.
   - Sell when the short SMA crosses below the long SMA.

### 2. **RSI & Bollinger Bands**
   - Combines RSI (Relative Strength Index) and Bollinger Bands for mean reversion trading.
   - Buy when RSI is oversold (<30) and price touches the lower Bollinger Band.
   - Sell when RSI is overbought (>70) and price touches the upper Bollinger Band.

### 3. **VWAP Reversion** (Volume Weighted Average Price)
   - Uses VWAP to detect mean reversion opportunities.
   - Buys when price deviates significantly below VWAP.
   - Sells when price deviates significantly above VWAP.

## Results & Conclusions
- **SMA Cross** works well in trending markets but underperforms in ranging conditions.
- **RSI & Bollinger Bands** provide strong mean reversion signals but require careful parameter tuning.
- **VWAP Reversion** is effective for intraday trading but depends on volume consistency.

The best strategy depends on market conditions and requires further optimization for live trading.

## Testing
To run unit tests:
```bash
pytest tests/
```

## Future Improvements
- Implement additional strategies (e.g., MACD, ATR-based stop losses).
- Integrate a paper trading module for live testing.
- Enhance visualization with more detailed performance analytics.

---

This project is actively maintained and open to contributions!


