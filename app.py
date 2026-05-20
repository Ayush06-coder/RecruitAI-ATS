import streamlit as st
import os
import pandas as pd

from parser import (
    extract_text_from_pdf,
    extract_text_from_docx
)

from extractor import (
    extract_email,
    extract_phone,
    extract_name,
    extract_skills,
    extract_education,
    extract_experience,
    match_candidate
)

from database import (
    init_db,
    save_candidate,
    get_all_candidates
)

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Intelligent Resume Parser",
    layout="wide"
)

init_db()

# ---------------- SIDEBAR ----------------

st.sidebar.title("Recruiter Panel")

jd_text = st.sidebar.text_area(
    "Paste Job Description",
    height=250
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Built using Python, Streamlit & spaCy NLP"
)

# ---------------- MAIN TITLE ----------------

st.title("📄 Intelligent Resume Parser using NLP")

st.caption(
    "Upload resumes, extract candidate information, and rank candidates using JD matching."
)

st.divider()

# ---------------- FILE UPLOAD ----------------

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"]
)

if uploaded_file is not None:

    # Create resumes folder
    os.makedirs("resumes", exist_ok=True)

    # Save uploaded file
    file_path = os.path.join(
        "resumes",
        uploaded_file.name
    )

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("File uploaded successfully!")

    # Extract text from resume
    if uploaded_file.name.endswith(".pdf"):

        resume_text = extract_text_from_pdf(file_path)

    elif uploaded_file.name.endswith(".docx"):

        resume_text = extract_text_from_docx(file_path)

    # Extract candidate information
    email = extract_email(resume_text)

    phone = extract_phone(resume_text)

    name = extract_name(resume_text)

    skills = extract_skills(resume_text)

    education = extract_education(resume_text)

    experience = extract_experience(resume_text)

    # Save candidate to database
    saved = save_candidate(
        name,
        email,
        phone,
        skills,
        education,
        experience
    )

    if saved:
        st.success("Candidate saved to database!")

    else:
        st.warning("Candidate already exists in database!")

    st.divider()

    # ---------------- CANDIDATE INFO ----------------

    st.subheader("Candidate Information")

    col1, col2 = st.columns(2)

    with col1:

        st.write(f"👤 **Name:** {name}")

        st.write(f"📧 **Email:** {email}")

        st.write(f"📞 **Phone:** {phone}")

    with col2:

        st.write(f"🛠️ **Skills:** {', '.join(skills)}")

        st.write(f"🎓 **Education:** {', '.join(education)}")

        st.write(f"💼 **Experience:** {', '.join(experience)}")

    st.divider()

    # ---------------- METRICS ----------------

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric(
        "Skills Found",
        len(skills)
    )

    metric2.metric(
        "Education Matches",
        len(education)
    )

    metric3.metric(
        "Experience Entries",
        len(experience)
    )

    st.divider()

    # ---------------- RESUME TEXT ----------------

    with st.expander("View Extracted Resume Text"):

        st.text_area(
            "Resume Content",
            resume_text,
            height=350
        )

# ---------------- ALL CANDIDATES ----------------

st.subheader("Candidate Database")

candidates = get_all_candidates()

candidate_data = []

for candidate in candidates:

    candidate_data.append({

        "Name": candidate[1],

        "Email": candidate[2],

        "Skills": candidate[4],

        "Education": candidate[5]
    })

if candidate_data:

    df = pd.DataFrame(candidate_data)

    st.dataframe(
        df,
        use_container_width=True
    )

st.divider()

# ---------------- JD MATCHING ----------------

if jd_text:

    st.subheader("JD Match Results")

    candidates = get_all_candidates()

    for candidate in candidates:

        result = match_candidate(
            candidate[4],
            jd_text
        )

        st.markdown("---")

        st.write(f"### {candidate[1]}")

        st.progress(result["score"] / 100)

        score = result['score']

        color = (
            "🟢" if score >= 70
            else "🟡" if score >= 40
            else "🔴"
        )

        st.write(
            f"**Match Score:** {color} {score}%"
        )

        st.write(
            f"**Matched Skills:** {', '.join(result['matched'])}"
        )

        st.write(
            f"**Missing Skills:** {', '.join(result['missing'])}"
        )

    st.divider()

    # ---------------- TOP CANDIDATE ----------------

    st.subheader("Top Candidate")

    ranked_candidates = []

    for candidate in candidates:

        result = match_candidate(
            candidate[4],
            jd_text
        )

        score = result["score"]

        ranked_candidates.append(
            (candidate[1], score)
        )

    ranked_candidates.sort(
        key=lambda x: x[1],
        reverse=True
    )

    top_candidate = ranked_candidates[0]

    st.success(
        f"🏆 {top_candidate[0]} is the best match with {top_candidate[1]}%"
    )

    st.divider()

    # ---------------- RANKING TABLE ----------------

    st.subheader("Candidate Rankings")

    ranking_data = []

    for index, candidate in enumerate(
        ranked_candidates,
        start=1
    ):

        score = candidate[1]

        if index == 1:
            medal = "🥇"

        elif index == 2:
            medal = "🥈"

        elif index == 3:
            medal = "🥉"

        else:
            medal = f"#{index}"

        ranking_data.append({

            "Rank": medal,

            "Name": candidate[0],

            "Match Score": f"{score}%"
        })

    ranking_df = pd.DataFrame(ranking_data)

    st.dataframe(
        ranking_df,
        use_container_width=True
    )