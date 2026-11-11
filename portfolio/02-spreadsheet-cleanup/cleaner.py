"""Conservative CSV/XLSX cleanup with an auditable JSON report."""
from __future__ import annotations
import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any
import pandas as pd


def normalize_header(value: Any) -> str:
    text = str(value).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "unnamed_column"


def normalize_date(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d", "%m-%d-%Y"):
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            continue
    return value


def clean_csv(input_path: str | Path, output_path: str | Path, report_path: str | Path, *, dedupe: bool = False) -> dict[str, Any]:
    source, output, report_file = Path(input_path), Path(output_path), Path(report_path)
    if not source.is_file():
        raise FileNotFoundError(source)
    if source.suffix.lower() not in {".csv", ".xlsx", ".xlsm"}:
        raise ValueError("Input must be CSV, XLSX, or XLSM")
    if output.suffix.lower() not in {".csv", ".xlsx"}:
        raise ValueError("Output must be CSV or XLSX")
    if source.suffix.lower() == ".csv":
        frame = pd.read_csv(source, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    else:
        frame = pd.read_excel(source, dtype=str, keep_default_na=False, engine="openpyxl")
    normalized_headers = [normalize_header(column) for column in frame.columns]
    if len(set(normalized_headers)) != len(normalized_headers):
        duplicates = sorted({name for name in normalized_headers if normalized_headers.count(name) > 1})
        raise ValueError(f"Duplicate headers after normalization: {', '.join(duplicates)}")
    frame.columns = normalized_headers
    for column in frame.columns:
        frame[column] = frame[column].map(lambda value: str(value).strip())
        if "email" in column:
            frame[column] = frame[column].str.lower()
        if "date" in column:
            frame[column] = frame[column].map(normalize_date)
    input_rows = len(frame)
    duplicate_mask = frame.duplicated(keep="first")
    duplicate_rows = int(duplicate_mask.sum())
    if dedupe:
        frame = frame.loc[~duplicate_mask].copy()
    missing_by_column = {column: int((frame[column] == "").sum()) for column in frame.columns}
    output.parent.mkdir(parents=True, exist_ok=True)
    report_file.parent.mkdir(parents=True, exist_ok=True)
    if output.suffix.lower() == ".csv":
        frame.to_csv(output, index=False, encoding="utf-8")
    else:
        frame.to_excel(output, index=False, engine="openpyxl")
    result = {
        "input_file": source.name, "output_file": output.name,
        "input_rows": input_rows, "rows_written": len(frame),
        "duplicate_rows": duplicate_rows, "rows_removed": input_rows - len(frame),
        "deduplication_enabled": dedupe, "normalized_columns": list(frame.columns),
        "missing_values_by_column": missing_by_column,
        "date_policy": "Known date columns normalized to ISO YYYY-MM-DD when a documented format is recognized; otherwise preserved.",
        "data_loss_policy": "Duplicates are reported but retained unless --dedupe is explicitly supplied.",
    }
    report_file.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean a CSV/XLSX file and write a JSON audit report.")
    parser.add_argument("input", help="Source CSV/XLSX file")
    parser.add_argument("output", help="Destination CSV/XLSX file")
    parser.add_argument("--report", default="cleanup-report.json", help="JSON audit report path")
    parser.add_argument("--dedupe", action="store_true", help="Explicitly remove exact normalized duplicate rows")
    args = parser.parse_args()
    print(json.dumps(clean_csv(args.input, args.output, args.report, dedupe=args.dedupe), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()