# Portfolio Sample 02 — Spreadsheet Cleanup & Validation

**Category:** CSV/XLSX cleanup · Data quality · Repeatable reporting  
**Status:** Implemented with automated tests.

## Client-style brief
A client supplies a messy contact or operations spreadsheet and needs consistent headers, trimmed values, normalized emails/dates, duplicate visibility, and a clear audit report without accidental data loss.

## Behavior
- Accepts CSV, XLSX, or XLSM input; writes CSV or XLSX output.
- Normalizes column names to lowercase snake_case and rejects collisions rather than silently overwriting columns.
- Trims whitespace, lowercases values in email columns, and normalizes recognizable date strings to ISO YYYY-MM-DD.
- Reports missing-value counts and exact duplicate rows.
- Preserves duplicate rows by default. Deletion is opt-in via --dedupe and is recorded in the report.
- Keeps unrecognized date strings unchanged; ambiguous dates use parser order: ISO year-first, then US month-first, then day-first. Confirm this assumption with the client before bulk normalization.

## Run
```bash
python -m pip install -r requirements.txt
python cleaner.py examples/messy_contacts.csv output/clean_contacts.csv --report output/audit.json
python cleaner.py examples/messy_contacts.csv output/clean_contacts.csv --report output/audit.json --dedupe
python -m unittest discover -s tests -v
```

## Tools
Python 3, pandas, openpyxl, Python standard library (argparse, json, unittest). All are free/open source.

## Acceptance
- [x] Header normalization and collision protection.
- [x] Whitespace and email normalization.
- [x] Recognized date normalization.
- [x] Duplicate reporting without implicit deletion.
- [x] Explicit deduplication mode and row-removal accounting.
- [x] JSON audit report.
- [x] CSV/XLSX input and output support.

## Data safety
The example is synthetic. No real personal data is included. Production use should operate on a copy, retain the original file, and confirm date-format assumptions with the client before bulk normalization.