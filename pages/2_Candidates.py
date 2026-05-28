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
st.caption("Search, filter and view all parsed candidates.")
st.divider()

# ---------------- SEARCH BAR ----------------

search_query = st.text_input(
    "🔍 Search candidates by name, email or skill",
    placeholder="e.g. Python, Ayush, gmail.com..."
)

# ---------------- SKILL FILTER ----------------

st.markdown("**Filter by Skill:**")

skill_options = [
    "Python", "Java", "Machine Learning", "SQL", "MySQL",
    "MongoDB", "Docker", "AWS", "React", "Django", "FastAPI",
    "Git", "NLP", "Deep Learning", "PostgreSQL"
]

selected_skill = st.selectbox(
    "Select a skill to filter",
    options=["All"] + skill_options
)

st.divider()

# ---------------- FETCH CANDIDATES ----------------

if search_query:
    response = requests.get(
        f"{API_URL}/candidates",
        params={"search": search_query}
    )
else:
    response = requests.get(f"{API_URL}/candidates")

if response.status_code == 200:

    data = response.json()
    candidates = data["candidates"]

    # Apply skill filter on frontend
    if selected_skill != "All":
        candidates = [
            c for c in candidates
            if selected_skill.lower() in c["skills"].lower()
        ]

    if not candidates:
        st.warning("No candidates found matching your search.")

    else:
        st.markdown(f"**{len(candidates)} candidate(s) found**")

        # ---------------- TABLE VIEW ----------------

        candidate_data = []
        for c in candidates:
            candidate_data.append({
                "Name": c["name"],
                "Email": c["email"],
                "Phone": c["phone"],
                "Skills": c["skills"],
                "Education": c["education"]
            })

        df = pd.DataFrame(candidate_data)
        st.dataframe(df, use_container_width=True)

        st.divider()

        # ---------------- DETAILED VIEW ----------------

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