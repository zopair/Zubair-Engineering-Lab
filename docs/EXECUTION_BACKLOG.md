# Engineering Lab — Execution Backlog

**Date:** 2026-11-11  
**Status:** Initial prioritized backlog derived from the partial audit.  
**Rule:** No task is marked complete without an inspectable artifact or execution result.

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
