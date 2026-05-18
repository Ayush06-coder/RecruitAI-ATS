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