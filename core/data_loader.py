
import os
import hashlib
import requests
import pandas as pd
import pyarrow.parquet as pq
from concurrent.futures import ThreadPoolExecutor

data_dir = "data_cache"
os.makedirs(data_dir, exist_ok=True)

def download_binance_data(symbol: str, date: str) -> str:
    url = f"https://data.binance.vision/data/spot/monthly/klines/{symbol}/1m/{symbol}-1m-{date}.zip"
    local_path = os.path.join(data_dir, f"{symbol}-{date}.zip")

    if os.path.exists(local_path):
        return local_path  # Кешування: файл уже завантажено

    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(local_path, "wb") as f:
            f.write(response.content)
        return local_path
    elif response.status_code == 404:  # Якщо файл не існує
        print(f"⚠️  No data for {symbol} on {date}. Skipping.")
        return None
    else:
        raise Exception(f"Failed to download {symbol} data for {date} - HTTP {response.status_code}")


def extract_csv_from_zip(zip_path: str) -> pd.DataFrame:
    import zipfile
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        csv_file = zip_ref.namelist()[0]
        with zip_ref.open(csv_file) as f:
            return pd.read_csv(f, header=None)

def hash_file(file_path: str) -> str:
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        hasher.update(f.read())
    return hasher.hexdigest()

def load_data_for_symbol(symbol: str, dates: list) -> pd.DataFrame:
    df_list = []
    for date in dates:
        zip_path = download_binance_data(symbol, date)
        if zip_path:  # Пропускати, якщо файл відсутній
            df = extract_csv_from_zip(zip_path)
            df_list.append(df)
    
    return pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame()


def get_top_liquid_pairs() -> list:
    url = "https://api.binance.com/api/v3/ticker/24hr"
    response = requests.get(url)
    data = response.json()
    
    btc_pairs = [d for d in data if d['symbol'].endswith('BTC')]
    sorted_pairs = sorted(btc_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)
    return [d['symbol'] for d in sorted_pairs[:100]]

def save_parquet(df: pd.DataFrame, output_path: str):
    df.to_parquet(output_path, engine='pyarrow', compression='snappy')

def load_and_save_data():
    dates = [f"2025-02"]  # Формат без дня, оскільки Binance зберігає дані по місяцях
    top_pairs = get_top_liquid_pairs()
    
    all_data = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(lambda symbol: load_data_for_symbol(symbol, dates), top_pairs))
        all_data.extend(results)
    
    if all_data:  # Перевірка, чи список не порожній
        df = pd.concat(all_data, ignore_index=True)
        output_file = os.path.join(data_dir, "btc_1m_feb25.parquet")  
        save_parquet(df, output_file)
        print(f"✅ Data saved to {output_file} with SHA-256: {hash_file(output_file)}")
    else:
        print("⚠️ No data available for the selected period.")
