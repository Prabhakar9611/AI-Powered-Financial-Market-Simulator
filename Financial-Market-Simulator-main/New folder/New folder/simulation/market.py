import requests
import random

class Market:
    def __init__(self, api_key, symbols):
        self.api_key = api_key
        self.symbols = symbols
        self.stocks = self._load_stock_data()

    def _load_stock_data(self):
        stock_data = {}
        for symbol in self.symbols:
            stock_data[symbol] = {
                "symbol": symbol,
                "current_price": random.uniform(100, 1500),  # Initialize with random prices
                "volatility": random.uniform(0.01, 0.05)
            }
        return stock_data

    def simulate_stock_price(self, symbol):
        stock = self.stocks.get(symbol)
        if stock:
            change_percent = random.uniform(-stock["volatility"], stock["volatility"])
            stock["current_price"] *= (1 + change_percent)
            stock["current_price"] = round(stock["current_price"], 2)
            return stock["current_price"]
        raise ValueError("Stock not found.")

    def get_stock_price(self, symbol):
        stock = self.stocks.get(symbol)
        if stock:
            return stock["current_price"]
        raise ValueError("Stock not found.")
