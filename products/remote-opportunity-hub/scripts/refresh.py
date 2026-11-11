from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from remote_hub.ingest import refresh


def main():
    parser = argparse.ArgumentParser(description="Refresh verified public remote job feeds.")
    parser.add_argument("--config", default=str(ROOT / "config/sources.json"))
    parser.add_argument("--output", default=str(ROOT / "web/jobs.json"))
    args = parser.parse_args()
    result = refresh(args.config, args.output)
    print(json.dumps({
        "generated_at": result["generated_at"],
        "jobs": len([job for job in result["jobs"] if job.get("status") == "active"]),
        "sources_ok": sum(1 for source in result["sources"] if source["status"] == "ok"),
        "sources_failed": sum(1 for source in result["sources"] if source["status"] == "error"),
    }, indent=2))
    if result["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
