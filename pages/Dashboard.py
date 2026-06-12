import streamlit as st
import requests
from styles import inject_css
from auth import enforce_access, render_sidebar

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
inject_css()

enforce_access()
render_sidebar()

API_URL = "http://localhost:8000"

st.markdown("""
<div class="hero">
    <h1>📊 Recruiter Dashboard</h1>
    <p class="hero-subtitle">Overview of all jobs and applications</p>
</div>
""", unsafe_allow_html=True)

# ---------------- FETCH DATA ----------------

try:
    jobs_response = requests.get(f"{API_URL}/jobs")
    jobs = jobs_response.json().get("jobs", [])
    candidates_response = requests.get(f"{API_URL}/candidates")
    candidates = candidates_response.json().get("candidates", [])
except:
    jobs = []
    candidates = []

open_jobs = [j for j in jobs if j["status"] == "open"]
closed_jobs = [j for j in jobs if j["status"] == "closed"]

# ---------------- METRICS ----------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Jobs</div>
        <div class="metric-value">{len(jobs)}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Open Positions</div>
        <div class="metric-value">{len(open_jobs)}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Candidates</div>
        <div class="metric-value">{len(candidates)}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    total_apps = 0
    for job in jobs:
        try:
            apps_response = requests.get(f"{API_URL}/jobs/{job['id']}/applications")
            total_apps += len(apps_response.json().get("applications", []))
        except:
            pass

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Applications</div>
        <div class="metric-value">{total_apps}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------------- JOBS SUMMARY ----------------

st.markdown('<div class="card-title" style="font-size:1.1rem">💼 Active Job Postings</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

if not open_jobs:
    st.info("No open positions. Post a job from the Admin panel.")
else:
    for job in open_jobs:
        try:
            apps_response = requests.get(f"{API_URL}/jobs/{job['id']}/applications")
            app_count = len(apps_response.json().get("applications", []))
        except:
            app_count = 0

        skills_html = "".join([
            f'<span class="badge badge-purple">{s.strip()}</span>'
            for s in job["required_skills"].split(",")[:4] if s.strip()
        ])

        st.markdown(f"""
        <div class="card">
            <div style="display:flex; justify-content:space-between;
                        align-items:center; flex-wrap:wrap; gap:1rem">
                <div>
                    <div style="font-size:1.1rem; font-weight:700;
                                color:#e2e8f0">{job['title']}</div>
                    <div style="color:#64748b; font-size:0.85rem; margin-top:0.3rem">
                        🏢 {job['department']} &nbsp;|&nbsp;
                        📍 {job['location']} &nbsp;|&nbsp;
                        📅 {job['posted_date']}
                    </div>
                    <div style="margin-top:0.5rem">{skills_html}</div>
                </div>
                <div style="text-align:center">
                    <div style="font-size:2rem; font-weight:700;
                                color:#22d3ee">{app_count}</div>
                    <div style="color:#64748b; font-size:0.75rem">Applications</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)