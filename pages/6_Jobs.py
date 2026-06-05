import streamlit as st
import requests
from auth import is_logged_in, render_sidebar, must_change_password
from styles import inject_css

st.set_page_config(page_title="Jobs", page_icon="💼", layout="wide")
inject_css()

if not is_logged_in():
    st.warning("Please login first.")
    st.stop()

render_sidebar()

if must_change_password():
    st.error("You must change your password before accessing this page.")
    st.stop()

API_URL = "http://localhost:8000"

# ---------------- SESSION STATE ----------------

if "applying_job_id" not in st.session_state:
    st.session_state["applying_job_id"] = None

if "application_result" not in st.session_state:
    st.session_state["application_result"] = None

# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <h1>💼 Job Openings</h1>
    <p class="hero-subtitle">Browse open positions and apply with your resume</p>
</div>
""", unsafe_allow_html=True)

# ---------------- FETCH JOBS ----------------

response = requests.get(f"{API_URL}/jobs")

if response.status_code != 200:
    st.error("Could not connect to backend. Make sure FastAPI is running.")
    st.stop()

jobs = response.json().get("jobs", [])
open_jobs = [j for j in jobs if j["status"] == "open"]

if not open_jobs:
    st.info("No open positions at the moment. Check back later.")
    st.stop()

st.markdown(f"<p style='color:#22d3ee; font-weight:600'>{len(open_jobs)} open position(s)</p>", unsafe_allow_html=True)
st.divider()

# ---------------- JOB LISTINGS ----------------

for job in open_jobs:

    skills_html = "".join([
        f'<span class="badge badge-purple">{s.strip()}</span>'
        for s in job["required_skills"].split(",") if s.strip()
    ])

    certs_html = "".join([
        f'<span class="badge badge-yellow">{c.strip()}</span>'
        for c in job["required_certifications"].split(",") if c.strip()
    ]) if job["required_certifications"] else ""

    st.markdown(f"""
    <div class="card">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:1rem">
            <div>
                <div style="font-size:1.3rem; font-weight:700; color:#e2e8f0">{job['title']}</div>
                <div style="color:#64748b; font-size:0.9rem; margin-top:0.3rem">
                    🏢 {job['department']} &nbsp;|&nbsp;
                    📍 {job['location']} &nbsp;|&nbsp;
                    🕐 {job['experience']} years &nbsp;|&nbsp;
                    📅 {job['posted_date']}
                </div>
            </div>
            <span class="badge badge-green">🟢 Open</span>
        </div>

        <div style="margin-top:1rem; color:#a0aec0; font-size:0.9rem; line-height:1.6">
            {job['description'][:200]}{'...' if len(job['description']) > 200 else ''}
        </div>

        <div style="margin-top:1rem">
            <div style="color:#64748b; font-size:0.8rem; margin-bottom:0.3rem">REQUIRED SKILLS</div>
            {skills_html}
        </div>

        {'<div style="margin-top:0.8rem"><div style="color:#64748b; font-size:0.8rem; margin-bottom:0.3rem">REQUIRED CERTIFICATIONS</div>' + certs_html + '</div>' if certs_html else ''}
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button(f"Apply Now", key=f"apply_{job['id']}"):
            st.session_state["applying_job_id"] = job["id"]
            st.session_state["application_result"] = None
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

# ---------------- APPLY SECTION ----------------

if st.session_state["applying_job_id"]:

    job_id = st.session_state["applying_job_id"]
    job_response = requests.get(f"{API_URL}/jobs/{job_id}")
    job = job_response.json()

    st.divider()
    st.markdown(f"""
    <div class="card" style="border-color:#0891b2">
        <div class="card-title">📤 Apply for — {job['title']}</div>
        <p style="color:#64748b; font-size:0.9rem">Upload your resume to apply. Your profile will be automatically matched against this role.</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx"],
        key="job_application_file"
    )

    col_apply, col_cancel = st.columns([1, 5])

    with col_apply:
        if st.button("Submit Application") and uploaded_file:
            with st.spinner("Submitting application..."):
                response = requests.post(
                    f"{API_URL}/jobs/{job_id}/apply",
                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file,
                            uploaded_file.type
                        )
                    }
                )

            if response.status_code == 200:
                data = response.json()
                if "error" in data:
                    st.error(f"❌ {data['error']}")
                else:
                    st.session_state["application_result"] = data
                    st.session_state["applying_job_id"] = None
                    st.rerun()
            else:
                st.error("Something went wrong. Please try again.")

    with col_cancel:
        if st.button("Cancel"):
            st.session_state["applying_job_id"] = None
            st.rerun()

# ---------------- APPLICATION RESULT ----------------

if st.session_state["application_result"]:
    result = st.session_state["application_result"]

    st.divider()
    st.success(f"✅ Application submitted successfully!")

    st.markdown(f"""
    <div class="card" style="border-color:#10b981">
        <div class="card-title">🎯 Your Match Results</div>
        <div style="margin-top:1rem">
            <div style="font-size:1.1rem; color:#e2e8f0; font-weight:600">{result['name']} — {result['email']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Overall Match</div>
            <div class="metric-value">{result['match_score']}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Skills Match</div>
            <div class="metric-value">{result['skills_score']}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Experience Match</div>
            <div class="metric-value">{result['experience_score']}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Certifications</div>
            <div class="metric-value">{result['certifications_score']}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.progress(result["match_score"] / 100)

    matched_html = "".join([f'<span class="badge badge-green">{s}</span>' for s in result['matched_skills']]) if result['matched_skills'] else "<span style='color:#64748b'>None</span>"
    missing_html = "".join([f'<span class="badge badge-red">{s}</span>' for s in result['missing_skills']]) if result['missing_skills'] else "<span style='color:#64748b'>None</span>"

    st.markdown(f"""
    <div class="card">
        <p style="margin:0.3rem 0">✅ <strong style="color:#22d3ee">Matched Skills:</strong> {matched_html}</p>
        <p style="margin:0.3rem 0">❌ <strong style="color:#ef4444">Missing Skills:</strong> {missing_html}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("View More Jobs"):
        st.session_state["application_result"] = None
        st.rerun()