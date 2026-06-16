import re

import spacy
nlp = spacy.load("en_core_web_lg")

def extract_email(text):
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    match = re.search(pattern, text)
    if match:
        return match.group()
    return "Email not found"

def extract_phone(text):
    pattern = r"\+?\d[\d\s\-]{8,15}"
    match = re.search(pattern, text)
    if match:
        return match.group()
    return "Phone number not found"

def extract_name(text):
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    headings = {
        "Resume", "Cv", "Curriculum", "Vitae", "Profile",
        "Summary", "Education", "Experience", "Skills",
        "Objective", "Contact", "References"
    }

    job_titles = {
        "junior", "senior", "developer", "engineer", "analyst",
        "manager", "designer", "lead", "frontend", "backend",
        "fullstack", "full-stack", "full", "stack", "software",
        "intern", "consultant", "architect", "executive",
        "associate", "trainee", "assistant", "scientist",
        "officer", "head", "director", "specialist", "coordinator",
        "administrator", "representative", "supervisor", "technician",
        "operator", "consultant", "freelance", "contractor"
    }

    # Strategy 1: Look for two consecutive uppercase single-word lines (common resume format)
    for i in range(len(lines[:10]) - 1):
        w1, w2 = lines[i], lines[i + 1]

        if (
            w1.isupper() and w2.isupper()
            and len(w1.split()) == 1
            and len(w2.split()) == 1
            and w1.title() not in headings
            and w2.title() not in headings
            and w1.lower() not in job_titles
            and w2.lower() not in job_titles
        ):
            return f"{w1} {w2}".title()

    # Strategy 2: Use spaCy NER with strict job title filtering
    text_for_nlp = " ".join(
        line.title() if line.isupper() else line
        for line in lines[:10]
    )

    doc = nlp(text_for_nlp)

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            words = ent.text.split()

            # Stop at job title words - STRICT filtering
            clean_words = []
            for word in words:
                # Check if word (or stripped version) is a job title
                word_clean = word.strip().lower().rstrip(",.:;-|")
                if word_clean in job_titles:
                    break
                # Also check if word contains job title as substring
                if any(jt in word_clean for jt in ["developer", "engineer", "analyst", "manager", "designer", "consultant", "architect", "intern", "trainee", "assistant"]):
                    break
                clean_words.append(word)

            # Only return if at least 2 clean words remain (First + Last name)
            if len(clean_words) >= 2:
                # Additional validation: check if result looks like a name
                result = " ".join(clean_words)
                # Make sure it doesn't end with a job title word
                last_word = clean_words[-1].lower().rstrip(",.:;-|")
                if last_word not in job_titles:
                    return result

    return "Name not found"

SKILLS_LIST = [
    "Python", "Java", "C", "C++", "C#", "JavaScript", "TypeScript",
    "R", "Swift", "Kotlin", "Go", "Rust", "PHP", "Ruby", "Scala",
    "HTML", "CSS", "React", "Angular", "Vue", "Node.js", "Django",
    "Flask", "FastAPI", "REST API", "GraphQL",
    "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
    "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "Pandas",
    "NumPy", "Matplotlib", "Seaborn",
    "SQL", "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Redis",
    "Git", "GitHub", "Docker", "Kubernetes", "AWS", "Azure", "GCP",
    "Linux", "Streamlit", "Power BI", "Tableau", "Excel",
    "Data Structures", "Algorithms", "OOP", "System Design",
]

def extract_skills(text):
    found_skills = []
    for skill in SKILLS_LIST:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            found_skills.append(skill)
    return found_skills if found_skills else ["No skills found"]

EDUCATION_KEYWORDS = [
    "b.tech", "m.tech", "btech", "mtech", "b.e", "m.e",
    "b.sc", "m.sc", "bsc", "msc", "bca", "mca", "bba", "mba",
    "bachelor", "master", "phd", "doctorate", "diploma",
    "b.com", "m.com", "b.a", "m.a"
]

UNIVERSITY_KEYWORDS = [
    "university", "college", "institute", "iit", "nit",
    "bits", "amity", "vit", "manipal", "school of"
]

def extract_education(text):
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    section_keywords = ["education", "qualification", "academic"]
    stop_keywords = ["experience", "skills", "projects",
                     "certifications", "summary", "objective"]
    keywords = EDUCATION_KEYWORDS + UNIVERSITY_KEYWORDS

    education_lines = []
    in_education_section = False

    for line in lines:
        line_lower = line.lower()

        if any(kw in line_lower for kw in section_keywords):
            in_education_section = True
            continue

        if in_education_section and any(kw in line_lower for kw in stop_keywords):
            break

        if in_education_section:
            education_lines.append(line)

    found_education = [
        line for line in education_lines
        if any(kw in line.lower() for kw in keywords)
    ]

    return found_education if found_education else ["Education not found"]

ROLE_KEYWORDS = [
    "intern", "internship", "engineer", "developer", "analyst",
    "manager", "consultant", "designer", "architect", "lead",
    "executive", "associate", "trainee", "assistant", "scientist"
]

COMPANY_KEYWORDS = [
    "technologies", "solutions", "systems", "services", "consulting",
    "software", "tech", "labs", "pvt", "ltd", "inc", "limited",
    "corp", "group", "studio"
]

def extract_experience(text):
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    section_keywords = ["experience", "employment", "work history", "internship"]
    stop_keywords = ["education", "skills", "projects", "certifications",
                     "achievements", "objective", "summary"]

    experience_lines = []
    in_experience_section = False

    for line in lines:
        line_lower = line.lower()

        if any(kw in line_lower for kw in section_keywords):
            in_experience_section = True
            continue

        if in_experience_section and any(kw in line_lower for kw in stop_keywords):
            break

        if in_experience_section:
            experience_lines.append(line)

    roles = []
    companies = []

    for line in experience_lines:
        line_lower = line.lower()
        if any(kw in line_lower for kw in ROLE_KEYWORDS) and line not in roles:
            roles.append(line)
        elif any(kw in line_lower for kw in COMPANY_KEYWORDS) and line not in companies:
            companies.append(line)

    result = roles + companies
    return result if result else ["Experience not found"]

CERTIFICATIONS_LIST = [
    "AWS Certified Solutions Architect", "AWS Certified Developer",
    "AWS Certified SysOps Administrator", "AWS Certified", "Google Cloud Professional",
    "Google Cloud", "Microsoft Azure", "Azure Administrator", "Azure Fundamentals",
    "PMP", "Certified Scrum Master", "Scrum Master", "Scrum", "CPA", "CFA",
    "CISSP", "CompTIA Security+", "CompTIA Network+", "CompTIA A+",
    "Oracle Certified Professional", "Oracle Certified", "Oracle",
    "Salesforce Certified Administrator", "Salesforce Certified", "Salesforce",
    "HubSpot Inbound", "HubSpot", "TensorFlow Developer Certificate",
    "TensorFlow Developer", "CKA", "CKAD", "CCNA", "CCNP", "ITIL",
    "Six Sigma Green Belt", "Six Sigma", "PHR", "SHRM-CP",
]

def extract_certifications(text):
    found_certifications = []
    for cert in CERTIFICATIONS_LIST:
        pattern = r'\b' + re.escape(cert) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            found_certifications.append(cert)
    return found_certifications if found_certifications else ["No certifications found"]

def _whole_word_match(term, text):
    pattern = r'\b' + re.escape(term) + r'\b'
    return bool(re.search(pattern, text, re.IGNORECASE))

def match_candidate(
    candidate_skills,
    jd_text,
    candidate_experience="",
    candidate_certifications="",
    job_title="",
):
    jd_skills = extract_skills(jd_text)
    jd_skills = [s for s in jd_skills if s != "No skills found"]

    matched_skills = []
    missing_skills = []
    for skill in jd_skills:
        if _whole_word_match(skill, candidate_skills):
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    total_skills = len(jd_skills)
    skills_score = round((len(matched_skills) / total_skills) * 100) if total_skills > 0 else 0

    # Experience: JD skills + job title words vs candidate experience text
    job_title_words = [
        w for w in re.split(r"[\s,/-]+", job_title.strip())
        if len(w) >= 2
    ]
    experience_keywords = list(dict.fromkeys(jd_skills + job_title_words))
    experience_text = candidate_experience if candidate_experience else ""

    matched_experience = []
    for keyword in experience_keywords:
        if _whole_word_match(keyword, experience_text):
            matched_experience.append(keyword)

    total_exp = len(experience_keywords)
    experience_score = (
        round((len(matched_experience) / total_exp) * 100) if total_exp > 0 else 0
    )

    # Certifications: certs mentioned in JD vs candidate certifications
    jd_certifications = extract_certifications(jd_text)
    jd_certifications = [c for c in jd_certifications if c != "No certifications found"]
    certs_text = candidate_certifications if candidate_certifications else ""

    matched_certifications = []
    for cert in jd_certifications:
        if _whole_word_match(cert, certs_text):
            matched_certifications.append(cert)

    total_certs = len(jd_certifications)
    certifications_score = (
        round((len(matched_certifications) / total_certs) * 100) if total_certs > 0 else 0
    )

    score = round(
        (skills_score * 0.60)
        + (experience_score * 0.25)
        + (certifications_score * 0.15)
    )

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "matched_experience": matched_experience,
        "matched_certifications": matched_certifications,
        "skills_score": skills_score,
        "experience_score": experience_score,
        "certifications_score": certifications_score,
    }