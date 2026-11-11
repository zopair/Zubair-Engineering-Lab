# Client-Ready Work Samples

A curated library of small-to-medium fixed-price deliverables, built as reproducible demonstrations rather than unverified claims of client work.

## Delivery rules
- Every sample has a written brief, scope boundary, source files, acceptance checklist, and automated checks where applicable.
- Use only free/open-source tooling unless a client explicitly supplies a paid license or service.
- No client credentials, private data, or copied proprietary assets are stored here.
- A sample is not represented as paid client work.
- Browser screenshots, hosted demos, and live integrations are added only after they are actually verified.

## Client-facing showcase

[Open the selected-work gallery](./index.html) · [Showcase documentation](./SHOWCASE_README.md)

The gallery presents only completed samples and links to their case studies, source files, and verified CI evidence. Static acceptance and internal-link checks pass in GitHub Actions (latest run 43044210684). The page is committed but not yet publicly hosted; browser visual QA remains outstanding.

## Catalogue

| ID | Sample | Category | Tools | Status |
|---|---|---|---|---|
| 01 | Responsive landing page repair | HTML/CSS, mobile fixes, accessibility | HTML5, CSS3, Python unittest | CI green; 7 acceptance checks pass (run 43034499497) |
| 02 | Excel/CSV cleanup and validation | Spreadsheet/data cleaning | Python, pandas, openpyxl, unittest | CI green; 6 tests pass; CSV/XLSX round-trip verified (run 43034845177) |
| 03 | WordPress/Elementor responsive section repair | CMS/front-end maintenance | WordPress, Elementor, CSS, browser QA | Queued; requires a safe demo WordPress instance |
| 04 | Python batch file automation | Scripting/automation | Python standard library, pathlib, argparse, unittest | CI green; 6 tests pass (run 43037071060) |
| 05 | REST API integration and smoke tests | API development/QA | Python, httpx, unittest | CI green; 9 acceptance tests pass (run 43043222968) |
| 06 | PDF extraction and structured export | Document automation | Python, pypdf, pandas | Queued |
| 07 | Business KPI dashboard | Data analysis/visualization | Python standard library, CSV, HTML/CSS | CI green; 8 tests pass (run 43044133557) |
| 08 | Bilingual RTL landing page | Web design/development | HTML, CSS logical properties, JavaScript | CI green; 7 acceptance tests pass (run 43044572639) |

## Sample 01
[Responsive landing page repair](./01-responsive-landing-page/README.md)

This is a standalone demonstration of removing duplicated content, restoring readable mobile typography, improving notice contrast, and adding basic accessibility safeguards.

## Sample 02
[Spreadsheet cleanup and validation](./02-spreadsheet-cleanup/README.md)

A conservative CSV/XLSX cleaner with schema normalization, explicit duplicate handling, missing-value reporting, and a JSON audit artifact. Synthetic input and output examples are included.

## Sample 04
[Safe batch file automation](./04-batch-file-automation/README.md)

A dry-run-first file renaming utility with extension filters, collision protection, idempotent prefix handling, and optional JSON audit output. Six tests pass locally and in GitHub Actions (run 43037071060).

## Sample 05
[REST API integration and smoke tests](./05-rest-api-integration/README.md)

A bounded-retry JSON API client with Bearer authentication, timeout controls, rate-limit handling, and a deliberate no-retry policy for POST. Nine deterministic HTTP-boundary tests pass in GitHub Actions (run 43043222968).

## Sample 06
[PDF text extraction and structured export](./06-pdf-extraction/README.md)

Extracts searchable PDF text into traceable page/line records and exports CSV/XLSX without overwriting existing outputs. Seven synthetic PDF integration tests pass in GitHub Actions (run 43043587807).

## Sample 07
[Business KPI dashboard](./07-kpi-dashboard/README.md)

A static, dependency-free HTML dashboard for sales CSVs, including revenue, order count, average order value, customer count, monthly breakdown, and visible data-quality issues. Eight tests pass in GitHub Actions (run 43044133557).

## Sample 08
[Bilingual RTL/LTR landing page](./08-bilingual-rtl-landing/README.md)

Responsive English/Arabic landing page with language-direction switching, CSS logical properties, accessible controls, and local-only form validation. Seven tests pass in GitHub Actions (run 43044572639).
