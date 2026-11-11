# Portfolio Repository Health Audit

## Purpose

This read-only auditor inventories only the explicit repository allowlist in `scripts/repo_health_audit.py`. It is designed to produce evidence and remediation priorities, not to modify repositories.

## Safety contract

- Exact allowlist under the `zopair` owner.
- Excludes forks and owner mismatches.
- Uses GitHub metadata, recursive trees, workflow YAML and latest Actions status.
- Never clones repositories, prints environment-file values, reads Actions secrets, creates PRs, pushes commits, or runs arbitrary repository code.
- Uses Python's standard library; no third-party runtime packages.
- Scheduled weekly; manual execution is available from GitHub Actions.

## Local execution

```bash
python -m unittest discover -s tests -p "test_repo_health_audit.py" -v
GITHUB_TOKEN=<read-only-token> python scripts/repo_health_audit.py
```

The token is optional for public repositories, but an authenticated read-only token increases API rate limits. Never place a token in the repository or command history; use an environment variable or secret store.

## Findings

| Finding | Meaning | Remediation |
|---|---|---|
| `tracked_env_file` | A non-template .env path is tracked | Check whether values are credentials; rotate exposed credentials and remove the file from the current tree |
| `write_all_permissions` | Workflow-wide write-all permissions | Use read-only defaults and narrow job-level write permissions |
| `broad_write_permissions` | Workflow-wide write permissions | Move write scope to the single job that needs it |
| `deprecated_artifact_action` | Legacy upload-artifact action | Upgrade to a supported version |
| `possible_placeholder_ci` | A workflow may report success without testing | Inspect the workflow and add real project-native checks |
| `missing_ci` | Source code exists without GitHub Actions checks | Add stack-specific build and test gates |
| `latest_ci_failed` | Latest workflow run concluded in failure | Inspect job logs and reproduce the failing step |
| `empty_repository` | No committed source tree exists on the default branch | Initialize or explicitly document the placeholder |
| `audit_unavailable` | GitHub API could not be read | Retry after checking API availability and rate limits |

## Interpretation limits

- A static finding is a review signal, not proof of exploitability.
- A green GitHub Actions run is not proof of production deployment or live service health.
- A missing workflow is not automatically a defect for documentation-only repositories.
- The auditor inspects at most three workflow files per repository to bound network use.
- It does not inspect secret values, private provider dashboards, runtime hosts, or external API quotas.

## Zero-cost operating model

Open-source software can remove license and subscription fees, but it cannot remove the cost of compute, storage, bandwidth, electricity, backups, or maintenance. Hosted CI and cloud providers also impose quotas. For workloads that must avoid hosted-runner quotas, run Dagger or native project test commands on hardware you control, and use a self-hosted Kubernetes distribution only when the hardware and operational capacity exist.

The control plane remains read-only by design. Remediation is delivered as reviewable pull requests, not silent pushes to production branches.
