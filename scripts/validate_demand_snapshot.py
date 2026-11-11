#!/usr/bin/env python3
"""Validate the demand snapshot using Python standard library only."""
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "research" / "upwork-demand" / "sample_jobs.json"
ALLOWED = {"excel_data", "wordpress_web", "python_scraping", "api_workflow", "pdf_documents", "dashboards_bi"}


def validate(payload):
    errors = []
    required = {"dataset_id", "snapshot_date", "source", "methodology", "caveats", "category_counts", "jobs"}
    missing = required - payload.keys()
    if missing:
        return ["missing top-level keys: " + ", ".join(sorted(missing))]
    try:
        date.fromisoformat(payload["snapshot_date"])
    except (TypeError, ValueError):
        errors.append("snapshot_date must be an ISO date")
    jobs = payload["jobs"]
    if not isinstance(jobs, list) or not jobs:
        return errors + ["jobs must be a non-empty array"]
    ids, urls, counts = [], [], Counter()
    required_job = {"id", "title", "category", "url", "budget", "summary", "delivery_notes", "snapshot_date"}
    for i, job in enumerate(jobs):
        p = "jobs[" + str(i) + "]"
        if not isinstance(job, dict):
            errors.append(p + " must be an object")
            continue
        absent = required_job - job.keys()
        if absent:
            errors.append(p + " missing: " + ", ".join(sorted(absent)))
            continue
        if not re.fullmatch(r"J\d{2}", str(job["id"])):
            errors.append(p + ".id must match JNN")
        ids.append(job["id"])
        if job["category"] not in ALLOWED:
            errors.append(p + ".category is not supported")
        else:
            counts[job["category"]] += 1
        parsed = urlparse(str(job["url"]))
        if parsed.scheme != "https" or parsed.netloc != "www.upwork.com" or not parsed.path.startswith("/jobs/~"):
            errors.append(p + ".url must be an Upwork job URL")
        urls.append(job["url"])
        for field in ("title", "summary", "delivery_notes"):
            if not isinstance(job[field], str) or not job[field].strip():
                errors.append(p + "." + field + " must be non-empty text")
        try:
            date.fromisoformat(job["snapshot_date"])
        except (TypeError, ValueError):
            errors.append(p + ".snapshot_date must be an ISO date")
        if job["budget"] is not None and not isinstance(job["budget"], str):
            errors.append(p + ".budget must be text or null")
    if len(ids) != len(set(ids)):
        errors.append("job IDs must be unique")
    if len(urls) != len(set(urls)):
        errors.append("job URLs must be unique")
    if dict(counts) != payload["category_counts"]:
        errors.append("category_counts does not match actual job records")
    if len(jobs) != 20:
        errors.append("expected 20 sample jobs; found " + str(len(jobs)))
    return errors


def main():
    try:
        payload = json.loads(DATA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print("FAIL: cannot read dataset: " + str(exc), file=sys.stderr)
        return 2
    errors = validate(payload)
    if errors:
        for error in errors:
            print("FAIL: " + error, file=sys.stderr)
        return 1
    print("PASS: 20 jobs; six categories; unique IDs/URLs; counts and URLs valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
