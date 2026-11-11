from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PortfolioParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.cards = 0
        self.title_seen = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "article" and "work-card" in attrs.get("class", "").split():
            self.cards += 1

    def handle_data(self, data):
        if data.strip() == "Selected Work":
            self.title_seen = True


class PortfolioSiteTests(unittest.TestCase):
    def setUp(self):
        self.html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.parser = PortfolioParser()
        self.parser.feed(self.html)

    def test_page_has_accessible_title_and_main_landmark(self):
        self.assertIn("<title>", self.html)
        self.assertIn("<main", self.html)
        self.assertIn('lang="en"', self.html)

    def test_three_completed_work_cards_are_present(self):
        self.assertEqual(self.parser.cards, 7)

    def test_each_card_has_a_local_case_study_and_source_link(self):
        self.assertGreaterEqual(self.parser.links.count("./01-responsive-landing-page/README.md"), 1)
        self.assertGreaterEqual(self.parser.links.count("./02-spreadsheet-cleanup/README.md"), 1)
        self.assertGreaterEqual(self.parser.links.count("./04-batch-file-automation/README.md"), 1)
        self.assertIn("./04-batch-file-automation/batch_organizer.py", self.parser.links)
        self.assertIn("./05-rest-api-integration/README.md", self.parser.links)
        self.assertIn("./05-rest-api-integration/api_client.py", self.parser.links)
        self.assertIn("./06-pdf-extraction/README.md", self.parser.links)
        self.assertIn("./06-pdf-extraction/pdf_extract.py", self.parser.links)
        self.assertIn("./07-kpi-dashboard/README.md", self.parser.links)
        self.assertIn("./07-kpi-dashboard/kpi_dashboard.py", self.parser.links)
        self.assertIn("./08-bilingual-rtl-landing/README.md", self.parser.links)
        self.assertIn("./08-bilingual-rtl-landing/index.html", self.parser.links)

    def test_external_evidence_links_are_safe(self):
        self.assertIn('rel="noopener noreferrer"', self.html)

    def test_stylesheet_is_linked(self):
        self.assertIn('href="./assets/portfolio.css"', self.html)
        self.assertTrue((ROOT / "assets" / "portfolio.css").is_file())

    def test_all_internal_links_resolve(self):
        for href in self.parser.links:
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc or href.startswith("#"):
                continue
            target = (ROOT / parsed.path).resolve()
            self.assertTrue(target.is_file(), f"Broken portfolio link: {href}")


if __name__ == "__main__":
    unittest.main()
