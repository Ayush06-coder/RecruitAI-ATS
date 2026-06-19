import streamlit as st
import requests
import pandas as pd
from styles import inject_css
from auth import enforce_access, render_sidebar, get_user_role

st.set_page_config(page_title="Candidates", page_icon="👥", layout="wide")
inject_css()

enforce_access()
render_sidebar()

from config import API_URL

st.markdown("""
<div class="hero">
    <h1>👥 Candidate Database</h1>
    <p class="hero-subtitle">Search, filter and view all parsed candidates</p>
</div>
""", unsafe_allow_html=True)

col_search, col_filter, col_page_size = st.columns([3, 1, 1])

with col_search:
    search_query = st.text_input(
        "",
        placeholder="🔍 Search by name, email or skill..."
    )

with col_filter:
    skill_options = [
        "Python", "Java", "Machine Learning", "SQL", "MySQL",
        "MongoDB", "Docker", "AWS", "React", "Django", "FastAPI",
        "Git", "NLP", "Deep Learning", "PostgreSQL"
    ]
    selected_skill = st.selectbox(
        "Filter by Skill",
        options=["All"] + skill_options
    )

with col_page_size:
    page_size = st.selectbox("Per page", options=[10, 20, 50], index=1)

st.divider()

if "candidate_page" not in st.session_state:
    st.session_state["candidate_page"] = 1

# Reset to page 1 when search or filter changes
if "last_search" not in st.session_state:
    st.session_state["last_search"] = ""
if "last_skill" not in st.session_state:
    st.session_state["last_skill"] = "All"

if search_query != st.session_state["last_search"] or selected_skill != st.session_state["last_skill"]:
    st.session_state["candidate_page"] = 1
    st.session_state["last_search"] = search_query
    st.session_state["last_skill"] = selected_skill

current_page = st.session_state["candidate_page"]

if search_query:
    response = requests.get(
        f"{API_URL}/candidates",
        params={"search": search_query, "page": current_page, "page_size": page_size}
    )
else:
    response = requests.get(
        f"{API_URL}/candidates",
        params={"page": current_page, "page_size": page_size}
    )

if response.status_code == 200:
    data = response.json()
    candidates = data["candidates"]
    total = data.get("total", len(candidates))

    if selected_skill != "All":
        candidates = [
            c for c in candidates
            if selected_skill.lower() in c["skills"].lower()
        ]

    if not candidates:
        st.warning("No candidates found.")
    else:
        total_pages = max(1, -(-total // page_size))  # ceiling division
        st.markdown(
            f"<p style='color:#22d3ee; font-weight:600'>"
            f"{total} candidate(s) total — Page {current_page} of {total_pages}</p>",
            unsafe_allow_html=True
        )

        candidate_data = []
        for c in candidates:
            candidate_data.append({
                "ID": c["id"],
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
        st.markdown(
            '<div class="card-title">👤 Candidate Details</div>',
            unsafe_allow_html=True
        )
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
                    skills_html = "".join([
                        f'<span class="badge badge-purple">{s.strip()}</span>'
                        for s in c['skills'].split(",")
                    ])
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

                # Admin-only delete button
                if get_user_role() == "admin":
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("🗑️ Delete Candidate", key=f"del_{c['id']}", type="primary"):
                        with st.spinner("Deleting..."):
                            del_response = requests.delete(
                                f"{API_URL}/candidates/{c['id']}"
                            )
                        if del_response.status_code == 200:
                            st.success("✅ Candidate deleted successfully")
                            st.rerun()
                        else:
                            st.error("❌ Failed to delete candidate")

        # Pagination controls
        st.markdown("<br>", unsafe_allow_html=True)
        col_prev, col_info, col_next = st.columns([1, 2, 1])
        with col_prev:
            if current_page > 1:
                if st.button("← Previous", use_container_width=True):
                    st.session_state["candidate_page"] -= 1
                    st.rerun()
        with col_info:
            st.markdown(
                f"<p style='text-align:center; color:#64748b; margin-top:0.5rem'>"
                f"Page {current_page} of {total_pages}</p>",
                unsafe_allow_html=True
            )
        with col_next:
            if current_page < total_pages:
                if st.button("Next →", use_container_width=True):
                    st.session_state["candidate_page"] += 1
                    st.rerun()
else:
    st.error("Could not connect to backend.")