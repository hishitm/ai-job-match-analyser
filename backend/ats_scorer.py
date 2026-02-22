"""
ATS (Applicant Tracking System) scorer.
Analyses a resume's structure, keyword presence, and formatting signals
to produce an ATS-friendliness score and actionable feedback.
"""

import re
from typing import Dict, Any, List


# Sections typically required by ATS systems
ATS_REQUIRED_SECTIONS = [
    ("contact",       ["email", "phone", "linkedin", "github", "address", "contact"]),
    ("summary",       ["summary", "objective", "about me", "profile", "overview"]),
    ("experience",    ["experience", "work experience", "employment", "internship", "career"]),
    ("education",     ["education", "academic", "degree", "university", "college", "school"]),
    ("skills",        ["skills", "technical skills", "technologies", "competencies", "expertise"]),
    ("projects",      ["projects", "personal projects", "key projects", "notable projects"]),
    ("certifications",["certification", "certificate", "credentials", "licenses", "courses"]),
    ("achievements",  ["achievement", "award", "honor", "recognition", "accomplishment"]),
]

# ATS-unfriendly formatting indicators (from text patterns)
FORMATTING_RED_FLAGS = [
    (r'\b(table|cell|row|column)\b', "Tables may confuse ATS parsers"),
    (r'[\u2022\u2023\u25E6\u2043]', None),  # Fancy bullets – OK, don't flag
    (r'[^\x00-\x7F]{5,}', "Non-ASCII characters may not parse correctly"),
]

# Action verbs that strengthen ATS relevance
ACTION_VERBS = [
    "developed", "built", "designed", "implemented", "created", "engineered",
    "improved", "optimized", "reduced", "increased", "achieved", "delivered",
    "managed", "led", "coordinated", "collaborated", "automated", "deployed",
    "integrated", "analyzed", "researched", "solved", "scaled", "launched",
    "migrated", "refactored", "tested", "mentored", "published"
]

# Measurable result indicators
METRIC_PATTERNS = [
    r'\d+\s*%',          # percentages
    r'\$\s*\d+',         # dollar amounts
    r'\d+\s*x\b',        # multiples
    r'\d+\s*(users|clients|customers|requests|queries|projects|teams)',
    r'(reduced|improved|increased|grew|scaled|saved)\b.*\d+',
]


def score_ats(resume_text: str, job_description: str = "") -> Dict[str, Any]:
    """
    Compute ATS score (0–100) and return detailed feedback.
    """
    text_lower = resume_text.lower()
    details = []
    deductions = []
    score = 0

    # ── 1. Section Coverage (30 pts) ─────────────────────────────────────────
    section_score = 0
    found_sections = []
    missing_sections = []

    for section_name, keywords in ATS_REQUIRED_SECTIONS:
        found = any(kw in text_lower for kw in keywords)
        if found:
            section_score += 1
            found_sections.append(section_name.title())
        else:
            if section_name in ("contact", "experience", "education", "skills"):
                missing_sections.append(section_name.title())

    section_pts = round((section_score / len(ATS_REQUIRED_SECTIONS)) * 30)
    score += section_pts
    details.append({
        "category": "Section Coverage",
        "score": section_pts,
        "max": 30,
        "found": found_sections,
        "missing": missing_sections,
        "note": f"{section_score}/{len(ATS_REQUIRED_SECTIONS)} standard sections detected"
    })

    # ── 2. Contact Info Completeness (10 pts) ────────────────────────────────
    contact_pts = 0
    has_email = bool(re.search(r'[\w.+-]+@[\w-]+\.\w+', resume_text))
    has_phone = bool(re.search(r'(\+?\d[\d\s\-\(\)]{7,}\d)', resume_text))
    has_linkedin = bool(re.search(r'linkedin\.com', text_lower))
    has_github = bool(re.search(r'github\.com', text_lower))

    if has_email:   contact_pts += 4
    if has_phone:   contact_pts += 3
    if has_linkedin: contact_pts += 2
    if has_github:  contact_pts += 1
    score += contact_pts

    contact_missing = []
    if not has_email:    contact_missing.append("Email address")
    if not has_phone:    contact_missing.append("Phone number")
    if not has_linkedin: contact_missing.append("LinkedIn URL")
    if not has_github:   contact_missing.append("GitHub URL")

    details.append({
        "category": "Contact Information",
        "score": contact_pts,
        "max": 10,
        "note": "Email, phone, LinkedIn, GitHub",
        "missing": contact_missing
    })

    # ── 3. Action Verbs & Impact Language (15 pts) ───────────────────────────
    found_verbs = [v for v in ACTION_VERBS if v in text_lower]
    verb_density = min(len(found_verbs) / 10, 1.0)
    verb_pts = round(verb_density * 15)
    score += verb_pts

    details.append({
        "category": "Action Verbs & Impact Language",
        "score": verb_pts,
        "max": 15,
        "note": f"{len(found_verbs)} strong action verbs found",
        "found": found_verbs[:6]
    })

    # ── 4. Measurable Results (10 pts) ───────────────────────────────────────
    metric_hits = sum(1 for p in METRIC_PATTERNS if re.search(p, text_lower))
    metric_pts = min(metric_hits * 2, 10)
    score += metric_pts

    details.append({
        "category": "Measurable Results",
        "score": metric_pts,
        "max": 10,
        "note": f"{metric_hits} quantified achievements detected (%, $, ×, user counts)"
    })

    # ── 5. Length & Word Count (10 pts) ──────────────────────────────────────
    word_count = len(resume_text.split())
    if 300 <= word_count <= 800:
        length_pts = 10
        length_note = f"{word_count} words — ideal length"
    elif 200 <= word_count < 300:
        length_pts = 7
        length_note = f"{word_count} words — slightly short, aim for 300–800"
    elif 800 < word_count <= 1200:
        length_pts = 8
        length_note = f"{word_count} words — slightly long for ATS"
    else:
        length_pts = 5
        length_note = f"{word_count} words — consider trimming to 300–800 for ATS"
    score += length_pts

    details.append({
        "category": "Resume Length",
        "score": length_pts,
        "max": 10,
        "note": length_note
    })

    # ── 6. Job Keyword Match (25 pts — only if job description provided) ─────
    keyword_pts = 0
    keyword_note = "No job description provided"
    jd_keywords: List[str] = []
    matched_jd_kw: List[str] = []

    if job_description:
        # Extract significant words from JD (nouns, compound phrases)
        jd_words = set(re.findall(r'\b[a-z][a-z]+\b', job_description.lower()))
        stopwords = {
            "and", "the", "for", "with", "that", "this", "are", "you",
            "will", "have", "our", "your", "from", "not", "but", "can",
            "all", "they", "their", "would", "should", "must", "also",
            "into", "more", "about", "what", "which", "such", "these",
            "those", "when", "then", "been", "may", "able", "per", "one"
        }
        jd_keywords = [w for w in jd_words if w not in stopwords and len(w) > 3][:40]
        matched_jd_kw = [w for w in jd_keywords if w in text_lower]
        kw_ratio = len(matched_jd_kw) / len(jd_keywords) if jd_keywords else 0
        keyword_pts = round(kw_ratio * 25)
        keyword_note = f"{len(matched_jd_kw)}/{len(jd_keywords)} JD keywords found in resume"
    score += keyword_pts

    details.append({
        "category": "Job Keyword Alignment",
        "score": keyword_pts,
        "max": 25,
        "note": keyword_note,
        "matched": matched_jd_kw[:10],
        "missing": [w for w in jd_keywords if w not in matched_jd_kw][:8]
    })

    final_score = min(score, 100)

    return {
        "ats_score": final_score,
        "grade": _grade(final_score),
        "details": details,
        "summary": _ats_summary(final_score)
    }


def _grade(score: int) -> str:
    if score >= 85: return "A"
    if score >= 70: return "B"
    if score >= 55: return "C"
    if score >= 40: return "D"
    return "F"


def _ats_summary(score: int) -> str:
    if score >= 85:
        return "Excellent ATS compatibility. Your resume is highly optimized for automated screening."
    if score >= 70:
        return "Good ATS compatibility. Minor improvements can push you into excellent range."
    if score >= 55:
        return "Moderate ATS compatibility. Several improvements are recommended."
    if score >= 40:
        return "Below average ATS compatibility. Significant formatting and keyword improvements needed."
    return "Poor ATS compatibility. Major restructuring is recommended before applying."
