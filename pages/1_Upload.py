import streamlit as st
import requests
import pandas as pd
from auth import is_logged_in, render_sidebar, must_change_password
from styles import inject_css

st.set_page_config(page_title="Upload Resume", page_icon="📤", layout="wide")
inject_css()

if not is_logged_in():
    st.warning("Please login first.")
    st.stop()

render_sidebar()

if must_change_password():
    st.error("You must change your password before accessing this page.")
    st.stop()

API_URL = "http://localhost:8000"

if "upload_history" not in st.session_state:
    st.session_state["upload_history"] = []

st.markdown("""
<div class="hero">
    <h1>📤 Upload Resume</h1>
    <p class="hero-subtitle">Upload PDF or DOCX resumes — Maximum file size 200MB</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("", type=["pdf", "docx"])

if uploaded_file is not None:

    file_size_mb = uploaded_file.size / (1024 * 1024)

    if file_size_mb > 200:
        st.error(f"❌ File too large — {file_size_mb:.1f}MB. Please upload a file smaller than 200MB.")
        st.stop()

    already_uploaded = any(
        r["File Name"] == uploaded_file.name
        for r in st.session_state["upload_history"]
    )

    if already_uploaded:
        st.warning(f"⚠️ {uploaded_file.name} already uploaded this session.")
    else:
        with st.spinner(f"Parsing {uploaded_file.name}..."):
            response = requests.post(
                f"{API_URL}/upload",
                files={"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            )

        if response.status_code == 200:
            data = response.json()

            if data.get("saved"):
                status = "✅ Saved"
                st.success(f"✅ {data['name']} saved to database!")
            else:
                status = "⚠️ Already Exists"
                st.warning(f"⚠️ {data['name']} already exists in database!")

            st.session_state["upload_history"].append({
                "File Name": uploaded_file.name,
                "Name": data["name"],
                "Email": data["email"],
                "Phone": data["phone"],
                "Skills Count": len(data["skills"]),
                "Size": f"{file_size_mb:.1f} MB",
                "Status": status
            })

            st.divider()
            st.markdown("""
            <div class="card-title">👤 Extracted Candidate Profile</div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Name</div>
                    <div class="metric-value" style="font-size:1.2rem">{data['name']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Email</div>
                    <div class="metric-value" style="font-size:1rem">{data['email']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Phone</div>
                    <div class="metric-value" style="font-size:1.2rem">{data['phone']}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            col4, col5, col6 = st.columns(3)
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Skills Found</div>
                    <div class="metric-value">{len(data['skills'])}</div>
                </div>
                """, unsafe_allow_html=True)
            with col5:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Education Entries</div>
                    <div class="metric-value">{len(data['education'])}</div>
                </div>
                """, unsafe_allow_html=True)
            with col6:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Experience Entries</div>
                    <div class="metric-value">{len(data['experience'])}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            col7, col8 = st.columns(2)
            with col7:
                skills_html = "".join([f'<span class="badge badge-purple">{s}</span>' for s in data['skills']])
                st.markdown(f"""
                <div class="card">
                    <div class="card-title">🛠️ Skills</div>
                    <div style="margin-top:0.5rem">{skills_html}</div>
                </div>
                """, unsafe_allow_html=True)
            with col8:
                edu_html = "".join([f'<span class="badge badge-green">{e}</span>' for e in data['education']])
                exp_html = "".join([f'<span class="badge badge-yellow">{e}</span>' for e in data['experience']])
                st.markdown(f"""
                <div class="card">
                    <div class="card-title">🎓 Education & 💼 Experience</div>
                    <div style="margin-top:0.5rem">{edu_html}{exp_html}</div>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.error("Something went wrong. Make sure FastAPI backend is running.")

st.divider()

st.markdown("""
<div class="card-title">📋 Upload History — Current Session</div>
""", unsafe_allow_html=True)

if not st.session_state["upload_history"]:
    st.info("No resumes uploaded yet. Upload a resume above to get started.")
else:
    st.markdown(f"<p style='color:#64748b'>{len(st.session_state['upload_history'])} resume(s) uploaded this session</p>", unsafe_allow_html=True)
    history_df = pd.DataFrame(st.session_state["upload_history"])
    history_df.index = history_df.index + 1
    st.dataframe(history_df, use_container_width=True)

    if st.button("🗑️ Clear Upload History"):
        st.session_state["upload_history"] = []
        st.rerun()