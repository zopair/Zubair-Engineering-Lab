# ADR 0001: Portfolio control plane, independent product repositories

- Status: Accepted
- Date: 2026-11-11

## Context

The portfolio contains projects with different stacks, deployment lifecycles, data boundaries and maturity levels. Combining all source code in one monorepo would create unnecessary coupling and migration risk.

## Decision

Use Zubair Engineering Lab as the central portfolio control plane for registry, standards, architecture decisions, templates, shared automation and evidence. Keep product code in independent repositories by default.

## Consequences

- Projects can ship independently.
- Shared components require explicit ownership and versioning.
- The registry becomes the authoritative index, not a copy of project source.
- Cross-project changes require compatibility and security review.
- Existing repositories are not moved, renamed or deleted as part of lab setup.
