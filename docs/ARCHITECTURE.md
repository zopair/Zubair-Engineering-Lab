# Lab Architecture

## Architectural boundary

Zubair Engineering Lab is a portfolio control plane. It does not absorb every product into one repository and does not become a runtime dependency for independent products.

```text
                 ZUBAIR ENGINEERING LAB
       Governance | Registry | Standards | QA
                         |
       +-----------------+------------------+
       |                 |                  |
  AI & Agents       Data Platform      Cloud & DevOps
       |                 |                  |
       +-----------------+------------------+
                         |
             Independent project repositories
                         |
         Product-specific CI, deployment and runtime
```

## Layers

1. **Portfolio layer** — project registry, priorities, lifecycle, risks and milestones.
2. **Standards layer** — architecture, coding, testing, security, release and documentation conventions.
3. **Shared capability layer** — reusable libraries and templates only where duplication and ownership justify extraction.
4. **Product layer** — independently versioned repositories, services, data and deployments.
5. **Evidence layer** — CI runs, test reports, release artifacts, security findings and operational metrics.

## Integration rules

- Integrate through documented APIs, events, packages or workflow artifacts.
- Avoid direct cross-repository source coupling.
- Pin dependency versions and define compatibility contracts.
- Keep secrets and environment-specific configuration outside Git.
- Record significant cross-project decisions in ADRs.
- Do not mirror third-party upstream repositories as if they were internally authored products.

## Project lifecycle

`proposed → discovery → active → validation → production → maintenance → archived`

A lifecycle transition requires evidence appropriate to the stage. A public repository or a green workflow alone does not establish production readiness.

## Initial delivery sequence

- M0: inventory and access verification.
- M1: project registry and governance standards.
- M2: reusable CI and project templates.
- M3: onboard existing repositories in priority order.
- M4: deliver a thin, working Enterprise AI & Data Platform vertical slice.
- M5: portfolio dashboard based on verified repository and CI data.
