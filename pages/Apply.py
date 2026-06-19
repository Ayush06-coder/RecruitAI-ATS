import streamlit as st
import requests
from styles import inject_css

st.set_page_config(page_title="Apply", page_icon="📤", layout="wide")
inject_css()

from config import API_URL

# ---------------- CHECK JOB SELECTED ----------------

if "apply_job_id" not in st.session_state:
    st.warning("No job selected. Please select a job from the listings.")
    if st.button("← Back to Jobs"):
        st.switch_page("pages/Home.py")
    st.stop()

job_id = st.session_state["apply_job_id"]
job_title = st.session_state.get("apply_job_title", "")

# ---------------- HEADER ----------------

st.markdown(f"""
<h2 style="color: #5eead4;">📤 Apply for {job_title}</h2>
<p>Fill in your details and upload your resume to apply</p>
""", unsafe_allow_html=True)

if st.button("← Back to Jobs"):
    st.switch_page("pages/Home.py")

st.divider()

# ---------------- APPLICATION FORM ----------------

if "application_submitted" not in st.session_state:
    st.session_state["application_submitted"] = False

if not st.session_state["application_submitted"]:

    st.markdown('<h4 style="color: #5eead4;">👤 Your Information</h4>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        candidate_name = st.text_input("Full Name *", placeholder="e.g. John Doe")
    with col2:
        candidate_email = st.text_input("Email Address *", placeholder="e.g. name@email.com")
    with col3:
        candidate_phone = st.text_input("Phone Number *", placeholder="e.g. +91 98765 43210")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<h4 style="color: #5eead4;">📄 Upload Resume</h4>', unsafe_allow_html=True)
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

    # Tracking link — uses FRONTEND_URL env var if set, else localhost
    import os
    base_url = os.getenv("FRONTEND_URL", "http://localhost:8501").rstrip("/")
    tracking_url = f"{base_url}/Track?email={result.get('email', '')}"

    st.markdown(f"""
    <div style="background-color: #0f2a2e; padding: 20px; border-radius: 12px; border: 1px solid #1e3a3f; margin-bottom: 20px;">
        <h4 style="color: #5eead4; margin-top: 0;">🔗 Track Your Application</h4>
        <p>Bookmark this link to check your application status anytime:</p>
        <div style="background-color: #0a1f23; padding: 12px; border-radius: 8px; font-family: monospace; color: #5eead4;">
            {tracking_url}
        </div>
        <p style="margin-bottom: 0; color: #94a3b8;"><small>💡 Save this link — you will need your email to track your status</small></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align: center; padding: 30px; background-color: #0f2a2e; border-radius: 12px; border: 1px solid #1e3a3f;">
        <div style="font-size: 40px; margin-bottom: 10px;">🎉</div>
        <h3 style="color: #ffffff; margin-bottom: 10px;">Thank you, {result.get('name', '')}!</h3>
        <p style="color: #94a3b8; margin-bottom: 0;">
            Your application for <strong style="color: #5eead4;">{job_title}</strong> 
            has been received. Our team will review it shortly.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; background-color: #0f2a2e; border-radius: 8px;">
            <p style="color: #94a3b8; font-size: 12px; margin-bottom: 5px;">OVERALL MATCH</p>
            <h2 style="color: #5eead4; margin: 0;">{result.get('match_score', 0)}%</h2>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; background-color: #0f2a2e; border-radius: 8px;">
            <p style="color: #94a3b8; font-size: 12px; margin-bottom: 5px;">SKILLS MATCH</p>
            <h2 style="color: #5eead4; margin: 0;">{result.get('skills_score', 0)}%</h2>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; background-color: #0f2a2e; border-radius: 8px;">
            <p style="color: #94a3b8; font-size: 12px; margin-bottom: 5px;">EXPERIENCE</p>
            <h2 style="color: #5eead4; margin: 0;">{result.get('experience_score', 0)}%</h2>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; background-color: #0f2a2e; border-radius: 8px;">
            <p style="color: #94a3b8; font-size: 12px; margin-bottom: 5px;">CERTIFICATIONS</p>
            <h2 style="color: #5eead4; margin: 0;">{result.get('certifications_score', 0)}%</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.progress(result.get("match_score", 0) / 100)

    if st.button("← View More Jobs"):
        st.session_state["application_submitted"] = False
        st.session_state["apply_job_id"] = None
        st.session_state["application_result"] = None
        st.switch_page("pages/Home.py")