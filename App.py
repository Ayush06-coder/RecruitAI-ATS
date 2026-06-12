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

apply_page = st.Page("pages/Apply.py", title="📤 Apply", icon="📤")
track_page = st.Page("pages/Track.py", title="🔍 Track", icon="🔍")
login_page = st.Page("pages/Login.py", title="🔐 Login", icon="🔐")

applications_page = st.Page("pages/Applications.py", title="📋 Applications", icon="📋")
candidates_page = st.Page("pages/Candidates.py", title="👥 Candidates", icon="👥")
jd_matching_page = st.Page("pages/JD_Matching.py", title="🎯 JD Matching", icon="🎯")
analytics_page = st.Page("pages/Analytics.py", title="📊 Analytics", icon="📊")
change_password_page = st.Page("pages/Change_Password.py", title="🔑 Change Password", icon="🔑")
admin_page = st.Page("pages/Admin.py", title="🛠️ Admin", icon="🛠️")

# ---------------- DETERMINE NAVIGATION ----------------

if not is_logged_in():
    home_page = st.Page("pages/Home.py", title="🏠 Home", icon="🏠", default=True)
    pages = [home_page, apply_page, track_page, login_page]

elif get_user_role() == "admin":
    dashboard_page = st.Page("pages/Dashboard.py", title="📊 Dashboard", icon="📊", default=True)
    pages = [
        dashboard_page, applications_page, candidates_page,
        jd_matching_page, analytics_page, admin_page, change_password_page
    ]

elif get_user_role() == "user":
    dashboard_page = st.Page("pages/Dashboard.py", title="📊 Dashboard", icon="📊", default=True)
    pages = [
        dashboard_page, applications_page, candidates_page,
        jd_matching_page, analytics_page, change_password_page
    ]

else:
    home_page = st.Page("pages/Home.py", title="🏠 Home", icon="🏠", default=True)
    pages = [home_page, apply_page, track_page, login_page]

# ---------------- RENDER NAVIGATION ----------------

nav = st.navigation(pages)
nav.run()