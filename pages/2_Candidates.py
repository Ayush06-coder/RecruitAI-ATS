import streamlit as st
import requests
import pandas as pd
from auth import is_logged_in, render_sidebar, must_change_password,is_admin
from styles import inject_css

st.set_page_config(page_title="Candidates", page_icon="👥", layout="wide")
inject_css()

if not is_logged_in():
    st.warning("Please login first.")
    st.stop()

render_sidebar()

if must_change_password():
    st.error("You must change your password before accessing this page.")
    st.stop()

API_URL = "http://localhost:8000"

st.markdown("""
<div class="hero">
    <h1>👥 Candidate Database</h1>
    <p class="hero-subtitle">Search, filter and view all parsed candidates</p>
</div>
""", unsafe_allow_html=True)

col_search, col_filter = st.columns([3, 1])

with col_search:
    search_query = st.text_input("", placeholder="🔍 Search by name, email or skill...")

with col_filter:
    skill_options = [
        "Python", "Java", "Machine Learning", "SQL", "MySQL",
        "MongoDB", "Docker", "AWS", "React", "Django", "FastAPI",
        "Git", "NLP", "Deep Learning", "PostgreSQL"
    ]
    selected_skill = st.selectbox("Filter by Skill", options=["All"] + skill_options)

st.divider()

if search_query:
    response = requests.get(f"{API_URL}/candidates", params={"search": search_query})
else:
    response = requests.get(f"{API_URL}/candidates")

if response.status_code == 200:
    data = response.json()
    candidates = data["candidates"]

    if selected_skill != "All":
        candidates = [c for c in candidates if selected_skill.lower() in c["skills"].lower()]

    if not candidates:
        st.warning("No candidates found matching your search.")
    else:
        st.markdown(f"<p style='color:#22d3ee; font-weight:600'>{len(candidates)} candidate(s) found</p>", unsafe_allow_html=True)

        candidate_data = []
        for c in candidates:
            candidate_data.append({
                "Name": c["name"],
                "Email": c["email"],
                "Phone": c["phone"],
                "Skills": c["skills"],
                "Education": c["education"]
            })

        df = pd.DataFrame(candidate_data)
        df.index = df.index + 1
        st.dataframe(df, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="card-title">👤 Candidate Details</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        for c in candidates:
            with st.expander(f"👤 {c['name']} — {c['email']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                    <div class="card">
                        <div class="card-title">Contact Info</div>
                        <p style="color:#a0aec0; margin:0.3rem 0">👤 {c['name']}</p>
                        <p style="color:#a0aec0; margin:0.3rem 0">📧 {c['email']}</p>
                        <p style="color:#a0aec0; margin:0.3rem 0">📞 {c['phone']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    skills_html = "".join([f'<span class="badge badge-purple">{s.strip()}</span>' for s in c['skills'].split(",")])
                    st.markdown(f"""
                    <div class="card">
                        <div class="card-title">🛠️ Skills</div>
                        <div style="margin-top:0.5rem">{skills_html}</div>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="card">
                    <div class="card-title">🎓 Education</div>
                    <p style="color:#a0aec0">{c['education']}</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown(f"""
                <div class="card">
                    <div class="card-title">💼 Experience</div>
                    <p style="color:#a0aec0">{c['experience']}</p>
                </div>
                """, unsafe_allow_html=True)

                if is_admin():
                    st.divider()

                    if st.button(
                        "🗑️ Delete Candidate",
                        key=f"delete_{c['id']}"
                    ):

                        response = requests.delete(
                            f"{API_URL}/candidate/{c['id']}"
                        )

                        if response.status_code == 200:
                            st.success("Candidate deleted successfully.")
                            st.rerun()
                        else:
                            st.error("Failed to delete candidate.")

else:
    st.error("Could not connect to backend. Make sure FastAPI is running.")