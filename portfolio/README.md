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

The gallery presents completed work samples and links to their case studies, source files, and CI evidence. The Elementor sample is explicitly labelled as static CI verified with live CMS QA pending. Static acceptance and internal-link checks pass in GitHub Actions (latest eight-card run 43045733840). The page is committed but not yet publicly hosted; browser visual QA remains outstanding.

## Catalogue

| ID | Sample | Category | Tools | Status |
|---|---|---|---|---|
| 01 | Responsive landing page repair | HTML/CSS, mobile fixes, accessibility | HTML5, CSS3, Python unittest | CI green (run 43034499497); 9 tests pass after 2026-11-26 narrow-viewport fix |
| 02 | Excel/CSV cleanup and validation | Spreadsheet/data cleaning | Python, pandas, openpyxl, unittest | CI green; 6 tests pass; CSV/XLSX round-trip verified (run 43034845177) |
| 03 | WordPress/Elementor responsive section repair | CMS/front-end maintenance | WordPress plugin API, PHP, CSS | Static CI green (run 43045096680); 6 tests and PHP lint pass; live CMS/browser QA pending |
| 04 | Python batch file automation | Scripting/automation | Python standard library, pathlib, argparse, unittest | CI green; 6 tests pass (run 43037071060) |
| 05 | REST API integration and smoke tests | API development/QA | Python, httpx, unittest | CI green; 10 acceptance tests pass (run 43045576143) |
| 06 | PDF extraction and structured export | Document automation | Python, pypdf, pandas, openpyxl | CI green; 7 PDF integration tests pass (run 43043587807) |
| 07 | Business KPI dashboard | Data analysis/visualization | Python standard library, CSV, HTML/CSS | CI green; 8 tests pass (run 43044133557) |
| 08 | Bilingual RTL landing page | Web design/development | HTML, CSS logical properties, JavaScript | CI green (run 43045595744); 7 acceptance tests pass (count corrected 2026-11-26 after local rerun) |


## Independent verification - 2026-11-26

Each sample was rerun locally from a fresh clone of this repository on 2026-11-26 (per-sample command: `python3 -m unittest discover -s tests` inside the sample folder) and the recorded CI run IDs were rechecked against GitHub Actions. Classification: proven = tests rerun green now; partially proven = static checks green, live-environment validation pending; demonstration = synthetic showcase, not client work.

| Sample | Provenance | Tests rerun 2026-11-26 | Recorded CI (verified links) | Status | Remaining gap |
|---|---|---|---|---|---|
| 01 Responsive landing page | Synthetic demo | 9/9 pass (2 new regression tests) | [43034499497](https://github.com/zopair/Zubair-Engineering-Lab/actions/runs/43034499497) (7 checks, pre-fix) and post-fix branch run [45743635917](https://github.com/zopair/Zubair-Engineering-Lab/actions/runs/45743635917), both success | Proven (static + browser check at 320/768px) | None blocking; 320px nav clipping and 768px orbit overflow fixed |
| 02 Spreadsheet cleanup | Synthetic demo | 6/6 pass | [43034845177](https://github.com/zopair/Zubair-Engineering-Lab/actions/runs/43034845177) success | Proven | None for demonstration scope |
| 03 Elementor repair | Synthetic demo (code-level) | 6/6 static tests pass | [43045096680](https://github.com/zopair/Zubair-Engineering-Lab/actions/runs/43045096680) success (static + PHP lint) | Partially proven | Live WordPress/Elementor browser QA still pending |
| 04 Batch file automation | Synthetic demo | 6/6 pass | [43037071060](https://github.com/zopair/Zubair-Engineering-Lab/actions/runs/43037071060) success | Proven | None for demonstration scope |
| 05 REST API integration | Synthetic demo (no live API) | 10/10 pass | [43045576143](https://github.com/zopair/Zubair-Engineering-Lab/actions/runs/43045576143) success; [43045557199](https://github.com/zopair/Zubair-Engineering-Lab/actions/runs/43045557199) success | Proven against HTTP-boundary fixtures | Real client API integration untested by design |
| 06 PDF extraction | Synthetic demo | 7/7 pass | [43043587807](https://github.com/zopair/Zubair-Engineering-Lab/actions/runs/43043587807) success | Proven for digital-text PDFs | OCR and table reconstruction explicitly out of scope |
| 07 KPI dashboard | Synthetic demo | 8/8 pass | [43044133557](https://github.com/zopair/Zubair-Engineering-Lab/actions/runs/43044133557) success | Proven | None for demonstration scope |
| 08 Bilingual RTL landing | Synthetic demo | 7/7 pass (count corrected from 8) | [43045595744](https://github.com/zopair/Zubair-Engineering-Lab/actions/runs/43045595744) success | Proven | None blocking; browser QA at 320-1280px verified |

Gallery and showcase checks: [43044660878](https://github.com/zopair/Zubair-Engineering-Lab/actions/runs/43044660878) (seven-card gallery) and [43045733840](https://github.com/zopair/Zubair-Engineering-Lab/actions/runs/43045733840) (eight-card refresh) both verified successful on 2026-11-26. None of the eight samples is represented as paid client work.

## Sample 01
[Responsive landing page repair](./01-responsive-landing-page/README.md)

This is a standalone demonstration of removing duplicated content, restoring readable mobile typography, improving notice contrast, and adding basic accessibility safeguards. A 2026-11-26 review fixed narrow-viewport header wrapping (320px nav clipping) and capped decorative orbit size at 768px; nine tests now pass locally, including new regression checks for both fixes.

## Sample 02
[Spreadsheet cleanup and validation](./02-spreadsheet-cleanup/README.md)

A conservative CSV/XLSX cleaner with schema normalization, explicit duplicate handling, missing-value reporting, and a JSON audit artifact. Synthetic input and output examples are included.

## Sample 03
[Elementor mobile section repair](./03-elementor-responsive-repair/README.md)

A WordPress plugin with a section-scoped Elementor CSS fix and a static markup preview. PHP syntax and six static tests pass in GitHub Actions (run 43045096680); live WordPress/Elementor browser QA is not yet claimed.

## Sample 04
[Safe batch file automation](./04-batch-file-automation/README.md)

A dry-run-first file renaming utility with extension filters, collision protection, idempotent prefix handling, and optional JSON audit output. Six tests pass locally and in GitHub Actions (run 43037071060).

## Sample 05
[REST API integration and smoke tests](./05-rest-api-integration/README.md)

A bounded-retry JSON API client with Bearer authentication, timeout controls, rate-limit handling, and a deliberate no-retry policy for POST. Ten deterministic HTTP-boundary tests pass in GitHub Actions (run 43045557199).

## Sample 06
[PDF text extraction and structured export](./06-pdf-extraction/README.md)

Extracts searchable PDF text into traceable page/line records and exports CSV/XLSX without overwriting existing outputs. Seven synthetic PDF integration tests pass in GitHub Actions (run 43043587807).

## Sample 07
[Business KPI dashboard](./07-kpi-dashboard/README.md)

A static, dependency-free HTML dashboard for sales CSVs, including revenue, order count, average order value, customer count, monthly breakdown, and visible data-quality issues. Eight tests pass in GitHub Actions (run 43044133557).

## Sample 08
[Bilingual RTL/LTR landing page](./08-bilingual-rtl-landing/README.md)

Responsive English/Arabic landing page with language-direction switching, CSS logical properties, accessible controls, and local-only form validation. Seven tests pass in GitHub Actions and in a 2026-11-26 local rerun (the earlier count of eight was corrected).
