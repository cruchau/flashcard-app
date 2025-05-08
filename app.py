import streamlit as st
import sqlite3
from database import db_path, verify_user, init_db

init_db()

st.set_page_config(page_title="Flashcard App", layout="centered")
st.markdown("<h1 style='text-align:center;'>📚 Welcome to Your Flashcard App</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px;'>A simple, interactive way to master acronyms 💡</p>", unsafe_allow_html=True)

# Load quick stats
with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    flashcard_count = cursor.execute("SELECT COUNT(*) FROM flashcards").fetchone()[0]
    review_count = cursor.execute("SELECT COUNT(*) FROM reviews").fetchone()[0]

st.markdown("---")

# Top stats section
col1, col2 = st.columns(2)
with col1:
    st.metric("📖 Flashcards Available", flashcard_count)
with col2:
    st.metric("📝 Total Reviews Logged", review_count)

st.markdown("---")

# Navigation Buttons
st.markdown("### 🚀 Jump Into:")
nav_col1, nav_col2, nav_col3 = st.columns(3)

with nav_col1:
    st.page_link("pages/1_Flashcards.py", label="🧠 Start Quiz", icon="➡️")

with nav_col2:
    st.page_link("pages/2_Statistics.py", label="📊 View Statistics", icon="📈")

with nav_col3:
    st.page_link("pages/3_Configuration.py", label="⚙️ Configure Flashcards", icon="🛠️")

# Optional tips
st.markdown("---")
with st.expander("💡 How to Use This App"):
    st.write("""
    - Use **Start Quiz** to test yourself on acronyms.
    - Track your performance in **Statistics**.
    - Manage flashcards in **Configuration**.
    - Import or export flashcards from a CSV file.
    """)

st.markdown("<p style='text-align:center; font-size:12px;'>Made with ❤️ using Python, Streamlit and SQLite.</p>", unsafe_allow_html=True)
