import streamlit as st
import os

from parser import (
    extract_text_from_pdf,
    extract_text_from_docx
)

from extractor import (
    extract_email,
    extract_phone,
    extract_name,
    extract_skills,
    extract_education
)

st.title("AI Resume Parser")

st.write("Upload a resume to begin parsing.")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"]
)

if uploaded_file is not None:

    # Create folder
    os.makedirs("resumes", exist_ok=True)

    # Save file
    file_path = os.path.join(
        "resumes",
        uploaded_file.name
    )

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("File uploaded successfully!")

    # Extract text
    if uploaded_file.name.endswith(".pdf"):

        resume_text = extract_text_from_pdf(file_path)

    elif uploaded_file.name.endswith(".docx"):

        resume_text = extract_text_from_docx(file_path)
    
    # Extract information
    email = extract_email(resume_text)
    phone = extract_phone(resume_text)
    name = extract_name(resume_text)
    skills = extract_skills(resume_text)
    education = extract_education(resume_text)
   
    # Display extracted information
    st.subheader("Extracted Information")

    st.write("Email:", email)
    st.write("Phone:", phone)
    st.write("Name:", name)
    st.write("Skills:", ", ".join(skills))
    st.write("Education:", ", ".join(education))
    
    # Display extracted text
    st.subheader("Extracted Resume Text")

    st.text_area(
        "Resume Content",
        resume_text,
        height=400
    )