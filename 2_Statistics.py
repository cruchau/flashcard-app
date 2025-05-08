import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from database import db_path


st.title("📊 Flashcard Performance Dashboard")

st.write("###") 

# Load review + flashcard data
with sqlite3.connect(db_path) as conn:
    df_reviews = pd.read_sql_query("SELECT * FROM reviews", conn)
    df_flashcards = pd.read_sql_query("SELECT * FROM flashcards", conn)

# ⛔ No data case
if df_reviews.empty or df_flashcards.empty:
    st.warning("Not enough data to display statistics. Try reviewing some flashcards first.")
    st.stop()

# =============================
# 🧾 GLOBAL METRICS
# =============================
total = len(df_reviews)
correct = df_reviews["correct"].sum()
accuracy = (correct / total) * 100 if total > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("🧾 Total Reviewed", total)
col2.metric("✅ Correct", correct)
col3.metric("🎯 Accuracy", f"{accuracy:.1f}%")

st.divider()

st.write("###")

# =============================
# 📊 Correct vs Incorrect Chart
# =============================
st.subheader("✅ Overall Answer Distribution")
counts = df_reviews["correct"].value_counts().sort_index()
label_map = {False: "Incorrect", True: "Correct"}
counts.index = [label_map.get(k, str(k)) for k in counts.index]

fig, ax = plt.subplots()
counts.plot(kind="bar", ax=ax)
ax.set_ylabel("Count")
ax.set_title("Correct vs Incorrect")
ax.set_ylim(0, max(counts) + 1)
st.pyplot(fig)

st.write("###")

# =============================
# 🔍 Per-Flashcard Performance
# =============================
st.subheader("🔎 Select Flashcard to Analyze")
# Build option label -> id dictionary
flashcard_options = {
    f"{row['acronym']} — {row['meaning']}": row["id"]
    for _, row in df_flashcards.iterrows()
}

selected_label = st.selectbox("Choose a flashcard", list(flashcard_options.keys()))
selected_id = flashcard_options[selected_label]

filtered_reviews = df_reviews[df_reviews["flashcard_id"] == selected_id]

if not filtered_reviews.empty:
    total_fc = len(filtered_reviews)
    correct_fc = filtered_reviews["correct"].sum()
    accuracy_fc = (correct_fc / total_fc) * 100 if total_fc > 0 else 0

    st.info(f"📌 You answered **{total_fc}** times on this flashcard")
    st.success(f"🎯 Accuracy on this flashcard: **{accuracy_fc:.1f}%**")

    st.markdown("##### Recent Responses for This Flashcard")
    filtered_reviews["timestamp"] = pd.to_datetime(filtered_reviews["timestamp"])
    st.dataframe(filtered_reviews.sort_values("timestamp", ascending=False).head(10)[["timestamp", "correct"]])
else:
    st.warning("No review history for this flashcard yet.")

st.write("###")

# =============================
# 🕒 Recent Activity (global)
# =============================
st.subheader("🕒 Recent Global Activity")
df_reviews["timestamp"] = pd.to_datetime(df_reviews["timestamp"])
st.dataframe(df_reviews.sort_values("timestamp", ascending=False).head(10)[["flashcard_id", "correct", "timestamp"]])

st.write("###")

# =============================
# 📉 Worst Performing Flashcards
# =============================
st.subheader("📉 Flashcards with Most Incorrect Answers")

# Join reviews with flashcard names
df_reviews = pd.merge(df_reviews, df_flashcards[["id", "acronym"]], left_on="flashcard_id", right_on="id", how="left")

# Count incorrect responses per flashcard
wrong_counts = df_reviews[df_reviews["correct"] == 0]["acronym"].value_counts()

if not wrong_counts.empty:
    fig, ax = plt.subplots(figsize=(6, min(10, len(wrong_counts) * 0.6)))
    wrong_counts.sort_values().plot(kind="barh", ax=ax, color="#e74c3c")
    ax.set_xlabel("Number of Incorrect Answers")
    ax.set_ylabel("Flashcard")
    ax.set_title("🚨 Most Missed Flashcards")
    st.pyplot(fig)
else:
    st.info("Nice job! No incorrect answers recorded yet.")
