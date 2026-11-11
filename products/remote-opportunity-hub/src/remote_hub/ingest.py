from __future__ import annotations

import json
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from .normalize import normalize_ashby, normalize_greenhouse, normalize_himalayas, normalize_lever

USER_AGENT = "RemoteOpportunityHub/0.1 (+https://github.com/zopair/Zubair-Engineering-Lab)"
TIMEOUT_SECONDS = 20
MAX_RESPONSE_BYTES = 8_000_000
BOARD_PATTERN = re.compile(r"^[A-Za-z0-9_.-]{1,120}$")
HIMALAYAS_REFRESH_HOURS = 24


def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _parse_time(value):
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def fetch_json(url: str):
    request = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        if response.status != 200:
            raise RuntimeError(f"Unexpected HTTP status: {response.status}")
        payload = response.read(MAX_RESPONSE_BYTES + 1)
    if len(payload) > MAX_RESPONSE_BYTES:
        raise ValueError("Source response exceeds 8 MB safety limit")
    return json.loads(payload.decode("utf-8"))


def source_url(source: dict) -> str:
    provider, board = source.get("provider"), str(source.get("board", ""))
    if not BOARD_PATTERN.fullmatch(board):
        raise ValueError("Invalid ATS board identifier")
    if provider == "greenhouse":
        return f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=true"
    if provider == "lever":
        return f"https://api.lever.co/v0/postings/{board}?mode=json"
    if provider == "ashby":
        return f"https://api.ashbyhq.com/posting-api/job-board/{board}"
    raise ValueError(f"Unsupported provider: {provider}")


def fetch_himalayas(source: dict):
    all_jobs = {}
    queries = source.get("queries") or [{"country": "EG"}, {"worldwide": "true"}]
    max_pages = max(1, min(int(source.get("max_pages", 3)), 5))
    for query in queries:
        for page in range(1, max_pages + 1):
            params = {"page": page, "sort": "recent"}
            params.update(query)
            url = "https://himalayas.app/jobs/api/search?" + urllib.parse.urlencode(params, doseq=True)
            payload = fetch_json(url)
            records = payload.get("jobs", [])
            if not records:
                break
            for raw in records:
                if not isinstance(raw, dict):
                    continue
                job = normalize_himalayas(raw, source)
                if job["title"] and job["application_url"]:
                    job["last_verified_at"] = utc_now()
                    all_jobs[job["id"]] = job
            if len(records) < 1:
                break
    return list(all_jobs.values())


def fetch_source(source: dict):
    provider = source.get("provider")
    if provider == "himalayas":
        return fetch_himalayas(source)
    payload = fetch_json(source_url(source))
    if provider == "greenhouse":
        records, normalizer = payload.get("jobs", []), normalize_greenhouse
    elif provider == "lever":
        records, normalizer = (payload if isinstance(payload, list) else payload.get("data", [])), normalize_lever
    elif provider == "ashby":
        records, normalizer = payload.get("jobs", []), normalize_ashby
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    jobs = []
    for raw in records:
        if not isinstance(raw, dict):
            continue
        job = normalizer(raw, source)
        if not job["title"] or not job["application_url"]:
            continue
        if job["remote_status"] != "remote":
            continue
        job["last_verified_at"] = utc_now()
        jobs.append(job)
    return jobs


def refresh(config_path: str, output_path: str, force: bool = False):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    output_file = Path(output_path)
    previous = json.loads(output_file.read_text(encoding="utf-8")) if output_file.exists() else {"jobs": [], "sources": []}
    old = {job["id"]: job for job in previous.get("jobs", []) if isinstance(job, dict) and job.get("id")}
    previous_sources = {item.get("source"): item for item in previous.get("sources", []) if isinstance(item, dict)}
    successful_sources, source_results, errors = {}, [], []

    for source in config.get("sources", []):
        if not source.get("enabled"):
            continue
        label = f'{source.get("provider")}:{source.get("board", "")}'
        prior = previous_sources.get(label, {})
        prior_time = _parse_time(prior.get("verified_at"))
        if source.get("provider") == "himalayas" and not force and prior.get("status") in {"ok", "cached"} and prior_time:
            age_hours = (datetime.now(timezone.utc) - prior_time).total_seconds() / 3600
            if age_hours < HIMALAYAS_REFRESH_HOURS:
                source_results.append({**prior, "status": "cached"})
                continue
        try:
            fresh = fetch_source(source)
            ids = set()
            for job in fresh:
                old[job["id"]] = job
                ids.add(job["id"])
            successful_sources[label] = ids
            source_results.append({"source": label, "status": "ok", "jobs": len(fresh), "verified_at": utc_now()})
        except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
            errors.append({"source": label, "error": str(exc)[:300]})
            source_results.append({"source": label, "status": "error", "jobs": None, "verified_at": None})

    # Only a successful complete response can deactivate records missing from that board.
    for label, current_ids in successful_sources.items():
        for job in old.values():
            job_label = f'{job.get("platform", "").lower()}:{job.get("board", "")}'
            if job_label == label:
                job["status"] = "active" if job["id"] in current_ids else "inactive"

    now = datetime.now(timezone.utc)
    for job in old.values():
        expiry = _parse_time(job.get("expiry_date"))
        if expiry and expiry < now:
            job["status"] = "inactive"

    jobs = sorted(old.values(), key=lambda item: (item.get("published_at") or "", item.get("last_verified_at") or ""), reverse=True)
    payload = {
        "generated_at": utc_now(),
        "jobs": jobs,
        "sources": source_results,
        "errors": errors,
        "notice": "Himalayas data is credited and linked to its original listing. All other jobs link to the employer's original application page. Confirm eligibility before applying.",
    }
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload
