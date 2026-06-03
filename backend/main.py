import sys
import os

sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil

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
    extract_certifications,
    match_candidate
)

from database import (
    init_db,
    save_candidate,
    get_all_candidates,
    search_candidates,
    delete_candidate,
)

# ---------------- APP SETUP ----------------

app = FastAPI(
    title="Resume Parser API",
    description="API for parsing resumes and matching candidates",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

init_db()

# ---------------- MODELS ----------------

class MatchRequest(BaseModel):
    jd_text: str
    job_title: str = ""

# ---------------- ROUTES ----------------

@app.get("/")
def home():
    return {"message": "Resume Parser API is running"}


@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    os.makedirs("resumes", exist_ok=True)
    file_path = os.path.join("resumes", file.filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    if file.filename.endswith(".pdf"):
        resume_text = extract_text_from_pdf(file_path)
    elif file.filename.endswith(".docx"):
        resume_text = extract_text_from_docx(file_path)
    else:
        return {"error": "Unsupported file format"}

    name = extract_name(resume_text)
    email = extract_email(resume_text)
    phone = extract_phone(resume_text)
    skills = extract_skills(resume_text)
    education = extract_education(resume_text)
    experience = extract_experience(resume_text)
    certifications = extract_certifications(resume_text)

    saved = save_candidate(
        name, email, phone, skills, education, experience, certifications
    )

    return {
        "saved": saved,
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "education": education,
        "experience": experience,
        "certifications": certifications,
    }


@app.get("/candidates")
def get_candidates(search: str = ""):
    if search:
        candidates = search_candidates(search)
    else:
        candidates = get_all_candidates()

    result = []
    for c in candidates:
        result.append({
            "id": c[0],
            "name": c[1],
            "email": c[2],
            "phone": c[3],
            "skills": c[4],
            "education": c[5],
            "experience": c[6]
        })

    return {"candidates": result}


@app.get("/candidate/{candidate_id}")
def get_candidate(candidate_id: int):
    candidates = get_all_candidates()

    for c in candidates:
        if c[0] == candidate_id:
            return {
                "id": c[0],
                "name": c[1],
                "email": c[2],
                "phone": c[3],
                "skills": c[4],
                "education": c[5],
                "experience": c[6]
            }

    return {"error": "Candidate not found"}


@app.post("/match")
def match_candidates(request: MatchRequest):
    candidates = get_all_candidates()
    results = []

    for c in candidates:
        candidate_experience = c[6] if len(c) > 6 else ""
        candidate_certifications = c[7] if len(c) > 7 else ""
        result = match_candidate(
            c[4],
            request.jd_text,
            candidate_experience=candidate_experience,
            candidate_certifications=candidate_certifications,
            job_title=request.job_title,
        )
        results.append({
            "name": c[1],
            "email": c[2],
            "score": result["score"],
            "matched_skills": result["matched_skills"],
            "missing_skills": result["missing_skills"],
            "matched_experience": result["matched_experience"],
            "matched_certifications": result["matched_certifications"],
            "skills_score": result["skills_score"],
            "experience_score": result["experience_score"],
            "certifications_score": result["certifications_score"],
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return {"results": results}


@app.delete("/candidate/{candidate_id}")
def delete_candidate_by_id(candidate_id: int):
    deleted = delete_candidate(candidate_id)
    if not deleted:
        return {"deleted": False, "message": "Candidate not found"}
    return {"deleted": True}