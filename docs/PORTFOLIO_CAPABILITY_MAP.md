# Portfolio Capability Map — Initial Evidence-Based Baseline

**Date:** 2026-11-11  
**Status:** Initial / partial audit. This is a decision baseline, not a claim that every repository has been code-reviewed or executed.

## Executive assessment

The portfolio already has breadth across AI agents, workflow automation, data platforms, cloud/compute, application backends, security tooling, and digital content production. The main constraint is not a lack of frameworks. It is the absence of verified integration, repeatable operational evidence, and a single current view of what is implemented, runnable, secure, and reusable.

The lab should act as a **portfolio control plane and evidence registry**, not as a replacement for existing products or a forced monorepo.

## Evidence levels

- **E1 — Static evidence:** README, architecture, roadmap, configuration or workflow inspected.
- **E2 — Repository evidence:** implementation, tests and dependency manifests inspected.
- **E3 — Execution evidence:** tests/build/workflow executed and result inspected.
- **E4 — Operational evidence:** deployed service, security boundary, monitoring and recovery demonstrated.

No project should be labelled production-ready from E1 evidence alone.

## Project capability map

| Project / repository | Capability contribution | Evidence now available | Main gap / decision |
|---|---|---|---|
| [Zubair Engineering Lab](https://github.com/zopair/Zubair-Engineering-Lab) | Portfolio registry, standards, ADRs and governance | E1: README, architecture, standards and registry inspected | Registry is provisional; add evidence-backed capability map and actionable backlog |
| [Universal Compute Fabric](https://github.com/zopair/Universal-Compute-Fabric) | Hybrid compute control plane, node inventory, placement, task lifecycle and worker execution | E1: README, M2 roadmap, open-source assessment and CI workflow inspected | Experimental. OIDC/RBAC/tenant quotas, hostile workload isolation, crash recovery, signed workloads, dependency/SBOM scanning and load tests remain |
| [Amazon KDP Pipeline](https://github.com/zopair/Amazon-work-) | Bilingual book content checks, PDF rendering, print preflight, artifact and release workflow | E1: README, requirements and build workflow inspected | 24 original illustrations are a hard prerequisite; Arabic RTL acceptance must be validated in KDP Print Previewer |
| [Sovereign AI Arsenal](https://github.com/zopair/Sovereign-AI-Arsenal) | Repository discovery, classification, analytics and semantic search | E2: backend routes, DB/session code, Dockerfile, Compose, Nginx and requirements inspected; focused config tests passed in an isolated verification workspace | No API authentication/authorization; request DB sessions are passed to background tasks; statistics route references an unimported `timedelta`; broad dependency set not yet optimized. Loopback-only; not production-ready |
| [Zubair AI Army](https://github.com/zopair/Zubair_AI_Army) | Portfolio initiatives spanning security, commerce, sovereign core and service delivery | E1: README inspected | Root package manifest not found at expected path; implementation, workflows and actual module boundaries remain unverified |
| [Zubair Hunter AI](https://github.com/zopair/Zubair-Hunter-AI) | CLT Sovereign OS / agent ecosystem concept | E1: README inspected | README claims 60 agents and encryption, but does not evidence implementation or security model |
| [CLT Platform](https://github.com/zopair/CLT-Platform) | Intended CLT orchestration layer | E1: minimal README inspected | Purpose is stated; architecture, source, tests and runtime remain unverified |
| [CLT Core Monorepo](https://github.com/zopair/CLT-Core-Monorepo) | Intended shared CLT core | Metadata only; README fetch returned 404 | Resolve repository contents/default branch/access before assigning a capability |
| [SINC-OS](https://github.com/zopair/SINC-OS) | Intended automation/media system | README is only a minimal stub | Do not count as a verified capability until code and workflow are inspected |
| Pink & Red Market | Commerce product and storefront | Project decisions exist in conversation; repository not identified in this pass | Locate the owning repository and map storefront, catalog, checkout, fulfillment and analytics |

## Reusable open-source assets present in the account

The repository inventory includes copies or repositories named after established projects. These are **candidate building blocks**, not verified integrated capabilities. Before use, record upstream URL, fork/mirror status, commit divergence, license, security posture, update method and local modifications.

| Capability domain | Candidate repositories present | Potential role |
|---|---|---|
| Agent frameworks and orchestration | LangChain, AutoGen, CrewAI, AutoGPT, AgentGPT, TaskMatrix, Langflow, Flowise | Agent/workflow prototyping; select per workload rather than combining every framework |
| Local and accelerated inference | Ollama, vLLM, Transformers | Local model serving, inference APIs and model integration; hardware and model-license checks required |
| Agent memory and tool integration | Mem0, Composio | Memory abstraction and external-tool integrations |
| Workflow automation | n8n, Activepieces, Huginn | Business and engineering workflow automation |
| Data ingestion and catalog | Airbyte, OpenMetadata | Connector-based ingestion, metadata catalog and lineage foundation |
| Analytics | Metabase, OpenBB | Business analytics and financial/research interfaces; distinct product scopes |
| Backend / data platforms | Supabase, Appwrite, PocketBase, Directus, Strapi, Payload, NocoDB | Candidate backends and admin/data layers; choose one per product boundary |
| Security and validation | testssl.sh, sqlmap, nuclei, KICS, OWASP CheatSheetSeries | Security assessment and IaC scanning; use only on owned or explicitly authorized targets |
| Infrastructure and runtime | Kubernetes, Ansible, Docker CE, Wasmer, ROS 2, Linux | Infrastructure, configuration, runtime and device/edge foundations |
| Mobile and desktop | Flutter, Tauri, Android platform source, Termux | Mobile/desktop delivery and device-side capabilities |

## Initial capability conclusions

1. **Compute scheduling is the most technically differentiated existing asset.** UCF already documents a real control-plane/worker architecture and CI integration tests. Preserve its product boundary and harden it in stages.
2. **KDP has a defined deterministic production pipeline.** Its critical path is original artwork and platform acceptance, not adding another agent framework.
3. **Sovereign AI Arsenal is a possible portfolio intelligence service, but not yet a trusted operational dependency.** Its configuration and startup path need repair and tests before it can become the lab's source of truth.
4. **The AI Army / Hunter / CLT family may overlap.** Do not merge them until ownership, code boundaries, runtime responsibilities and actual duplication are established.
5. **There is ample upstream tooling.** The lab's value will come from selection, adapters, policy, integration and evidence—not from accumulating more cloned repositories.

## Immediate architectural direction

- Keep GitHub as source control and CI evidence initially.
- Keep product repositories independently deployable.
- Keep the portfolio registry declarative and human-reviewable.
- Use PostgreSQL only where an application needs durable structured state; do not introduce a shared database dependency for every product.
- Prefer GitHub Actions for existing CI and local/self-hosted runners where workloads require it.
- Evaluate Backstage only when a searchable service catalog, ownership, templates and plugin-backed portal materially improve operations. It is not a prerequisite for M0/M1.
- Avoid requiring Kubernetes, a paid LLM API, or a paid cloud account for the initial lab control plane.

## External architecture references

- [CNCF — Backstage project](https://www.cncf.io/projects/backstage/)
- [CNCF — Building a cloud-native IDP with Kubernetes, GitOps and supply-chain security](https://www.cncf.io/blog/2026/05/29/building-a-cloud-native-internal-developer-platform-with-kubernetes-gitops-and-supply-chain-security/)
