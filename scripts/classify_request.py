#!/usr/bin/env python3
"""Deterministic, dependency-free first-pass request classifier."""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAYBOOKS = ROOT / "config" / "delivery_playbooks.json"


def normalize(value):
    return re.sub(r"\s+", " ", str(value or "").lower()).strip()


def classify(request, config):
    text = normalize(request)
    scores = {}
    for family, item in config["categories"].items():
        scores[family] = sum(1 for term in item["keywords"] if normalize(term) in text)
    ranked = sorted(scores.items(), key=lambda pair: (-pair[1], pair[0]))
    best_score = ranked[0][1] if ranked else 0
    winners = [name for name, score in ranked if score == best_score and score > 0]
    flags = []
    for flag in config.get("global_red_flags", []):
        if any(normalize(phrase) in text for phrase in flag["phrases"]):
            flags.append({"id": flag["id"], "action": flag["action"]})
    if not winners:
        return {
            "status": "unclassified",
            "category": None,
            "scores": scores,
            "red_flags": flags,
            "provided_request": request,
            "missing_information": ["Clarify the desired outcome, input, output and system involved."],
            "tools": [],
            "acceptance_checks": [],
            "estimate_status": "not_estimable_until_scope_is_bounded"
        }
    if len(winners) > 1:
        return {
            "status": "ambiguous",
            "category": None,
            "candidates": winners,
            "scores": scores,
            "red_flags": flags,
            "provided_request": request,
            "missing_information": ["Choose the primary deliverable or split the request into independently scoped work packages."],
            "tools": [],
            "acceptance_checks": [],
            "estimate_status": "not_estimable_until_scope_is_bounded"
        }
    category = winners[0]
    playbook = config["categories"][category]
    return {
        "status": "red_flag" if flags else "classified",
        "category": category,
        "readiness": playbook["readiness"],
        "scores": scores,
        "red_flags": flags,
        "provided_request": request,
        "missing_information": playbook["intake"],
        "tools": playbook["tools"],
        "acceptance_checks": playbook["acceptance"],
        "estimate_status": "not_estimable_until_scope_is_bounded"
    }


def main():
    parser = argparse.ArgumentParser(description="Classify a scoped customer request without network access.")
    parser.add_argument("request", help="Customer request text; do not include credentials or personal data.")
    parser.add_argument("--playbooks", default=str(PLAYBOOKS))
    args = parser.parse_args()
    try:
        config = json.loads(Path(args.playbooks).read_text(encoding="utf-8"))
        result = classify(args.request, config)
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        print("Configuration error: " + str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
