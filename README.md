# 📚 Flashcard App
A web-based acronym flashcard app using **Streamlit** and **SQLite** with multi-user support, statistics tracking, and configuration interface.

---

## ✅ Features
- Interactive flashcard quiz (reveal + self-assess)
- User-based performance tracking with statistics
- Admin/config panel to manage flashcards and users
- Import/export flashcards via CSV

---

## 🚀 Getting Started

### 1. Clone or download the project
Place yourself inside the project folder:
```powershell
cd flashcard_app
```

### 2. Create the Conda environment
```powershell
conda env create -f environment.yml
```

### 3. Activate the environment
```powershell
conda activate flashcard-app
```

### 4. Launch the app with Streamlit
```powershell
streamlit run app.py
```

---

## 📁 Folder Structure
```plaintext
flashcard_app/
├── app.py                  # Entry point (Streamlit launcher)
├── database.py             # DB schema and setup logic
├── environment.yml         # Conda environment definition
├── README.md               # This file
├── data/
│   └── flashcards.db       # SQLite DB (auto-generated)
└── pages/
    ├── 1_Flashcards.py     # Flashcard quiz interface
    ├── 2_Statistics.py     # User statistics
    └── 3_Configuration.py  # Admin panel
```

---

## 📝 CSV Format for Importing Flashcards
When uploading CSVs, they must follow this structure:

```csv
acronym,meaning
API,Application Programming Interface
HTML,HyperText Markup Language
```

---

## 💡 Ideas for Extension
- Add flashcard categories or difficulty levels
- Implement login with password
- Use spaced repetition algorithms
- Deploy to [Streamlit Cloud](https://streamlit.io/cloud)

---

Made with ❤️ using Python, Streamlit and SQLite.
