import requests
import streamlit as st

def fetch_financial_news(api_key, category="business", country="us"):
    """
    Fetch financial news headlines using the NewsAPI.
    :param api_key: API key for NewsAPI
    :param category: News category to fetch (default: 'business')
    :param country: Country code for the news (default: 'us')
    :return: List of news headlines and URLs
    """
    base_url = "https://newsapi.org/v2/top-headlines"
    params = {
        "category": category,
        "country": country,
        "apiKey": api_key,
    }

    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            news = [{"title": article["title"], "url": article["url"]} for article in articles]
            return news
        else:
            st.error("Failed to fetch news. Please check your API key and parameters.")
            return []
    except Exception as e:
        st.error(f"An error occurred while fetching news: {e}")
        return []

def display_news():
    """
    Display the fetched financial news headlines in a ticker format.
    """
    st.write("### 📰 Latest Financial News")
    
    # Replace 'your_newsapi_key' with your actual API key
    api_key = "909cf15171c74f14bbd515993ad5a594"  
    news = fetch_financial_news(api_key)

    if not news:
        st.info("No news available at the moment.")
        return

    # Display the news headlines
    st.markdown("""
        <style>
            .news-ticker {
                background-color: #007BFF;
                color: white;
                padding: 10px;
                overflow: hidden;
                white-space: nowrap;
                animation: scroll 15s linear infinite;
                font-size: 16px;
                font-weight: bold;
            }

            @keyframes scroll {
                0% { transform: translateX(100%); }
                100% { transform: translateX(-100%); }
            }
        </style>
    """, unsafe_allow_html=True)

    news_html = "".join([f"<span style='margin-right: 30px;'><a href='{item['url']}' target='_blank' style='color: white; text-decoration: none;'>{item['title']}</a></span>" for item in news])

    st.markdown(f"""
        <div class="news-ticker">{news_html}</div>
    """, unsafe_allow_html=True)