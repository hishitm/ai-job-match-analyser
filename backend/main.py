"""
FastAPI main application — AI Job Match Analyser
- POST /api/analyse  → resume file + job URL(s) → full analysis
- GET  /health       → health check
- Serves built React frontend on all other routes
- Port 7860 (Hugging Face Spaces requirement)
"""

import os
import json
import asyncio
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

try:
    from parser import parse_resume
    from skill_extractor import extract_skills_from_text
    from scraper import scrape_job
    from ats_scorer import score_ats
    from scorer import score_match
except ImportError:
    from backend.parser import parse_resume
    from backend.skill_extractor import extract_skills_from_text
    from backend.scraper import scrape_job
    from backend.ats_scorer import score_ats
    from backend.scorer import score_match

app = FastAPI(
    title="CareerPath - Professional Job Matcher",
    description="Upload your resume and paste job links — get compatibility scores, career insights & tailored improvements.",
    version="2.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

executor = ThreadPoolExecutor(max_workers=4)


# ─── Health ─────────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok", "version": "2.0.0"}


# ─── Main Analysis Endpoint ─────────────────────────────────────────────────

@app.post("/api/analyse")
async def analyse(
    file: UploadFile = File(...),
    job_urls: str = Form(...)          # JSON array of URLs as string
):
    """
    Accepts:
      - file       : PDF or DOCX resume
      - job_urls   : JSON-encoded list of job posting URLs

    Returns full analysis:
      - Resume skill extraction + ATS score
      - Per-job: match score, fit label, probability, matched/missing skills,
        insights, improvements
    """

    # ── Validate file ────────────────────────────────────────────────────────
    if not file.filename:
        raise HTTPException(400, "No filename provided.")
    if not file.filename.lower().endswith((".pdf", ".docx", ".doc")):
        raise HTTPException(400, "Please upload a PDF or DOCX file.")

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(400, "Uploaded file is empty.")
    if len(file_bytes) > 10 * 1024 * 1024:
        raise HTTPException(400, "File too large. Maximum 10 MB.")

    # ── Validate job URLs ────────────────────────────────────────────────────
    try:
        urls: List[str] = json.loads(job_urls)
    except Exception:
        raise HTTPException(400, "job_urls must be a valid JSON array of strings.")

    if not isinstance(urls, list) or len(urls) == 0:
        raise HTTPException(400, "Provide at least one job URL.")
    if len(urls) > 5:
        raise HTTPException(400, "Maximum 5 job URLs per request.")

    # Sanitise URLs
    valid_urls = []
    for u in urls:
        u = u.strip()
        if u and (u.startswith("http://") or u.startswith("https://")):
            valid_urls.append(u)
    if not valid_urls:
        raise HTTPException(400, "No valid URLs found. URLs must start with http:// or https://")

    # ── Parse Resume ─────────────────────────────────────────────────────────
    try:
        parsed = parse_resume(file_bytes, file.filename)
    except ValueError as e:
        raise HTTPException(422, str(e))

    resume_text = parsed["text"]

    # ── Extract Resume Skills ─────────────────────────────────────────────────
    skill_data = extract_skills_from_text(resume_text)

    # ── ATS Score (no JD yet — per-JD will also be computed per job) ─────────
    overall_ats = score_ats(resume_text, "")

    # ── Scrape Jobs & Score (in parallel) ────────────────────────────────────
    loop = asyncio.get_event_loop()

    def scrape_and_score(url: str) -> dict:
        try:
            job_data = scrape_job(url)
            jd_combined = (
                job_data.get("full", "") + " " +
                job_data.get("requirements", "") + " " +
                job_data.get("skills", "")
            )
            # ATS score with JD keyword context
            ats = score_ats(resume_text, jd_combined)
            # Match score
            match = score_match(skill_data["skills"], job_data)

            return {
                "success": True,
                "url": url,
                "job": {
                    "title": job_data.get("title", ""),
                    "company": job_data.get("company", ""),
                    "location": job_data.get("location", ""),
                    "platform": job_data.get("platform", "generic")
                },
                "compatibility_index": ats["compatibility_index"],
                "readiness_grade": ats["readiness_grade"],
                "readiness_summary": ats["summary"],
                "readiness_details": ats["details"],
                "match_score": match["match_score"],
                "match_label": match["fit_label"],
                "match_readiness": match["match_readiness"],
                "matched_skills": match["matched_skills"],
                "missing_skills": match["missing_skills"],
                "matched_by_category": match["matched_by_category"],
                "missing_by_category": match["missing_by_category"],
                "insights": match["insights"],
                "recommendations": match["recommendations"]
            }
        except Exception as e:
            return {
                "success": False,
                "url": url,
                "error": str(e)
            }

    # Run all scrape+score tasks concurrently
    tasks = [
        loop.run_in_executor(executor, scrape_and_score, url)
        for url in valid_urls
    ]
    job_results = list(await asyncio.gather(*tasks))

    return {
        "success": True,
        "resume": {
            "filename": parsed["filename"],
            "file_type": parsed["file_type"],
            "word_count": parsed["word_count"]
        },
        "resume_skills": skill_data["skills"],
        "skill_count": skill_data["skill_count"],
        "clusters": skill_data["clusters"],
        "experience_level": skill_data["experience_level"],
        "top_categories": skill_data["top_categories"],
        "overall_compatibility": overall_ats,
        "job_results": job_results
    }


# ─── Serve React SPA ─────────────────────────────────────────────────────────

FRONTEND_BUILD = Path(__file__).parent.parent / "frontend" / "dist"
# Also check Docker path: /app/frontend/dist
if not FRONTEND_BUILD.exists():
    FRONTEND_BUILD = Path("/app/frontend/dist")

if FRONTEND_BUILD.exists():
    assets_dir = FRONTEND_BUILD / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        index_file = FRONTEND_BUILD / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        return JSONResponse({"error": "Frontend not built."}, status_code=404)
