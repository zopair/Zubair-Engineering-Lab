# Engineering Lab — Execution Backlog

**Date:** 2026-11-11  
**Status:** Initial prioritized backlog derived from the partial audit.  
**Rule:** No task is marked complete without an inspectable artifact or execution result.

## Execution update — 2026-11-11

### SAA security stabilization — code changes committed, runtime verification pending

The following changes have been committed to Sovereign-AI-Arsenal:

- Removed PostgreSQL trust authentication and hard-coded database credentials from Compose/config defaults.
- Split the PostgreSQL bootstrap administrator from a least-privilege application role.
- Added URL-safe SQLAlchemy credential construction and fail-fast behavior when DB_PASSWORD is absent.
- Restricted PostgreSQL, Grafana, Prometheus and API host bindings to loopback by default; Redis is not host-published.
- Replaced wildcard CORS defaults with an empty allowlist and explicit CORS_ORIGINS configuration.
- Fixed log-directory initialization order, SQLAlchemy health-check execution, database session lifecycle, and package-relative config loading.
- Corrected container startup to import the backend as a package and run as a non-root user.
- Added a safe blank-secret environment template and regression tests.
- Removed inaccurate claims that API authentication and production readiness are already implemented.

### Verification performed

- Six focused regression tests passed in an isolated verification workspace populated from the committed file contents.
- Docker Compose YAML parsed successfully in that workspace.
- PostgreSQL bootstrap shell script passed shell syntax validation.
- The GitHub connector does not provide a shell/container runtime in this workflow. Docker is unavailable in the verification runtime, so no image build, Compose config interpolation, database initialization, API startup or integration suite is claimed as passed.

### Migration safety gate

The new PostgreSQL role bootstrap runs only when the data volume is initialized for the first time. Do not delete or recreate any existing volume to apply it. Existing installations require a backup and a separately reviewed role/password migration before deployment.

### Current task states

| Task | State |
|---|---|
| SAA-001 — Compose validation and safe defaults | Code updated; Docker validation pending |
| SAA-002 — remove insecure DB defaults | Code updated; existing-volume migration pending |
| SAA-003 — logging/startup ordering | Code updated; container startup test pending |
| SAA-004 — SQLAlchemy health/session behavior | Code updated; database integration test pending |
| SAA-005 — explicit CORS allowlist | Code updated; API runtime test pending |
| SAA-006 — full regression/build verification | Focused tests passed in isolated copy; full suite and image build pending |

No existing database volume was deleted, no external API key was added, and no paid service was introduced.

## Priority model

- **P0 — Blocker / risk:** prevents safe use, trustworthy status, or further integration.
- **P1 — Foundation:** enables repeatable work across multiple projects.
- **P2 — Capability:** delivers a reusable technical capability or product milestone.
- **P3 — Optimization:** useful after the core path is proven.

## Work packages

### P0 — Establish trustworthy inventory

| ID | Task | Acceptance evidence | Dependencies |
|---|---|---|---|
| LAB-001 | Add the initial capability map and evidence levels to the lab | docs/PORTFOLIO_CAPABILITY_MAP.md committed; unknowns explicitly labelled | None |
| LAB-002 | Add this prioritized backlog and task states | docs/EXECUTION_BACKLOG.md committed; each item has acceptance evidence | None |
| LAB-003 | Resolve CLT Core repository access/content and identify the actual default-branch files | Repository root, README, manifests and source tree successfully inspected | GitHub access |
| LAB-004 | Identify Pink & Red Market's owning repository | Repository URL and product modules recorded in registry | Existing GitHub portfolio |
| LAB-005 | Determine upstream/fork status and license for high-value third-party repositories | Upstream URL, license, pinned commit, local divergence and update policy recorded for each selected dependency | Repository metadata/content access |

### P0 — Repair the highest-risk existing service

| ID | Task | Acceptance evidence | Dependencies |
|---|---|---|---|
| SAA-001 | Validate Sovereign AI Arsenal Compose configuration and fix invalid service/network/container identifiers and database URL handling | Compose config parses; services start in a clean test environment | SAA-002 |
| SAA-002 | Remove insecure database defaults (trust, known password) and require generated local secrets / safe examples | Automated config test rejects insecure production defaults; no real secret committed | None |
| SAA-003 | Fix backend startup ordering and logging directory initialization | Import/startup test succeeds from a clean checkout without pre-created log directory | SAA-001 |
| SAA-004 | Validate SQLAlchemy health-check query and database readiness behavior | Health endpoint integration test returns healthy only when DB is reachable | SAA-001 |
| SAA-005 | Replace wildcard credentialed CORS defaults with explicit environment-based origins | Config tests cover allowed and rejected origins | SAA-002 |
| SAA-006 | Verify actual test suite, migrations and Docker build; add missing regression tests before behavior changes | Reproducible test/build evidence attached to the repo | SAA-001–005 |

**Static-review findings, not yet runtime-confirmed:** the inspected Compose file contains names with spaces in service/container/network-related values and an unescaped database name in a URL; it configures PostgreSQL trust authentication and a known password; backend startup creates the log directory after configuring a file handler; and the health check uses a raw SQL string with SQLAlchemy 2.x. Verify each in a controlled test before changing it.

### P1 — Lab engineering baseline

| ID | Task | Acceptance evidence | Dependencies |
|---|---|---|---|
| LAB-006 | Expand project registry schema with owner, lifecycle, evidence level, stack, test command, deployment model, risk and next milestone | YAML schema validates and all unknown values remain explicit | LAB-001 |
| LAB-007 | Add a lightweight registry validator (schema + duplicate IDs + repository URL checks) | Unit tests include valid, invalid, duplicate and unknown-field cases | LAB-006 |
| LAB-008 | Add a reusable GitHub Actions workflow for registry validation and documentation links | Workflow runs green on pull requests and main | LAB-007 |
| LAB-009 | Define a project onboarding template and ADR template | New project can be registered consistently without copying product code | LAB-006 |
| LAB-010 | Define evidence-based maturity levels (discovery, runnable, tested, deployable, production) | Criteria are documented and applied consistently | LAB-006–010 |

### P1 — UCF security and reliability path

| ID | Task | Acceptance evidence | Dependencies |
|---|---|---|---|
| UCF-001 | Threat-model control plane, worker identity, task submission and Docker execution boundaries | Reviewed threat model and abuse cases | Existing UCF M2 |
| UCF-002 | Implement OIDC-compatible authentication, RBAC and tenant quotas | Integration tests prove cross-tenant access is denied | UCF-001 |
| UCF-003 | Test worker crash, daemon failure, expired lease and stale claim-token recovery | Deterministic fault-injection tests pass | UCF-001 |
| UCF-004 | Add dependency lock strategy, SBOM generation and vulnerability scanning | CI publishes SBOM and fails on defined severity policy | Existing CI |
| UCF-005 | Evaluate Firecracker/gVisor/Wasmtime as isolated execution adapters | Benchmark and security comparison; no adoption without workload compatibility tests | UCF-001 |
| UCF-006 | Add load tests for scheduler and concurrent reservations | Reproducible throughput/latency report with hardware and dataset disclosed | UCF-003 |
### P1 — Product-specific critical paths

| ID | Task | Acceptance evidence | Dependencies |
|---|---|---|---|
| KDP-001 | Verify all 24 original illustrations against dimensions, color mode and page mapping | Artwork preflight report passes | Existing KDP pipeline |
| KDP-002 | Validate rendered Arabic/English PDF in KDP Print Previewer and document the outcome | Previewer evidence and explicit accept/reject decision | KDP-001 |
| KDP-003 | Add reproducible visual regression checks for page layout and RTL text | Baseline proof images and reviewed diff | KDP-001 |
| AI-001 | Map overlap and ownership between Zubair AI Army, Zubair Hunter AI, CLT Platform and CLT Core | One architecture/ownership map with verified code references | LAB-003 |
| AI-002 | Select one agent orchestration approach for the first real workload | Decision record comparing existing code, complexity, license, model cost and tool support | AI-001 |
| AI-003 | Verify zero-cost/local inference path using Ollama; document model/hardware limits | Successful local inference test and resource report | AI-002 |

### P2 — Reusable data and platform capabilities

| ID | Task | Acceptance evidence | Dependencies |
|---|---|---|---|
| DATA-001 | Evaluate Airbyte and OpenMetadata for a single real portfolio data source | Working ingestion + catalog demo with lineage or clear documented limitation | LAB-005 |
| DATA-002 | Choose one application backend per product based on auth, DB, storage, portability and maintenance | ADR; no portfolio-wide forced backend | LAB-005 |
| OPS-001 | Standardize OpenTelemetry conventions and health/readiness endpoints where applicable | One service emits traces/metrics with documented local setup | LAB-006 |
| OPS-002 | Add secret scanning, dependency scanning and IaC scanning to suitable first-party repositories | CI results and documented false-positive policy | LAB-008 |
| PORTAL-001 | Reassess Backstage only after registry and metadata are reliable | Go/no-go ADR based on actual self-service/catalog needs | LAB-006–010 |

## Recommended execution order

1. LAB-001 and LAB-002 — publish the evidence map and backlog.
2. LAB-003 to LAB-005 — close inventory unknowns that change architecture choices.
3. SAA-001 to SAA-006 — repair or formally quarantine Sovereign AI Arsenal.
4. LAB-006 to LAB-010 — make the lab registry self-validating.
5. UCF-001 to UCF-004 — raise the highest-value compute asset's security and reliability floor.
6. KDP-001 to KDP-003 — clear the production-critical artwork and platform-validation gates.
7. AI-001 to AI-003 — resolve overlapping agent/CLT projects and select one stack for one use case.
8. Expand data, observability and portal capabilities only when a project needs them.

## Explicit non-goals for this phase

- No mass migration or monorepo consolidation.
- No bulk installation of every open-source repository.
- No Kubernetes requirement for all projects.
- No paid API, paid cloud, or card-required service as a mandatory baseline.
- No production-readiness claims based only on README or a green CI badge.
- No deletion of repositories or experimental code during inventory.

## Follow-up audit — Sovereign AI Arsenal runtime blockers (2026-11-11)

A second source inspection was performed after the initial hardening commit. The following are **newly observed code-level findings**, not runtime-confirmed failures:

| ID | Priority | Finding | Required evidence / action |
|---|---|---|---|
| SAA-007 | P0 | API routes have no authentication/authorization dependency. Compose defaults to loopback, but configurable bind addresses and the Nginx proxy could expose unauthenticated discovery, analysis and data endpoints if deployed publicly. | Keep all ingress loopback-only until an authentication design and route-level authorization tests exist. Add auth/RBAC before any public binding. |
| SAA-008 | P1 | Both discovery and analysis endpoints pass a request-scoped SQLAlchemy Session into BackgroundTasks. The worker then retains and reuses that session across asynchronous network work. | Refactor workers to create/close their own session inside the worker; add tests proving no request Session is captured or reused. |
| SAA-009 | P1 | `get_statistics()` referenced `timedelta` without a module-level import. | **Code fix committed** in `backend/api/routes.py`; structural regression test added and passed (1 passed in isolated test workspace). Full endpoint integration test remains pending. |
| SAA-010 | P1 | The backend image installs the entire broad requirements file, including notebook/Colab, browser automation, NLP and other potentially optional packages. | Build an import map first; split runtime, optional feature and dev/test dependencies only after proving each import path and image build. Do not remove packages by name alone. |
| SAA-011 | P0 | Nginx proxies API, docs and ReDoc without authentication. This is acceptable only while every published ingress remains loopback-bound. | Keep Nginx loopback-bound; disable public deployment until auth, TLS certificate provisioning and route policy are verified. |
| SAA-012 | P1 | Docker Compose passes database and Grafana credentials through environment variables. Docker recommends Compose secrets for sensitive values where supported. | Evaluate file-backed Compose secrets and application `*_FILE` support; retain current required-secret fail-fast behavior until the replacement is tested end-to-end. |

### Updated execution gate

1. Preserve loopback-only exposure; do not set API/Nginx bind variables to public interfaces.
2. Fix and test the statistics endpoint regression.
3. Refactor background tasks to own their database sessions.
4. Design and test API authentication/authorization before public exposure.
5. Build and run the container stack in a real Docker-capable runner, with a disposable test database volume only.
6. Review dependency imports and image size; split optional dependencies only with tests and a successful image build.

The source inspection also confirmed that PostgreSQL initialization scripts run only for an empty data directory; existing volumes must not be deleted to force bootstrap. Docker's current guidance likewise describes this first-initialization behavior and recommends dedicated application roles and limited network exposure. See [Docker PostgreSQL guide](https://docs.docker.com/guides/postgresql/) and [Compose secrets guidance](https://docs.docker.com/compose/how-tos/use-secrets/).

## SAA implementation update — API boundary and background sessions (2026-11-11)

Code changes committed to `zopair/Sovereign-AI-Arsenal`:

- Added fail-closed shared API-key validation in `backend/security.py`, using constant-time comparison.
- Added HTTP middleware requiring `X-API-Key` for `/api/*` and `/metrics`; missing server configuration returns 503 and invalid/missing client keys return 401. `/health` remains available for container probes.
- Added required `API_AUTH_TOKEN` Compose interpolation and blank `.env.example` entry. The deployment will not start through Compose until a unique value is configured.
- Updated README security and authenticated request instructions. This is a shared-token gate only; it is **not** user identity, RBAC, tenant isolation or OAuth.
- Refactored discovery and analysis background workers to accept identifiers/data only, open short-lived database sessions for database operations, and perform network/model work outside those sessions.
- Added focused regression tests for API key behavior, request/background session separation and the statistics import.
- Added `.github/workflows/backend-verify.yml` to run focused tests and build the backend image on relevant pushes and pull requests.

### Verification boundary

- Four focused tests passed in a local isolated harness using a reduced structural fixture. This confirms the test assertions and helper behavior, **not** the full repository test suite or the actual container runtime.
- The GitHub Actions workflow has been committed; a completed run has not yet been inspected. Do not report CI green until its run result and logs are checked.
- Docker image build, Compose startup, database integration, and authenticated HTTP request tests remain pending.
- API key protection is a necessary first boundary, not sufficient for public production exposure. Keep all published ports loopback-bound; complete identity/RBAC, TLS deployment validation, and security review before public exposure.

### Updated task states

| Task | State |
|---|---|
| SAA-007 — API authentication gate | Shared API-key middleware committed; runtime test and RBAC remain |
| SAA-008 — background DB session ownership | Workers refactored to own short-lived sessions; DB integration/fault tests pending |
| SAA-009 — statistics timedelta regression | Fix and regression test committed; endpoint integration pending |
| SAA-010 — dependency minimization | Deferred pending import map and successful image build |
| SAA-011 — Nginx/public ingress boundary | Loopback defaults retained; auth does not authorize public exposure |
| SAA-012 — Compose secrets migration | Deferred; current fail-fast environment secret model retained pending end-to-end secrets-file support |
| SAA-013 — CI verification gate | Workflow committed; first GitHub Actions result not yet verified |

### Follow-up refinement — API key/CORS boundary and CI gate (2026-11-11)

- CORS now explicitly permits the `X-API-Key` header and is registered outside the authentication middleware so preflight handling and CORS response headers wrap authorization responses.
- The auth middleware bypasses only CORS `OPTIONS` preflight; protected `/api/*` and `/metrics` requests still require the configured key.- README now documents the required token and a curl example.
- Added structural regression checks for the protected paths, CORS preflight, required Compose secret, and worker-owned sessions.
- Added a backend CI workflow with Python compile checks, focused tests, and a Docker image build.

**Current verification status:** the workflow and tests are committed, but the GitHub connector did not return a completed push-run result (its available commit-run view is PR-filtered). The local network runtime cannot reach GitHub raw content, and no Docker daemon is available here. Therefore no claim is made that the full source test job or image build has passed.

**Operational caution:** a shared API key is an initial access gate, not production identity/RBAC. Public ingress remains disabled. Nginx TLS certificate provisioning and protected documentation policy still need runtime review.

### Snapshot adapter contract correction (2026-11-11)

A follow-up inspection of `backend/core/discovery.py` showed that `update_repository_metrics()` accesses `repository.full_name` as an attribute. The session-isolation refactor initially passed a plain dictionary, which would have broken that call. Corrected the worker to pass a detached `SimpleNamespace` snapshot instead, preserving the attribute contract without retaining an ORM object/session across network calls. Added a structural regression test for this adapter contract.

The CI-focused test set now contains eight tests across the API regression and security/background-task files. These tests are committed but have **not yet been observed passing in GitHub Actions**. Docker build and full runtime integration remain unverified.

### Discovery HTTP client lifetime correction (2026-11-11)

A further source trace found that `update_repository_metrics()` previously opened and closed its own aiohttp session, while the analysis worker then called `get_repository_readme()` on that now-closed session. The analysis worker now owns one `async with discovery_engine` scope spanning both metrics and README retrieval; `update_repository_metrics()` now uses the caller-owned session rather than closing it. Added regression guards for the shared client lifetime and the attribute-based detached repository snapshot.

The focused CI set now contains ten tests. Their execution and the Docker build remain pending inspection of a completed GitHub Actions run.


## Consolidated audit correction — 2026-11-11

This section supersedes earlier status statements in this file where they conflict with the verified runs below. Do not restart already-green CI jobs merely to reproduce the same evidence.

### Verified execution evidence

| Project | Evidence | Current decision |
|---|---|---|
| Sovereign AI Arsenal | PR #2 backend run 42959911803 passed focused regressions, Docker image build, disposable PostgreSQL startup, health and API-auth checks. Sandbox run 42959911801 passed. | Keep PR #2 open for review; code is not yet on main. PR #1 remains an old draft and is not a prerequisite for starting other work. |
| Universal Compute Fabric | Main CI run 42864498823 passed on 2026-11-10. M2 roadmap records task lifecycle, reservations, claim fencing and Docker smoke test as complete. | M2 experimental foundation is established. Do not expand into enterprise security work before the first real workload requires it. |
| Amazon KDP Pipeline | Feature-branch run 42718252743 passed bilingual content audit, generation/audit of 24 original illustrations, EPUBCheck 5.4.0, print PDF render/preflight, full-wrap cover and proof packaging. | Production pipeline exists on a feature branch. Review the artifacts and KDP Print Previewer; release was skipped and Arabic paperback eligibility remains unresolved. |
| Zubair AI Army | Main CI run 42894115088 and Pages deployment 42894113040 passed. | Treat as an active codebase with multiple modules, not yet as a single verified production system. |
| SINC-OS | Main CI run 40488818115 passed. | Keep in discovery until its runtime boundary with CLT Platform is clear. |
| CLT Platform | Main workflow run 42931512191 failed at configuration validation because YouTube OAuth credentials were absent; media generation/publishing was skipped. | This is an external-credential gate, not a code regression. Do not spend time retrying without credentials or an offline-preview requirement. |
| CLT Core Monorepo | The current main branch points to an empty Git tree; README is absent. Historical OPENCONNECT runs failed on a separate branch. | Keep the prototype isolated on its branch; inspect the failed metrics artifact and decide whether to promote it. Do not treat the empty main branch as the working source. |
| Pink & Red Market | No matching repository was found in the account repository search. | Keep repository identification as a product-start task, not a lab-foundation blocker. |

### Close / defer decisions

- **Close as verified:** UCF M2 CI foundation; SAA PR-branch backend and sandbox verification; KDP feature-branch production pipeline checks; Zubair AI Army main CI; SINC-OS main CI.
- **Keep visible but do not block the portfolio:** SAA PR review, KDP platform acceptance, CLT Platform OAuth configuration, CLT Core source recovery, Hunter AI tracked-artifact security review, Pink & Red Market repository identification.
- **Do not start in this phase:** portfolio-wide Kubernetes, Backstage portal, shared database, broad observability rollout, bulk upstream cloning, or enterprise identity work for projects that do not yet need it.
- **No destructive actions:** do not delete databases, volumes, tracked local artifacts, branches, or repositories as part of this closure pass.

### Actual start-work threshold

The lab is sufficiently established to stop general preparation. Choose one real deliverable and implement it in its owning repository. Shared controls are added only when that deliverable requires them. No further portfolio-wide readiness campaign is authorized by this backlog.

## Upwork Demand Intelligence & Delivery Readiness Hub — 2026-11-11

| ID | Priority | Work | State | Acceptance / next gate |
|---|---|---|---|---|
| DEMAND-001 | P1 | Preserve 20 targeted Upwork postings in a dated structured snapshot | Implemented | JSON snapshot, category counts, source URLs and methodology stored under research/upwork-demand/ |
| DEMAND-002 | P1 | Document demand patterns, intake pipeline, scope and commercial guardrails | Implemented | docs/UPWORK_DEMAND_INTELLIGENCE.md |
| DEMAND-003 | P1 | Map six service families to existing portfolio samples, tools, license risks and acceptance checks | Implemented | docs/DELIVERY_READINESS_MATRIX.md; gaps remain explicitly marked |
| DEMAND-004 | P1 | Add deterministic dataset validator and regression tests | Verified | GitHub Actions run 43073715347 passed; five tests passed |
| DEMAND-005 | P1 | Add deterministic request classifier and six family playbooks | Verified | GitHub Actions run 43074061505 passed; six classifier tests passed, including Arabic routing, ambiguity, unclassified input and red-flag handling |
| DEMAND-006 | P2 | Extend the highest-value capability gaps only when a real scoped request requires them | Deferred by design | First candidates: Google Sheets adapter, WordPress staging/form QA, fillable PDF forms, compliant scraper checkpoints and client BI connectors |

### Delivery rules

- The 20-posting dataset is a purposive capability-fit sample, not a random market sample or market-share estimate. Keep the snapshot immutable and add dated snapshots for future research.
- Do not install or clone a tool until the use case, upstream maintenance, exact license, transitive dependencies and resource cost have been checked.
- Prefer Python standard library and existing sample implementations for the first version; the new validator introduces no runtime package dependency.
- Do not treat a portfolio sample as proof of compatibility with a client's production environment.
- Keep client data, private proposals, credentials, cookies and personal data out of the public repository.
- Red-flag requests involving payment handling, credential sharing, access-control bypass, unauthorized scraping, destructive production changes or regulated professional judgment must be rejected or re-scoped.
- No Connects were spent and no proposals were submitted in this research implementation.

### Immediate next gate

The dataset validator (five tests) and request classifier (six tests) are verified green in GitHub Actions runs 43073715347 and 43074061505. The first classifier run exposed a non-ambiguous fixture; the fixture was corrected and the rerun passed. No external dependencies were added.
