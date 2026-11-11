import csv
import tempfile
import unittest
from pathlib import Path

from reportlab.pdfgen import canvas

from pdf_extract import PdfExtractionError, extract_pdf_lines, export_records


class PdfExtractionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.pdf = self.root / "sample.pdf"
        doc = canvas.Canvas(str(self.pdf))
        doc.drawString(72, 760, "Invoice: INV-204")
        doc.drawString(72, 740, "Customer: Example Trading")
        doc.showPage()
        doc.drawString(72, 760, "Total: 1250.00")
        doc.save()

    def tearDown(self):
        self.temp.cleanup()

    def test_extracts_nonempty_lines_with_page_and_line_numbers(self):
        rows = extract_pdf_lines(self.pdf)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0], {
            "page_number": 1, "line_number": 1, "text": "Invoice: INV-204"
        })
        self.assertEqual(rows[2]["page_number"], 2)
        self.assertEqual(rows[2]["text"], "Total: 1250.00")

    def test_exports_csv_with_stable_columns(self):
        rows = extract_pdf_lines(self.pdf)
        output = self.root / "result.csv"
        summary = export_records(rows, output)
        self.assertEqual(summary["rows"], 3)
        with output.open(newline="", encoding="utf-8") as stream:
            parsed = list(csv.DictReader(stream))
        self.assertEqual(list(parsed[0]), ["page_number", "line_number", "text"])
        self.assertEqual(parsed[0]["text"], "Invoice: INV-204")

    def test_exports_xlsx_round_trip(self):
        rows = extract_pdf_lines(self.pdf)
        output = self.root / "result.xlsx"
        summary = export_records(rows, output)
        self.assertEqual(summary["rows"], 3)
        import pandas as pd
        frame = pd.read_excel(output)
        self.assertEqual(frame.shape, (3, 3))
        self.assertEqual(frame.iloc[2]["text"], "Total: 1250.00")

    def test_refuses_to_overwrite_existing_output(self):
        output = self.root / "result.csv"
        output.write_text("keep", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            export_records(extract_pdf_lines(self.pdf), output)
        self.assertEqual(output.read_text(encoding="utf-8"), "keep")

    def test_rejects_unsupported_export_format(self):
        with self.assertRaises(ValueError):
            export_records([], self.root / "result.json")

    def test_rejects_invalid_pdf(self):
        invalid = self.root / "invalid.pdf"
        invalid.write_text("not a PDF", encoding="utf-8")
        with self.assertRaises(PdfExtractionError):
            extract_pdf_lines(invalid)

    def test_rejects_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            extract_pdf_lines(self.root / "missing.pdf")


if __name__ == "__main__":
    unittest.main()
