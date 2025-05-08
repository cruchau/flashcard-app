import streamlit as st
import sqlite3
from database import db_path, verify_user

st.title("🔐 Login / Logout")

if "user" not in st.session_state:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        with sqlite3.connect(db_path) as conn:
            user_id = verify_user(conn, username, password)
            if user_id:
                st.session_state.user = {"id": user_id, "name": username}
                st.success(f"Welcome, {username}!")
                st.rerun()
            else:
                st.error("Invalid credentials.")
else:
    st.success(f"✅ Logged in as: {st.session_state.user['name']}")
    if st.button("Logout"):
        del st.session_state["user"]
        st.rerun()
