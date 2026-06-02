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

jd_text = st.text_area(
    "Paste Job Description here",
    height=200,
    placeholder="Paste the job description here..."
)

if jd_text:

    with st.spinner("Matching candidates..."):

        response = requests.post(
            f"{API_URL}/match",
            json={"jd_text": jd_text}
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
                    st.progress(result["score"] / 100)
                    st.markdown(f"✅ **Matched:** {', '.join(result['matched']) if result['matched'] else 'None'}")
                    st.markdown(f"❌ **Missing:** {', '.join(result['missing']) if result['missing'] else 'None'}")

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