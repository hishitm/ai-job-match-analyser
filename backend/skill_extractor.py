"""
Skill extractor: scans resume text, matches against taxonomy,
clusters skills by category, and estimates experience level.
"""

import re
from collections import defaultdict
from typing import Dict, List, Any

try:
    from skills_taxonomy import SKILLS_TAXONOMY, SKILL_TO_CATEGORY, ALL_SKILLS
except ImportError:
    from backend.skills_taxonomy import SKILLS_TAXONOMY, SKILL_TO_CATEGORY, ALL_SKILLS


def normalize(text: str) -> str:
    return text.lower().strip()


def extract_skills_from_text(text: str) -> Dict[str, Any]:
    """
    Scan resume text and extract all matching skills.
    Uses multi-word phrase matching + single-word matching.
    Returns categorized skills, clusters, and experience level.
    """
    text_lower = text.lower()
    # Remove noise
    text_lower = re.sub(r'[^a-z0-9\s\.\+\#\/\-]', ' ', text_lower)
    
    found_skills = {}  # skill -> category

    # --- Phase 1: Multi-word phrase matching (longest match first) ---
    multi_word_skills = [(s, c) for s, c in SKILL_TO_CATEGORY.items() if ' ' in s]
    multi_word_skills.sort(key=lambda x: -len(x[0]))
    
    for skill, category in multi_word_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found_skills[skill] = category

    # --- Phase 2: Single-word matching with word boundaries ---
    single_word_skills = [(s, c) for s, c in SKILL_TO_CATEGORY.items() if ' ' not in s]
    for skill, category in single_word_skills:
        # Skip if already covered by a longer phrase variant
        if any(skill in fs for fs in found_skills.keys() if fs != skill):
            continue
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills[skill] = category

    # --- Organize by category ---
    categorized = defaultdict(list)
    for skill, category in found_skills.items():
        categorized[category].append(skill)

    # Build category summary with metadata
    clusters = []
    total_skills = len(found_skills)
    
    for cat_key, skills in categorized.items():
        cat_meta = SKILLS_TAXONOMY.get(cat_key, {})
        clusters.append({
            "category": cat_key,
            "label": cat_meta.get("label", cat_key.replace("_", " ").title()),
            "color": cat_meta.get("color", "#888888"),
            "skills": sorted(list(set(skills))),
            "count": len(set(skills))
        })

    # Sort clusters by skill count (descending)
    clusters.sort(key=lambda x: x["count"], reverse=True)

    # --- Experience level estimation ---
    experience_level = _estimate_experience_level(text, total_skills)

    # --- Top categories ---
    top_categories = [c["label"] for c in clusters[:3]]

    # --- All skills flat list for matching ---
    all_found = list(found_skills.keys())

    return {
        "skills": all_found,
        "skill_count": total_skills,
        "clusters": clusters,
        "experience_level": experience_level,
        "top_categories": top_categories
    }


def _estimate_experience_level(text: str, skill_count: int) -> str:
    """Estimate experience level from resume text signals."""
    text_lower = text.lower()

    # Check for seniority keywords
    senior_keywords = ["senior", "lead", "principal", "staff", "architect",
                       "vp ", "director", "head of", "manager", "8 years",
                       "9 years", "10 years", "10+ years", "12 years", "15 years"]
    mid_keywords = ["mid-level", "3 years", "4 years", "5 years", "6 years",
                    "7 years", "intermediate"]
    junior_keywords = ["junior", "intern", "fresher", "graduate", "entry-level",
                       "entry level", "1 year", "2 years", "recent graduate",
                       "new grad", "bootcamp"]

    score_senior = sum(1 for k in senior_keywords if k in text_lower)
    score_mid = sum(1 for k in mid_keywords if k in text_lower)
    score_junior = sum(1 for k in junior_keywords if k in text_lower)

    # Also use skill count as signal
    if skill_count >= 25:
        score_senior += 2
    elif skill_count >= 15:
        score_mid += 2
    elif skill_count >= 6:
        score_junior += 1

    if score_senior > score_mid and score_senior > score_junior:
        return "Senior"
    elif score_mid >= score_junior:
        return "Mid-Level"
    else:
        return "Junior / Entry-Level"
