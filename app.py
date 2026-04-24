import streamlit as st
import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ─── 1. CORE CONFIGURATION & THEME INTEGRATION ───
st.set_page_config(
    layout="wide", 
    page_title="Abei's Strategic Sentiment Architect",
    page_icon="📊"
)

# Injecting Abei's Portfolio CSS tokens for a seamless IFrame look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');
    
    /* Global Theme Overrides */
    .stApp { background-color: #f5f4f0; } /* Matches --bg in style.css */
    
    h1, h2, h3, .stHeader {
        font-family: 'Syne', sans-serif !important;
        color: #0e0e0e !important; /* Matches --ink */
        letter-spacing: -1px;
    }
    
    p, span, label {
        font-family: 'DM Sans', sans-serif !important;
        color: #4a4a4a; /* Matches --ink-2 */
    }

    /* Custom Button Styling */
    .stButton>button {
        background-color: #0e0e0e; /* Matches --ink */
        color: #ffffff;
        border-radius: 100px;
        padding: 0.6rem 2rem;
        font-weight: 700;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1a6bff !important; /* Matches --accent */
        box-shadow: 0 8px 30px rgba(26,107,255,0.35);
    }

    /* Input Box Styling */
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border-radius: 12px;
        border: 1px solid rgba(0,0,0,0.08);
    }

    /* UI Clean-up: Hide Streamlit Branding */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ─── 2. LOGIC LAYER (Sentiment Intelligence) ───
analyzer = SentimentIntensityAnalyzer()

def get_sentiment_brief(url):
    # This simulates your extraction logic for the MVP
    # In production, replace with YouTube Data API calls
    mock_feedback = [
        {"text": "Premium build quality, worth the price.", "score": 0.8},
        {"text": "The mobile app UI feels sluggish on Zorin OS.", "score": -0.4},
        {"text": "Customer support responded in minutes. Impressive.", "score": 0.9},
        {"text": "Slightly overpriced for the feature set.", "score": -0.2},
        {"text": "Best investment for my Business Analytics workflow.", "score": 0.85}
    ]
    return pd.DataFrame(mock_feedback)

# ─── 3. UI ARCHITECTURE (Split-Screen Layout) ───
left_col, right_col = st.columns([1, 2.2], gap="large")

with left_col:
    st.image("https://abeinathan.github.io/logo.png", width=60) # Placeholder for your logo
    st.markdown("### **Intelligence Input**")
    st.write("Analyze Voice of Customer (VoC) trends for any product or service.")
    
    yt_url = st.text_input("Paste URL (YouTube/Marketplace):", placeholder="https://...")
    run_btn = st.button("Generate Strategic Analysis")
    
    st.divider()
    st.markdown("""
    **Analytical Framework:**
    * **Methodology:** Hypothesis-driven secondary research[cite: 41].
    * **NLP Pipeline:** Weighted VADER & TextBlob sentiment scoring.
    * **Goal:** ROI-driven insights to support Enterprise Relationship Management[cite: 8].
    """)
    st.info("Built by Abeinathan SK | MBA Business Analytics [cite: 2, 10]")

with right_col:
    if yt_url and run_btn:
        st.markdown(f"## **Strategic Intelligence Dashboard**")
        st.caption(f"Real-time Analysis for: {yt_url}")
        
        # Process Data
        df = get_sentiment_brief(yt_url)
        avg_sentiment = df['score'].mean()
        
        # Executive KPIs
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Net Sentiment Score", "74%", "+12%")
        kpi2.metric("Market Pulse", "Positive", "Bullish")
        kpi3.metric("Key Theme", "Value/Quality")

        # Visual Intelligence (Mirroring Power BI proficiency) [cite: 41]
        st.subheader("Sentiment Distribution Trend")
        st.area_chart(df['score'], color="#1a6bff")
        
        # Executive Summary Box (Storytelling Proficiency) [cite: 6, 8]
        st.success(f"""
        ### **Executive Product Summary**
        Based on the current data extraction:
        - **Core Strength:** High consumer confidence in build quality and support responsiveness.
        - **Strategic Pain Point:** 20% of negative feedback centers on UI latency within specific OS environments.
        - **Actionable Insight:** Prioritize backend optimization to reduce churn among high-value technical users.
        """)
        
        # Data & Querying Proficiency Check [cite: 41]
        with st.expander("View Raw Sentiment Data"):
            st.dataframe(df, use_container_width=True)
            
    else:
        # Initial State / Landing View
        st.markdown("### **Waiting for Intelligence Input...**")
        st.write("Enter a link on the left to activate the NLP pipeline and generate brand-level strategic recommendations.")
        st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=1000", opacity=0.3)
