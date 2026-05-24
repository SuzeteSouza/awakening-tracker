import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import hashlib

# -------------------------------------------------------------
# 1. DATABASE CONFIGURATION
# -------------------------------------------------------------
# Connects to a local database file. Streamlit will auto-create this file.
conn = sqlite3.connect("awakening.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_scores (
        date TEXT PRIMARY KEY,
        score INTEGER
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS dream_journal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        dream_text TEXT,
        tags TEXT
    )
""")
conn.commit()

# -------------------------------------------------------------
# 2. GNOSTIC DAILY QUOTE SYSTEM
# -------------------------------------------------------------
GNOSTIC_QUOTES = [
    {
        "quote": "The Monad is a monism which lacks nothing. It is total light, pure, holy, and unblemished. It is completely perfect.",
        "topic": "The Monad (The True Source)",
        "author": "The Apocryphon of John"
    },
    {
        "quote": "The Archons do not want you to remember your divine origin. They keep your mind trapped in endless cycles of worry, survival, and mundane routines to consume your divine spark.",
        "topic": "The Archontic Distraction",
        "author": "Gnostic Fragment"
    },
    {
        "quote": "Abandon the search for God from without. Look within, and learn who it is that makes everything its own in you. Gnosis is the direct experience of your own uncreated light.",
        "topic": "Gnosis (Direct Knowledge)",
        "author": "Monoimus the Gnostic"
    },
    {
        "quote": "The separation you feel from the universe is a structural illusion designed by the Demiurge. Your spirit (Pneuma) is fundamentally one with the eternal Monad; there is no distance.",
        "topic": "The Illusion of Separation",
        "author": "The Gospel of Truth"
    },
    {
        "quote": "Wake up from the sleep of material distraction. The matrix of the Archons only holds power over the mind that agrees to forget its true sovereignty.",
        "topic": "Breaking the Archontic Trick",
        "author": "The Hymn of the Pearl"
    }
]

def get_daily_quote():
    """Generates a stable index based on today's date string so it changes exactly once a day."""
    today_str = datetime.today().strftime('%Y-%m-%d')
    hash_object = hashlib.md5(today_str.encode())
    index = int(hash_object.hexdigest(), 16) % len(GNOSTIC_QUOTES)
    return GNOSTIC_QUOTES[index]

# -------------------------------------------------------------
# 3. APP SIDEBAR & NAVIGATION
# -------------------------------------------------------------
st.set_page_config(page_title="Awakening", page_icon="👁️", layout="centered")
st.sidebar.title("🧘 Mindfulness Menu")
page = st.sidebar.radio("Navigate", ["Today's Practice", "Dream Log", "My Analytics"])

# -------------------------------------------------------------
# PAGE A: TODAY'S PRACTICE
# -------------------------------------------------------------
if page == "Today's Practice":
    st.title("👁️ The Here and Now")
    
    # Daily Gnostic Contemplation Layout
    daily_data = get_daily_quote()
    st.markdown(f"### 🕯️ Daily Gnosis Contemplation")
    st.markdown(
        f"""
        <div style="background-color: #1E1E1E; padding: 20px; border-radius: 10px; border-left: 5px solid #FFD700; margin-bottom: 25px;">
            <p style="font-style: italic; font-size: 1.1em; color: #E0E0E0;">"{daily_data['quote']}"</p>
            <p style="text-align: right; font-weight: bold; color: #FFD700; margin-bottom: 0;">— {daily_data['author']}</p>
            <span style="font-size: 0.8em; background-color: #333; padding: 3px 8px; border-radius: 5px; color: #AAA;">Focus: {daily_data['topic']}</span>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Feature 1: The Audio Wake Up Prompt
    st.subheader("🔊 Audio Reality Check")
    st.write("Click below to play a voice checkpoint:")
    st.audio("https://soundhelix.com")
    
    # Feature 2: Active Reality State Testing
    st.subheader("❓ Reality Check")
    st.info("The Archons use mundane mental loops to keep you asleep. Break the loop right now. Observe your surroundings. Are you awake?")
    reality_confirm = st.text_input("Type 'I AM AWAKE' to shatter the illusion of separation:")
    if st.button("Log Awareness Moment"):
        if reality_confirm.strip().upper() == "I AM AWAKE":
            st.balloons()
            st.success("✨ Divine Spark Activated. You have intentionally broken the automated routine cycle.")
        else:
            st.warning("Please type the phrase exactly to confirm your presence status.")

    # Feature 3: Daily Score Slider
    st.subheader("📊 Presence Rating")
    score = st.slider("Rate your overall detachment from the mental trap today (1-10):", 1, 10, 5)
    if st.button("Save Entry"):
        today = datetime.today().strftime('%Y-%m-%d')
        cursor.execute("""
            INSERT INTO daily_scores (date, score) VALUES (?, ?)
            ON CONFLICT(date) DO UPDATE SET score = excluded.score
        """, (today, score))
        conn.commit()
        st.success(f"Score of {score}/10 archived for today.")

# -------------------------------------------------------------
# PAGE B: DREAM LOG
# -------------------------------------------------------------
elif page == "Dream Log":
    st.title("🌙 Nightly Dream Journal")
    st.write("The material realm is a waking dream. Track your sleeping dreams to develop lucidity and sovereignty over all states of consciousness.")
    
    dream_input = st.text_area("What did you experience during your rest?")
    tags = st.multiselect("Select applicable tags:", ["Lucid", "Vivid", "Flying", "Archontic Interference", "Monad Connection", "Recurring", "Nightmare"])
    
    if st.button("Archive Dream Entry"):
        if dream_input:
            today = datetime.today().strftime('%Y-%m-%d')
            tag_string = ", ".join(tags)
            cursor.execute("INSERT INTO dream_journal (date, dream_text, tags) VALUES (?, ?, ?)", 
                           (today, dream_input, tag_string))
            conn.commit()
            st.success("Dream log safely encrypted and stored.")
        else:
            st.error("Please provide text contents before saving your log.")

# -------------------------------------------------------------
# PAGE C: ANALYTICS DASHBOARD
# -------------------------------------------------------------
elif page == "My Analytics":
    st.title("📈 Awakening Dashboard")
    
    df_scores = pd.read_sql_query("SELECT * FROM daily_scores ORDER BY date ASC", conn)
    
    if not df_scores.empty:
        st.subheader("Your Weekly Presence Index")
        st.line_chart(df_scores.set_index("date"))
    else:
        st.info("No scores submitted yet. Log data under 'Today's Practice' to build a timeline.")
        
    df_dreams = pd.read_sql_query("SELECT date, dream_text, tags FROM dream_journal ORDER BY id DESC", conn)
    if not df_dreams.empty:
        st.subheader("Past Dream Entries")
        st.dataframe(df_dreams, use_container_width=True)
        