# Sample 04 — Safe Batch File Automation

A client-oriented demonstration of repeatable file renaming with a safety-first execution model.

## Business problem

Renaming batches of documents or media by hand is slow and error-prone. A bulk operation must also avoid overwriting existing files and provide a traceable record of what changed.

## What this delivers

- Deterministic filename planning with configurable prefix, suffix, and extension filters.
- **Dry-run by default**: preview the proposed changes without modifying files.
- Explicit execution only with `--apply`.
- Existing destinations are skipped; they are never overwritten.
- Files already carrying the selected prefix are skipped to make repeat runs idempotent.
- Directories and symbolic links are excluded.
- Optional JSON audit report with per-file outcomes.
- Clear counts for planned, applied, skipped, and failed operations.

## Quick start

Requires Python 3.10+; no third-party packages are required.

Preview all regular files in a folder:

```bash
python batch_organizer.py ./incoming --prefix "processed_"
```

Preview only PDF and DOCX files and save an audit report:

```bash
python batch_organizer.py ./incoming --prefix "reviewed_" --ext .pdf --ext .docx --audit ./reports/preview.json
```

Apply the operation after reviewing the dry-run output:

```bash
python batch_organizer.py ./incoming --prefix "reviewed_" --ext .pdf --ext .docx --apply --audit ./reports/applied.json
```

## Safety and operating boundaries

- Scans one directory level only; it does not recurse into subdirectories.
- Does not delete or overwrite destination files.
- Uses exclusive file creation before removing the original name, so a destination collision at execution time is safely rejected.
- The source and destination must be on the same filesystem and support hard links. Unsupported filesystems produce a recorded failure rather than silently falling back to an overwrite-prone operation.
- Review the preview and keep a backup before applying bulk changes to important data.
- This sample is a demonstration; it has not been run against a client filesystem.

## Acceptance evidence

Run locally:

```bash
python -m unittest discover -s tests -v
```

Six deterministic tests cover dry-run behavior, extension filtering, destination collisions, idempotency, audit output, invalid directories, and exclusion of directories/symlinks. The repository CI workflow runs the same test suite on Python 3.12.

## Deliverables

- `batch_organizer.py` — CLI and reusable planning/execution functions.
- `tests/test_batch_organizer.py` — isolated temporary-directory tests.
- `.github/workflows/portfolio-sample-04.yml` — automated acceptance workflow.

**Work-sample status:** implemented; local tests pass. CI verification is pending until the workflow run completes.
