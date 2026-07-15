import re
import streamlit as st
import pandas as pd
from collections import Counter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ─── 1. CORE CONFIGURATION & THEME INTEGRATION ───
st.set_page_config(
    layout="wide",
    page_title="Abei's Strategic Sentiment Architect",
    page_icon="📊"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');

    .stApp { background-color: #f5f4f0; }

    h1, h2, h3, .stHeader {
        font-family: 'Syne', sans-serif !important;
        color: #0e0e0e !important;
        letter-spacing: -1px;
    }

    p, span, label {
        font-family: 'DM Sans', sans-serif !important;
        color: #0e0e0e !important;
    }

    a {
        color: #1a6bff !important;
        text-decoration: underline !important;
        font-weight: 500;
    }

    div.stButton > button:first-child {
        background-color: #1a6bff !important;
        color: #ffffff !important;
        opacity: 1 !important;
        visibility: visible !important;
        border-radius: 100px;
        padding: 0.6rem 2rem;
        font-weight: 700;
        border: none;
        box-shadow: 0 4px 14px 0 rgba(26,107,255,0.39);
        display: block !important;
    }

    div.stButton > button:hover {
        background-color: #0e0e0e !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.23);
        transform: translateY(-1px);
    }

    .audit-container {
        margin-top: 40px !important;
        padding-top: 20px !important;
        border-top: 1px solid #e0e0e0;
    }

    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ─── 2. LOGIC LAYER (Real YouTube Extraction + VADER Sentiment) ───
analyzer = SentimentIntensityAnalyzer()

STOPWORDS = {
    "the","a","an","and","or","but","is","are","was","were","be","been","to","of",
    "in","on","for","it","this","that","with","as","at","by","from","i","you","he",
    "she","they","we","my","your","his","her","their","our","not","so","if","just",
    "im","its","it's","have","has","had","do","does","did","can","will","would",
    "could","should","about","what","when","how","all","one","also","like","more",
    "very","really","because","get","got","video","comment"
}


def extract_video_id(url: str):
    """Pulls the 11-char YouTube video ID out of common URL formats."""
    patterns = [
        r"(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/shorts\/|youtube\.com\/embed\/)([A-Za-z0-9_-]{11})"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    # fallback: bare 11-char ID pasted directly
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", url.strip()):
        return url.strip()
    return None


@st.cache_data(show_spinner=False, ttl=3600)
def fetch_comments(video_id: str, api_key: str, max_comments: int = 100):
    """Pulls top-level comments via YouTube Data API v3. Returns (comments_list, error_str)."""
    youtube = build("youtube", "v3", developerKey=api_key)
    comments = []
    next_page_token = None

    try:
        while len(comments) < max_comments:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=min(100, max_comments - len(comments)),
                pageToken=next_page_token,
                textFormat="plainText",
                order="relevance"
            )
            response = request.execute()

            for item in response.get("items", []):
                snippet = item["snippet"]["topLevelComment"]["snippet"]
                comments.append({
                    "author": snippet.get("authorDisplayName", "Unknown"),
                    "text": snippet.get("textDisplay", ""),
                    "likes": snippet.get("likeCount", 0),
                    "published": snippet.get("publishedAt", "")
                })

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        return comments, None

    except HttpError as e:
        reason = ""
        try:
            reason = e.error_details[0].get("reason", "") if e.error_details else ""
        except Exception:
            pass

        if "commentsDisabled" in str(e) or reason == "commentsDisabled":
            return [], "Comments are disabled for this video."
        if "quotaExceeded" in str(e) or reason == "quotaExceeded":
            return [], "YouTube API daily quota exceeded. Try again tomorrow, or use a different API key."
        if e.resp.status == 403:
            return [], "API key rejected (403). Double-check the key and that the YouTube Data API v3 is enabled for it."
        if e.resp.status == 404:
            return [], "Video not found. Double-check the URL."
        return [], f"YouTube API error: {e}"
    except Exception as e:
        return [], f"Unexpected error: {e}"


def analyze_sentiment(comments: list):
    """Runs VADER over every comment and returns a scored DataFrame."""
    rows = []
    for c in comments:
        scores = analyzer.polarity_scores(c["text"])
        compound = scores["compound"]
        if compound >= 0.05:
            label = "Positive"
        elif compound <= -0.05:
            label = "Negative"
        else:
            label = "Neutral"
        rows.append({
            "Comment Sample": (c["text"][:140] + "…") if len(c["text"]) > 140 else c["text"],
            "score": compound,
            "label": label,
            "likes": c["likes"],
            "author": c["author"]
        })
    return pd.DataFrame(rows)


def top_keywords(comments: list, n: int = 6):
    """Very lightweight keyword frequency for a 'Key Theme' signal."""
    words = []
    for c in comments:
        tokens = re.findall(r"[a-zA-Z']+", c["text"].lower())
        words.extend([t for t in tokens if t not in STOPWORDS and len(t) > 2])
    if not words:
        return "N/A"
    most_common = Counter(words).most_common(n)
    return ", ".join(w for w, _ in most_common[:3]).title()


# ─── 3. UI ARCHITECTURE (Split-Screen Layout) ───
left_col, right_col = st.columns([1, 2.2], gap="large")

with left_col:
    st.markdown("### **Intelligence Input**")
    st.write("Analyze real Voice of Customer (VoC) trends from any public YouTube video's comments.")

    yt_url = st.text_input("Paste YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

    api_key = st.secrets.get("YOUTUBE_API_KEY", None) if hasattr(st, "secrets") else None
    if not api_key:
        api_key = st.text_input("YouTube Data API v3 Key:", type="password",
                                 help="Get one free at console.cloud.google.com → APIs & Services → Credentials")

    max_comments = st.slider("Max comments to pull", 20, 200, 100, step=20)
    run_btn = st.button("Generate Strategic Analysis")

    st.divider()
    st.markdown("""
    **Analytical Framework:**
    * **Data Source:** YouTube Data API v3 (live comment extraction).
    * **NLP Pipeline:** VADER (Valence Aware Dictionary and sEntiment Reasoner).
    * **Goal:** ROI-driven insights to support CRM strategy.
    """)
    st.info("Built by Abeinathan SK | MBA Business Analytics")

with right_col:
    if yt_url and run_btn:
        if not api_key:
            st.error("Please enter a YouTube Data API v3 key on the left to run a live analysis.")
        else:
            video_id = extract_video_id(yt_url)
            if not video_id:
                st.error("Couldn't parse a video ID from that URL. Paste a standard YouTube link.")
            else:
                with st.spinner("Pulling comments and scoring sentiment..."):
                    comments, error = fetch_comments(video_id, api_key, max_comments)

                if error:
                    st.error(error)
                elif not comments:
                    st.warning("No comments found for this video.")
                else:
                    df = analyze_sentiment(comments)

                    st.markdown("## **Strategic Intelligence Dashboard**")
                    st.markdown(f"**Live Analysis for:** [{yt_url}]({yt_url}) · {len(df)} comments pulled")

                    pos_pct = (df["label"] == "Positive").mean() * 100
                    neg_pct = (df["label"] == "Negative").mean() * 100
                    net_sentiment = pos_pct - neg_pct
                    avg_compound = df["score"].mean()

                    if net_sentiment > 15:
                        pulse = "Positive"
                    elif net_sentiment < -15:
                        pulse = "Negative"
                    else:
                        pulse = "Mixed"

                    kpi1, kpi2, kpi3 = st.columns(3)
                    kpi1.metric("Net Sentiment Score", f"{net_sentiment:+.0f}%", f"avg compound {avg_compound:+.2f}")
                    kpi2.metric("Market Pulse", pulse, f"{pos_pct:.0f}% positive")
                    kpi3.metric("Key Theme", top_keywords(comments))

                    st.subheader("Sentiment Distribution Trend")
                    st.area_chart(df["score"], color="#1a6bff")

                    label_counts = df["label"].value_counts()
                    top_pos = df.sort_values("score", ascending=False).iloc[0]["Comment Sample"] if len(df) else ""
                    top_neg = df.sort_values("score", ascending=True).iloc[0]["Comment Sample"] if len(df) else ""

                    st.success(f"""
                    ### **Executive Product Summary**
                    Based on {len(df)} live comments extracted from this video:
                    - **Sentiment Split:** {int(label_counts.get('Positive', 0))} positive, {int(label_counts.get('Neutral', 0))} neutral, {int(label_counts.get('Negative', 0))} negative.
                    - **Strongest Positive Signal:** "{top_pos}"
                    - **Strongest Negative Signal:** "{top_neg}"
                    """)

                    st.markdown('<div class="audit-container"></div>', unsafe_allow_html=True)
                    st.markdown("### **Data Audit Trail**")
                    with st.expander("Expand to view raw sentiment scores and datasets"):
                        st.dataframe(
                            df[["author", "Comment Sample", "score", "label", "likes"]],
                            use_container_width=True
                        )
                        st.download_button(
                            "Download full results as CSV",
                            df.to_csv(index=False),
                            file_name="youtube_sentiment_results.csv",
                            mime="text/csv"
                        )
    else:
        st.markdown("### **Waiting for Intelligence Input...**")
        st.write("Paste a YouTube video link and add your API key on the left to pull live comments and generate strategic recommendations.")
        st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=1000")
