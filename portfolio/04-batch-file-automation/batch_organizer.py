"""Safe, dry-run-first batch file renaming utility.

Only regular files directly inside the selected directory are considered.
Existing destinations are never overwritten.
"""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


def _normalize_extensions(extensions: Iterable[str] | None) -> set[str] | None:
    if extensions is None:
        return None
    normalized = set()
    for extension in extensions:
        value = extension.strip().lower()
        if not value:
            continue
        normalized.add(value if value.startswith(".") else f".{value}")
    return normalized


def build_plan(
    directory: str | Path,
    *,
    prefix: str = "",
    suffix: str = "",
    extensions: Iterable[str] | None = None,
) -> list[dict[str, str]]:
    """Build a deterministic rename plan without changing the filesystem."""
    root = Path(directory).expanduser()
    if not root.exists() or not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")
    if not prefix and not suffix:
        raise ValueError("Provide a non-empty prefix or suffix")

    allowed = _normalize_extensions(extensions)
    candidates = sorted(
        (entry for entry in root.iterdir() if entry.is_file() and not entry.is_symlink()),
        key=lambda entry: entry.name.casefold(),
    )
    plan: list[dict[str, str]] = []
    reserved: set[str] = set()

    for source in candidates:
        if allowed is not None and source.suffix.lower() not in allowed:
            continue
        destination_name = f"{prefix}{source.stem}{suffix}{source.suffix}"
        destination = source.with_name(destination_name)
        key = destination.name.casefold()

        if destination == source:
            status, reason = "skipped", "destination_is_source"
        elif key in reserved:
            status, reason = "skipped", "duplicate_planned_destination"
        elif destination.exists() or destination.is_symlink():
            status, reason = "skipped", "destination_already_exists"
        else:
            status, reason = "planned", ""

        reserved.add(key)
        plan.append({
            "source": str(source),
            "destination": str(destination),
            "status": status,
            "reason": reason,
        })
    return plan


def execute_plan(
    plan: list[dict[str, str]],
    *,
    apply: bool = False,
    audit_path: str | Path | None = None,
) -> dict[str, object]:
    """Execute eligible moves only when apply=True; never replace a destination."""
    results: list[dict[str, str]] = []
    applied = 0

    for item in plan:
        result = dict(item)
        if result["status"] == "planned":
            if not apply:
                result["status"] = "dry_run"
            else:
                source = Path(result["source"])
                destination = Path(result["destination"])
                try:
                    if not source.is_file() or source.is_symlink():
                        raise FileNotFoundError("Source is no longer a regular file")
                    # link() creates the destination atomically and fails if it exists.
                    # Both paths are in the same directory/filesystem.
                    os.link(source, destination, follow_symlinks=False)
                    try:
                        source.unlink()
                    except OSError:
                        destination.unlink(missing_ok=True)
                        raise
                    result["status"] = "applied"
                    applied += 1
                except FileExistsError:
                    result["status"] = "skipped"
                    result["reason"] = "destination_already_exists_at_execution"
                except OSError as exc:
                    result["status"] = "failed"
                    result["reason"] = f"{type(exc).__name__}: {exc}"
        results.append(result)

    summary: dict[str, object] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": "apply" if apply else "dry_run",
        "planned": sum(1 for item in plan if item["status"] == "planned"),
        "applied": applied,
        "skipped": sum(1 for item in results if item["status"] == "skipped"),
        "failed": sum(1 for item in results if item["status"] == "failed"),
        "items": results,
    }
    if audit_path is not None:
        target = Path(audit_path).expanduser()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan or safely apply batch file renames.")
    parser.add_argument("directory", type=Path, help="Directory to scan (non-recursive)")
    parser.add_argument("--prefix", default="", help="Prefix to add to each selected filename")
    parser.add_argument("--suffix", default="", help="Suffix to add before the extension")
    parser.add_argument("--ext", action="append", dest="extensions", help="Allowed extension; repeat as needed")
    parser.add_argument("--apply", action="store_true", help="Actually rename files; default is dry-run")
    parser.add_argument("--audit", type=Path, help="Optional JSON audit-log destination")
    args = parser.parse_args()

    try:
        plan = build_plan(
            args.directory,
            prefix=args.prefix,
            suffix=args.suffix,
            extensions=args.extensions,
        )
        report = execute_plan(plan, apply=args.apply, audit_path=args.audit)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if report["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
