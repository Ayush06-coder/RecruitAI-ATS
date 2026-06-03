import streamlit as st
import requests
import pandas as pd

from auth import enforce_access, render_sidebar

st.set_page_config(
    page_title="JD Matching",
    page_icon="🎯",
    layout="wide"
)

enforce_access()
render_sidebar()

API_URL = "http://localhost:8000"

st.title("🎯 JD Matching & Candidate Ranking")
st.caption("Paste a job description to match and rank all candidates.")
st.divider()

job_title = st.text_input(
    "Job Title (optional)",
    placeholder="e.g. AI Engineer, Data Scientist",
)

jd_text = st.text_area(
    "Paste Job Description here",
    height=200,
    placeholder="Paste the job description here..."
)

if jd_text:

    with st.spinner("Matching candidates..."):

        response = requests.post(
            f"{API_URL}/match",
            json={"jd_text": jd_text, "job_title": job_title},
        )

    if response.status_code == 200:

        data = response.json()
        results = data["results"]

        if not results:
            st.warning("No candidates in database. Upload resumes first.")

        else:
            st.divider()

            # Top Candidate
            top = results[0]
            st.success(f"🏆 Top Candidate: {top['name']} ({top['score']}%)")

            st.divider()

            # Match Results
            st.subheader("Match Results")

            for i, result in enumerate(results):

                col_rank, col_info = st.columns([1, 5])

                with col_rank:
                    medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"#{i+1}"
                    st.markdown(f"### {medal}")
                    color = "🟢" if result['score'] >= 70 else "🟡" if result['score'] >= 40 else "🔴"
                    st.markdown(f"## {color} {result['score']}%")

                with col_info:
                    st.markdown(f"**{result['name']}** — {result['email']}")
                    st.markdown("**Overall Match Score**")
                    st.progress(result["score"] / 100)

                    col_skills, col_exp, col_certs = st.columns(3)
                    with col_skills:
                        st.caption(f"Skills ({result['skills_score']}%)")
                        st.progress(result["skills_score"] / 100)
                    with col_exp:
                        st.caption(f"Experience ({result['experience_score']}%)")
                        st.progress(result["experience_score"] / 100)
                    with col_certs:
                        st.caption(f"Certifications ({result['certifications_score']}%)")
                        st.progress(result["certifications_score"] / 100)

                    matched_skills = result.get("matched_skills", [])
                    missing_skills = result.get("missing_skills", [])
                    matched_experience = result.get("matched_experience", [])
                    matched_certifications = result.get("matched_certifications", [])

                    st.markdown(
                        f"✅ **Matched Skills:** {', '.join(matched_skills) if matched_skills else 'None'}"
                    )
                    st.markdown(
                        f"❌ **Missing Skills:** {', '.join(missing_skills) if missing_skills else 'None'}"
                    )
                    st.markdown(
                        f"💼 **Matched Experience:** {', '.join(matched_experience) if matched_experience else 'None'}"
                    )
                    st.markdown(
                        f"📜 **Matched Certifications:** {', '.join(matched_certifications) if matched_certifications else 'None'}"
                    )

                st.divider()

            # Ranking Table
            st.subheader("📊 Ranking Table")

            ranking_data = []
            for i, result in enumerate(results):
                medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"#{i+1}"
                ranking_data.append({
                    "Rank": medal,
                    "Name": result["name"],
                    "Email": result["email"],
                    "Match Score": f"{result['score']}%"
                })

            st.dataframe(pd.DataFrame(ranking_data), use_container_width=True)

    else:
        st.error("Could not connect to backend. Make sure FastAPI is running.")