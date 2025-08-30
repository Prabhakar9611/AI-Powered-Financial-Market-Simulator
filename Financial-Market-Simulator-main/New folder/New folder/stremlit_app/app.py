import sys
import os
import streamlit as st

# Add the project root directory to sys.path so Python can find the 'simulation' package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simulation.market import Market
from simulation.portfolio import Portfolio
from simulation.leaderboard import Leaderboard

# Stock Advice Functions
def generate_stock_advice(symbol, current_price, high_price, low_price):
    """
    Generate contextual stock advice based on current market conditions
    """
    advice_list = []
    
    # Price position relative to high and low
    price_range = high_price - low_price
    position_in_range = (current_price - low_price) / price_range if price_range > 0 else 0.5
    
    # General Stock Knowledge Advice
    company_insights = {
        "AAPL": [
            "Apple continues to be a tech leader with strong innovation.",
            "Consider Apple's ecosystem and services growth potential.",
            "Watch for new product announcements and tech innovations."
        ],
        "GOOGL": [
            "Alphabet's diverse business model provides multiple revenue streams.",
            "Google's AI and cloud computing sectors show significant promise.",
            "Monitor regulatory environment and potential tech sector changes."
        ],
        "MSFT": [
            "Microsoft's cloud services and AI integration remain strong.",
            "Enterprise solutions continue to be a key growth area.",
            "Windows and Office ecosystem provide stable revenue."
        ],
        "TSLA": [
            "Tesla's innovation in electric vehicles and renewable energy is notable.",
            "Watch for new technological breakthroughs and expansion plans.",
            "Global EV market trends can significantly impact Tesla's performance."
        ],
        "AMZN": [
            "Amazon's e-commerce and cloud computing remain robust.",
            "AWS continues to be a significant revenue generator.",
            "Watch for potential expansion in new market segments."
        ]
    }
    
    # Price position advice
    if position_in_range < 0.3:
        # Near low price
        low_price_advices = [
            f"🟢 {symbol} is trading near its daily low. Potential buying opportunity!",
            f"💡 Current price is attractive for long-term investors.",
            "Consider averaging down if you believe in the stock's fundamentals."
        ]
        advice_list.extend(low_price_advices)
    
    elif position_in_range > 0.7:
        # Near high price
        high_price_advices = [
            f"⚠️ {symbol} is trading near its daily high. Be cautious of potential pullback.",
            "Consider taking partial profits if you're holding the stock.",
            "Watch for potential market correction or consolidation."
        ]
        advice_list.extend(high_price_advices)
    
    else:
        # Mid-range
        mid_range_advices = [
            f"📊 {symbol} is trading in its mid-range. Balanced investment opportunity.",
            "Consider your risk tolerance and investment strategy.",
            "Look for additional fundamental analysis before making decisions."
        ]
        advice_list.extend(mid_range_advices)
    
    # Company specific insights
    if symbol in company_insights:
        advice_list.append(company_insights[symbol][0])
    
    # Risk management advice
    risk_advices = [
        "Always diversify your investment portfolio.",
        "Never invest more than you can afford to lose.",
        "Consider your long-term financial goals.",
        "Regularly review and rebalance your investments."
    ]
    advice_list.append(risk_advices[hash(symbol) % len(risk_advices)])
    
    return advice_list

def display_stock_advice(symbol, current_price, high_price, low_price):
    """
    Display stock-specific advice in a Streamlit app
    """
    advice_list = generate_stock_advice(symbol, current_price, high_price, low_price)
    
    st.subheader("🌟 Investment Insights")
    for i, advice in enumerate(advice_list, 1):
        st.markdown(f"{i}. {advice}")

# Custom CSS for attractive UI
def set_custom_styles():
    st.markdown("""
    <style>
    /* Background Image */
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1611974789259-0cc33ff0b897?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    /* Card-like containers */
    .card {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Main Application Class
class StockMarketSimulator:
    def __init__(self):
        # Streamlit configuration
        st.set_page_config(page_title="Stock Market Simulator", page_icon="📊", layout="wide")
        
        # Initialize global variables
        self.API_KEY = "YQ36BTAFBGZ4XEN5"  # Replace with your API key
        self.symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
        
        self.market = Market(self.API_KEY, self.symbols)
        self.leaderboard = Leaderboard()
        
        # Apply custom styles
        set_custom_styles()
        
        # Initialize session state
        self.initialize_session_state()
    
    def initialize_session_state(self):
        # Initialize session state if not exists
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'Home'
        
        # Initialize stock price history
        if "stock_price_history" not in st.session_state:
            try:
                # Simulate price history for all stocks
                st.session_state["stock_price_history"] = {
                    symbol: [self.market.simulate_stock_price(symbol) for _ in range(24)] for symbol in self.symbols
                }
            except Exception as e:
                st.session_state["stock_price_history"] = {}
                st.error(f"Failed to initialize stock price history: {e}")
        
        # Initialize stock highs and lows
        if "stock_highs_lows" not in st.session_state:
            try:
                st.session_state["stock_highs_lows"] = {
                    symbol: {
                        "highest": max(prices),
                        "lowest": min(prices),
                        "current": prices[-1],
                    }
                    for symbol, prices in st.session_state["stock_price_history"].items()
                }
            except Exception as e:
                st.session_state["stock_highs_lows"] = {}
                st.error(f"Failed to initialize stock highs and lows: {e}")
    
    def render_navigation(self):
        """Render navigation with Streamlit buttons"""
        nav_cols = st.columns(4)
        
        pages = [
            ('Home 🏠', 'Home'),
            ('Trade 💱', 'Trade'),
            ('Portfolio 📂', 'Portfolio'),
            ('Leaderboard 🏆', 'Leaderboard')
        ]
        
        for col, (label, page) in zip(nav_cols, pages):
            with col:
                if st.button(label):
                    st.session_state.current_page = page
    
    def render_home_page(self):
        """Render the Home page"""
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.title("Stock Market Overview 📈")
        st.subheader("Today's Stock Data and Graphs")

        # Display stock data in a grid layout (2 companies per row)
        columns = st.columns(2)
        for i, symbol in enumerate(self.symbols):
            col = columns[i % 2]
            with col:
                if symbol in st.session_state["stock_highs_lows"]:
                    stock_data = st.session_state["stock_highs_lows"][symbol]
                    st.write(f"### {symbol}")
                    st.write(f"**Current Price:** ${stock_data['current']:.2f}")
                    st.write(f"**High:** ${stock_data['highest']:.2f}")
                    st.write(f"**Low:** ${stock_data['lowest']:.2f}")

                    # Graph of today's price movements
                    prices = st.session_state["stock_price_history"][symbol]
                    st.line_chart(prices)
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_trade_page(self):
        """Render the Trade page"""
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.title("Trade Stocks 💱")
        username = st.text_input("Enter your username:")
        
        if username:
            portfolio = Portfolio(username)
            stock_symbol = st.selectbox("Select Stock", self.symbols)
            current_price = self.market.get_stock_price(stock_symbol)
            stock_highs_lows = st.session_state["stock_highs_lows"].get(stock_symbol, {})
            lowest_price_today = stock_highs_lows.get("lowest")

            # Show selected stock information
            st.subheader(f"Details for {stock_symbol}")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Current Price:** ${current_price:.2f}")
                st.write(f"**High Today:** ${stock_highs_lows.get('highest', 'N/A'):.2f}")
                st.write(f"**Low Today:** ${stock_highs_lows.get('lowest', 'N/A'):.2f}")
            with col2:
                st.line_chart(st.session_state["stock_price_history"][stock_symbol])

            # List user's holdings in the selected stock
            st.write(f"**Your Holdings in {stock_symbol}:** {portfolio.holdings.get(stock_symbol, 0)} shares")

            # Display Stock Advice
            display_stock_advice(stock_symbol, current_price, 
                                 stock_highs_lows.get('highest', current_price), 
                                 stock_highs_lows.get('lowest', current_price))

            # Buy/Sell Actions
            quantity = st.number_input("Enter Quantity", min_value=1, step=1)

            col3, col4 = st.columns(2)
            with col3:
                if st.button("Buy"):
                    try:
                        portfolio.buy_stock(self.market, stock_symbol, quantity)
                        st.success(f"Bought {quantity} shares of {stock_symbol} at ${current_price:.2f}")
                        if current_price == lowest_price_today:
                            st.success("🎉 Best Buy Bhai! You bought at the lowest price today!")
                            self.leaderboard.update_leaderboard(username, portfolio.balance)
                    except Exception as e:
                        st.error(f"Error: {e}")

            with col4:
                if st.button("Sell"):
                    try:
                        portfolio.sell_stock(self.market, stock_symbol, quantity)
                        st.success(f"Sold {quantity} shares of {stock_symbol} at ${current_price:.2f}")
                        if (
                            st.session_state["stock_price_history"][stock_symbol][-1]
                            > st.session_state["stock_price_history"][stock_symbol][-2]
                        ):
                            st.success("🌟 Great Sell! You're awarded as a Good Seller!")
                            self.leaderboard.update_leaderboard(username, portfolio.balance)
                    except Exception as e:
                        st.error(f"Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_portfolio_page(self):
        """Render the Portfolio page"""
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.title("Your Portfolio 📂")
        username = st.text_input("Enter your username:")
        
        if username:
            portfolio = Portfolio(username)
            st.write(f"**Cash Balance:** ${portfolio.balance:.2f}")
            st.write("**Current Holdings:**")
            for symbol, qty in portfolio.holdings.items():
                price = self.market.get_stock_price(symbol)
                st.write(f"{symbol}: {qty} shares (${price:.2f} each)")

            # Portfolio Performance
            performance = portfolio.get_performance(self.market)
            st.subheader("Portfolio Performance:")
            st.write(f"Total Investment: ${performance['total_investment']:.2f}")
            st.write(f"Current Value: ${performance['current_value']:.2f}")
            st.write(f"Profit/Loss: ${performance['profit_loss']:.2f}")
            st.write(f"Return: {performance['return_percentage']:.2f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_leaderboard_page(self):
        """Render the Leaderboard page"""
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.title("Leaderboard 🏆")
        leaderboard_data = self.leaderboard.leaderboard
        
        if leaderboard_data:
            st.table(leaderboard_data)
        else:
            st.write("No entries in the leaderboard yet.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    def run(self):
        """Main application runner"""
        # Render Navigation
        self.render_navigation()
        
        # Render appropriate page based on current state
        if st.session_state.current_page == 'Home':
            self.render_home_page()
        elif st.session_state.current_page == 'Trade':
            self.render_trade_page()
        elif st.session_state.current_page == 'Portfolio':
            self.render_portfolio_page()
        elif st.session_state.current_page == 'Leaderboard':
            self.render_leaderboard_page()

# Run the application
if __name__ == "__main__":
    simulator = StockMarketSimulator()
    simulator.run()