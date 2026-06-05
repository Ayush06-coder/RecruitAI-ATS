import sys
import os
sys.path.append(os.path.dirname(__file__)) 

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil

from database import (
    init_db,
    save_candidate,
    get_all_candidates,
    search_candidates,
    delete_candidate,
    init_jobs_db,
    create_job,
    get_all_jobs,
    get_job_by_id,
    update_job_status,
    delete_job,
    save_application,
    get_applications_by_job,
    update_application_status
)

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
init_jobs_db()

# ---------------- MODELS ----------------

class MatchRequest(BaseModel):
    jd_text: str
    job_title: str = ""

class JobRequest(BaseModel):
    title: str
    department: str
    location: str
    experience: str
    description: str
    required_skills: str
    required_certifications: str
    posted_by: str

class ApplicationStatusRequest(BaseModel):
    status: str

class JobStatusRequest(BaseModel):
    status: str

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

# ============ JOB ENDPOINTS ============

@app.post("/jobs")
def post_job(job: JobRequest):
    create_job(
        job.title, job.department, job.location,
        job.experience, job.description,
        job.required_skills, job.required_certifications,
        job.posted_by
    )
    return {"message": "Job posted successfully"}


@app.get("/jobs")
def list_jobs():
    jobs = get_all_jobs()
    result = []
    for j in jobs:
        result.append({
            "id": j[0],
            "title": j[1],
            "department": j[2],
            "location": j[3],
            "experience": j[4],
            "description": j[5],
            "required_skills": j[6],
            "required_certifications": j[7],
            "posted_date": j[8],
            "status": j[9],
            "posted_by": j[10]
        })
    return {"jobs": result}


@app.get("/jobs/{job_id}")
def get_job(job_id: int):
    job = get_job_by_id(job_id)
    if not job:
        return {"error": "Job not found"}
    return {
        "id": job[0],
        "title": job[1],
        "department": job[2],
        "location": job[3],
        "experience": job[4],
        "description": job[5],
        "required_skills": job[6],
        "required_certifications": job[7],
        "posted_date": job[8],
        "status": job[9],
        "posted_by": job[10]
    }


@app.put("/jobs/{job_id}")
def update_job(job_id: int, request: JobStatusRequest):
    update_job_status(job_id, request.status)
    return {"message": "Job status updated"}


@app.delete("/jobs/{job_id}")
def remove_job(job_id: int):
    delete_job(job_id)
    return {"message": "Job deleted"}


@app.post("/jobs/{job_id}/apply")
async def apply_to_job(job_id: int, file: UploadFile = File(...)):

    job = get_job_by_id(job_id)
    if not job:
        return {"error": "Job not found"}

    # Save resume
    os.makedirs("resumes", exist_ok=True)
    file_path = os.path.join("resumes", file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Extract text
    if file.filename.endswith(".pdf"):
        resume_text = extract_text_from_pdf(file_path)
    elif file.filename.endswith(".docx"):
        resume_text = extract_text_from_docx(file_path)
    else:
        return {"error": "Unsupported format"}

    # Extract candidate info
    name = extract_name(resume_text)
    email = extract_email(resume_text)
    skills = extract_skills(resume_text)
    certifications = extract_certifications(resume_text)
    experience = extract_experience(resume_text)

    # Calculate match against job
    required_skills = job[6]
    required_certs = job[7]
    job_description = job[5]

    result = match_candidate(
        ", ".join(skills),
        job_description + " " + required_skills,
        ", ".join(experience),
        ", ".join(certifications)
    )

    # Save application
    saved = save_application(
        job_id, name, email,
        ", ".join(skills),
        ", ".join(certifications),
        result["score"],
        result["skills_score"],
        result["experience_score"],
        result["certifications_score"],
        file_path
    )

    if not saved:
        return {"error": "Already applied to this job"}

    return {
        "message": "Application submitted successfully",
        "name": name,
        "email": email,
        "match_score": result["score"],
        "skills_score": result["skills_score"],
        "experience_score": result["experience_score"],
        "certifications_score": result["certifications_score"],
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"]
    }


@app.get("/jobs/{job_id}/applications")
def get_job_applications(job_id: int):
    applications = get_applications_by_job(job_id)
    result = []
    for a in applications:
        result.append({
            "id": a[0],
            "job_id": a[1],
            "name": a[2],
            "email": a[3],
            "skills": a[4],
            "certifications": a[5],
            "match_score": a[6],
            "skills_score": a[7],
            "experience_score": a[8],
            "certifications_score": a[9],
            "status": a[10],
            "applied_date": a[11]
        })
    return {"applications": result}


@app.put("/applications/{application_id}")
def update_status(application_id: int, request: ApplicationStatusRequest):
    update_application_status(application_id, request.status)
    return {"message": "Application status updated"}