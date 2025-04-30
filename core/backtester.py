
import os
import pandas as pd
import numpy as np
import vectorbt as vbt
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from core.metrics import compute_metrics    

class Backtester:
    def __init__(self, data, strategy_func, strategy_name):
        self.data = data
        self.strategy_func = strategy_func
        self.strategy_name = strategy_name
        self.all_metrics = []
        self.heatmap_data = []

    def run(self):
        
        for symbol, df_symbol in self.data.groupby("symbol"):
        #for symbol in self.data['symbol'].unique():
            print(f"Running backtest for symbol {symbol}  for {self.strategy_name}...")

            df_symbol = self.data[self.data['symbol'] == symbol]
            # Ініціалізація стратегії
            strategy = self.strategy_func(df_symbol) 
            # Генеруємо сигнали
            entries = strategy.entries()
            exits = strategy.exits()

            pf = vbt.Portfolio.from_signals(
                close=df_symbol['close'],
                entries=entries,
                exits=exits,
                size=0.25,  # *100% від балансу на угоду ; Або 0.1 ;  Або 0.5  - агресивна версія                  
                fees=0.001,
                slippage=0.0005,   
                direction='both',
                freq='1min'
            )

            # Обчислення метрик
            metrics = compute_metrics(pf,symbol, self.strategy_name)
            self.all_metrics.append(metrics)

            self.heatmap_data.append({
                'symbol': symbol,
                'total_return': metrics['Total Return [%]'], 
                'sharpe_ratio': metrics['Sharpe Ratio'],
                'max_drawdown': metrics['Max Drawdown [%]'],
                'win_rate': metrics['Win Rate [%]'],         
                'expectancy': metrics['Expectancy']
            })

            self.plot_equity_curve(symbol,pf)

        self.performance_heatmap()
        self.save_results()
        return self.plot_equity_curve(symbol,pf)
    
    # Equity curve
    def plot_equity_curve(self,symbol,pf):    
        equity_curve_path = f"results/plots/{symbol}_{self.strategy_name}.html"
        os.makedirs(os.path.dirname(equity_curve_path), exist_ok=True)
        fig = pf.plot(title=f"{symbol} - {self.strategy_name}")
        #fig.write_image(equity_curve_path)
        fig.write_html(equity_curve_path)

    # Heatmap по performance
    def performance_heatmap(self):
        heatmap_df = pd.DataFrame(self.heatmap_data)
        if len(heatmap_df) < 100:
            print("Not enough data for 10x10 heatmap, skipping.")
            return  # або побудуйте меншу heatmap, якщо хочете
            
        heatmap_df_sorted = heatmap_df.sort_values(by="total_return", ascending=False)

        heatmap_df_sorted["tooltip"] = (
            "Symbol: " + heatmap_df_sorted["symbol"] +
            "<br>Total Return: " + heatmap_df_sorted["total_return"].round(2).astype(str) + "%" +
            "<br>Sharpe Ratio: " + heatmap_df_sorted["sharpe_ratio"].round(2).astype(str)
        )

        heatmap_fig = px.imshow(
            heatmap_df_sorted["total_return"].values.reshape(10, 10),
            labels=dict(color="Total Return [%]"),
            x=heatmap_df_sorted["symbol"].values.reshape(10, 10)[0],
            y=heatmap_df_sorted["symbol"].values.reshape(10, 10)[:, 0],
            text_auto=True,
            aspect="auto"
        )
        heatmap_fig.update_layout(title=f"Performance Heatmap - {self.strategy_name}")

        heatmap_path = f"results/plots/1performance_heatmap_{self.strategy_name}.html"
        os.makedirs(os.path.dirname(heatmap_path), exist_ok=True)
        heatmap_fig.write_html(heatmap_path)

    def save_results(self):

        metrics_df = pd.DataFrame(self.all_metrics)
        metrics_path = f"results/metrics_{self.strategy_name}.csv"
        os.makedirs(os.path.dirname(metrics_path), exist_ok=True)
        metrics_df.to_csv(metrics_path, index=False)

    def compare_strategies_full(self, strategy_files):

        # Зчитування всіх метрик
        all_metrics = []
        for file_path in strategy_files:
            strategy_df = pd.read_csv(file_path)
            strategy_name = os.path.basename(file_path).replace("metrics_", "").replace(".csv", "")
            strategy_df["strategy_name"] = strategy_name
            all_metrics.append(strategy_df)

        metrics_df = pd.concat(all_metrics, ignore_index=True)

        # Групування по стратегії
        grouped_metrics = metrics_df.groupby("strategy_name").agg({
            "Total Return [%]": "mean",
            "Sharpe Ratio": "mean",
            "Max Drawdown [%]": "mean",
            "Win Rate [%]": "mean"
        }).reset_index()

        # Побудова бар-графіка по всім метрикам
        fig = go.Figure()

        metrics = ["Total Return [%]", "Sharpe Ratio", "Max Drawdown [%]", "Win Rate [%]"]
        colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA']

        for i, metric in enumerate(metrics):
            fig.add_trace(go.Bar(
                x=grouped_metrics["strategy_name"],
                y=grouped_metrics[metric],
                name=metric,
                marker_color=colors[i]
            ))

        fig.update_layout(
            title="Порівняння стратегій за основними метриками",
            barmode='group',
            xaxis_title="Стратегія",
            yaxis_title="Значення",
            legend_title="Метрика",
            height=600
        )

        # Збереження графіка
        compare_path = "results/plots/1compare_strategies_full.html"
        os.makedirs(os.path.dirname(compare_path), exist_ok=True)
        fig.write_html(compare_path)

        print(f"Створено повний порівняльний звіт: {compare_path}")

