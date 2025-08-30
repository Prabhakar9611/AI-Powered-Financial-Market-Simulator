import requests
import json
import os

class StockDataFetcher:
    def __init__(self, api_key, symbols):
        """
        Initialize the StockDataFetcher with API key and stock symbols.
        
        :param api_key: Alpha Vantage API key
        :param symbols: List of stock symbols to fetch
        """
        self.api_key = api_key
        self.symbols = symbols

    def fetch_stock_data(self):
        """
        Fetch real-time stock data for all symbols using the Alpha Vantage API.
        
        :return: Dictionary of stock symbols and their latest prices
        """
        base_url = "https://www.alphavantage.co/query"
        stock_data = {}

        for symbol in self.symbols:
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": self.api_key
            }
            response = requests.get(base_url, params=params)

            if response.status_code == 200:
                data = response.json()
                if "Global Quote" in data and "05. price" in data["Global Quote"]:
                    stock_data[symbol] = float(data["Global Quote"]["05. price"])
                else:
                    print(f"Warning: No data available for {symbol}")
            else:
                print(f"Error fetching data for {symbol}: {response.status_code}")

        return stock_data
