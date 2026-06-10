import streamlit as st
import requests
from styles import inject_css

st.set_page_config(page_title="Track Application", page_icon="🔍", layout="wide")
inject_css()

API_URL = "http://localhost:8000"

st.markdown("""
<div class="hero">
    <h1>🔍 Track Your Application</h1>
    <p class="hero-subtitle">
        Enter your email address to see all your application statuses
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- CHECK URL PARAMS ----------------

params = st.query_params
email_from_url = params.get("email", "")

# ---------------- EMAIL INPUT ----------------

email = st.text_input(
    "",
    value=email_from_url,
    placeholder="Enter your email address..."
)

if st.button("🔍 Track Applications", use_container_width=False):
    if not email:
        st.error("Please enter your email address.")
    else:
        with st.spinner("Looking up your applications..."):
            response = requests.get(f"{API_URL}/track/{email.strip()}")

        if response.status_code == 200:
            data = response.json()

            if not data["found"] or not data["applications"]:
                st.warning(f"No applications found for **{email}**. Please check your email address.")
            else:
                applications = data["applications"]

                st.divider()
                st.markdown(
                    f"<p style='color:#22d3ee; font-weight:600'>"
                    f"Found {len(applications)} application(s) for "
                    f"<strong>{email}</strong></p>",
                    unsafe_allow_html=True
                )
                st.markdown("<br>", unsafe_allow_html=True)

                for app in applications:

                    # Status styling
                    status_config = {
                        "Applied": ("badge-purple", "📝"),
                        "Shortlisted": ("badge-green", "⭐"),
                        "Rejected": ("badge-red", "❌"),
                        "Interview Scheduled": ("badge-yellow", "📅")
                    }
                    badge_class, status_icon = status_config.get(
                        app["status"],
                        ("badge-purple", "📝")
                    )

                    score_color = (
                        "#22d3ee" if app["match_score"] >= 70
                        else "#f59e0b" if app["match_score"] >= 40
                        else "#ef4444"
                    )

                    st.markdown(f"""
                    <div class="card">
                        <div style="display:flex; justify-content:space-between;
                                    align-items:flex-start; flex-wrap:wrap; gap:1rem">
                            <div>
                                <div style="font-size:1.2rem; font-weight:700;
                                            color:#e2e8f0">{app['job_title']}</div>
                                <div style="color:#64748b; font-size:0.85rem;
                                            margin-top:0.3rem">
                                    🏢 {app['department']} &nbsp;|&nbsp;
                                    📍 {app['location']} &nbsp;|&nbsp;
                                    📅 Applied: {app['applied_date']}
                                </div>
                            </div>
                            <span class="badge {badge_class}">
                                {status_icon} {app['status']}
                            </span>
                        </div>

                        <div style="margin-top:1.2rem">
                            <div style="display:flex; gap:2rem;
                                        flex-wrap:wrap; align-items:center">
                                <div>
                                    <div style="color:#64748b; font-size:0.75rem;
                                                text-transform:uppercase;
                                                letter-spacing:0.05em">
                                        Overall Match
                                    </div>
                                    <div style="font-size:1.5rem; font-weight:700;
                                                color:{score_color}">
                                        {app['match_score']}%
                                    </div>
                                </div>
                                <div>
                                    <div style="color:#64748b; font-size:0.75rem;
                                                text-transform:uppercase;
                                                letter-spacing:0.05em">Skills</div>
                                    <div style="color:#e2e8f0; font-weight:600">
                                        {app['skills_score']}%
                                    </div>
                                </div>
                                <div>
                                    <div style="color:#64748b; font-size:0.75rem;
                                                text-transform:uppercase;
                                                letter-spacing:0.05em">Experience</div>
                                    <div style="color:#e2e8f0; font-weight:600">
                                        {app['experience_score']}%
                                    </div>
                                </div>
                                <div>
                                    <div style="color:#64748b; font-size:0.75rem;
                                                text-transform:uppercase;
                                                letter-spacing:0.05em">Certifications</div>
                                    <div style="color:#e2e8f0; font-weight:600">
                                        {app['certifications_score']}%
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div style="margin-top:1rem">
                            <div style="height:6px; background:#0a2a35;
                                        border-radius:10px; overflow:hidden">
                                <div style="height:100%; width:{app['match_score']}%;
                                            background:linear-gradient(90deg, #0891b2, #67e8f9);
                                            border-radius:10px; transition:width 0.3s ease">
                                </div>
                            </div>
                        </div>

                    </div>
                    """, unsafe_allow_html=True)

                    # Status message
                    if app["status"] == "Applied":
                        st.info("⏳ Your application is under review. We will get back to you soon.")
                    elif app["status"] == "Shortlisted":
                        st.success("🌟 Congratulations! You have been shortlisted for this position.")
                    elif app["status"] == "Interview Scheduled":
                        st.success("📅 Your interview has been scheduled. Please check your email for details.")
                    elif app["status"] == "Rejected":
                        st.warning("We appreciate your interest. Unfortunately you were not selected for this role.")

                    st.markdown("<br>", unsafe_allow_html=True)

        else:
            st.error("Could not connect. Make sure the backend is running.")

st.divider()

col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    if st.button("← Back to Jobs", use_container_width=True):
        st.switch_page("App.py")