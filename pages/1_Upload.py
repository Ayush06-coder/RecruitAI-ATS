import streamlit as st
import requests

st.set_page_config(
    page_title="Upload Resume",
    page_icon="📤",
    layout="wide"
)

API_URL = "http://localhost:8000"

st.title("📤 Upload Resume")
st.caption("Upload a PDF or DOCX resume to extract candidate information.")
st.divider()

uploaded_file = st.file_uploader("", type=["pdf", "docx"])

if uploaded_file is not None:

    with st.spinner("Parsing resume..."):

        response = requests.post(
            f"{API_URL}/upload",
            files={"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        )

    if response.status_code == 200:

        data = response.json()

        if data.get("saved"):
            st.success(f"✅ {data['name']} saved to database!")
        else:
            st.warning(f"⚠️ {data['name']} already exists in database!")

        st.divider()

        # Candidate Profile
        st.subheader("👤 Candidate Profile")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"👤 **Name:** {data['name']}")
            st.write(f"📧 **Email:** {data['email']}")
            st.write(f"📞 **Phone:** {data['phone']}")

        with col2:
            st.write(f"🛠️ **Skills:** {', '.join(data['skills'])}")
            st.write(f"🎓 **Education:** {', '.join(data['education'])}")
            st.write(f"💼 **Experience:** {', '.join(data['experience'])}")

        st.divider()

        # Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Skills Found", len(data['skills']))
        m2.metric("Education Matches", len(data['education']))
        m3.metric("Experience Entries", len(data['experience']))

    else:
        st.error("Something went wrong. Make sure the FastAPI backend is running.")