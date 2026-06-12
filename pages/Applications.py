import streamlit as st
import requests
import pandas as pd
from styles import inject_css
from auth import render_sidebar

st.set_page_config(page_title="Applications", page_icon="📋", layout="wide")
inject_css()
render_sidebar()
API_URL = "http://localhost:8000"

st.markdown("""
<div class="hero">
    <h1>📋 Applications</h1>
    <p class="hero-subtitle">Review and manage all candidate applications</p>
</div>
""", unsafe_allow_html=True)

jobs_response = requests.get(f"{API_URL}/jobs")
jobs = jobs_response.json().get("jobs", [])

if not jobs:
    st.info("No jobs posted yet. Post a job from the Admin panel.")
    st.stop()

job_options = {f"#{j['id']} — {j['title']} ({j['status']})": j["id"] for j in jobs}
selected_label = st.selectbox("Select Job", options=list(job_options.keys()))
selected_job_id = job_options[selected_label]

st.divider()

apps_response = requests.get(f"{API_URL}/jobs/{selected_job_id}/applications")
applications = apps_response.json().get("applications", [])

if not applications:
    st.info("No applications yet for this job.")
    st.stop()

st.markdown(f"<p style='color:#22d3ee; font-weight:600'>{len(applications)} application(s) — ranked by match score</p>", unsafe_allow_html=True)

for i, app in enumerate(applications):
    medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"#{i+1}"
    status_colors = {
        "Applied": "badge-purple",
        "Shortlisted": "badge-green",
        "Rejected": "badge-red",
        "Interview Scheduled": "badge-yellow"
    }
    status_color = status_colors.get(app["status"], "badge-purple")
    score_color = "#22d3ee" if app["match_score"] >= 70 else "#f59e0b" if app["match_score"] >= 40 else "#ef4444"

    st.markdown(f"""
    <div class="rank-card">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem">
            <div style="display:flex; align-items:center; gap:1rem">
                <div style="font-size:1.5rem">{medal}</div>
                <div>
                    <div style="font-size:1.1rem; font-weight:700; color:#e2e8f0">{app['name']}</div>
                    <div style="color:#64748b; font-size:0.85rem">{app['email']} | Applied: {app['applied_date']}</div>
                </div>
            </div>
            <div style="display:flex; align-items:center; gap:1rem">
                <div style="font-size:1.5rem; font-weight:700; color:{score_color}">{app['match_score']}%</div>
                <span class="badge {status_color}">{app['status']}</span>
            </div>
        </div>
        <div style="margin-top:1rem; display:flex; gap:2rem; flex-wrap:wrap">
            <div>
                <div style="color:#64748b; font-size:0.75rem">SKILLS</div>
                <div style="color:#e2e8f0; font-weight:600">{app['skills_score']}%</div>
            </div>
            <div>
                <div style="color:#64748b; font-size:0.75rem">EXPERIENCE</div>
                <div style="color:#e2e8f0; font-weight:600">{app['experience_score']}%</div>
            </div>
            <div>
                <div style="color:#64748b; font-size:0.75rem">CERTIFICATIONS</div>
                <div style="color:#e2e8f0; font-weight:600">{app['certifications_score']}%</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_s, col_i, col_r, col_space = st.columns([1, 1.5, 1, 3])

    with col_s:
        if st.button("⭐ Shortlist", key=f"short_{app['id']}"):
            requests.put(f"{API_URL}/applications/{app['id']}", json={"status": "Shortlisted"})
            st.rerun()
    with col_i:
        if st.button("📅 Interview", key=f"interview_{app['id']}"):
            requests.put(f"{API_URL}/applications/{app['id']}", json={"status": "Interview Scheduled"})
            st.rerun()
    with col_r:
        if st.button("❌ Reject", key=f"reject_{app['id']}"):
            requests.put(f"{API_URL}/applications/{app['id']}", json={"status": "Rejected"})
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)