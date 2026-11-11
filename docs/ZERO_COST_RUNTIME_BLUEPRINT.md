# Zero-Cost, Local-First Runtime Blueprint

## Objective

Eliminate recurring software-license and managed-service subscriptions wherever technically practical, while keeping the portfolio deployable on hardware controlled by the owner. The design is local-first, open-source, portable, and cost-aware.

**Important boundary:** open-source software can remove license fees; it cannot make CPU, RAM, disks, GPUs, electricity, bandwidth, backups, domain registration, or maintenance unlimited or costless. Hosted free tiers and hosted CI also have quotas. The realistic target is **zero recurring software/service spend**, not infinite compute.

## Reference architecture

| Layer | Default choice | Purpose | Cost boundary |
|---|---|---|---|
| Source of truth | GitHub repositories | Versioned source, reviewable PRs, CI evidence | Public repositories; hosted Actions still has policy and quota limits |
| Local CI and build graph | Dagger Engine | Reproducible pipelines and cache on a machine or owned server | Open-source engine runs locally; managed Dagger Cloud is a separate paid service |
| Infrastructure as code | OpenTofu | Declarative compute, networking, DNS and storage configuration | CLI is open source; provisioned cloud resources may cost money |
| Single-node orchestration | k0s or k3s | Lightweight Kubernetes for owned hardware | Software is free; host hardware and operations are not |
| Serverless workloads | Knative Serving/Eventing | HTTP services, event routing, scale-to-zero when idle | Requires Kubernetes and available underlying capacity |
| Containers | OCI images + containerd/Podman | Portable app packaging | Local execution avoids hosted runtime fees |
| API contracts | OpenAPI + FastAPI | Typed API schemas, docs, validation and client generation | Local generation; external API usage remains subject to provider policy |
| Internal credentials | OS-backed secret store + SOPS/age | Encrypt configuration and manage service credentials | Never commit plaintext secrets; external credentials must be issued by their providers |
| Local model runtime | Ollama or llama.cpp | Run supported open models on owned CPU/GPU | No per-token provider bill; hardware and model-license constraints remain |
| Data | SQLite for single-node; PostgreSQL for services; Valkey for cache | Persistent state and low-cost caching | Self-hosted; backup/storage capacity is finite |
| Observability | Prometheus + Grafana + Loki + OpenTelemetry | Metrics, logs and traces | Self-hosted; retain only useful telemetry |
| Backups | Restic to a second owned disk or approved storage | Recovery and portability | A second copy needs physical or storage capacity |

## Operating profiles

### Profile A — Developer workstation

- Run application services with Docker Compose or Podman Compose.
- Use Dagger locally for build/test pipelines.
- Use SQLite for isolated development and PostgreSQL only when integration behavior requires it.
- Run small local models only when RAM/VRAM permits.
- No public ingress by default.

### Profile B — One owned server

- Install k0s or k3s as a single-node cluster.
- Deploy ingress, TLS automation, metrics and backups.
- Use Knative only for workloads that benefit from scale-to-zero; do not add Kubernetes complexity to a simple static site or single binary.
- Keep databases stateful and backed up; do not scale them to zero blindly.
- Expose only required endpoints through a hardened reverse proxy or outbound tunnel.

### Profile C — Multiple owned nodes

- Add nodes only after measured CPU, memory, storage and network pressure.
- Use Kubernetes scheduling and replicated storage only where the availability benefit justifies the operational cost.
- Add GitOps reconciliation after the deployment manifests and rollback process are tested.
- Keep a resource budget per project; cap concurrency and model contexts.

## Repository delivery contract

Every owned application repository should expose:

1. A truthful README with supported local run commands.
2. A dependency lockfile or pinned constraints.
3. A CI workflow with read-only default permissions.
4. Unit tests and integration tests appropriate to its stack.
5. A Dockerfile or documented native runtime when deployment is required.
6. A health endpoint for long-running services.
7. A .env.example containing names and safe placeholders only.
8. No secrets, private keys, live account tokens, or credential-bearing database files.
9. A bounded resource profile and cleanup policy.
10. A deployment manifest that does not create paid cloud resources implicitly.

## Internal API-key generation

For services owned by this portfolio, generate high-entropy random keys locally (for example, Python's secrets.token_urlsafe), store only a one-way hash server-side, support rotation and revocation, and scope keys by service and capability.

This does **not** generate valid credentials for external providers, bypass quotas, or grant access to third-party APIs. External API credentials must come from the provider's documented OAuth or key-issuance flow. Prefer anonymous/public endpoints or local alternatives where permitted.

## Resource and cost controls

- Cache dependencies and build artifacts; pin cache keys to lockfiles.
- Use concurrency groups and cancel superseded CI runs.
- Run expensive workflows only on relevant path changes or manual approval.
- Prefer CPU-friendly quantized models and bounded context windows.
- Apply per-container CPU, memory, disk and timeout limits.
- Avoid permanent high-frequency polling; use webhooks or scheduled batches.
- Keep generated binaries out of Git history unless they are deliberate release assets.
- Keep artifact retention short and upload only deliverables needed for review.
- Measure actual resource usage before increasing concurrency.

## Rollout sequence

1. Inventory hardware and available network/storage capacity.
2. Establish the local Dagger pipeline and verify each repository's native tests.
3. Containerize only services with a real deployment need.
4. Deploy one pilot service on one owned host.
5. Add monitoring, backups and restore drills.
6. Add k0s/k3s and Knative only after the pilot proves a need.
7. Move remaining services in small batches with rollback evidence.

## Approval and safety gates

No infrastructure provisioning, DNS changes, external account creation, paid API activation, public exposure, destructive data migration, or production deployment is performed by this blueprint. Each requires a separate review against the actual hardware, provider terms, data sensitivity and rollback plan.
