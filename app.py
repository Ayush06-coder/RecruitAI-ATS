import streamlit as st
import os

from parser import (
    extract_text_from_pdf,
    extract_text_from_docx
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

    # Display extracted text
    st.subheader("Extracted Resume Text")

    st.text_area(
        "Resume Content",
        resume_text,
        height=400
    )