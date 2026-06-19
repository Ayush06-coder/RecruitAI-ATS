import streamlit as st
import requests
import pandas as pd
from collections import Counter
from styles import inject_css
from auth import enforce_access, render_sidebar

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")
inject_css()

enforce_access()
render_sidebar()

from config import API_URL

st.markdown("""
<div class="hero">
    <h1>📊 Analytics Dashboard</h1>
    <p class="hero-subtitle">Insights from all parsed candidates in the database</p>
</div>
""", unsafe_allow_html=True)

try:
    response = requests.get(f"{API_URL}/candidates", params={"page_size": 9999})
    data = response.json()
    candidates = data["candidates"]
except:
    st.error("Could not connect to backend. Make sure FastAPI is running.")
    st.stop()

if not candidates:
    st.info("No candidates in database yet. Candidates will appear after they apply to jobs.")
    st.stop()

all_skills = []
for c in candidates:
    if c["skills"] and c["skills"] != "No skills found":
        all_skills.extend([s.strip() for s in c["skills"].split(",")])

all_experience = []
for c in candidates:
    if c["experience"] and c["experience"] != "Experience not found":
        all_experience.extend([e.strip() for e in c["experience"].split(",")])

all_education = []
for c in candidates:
    if c["education"] and c["education"] != "Education not found":
        all_education.extend([e.strip() for e in c["education"].split(",")])

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Candidates</div>
        <div class="metric-value">{len(candidates)}</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Unique Skills</div>
        <div class="metric-value">{len(set(all_skills))}</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Experience Entries</div>
        <div class="metric-value">{len(all_experience)}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.divider()

st.markdown(
    '<div class="card-title" style="font-size:1.1rem">🛠️ Top Skills Across All Candidates</div>',
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)

if all_skills:
    skill_counts = Counter(all_skills)
    top_skills = dict(
        sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:15]
    )
    skills_df = pd.DataFrame({
        "Skill": list(top_skills.keys()),
        "Count": list(top_skills.values())
    })
    st.bar_chart(skills_df.set_index("Skill"))

st.divider()

col_edu, col_exp = st.columns(2)

with col_edu:
    st.markdown(
        '<div class="card-title">🎓 Education Breakdown</div>',
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

    if all_education:
        edu_keywords = {
            "B.Tech": ["b.tech", "btech", "bachelor of technology"],
            "M.Tech": ["m.tech", "mtech"],
            "MBA": ["mba"],
            "BCA": ["bca"],
            "MCA": ["mca"],
            "B.Sc": ["b.sc", "bsc"],
            "M.Sc": ["m.sc", "msc"],
            "BBA": ["bba"],
            "Diploma": ["diploma"],
            "PhD": ["phd"],
            "Other": []
        }
        edu_counts = {key: 0 for key in edu_keywords}
        for edu in all_education:
            edu_lower = edu.lower()
            matched = False
            for degree, keywords in edu_keywords.items():
                if degree == "Other":
                    continue
                if any(kw in edu_lower for kw in keywords):
                    edu_counts[degree] += 1
                    matched = True
                    break
            if not matched:
                edu_counts["Other"] += 1
        edu_counts = {k: v for k, v in edu_counts.items() if v > 0}
        edu_df = pd.DataFrame({
            "Degree": list(edu_counts.keys()),
            "Count": list(edu_counts.values())
        })
        st.bar_chart(edu_df.set_index("Degree"))
    else:
        st.info("No education data available.")

with col_exp:
    st.markdown(
        '<div class="card-title">💼 Experience Breakdown</div>',
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

    if all_experience:
        role_keywords = {
            "Intern": ["intern", "internship", "trainee"],
            "Developer": ["developer", "programmer"],
            "Engineer": ["engineer"],
            "Analyst": ["analyst"],
            "Manager": ["manager"],
            "Designer": ["designer"],
            "Consultant": ["consultant"],
            "Scientist": ["scientist"],
            "Other": []
        }
        role_counts = {key: 0 for key in role_keywords}
        for exp in all_experience:
            exp_lower = exp.lower()
            matched = False
            for role, keywords in role_keywords.items():
                if role == "Other":
                    continue
                if any(kw in exp_lower for kw in keywords):
                    role_counts[role] += 1
                    matched = True
                    break
            if not matched:
                role_counts["Other"] += 1
        role_counts = {k: v for k, v in role_counts.items() if v > 0}
        role_df = pd.DataFrame({
            "Role": list(role_counts.keys()),
            "Count": list(role_counts.values())
        })
        st.bar_chart(role_df.set_index("Role"))
    else:
        st.info("No experience data available.")

st.divider()

st.markdown(
    '<div class="card-title">👥 Candidate Skills Overview</div>',
    unsafe_allow_html=True
)
st.markdown("<br>", unsafe_allow_html=True)

overview_data = []
for c in candidates:
    skill_count = len([
        s for s in c["skills"].split(",")
        if s.strip() and s.strip() != "No skills found"
    ])
    overview_data.append({
        "Name": c["name"],
        "Email": c["email"],
        "Skills Count": skill_count,
        "Top Skills": ", ".join(c["skills"].split(",")[:3]) if c["skills"] else "None"
    })

overview_df = pd.DataFrame(overview_data)
overview_df = overview_df.sort_values("Skills Count", ascending=False)
overview_df.index = range(1, len(overview_df) + 1)
st.dataframe(overview_df, use_container_width=True)