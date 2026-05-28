import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Candidates",
    page_icon="👥",
    layout="wide"
)

API_URL = "http://localhost:8000"

st.title("👥 Candidate Database")
st.caption("All parsed candidates stored in the database.")
st.divider()

response = requests.get(f"{API_URL}/candidates")

if response.status_code == 200:

    data = response.json()
    candidates = data["candidates"]

    if not candidates:
        st.info("No candidates yet. Upload resumes from the Upload page.")

    else:
        st.markdown(f"**{len(candidates)} candidate(s) in database**")

        candidate_data = []

        for c in candidates:
            candidate_data.append({
                "Name": c["name"],
                "Email": c["email"],
                "Phone": c["phone"],
                "Skills": c["skills"],
                "Education": c["education"],
                "Experience": c["experience"]
            })

        df = pd.DataFrame(candidate_data)
        st.dataframe(df, use_container_width=True)

        st.divider()

        # Individual candidate expanders
        st.subheader("Candidate Details")

        for c in candidates:
            with st.expander(f"👤 {c['name']} — {c['email']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Name:** {c['name']}")
                    st.markdown(f"**Email:** {c['email']}")
                    st.markdown(f"**Phone:** {c['phone']}")
                with col2:
                    st.markdown(f"**Skills:** {c['skills']}")
                    st.markdown(f"**Education:** {c['education']}")
                    st.markdown(f"**Experience:** {c['experience']}")

else:
    st.error("Could not connect to backend. Make sure FastAPI is running.")