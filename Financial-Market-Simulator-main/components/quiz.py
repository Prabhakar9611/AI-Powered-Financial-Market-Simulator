import streamlit as st


# Add custom CSS for animations and hover effects
def add_custom_css():
    st.markdown(
        """
        <style>
            /* Background Styling */
            body {
                background: linear-gradient(to bottom, #e3f2fd, #ffffff);
                font-family: "Arial", sans-serif;
                color: #333;
            }

            /* Title Styling */
            h1 {
                color: #1a237e;
                text-align: center;
                margin-top: 20px;
                animation: fadeIn 2s ease-in-out;
            }

            /* Card Styles */
            .card {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                margin: 20px 0;
                padding: 20px;
                transition: transform 0.3s, box-shadow 0.3s;
            }

            .card:hover {
                transform: translateY(-10px);
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
            }

            /* Animated Icons */
            .icon {
                font-size: 30px;
                color: #1565c0;
                margin-right: 10px;
                animation: bounce 2s infinite;
            }

            @keyframes bounce {
                0%, 100% {
                    transform: translateY(0);
                }
                50% {
                    transform: translateY(-8px);
                }
            }

            /* List Styling */
            ul {
                list-style-type: none;
                padding: 0;
                margin: 20px 0;
            }

            ul li {
                background-color: #e3f2fd;
                border-radius: 5px;
                padding: 10px;
                margin-bottom: 10px;
                transition: background-color 0.3s;
            }

            ul li:hover {
                background-color: #bbdefb;
            }

            /* Section Header Styling */
            .section-header {
                color: #0d47a1;
                text-align: center;
                margin-bottom: 10px;
            }

            /* Fade In Animation */
            @keyframes fadeIn {
                from {
                    opacity: 0;
                }
                to {
                    opacity: 1;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


# Display the Stock Market Description Page
def stock_market_description():
    # Apply custom CSS
    add_custom_css()

    # Title
    st.markdown("<h1>📈 What is Trading and the Stock Market?</h1>", unsafe_allow_html=True)

    # Introduction
    st.markdown(
        """
        <div class="card">
            <h2 class="section-header">Introduction</h2>
            <p>Trading in the stock market involves buying and selling shares of publicly listed companies. 
            It is a dynamic environment where investors and traders aim to profit by predicting changes 
            in stock prices and taking positions accordingly.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Key Concepts
    st.markdown(
        """
        <div class="card">
            <h2 class="section-header">Key Concepts</h2>
            <ul>
                <li><span class="icon">📊</span><b>Stocks</b>: Represent ownership in a company. Owning a stock means you are a shareholder.</li>
                <li><span class="icon">💸</span><b>Dividends</b>: Profits shared by a company to its shareholders.</li>
                <li><span class="icon">🐂</span><b>Bull Market</b>: A market condition where stock prices are rising.</li>
                <li><span class="icon">🐻</span><b>Bear Market</b>: A market condition where stock prices are falling.</li>
                <li><span class="icon">🏦</span><b>IPO (Initial Public Offering)</b>: When a company offers its shares to the public for the first time.</li>
                <li><span class="icon">⚖️</span><b>Bid Price and Ask Price</b>: The bid is the price buyers are willing to pay, while the ask is the price sellers want.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Risks in Trading
    st.markdown(
        """
        <div class="card">
            <h2 class="section-header">Risks in Trading</h2>
            <ul>
                <li><span class="icon">⚡</span><b>Market Volatility</b>: Prices can change rapidly, leading to potential losses.</li>
                <li><span class="icon">📖</span><b>Lack of Knowledge</b>: Without proper understanding, trading can lead to poor decisions.</li>
                <li><span class="icon">🌍</span><b>Economic Events</b>: Global events like recessions or pandemics can impact stock markets.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Why Participate
    st.markdown(
        """
        <div class="card">
            <h2 class="section-header">Why To Participate in the Stock Market?</h2>
            <ul>
                <li><span class="icon">📈</span><b>Wealth Creation</b>: A well-thought-out investment strategy can grow your wealth over time.</li>
                <li><span class="icon">📂</span><b>Diversification</b>: Stocks allow you to diversify your investment portfolio.</li>
                <li><span class="icon">💰</span><b>Liquidity</b>: Shares can be quickly bought or sold in the market.</li>
                <li><span class="icon">🏢</span><b>Ownership</b>: Shareholders get a stake in the company's growth and profits.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Tips for Success
    st.markdown(
        """
        <div class="card">
            <h2 class="section-header">How to Succeed in Trading?</h2>
            <ul>
                <li>Research the companies you invest in.</li>
                <li>Understand financial news and market trends.</li>
                <li>Diversify your investments to manage risks.</li>
                <li>Keep emotions in check and focus on long-term goals.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Run the app
if __name__ == "__main__":
    stock_market_description()
