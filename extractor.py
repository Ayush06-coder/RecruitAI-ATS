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
    lines = text.split("\n")
    cleaned_lines = [line.strip() for line in lines if line.strip()]

    headings = {
        "Resume", "Cv", "Curriculum", "Vitae", "Profile", "Portfolio",
        "Summary", "Education", "Experience", "Skills", "Objective",
        "Contact", "References"
    }

    # Handle name split across lines: AYUSH \n SAWHNEY
    for i in range(len(cleaned_lines[:10]) - 1):
        w1 = cleaned_lines[i].strip()
        w2 = cleaned_lines[i+1].strip()
        if (len(w1.split()) == 1 and len(w2.split()) == 1
                and w1.isupper() and w2.isupper()
                and w1.title() not in headings
                and w2.title() not in headings):
            return (w1 + " " + w2).title()

    # NLP for everything else
    normalized = []
    for line in cleaned_lines[:10]:
        normalized.append(line.title() if line.isupper() else line)

    doc = nlp(" ".join(normalized))
    for entity in doc.ents:
        if entity.label_ == "PERSON" and len(entity.text.split()) >= 2:
            return entity.text

    return "Name not found"