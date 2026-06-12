import streamlit as st
import pandas as pd
import requests
from auth import (
    enforce_access,
    render_sidebar,
    get_users_for_admin,
    create_user_by_admin,
    force_reset_password_by_admin,
    remove_user_by_admin,
)
from styles import inject_css

st.set_page_config(page_title="Admin Panel", page_icon="🛠️", layout="wide")
inject_css()

enforce_access(admin_only=True)
render_sidebar()

API_URL = "http://localhost:8000"

st.markdown("""
<div class="hero">
    <h1>🛠️ Admin Panel</h1>
    <p class="hero-subtitle">Manage users, job postings and applications</p>
</div>
""", unsafe_allow_html=True)

# ---------------- TABS ----------------

tab1, tab2, tab3 = st.tabs(["👥 User Management", "💼 Job Management", "📋 Applications"])

# ============ TAB 1 — USER MANAGEMENT ============

with tab1:

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="card-title" style="font-size:1.1rem">➕ Add New User</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        new_username = st.text_input("Username")
    with col2:
        new_role = st.selectbox("Role", ["user", "admin"])

    if st.button("Create User"):
        ok, message = create_user_by_admin(new_username, new_role)
        if ok:
            st.success(message)
            st.rerun()
        else:
            st.error(message)

    st.divider()
    st.markdown('<div class="card-title" style="font-size:1.1rem">👥 Existing Users</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    users = get_users_for_admin()
    if not users:
        st.info("No users found.")
    else:
        df = pd.DataFrame([
            {
                "Username": u["username"],
                "Role": u["role"],
                "Must Change Password": "Yes" if u["must_change_password"] else "No",
                "Failed Attempts": u["failed_attempts"],
                "Active": "Yes" if u["is_active"] else "No",
            }
            for u in users
        ])
        df.index = range(1, len(df) + 1)
        st.dataframe(df, use_container_width=True)

        st.divider()
        st.markdown('<div class="card-title">⚙️ Manage User</div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        user_options = {
            f"{u['id']} - {u['username']} ({u['role']})": u["id"]
            for u in users
        }
        selected_label = st.selectbox("Select user", options=list(user_options.keys()))
        selected_user_id = user_options[selected_label]
        current_user_id = st.session_state.get("user_id")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Force Password Reset"):
                ok, message = force_reset_password_by_admin(selected_user_id)
                if ok:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
        with col_b:
            if st.button("Remove User"):
                ok, message = remove_user_by_admin(current_user_id, selected_user_id)
                if ok:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

# ============ TAB 2 — JOB MANAGEMENT ============

with tab2:

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="card-title" style="font-size:1.1rem">➕ Post New Job</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        job_title = st.text_input("Job Title", placeholder="e.g. AI Engineer")
        job_location = st.text_input("Location", placeholder="e.g. Delhi, India")
        job_skills = st.text_input(
            "Required Skills",
            placeholder="e.g. Python, ML, Docker"
        )
    with col2:
        job_department = st.text_input("Department", placeholder="e.g. Technology")
        job_experience = st.text_input("Experience Required", placeholder="e.g. 2-4 years")
        job_certs = st.text_input(
            "Required Certifications",
            placeholder="e.g. AWS Certified, PMP"
        )

    job_description = st.text_area(
        "Job Description",
        height=150,
        placeholder="Enter full job description here..."
    )

    if st.button("📢 Post Job"):
        if not job_title or not job_description or not job_skills:
            st.error("Title, description and required skills are mandatory.")
        else:
            response = requests.post(
                f"{API_URL}/jobs",
                json={
                    "title": job_title,
                    "department": job_department,
                    "location": job_location,
                    "experience": job_experience,
                    "description": job_description,
                    "required_skills": job_skills,
                    "required_certifications": job_certs,
                    "posted_by": st.session_state.get("username", "admin")
                }
            )
            if response.status_code == 200:
                st.success(f"✅ Job '{job_title}' posted successfully!")
                st.rerun()
            else:
                st.error("Failed to post job. Make sure FastAPI is running.")

    st.divider()
    st.markdown('<div class="card-title" style="font-size:1.1rem">📋 All Job Postings</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    jobs_response = requests.get(f"{API_URL}/jobs")
    if jobs_response.status_code == 200:
        jobs = jobs_response.json().get("jobs", [])

        if not jobs:
            st.info("No jobs posted yet.")
        else:
            for job in jobs:
                status_color = "badge-green" if job["status"] == "open" else "badge-red"
                status_label = "🟢 Open" if job["status"] == "open" else "🔴 Closed"

                st.markdown(f"""
                <div class="card">
                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap">
                        <div>
                            <div style="font-size:1.1rem; font-weight:700; color:#e2e8f0">
                                #{job['id']} — {job['title']}
                            </div>
                            <div style="color:#64748b; font-size:0.85rem; margin-top:0.3rem">
                                🏢 {job['department']} &nbsp;|&nbsp;
                                📍 {job['location']} &nbsp;|&nbsp;
                                🕐 {job['experience']} &nbsp;|&nbsp;
                                📅 {job['posted_date']}
                            </div>
                        </div>
                        <span class="badge {status_color}">{status_label}</span>
                    </div>
                    <div style="margin-top:0.8rem; color:#a0aec0; font-size:0.85rem">
                        {job['description'][:150]}{'...' if len(job['description']) > 150 else ''}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                col_open, col_close, col_delete = st.columns([1, 1, 4])

                with col_open:
                    if st.button("🟢 Open", key=f"open_{job['id']}"):
                        requests.put(
                            f"{API_URL}/jobs/{job['id']}",
                            json={"status": "open"}
                        )
                        st.rerun()

                with col_close:
                    if st.button("🔴 Close", key=f"close_{job['id']}"):
                        requests.put(
                            f"{API_URL}/jobs/{job['id']}",
                            json={"status": "closed"}
                        )
                        st.rerun()

                with col_delete:
                    if st.button("🗑️ Delete Job", key=f"delete_{job['id']}"):
                        requests.delete(f"{API_URL}/jobs/{job['id']}")
                        st.rerun()

                st.markdown("<br>", unsafe_allow_html=True)

# ============ TAB 3 — APPLICATIONS ============

with tab3:

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="card-title" style="font-size:1.1rem">📋 View Applications by Job</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    jobs_response = requests.get(f"{API_URL}/jobs")
    if jobs_response.status_code == 200:
        jobs = jobs_response.json().get("jobs", [])

        if not jobs:
            st.info("No jobs posted yet.")
        else:
            job_options = {
                f"#{j['id']} — {j['title']} ({j['status']})": j["id"]
                for j in jobs
            }
            selected_job_label = st.selectbox(
                "Select Job",
                options=list(job_options.keys())
            )
            selected_job_id = job_options[selected_job_label]

            apps_response = requests.get(
                f"{API_URL}/jobs/{selected_job_id}/applications"
            )

            if apps_response.status_code == 200:
                applications = apps_response.json().get("applications", [])

                if not applications:
                    st.info("No applications yet for this job.")
                else:
                    st.markdown(
                        f"<p style='color:#22d3ee; font-weight:600'>"
                        f"{len(applications)} application(s) received</p>",
                        unsafe_allow_html=True
                    )

                    for app in applications:
                        status_colors = {
                            "Applied": "badge-purple",
                            "Shortlisted": "badge-green",
                            "Rejected": "badge-red",
                            "Interview Scheduled": "badge-yellow"
                        }
                        status_color = status_colors.get(app["status"], "badge-purple")

                        st.markdown(f"""
                        <div class="rank-card">
                            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap">
                                <div>
                                    <div style="font-size:1.1rem; font-weight:700; color:#e2e8f0">
                                        {app['name']}
                                    </div>
                                    <div style="color:#64748b; font-size:0.85rem">
                                        {app['email']} &nbsp;|&nbsp; Applied: {app['applied_date']}
                                    </div>
                                </div>
                                <span class="badge {status_color}">{app['status']}</span>
                            </div>
                            <div style="margin-top:1rem; display:flex; gap:2rem; flex-wrap:wrap">
                                <div style="text-align:center">
                                    <div style="color:#64748b; font-size:0.75rem">OVERALL</div>
                                    <div style="color:#22d3ee; font-size:1.3rem; font-weight:700">
                                        {app['match_score']}%
                                    </div>
                                </div>
                                <div style="text-align:center">
                                    <div style="color:#64748b; font-size:0.75rem">SKILLS</div>
                                    <div style="color:#e2e8f0; font-size:1.1rem; font-weight:600">
                                        {app['skills_score']}%
                                    </div>
                                </div>
                                <div style="text-align:center">
                                    <div style="color:#64748b; font-size:0.75rem">EXPERIENCE</div>
                                    <div style="color:#e2e8f0; font-size:1.1rem; font-weight:600">
                                        {app['experience_score']}%
                                    </div>
                                </div>
                                <div style="text-align:center">
                                    <div style="color:#64748b; font-size:0.75rem">CERTIFICATIONS</div>
                                    <div style="color:#e2e8f0; font-size:1.1rem; font-weight:600">
                                        {app['certifications_score']}%
                                    </div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        col_s, col_i, col_r, col_space = st.columns([1, 1.5, 1, 3])

                        with col_s:
                            if st.button("⭐ Shortlist", key=f"short_{app['id']}"):
                                requests.put(
                                    f"{API_URL}/applications/{app['id']}",
                                    json={"status": "Shortlisted"}
                                )
                                st.rerun()

                        with col_i:
                            if st.button("📅 Schedule Interview", key=f"interview_{app['id']}"):
                                requests.put(
                                    f"{API_URL}/applications/{app['id']}",
                                    json={"status": "Interview Scheduled"}
                                )
                                st.rerun()

                        with col_r:
                            if st.button("❌ Reject", key=f"reject_{app['id']}"):
                                requests.put(
                                    f"{API_URL}/applications/{app['id']}",
                                    json={"status": "Rejected"}
                                )
                                st.rerun()

                        st.markdown("<br>", unsafe_allow_html=True)