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
| 2 | Spreadsheet cleanup | Normalize headers, dates, whitespace, duplicates, missing values; validate CSV/XLSX | Python 3, pandas, openpyxl, pytest/unittest | Before/after synthetic dataset, validation report, deterministic tests, no silent data loss |
| 3 | WordPress/Elementor section repair | Fix one section's mobile layout without changing desktop appearance | WordPress, Elementor free where possible, CSS, browser/device QA | Reproducible demo, desktop/mobile screenshots, rollback instructions; no production credentials |
| 4 | Batch file automation | Rename, classify, convert or organize files safely | Python, pathlib, argparse, logging, unittest | Dry-run mode, collision handling, audit log, tests on temporary files |
| 5 | REST API integration | Connect two endpoints, map fields, handle errors and retries | Python, httpx/requests, pytest, JSON Schema | Mock/local API tests, timeout/retry policy, sanitized logs, README |
| 6 | PDF to structured data | Extract tables/text and export to CSV/XLSX | Python, pypdf, pandas, openpyxl | Synthetic sample PDF, extracted output, row-count and schema checks |
| 7 | KPI mini-dashboard | Turn a CSV into a compact business report/dashboard | Python, pandas, Plotly or HTML/CSS | Synthetic dataset, metric definitions, chart output, data-quality checks |
| 8 | Bilingual RTL landing page | Build Arabic/English opt-in or service landing page | HTML, CSS logical properties, accessibility checks | RTL/LTR layout checks, responsive states, form validation demo without real PII |

## Execution order and dependencies

- Complete samples 01 and 02 first; they need no accounts or paid infrastructure.
- Build sample 03 only in a disposable local WordPress environment; never install plugins or modify a live site without explicit client authorization.
- Samples 04–07 use local synthetic inputs and test fixtures.
- Sample 08 reuses the responsive foundation from sample 01 and adds RTL-specific acceptance tests.

## Out of scope for this starter library
Full e-commerce builds, malware cleanup on live production systems, enterprise CRM/ERP implementations, paid API integrations, large migrations, and tasks requiring client-owned proprietary data or credentials.
