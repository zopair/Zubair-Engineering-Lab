# Upwork Demand Intelligence & Delivery Readiness Hub

**Snapshot:** 2026-11-11  
**Status:** Initial evidence-backed demand baseline; readiness is capability-specific.

## Purpose
Convert representative customer requests into reusable delivery definitions: scope, inputs, tools, workflow, acceptance tests, security gates, exclusions and evidence. This remains a control-plane capability; product code stays in its owning repository.

## Evidence and limits
- Twenty targeted Upwork postings reviewed on 2026-11-11 are preserved in the research dataset.
- Selection was purposive across six service families intersecting current portfolio capabilities. It is not a random sample or a market-share estimate.
- Counts: Excel/data 5; WordPress/web 4; Python/scraping 3; API/workflow 3; PDF/documents 3; dashboards/BI 2.
- Budgets are individual listing observations, not pricing guidance. Null means no reliable fixed budget was captured.
- Listings can close or change. Revalidate listing, client history, scope, budget and Connects before applying.
- No proposal was submitted and no Connects were spent in this research pass.
- Upwork's 2026 skills report is a separate macro signal, not validation of this sample's proportions: https://www.upwork.com/press/releases/upworks-in-demand-skills-2026-demand-top-ai-skills-more-than-doubles-ai

## Repeating customer outcomes
1. Repair or improve an existing asset rather than build a large platform.
2. Normalize, validate, connect or summarize customer-owned data.
3. Automate bounded workflows and make failures observable.
4. Deliver an editable artifact plus a concise evidence/exception report.
5. Clarify access, source of truth, data handling and acceptance before estimating.

## Default delivery contracts

| Family | Inputs | Deliverables | Acceptance baseline | Existing lab samples |
|---|---|---|---|---|
| Excel & data | XLSX/CSV, data dictionary, rules | Clean workbook/CSV, exception report, transformation notes | Preserve source; reconcile row counts; test duplicates, missing values, types and formulas | Spreadsheet Cleanup & Validation; Sales KPI Dashboard |
| WordPress & web | Staging/export, theme/plugin versions, viewports | Scoped CSS/template change and before/after evidence | No overflow; responsive checks; form path; no unrelated regressions | Responsive Landing Page Repair; Elementor Mobile Section Repair; Bilingual RTL/LTR Landing Page |
| Python scraping | Public/authorized URLs, schema, rate limits | Script, structured export, logs, retry/resume | Terms review; bounded requests; schema validation; no access-control bypass | Safe Python Batch File Automation; REST API Integration & Smoke Tests |
| API/workflow | API docs, sanitized samples, approved credentials | Integration/workflow, mapping, runbook | Least privilege; secrets isolation; idempotency; bounded retries; webhook verification | REST API Integration & Smoke Tests |
| PDF/documents | Source PDFs/HTML/DOCX, target layout | Editable PDF/DOCX/CSV and report | Page/field counts; text integrity; visual checks; no silent OCR assumptions | PDF Text Extraction & Structured Export |
| Dashboards/BI | Approved extracts, metric definitions | Dashboard/report, metric dictionary | Reconcile totals; disclose grain/filters; test date boundaries and empty data | Sales KPI Dashboard |

## Readiness vocabulary
- **Ready with existing sample:** adjacent sample and acceptance tests exist; client environment compatibility is not guaranteed.
- **Extension needed:** core pattern exists but explicit capability must be added and verified.
- **External dependency:** client credentials, paid entitlements, live tenant/CMS or third-party acceptance required.
- **Do not accept as scoped:** unresolved safety, legal, privacy, payment or production-access risk.

See DELIVERY_READINESS_MATRIX.md for the family mapping, tool/license notes, playbooks and stop gates.

## Intake-to-delivery pipeline
1. Classify one primary service family and optional secondary tags.
2. Extract actors, inputs, output format, business rules, scale, integrations, acceptance and exclusions.
3. Resolve only unknowns that change feasibility, estimate, access or risk.
4. Run red-flag gate: credentials, payments, unauthorized scraping, bypasses, sensitive data, destructive production changes and unbounded scope.
5. Select an existing playbook; do not fork a stack by default.
6. Estimate discovery, implementation, verification and handover separately; record assumptions and change triggers.
7. Derive tests from explicit acceptance criteria; use synthetic fixtures where client data is unavailable.
8. Deliver artifact/source, runbook, evidence, limitations and handover.
9. Update demand evidence using public listing facts only. Never commit client secrets, private proposals, personal data or proprietary files.

## Commercial and operational guardrails
- Do not quote fixed price until inputs, outputs, revisions, access and acceptance are bounded.
- Very low budgets are not targets; narrow or decline uneconomic scopes.
- Hosting, monitoring, API usage, model inference and paid plugin fees are excluded unless separately priced and authorized.
- Separate implementation from live deployment and ongoing support.
- Use staging first; require backup and rollback for production changes.
- No Connects spending, proposals, contracts, purchases or payment-instrument access without explicit authorization.
- Client provisions scoped credentials through an approved secure channel; never store credentials in Git or chat artifacts.

## Open-source policy
Prefer local deterministic tools and permissive licenses. Public source code is not automatically OSI-open-source or safe to use. Verify exact upstream license, pinned version, maintenance, transitive dependencies and deployment model before adoption.

No bulk clone, package install, container pull, SaaS signup or paid service was required for this hub. Avoid PyMuPDF as a default commercial dependency without legal review (AGPL/commercial dual license). n8n and Metabase also require license review for hosting/embedding; use Python adapters or permissive alternatives when needed.

## Maintenance
- Keep snapshots immutable; add a new dated snapshot instead of silently rewriting history.
- Record URL, category, captured budget or null, deliverables and selection notes.
- Validate the JSON dataset in CI with Python standard library only.
- Update readiness only when source code, test evidence, license or external dependency state changes.


## Executable first-pass request classifier

A local, deterministic classifier is available at scripts/classify_request.py. It maps English/Arabic request phrases to one of six service families, returns family-specific intake questions, tool candidates and acceptance checks, flags explicit red-flag phrases, and refuses to guess when no category or multiple equally scored categories match. It deliberately does not produce a fixed quote or claim live environment readiness. Run:

```bash
python scripts/classify_request.py "Clean this Excel workbook and remove duplicate rows"
```

Rules are editable in config/delivery_playbooks.json. The classifier uses Python standard library only, has no network access, and is a first-pass routing aid; a human must validate scope, context, source permissions and exact license requirements.
