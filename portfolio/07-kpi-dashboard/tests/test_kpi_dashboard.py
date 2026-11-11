import csv
import tempfile
import unittest
from pathlib import Path

from kpi_dashboard import DashboardError, build_dashboard


HEADERS = ["order_id", "order_date", "customer_id", "revenue", "status"]


class KpiDashboardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "orders.csv"
        self.output = self.root / "dashboard.html"
        self.write_rows([
            ["A-100", "2026-01-05", "C-1", "100.00", "paid"],
            ["A-101", "2026-01-18", "C-2", "50.00", "completed"],
            ["A-102", "2026-02-02", "C-1", "75.00", "paid"],
            ["A-103", "2026-02-03", "C-3", "900.00", "cancelled"],
        ])

    def tearDown(self):
        self.temp.cleanup()

    def write_rows(self, rows, headers=HEADERS):
        with self.source.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.writer(stream)
            writer.writerow(headers)
            writer.writerows(rows)

    def test_calculates_revenue_orders_aov_customers_and_months(self):
        result = build_dashboard(self.source, self.output)
        self.assertEqual(result["metrics"]["revenue"], "225.00")
        self.assertEqual(result["metrics"]["orders"], 3)
        self.assertEqual(result["metrics"]["average_order_value"], "75.00")
        self.assertEqual(result["metrics"]["customers"], 3)
        self.assertEqual(result["monthly_revenue"], [
            {"month": "2026-01", "revenue": "150.00", "orders": 2},
            {"month": "2026-02", "revenue": "75.00", "orders": 1},
        ])

    def test_excludes_cancelled_and_refunded_orders_from_kpis(self):
        result = build_dashboard(self.source, self.output)
        self.assertEqual(result["metrics"]["revenue"], "225.00")
        self.assertEqual(result["excluded_orders"], 1)

    def test_reports_duplicate_order_ids_and_counts_only_first(self):
        self.write_rows([
            ["A-100", "2026-01-05", "C-1", "100.00", "paid"],
            ["A-100", "2026-01-06", "C-2", "500.00", "paid"],
        ])
        result = build_dashboard(self.source, self.output)
        self.assertEqual(result["metrics"]["revenue"], "100.00")
        self.assertTrue(any(issue["code"] == "duplicate_order_id" for issue in result["issues"]))

    def test_reports_invalid_rows_without_counting_them(self):
        self.write_rows([
            ["A-100", "not-a-date", "C-1", "100.00", "paid"],
            ["A-101", "2026-01-07", "C-2", "-4.00", "paid"],
            ["A-102", "2026-01-08", "", "20.00", "paid"],
        ])
        result = build_dashboard(self.source, self.output)
        self.assertEqual(result["metrics"]["orders"], 0)
        codes = {issue["code"] for issue in result["issues"]}
        self.assertTrue({"invalid_order_date", "negative_revenue", "missing_customer_id"}.issubset(codes))

    def test_rejects_missing_required_columns(self):
        self.write_rows([["A-100", "2026-01-05"]], headers=["order_id", "order_date"])
        with self.assertRaises(DashboardError):
            build_dashboard(self.source, self.output)

    def test_refuses_to_overwrite_existing_dashboard(self):
        self.output.write_text("keep", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            build_dashboard(self.source, self.output)
        self.assertEqual(self.output.read_text(encoding="utf-8"), "keep")

    def test_dashboard_escapes_untrusted_customer_and_source_values(self):
        self.write_rows([["<script>", "2026-01-05", "<img src=x>", "20", "paid"]])
        build_dashboard(self.source, self.output)
        html = self.output.read_text(encoding="utf-8")
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)

    def test_empty_valid_dataset_produces_zero_metrics(self):
        self.write_rows([["A-200", "2026-01-05", "C-1", "20", "pending"]])
        result = build_dashboard(self.source, self.output)
        self.assertEqual(result["metrics"]["orders"], 0)
        self.assertEqual(result["metrics"]["revenue"], "0.00")
        self.assertIn("No qualifying transactions", self.output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
