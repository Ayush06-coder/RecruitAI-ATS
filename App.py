import streamlit as st
from styles import inject_css
from auth import is_logged_in, get_user_role

st.set_page_config(
    page_title="RecruitAI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_css()

# ---------------- DEFINE PAGES ----------------

# Public pages (candidate — no login)
home_page = st.Page("App.py", title="🏠 Home", icon="🏠", default=True)
apply_page = st.Page("pages/public/Apply.py", title="📤 Apply", icon="📤")
track_page = st.Page("pages/public/Track.py", title="🔍 Track", icon="🔍")

# Login page
login_page = st.Page("pages/Login.py", title="🔐 Login", icon="🔐")

# Company pages (require login)
dashboard_page = st.Page("pages/company/Dashboard.py", title="📊 Dashboard", icon="📊")
applications_page = st.Page("pages/company/Applications.py", title="📋 Applications", icon="📋")
candidates_page = st.Page("pages/company/Candidates.py", title="👥 Candidates", icon="👥")
jd_matching_page = st.Page("pages/company/JD_Matching.py", title="🎯 JD Matching", icon="🎯")
analytics_page = st.Page("pages/company/Analytics.py", title="📊 Analytics", icon="📊")
change_password_page = st.Page("pages/company/Change_Password.py", title="🔑 Change Password", icon="🔑")

# Admin-only page
admin_page = st.Page("pages/company/Admin.py", title="🛠️ Admin", icon="🛠️")

# ---------------- DETERMINE NAVIGATION BASED ON ROLE ----------------

if not is_logged_in():
    # Candidate — public pages only
    pages = [home_page, apply_page, track_page, login_page]

elif get_user_role() == "admin":
    # Admin — all company pages + admin
    pages = [
        dashboard_page, applications_page, candidates_page,
        jd_matching_page, analytics_page, admin_page, change_password_page
    ]

elif get_user_role() == "user":
    # User — company pages except admin
    pages = [
        dashboard_page, applications_page, candidates_page,
        jd_matching_page, analytics_page, change_password_page
    ]

else:
    # Fallback — public pages
    pages = [home_page, apply_page, track_page, login_page]

# ---------------- RENDER NAVIGATION ----------------

nav = st.navigation(pages)
nav.run()

# ---------------- HOME PAGE CONTENT (only when on home) ----------------

if not is_logged_in():
    import requests
    
    API_URL = "http://localhost:8000"
    
    st.markdown("""
    <div class="hero" style="padding: 4rem 2rem">
        <h1>📄 RecruitAI</h1>
        <p class="hero-subtitle" style="font-size:1.2rem">
            Intelligent Resume Parsing & Candidate Matching Platform
        </p>
        <p style="color:#0e3a45; margin-top:1rem; font-size:0.9rem">
            Powered by Python · FastAPI · spaCy NLP
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📤</div>
            <div class="feature-title">Easy Apply</div>
            <div class="feature-desc">Upload your resume and apply to jobs in seconds</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <div class="feature-title">AI Matching</div>
            <div class="feature-desc">Smart NLP matching against job requirements</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">Instant Score</div>
            <div class="feature-desc">Get your match score immediately after applying</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🏆</div>
            <div class="feature-title">Fair Ranking</div>
            <div class="feature-desc">Ranked fairly based on skills, experience and certifications</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    
    # Open jobs section
    st.markdown("""
    <div class="card-title" style="font-size:1.3rem; margin-bottom:1rem">
        💼 Current Openings
    </div>
    """, unsafe_allow_html=True)
    
    try:
        response = requests.get(f"{API_URL}/jobs")
        jobs = response.json().get("jobs", [])
        open_jobs = [j for j in jobs if j["status"] == "open"]
    except:
        open_jobs = []
    
    if not open_jobs:
        st.info("No open positions at the moment. Check back soon.")
    else:
        st.markdown(
            f"<p style='color:#22d3ee; font-weight:600; margin-bottom:1.5rem'>"
            f"{len(open_jobs)} open position(s)</p>",
            unsafe_allow_html=True
        )
        
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
                <div style="display:flex; justify-content:space-between;
                            align-items:flex-start; flex-wrap:wrap; gap:1rem">
                    <div>
                        <div style="font-size:1.2rem; font-weight:700;
                                    color:#e2e8f0">{job['title']}</div>
                        <div style="color:#64748b; font-size:0.85rem; margin-top:0.3rem">
                            🏢 {job['department']} &nbsp;|&nbsp;
                            📍 {job['location']} &nbsp;|&nbsp;
                            🕐 {job['experience']} &nbsp;|&nbsp;
                            📅 {job['posted_date']}
                        </div>
                    </div>
                    <span class="badge badge-green">🟢 Open</span>
                </div>
                <div style="margin-top:0.8rem; color:#a0aec0;
                            font-size:0.9rem; line-height:1.6">
                    {job['description'][:250]}{'...' if len(job['description']) > 250 else ''}
                </div>
                <div style="margin-top:1rem">
                    <div style="color:#64748b; font-size:0.75rem;
                                margin-bottom:0.4rem; text-transform:uppercase;
                                letter-spacing:0.05em">Required Skills</div>
                    {skills_html}
                </div>
                {'<<div style="margin-top:0.8rem"><div style="color:#64748b; font-size:0.75rem; margin-bottom:0.4rem; text-transform:uppercase; letter-spacing:0.05em">Required Certifications</div>' + certs_html + '</div>' if certs_html else ''}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Apply for {job['title']}", key=f"apply_{job['id']}"):
                st.session_state["apply_job_id"] = job["id"]
                st.session_state["apply_job_title"] = job["title"]
                st.switch_page("pages/public/Apply.py")
            
            st.markdown("<br>", unsafe_allow_html=True)
    
    st.divider()
    
    # Company login CTA
    st.markdown("""
    <div style="text-align:center; padding:1.5rem">
        <p style="color:#64748b; font-size:0.9rem">
            Are you a recruiter or part of the hiring team?
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🔐 Company Login", use_container_width=True):
            st.switch_page("pages/Login.py")