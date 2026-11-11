from __future__ import annotations

import hashlib
import html
import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urlparse


class _TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def plain_text(value: object) -> str:
    if not value:
        return ""
    parser = _TextExtractor()
    try:
        parser.feed(str(value))
        return re.sub(r"\s+", " ", html.unescape(" ".join(parser.parts))).strip()
    except Exception:
        return re.sub(r"\s+", " ", html.unescape(str(value))).strip()


def _safe_url(value: object) -> str:
    candidate = str(value or "").strip()
    parsed = urlparse(candidate)
    return candidate if parsed.scheme == "https" and parsed.netloc else ""


def _date_value(value: object):
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value / 1000, tz=timezone.utc).isoformat()
    return str(value)


def is_explicitly_remote(location: str, title: str = "", description: str = "") -> bool:
    text = " ".join((location or "", title or "", description or "")).lower()
    if re.search(r"\b(hybrid|on[- ]?site|office[- ]based)\b", text):
        return False
    return bool(re.search(
        r"\b(remote|work from home|work-from-home|distributed|anywhere|worldwide|fully remote|100% remote)\b",
        text,
    ))


def _base(raw: dict, source: dict, platform: str, external_id: object,
          title: object, location: object, description: object, url: object,
          published: object = None, remote_hint: object = None) -> dict:
    location_text = plain_text(location)
    description_text = plain_text(description)
    workplace = str(remote_hint or "").strip().lower()
    if workplace == "hybrid":
        remote_status = "hybrid"
    elif workplace in {"remote", "fully remote"}:
        remote_status = "remote"
    elif workplace in {"onsite", "on-site", "office"}:
        remote_status = "onsite"
    else:
        remote_status = "remote" if is_explicitly_remote(location_text, str(title or ""), description_text) else "unknown"
    stable = f"{platform.lower()}:{source.get('board','')}:{external_id or url or title}"
    job_id = hashlib.sha256(stable.encode("utf-8")).hexdigest()[:20]
    return {
        "id": job_id,
        "external_id": str(external_id or ""),
        "company": str(source.get("company") or "Unknown company").strip(),
        "title": plain_text(title),
        "platform": platform,
        "board": str(source.get("board") or ""),
        "careers_url": _safe_url(source.get("careers_url")),
        "location": location_text,
        "remote_status": remote_status,
        "description": description_text[:12000],
        "application_url": _safe_url(url),
        "published_at": _date_value(published),
        "last_verified_at": None,
        "status": "active",
    }


def normalize_greenhouse(raw: dict, source: dict) -> dict:
    return _base(raw, source, "Greenhouse", raw.get("id"), raw.get("title"),
                 (raw.get("location") or {}).get("name", ""),
                 raw.get("content", ""), raw.get("absolute_url"),
                 raw.get("first_published") or raw.get("updated_at"))


def normalize_lever(raw: dict, source: dict) -> dict:
    categories = raw.get("categories") or {}
    return _base(raw, source, "Lever", raw.get("id"), raw.get("text"),
                 categories.get("location", ""), raw.get("descriptionPlain") or raw.get("description"),
                 raw.get("hostedUrl") or raw.get("applyUrl"),
                 raw.get("createdAt") or raw.get("updatedAt"))


def normalize_ashby(raw: dict, source: dict) -> dict:
    return _base(raw, source, "Ashby", raw.get("id") or raw.get("jobUrl"), raw.get("title"),
                 raw.get("location"), raw.get("descriptionPlain") or raw.get("descriptionHtml"),
                 raw.get("applyUrl") or raw.get("jobUrl"), raw.get("publishedAt"),
                 raw.get("workplaceType"))


def normalize_himalayas(raw: dict, source: dict) -> dict:
    restrictions = raw.get("locationRestrictions") or []
    if restrictions:
        location = ", ".join(
            str(item.get("name") or item.get("alpha2") or "").strip()
            for item in restrictions if isinstance(item, dict)
        )
    else:
        location = "Worldwide"
    job = _base(raw, source, "Himalayas", raw.get("guid"), raw.get("title"),
                location, raw.get("description") or raw.get("excerpt"),
                raw.get("applicationLink"), raw.get("pubDate"), "remote")
    job.update({
        "source_credit": "Himalayas",
        "source_credit_url": job["application_url"],
        "expiry_date": _date_value(raw.get("expiryDate")),
        "employment_type": raw.get("employmentType"),
        "seniority": raw.get("seniority") or [],
        "categories": raw.get("categories") or [],
        "location_restrictions": [item.get("name") or item.get("alpha2") for item in restrictions if isinstance(item, dict)],
        "timezone_restrictions": raw.get("timezoneRestrictions") or [],
        "salary_min": raw.get("minSalary"),
        "salary_max": raw.get("maxSalary"),
        "salary_period": raw.get("salaryPeriod"),
        "salary_currency": raw.get("currency"),
    })
    return job
