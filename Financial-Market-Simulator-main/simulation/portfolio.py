import json
import os
from datetime import datetime

class Portfolio:
    def __init__(self, username, initial_balance=10000):
        """
        Initialize a portfolio for a user
        
        :param username: User's username
        :param initial_balance: Starting cash balance
        """
        self.username = username
        self.balance = initial_balance
        self.holdings = {}
        self.transaction_history = []
        
        # Create user profile directory if not exists
        os.makedirs('user_profiles', exist_ok=True)
        
        # Load existing profile if available
        self.profile_file = f'user_profiles/{username}_portfolio.json'
        self._load_profile()

    def _load_profile(self):
        """
        Load existing user portfolio from file
        """
        if os.path.exists(self.profile_file):
            with open(self.profile_file, 'r') as f:
                data = json.load(f)
                self.balance = data.get('balance', self.balance)
                self.holdings = data.get('holdings', {})
                self.transaction_history = data.get('transaction_history', [])

    def buy_stock(self, market, symbol, quantity):
        """
        Buy stocks for the portfolio
        
        :param market: Market instance
        :param symbol: Stock symbol
        :param quantity: Number of shares to buy
        """
        current_price = market.get_stock_price(symbol)
        total_cost = current_price * quantity
        
        # Check if enough balance
        if total_cost > self.balance:
            raise ValueError("Insufficient funds to complete purchase")
        
        # Update balance and holdings
        self.balance -= total_cost
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
        
        # Record transaction
        transaction = {
            'type': 'buy',
            'symbol': symbol,
            'quantity': quantity,
            'price': current_price,
            'timestamp': datetime.now().isoformat()
        }
        self.transaction_history.append(transaction)
        
        # Save profile
        self._save_profile()

    def sell_stock(self, market, symbol, quantity):
        """
        Sell stocks from the portfolio
        
        :param market: Market instance
        :param symbol: Stock symbol
        :param quantity: Number of shares to sell
        """
        # Check if enough shares
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            raise ValueError("Insufficient shares to sell")
        
        current_price = market.get_stock_price(symbol)
        total_revenue = current_price * quantity
        
        # Update balance and holdings
        self.balance += total_revenue
        self.holdings[symbol] -= quantity
        
        # Remove symbol if no shares left
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        
        # Record transaction
        transaction = {
            'type': 'sell',
            'symbol': symbol,
            'quantity': quantity,
            'price': current_price,
            'timestamp': datetime.now().isoformat()
        }
        self.transaction_history.append(transaction)
        
        # Save profile
        self._save_profile()

    def _save_profile(self):
        """
        Save portfolio state to file
        """
        profile_data = {
            'username': self.username,
            'balance': self.balance,
            'holdings': self.holdings,
            'transaction_history': self.transaction_history
        }
        
        with open(self.profile_file, 'w') as f:
            json.dump(profile_data, f, indent=4)

    def get_performance(self, market):
        """
        Calculate portfolio performance metrics
        
        :param market: Market instance
        :return: Performance dictionary
        """
        total_investment = 0
        current_value = 0
        
        for transaction in self.transaction_history:
            if transaction['type'] == 'buy':
                total_investment += transaction['price'] * transaction['quantity']
        
        current_value = self.get_portfolio_value(market)
        
        return {
            'total_investment': total_investment,
            'current_value': current_value,
            'profit_loss': current_value - total_investment,
            'return_percentage': ((current_value - total_investment) / total_investment) * 100 if total_investment > 0 else 0
        }

    def get_portfolio_value(self, market):
        """
        Calculate total portfolio value
        
        :param market: Market instance
        :return: Total portfolio value
        """
        total_value = self.balance
        
        for symbol, quantity in self.holdings.items():
            current_price = market.get_stock_price(symbol)
            total_value += current_price * quantity
        
        return total_value
