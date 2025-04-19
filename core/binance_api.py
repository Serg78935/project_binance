
import requests
import time
import hmac
import hashlib
import urllib.parse
import json

class BinanceAPI:
    def __init__(self, config_path="config.json"):
        with open(config_path) as f:
            config = json.load(f)
            self.api_key = config["api_key"]
            self.api_secret = config["api_secret"]
        
        self.base_url = "https://api.binance.com"

    def _sign(self, params):
        query_string = urllib.parse.urlencode(params)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature

    def get_account_info(self):
        endpoint = "/api/v3/account"
        url = self.base_url + endpoint

        timestamp = int(time.time() * 1000)
        params = {
            "timestamp": timestamp
        }
        params["signature"] = self._sign(params)

        headers = {
            "X-MBX-APIKEY": self.api_key
        }

        response = requests.get(url, headers=headers, params=params)
        return response.json()

    def get_ticker_24hr(self):
        endpoint = "/api/v3/ticker/24hr"
        url = self.base_url + endpoint

        # timestamp і підпис
        timestamp = int(time.time() * 1000)
        params = {
            "timestamp": timestamp
        }
        params["signature"] = self._sign(params)

        headers = {
            "X-MBX-APIKEY": self.api_key
        }

        response = requests.get(url, headers=headers, params=params)
        return response.json()
