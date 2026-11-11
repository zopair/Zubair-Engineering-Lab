"""Extract searchable PDF text into auditable CSV/XLSX line records.

This utility does not perform OCR and does not infer table structure.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

import pandas as pd
from pypdf import PdfReader
from pypdf.errors import PdfReadError


COLUMNS = ["page_number", "line_number", "text"]


class PdfExtractionError(RuntimeError):
    """Raised when a PDF cannot be safely read or parsed."""


def extract_pdf_lines(pdf_path: str | Path) -> list[dict[str, Any]]:
    """Extract non-empty text lines, retaining page and within-page line numbers."""
    source = Path(pdf_path).expanduser()
    if not source.is_file():
        raise FileNotFoundError(source)

    try:
        reader = PdfReader(str(source), strict=False)
        if reader.is_encrypted:
            raise PdfExtractionError("Encrypted PDFs are not supported by this sample")
        rows: list[dict[str, Any]] = []
        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            for line_number, line in enumerate(text.splitlines(), start=1):
                normalized = " ".join(line.split())
                if normalized:
                    rows.append({
                        "page_number": page_number,
                        "line_number": line_number,
                        "text": normalized,
                    })
        return rows
    except PdfExtractionError:
        raise
    except (PdfReadError, OSError, ValueError) as exc:
        raise PdfExtractionError(f"Unable to read PDF: {type(exc).__name__}") from exc


def export_records(
    records: list[dict[str, Any]],
    output_path: str | Path,
) -> dict[str, Any]:
    """Write line records to CSV or XLSX without overwriting an existing file."""
    output = Path(output_path).expanduser()
    suffix = output.suffix.lower()
    if suffix not in {".csv", ".xlsx"}:
        raise ValueError("Output format must be .csv or .xlsx")
    if not output.parent.exists() or not output.parent.is_dir():
        raise NotADirectoryError(output.parent)

    frame = pd.DataFrame.from_records(records, columns=COLUMNS)
    # Exclusive creation prevents clobbering a file created between the check
    # and write. On failure, remove the partial output.
    try:
        descriptor = os.open(output, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    except FileExistsError:
        raise
    else:
        os.close(descriptor)

    try:
        if suffix == ".csv":
            frame.to_csv(output, index=False, encoding="utf-8")
        else:
            frame.to_excel(output, index=False, engine="openpyxl")
    except Exception:
        output.unlink(missing_ok=True)
        raise

    return {
        "output": str(output),
        "format": suffix.lstrip("."),
        "rows": len(frame),
        "columns": COLUMNS,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract searchable PDF text lines to CSV or XLSX."
    )
    parser.add_argument("input_pdf", type=Path)
    parser.add_argument("output_file", type=Path, help="Destination .csv or .xlsx")
    args = parser.parse_args()

    try:
        records = extract_pdf_lines(args.input_pdf)
        summary = export_records(records, args.output_file)
    except (OSError, ValueError, PdfExtractionError) as exc:
        parser.error(str(exc))

    print(pd.Series(summary).to_json(indent=2, force_ascii=False))
    if not records:
        print("Warning: no searchable text lines were found; OCR may be required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
