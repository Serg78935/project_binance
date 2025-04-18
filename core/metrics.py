
import pandas as pd

def compute_metrics(pf, symbol, strategy):
    #print(pf.trades.count())
    stats = pf.stats()

    return {
        "Total Return [%]": stats.get("Total Return [%]", None),
        "Sharpe Ratio": stats.get("Sharpe Ratio", None),
        "Max Drawdown [%]": stats.get("Max Drawdown [%]", None),
        "Win Rate [%]": stats.get("Win Rate [%]", None),
        "Expectancy": stats.get("Expectancy", None),
        "Max Gross Exposure [%]": stats.get("Max Gross Exposure [%]", None),
        "Symbol" : symbol,
        "Strategy" : strategy
    }

