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

    for i in range(len(lines[:10]) - 1):
        w1, w2 = lines[i], lines[i + 1]

        if (
            w1.isupper() and w2.isupper()
            and len(w1.split()) == 1
            and len(w2.split()) == 1
            and w1.title() not in headings
            and w2.title() not in headings
        ):
            return f"{w1} {w2}".title()

    text_for_nlp = " ".join(
        line.title() if line.isupper() else line
        for line in lines[:10]
    )

    doc = nlp(text_for_nlp)

    for ent in doc.ents:
        if ent.label_ == "PERSON" and len(ent.text.split()) >= 2:
            return ent.text

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
    text_lower = text.lower()
    found_skills = []

    for skill in SKILLS_LIST:
        if skill.lower() in text_lower:
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