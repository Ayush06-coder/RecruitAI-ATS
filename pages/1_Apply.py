import streamlit as st
import requests
from styles import inject_css

st.set_page_config(
    page_title="Apply",
    page_icon="📤",
    layout="wide"
)

inject_css()

API_URL = "http://localhost:8000"

# ---------------- CHECK JOB SELECTED ----------------

if "apply_job_id" not in st.session_state:
    st.warning("No job selected. Please select a job from the listings.")
    if st.button("← Back to Jobs"):
        st.switch_page("App.py")
    st.stop()

job_id = st.session_state["apply_job_id"]
job_title = st.session_state.get("apply_job_title", "")

# ---------------- HEADER ----------------

st.markdown(f"""
<div class="hero">
    <h1>📤 Apply for {job_title}</h1>
    <p class="hero-subtitle">
        Fill in your details and upload your resume to apply
    </p>
</div>
""", unsafe_allow_html=True)

if st.button("← Back to Jobs"):
    st.switch_page("App.py")

st.divider()

# ---------------- APPLICATION FORM ----------------

if "application_submitted" not in st.session_state:
    st.session_state["application_submitted"] = False

if not st.session_state["application_submitted"]:

    st.markdown('<div class="card-title" style="font-size:1.1rem">👤 Your Information</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        candidate_name = st.text_input("Full Name *", placeholder="e.g. Ayush Sawhney")
    with col2:
        candidate_email = st.text_input("Email Address *", placeholder="e.g. ayush@gmail.com")
    with col3:
        candidate_phone = st.text_input("Phone Number *", placeholder="e.g. 9810469256")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="card-title" style="font-size:1.1rem">📄 Upload Resume</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload your resume (PDF or DOCX, max 200MB)",
        type=["pdf", "docx"]
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Submit Application", use_container_width=False):

        if not candidate_name or not candidate_email or not candidate_phone:
            st.error("Please fill in all required fields.")
        elif not uploaded_file:
            st.error("Please upload your resume.")
        else:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            if file_size_mb > 200:
                st.error(f"❌ File too large — {file_size_mb:.1f}MB. Max 200MB.")
            else:
                with st.spinner("Submitting your application..."):
                    response = requests.post(
                        f"{API_URL}/jobs/{job_id}/apply",
                        files={
                            "file": (
                                uploaded_file.name,
                                uploaded_file,
                                uploaded_file.type
                            )
                        },
                        data={
                            "candidate_name": candidate_name,
                            "candidate_email": candidate_email,
                            "candidate_phone": candidate_phone
                        }
                    )

                if response.status_code == 200:
                    data = response.json()
                    if "error" in data:
                        st.error(f"❌ {data['error']}")
                    else:
                        st.session_state["application_result"] = data
                        st.session_state["application_submitted"] = True
                        st.rerun()
                else:
                    st.error("Something went wrong. Please try again.")

# ---------------- SUCCESS PAGE ----------------

else:
    result = st.session_state.get("application_result", {})

    st.success("✅ Application submitted successfully!")

    st.markdown(f"""
    <div class="card" style="border-color:#10b981; text-align:center; padding:2rem">
        <div style="font-size:2rem">🎉</div>
        <div style="font-size:1.3rem; font-weight:700; color:#e2e8f0; margin-top:0.5rem">
            Thank you, {result.get('name', '')}!
        </div>
        <div style="color:#64748b; margin-top:0.5rem">
            Your application for <strong style="color:#22d3ee">{job_title}</strong>
            has been received. Our team will review it shortly.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Overall Match</div>
            <div class="metric-value">{result.get('match_score', 0)}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Skills Match</div>
            <div class="metric-value">{result.get('skills_score', 0)}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Experience</div>
            <div class="metric-value">{result.get('experience_score', 0)}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Certifications</div>
            <div class="metric-value">{result.get('certifications_score', 0)}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.progress(result.get("match_score", 0) / 100)

    if st.button("← View More Jobs"):
        st.session_state["application_submitted"] = False
        st.session_state["apply_job_id"] = None
        st.session_state["application_result"] = None
        st.switch_page("App.py")