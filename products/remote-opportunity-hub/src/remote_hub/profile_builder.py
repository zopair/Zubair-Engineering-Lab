from __future__ import annotations

import re


def _clean(value):
    if value is None:
        return ""
    return re.sub(r"\\s+", " ", str(value)).strip()


def _items(value):
    if not isinstance(value, list):
        return []
    seen, result = set(), []
    for item in value:
        text = _clean(item)
        key = text.casefold()
        if text and key not in seen:
            seen.add(key)
            result.append(text)
    return result


def build_profile(answers: dict) -> dict:
    """Create truthful profile copy using only optional, user-supplied facts."""
    answers = answers if isinstance(answers, dict) else {}
    role = _clean(answers.get("target_role"))
    skills = _items(answers.get("skills"))
    languages = _items(answers.get("languages"))
    projects = answers.get("projects") if isinstance(answers.get("projects"), list) else []
    projects = [p for p in projects if isinstance(p, dict) and _clean(p.get("name"))]
    education = _clean(answers.get("education"))
    experience = _clean(answers.get("experience_summary"))
    years = answers.get("experience_years")

    headline_parts = [role] if role else []
    headline_parts.extend(skills[:3])
    headline = " | ".join(headline_parts)

    sentences = []
    if role:
        sentences.append(f"I am building my professional profile for {role} opportunities.")
    if experience:
        sentences.append(experience.rstrip(".") + ".")
    if projects:
        names = ", ".join(_clean(p.get("name")) for p in projects[:3])
        sentences.append(f"Selected projects include {names}.")
    if education:
        sentences.append(f"Education: {education}.")
    if years is not None and str(years).strip() and str(years).strip().isdigit():
        sentences.append(f"Experience: {int(years)} years.")
    if languages:
        sentences.append("Languages: " + ", ".join(languages) + ".")
    if not sentences:
        about = "Add your real role, skills, projects, education, or experience to generate an accurate profile. No qualifications have been assumed."
    else:
        about = " ".join(sentences) + " Please verify every detail before publishing."

    return {
        "headline": headline,
        "about": about,
        "skills": skills,
        "project_descriptions": [
            {"title": _clean(p.get("name")), "description": _clean(p.get("description"))}
            for p in projects
        ],
        "platform_variants": {
            "upwork": {"title": headline, "overview": about},
            "linkedin": {"headline": headline, "about": about},
            "fiverr": {"tagline": headline, "description": about},
        },
        "disclaimer": "Generated only from answers supplied by the user. Review accuracy and platform-specific character limits before use.",
    }
