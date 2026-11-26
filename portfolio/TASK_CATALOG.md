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
| 3 | WordPress/Elementor section repair | Fix one section's mobile layout without changing desktop appearance | WordPress, Elementor free where possible, CSS, browser/device QA | Scoped WordPress plugin, static Elementor markup preview, PHP lint and six static tests; live WordPress/Elementor browser QA remains pending |
| 4 | Batch file automation | Rename, classify, convert or organize files safely | Python standard library, pathlib, argparse, unittest | CI green (run 43037071060); six tests pass; dry-run mode, collision protection, audit log, idempotency |
| 5 | REST API integration | Connect endpoints, map payloads, handle failures and retries | Python, httpx, unittest | CI green (43045576143); 10 HTTP-boundary tests; bounded retry, no automatic POST retry, and absolute URL rejection |
| 6 | PDF text extraction | Extract searchable text and export traceable CSV/XLSX rows | Python, pypdf, pandas, openpyxl, reportlab (tests) | CI green (43043587807); 7 synthetic PDF integration tests; OCR and table reconstruction explicitly out of scope |
| 7 | Business KPI dashboard | Turn sales CSV exports into a compact decision-support report | Python standard library, CSV, HTML/CSS | CI green (43044133557); 8 tests; metric definitions, monthly trend, and data-quality review |
| 8 | Bilingual RTL landing page | Build Arabic/English opt-in or service landing page | HTML, CSS logical properties, JavaScript | CI green (43045595744); 8 tests; responsive LTR/RTL, language switching, local-only form validation with no-script controls disabled |

## Execution order and dependencies

- Samples 01, 02, 03 (code-level only), 04, 05, 06, 07, and 08 have automated test coverage. Samples 05–07 use deterministic local fixtures and require no live client API, document, or data credentials.
- Sample 04 was advanced ahead of sample 03 because it can be completed and verified without provisioning a separate CMS environment.
- Build sample 03 only in a disposable local WordPress environment; never install plugins or modify a live site without explicit client authorization.
- Samples 04–07 use local synthetic inputs and test fixtures.
- Sample 08 reuses the responsive foundation from sample 01 and adds RTL-specific acceptance tests.

## Out of scope for this starter library
Full e-commerce builds, malware cleanup on live production systems, enterprise CRM/ERP implementations, paid API integrations, large migrations, and tasks requiring client-owned proprietary data or credentials.

## Market review evidence

Market review details (posting links, budgets, client history and account observations) are maintained in the owner's private work ledger and are intentionally not published here. The catalog above reflects the demand patterns found in that review.

## Portfolio build status

- Samples 01–08 are represented on the lab's main branch; Sample 03 is a code-level plugin demonstration and still needs live CMS validation.
- Samples 01 and 02 have successful dedicated GitHub Actions runs from 2026-11-11. Sample 04 has a dedicated GitHub Actions workflow and a successful run (43037071060). Sample 05 has a successful dedicated GitHub Actions run (43043222968). Sample 06 has a successful dedicated GitHub Actions run (43043587807). Sample 07 has a successful dedicated GitHub Actions run (43044133557). Sample 08 has a successful dedicated GitHub Actions run (43044572639). The seven-card gallery and all internal links passed in run 43044660878; an eight-card refresh is now being verified.
- This proves the committed tests passed in GitHub Actions where a successful run is recorded; it does not claim that a client production system was modified.
