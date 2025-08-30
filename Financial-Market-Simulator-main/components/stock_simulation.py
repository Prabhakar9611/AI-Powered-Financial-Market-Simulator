import streamlit as st

import pandas as pd

import numpy as np



portfolio = {}



def simulate_stocks():

    st.write("### Simulated Stock Prices")

    days = st.slider("Days to Simulate", min_value=10, max_value=100, value=30)

    companies = ["Company A", "Company B", "Company C"]



    data = {company: np.cumsum(np.random.randn(days)) + 100 for company in companies}

    df = pd.DataFrame(data, index=range(1, days + 1))

    st.line_chart(df)