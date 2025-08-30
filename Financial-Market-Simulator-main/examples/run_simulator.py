import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simulation.market import Market
from simulation.portfolio import Portfolio
from simulation.leaderboard import Leaderboard

def run_simulation():
    api_key = "86ZCTA37OK0HBPSY"  # Replace with your Alpha Vantage API key
    symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]  # Stock symbols to simulate

    # Initialize market, user profile, and leaderboard
    market = Market(api_key, symbols)
    username = input("Enter your username: ")
    portfolio = Portfolio(username)
    leaderboard = Leaderboard()

    while True:
        print("\n--- Stock Market Simulation ---")
        print("1. View Stocks")
        print("2. Buy Stocks")
        print("3. Sell Stocks")
        print("4. View Portfolio")
        print("5. View Leaderboard")
        print("6. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                # Display current stock prices
                print("\nCurrent Stock Prices:")
                for symbol, stock in market.stocks.items():
                    print(f"{symbol}: ${stock['current_price']:.2f}")

            elif choice == "2":
                # Buy stocks
                symbol = input("Enter stock symbol to buy: ")
                quantity = int(input("Enter quantity: "))
                price = market.get_stock_price(symbol)
                portfolio.buy_stock(market, symbol, quantity)
                print(f"Bought {quantity} shares of {symbol} at ${price:.2f}")

            elif choice == "3":
                # Sell stocks
                symbol = input("Enter stock symbol to sell: ")
                quantity = int(input("Enter quantity: "))
                price = market.get_stock_price(symbol)
                portfolio.sell_stock(market, symbol, quantity)
                print(f"Sold {quantity} shares of {symbol} at ${price:.2f}")

            elif choice == "4":
                # View portfolio details
                print(portfolio)

            elif choice == "5":
                # Update and display the leaderboard
                total_balance = portfolio.balance + sum(
                    [market.get_stock_price(symbol) * quantity for symbol, quantity in portfolio.holdings.items()]
                )
                leaderboard.update_leaderboard(username, total_balance)
                leaderboard.display_leaderboard()

            elif choice == "6":
                print("Exiting simulation. Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")

            # Simulate small price movements after each action
            market.simulate_price_changes()

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_simulation()
