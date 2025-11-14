import json
from pathlib import Path
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import os
import plotly.express as px

st.set_page_config(page_title="MindScape Global News", layout="wide", page_icon="📰")
st.markdown(
    """
    <div style="background-color:#FF6F61;padding:20px;border-radius:12px;">
        <h1 style="color:white;text-align:center;">📰 MindScape - Global News Summarization & Sentiment Dashboard</h1>
        <p style="color:#fff;text-align:center;">Empowering insights through real-time news analytics 🌍</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.header("🌍 Filter Options")

topic = st.sidebar.selectbox(
    "Select a Topic:",
    [
        "general",
        "technology",
        "health",
        "science",
        "business",
        "sports",
        "entertainment",
        "education",
        "environment",
    ],
)


if st.sidebar.button("🔁 Fetch & Update This Topic"):
    with st.spinner(f"⏳ Fetching and processing latest {topic} news..."):
        os.system(f"python fetch_news.py {topic}")
        os.system("python process_articles.py")
        os.system("python summarize_sentiment.py")
        time.sleep(2) 

    st.success(f"✅ {topic.capitalize()} news updated successfully!")
    st.info("🔄 Please click the **Refresh Dashboard** button below to see the latest updates.")

if st.sidebar.button("🔄 Refresh Dashboard"):
    st.cache_data.clear() 
    st.rerun() 


st.sidebar.markdown("---")
st.sidebar.caption("🕓 Auto-refresh every 2 minutes enabled.")

PROCESSED_FILE = Path("processed.json")

if not PROCESSED_FILE.exists():
    st.warning("⚠️ No processed data found. Run the summarization pipeline first.")
    st.stop()

with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

st.markdown("### 🗞️ Overview")
col1, col2, col3 = st.columns(3)

col1.metric("Total Articles", len(df))
col2.metric("Unique Sources", df["source"].nunique() if "source" in df.columns else "N/A")
col3.metric("Average Sentiment", round(df["sentiment_score"].mean(), 2) if "sentiment_score" in df.columns else "N/A")

st.markdown("### 💬 Sentiment Distribution")

if "sentiment" in df.columns:
    df["sentiment"] = df["sentiment"].apply(
        lambda x: x.get("label") if isinstance(x, dict) else str(x)
    )
    df = df[df["sentiment"].notnull() & (df["sentiment"] != "nan")]
    sentiment_counts = df["sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]

    fig_sentiment = px.bar(
        sentiment_counts,
        x="Sentiment",
        y="Count",
        color="Sentiment",
        title="💬 Sentiment Breakdown",
        color_discrete_sequence=px.colors.qualitative.Set2,
        text_auto=True,
    )

    st.plotly_chart(fig_sentiment, use_container_width=True)
else:
    st.warning("⚠️ No sentiment data found in processed.json")


if "topic" in df.columns:
    st.markdown("### 🗂️ Topic Distribution")
    fig_topic = px.pie(
        df,
        names="topic",
        title="Topic Categories",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    st.plotly_chart(fig_topic, use_container_width=True)

st.markdown("### 📰 Latest Summarized Articles")
for i, row in df.iterrows():
    st.markdown(
        f"""
        <div style='background-color:#FFFFFF;padding:15px;border-radius:10px;margin-bottom:10px;
                    box-shadow:0 2px 8px rgba(0,0,0,0.05);'>
            <h4 style='color:#FF6F61;margin-bottom:5px;'>{row.get('title','No Title')}</h4>
            <p style='color:#444;'>{row.get('summary','No summary available.')}</p>
            <p><b>Sentiment:</b> {row.get('sentiment','N/A')} | 
               <b>Source:</b> {row.get('source','N/A')}</p>
            <a href='{row.get('url','#')}' target='_blank' style='color:#0066CC;text-decoration:none;'>
                🔗 Read Full Article
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )
st.markdown(
    """
    <hr>
    <div style='text-align:center;color:gray;font-size:14px;'>
        Developed by <b>Ayisha Salmira</b> 💡 | Powered by Python 🐍, Streamlit, and Hugging Face 🤗
    </div>
    """,
    unsafe_allow_html=True,
)
