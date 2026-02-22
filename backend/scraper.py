"""
Job URL scraper: fetches job postings from Internshala, LinkedIn, Naukri,
Indeed, Glassdoor and extracts structured job requirements.
"""

import re
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List
from urllib.parse import urlparse


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def detect_platform(url: str) -> str:
    domain = urlparse(url).netloc.lower()
    if "internshala" in domain:
        return "internshala"
    if "linkedin" in domain:
        return "linkedin"
    if "naukri" in domain:
        return "naukri"
    if "indeed" in domain:
        return "indeed"
    if "glassdoor" in domain:
        return "glassdoor"
    if "foundit" in domain or "monster" in domain:
        return "foundit"
    if "shine" in domain:
        return "shine"
    if "wellfound" in domain or "angel" in domain:
        return "wellfound"
    return "generic"


def fetch_html(url: str, timeout: int = 12) -> str:
    resp = requests.get(url, headers=HEADERS, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def _clean(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


# ──────────────────────────────────────────────────────────────────────────────
# Platform-specific scrapers
# ──────────────────────────────────────────────────────────────────────────────

def scrape_internshala(soup: BeautifulSoup, url: str) -> Dict[str, Any]:
    title = ""
    company = ""
    location = ""
    description_parts = []

    # Title
    h1 = soup.find("h1", class_=re.compile(r"profile|heading|job_title|title", re.I))
    if not h1:
        h1 = soup.find("h1")
    if h1:
        title = _clean(h1.get_text())

    # Company
    for sel in ["a.link_display_like_text", ".company_name", ".company-name", "h2"]:
        el = soup.select_one(sel)
        if el:
            company = _clean(el.get_text())
            break

    # Location
    for sel in [".location_link", ".job-location", ".location"]:
        el = soup.select_one(sel)
        if el:
            location = _clean(el.get_text())
            break

    # Description / Requirements
    for sel in [
        "#about_internship", "#about_job", ".internship_other_details_container",
        ".job_other_details", ".section-jobs", ".job-description",
        "#job-description", ".about-company", "[id*='detail']"
    ]:
        for el in soup.select(sel):
            txt = _clean(el.get_text())
            if len(txt) > 60:
                description_parts.append(txt)

    description = " ".join(description_parts) if description_parts else _fallback_description(soup)
    return {
        "title": title or "Job on Internshala",
        "company": company,
        "location": location,
        "description": description,
        "platform": "internshala",
        "url": url
    }


def scrape_linkedin(soup: BeautifulSoup, url: str) -> Dict[str, Any]:
    title = ""
    company = ""
    location = ""
    description = ""

    el = soup.find("h1", class_=re.compile(r"top-card|job-title", re.I))
    if el:
        title = _clean(el.get_text())

    for sel in [".topcard__org-name-link", ".top-card-layout__second-subline", "a.ember-view"]:
        el = soup.select_one(sel)
        if el:
            company = _clean(el.get_text())
            break

    el = soup.find("span", class_=re.compile(r"location", re.I))
    if el:
        location = _clean(el.get_text())

    el = soup.find("div", class_=re.compile(r"description|show-more-less-html", re.I))
    if el:
        description = _clean(el.get_text())
    else:
        description = _fallback_description(soup)

    return {
        "title": title or "Job on LinkedIn",
        "company": company,
        "location": location,
        "description": description,
        "platform": "linkedin",
        "url": url
    }


def scrape_naukri(soup: BeautifulSoup, url: str) -> Dict[str, Any]:
    title = ""
    company = ""
    location = ""
    description = ""

    el = soup.find("h1", class_=re.compile(r"jd-header|title|heading", re.I))
    if not el:
        el = soup.find("h1")
    if el:
        title = _clean(el.get_text())

    for sel in [".jd-header-comp-name", ".comp-name", ".company-name"]:
        el = soup.select_one(sel)
        if el:
            company = _clean(el.get_text())
            break

    for sel in [".loc", ".location", ".jd-header-location"]:
        el = soup.select_one(sel)
        if el:
            location = _clean(el.get_text())
            break

    for sel in [".job-desc", ".jd-desc", "#job-desc", ".dang-inner-html"]:
        el = soup.select_one(sel)
        if el:
            description = _clean(el.get_text())
            break
    if not description:
        description = _fallback_description(soup)

    return {
        "title": title or "Job on Naukri",
        "company": company,
        "location": location,
        "description": description,
        "platform": "naukri",
        "url": url
    }


def scrape_generic(soup: BeautifulSoup, url: str) -> Dict[str, Any]:
    """Generic scraper fallback for unknown platforms."""
    title = ""
    description = ""

    h1 = soup.find("h1")
    if h1:
        title = _clean(h1.get_text())

    description = _fallback_description(soup)

    return {
        "title": title or "Job Posting",
        "company": "",
        "location": "",
        "description": description,
        "platform": "generic",
        "url": url
    }


def _fallback_description(soup: BeautifulSoup) -> str:
    """Try common description selectors then fall back to main body text."""
    for sel in [
        "article", "main", ".job-description", "#job-description",
        ".description", ".content", ".jd", "[class*='desc']",
        "[class*='detail']", "[id*='desc']", "[id*='detail']"
    ]:
        els = soup.select(sel)
        for el in els:
            txt = _clean(el.get_text())
            if len(txt) > 150:
                return txt[:5000]

    # Last resort: all paragraph / list text
    parts = []
    for tag in soup.find_all(["p", "li", "span"]):
        t = _clean(tag.get_text())
        if 20 < len(t) < 500:
            parts.append(t)
    return " ".join(parts[:80])


# ──────────────────────────────────────────────────────────────────────────────
# Extract structured requirements from raw description text
# ──────────────────────────────────────────────────────────────────────────────

def extract_requirements_text(description: str) -> Dict[str, str]:
    """
    Extract focused parts of the description:
    - requirements block
    - responsibilities block
    - skills/qualifications block
    """
    text_lower = description.lower()
    result = {"full": description}

    section_patterns = {
        "requirements": [
            r"(requirement[s]?[:\-\s].{50,2000}?)(?=responsibilit|qualif|about|benefit|what we|note:|apply|$)",
            r"(must have[:\-\s].{50,1500}?)(?=responsibilit|qualif|about|benefit|$)",
            r"(qualifications?[:\-\s].{50,2000}?)(?=responsibilit|benefit|about|apply|$)",
        ],
        "skills": [
            r"(skill[s]? required[:\-\s].{20,1500}?)(?=responsibilit|benefit|about|apply|we offer|$)",
            r"(technical skill[s]?[:\-\s].{20,1200}?)(?=soft skill|responsibilit|benefit|note:|$)",
        ],
        "responsibilities": [
            r"(responsibilit(?:y|ies)[:\-\s].{50,2000}?)(?=requirement|qualif|skill|benefit|about|apply|$)",
            r"(what you.?ll do[:\-\s].{50,1500}?)(?=requirement|qualif|skill|benefit|about|$)",
        ],
    }

    for section, patterns in section_patterns.items():
        for pat in patterns:
            m = re.search(pat, description, re.IGNORECASE | re.DOTALL)
            if m:
                result[section] = _clean(m.group(1))[:2000]
                break

    return result


# ──────────────────────────────────────────────────────────────────────────────
# Main public function
# ──────────────────────────────────────────────────────────────────────────────

def scrape_job(url: str) -> Dict[str, Any]:
    """
    Fetch a job posting URL and return structured job data.
    Returns:
        {
            title, company, location, platform, url,
            description, requirements, skills, responsibilities
        }
    """
    try:
        html = fetch_html(url)
    except requests.exceptions.Timeout:
        raise ValueError(f"Request timed out fetching: {url}")
    except requests.exceptions.HTTPError as e:
        raise ValueError(f"HTTP {e.response.status_code} error for: {url}")
    except Exception as e:
        raise ValueError(f"Could not fetch job URL: {str(e)}")

    soup = BeautifulSoup(html, "html.parser")

    # Remove script/style noise
    for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        tag.decompose()

    platform = detect_platform(url)

    scrapers = {
        "internshala": scrape_internshala,
        "linkedin":    scrape_linkedin,
        "naukri":      scrape_naukri,
    }
    scraper = scrapers.get(platform, scrape_generic)
    job_data = scraper(soup, url)

    # Make sure we have meaningful description
    if not job_data["description"] or len(job_data["description"]) < 80:
        job_data["description"] = _fallback_description(soup)

    # Extract structured requirement blocks
    req_blocks = extract_requirements_text(job_data["description"])
    job_data.update(req_blocks)

    return job_data
