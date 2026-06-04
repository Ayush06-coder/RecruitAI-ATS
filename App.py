import streamlit as st
from auth import login_page, is_logged_in, render_sidebar, must_change_password
from styles import inject_css

st.set_page_config(
    page_title="Intelligent Resume Parser",
    page_icon="📄",
    layout="wide"
)

inject_css()

if not is_logged_in():
    login_page()
    st.stop()

render_sidebar()

if must_change_password():
    st.error("You must change your password before accessing this page.")
    st.info("Open **Change Password** from the sidebar.")
    st.stop()

# ---------------- HOME PAGE ----------------

st.markdown("""
<div class="hero">
    <h1>📄 Intelligent Resume Parser</h1>
    <p class="hero-subtitle">AI-powered recruitment tool built with Python, FastAPI, Streamlit and spaCy NLP</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📤</div>
        <div class="feature-title">Upload Resumes</div>
        <div class="feature-desc">Upload PDF or DOCX resumes with instant NLP parsing</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">👥</div>
        <div class="feature-title">Candidate Database</div>
        <div class="feature-desc">Search and filter all parsed candidates instantly</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <div class="feature-title">JD Matching</div>
        <div class="feature-desc">Match and rank candidates against any job description</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Analytics</div>
        <div class="feature-desc">Visual insights across all candidates and skills</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="card">
    <div class="card-title">🧠 What this system does</div>
    <p style="color: #a0aec0; margin: 0.5rem 0; line-height: 1.8;">
        📤 <strong style="color: #818cf8;">Upload</strong> resumes in PDF or DOCX format<br>
        🧠 <strong style="color: #818cf8;">Extracts</strong> Name, Email, Phone, Skills, Education, Experience using NLP<br>
        👥 <strong style="color: #818cf8;">Stores</strong> all candidates in a searchable database<br>
        🎯 <strong style="color: #818cf8;">Matches</strong> candidates against a job description<br>
        🏆 <strong style="color: #818cf8;">Ranks</strong> candidates by match score
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
    <div class="card-title">🚀 How to use</div>
    <p style="color: #a0aec0; margin: 0.5rem 0; line-height: 1.8;">
        1. Go to <strong style="color: #818cf8;">Upload Resume</strong> to parse a new resume<br>
        2. Go to <strong style="color: #818cf8;">Candidates</strong> to view all stored candidates<br>
        3. Go to <strong style="color: #818cf8;">JD Matching</strong> to match and rank candidates<br>
        4. Go to <strong style="color: #818cf8;">Analytics</strong> to see hiring insights
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p style="text-align: center; color: #2d2d5e; font-size: 0.8rem; margin-top: 2rem;">
    Built with Python · FastAPI · Streamlit · spaCy · SQLite
</p>
""", unsafe_allow_html=True)