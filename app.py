import streamlit as st
import os

st.title("Intelligent Resume Parsing System")

st.write("Upload a resume to begin parsing.")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx"]
)

if uploaded_file is not None:

    # Create resumes folder if it doesn't exist
    os.makedirs("resumes", exist_ok=True)

    # File path
    file_path = os.path.join("resumes", uploaded_file.name)

    # Save uploaded file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("File uploaded and saved successfully!")

    st.write("Filename:", uploaded_file.name)