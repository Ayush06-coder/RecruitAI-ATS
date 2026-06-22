import streamlit as st
import requests
import pandas as pd
from styles import inject_css
from auth import enforce_access, render_sidebar

st.set_page_config(page_title="JD Matching", page_icon="🎯", layout="wide")
inject_css()

enforce_access()
render_sidebar()

from config import API_URL

st.markdown("""
<div class="hero">
    <h1>🎯 JD Matching & Ranking</h1>
    <p class="hero-subtitle">Match and rank all candidates against a job description</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    job_title = st.text_input("", placeholder="💼 Job Title — e.g. AI Engineer")

with col2:
    jd_text = st.text_area("", height=120, placeholder="📋 Paste job description here...")

if jd_text:
    with st.spinner("Matching candidates..."):
        try:
            response = requests.post(
                f"{API_URL}/match",
                json={"jd_text": jd_text, "job_title": job_title}
            )
        except Exception:
            st.error("Could not connect to backend. Make sure FastAPI is running.")
            st.stop()

    if response.status_code == 200:
        data = response.json()
        results = data["results"]

        if not results:
            st.warning("No candidates in database. Upload resumes first.")
        else:
            st.divider()

            top = results[0]
            st.markdown(f"""
            <div class="card" style="border-color:#22d3ee;
                background: linear-gradient(135deg, #061a20, #0a2a35)">
                <div style="display:flex; align-items:center; gap:1rem">
                    <span style="font-size:2rem">🏆</span>
                    <div>
                        <div class="card-title" style="font-size:1.1rem">
                            Top Candidate
                        </div>
                        <div style="color:#e2e8f0; font-size:1.3rem; font-weight:700">
                            {top['name']} — {top['score']}% Match
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                '<div class="card-title" style="font-size:1.1rem">📊 Match Results</div>',
                unsafe_allow_html=True
            )
            st.markdown("<br>", unsafe_allow_html=True)

            for i, result in enumerate(results):
                medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"#{i+1}"
                color = "#22d3ee" if result['score'] >= 70 else "#f59e0b" if result['score'] >= 40 else "#ef4444"
                dot = "🟢" if result['score'] >= 70 else "🟡" if result['score'] >= 40 else "🔴"

                st.markdown(f"""
                <div class="rank-card">
                    <div style="display:flex; align-items:center;
                                gap:1.5rem; flex-wrap:wrap">
                        <div style="text-align:center; min-width:80px">
                            <div style="font-size:1.8rem">{medal}</div>
                            <div style="font-size:1.5rem; font-weight:700;
                                        color:{color}">{dot} {result['score']}%</div>
                        </div>
                        <div style="flex:1">
                            <div style="font-size:1.1rem; font-weight:600;
                                        color:#e2e8f0">{result['name']}</div>
                            <div style="color:#64748b; font-size:0.85rem">
                                {result['email']}
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                col_s, col_e, col_c = st.columns(3)
                with col_s:
                    st.caption(f"Skills ({result['skills_score']}%)")
                    st.progress(result["skills_score"] / 100)
                with col_e:
                    st.caption(f"Experience ({result['experience_score']}%)")
                    st.progress(result["experience_score"] / 100)
                with col_c:
                    st.caption(f"Certifications ({result['certifications_score']}%)")
                    st.progress(result["certifications_score"] / 100)

                matched_skills = result.get("matched_skills", [])
                missing_skills = result.get("missing_skills", [])

                matched_html = "".join([
                    f'<span class="badge badge-green">{s}</span>'
                    for s in matched_skills
                ]) if matched_skills else "<span style='color:#64748b'>None</span>"

                missing_html = "".join([
                    f'<span class="badge badge-red">{s}</span>'
                    for s in missing_skills
                ]) if missing_skills else "<span style='color:#64748b'>None</span>"

                st.markdown(f"""
                <div style="margin: 0.5rem 0 1.5rem 0">
                    <p style="margin:0.3rem 0">
                        ✅ <strong style="color:#22d3ee">Matched:</strong> {matched_html}
                    </p>
                    <p style="margin:0.3rem 0">
                        ❌ <strong style="color:#ef4444">Missing:</strong> {missing_html}
                    </p>
                </div>
                """, unsafe_allow_html=True)

                st.divider()

            st.markdown(
                '<div class="card-title">📊 Ranking Table</div>',
                unsafe_allow_html=True
            )
            st.markdown("<br>", unsafe_allow_html=True)

            ranking_data = []
            for i, result in enumerate(results):
                medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else f"#{i+1}"
                ranking_data.append({
                    "Rank": medal,
                    "Name": result["name"],
                    "Email": result["email"],
                    "Overall": f"{result['score']}%",
                    "Skills": f"{result['skills_score']}%",
                    "Experience": f"{result['experience_score']}%",
                    "Certifications": f"{result['certifications_score']}%"
                })

            rank_df = pd.DataFrame(ranking_data)
            rank_df.index = rank_df.index + 1
            st.dataframe(rank_df, use_container_width=True)

    else:
        st.error("Could not connect to backend. Make sure FastAPI is running.")