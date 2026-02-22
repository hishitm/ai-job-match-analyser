"""
Match scorer: computes how well a resume matches a specific job posting,
generates insights, and produces improvement suggestions.
"""

import re
from typing import Dict, Any, List

try:
    from skill_extractor import extract_skills_from_text
    from skills_taxonomy import SKILLS_TAXONOMY, SKILL_TO_CATEGORY
except ImportError:
    from backend.skill_extractor import extract_skills_from_text
    from backend.skills_taxonomy import SKILLS_TAXONOMY, SKILL_TO_CATEGORY


def score_match(resume_skills: List[str], job_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compare resume skills against a job description to compute:
    - Match score (0–100)
    - Matched skills
    - Missing skills
    - Insights & improvement recommendations
    - Probability of getting the role
    """
    # Extract skills from the full job description text
    jd_full_text = (
        job_data.get("full", "") + " " +
        job_data.get("requirements", "") + " " +
        job_data.get("skills", "") + " " +
        job_data.get("responsibilities", "")
    )

    job_skill_data = extract_skills_from_text(jd_full_text)
    jd_skills = set(s.lower() for s in job_skill_data["skills"])
    resume_skills_set = set(s.lower() for s in resume_skills)

    matched_skills = sorted(list(jd_skills & resume_skills_set))
    missing_skills = sorted(list(jd_skills - resume_skills_set))

    # ── Score Calculation ────────────────────────────────────────────────────
    if not jd_skills:
        # Fallback: keyword overlap on raw text
        match_score = _keyword_fallback_score(resume_skills, jd_full_text)
        matched_skills = []
        missing_skills = []
    else:
        raw = (len(matched_skills) / len(jd_skills)) * 100
        match_score = round(min(raw, 100), 1)

    # ── Fit Label & Probability ──────────────────────────────────────────────
    fit_label, probability = _get_fit_and_probability(match_score)

    # ── Categorise matched/missing by domain ────────────────────────────────
    matched_by_cat = _group_by_category(matched_skills)
    missing_by_cat = _group_by_category(missing_skills[:15])  # top 15 missing

    # ── Insights ─────────────────────────────────────────────────────────────
    insights = _generate_insights(
        match_score, matched_skills, missing_skills,
        job_data, resume_skills_set, jd_skills
    )

    # ── Improvements ─────────────────────────────────────────────────────────
    improvements = _generate_improvements(
        match_score, missing_skills, job_data, resume_skills_set
    )

    return {
        "match_score": match_score,
        "fit_label": fit_label,
        "match_readiness": probability,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills[:12],
        "matched_by_category": matched_by_cat,
        "missing_by_category": missing_by_cat,
        "jd_skill_count": len(jd_skills),
        "insights": insights,
        "recommendations": improvements
    }


def _keyword_fallback_score(resume_skills: List[str], jd_text: str) -> float:
    """Simple keyword match when NLP skill extraction yields nothing."""
    jd_lower = jd_text.lower()
    hits = sum(1 for s in resume_skills if len(s) > 2 and s.lower() in jd_lower)
    return round(min((hits / max(len(resume_skills), 1)) * 120, 100), 1)


def _get_fit_and_probability(score: float):
    if score >= 85:
        return "Exceptional Match", {"label": "Highly Qualified", "range": "85–100%", "color": "#10b981"}
    if score >= 70:
        return "Strong Match",    {"label": "Qualified",      "range": "70–85%", "color": "#3b82f6"}
    if score >= 55:
        return "Good Match",      {"label": "Candidate",      "range": "55–70%", "color": "#f59e0b"}
    if score >= 40:
        return "Partial Match",   {"label": "Potential",      "range": "40–55%", "color": "#f97316"}
    if score >= 20:
        return "Low Alignment",   {"label": "Emerging",       "range": "20–40%", "color": "#ef4444"}
    return "Weak Alignment",      {"label": "Underqualified", "range": "<20%",   "color": "#991b1b"}


def _group_by_category(skills: List[str]) -> List[Dict]:
    cat_map: Dict[str, List[str]] = {}
    for skill in skills:
        cat = SKILL_TO_CATEGORY.get(skill.lower(), "other")
        cat_map.setdefault(cat, []).append(skill)

    result = []
    for cat_key, skills_list in cat_map.items():
        meta = SKILLS_TAXONOMY.get(cat_key, {})
        result.append({
            "category": cat_key,
            "label": meta.get("label", cat_key.replace("_", " ").title()),
            "color": meta.get("color", "#888888"),
            "skills": skills_list
        })
    return sorted(result, key=lambda x: len(x["skills"]), reverse=True)


def _generate_insights(
    score: float,
    matched: List[str],
    missing: List[str],
    job_data: Dict,
    resume_set: set,
    jd_set: set
) -> List[Dict]:
    insights = []

    # Overall score insight
    if score >= 70:
        insights.append({
            "type": "success",
            "icon": "✅",
            "title": "Strong Skill Alignment",
            "message": f"You match {score}% of the job's technical requirements. You're a competitive candidate."
        })
    elif score >= 40:
        insights.append({
            "type": "warning",
            "icon": "⚠️",
            "title": "Partial Skill Match",
            "message": f"You have {score}% of required skills. Bridging a few gaps could make you a strong applicant."
        })
    else:
        insights.append({
            "type": "danger",
            "icon": "❌",
            "title": "Significant Skill Gap",
            "message": f"Only {score}% skill match. Consider upskilling in the missing areas before applying."
        })

    # Skill match count
    if matched:
        insights.append({
            "type": "info",
            "icon": "🎯",
            "title": "Skills You Already Have",
            "message": f"{len(matched)} skills match the job requirements: {', '.join(matched[:5])}{'…' if len(matched) > 5 else ''}."
        })

    # Missing high-value skills
    if missing:
        top_missing = missing[:4]
        insights.append({
            "type": "warning",
            "icon": "📌",
            "title": "Key Missing Skills",
            "message": f"Top skills to acquire: {', '.join(top_missing)}. Adding these could significantly improve your match."
        })

    # Gender/uniqueness of skills
    unique_to_resume = resume_set - jd_set
    if len(unique_to_resume) > 5:
        insights.append({
            "type": "info",
            "icon": "💡",
            "title": "Extra Skills on Your Resume",
            "message": f"You have {len(unique_to_resume)} skills not mentioned in this JD — they could make you stand out if highlighted correctly."
        })

    return insights


def _generate_improvements(
    score: float,
    missing: List[str],
    job_data: Dict,
    resume_set: set
) -> List[Dict]:
    improvements = []

    # Tailor resume to JD
    improvements.append({
        "priority": "high",
        "icon": "✍️",
        "title": "Tailor Your Resume to This Job",
        "detail": "Mirror exact keywords and phrases from the job description in your resume. ATS systems do exact-match filtering."
    })

    # Add missing skills
    if missing[:3]:
        improvements.append({
            "priority": "high",
            "icon": "📚",
            "title": f"Learn: {', '.join(missing[:3])}",
            "detail": f"These are required by this role. Completing a short course or project demonstrating these skills can close the gap quickly."
        })

    # Quantify achievements
    improvements.append({
        "priority": "medium",
        "icon": "📊",
        "title": "Add Quantified Achievements",
        "detail": "Replace vague bullets like 'worked on X' with 'Improved X by 30%, reducing load time by 2s'. Numbers make your resume stand out."
    })

    # LinkedIn + GitHub
    if "linkedin" not in " ".join(resume_set) and "github" not in " ".join(resume_set):
        improvements.append({
            "priority": "medium",
            "icon": "🔗",
            "title": "Include LinkedIn & GitHub URLs",
            "detail": "Many recruiters and ATS systems extract profile links. An active GitHub with relevant projects dramatically increases credibility."
        })

    # Cover letter
    improvements.append({
        "priority": "low",
        "icon": "📝",
        "title": "Write a Targeted Cover Letter",
        "detail": f"Reference the company ({job_data.get('company', 'this company')}) and the specific role ({job_data.get('title', 'this position')}). Personalised letters get 3× more callbacks."
    })

    if score < 50:
        improvements.append({
            "priority": "medium",
            "icon": "🏗️",
            "title": "Build a Relevant Portfolio Project",
            "detail": "If you lack direct experience, a project demonstrating the missing skills (deployed and publicly viewable) can substitute for formal experience."
        })

    return improvements
