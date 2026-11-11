# Delivery Readiness Matrix

**Date:** 2026-11-11  
**Rule:** A matching sample is evidence of a reusable pattern, not a guarantee that every client environment is supported.

| Priority | Family | Existing asset | Status | Baseline | Main gap |
|---:|---|---|---|---|---|
| P1 | Excel & data | Spreadsheet Cleanup & Validation; Sales KPI Dashboard | Ready with existing sample | Python stdlib, pandas, openpyxl; schema checks, deduplication, reconciliation, exception report | Google Sheets API only when required; test formulas/macros/pivots separately |
| P1 | WordPress & web | Responsive Landing Page Repair; Elementor Mobile Section Repair; Bilingual RTL/LTR Landing Page | Extension needed | HTML/CSS, scoped repair, responsive/RTL checks | Disposable WordPress/Elementor runtime; form delivery, plugin compatibility, staging rollback |
| P2 | API & workflow | REST API Integration & Smoke Tests | Ready for bounded REST flows | Python HTTP client, fixtures, bounded retries, idempotency tests | Provider OAuth, webhook signature verification and durable scheduling are request-dependent |
| P2 | PDF & documents | PDF Text Extraction & Structured Export | Extension needed | pypdf/pdfplumber, structured export | Fillable AcroForm authoring/update and visual regression; OCR only for scans |
| P2 | Python scraping | Safe Python Batch File Automation; REST API sample | Extension needed | Python, bounded HTTP client; Scrapy only when scale justifies it | Per-source terms/robots, rate limits, pagination/resume, schema drift and legal review |
| P3 | Dashboards & BI | Sales KPI Dashboard | Ready for CSV-driven reporting | Python/CSV/HTML, deterministic KPIs and monthly trends | Power BI/ERP/CRM connectors, scheduled refresh, row-level security and tenant validation |

## Tool selection register

| Need | Preferred starting point | License/risk | Fallback |
|---|---|---|---|
| Tabular transforms | [pandas](https://github.com/pandas-dev/pandas) ([license](https://github.com/pandas-dev/pandas/blob/main/LICENSE)); [openpyxl](https://github.com/ericgazoni/openpyxl) ([license](https://github.com/ericgazoni/openpyxl/blob/master/LICENCE.rst)) | BSD-3-Clause / MIT; upstream license files inspected 2026-11-11; verify pinned release and transitive licenses | Python csv for small CSV-only jobs |
| Browser QA | [Playwright Python](https://github.com/microsoft/playwright-python) ([license](https://github.com/microsoft/playwright-python/blob/main/LICENSE)) | Apache-2.0; upstream license inspected 2026-11-11; browser binaries add storage/install cost | Static checks and manual browser QA |
| Scraping | [Scrapy](https://github.com/scrapy/scrapy) ([license](https://github.com/scrapy/scrapy/blob/master/LICENSE)) | BSD-3-Clause; upstream license inspected 2026-11-11; license does not authorize target data collection | Small bounded Python HTTP client |
| PDF extraction | [pypdf](https://github.com/py-pdf/pypdf) ([license](https://github.com/py-pdf/pypdf/blob/main/LICENSE)); [pdfplumber](https://github.com/jsvine/pdfplumber) ([license](https://github.com/jsvine/pdfplumber/blob/stable/LICENSE.txt)) | BSD-3-Clause / MIT; upstream license files inspected 2026-11-11; test fonts/forms/document-specific behavior | Existing text-only pipeline when extraction quality is insufficient |
| PDF editing/rendering | [PyMuPDF](https://github.com/pymupdf/PyMuPDF) ([COPYING](https://github.com/pymupdf/PyMuPDF/blob/main/COPYING)) | AGPL-3.0 source license with commercial licensing path; upstream license inspected 2026-11-11; legal review before commercial distribution | pypdf/pdfplumber/ReportLab when sufficient |
| OCR | [Tesseract](https://github.com/tesseract-ocr/tesseract) | Apache-2.0; confirm exact release/license and language-data terms; OCR error rate needs acceptance criteria | Manual exception queue |
| Workflow | Python + existing REST sample; optional [n8n](https://github.com/n8n-io/n8n) ([license](https://github.com/n8n-io/n8n/blob/master/LICENSE.md)) | Sustainable Use License for covered source; not OSI-approved open source; hosting/embedding requires review | Python worker/webhook adapter |
| Dashboard | Existing Python/HTML KPI sample; optional [Streamlit](https://github.com/streamlit/streamlit) ([license](https://github.com/streamlit/streamlit/blob/develop/LICENSE)) | Apache-2.0; upstream license inspected 2026-11-11 | Static HTML/CSV report |
| BI platform | [Metabase](https://github.com/metabase/metabase) ([license](https://github.com/metabase/metabase/blob/master/LICENSE.txt)) | AGPL-3.0/commercial editions; upstream license inspected 2026-11-11; review hosting, embedding and distribution | Client's existing BI environment |
| WordPress QA | WordPress + client-approved Elementor tier; optional axe-core | Theme/plugin licenses and access vary; no paid plugin assumed | Static reproduction + disposable staging |

## Universal playbook
1. Intake only required files, sanitized samples, output, rules, volume, versions and access owner.
2. Bound scope, exclusions, assumptions, revisions, acceptance and change triggers.
3. Use staging/copies; preserve originals; keep secrets out of Git/logs; least privilege.
4. Reuse existing sample patterns; pin dependencies only when justified.
5. Run focused tests, edge cases, reconciliation and owning repo's full suite.
6. Handover artifacts, source, run instructions, evidence, limitations and rollback.

## Red-flag gate — stop, reject or re-scope
- Bypass CAPTCHA, MFA, paywalls, rate limits, access controls, bot protections or platform terms.
- Collect private, restricted, personal or sensitive data without documented authorization and lawful basis.
- Handle deposits, withdrawals, card data, wallets, payment credentials or real-money transfers.
- Client sends passwords, API keys or session cookies in chat/email/source files.
- Unbounded production access, destructive bulk edits, database/volume deletion or no rollback.
- Malware, credential harvesting, spam, deceptive reviews, impersonation or evasion.
- Regulated medical/legal/financial decisions requiring licensed judgment.
- Vague acceptance, unlimited revisions, uneconomic budget or unpaid discovery disguised as fixed price.
- Dependency license incompatible with commercial distribution or hosted/embedded use.

## Family acceptance checks

### Excel & data
Preserve raw input; reconcile row counts; explain rejected rows; define duplicate/blank/type/date/currency/formula rules; no silent coercion or destructive overwrite; deterministic rerun.

### WordPress & web
Record theme/plugin versions; use staging; test mobile/tablet/desktop and overflow; verify form success/failure safely; inspect accessibility and console/network; agree backup/rollback.

### API & workflow
Least-privilege auth; credentials outside Git; schema/error mapping; timeouts, bounded retries and idempotency; verify webhook signatures/replay protection; never retry non-idempotent writes without an idempotency design.

### PDF & documents
Preserve source; record page/field counts; check fonts, RTL, page breaks, tab order and print; surface OCR uncertainty; test target viewers and representative pages.

### Scraping & automation
Review authorization/terms/robots; bound rate/time/pagination; test checkpoint/resume/deduplication; handle schema drift and partial responses; no access-control evasion.

### Dashboards & BI
Document metric formula/grain/filter/source; reconcile totals; test dates, missing data, duplicates and outliers; disclose refresh, access and licensing; do not claim live integration until verified.
