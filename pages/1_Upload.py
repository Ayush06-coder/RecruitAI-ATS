import streamlit as st
import requests
import pandas as pd
from auth import enforce_access, render_sidebar

st.set_page_config(
    page_title="Upload Resume",
    page_icon="📤",
    layout="wide"
)

enforce_access()
render_sidebar()

API_URL = "http://localhost:8000"

# ---------------- SESSION STATE INIT ----------------

if "upload_history" not in st.session_state:
    st.session_state["upload_history"] = []

# ---------------- PAGE HEADER ----------------

st.title("📤 Upload Resume")
st.caption("Upload PDF or DOCX resumes. Maximum file size: 200MB.")
st.divider()

# ---------------- FILE UPLOAD ----------------

uploaded_file = st.file_uploader(
    "Choose a resume to upload",
    type=["pdf", "docx"]
)

if uploaded_file is not None:

    # ---------------- FILE SIZE CHECK ----------------

    file_size_mb = uploaded_file.size / (1024 * 1024)

    if file_size_mb > 200:
        st.error(
            f"❌ File too large — {file_size_mb:.1f}MB. "
            f"Please upload a file smaller than 200MB."
        )
        st.stop()

    # ---------------- CHECK ALREADY UPLOADED IN SESSION ----------------

    already_uploaded = any(
        r["File Name"] == uploaded_file.name
        for r in st.session_state["upload_history"]
    )

    if already_uploaded:
        st.warning(f"⚠️ {uploaded_file.name} has already been uploaded this session.")

    else:

        with st.spinner(f"Parsing {uploaded_file.name}..."):

            response = requests.post(
                f"{API_URL}/upload",
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

            if data.get("saved"):
                status = "✅ Saved"
                st.success(f"✅ {data['name']} saved to database!")
            else:
                status = "⚠️ Already Exists"
                st.warning(f"⚠️ {data['name']} already exists in database!")

            # Add to session upload history
            st.session_state["upload_history"].append({
                "File Name": uploaded_file.name,
                "Name": data["name"],
                "Email": data["email"],
                "Phone": data["phone"],
                "Skills Count": len(data["skills"]),
                "Size": f"{file_size_mb:.1f} MB",
                "Status": status
            })

        else:
            st.error("Something went wrong. Make sure FastAPI backend is running.")

st.divider()

# ---------------- UPLOAD HISTORY TABLE ----------------

st.subheader("📋 Upload History — Current Session")

if not st.session_state["upload_history"]:
    st.info("No resumes uploaded yet in this session. Upload a resume above to get started.")

else:
    st.markdown(f"**{len(st.session_state['upload_history'])} resume(s) uploaded this session**")

    history_df = pd.DataFrame(st.session_state["upload_history"])
    st.dataframe(history_df, use_container_width=True)

    st.divider()

    # ---------------- LAST UPLOADED CANDIDATE DETAILS ----------------

    st.subheader("👤 Last Uploaded Candidate")

    last = st.session_state["upload_history"][-1]

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"👤 **Name:** {last['Name']}")
        st.write(f"📧 **Email:** {last['Email']}")
        st.write(f"📞 **Phone:** {last['Phone']}")

    with col2:
        st.write(f"🛠️ **Skills Found:** {last['Skills Count']}")
        st.write(f"📁 **File Size:** {last['Size']}")
        st.write(f"💾 **Status:** {last['Status']}")

    st.divider()

    # ---------------- CLEAR SESSION BUTTON ----------------

    if st.button("🗑️ Clear Upload History"):
        st.session_state["upload_history"] = []
        st.rerun()