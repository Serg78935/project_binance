
import os
import requests
import pandas as pd
from pathlib import Path
import datetime  
from tqdm import tqdm 
#from binance.client import Client

#client = Client("YOUR_API_KEY", "YOUR_API_SECRET")
# Отримати всі пари BTC
#tickers = client.get_ticker_24hr()
#btc_pairs = [item for item in tickers if item['symbol'].endswith('BTC')]

class DataLoader:
    def __init__(self, data_dir='data', month='2025-02', top_n=100, config_path="config.json"): 
        self.data_dir = Path(data_dir)
        self.month = month
        self.top_n = top_n
        #self.api = BinanceAPI(config_path)
        self.filepath = self.data_dir / f'btc_1m_{month}.parquet'
        self.url_template = f"https://data.binance.vision/data/spot/monthly/klines/{{symbol}}/1m/{{symbol}}-1m-{self.month}.zip"

    def load(self):
        if self.filepath.exists():
            print("Using cached data.")
            return pd.read_parquet(self.filepath)

        self.data_dir.mkdir(parents=True, exist_ok=True)
        symbols = self._get_top_symbols()
        all_data = []
        failed_symbols = []

        print(f"Fetching data for {len(symbols)} symbols...")

        for symbol in tqdm(symbols, desc="Downloading symbols"):
            df = self._fetch_data(symbol)
            if df is not None:
                df['symbol'] = symbol
                all_data.append(df)
            else:
                failed_symbols.append(symbol)

        if all_data:
            final_df = pd.concat(all_data)
            final_df.to_parquet(self.filepath, compression='snappy')

            if failed_symbols:
                log_file = self.data_dir / f"failed_symbols_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(log_file, "w") as f:
                    f.write("\n".join(failed_symbols))
                print(f"\n⚠️ Failed to fetch data for {len(failed_symbols)} symbols. Logged to {log_file}")

            return final_df
        else:
            raise Exception("No data downloaded!")

    def _get_top_symbols(self):
        url = "https://api.binance.com/api/v3/ticker/24hr"
        response = requests.get(url)
        data = response.json()
        # Отримати всі пари BTC
        #data = client.get_ticker_24hr()
    
        if not isinstance(data, list):
            raise Exception(f"Неочікуваний формат відповіді: {data}")
    
        btc_pairs = [item for item in data if item['symbol'].endswith('BTC')]
        sorted_pairs = sorted(btc_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)
        return [pair['symbol'] for pair in sorted_pairs[:self.top_n]]
    
    def _fetch_data(self, symbol):
        url = self.url_template.format(symbol=symbol)
        zip_path = self.data_dir / f"{symbol}.zip"

        try:
            # Завантаження ZIP-файлу
            response = requests.get(url, stream=True)
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)

            # Зчитування CSV без розпаковки
            df = pd.read_csv(zip_path, compression='zip', header=None, sep=",",
                names=['timestamp', 'open', 'high', 'low', 'close', 'volume',
                        'close_time', 'quote_asset_volume', 'num_trades',
                        'taker_buy_base', 'taker_buy_quote', 'ignore'],
                dtype={"open": str, "high": str, "low": str, "close": str, "volume": str})

            # Очистка та конвертація
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = df[col].str.replace(r"[^\d.]", "", regex=True)
                df[col] = pd.to_numeric(df[col], errors="coerce")

            df = df.dropna(subset=['open', 'high', 'low', 'close', 'volume'])
            df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='us', errors='coerce')

            # Видаляємо zip після зчитування
            zip_path.unlink(missing_ok=True)

            return df
        except Exception as e:
            print(f"Failed to fetch {symbol}: {e}")
            return None
            
