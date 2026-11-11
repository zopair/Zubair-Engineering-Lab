import csv
import json
import tempfile
import unittest
from pathlib import Path
import pandas as pd
from cleaner import clean_csv


class SpreadsheetCleanerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "messy.csv"
        self.output = self.root / "clean.csv"
        self.report = self.root / "report.json"
        self.source.write_text(
            "Full Name, Email Address, Signup Date, Notes\n"
            "  Ada Lovelace , ADA@EXAMPLE.COM , 11/09/2026 , hello  \n"
            "Grace Hopper, grace@example.com, 2026-09-12,   \n"
            "Ada Lovelace,ada@example.com,2026-11-09,hello\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_normalizes_headers_and_whitespace(self):
        clean_csv(self.source, self.output, self.report)
        with self.output.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(list(rows[0]), ["full_name", "email_address", "signup_date", "notes"])
        self.assertEqual(rows[0]["full_name"], "Ada Lovelace")
        self.assertEqual(rows[0]["email_address"], "ada@example.com")

    def test_normalizes_supported_dates_to_iso(self):
        clean_csv(self.source, self.output, self.report)
        with self.output.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(rows[0]["signup_date"], "2026-11-09")

    def test_reports_duplicates_without_deleting_by_default(self):
        result = clean_csv(self.source, self.output, self.report)
        with self.output.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        report = json.loads(self.report.read_text(encoding="utf-8"))
        self.assertEqual(len(rows), 3)
        self.assertEqual(result["duplicate_rows"], 1)
        self.assertEqual(report["rows_written"], 3)

    def test_deduplication_is_explicit_and_reported(self):
        result = clean_csv(self.source, self.output, self.report, dedupe=True)
        with self.output.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 2)
        self.assertEqual(result["rows_removed"], 1)

    def test_reads_and_writes_xlsx(self):
        source_xlsx = self.root / "source.xlsx"
        output_xlsx = self.root / "clean.xlsx"
        pd.DataFrame({"Full Name": [" Ada "], "Email Address": ["ADA@EXAMPLE.COM"]}).to_excel(source_xlsx, index=False)
        clean_csv(source_xlsx, output_xlsx, self.report)
        result = pd.read_excel(output_xlsx, dtype=str)
        self.assertEqual(result.loc[0, "full_name"], "Ada")
        self.assertEqual(result.loc[0, "email_address"], "ada@example.com")

    def test_rejects_duplicate_normalized_headers(self):
        self.source.write_text("Email, email\na@example.com,b@example.com\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            clean_csv(self.source, self.output, self.report)


if __name__ == "__main__":
    unittest.main(verbosity=2)