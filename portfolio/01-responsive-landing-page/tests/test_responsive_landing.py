from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")
CSS = (ROOT / "styles.css").read_text(encoding="utf-8")


class ResponsiveLandingPageTests(unittest.TestCase):
    def test_document_has_mobile_viewport(self):
        self.assertRegex(HTML, r'<meta[^>]+name=["\']viewport["\'][^>]+content=["\']width=device-width')

    def test_hero_has_one_description_not_duplicated_fragments(self):
        self.assertEqual(HTML.count('class="hero__description"'), 1)

    def test_hero_description_is_readable_on_small_screens(self):
        self.assertRegex(CSS, r'@media\s*\(max-width:\s*\d+px\)')
        self.assertRegex(CSS, r'\.hero__description\s*\{[^}]*font-size:\s*(?:1[6-9]|2\d)px')

    def test_construction_notice_uses_high_contrast_tokens(self):
        self.assertRegex(CSS, r'--notice-bg:\s*#[0-9a-fA-F]{6}')
        self.assertRegex(CSS, r'--notice-text:\s*#[0-9a-fA-F]{6}')

    def test_layout_avoids_horizontal_overflow(self):
        self.assertIn('max-width: 100%', CSS)
        self.assertIn('overflow-x: hidden', CSS)

    def test_page_has_accessible_landmarks_and_skip_link(self):
        self.assertIn('<main', HTML)
        self.assertIn('<header', HTML)
        self.assertIn('href="#main-content"', HTML)

    def test_no_inline_styles(self):
        self.assertNotRegex(HTML, r'\sstyle=')


if __name__ == "__main__":
    unittest.main(verbosity=2)