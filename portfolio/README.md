# Client-Ready Work Samples

A curated library of small-to-medium fixed-price deliverables, built as reproducible demonstrations rather than unverified claims of client work.

## Delivery rules
- Every sample has a written brief, scope boundary, source files, acceptance checklist, and automated checks where applicable.
- Use only free/open-source tooling unless a client explicitly supplies a paid license or service.
- No client credentials, private data, or copied proprietary assets are stored here.
- A sample is not represented as paid client work.
- Browser screenshots, hosted demos, and live integrations are added only after they are actually verified.

## Catalogue

| ID | Sample | Category | Tools | Status |
|---|---|---|---|---|
| 01 | Responsive landing page repair | HTML/CSS, mobile fixes, accessibility | HTML5, CSS3, Python unittest | CI green; 7 acceptance checks pass (run 43034499497) |
| 02 | Excel/CSV cleanup and validation | Spreadsheet/data cleaning | Python, pandas, openpyxl, unittest | CI green; 6 tests pass; CSV/XLSX round-trip verified (run 43034845177) |
| 03 | WordPress/Elementor responsive section repair | CMS/front-end maintenance | WordPress, Elementor, CSS, browser QA | Queued; requires a safe demo WordPress instance |
| 04 | Python batch file automation | Scripting/automation | Python standard library, pathlib, argparse, unittest | Implemented; 6 local tests pass; CI verification pending |
| 05 | REST API integration and smoke tests | API development/QA | Python, requests/httpx, pytest | Queued |
| 06 | PDF extraction and structured export | Document automation | Python, pypdf, pandas | Queued |
| 07 | Business KPI dashboard | Data analysis/visualization | Python, pandas, Plotly or static HTML | Queued |
| 08 | Bilingual RTL landing page | Web design/development | HTML, CSS logical properties, RTL QA | Queued |

## Sample 01
[Responsive landing page repair](./01-responsive-landing-page/README.md)

This is a standalone demonstration of removing duplicated content, restoring readable mobile typography, improving notice contrast, and adding basic accessibility safeguards.

## Sample 02
[Spreadsheet cleanup and validation](./02-spreadsheet-cleanup/README.md)

A conservative CSV/XLSX cleaner with schema normalization, explicit duplicate handling, missing-value reporting, and a JSON audit artifact. Synthetic input and output examples are included.

## Sample 04
[Safe batch file automation](./04-batch-file-automation/README.md)

A dry-run-first file renaming utility with extension filters, collision protection, idempotent prefix handling, and optional JSON audit output. Six local tests pass; the dedicated CI run is pending.
