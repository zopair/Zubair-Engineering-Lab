# Sample 06 — PDF Text Extraction & Structured Export

A repeatable pipeline for extracting searchable PDF text into auditable CSV or Excel records.

## Business problem

Clients often receive invoices, statements, forms, and reports as PDFs but need the text in a spreadsheet for review, reconciliation, or downstream processing.

## What this delivers

- Extracts searchable text page by page.
- Produces one record per non-empty text line.
- Preserves page number and original line number for traceability.
- Exports to CSV or XLSX with a stable schema.
- Refuses to overwrite an existing output file.
- Reports empty-text PDFs so users can identify when OCR is needed.
- Handles malformed and encrypted PDFs with explicit errors.

## Quick start

Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```bash
python pdf_extract.py ./input.pdf ./extracted-lines.xlsx
```

CSV is also supported:

```bash
python pdf_extract.py ./input.pdf ./extracted-lines.csv
```

## Output schema

| Field | Meaning |
|---|---|
| `page_number` | 1-based PDF page number |
| `line_number` | 1-based line position within the extracted page text |
| `text` | Normalized, non-empty extracted line |

## Reliability and limitations

- This sample extracts the PDF's embedded text layer. It does **not** run OCR on scanned/image-only documents.
- It does not claim semantic table reconstruction; each non-empty text line is exported as a row.
- Complex multi-column layouts, unusual reading order, handwriting, and malformed font encodings may need document-specific handling.
- Encrypted PDFs are rejected rather than prompting for or storing passwords.
- Existing destination files are never overwritten.
- Test PDFs are generated from synthetic content; no customer documents are included.

## Acceptance evidence

Run:

```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Seven tests cover page/line traceability, CSV output, XLSX round-trip, overwrite protection, unsupported formats, malformed PDFs, and missing files. ReportLab is used only to generate synthetic test PDFs.

The dedicated GitHub Actions workflow runs the suite on Python 3.12.

## Deliverables

- `pdf_extract.py` — reusable extraction functions and CLI.
- `tests/test_pdf_extract.py` — isolated synthetic PDF integration tests.
- `requirements.txt` — runtime and test dependencies.
- `.github/workflows/portfolio-sample-06.yml` — automated acceptance workflow.

**Work-sample status:** implementation committed; CI verification pending.
