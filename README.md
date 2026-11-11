# Zubair Engineering Lab

**Central Engineering & AI Research Workspace**

A portfolio-level engineering control plane for the Zubair technology projects. The lab standardizes architecture, delivery, testing, security, observability, and project status while keeping each product and repository independently deployable.

## Mission

- Build reusable engineering capabilities instead of duplicating solutions.
- Maintain a verified inventory of projects, repositories, dependencies, and delivery status.
- Establish consistent quality and security gates.
- Prefer free, open-source, and self-hostable tooling where practical.
- Produce demonstrable, tested software—not documentation-only prototypes.

## Operating model

The lab is the **governance and integration layer**, not a monolithic codebase. Product code stays in its owning repository unless a deliberate architecture decision says otherwise.

## Initial domains

| Domain | Scope |
|---|---|
| AI & Agents | Agent runtimes, orchestration, tool integration, evaluation |
| Data Engineering | Ingestion, transformation, storage, analytics, data quality |
| Cloud & DevOps | CI/CD, infrastructure as code, deployment, observability |
| Application Engineering | Web, mobile, APIs, SaaS and commerce |
| Automation | Workflows, content pipelines, integrations and browser-based publishing |
| Research & QA | Technical evaluation, testing, security and performance |

## Project onboarding

Every project must have an owner, purpose, repository, lifecycle status, architecture note, test strategy, deployment method, security classification, and next milestone. Unknown fields must remain explicitly marked **unknown** until verified.

See:
- [Portfolio capability map](docs/PORTFOLIO_CAPABILITY_MAP.md)
- [Prioritized execution backlog](docs/EXECUTION_BACKLOG.md)
- [Upwork Publishing Engine plan](docs/UPWORK_PUBLISHING_ENGINE.md)
- [Upwork Demand Intelligence](docs/UPWORK_DEMAND_INTELLIGENCE.md)
- [Remote Opportunity Hub — zero-budget remote job market and profile builder](products/remote-opportunity-hub/README.md)
- [Delivery Readiness Matrix](docs/DELIVERY_READINESS_MATRIX.md)
- [Dated Upwork demand snapshot](research/upwork-demand/sample_jobs.json)
- [Demand snapshot dashboard](research/upwork-demand/dashboard.html)
- [Delivery playbooks](config/delivery_playbooks.json)
- [Request classifier](scripts/classify_request.py)
- [Architecture](docs/ARCHITECTURE.md)
- [Engineering standards](standards/ENGINEERING_STANDARDS.md)
- [Portfolio repository health audit](docs/REPOSITORY_HEALTH_AUDIT.md)
- [Read-only repository auditor](scripts/repo_health_audit.py)
- [Project registry](registry/projects.yaml)
- [Decision records](docs/decisions/)

## Portfolio work samples

A client-ready sample library is maintained under [portfolio/](portfolio/README.md), with a prioritized [task catalog](portfolio/TASK_CATALOG.md). Samples are clearly labeled as demonstrations, include reproducible source and acceptance tests, and never claim unperformed client work.

## Quality principles

1. Tests before implementation for behavior changes (RED → GREEN → REFACTOR).
2. No secrets in source control, logs, screenshots, or artifacts.
3. CI must validate the actual project stack; never assume a test command.
4. Changes must be scoped, reviewable, and reversible.
5. Claims of success require execution evidence.
6. No destructive cleanup or repository consolidation without explicit review.

## Current phase

**Foundation established; product execution is the active phase.** The portfolio registry and capability map now record observed CI/build evidence and unresolved exceptions. The inventory remains explicitly partial where source is empty, credentials are absent, or a project repository is unidentified. Do not extend the foundation phase to make every project production-ready before starting a real deliverable.
