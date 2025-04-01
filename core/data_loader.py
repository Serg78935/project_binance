
import os
import pandas as pd
import requests
from pathlib import Path

class DataLoader:
    def __init__(self, data_dir='data', month='2025-02', top_n=100):
        self.data_dir = Path(data_dir)
        self.month = month
        self.top_n = top_n
        self.filepath = self.data_dir / f'btc_1m_{month}.parquet'
        self.url_template = f"https://data.binance.vision/data/spot/monthly/klines/{{symbol}}/1m/{{symbol}}-1m-{self.month}.zip"

    def load(self):
        if Path(self.filepath).exists():
            print("Using cached data.")
            return pd.read_parquet(self.filepath)
        
        self.data_dir.mkdir(parents=True, exist_ok=True)
        symbols = self._get_top_symbols()
        all_data = []
        
        for symbol in symbols:
            df = self._fetch_data(symbol)
            if df is not None:
                df['symbol'] = symbol
                all_data.append(df)
        
        if all_data:
            final_df = pd.concat(all_data)
            final_df.to_parquet(self.filepath, compression='snappy')
            return final_df
        else:
            raise Exception("No data downloaded!")

    def _get_top_symbols(self):
        url = "https://api.binance.com/api/v3/ticker/24hr"
        response = requests.get(url)
        data = response.json()
        if isinstance(data, dict) and "msg" in data:
            raise RuntimeError(f"Binance API error: {data['msg']}")

        btc_pairs = [item for item in data if item['symbol'].endswith('BTC')]
        sorted_pairs = sorted(btc_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)
        return [pair['symbol'] for pair in sorted_pairs[:self.top_n]]
    

    def _fetch_data(self, symbol):
        url = self.url_template.format(symbol=symbol)
        zip_path = self.data_dir / f"{symbol}.zip"
        csv_path = self.data_dir / f"{symbol}.csv"

        try:
            response = requests.get(url, stream=True)
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
            
            pd.read_csv(zip_path, compression='zip').to_csv(csv_path, index=False)
            df = pd.read_csv(csv_path, header=None, sep=",",
                 names=['timestamp', 'open', 'high', 'low', 'close', 'volume', 
                        'close_time', 'quote_asset_volume', 'num_trades', 
                        'taker_buy_base', 'taker_buy_quote', 'ignore'],
                 dtype={"open": str, "high": str, "low": str, "close": str, "volume": str})
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = df[col].str.replace(r"[^\d.]", "", regex=True)  # Видаляємо непотрібні символи
                df[col] = pd.to_numeric(df[col], errors="coerce")  # Конвертуємо у float
            df = df.dropna(subset=['open', 'high', 'low', 'close', 'volume'])
            df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', errors='coerce')

            return df
        except Exception as e:
            print(f"Failed to fetch {symbol}: {e}")
            return None
"""
import pandas as pd

# Завантаження даних
file_path = "data/btc_1m_2025-02.parquet"
df = pd.read_parquet(file_path)

# Відображення перших рядків
print(df.head())

# Загальна інформація про датафрейм
print(df.info())
"""
