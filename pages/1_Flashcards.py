import streamlit as st
import sqlite3
import random
from database import db_path

# 🌗 Theme styling (dark mode)
theme = st.session_state.get("theme", "light")
if theme == "dark":
    st.markdown(
        """
        <style>
        html, body, [class*="css"] {
            background-color: #1e1e1e !important;
            color: #f5f5f5 !important;
        }
        .stButton button {
            background-color: #444 !important;
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# 🧠 Title
st.title("🧠 Flashcard Quiz")

# 🔐 Require login
user = st.session_state.get("user")
if not user:
    st.warning("Please log in to access the quiz.")
    st.stop()

# 📚 Load flashcards from DB
with sqlite3.connect(db_path) as conn:
    cursor = conn.cursor()
    flashcards = cursor.execute("SELECT id, acronym, meaning FROM flashcards").fetchall()

if not flashcards:
    st.warning("No flashcards available. Please add some in the Configuration page.")
    st.stop()

# 🎲 Pick one flashcard at a time
if "current_flashcard" not in st.session_state:
    st.session_state.current_flashcard = random.choice(flashcards)

fid, acronym, meaning = st.session_state.current_flashcard

# 📝 User input
st.subheader(f"What does **{acronym}** stand for?")
user_input = st.text_input("✍️ Your Answer", key="user_input")

# 👁️ Reveal logic
if "revealed" not in st.session_state:
    st.session_state.revealed = False

if st.button("Reveal Answer"):
    st.session_state.revealed = True

# ✅ Display result if revealed
if st.session_state.revealed:
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Your Answer:** {user_input or '*No input*'}")
    with col2:
        st.success(f"**Correct Answer:** {meaning}")

    correct = st.radio("Did you get it right?", ["Yes", "No"], horizontal=True)

    if st.button("Submit Response"):
        # Insert review with user_id
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO reviews (flashcard_id, user_id, correct) VALUES (?, ?, ?)",
                (fid, user["id"], correct == "Yes")
            )
            conn.commit()

        st.success("Response recorded. Loading next flashcard...")

        # 🔄 Reset for next round
        st.session_state.pop("current_flashcard", None)
        st.session_state.pop("revealed", None)
        st.session_state.pop("user_input", None)
        st.rerun()
