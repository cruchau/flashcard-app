import streamlit as st
import sqlite3
from database import db_path, hash_password


st.title("⚙️ Settings")

# --- User creation ---
st.subheader("👤 Create New User")
new_user = st.text_input("New Username")
new_pass = st.text_input("Password", type="password")

if st.button("Create User"):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, password_hash) VALUES (?, ?)",
                (new_user, hash_password(new_pass))
            )
            conn.commit()
            st.success("User created successfully.")
    except sqlite3.IntegrityError:
        st.error("Username already exists.")

# --- Theme selector ---
st.subheader("🎨 Theme Settings")

theme = st.selectbox("Choose Theme", ["Light Mode", "Dark Mode"])

if theme == "Dark Mode":
    st.session_state.theme = "dark"
else:
    st.session_state.theme = "light"

st.success(f"Theme set to {theme}")
