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

# AI Job Match Analyzer
NLP app to score your resume against any job description and highlight missing skills.

## Instructions
1) Upload your resume (PDF or text)
2) Paste job description or job links (Internshala, LinkedIn, Naukri, Indeed, etc.)
3) See match score and missing skills

![App Screenshot](screenshot.png)

## Overview
**Problem Description**: Job seekers often apply blindly to roles where they miss keyword filters. This app acts as an ATS scanner to highlight missing skills before applying.
**Dataset / Sample File**: Pre-loaded with a comprehensive 500+ skill taxonomy mapped to real-world tech and business domains. Users provide their own Resume (PDF/DOCX) and Job URLs.
**Algorithm Used**: NLP with Regex pattern matching, text tokenization, and custom scoring heuristics based on weighted skill categorization (Hard Skills vs Soft Skills). Web scraping implemented via BeautifulSoup4.
**Evaluation Metrics**: Evaluated primarily on **Resume Match %** (alignment of skills) and **ATS Score** (readability and keyword optimization format).
**Insight**: Grouping skills by synonyms (e.g., 'React' vs 'ReactJS') significantly reduced false negatives in skill gap reporting. Moving from simple word counts to weighted keyword extractions provided more realistic ATS simulations.

## Links
- **Live Demo**: [https://huggingface.co/spaces/hishitm/ai-job-match-analyser](https://huggingface.co/spaces/hishitm/ai-job-match-analyser)
- **GitHub**: [https://github.com/hishitm/ai-job-match-analyser](https://github.com/hishitm/ai-job-match-analyser)

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
