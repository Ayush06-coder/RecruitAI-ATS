# 📄 RecruitAI — Intelligent Resume Parser & Hiring Platform

&gt; An AI-powered recruitment platform with role-based access. Candidates apply to jobs without login. Recruiters login to manage applications, rank candidates, and post jobs with auto-generated JDs.

---

## 🧠 What This Project Does

Companies receive hundreds of resumes for each job posting. Manual screening is slow and biased. This platform solves that by:

- **Public Job Board** — Candidates view open jobs and apply without any login
- **AI Resume Parsing** — Automatically extracts name, email, phone, skills, education, experience, certifications from PDF/DOCX
- **Smart Matching** — Calculates match scores (skills + experience + certifications) against job requirements
- **Candidate Ranking** — Ranks applicants with medals and progress bars
- **Auto JD Generation** — Admin generates professional job descriptions with one click
- **Role-Based Access** — Three user types: Candidate (public), Recruiter (user), Admin

---

## ✨ Features

| Feature | Description |
|---|---|
| 📤 Public Apply | Candidates apply to jobs without login |
| 🧠 NLP Extraction | spaCy-powered extraction of all candidate details |
| 🎯 AI Match Scoring | Skills + Experience + Certifications breakdown |
| 🏆 Ranked Applications | Top 3 get medals, progress bars for all |
| 💼 Job Posting | Admin posts jobs with auto-generated descriptions |
| ✨ Auto JD Generation | One-click professional job description generation |
| 🔐 Authentication | Admin vs User roles with password management |
| 📊 Analytics Dashboard | Charts for skills, education, experience distribution |
| 👥 Candidate Database | Search, filter, and admin-only delete |
| 🔍 Track Application | Candidates track status via email |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit (Multi-page + st.navigation) |
| Backend | FastAPI + Uvicorn |
| NLP | spaCy (en_core_web_lg) + Regex |
| Database | SQLite |
| Auth | Bcrypt password hashing |
| Styling | Custom CSS (Dark cyan/teal theme) |
| Language | Python 3.10+ |

---

## 📁 Project Structure
resume-parser-project/
├── App.py                          ← Navigation controller + Home page content
├── auth.py                         ← Login/logout, roles, password management
├── styles.py                       ← Shared dark CSS (cyan/teal theme)
├── config.py                       ← Centralized API URL configuration
├── requirements.txt
│
├── backend/
│   ├── main.py                     ← FastAPI endpoints (upload, match, jobs, applications, generate-jd)
│   ├── parser.py                   ← PDF/DOCX text extraction
│   ├── extractor.py                ← NLP: name, email, phone, skills, education, experience, certifications
│   └── database.py                 ← SQLite: candidates, jobs, applications, users
│
├── database/
│   └── resumes.db                  ← SQLite database
│
├── pages/
│   ├── Home.py                     ← Public landing page with job listings
│   ├── Apply.py                    ← Candidate application form (no login)
│   ├── Track.py                    ← Track application by email (no login)
│   ├── Login.py                    ← Company login page
│   ├── Dashboard.py                ← Company overview after login
│   ├── Applications.py             ← View applications per job, ranked by match
│   ├── JD_Matching.py             ← Match candidates against JD
│   ├── Analytics.py                ← Charts: skills, education, experience breakdown
│   ├── Admin.py                    ← Admin only: users, jobs, applications
│   ├── Candidates.py              ← View all candidates (search, filter, admin delete)
│   └── Change_Password.py          ← Password change (first-time + optional)
│
└── resumes/                        ← Uploaded resume files

---

## 🔄 Workflow

### Candidate Flow (No Login)
1. Visits public landing page → sees open jobs
2. Clicks "Apply" on a job → fills form + uploads resume
3. Gets instant match score with breakdown
4. Can track application status via email

### Company Flow (Login Required)
1. Admin/User logs in → sees Dashboard
2. Dashboard shows metrics: Total Jobs, Candidates, Applications
3. Applications page → select job → see ranked applicants
4. Can shortlist, schedule interview, or reject
5. JD Matching → paste JD → see ranked candidates
6. Analytics → visual breakdown of all candidates
7. Admin can post jobs, manage users, delete candidates

---

## ▶️ Running the Project

**Prerequisites:**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_lg

Open two separate terminals:
Terminal 1 — FastAPI Backend:
uvicorn backend.main:app --reload --port 8000
Terminal 2 — Streamlit Frontend:
streamlit run App.py

| Service       | URL                          |
| ------------- | ---------------------------- |
| Streamlit App | <http://localhost:8501>      |
| FastAPI Docs  | <http://localhost:8000/docs> |

🔌 API Endpoints
| Method   | Endpoint                  | Description                              |
| -------- | ------------------------- | ---------------------------------------- |
| `GET`    | `/`                       | Health check                             |
| `POST`   | `/upload`                 | Upload resume, parse and extract info    |
| `GET`    | `/candidates`             | Fetch all candidates (optional ?search=) |
| `DELETE` | `/candidates/{id}`        | Delete candidate (admin)                 |
| `POST`   | `/match`                  | Match candidates against JD              |
| `POST`   | `/generate-jd`            | Auto-generate job description            |
| `POST`   | `/jobs`                   | Post new job                             |
| `GET`    | `/jobs`                   | List all jobs                            |
| `PUT`    | `/jobs/{id}`              | Update job status (open/closed)          |
| `DELETE` | `/jobs/{id}`              | Delete job                               |
| `POST`   | `/jobs/{id}/apply`        | Apply to job with resume                 |
| `GET`    | `/jobs/{id}/applications` | Get applications for job                 |
| `PUT`    | `/applications/{id}`      | Update application status                |
| `GET`    | `/track/{email}`          | Track applications by email              |

🔐 Default Credentials
| Role  | Username             | Password         | Notes                      |
| ----- | -------------------- | ---------------- | -------------------------- |
| Admin | `admin`              | `RecruitAI@2026` | Must change on first login |
| User  | Any created by admin | `ChangeMe@123`   | Must change on first login |

🎨 UI Theme
Dark background: #070711
Primary accent: Cyan/Teal (#22d3ee, #0891b2)
Cards: Glassmorphism with subtle borders
Progress bars: Gradient cyan
Status badges: Color-coded (green, yellow, red, purple)

📸 Screenshots
| Page         | Screenshot                     |
| ------------ | ------------------------------ |
| Landing Page | `Screenshots/Landing.png`      |
| Apply Page   | `Screenshots/Apply.png`        |
| Login Page   | `Screenshots/Login.png`        |
| Dashboard    | `Screenshots/Dashboard.png`    |
| Applications | `Screenshots/Applications.png` |
| JD Matching  | `Screenshots/JD_Matching.png`  |
| Analytics    | `Screenshots/Analytics.png`    |
| Admin Panel  | `Screenshots/Admin.png`        |
| Candidates   | `Screenshots/Candidates.png`   |

📦 Dependencies
See requirements.txt for full list. Key packages:
streamlit — Frontend UI
fastapi + uvicorn — Backend API
spacy + en_core_web_lg — NLP processing
bcrypt — Password hashing
pdfplumber — PDF text extraction
python-docx — DOCX text extraction
pandas — Data tables
requests — HTTP calls
python-dotenv — Environment variables

🌿 Git Branches
| Branch                | Description                                    |
| --------------------- | ---------------------------------------------- |
| `main`                | Current stable version with full workflow      |
| `workflow-redesign`   | Merged — public apply flow + company dashboard |
| `navigation-redesign` | Merged — role-based sidebar with st.navigation |

👨‍💻 Author
Ayush Sawhney
B.Tech Computer Science Engineering — Amity University, Noida
GitHub: https://github.com/Ayush06-coder

📌 Project Status
🟢 Active Development — Internship Project

Built with Python · FastAPI · Streamlit · spaCy · SQLite · Bcrypt
