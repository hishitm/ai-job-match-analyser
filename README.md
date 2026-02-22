---
title: AI Job Match Analyser
emoji: 🎯
colorFrom: purple
colorTo: cyan
sdk: docker
app_port: 7860
pinned: false
license: mit
short_description: Paste job links + upload resume → ATS score, match %, skill gaps & improvements
---

# 🎯 AI Job Match Analyser

Upload your resume and paste job links from **Internshala, LinkedIn, Naukri, Indeed** and more.
Get an instant AI-powered breakdown of:

- **Match Score** — how well your skills align with the job
- **ATS Score** — how resume-scanner-friendly your CV is
- **Skill Gaps** — skills you have vs. skills the job needs
- **Insights** — personalised analysis of your candidacy
- **Improvements** — actionable tips to increase your chances

## 🚀 How to Use

1. Paste 1–5 job posting URLs into the **Job Links** panel
2. Upload your **resume/CV** (PDF or DOCX)
3. Click **Analyse My Profile**
4. Review your scores, insights, and improvement suggestions

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + Vite, Vanilla CSS (dark glassmorphism) |
| Backend  | FastAPI + Uvicorn (Python) |
| NLP      | Regex + curated 500-skill taxonomy |
| Scraping | BeautifulSoup4 + requests |
| Deploy   | Hugging Face Spaces (Docker) |

## 🗂 Supported Platforms

- Internshala ✅
- LinkedIn ✅
- Naukri ✅
- Indeed ✅
- Glassdoor ✅
- Wellfound / AngelList ✅
- Any generic job URL ✅

## 📁 Project Structure

```
ai-job-match-analyser/
├── backend/
│   ├── main.py             # FastAPI app + static serving
│   ├── scraper.py          # Multi-platform job URL scraper
│   ├── parser.py           # PDF/DOCX resume text extraction
│   ├── skill_extractor.py  # NLP skill extraction & clustering
│   ├── ats_scorer.py       # ATS score with 6 dimensions
│   ├── scorer.py           # Match score, insights, improvements
│   ├── job_matcher.py      # Job role templates
│   ├── skills_taxonomy.py  # 500+ skills taxonomy
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── components/     # All UI components
│   ├── package.json
│   └── vite.config.js
├── Dockerfile
└── README.md
```

## 🏃 Run Locally

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 7860

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
# Visit http://localhost:5173
```

## 🐳 Docker

```bash
docker build -t ai-job-match .
docker run -p 7860:7860 ai-job-match
# Visit http://localhost:7860
```
