import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# 1. Page configuration
st.set_page_config(page_title="NewsPulse ML", layout="wide")
st.title("📈 Market Sentiment (NewsPulse ML)")

# 2. Connect to the database
engine = create_engine("sqlite:///news_data.db")

# Load only processed news using Pandas
query = "SELECT title, published_at, sentiment FROM articles WHERE status='processed'"
df = pd.read_sql_query(query, engine)

if df.empty:
    st.warning("No processed news in the database yet. Run the worker!")
else:
    # 3. Calculate the "average temperature" of the market
    avg_score = df["sentiment"].mean()
    
    # 4. Display the main metric
    st.metric(
        label="Average Sentiment Score (Above 0 = Bulls 🟢, Below 0 = Bears 🔴)", 
        value=round(avg_score, 4)
    ) 
    
    # 5. Draw a nice chart
    st.write("### Sentiment Chart (by Article)")
    st.bar_chart(df.set_index("title")["sentiment"])
    
    # 6. Show the raw data table
    st.write("### Raw Data")
    st.dataframe(df, use_container_width=True)
