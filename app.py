import streamlit as st
from agent_utils import get_recommendations

# --------------------------
# Page Configuration
# --------------------------
st.set_page_config(
    page_title="⚔️ Armor of God Content Finder",
    page_icon="⚔️",
    layout="wide"
)

st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px; border-radius: 12px; color: white; text-align: center;">
<h1>⚔️ Full Armor of God Video Recommendations</h1>
<p>Click on a topic and get spiritually enriching Christian videos!</p>
</div>
""", unsafe_allow_html=True)

# --------------------------
# Armor of God topics
# --------------------------
topics = {
    "Helmet of Salvation": "Foundations of being a Christian",
    "Breastplate of Righteousness": "Teachings on righteousness",
    "Belt of Truth": "Living in truth",
    "Sword of the Spirit": "Using the Word in daily life",
    "Shield of Faith": "Strengthening your faith",
    "Feet Shod with Gospel of Peace": "Walking in peace",
    "Backs Protected by Glory of God": "Protection and guidance"
}

# --------------------------
# Topic selection
# --------------------------
selected_topic = st.selectbox(
    "Select an Armor of God topic:",
    list(topics.keys()),
    help="Each topic relates to a spiritual aspect. Videos are curated for mature Christians."
)

# --------------------------
# Get Recommendations Button
# --------------------------
if st.button("Recommend Videos"):
    with st.spinner("Fetching videos..."):
        videos = get_recommendations(selected_topic)

    if videos:
        st.success(f"🎬 Recommended videos for: {selected_topic}")
        # Layout videos in 2 columns
        cols = st.columns(2)
        for idx, video in enumerate(videos):
            col = cols[idx % 2]
            with col:
                st.subheader(video["title"])
                st.markdown(f"*{video.get('description', '')}*")
                # Embed smaller YouTube player
                st.video(video["url"], format="video/mp4", start_time=0)
    else:
        st.warning("No videos found. Try another topic or check your API keys.")
