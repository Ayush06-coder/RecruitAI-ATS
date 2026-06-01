import streamlit as st
from auth import login_page, logout, is_logged_in

st.set_page_config(
    page_title="Intelligent Resume Parser",
    page_icon="📄",
    layout="wide"
)

if not is_logged_in():
    login_page()
    st.stop()

# ---------------- SIDEBAR LOGOUT ----------------
with st.sidebar:
    st.markdown(f"👤 Logged in as **{st.session_state['username']}**")
    if st.button("Logout"):
        logout()

# ---------------- HOME PAGE ----------------
st.title("📄 Intelligent Resume Parser using NLP")

st.markdown("""
Welcome to the **Intelligent Resume Parser** — a recruiter tool built using Python, FastAPI, Streamlit, and spaCy NLP.

### What this system does:
- 📤 **Upload** resumes in PDF or DOCX format
- 🧠 **Extracts** Name, Email, Phone, Skills, Education, Experience using NLP
- 👥 **Stores** all candidates in a database
- 🎯 **Matches** candidates against a job description
- 🏆 **Ranks** candidates by match score

### How to use:
1. Go to **Upload Resume** to parse a new resume
2. Go to **Candidates** to view all stored candidates
3. Go to **JD Matching** to match and rank candidates

---
*Built using Python · FastAPI · Streamlit · spaCy · SQLite*
""")