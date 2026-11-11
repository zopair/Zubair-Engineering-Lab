#!/usr/bin/env python3
"""Read-only health inventory for explicitly allowlisted Zopair repositories.

The tool never clones, writes to, opens issues in, or changes any target repository.
It uses only Python's standard library and public GitHub REST endpoints.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OWNER = "zopair"
REPOSITORIES = (
    "-CarExit-Platform",
    "-CLT_ALY",
    "Amazon-work-",
    "CLT-Core-Monorepo",
    "CLT-Core-System",
    "CLT-Platform",
    "CLT_Global_System",
    "DUBAI-NEXUS-AI",
    "EasyHub-",
    "inwork",
    "inwork-ai-repo",
    "NexaPay-Nexa-Next-Generation-Pay",
    "SENTINEL",
    "SINC-OS",
    "STAMP",
    "Sovereign-AI-Arsenal",
    "World-Monitor-Arabic",
    "Zopair",
    "Zubair-Engineering-Lab",
    "Zubair_AI_Army",
    "Zubair-Hunter-AI",
    "security_matrix",
    "universal-compute-fabric",
)
API_ROOT = "https://api.github.com"
RAW_ROOT = "https://raw.githubusercontent.com"
ENV_EXAMPLES = {".env.example", ".env.sample", ".env.template", ".env.dist"}
WORKFLOW_LIMIT = 3


def is_in_scope(name: str) -> bool:
    """Require an exact allowlist match; reject path-like or untrusted names."""
    return name in REPOSITORIES and "/" not in name and "\\" not in name


def classify_repository(
    requested_name: str,
    metadata: dict[str, Any],
    paths: list[str],
    workflow_texts: dict[str, str],
    latest_run: dict[str, Any] | None,
) -> dict[str, Any]:
    """Pure classifier: returns evidence-based findings without modifying anything."""
    if not is_in_scope(requested_name):
        return {
            "repository": requested_name,
            "status": "excluded",
            "reason": "not_in_explicit_allowlist",
            "findings": [],
        }

    owner = (metadata.get("owner") or {}).get("login")
    if owner != OWNER or metadata.get("fork") is not False:
        reason = "owner_mismatch" if owner != OWNER else "fork_repository"
        return {
            "repository": requested_name,
            "status": "excluded",
            "reason": reason,
            "findings": [],
        }

    findings: list[dict[str, str]] = []
    if metadata.get("size") == 0:
        findings.append({
            "id": "empty_repository",
            "severity": "medium",
            "evidence": "Repository has no committed source tree on its default branch",
            "recommendation": "Initialize the repository or document it as an intentionally empty placeholder before claiming operational readiness.",
        })

    tracked_env = [
        path for path in paths
        if Path(path).name.startswith(".env")
        and Path(path).name not in ENV_EXAMPLES
    ]
    if tracked_env:
        findings.append({
            "id": "tracked_env_file",
            "severity": "high",
            "evidence": f"{len(tracked_env)} tracked environment file path(s)",
            "recommendation": "Inspect without printing values; rotate any exposed credentials and remove from current tree/history through an approved incident process.",
        })

    workflows = [path for path in paths if path.startswith(".github/workflows/") and path.endswith((".yml", ".yaml"))]
    source_extensions = (".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs", ".java", ".kt", ".swift", ".php", ".rb", ".cs")
    has_source = any(path.endswith(source_extensions) for path in paths)
    if not workflows and has_source:
        findings.append({
            "id": "missing_ci",
            "severity": "medium",
            "evidence": "Source files exist but no GitHub Actions workflow files were found",
            "recommendation": "Add stack-specific tests and least-privilege CI before treating the repository as deployable.",
        })

    for path, content in workflow_texts.items():
        # Only workflow-wide permissions are flagged. A write permission scoped
        # to one release/remediation job is not equivalent to write-all.
        top_permissions = re.search(
            r"(?ms)^permissions\s*:\s*([^\n]*)\n((?:[ \t]+[^\n]*\n?)*)",
            content,
        )
        permission_block = ""
        if top_permissions:
            permission_block = (top_permissions.group(1) or "") + "\n" + top_permissions.group(2)
        if re.search(r"\bwrite-all\b", permission_block):
            findings.append({
                "id": "write_all_permissions",
                "severity": "high",
                "evidence": f"Workflow-wide write-all permissions in {path}",
                "recommendation": "Replace write-all with read-only workflow permissions and narrowly scoped job permissions.",
            })
        elif re.search(r"(?m)^\s*(?:contents|actions|pull-requests|packages):\s*write\b", permission_block):
            findings.append({
                "id": "broad_write_permissions",
                "severity": "medium",
                "evidence": f"Workflow-wide write permission in {path}",
                "recommendation": "Move write access to the single job that needs it; keep validation jobs read-only.",
            })
        if re.search(r"actions/upload-artifact@v[123]\b", content):
            findings.append({
                "id": "deprecated_artifact_action",
                "severity": "medium",
                "evidence": f"Legacy upload-artifact major version in {path}",
                "recommendation": "Upgrade to the supported upload-artifact v4+ action and verify runner compatibility.",
            })
        if re.search(r"(?m)^\s*run:\s*echo\s+['\"]?(?:ok|success|passed|tests passed)", content, re.IGNORECASE):
            findings.append({
                "id": "possible_placeholder_ci",
                "severity": "medium",
                "evidence": f"Echo-only success marker in {path}",
                "recommendation": "Verify the workflow runs real project-specific build and test commands.",
            })

    ci_summary = None
    if latest_run:
        ci_summary = {
            "name": latest_run.get("name"),
            "status": latest_run.get("status"),
            "conclusion": latest_run.get("conclusion"),
            "html_url": latest_run.get("html_url"),
            "head_branch": latest_run.get("head_branch"),
        }
        if latest_run.get("conclusion") == "failure":
            findings.append({
                "id": "latest_ci_failed",
                "severity": "high",
                "evidence": f"Latest workflow run failed: {latest_run.get('name', 'unknown')}",
                "recommendation": "Inspect failing job logs and reproduce with the repository's native build/test commands.",
            })

    return {
        "repository": requested_name,
        "status": "needs_review" if findings else "no_static_findings",
        "default_branch": metadata.get("default_branch"),
        "language": metadata.get("language"),
        "archived": metadata.get("archived", False),
        "tree_truncated": False,
        "workflow_count": len(workflows),
        "latest_ci": ci_summary,
        "findings": findings,
    }


class GitHubClient:
    def __init__(self, token: str | None = None, timeout: int = 20):
        self.token = token
        self.timeout = timeout

    def get_json(self, path: str) -> dict[str, Any]:
        request = urllib.request.Request(
            f"{API_ROOT}{path}",
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "zopair-repository-health-audit",
                **({"Authorization": f"Bearer {self.token}"} if self.token else {}),
            },
        )
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            return json.loads(response.read().decode("utf-8"))

    def get_text(self, url: str) -> str:
        request = urllib.request.Request(url, headers={"User-Agent": "zopair-repository-health-audit"})
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            return response.read().decode("utf-8", errors="replace")


def audit_one(client: GitHubClient, name: str) -> dict[str, Any]:
    if not is_in_scope(name):
        return classify_repository(name, {}, [], {}, None)

    try:
        metadata = client.get_json(f"/repos/{OWNER}/{name}")
        owner = (metadata.get("owner") or {}).get("login")
        if owner != OWNER or metadata.get("fork") is not False:
            return classify_repository(name, metadata, [], {}, None)
        if metadata.get("size") == 0:
            return classify_repository(name, metadata, [], {}, None)

        branch = metadata.get("default_branch") or "main"
        try:
            tree = client.get_json(f"/repos/{OWNER}/{name}/git/trees/{branch}?recursive=1")
        except urllib.error.HTTPError as exc:
            if exc.code != 404:
                raise
            # GitHub returns 404 for a repository with no commit/tree on its
            # configured default branch. Treat it as uninitialized, not outage.
            result = classify_repository(name, metadata, [], {}, None)
            if not any(item["id"] == "empty_repository" for item in result["findings"]):
                result["findings"].append({
                    "id": "empty_repository",
                    "severity": "medium",
                    "evidence": "Default branch has no readable Git tree",
                    "recommendation": "Initialize the repository or document it as an intentionally empty placeholder.",
                })
            result["status"] = "needs_review"
            return result
        paths = [entry.get("path", "") for entry in tree.get("tree", []) if entry.get("type") == "blob"]
        workflows = [
            path for path in paths
            if path.startswith(".github/workflows/") and path.endswith((".yml", ".yaml"))
        ][:WORKFLOW_LIMIT]
        workflow_texts: dict[str, str] = {}
        for path in workflows:
            url = f"{RAW_ROOT}/{OWNER}/{name}/{branch}/{path}"
            try:
                workflow_texts[path] = client.get_text(url)
            except (urllib.error.URLError, TimeoutError):
                workflow_texts[path] = ""

        latest_run = None
        try:
            runs = client.get_json(f"/repos/{OWNER}/{name}/actions/runs?branch={branch}&per_page=1")
            items = runs.get("workflow_runs") or []
            latest_run = items[0] if items else None
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
            # Public repos can still be inventoried when Actions metadata is unavailable.
            latest_run = None

        result = classify_repository(name, metadata, paths, workflow_texts, latest_run)
        result["tree_truncated"] = bool(tree.get("truncated"))
        if tree.get("truncated"):
            result["findings"].append({
                "id": "tree_truncated",
                "severity": "low",
                "evidence": "GitHub returned a truncated recursive tree",
                "recommendation": "Use paginated contents/tree inspection before making a completeness claim.",
            })
        return result
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {
            "repository": name,
            "status": "audit_error",
            "error_type": type(exc).__name__,
            "findings": [{
                "id": "audit_unavailable",
                "severity": "unknown",
                "evidence": "Repository metadata could not be retrieved",
                "recommendation": "Retry after checking GitHub API availability and rate limits.",
            }],
        }


def build_report(client: GitHubClient) -> dict[str, Any]:
    results = [audit_one(client, name) for name in REPOSITORIES]
    counts: dict[str, int] = {}
    severities: dict[str, int] = {}
    for result in results:
        counts[result["status"]] = counts.get(result["status"], 0) + 1
        for finding in result.get("findings", []):
            severity = finding["severity"]
            severities[severity] = severities.get(severity, 0) + 1
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": {"owner": OWNER, "allowlisted_repositories": len(REPOSITORIES), "mode": "read_only"},
        "summary": {"repositories_by_status": counts, "findings_by_severity": severities},
        "repositories": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="artifacts/repository-health-report.json")
    args = parser.parse_args()

    client = GitHubClient(token=os.environ.get("GITHUB_TOKEN"))
    report = build_report(client)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    print(f"Report written to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
