"""
Job matcher: matches resume skills against job role templates
and computes similarity scores.
"""

from typing import List, Dict, Any

# Job role templates with required + bonus skills
JOB_ROLES = [
    {
        "id": "fullstack_dev",
        "title": "Full Stack Developer",
        "icon": "🌐",
        "description": "Build and maintain both frontend and backend of web applications.",
        "required_skills": ["html", "css", "javascript", "react", "node.js", "sql", "git"],
        "bonus_skills": ["typescript", "docker", "aws", "postgresql", "redis", "graphql", "next.js"],
        "min_skills": 4
    },
    {
        "id": "frontend_dev",
        "title": "Frontend Developer",
        "icon": "🎨",
        "description": "Create stunning user interfaces and experiences for web apps.",
        "required_skills": ["html", "css", "javascript", "react", "git"],
        "bonus_skills": ["typescript", "vue", "next.js", "tailwindcss", "figma", "testing library", "webpack", "storybook"],
        "min_skills": 3
    },
    {
        "id": "backend_dev",
        "title": "Backend Developer",
        "icon": "⚙️",
        "description": "Design and develop robust server-side logic and APIs.",
        "required_skills": ["python", "sql", "rest", "git", "linux"],
        "bonus_skills": ["fastapi", "django", "docker", "redis", "postgresql", "mongodb", "aws", "microservices", "celery"],
        "min_skills": 3
    },
    {
        "id": "data_scientist",
        "title": "Data Scientist",
        "icon": "📊",
        "description": "Analyse data, build predictive models, and extract business insights.",
        "required_skills": ["python", "machine learning", "pandas", "numpy", "sql", "statistics"],
        "bonus_skills": ["tensorflow", "pytorch", "scikit-learn", "matplotlib", "deep learning", "r", "spark", "nlp", "tableau"],
        "min_skills": 3
    },
    {
        "id": "ml_engineer",
        "title": "ML Engineer",
        "icon": "🤖",
        "description": "Build, train, and deploy ML  models at scale in production systems.",
        "required_skills": ["python", "machine learning", "deep learning", "tensorflow", "docker", "git"],
        "bonus_skills": ["pytorch", "kubernetes", "mlops", "mlflow", "aws", "fastapi", "spark", "feature engineering", "model deployment"],
        "min_skills": 3
    },
    {
        "id": "devops_engineer",
        "title": "DevOps / Cloud Engineer",
        "icon": "☁️",
        "description": "Automate infrastructure, deployments, and maintain cloud systems.",
        "required_skills": ["docker", "kubernetes", "aws", "ci/cd", "linux", "bash"],
        "bonus_skills": ["terraform", "ansible", "jenkins", "github actions", "prometheus", "grafana", "gcp", "azure", "helm"],
        "min_skills": 3
    },
    {
        "id": "mobile_dev",
        "title": "Mobile Developer",
        "icon": "📱",
        "description": "Build native or cross-platform mobile applications.",
        "required_skills": ["react native", "javascript", "git"],
        "bonus_skills": ["flutter", "dart", "swift", "kotlin", "android", "ios", "firebase", "expo", "typescript"],
        "min_skills": 2
    },
    {
        "id": "data_engineer",
        "title": "Data Engineer",
        "icon": "🔧",
        "description": "Design and build data pipelines, warehouses, and ETL processes.",
        "required_skills": ["sql", "python", "etl", "spark", "git"],
        "bonus_skills": ["kafka", "airflow", "dbt", "snowflake", "bigquery", "redshift", "hadoop", "databricks", "data pipeline"],
        "min_skills": 3
    },
    {
        "id": "security_engineer",
        "title": "Security Engineer",
        "icon": "🔒",
        "description": "Identify, mitigate, and protect systems from cybersecurity threats.",
        "required_skills": ["cybersecurity", "linux", "networking", "encryption"],
        "bonus_skills": ["penetration testing", "owasp", "siem", "ethical hacking", "python", "compliance", "vulnerability assessment", "burp suite"],
        "min_skills": 2
    },
    {
        "id": "ai_engineer",
        "title": "AI / GenAI Engineer",
        "icon": "✨",
        "description": "Build AI-powered applications with LLMs, RAG, and generative AI.",
        "required_skills": ["python", "llm", "openai api", "langchain"],
        "bonus_skills": ["hugging face", "rag", "vector database", "fastapi", "docker", "pytorch", "transformers", "nlp", "generative ai"],
        "min_skills": 2
    },
    {
        "id": "android_dev",
        "title": "Android Developer",
        "icon": "🤖",
        "description": "Build native Android applications using Kotlin or Java.",
        "required_skills": ["android", "kotlin", "git"],
        "bonus_skills": ["java", "jetpack compose", "firebase", "mvvm", "room", "retrofit", "coroutines"],
        "min_skills": 2
    },
    {
        "id": "product_manager",
        "title": "Product Manager",
        "icon": "📋",
        "description": "Define product vision, strategy, and work with cross-functional teams.",
        "required_skills": ["agile", "scrum", "jira", "communication", "stakeholder management"],
        "bonus_skills": ["sql", "tableau", "figma", "project management", "a/b testing", "leadership", "presentation"],
        "min_skills": 2
    }
]


def match_jobs(found_skills: List[str], experience_level: str) -> List[Dict[str, Any]]:
    """
    Score resume skills against all job templates.
    Returns sorted list of matches with score, matched skills, and missing skills.
    """
    found_set = set(s.lower() for s in found_skills)
    results = []

    for job in JOB_ROLES:
        required = [s.lower() for s in job["required_skills"]]
        bonus = [s.lower() for s in job["bonus_skills"]]
        all_role_skills = required + bonus

        matched_required = [s for s in required if s in found_set]
        matched_bonus = [s for s in bonus if s in found_set]
        matched_all = matched_required + matched_bonus

        missing_required = [s for s in required if s not in found_set]

        if not all_role_skills:
            continue

        # Score: required skills weighted 2x, bonus 1x
        score_num = len(matched_required) * 2 + len(matched_bonus)
        score_den = len(required) * 2 + len(bonus)
        raw_score = (score_num / score_den) * 100 if score_den > 0 else 0

        # Boost for experience level match
        if experience_level == "Senior":
            raw_score = min(100, raw_score * 1.05)
        elif experience_level == "Junior / Entry-Level" and raw_score > 0:
            raw_score = raw_score * 0.95

        score = round(raw_score, 1)

        results.append({
            "id": job["id"],
            "title": job["title"],
            "icon": job["icon"],
            "description": job["description"],
            "score": score,
            "matched_skills": matched_all,
            "missing_skills": missing_required[:5],  # Top 5 missing required skills
            "skill_coverage": f"{len(matched_all)}/{len(all_role_skills)}",
            "fit_level": _fit_label(score)
        })

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:8]  # Return top 8 matches


def _fit_label(score: float) -> str:
    if score >= 80:
        return "Excellent Fit"
    elif score >= 60:
        return "Good Fit"
    elif score >= 40:
        return "Moderate Fit"
    elif score >= 20:
        return "Partial Fit"
    else:
        return "Low Fit"
