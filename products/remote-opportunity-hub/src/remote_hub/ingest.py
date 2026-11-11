from __future__ import annotations

import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from .normalize import normalize_ashby, normalize_greenhouse, normalize_lever

USER_AGENT = "RemoteOpportunityHub/0.1 (+https://github.com/zopair/Zubair-Engineering-Lab)"
TIMEOUT_SECONDS = 20
MAX_RESPONSE_BYTES = 8_000_000


def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


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
    provider, board = source.get("provider"), source.get("board", "")
    if provider == "greenhouse":
        return f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=true"
    if provider == "lever":
        return f"https://api.lever.co/v0/postings/{board}?mode=json"
    if provider == "ashby":
        return f"https://api.ashbyhq.com/posting-api/job-board/{board}"
    raise ValueError(f"Unsupported provider: {provider}")


def fetch_source(source: dict):
    payload = fetch_json(source_url(source))
    provider = source["provider"]
    if provider == "greenhouse":
        records = payload.get("jobs", [])
        normalizer = normalize_greenhouse
    elif provider == "lever":
        records = payload if isinstance(payload, list) else payload.get("data", [])
        normalizer = normalize_lever
    else:
        records = payload.get("jobs", [])
        normalizer = normalize_ashby

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


def refresh(config_path: str, output_path: str):
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    output_file = Path(output_path)
    previous = json.loads(output_file.read_text(encoding="utf-8")) if output_file.exists() else {"jobs": []}
    old = {job["id"]: job for job in previous.get("jobs", []) if isinstance(job, dict) and job.get("id")}
    active_ids_by_source, source_results, errors = {}, [], []

    for source in config.get("sources", []):
        if not source.get("enabled"):
            continue
        label = f'{source.get("provider")}:{source.get("board")}'
        try:
            fresh = fetch_source(source)
            source_ids = set()
            for job in fresh:
                old[job["id"]] = job
                source_ids.add(job["id"])
            active_ids_by_source[label] = source_ids
            source_results.append({"source": label, "status": "ok", "jobs": len(fresh), "verified_at": utc_now()})
        except (OSError, ValueError, RuntimeError, urllib.error.URLError, json.JSONDecodeError) as exc:
            errors.append({"source": label, "error": str(exc)[:300]})
            source_results.append({"source": label, "status": "error", "jobs": None, "verified_at": None})

    for label, ids in active_ids_by_source.items():
        for job in old.values():
            if f'{job.get("platform","").lower()}:{job.get("board","")}' == label and job["id"] not in ids:
                job["status"] = "inactive"

    jobs = sorted(old.values(), key=lambda item: (item.get("published_at") or "", item.get("last_verified_at") or ""), reverse=True)
    payload = {
        "generated_at": utc_now(),
        "jobs": jobs,
        "sources": source_results,
        "errors": errors,
        "notice": "Listings are links to original employer/platform pages. Confirm eligibility and availability on the source before applying.",
    }
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
    return payload
