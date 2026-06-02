import streamlit as st
import requests
import pandas as pd
from collections import Counter
from auth import enforce_access, render_sidebar

st.set_page_config(
    page_title="Analytics",
    page_icon="📊",
    layout="wide"
)

enforce_access()
render_sidebar()

API_URL = "http://localhost:8000"

st.title("📊 Analytics Dashboard")
st.caption("Insights from all parsed candidates in the database.")
st.divider()

# ---------------- FETCH DATA ----------------

response = requests.get(f"{API_URL}/candidates")

if response.status_code != 200:
    st.error("Could not connect to backend. Make sure FastAPI is running.")
    st.stop()

data = response.json()
candidates = data["candidates"]

if not candidates:
    st.info("No candidates in database yet. Upload resumes to see analytics.")
    st.stop()

# ---------------- SUMMARY METRICS ----------------

total_candidates = len(candidates)

all_skills = []
for c in candidates:
    if c["skills"] and c["skills"] != "No skills found":
        skills = [s.strip() for s in c["skills"].split(",")]
        all_skills.extend(skills)

all_education = []
for c in candidates:
    if c["education"] and c["education"] != "Education not found":
        edu = [e.strip() for e in c["education"].split(",")]
        all_education.extend(edu)

all_experience = []
for c in candidates:
    if c["experience"] and c["experience"] != "Experience not found":
        exp = [e.strip() for e in c["experience"].split(",")]
        all_experience.extend(exp)

unique_skills = len(set(all_skills))

m1, m2, m3 = st.columns(3)
m1.metric("👥 Total Candidates", total_candidates)
m2.metric("🛠️ Unique Skills Found", unique_skills)
m3.metric("📋 Total Experience Entries", len(all_experience))

st.divider()

# ---------------- SKILLS CHART ----------------

st.subheader("🛠️ Top Skills Across All Candidates")

if all_skills:
    skill_counts = Counter(all_skills)
    top_skills = dict(sorted(
        skill_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )[:15])

    skills_df = pd.DataFrame({
        "Skill": list(top_skills.keys()),
        "Count": list(top_skills.values())
    })

    st.bar_chart(skills_df.set_index("Skill"))

else:
    st.info("No skills data available.")

st.divider()

# ---------------- EDUCATION CHART ----------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("🎓 Education Breakdown")

    if all_education:
        edu_keywords = {
            "B.Tech": ["b.tech", "btech", "bachelor of technology"],
            "M.Tech": ["m.tech", "mtech", "master of technology"],
            "MBA": ["mba", "master of business"],
            "BCA": ["bca"],
            "MCA": ["mca"],
            "B.Sc": ["b.sc", "bsc", "bachelor of science"],
            "M.Sc": ["m.sc", "msc", "master of science"],
            "BBA": ["bba"],
            "Diploma": ["diploma"],
            "PhD": ["phd", "doctorate"],
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

# ---------------- EXPERIENCE CHART ----------------

with col2:
    st.subheader("💼 Experience Breakdown")

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

# ---------------- CANDIDATES SKILLS TABLE ----------------

st.subheader("👥 Candidate Skills Overview")

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
st.dataframe(overview_df, use_container_width=True)