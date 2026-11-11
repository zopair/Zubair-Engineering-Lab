from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "research" / "upwork-demand" / "dashboard.html"


class DemandDashboardTests(unittest.TestCase):
    def test_dashboard_loads_the_versioned_dataset(self):
        page = DASHBOARD.read_text(encoding="utf-8")
        self.assertIn('fetch("./sample_jobs.json"', page)

    def test_dashboard_has_search_and_category_filters(self):
        page = DASHBOARD.read_text(encoding="utf-8")
        self.assertIn('id="search"', page)
        self.assertIn('id="category-filter"', page)

    def test_dashboard_discloses_historical_snapshot_and_links_readiness(self):
        page = DASHBOARD.read_text(encoding="utf-8")
        self.assertIn("Historical snapshot", page)
        self.assertIn("../../docs/DELIVERY_READINESS_MATRIX.md", page)


if __name__ == "__main__":
    unittest.main()
