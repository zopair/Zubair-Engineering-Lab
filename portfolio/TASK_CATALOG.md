# Work-Sample Task Catalog

Scope derived from a review of current and representative Upwork fixed-price postings for entry-level to intermediate work. This is a portfolio build plan, not a promise that every listed tool or paid service is available on every client engagement.

## Selection principles
1. A clearly bounded deliverable that can be demonstrated independently.
2. Repeat demand across small website, data, automation, API, and document tasks.
3. Zero-cost local toolchain wherever practical.
4. Acceptance criteria that can be tested without client credentials.
5. No sample may claim to have modified a real client system unless that work actually occurred.

## Prioritized tasks

| Priority | Sample | Typical client request | Required tools | Evidence / acceptance |
|---:|---|---|---|---|
| 1 | Responsive landing page repair | Fix mobile font scaling, duplicated HTML, spacing and contrast | HTML5, CSS3, Python unittest; optional Playwright when available | Responsive breakpoints, one copy block, contrast tokens, no overflow, automated checks |
| 2 | Spreadsheet cleanup | Normalize headers, dates, whitespace, duplicates, missing values; validate CSV/XLSX | Python 3, pandas, openpyxl, unittest | Before/after synthetic dataset, JSON validation report, six deterministic tests, no silent data loss |
| 3 | WordPress/Elementor section repair | Fix one section's mobile layout without changing desktop appearance | WordPress, Elementor free where possible, CSS, browser/device QA | Reproducible demo, desktop/mobile screenshots, rollback instructions; no production credentials (blocked pending isolated demo environment) |
| 4 | Batch file automation | Rename, classify, convert or organize files safely | Python standard library, pathlib, argparse, unittest | Implemented; dry-run mode, collision protection, audit log, idempotency; six local tests pass; CI pending |
| 5 | REST API integration | Connect two endpoints, map fields, handle errors and retries | Python, httpx/requests, pytest, JSON Schema | Mock/local API tests, timeout/retry policy, sanitized logs, README |
| 6 | PDF to structured data | Extract tables/text and export to CSV/XLSX | Python, pypdf, pandas, openpyxl | Synthetic sample PDF, extracted output, row-count and schema checks |
| 7 | KPI mini-dashboard | Turn a CSV into a compact business report/dashboard | Python, pandas, Plotly or HTML/CSS | Synthetic dataset, metric definitions, chart output, data-quality checks |
| 8 | Bilingual RTL landing page | Build Arabic/English opt-in or service landing page | HTML, CSS logical properties, accessibility checks | RTL/LTR layout checks, responsive states, form validation demo without real PII |

## Execution order and dependencies

- Samples 01, 02, and 04 are implemented and tested locally; they need no accounts or paid infrastructure.
- Sample 04 was advanced ahead of sample 03 because it can be completed and verified without provisioning a separate CMS environment.
- Build sample 03 only in a disposable local WordPress environment; never install plugins or modify a live site without explicit client authorization.
- Samples 04–07 use local synthetic inputs and test fixtures.
- Sample 08 reuses the responsive foundation from sample 01 and adds RTL-specific acceptance tests.

## Out of scope for this starter library
Full e-commerce builds, malware cleanup on live production systems, enterprise CRM/ERP implementations, paid API integrations, large migrations, and tasks requiring client-owned proprietary data or credentials.


## Market review evidence — 2026-11-11

Representative live postings reviewed through the connected Upwork account. These validate demand patterns; none has been applied to.

| Posting | Budget / competition | Client evidence | Decision |
|---|---|---|---|
| [HTML/CSS mobile landing-page repair](https://www.upwork.com/jobs/~022120287337497903574) (2120287337497903574) | $30 fixed; 50+ proposals; 14 Connects | Verified; 4.81/5 from 30 reviews; $16,973 spent; 64% hire rate | Strong scope match for sample 01, but high competition. |
| [Website redesign and booking](https://www.upwork.com/jobs/~022120463290398324808) (2120463290398324808) | $300 fixed; 50+ proposals; 16 Connects | Verified; one prior hire, no reviews, $153 spent; 50% hire rate | Medium scope but client history is too thin for priority. |
| [UiPath-to-Python converter testing](https://www.upwork.com/jobs/~022120480982769400471) (2120480982769400471) | $45 fixed; fewer than 5 proposals; 11 Connects | Verified; 5/5 from 5 reviews; $1,303 spent; 86% hire rate | Do not pursue without three real, shareable production UiPath robots and 1+ year hands-on UiPath experience. |
| [WordPress/Elementor troubleshooting](https://www.upwork.com/jobs/~022112551688104778953) (2112551688104778953) | $5 fixed; 10–15 proposals; 11 Connects | Verified; 4.99/5 from 1,150 reviews; $13,080 spent; 97% hire rate | Client is established, but the $5 budget is uneconomic. |
| [Egypt-based Vodafone Cash testing](https://www.upwork.com/jobs/~022119777220363909076) (2119777220363909076) | $15 fixed; 20–50 proposals | Verified; 4.96/5 from 430 reviews; $2.0M spent; 719 hires | Do not prioritize: testing deposits/withdrawals can involve real-money exposure and payment-account access. |
| [Webflow website management](https://www.upwork.com/jobs/~022120099831429664591) (2120099831429664591) | $300 fixed; 20–50 proposals; 11 Connects | Verified, but no hire/review/spend history returned | Do not prioritize until scope and client track record are clearer. |

**Account observation:** the job-detail responses showed 92 Connects at the time of review. No Connects were spent and no proposals were submitted. Recheck the balance before any future application.

## Portfolio build status

- Samples 01, 02, and 04 are implemented on the lab's main branch.
- Samples 01 and 02 have successful dedicated GitHub Actions runs from 2026-11-11. Sample 04 has a dedicated workflow; its run is pending verification.
- This proves the committed tests passed in GitHub Actions where a successful run is recorded; it does not claim that a client production system was modified.
