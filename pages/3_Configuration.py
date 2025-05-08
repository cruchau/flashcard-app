import streamlit as st
import sqlite3
import pandas as pd
from database import db_path, hash_password


conn = sqlite3.connect(db_path)
cursor = conn.cursor()

st.set_page_config(page_title="Flashcard App", layout="wide")

# Layout: Title (left) | Counter & Button (right)
col_title, col_stats = st.columns([3, 2])

with col_title:
    st.title("⚙️ Flashcard Configuration")

with col_stats:
    flashcard_count = cursor.execute("SELECT COUNT(*) FROM flashcards").fetchone()[0]
    st.markdown(
        f"""
        <div style="
            background-color:#f0f2f6;
            border: 1px solid #ccc;
            border-radius: 12px;
            padding: 10px 15px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style='font-size:14px;'>🧾 Total Flashcards</div>
            <div style='font-size:28px; font-weight:600; color:#4CAF50;'>{flashcard_count}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

    st.markdown(
        "<div style='text-align: center;'>"
        "<a href='https://w.amazon.com/bin/view/Acronym_Central' style='text-decoration: none;'>"
        "<button style='background-color: #4CAF50; color: white; padding: 6px 12px; "
        "border: none; border-radius: 6px; font-size: 14px; cursor: pointer;'>🔗 Go to Acronyms wiki</button>"
        "</a></div>",
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)




st.write("###")

# ---------- ADD NEW ----------
st.subheader("➕ Add New Flashcard")
acronym = st.text_input("Acronym")
meaning = st.text_input("Meaning")

if st.button("Add Flashcard") and acronym and meaning:
    cursor.execute(
        "INSERT INTO flashcards (acronym, meaning) VALUES (?, ?)",
        (acronym, meaning) #, category, difficulty)
    )
    conn.commit()
    st.success("Flashcard added.")

st.write("###")

# ---------- MODIFY EXISTING ----------
st.subheader("✏️ Modify Flashcard")

flashcards = cursor.execute("SELECT * FROM flashcards").fetchall()
if flashcards:
    flashcard_df = pd.DataFrame(flashcards, columns=["id", "acronym", "meaning"])
    selected = st.selectbox("Select Flashcard to Modify", flashcard_df["acronym"] + " (ID: " + flashcard_df["id"].astype(str) + ")")
    selected_id = int(selected.split("ID: ")[-1][:-1])
    selected_row = flashcard_df[flashcard_df["id"] == selected_id].iloc[0]

    new_acronym = st.text_input("New Acronym", value=selected_row["acronym"], key="edit_acronym")
    new_meaning = st.text_input("New Meaning", value=selected_row["meaning"], key="edit_meaning")

    if st.button("Save Changes"):
        cursor.execute(
            "UPDATE flashcards SET acronym = ?, meaning = ?  WHERE id = ?",
            (new_acronym, new_meaning, selected_id)
        )
        conn.commit()
        st.success("Flashcard updated.")

st.write("###")

# ---------- DELETE ----------
st.subheader("🗑️ Delete Flashcard")
flashcards = cursor.execute("SELECT id, acronym FROM flashcards").fetchall()

if flashcards:
    flashcard_dict = {f"{fid}: {acronym}": fid for fid, acronym in flashcards}
    to_delete = st.selectbox("Select flashcard to delete", list(flashcard_dict.keys()))

    if st.button("Delete Selected Flashcard"):
        cursor.execute("DELETE FROM flashcards WHERE id = ?", (flashcard_dict[to_delete],))
        conn.commit()
        st.success("Flashcard deleted.")

st.write("###")


# ---------- EXPORT FLASHCARDS ----------
st.subheader("📤 Export Flashcards to CSV")
df_flashcards = pd.read_sql_query("SELECT * FROM flashcards", conn)
st.download_button(
    label="Download CSV",
    data=df_flashcards.to_csv(index=False).encode("utf-8"),
    file_name="flashcards_export.csv",
    mime="text/csv"
)

st.write("###")


# Import Flashcards
st.subheader("📥 Import Flashcards from CSV")
uploaded = st.file_uploader("Upload CSV", type=["csv"])
if uploaded:
    try:
        df_new = pd.read_csv(uploaded)

        required_cols = {"acronym", "meaning"}
        if not required_cols.issubset(df_new.columns):
            st.error("CSV must include 'acronym' and 'meaning' columns.")
        else:
            inserted = 0
            for _, row in df_new.iterrows():
                if pd.notna(row["acronym"]) and pd.notna(row["meaning"]):
                    cursor.execute(
                        "INSERT INTO flashcards (acronym, meaning) VALUES (?, ?)",
                        (row["acronym"], row["meaning"])
                    )
                    inserted += 1
            conn.commit()
            st.success(f"{inserted} flashcards imported.")
    except Exception as e:
        st.error(f"Failed to import: {e}")


st.write("###")

# # ---------- USER MANAGEMENT ----------
# st.subheader("👤 Add New User")
# new_user = st.text_input("New Username")
# new_pass = st.text_input("Password", type="password")

# if st.button("Create User"):
#     try:
#         with sqlite3.connect(db_path) as conn:
#             cursor = conn.cursor()
#             cursor.execute("INSERT INTO users (name, password_hash) VALUES (?, ?)",
#                            (new_user, hash_password(new_pass)))
#             conn.commit()
#             st.success("User created.")
#     except sqlite3.IntegrityError:
#         st.error("Username already exists.")
        
