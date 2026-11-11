import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class LandingPageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.languages = set()
        self.labels = []
        self.forms = 0
        self.email_inputs = 0
        self.main_landmarks = 0
        self.external_assets = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "section" and attrs.get("data-language"):
            self.languages.add(attrs["data-language"])
        if tag == "label":
            self.labels.append(attrs.get("for"))
        if tag == "form":
            self.forms += 1
        if tag == "input" and attrs.get("type") == "email":
            self.email_inputs += 1
        if tag == "main":
            self.main_landmarks += 1
        if tag in {"script", "link"}:
            url = attrs.get("src") or attrs.get("href", "")
            if url.startswith("http"):
                self.external_assets.append(url)


class BilingualLandingTests(unittest.TestCase):
    def setUp(self):
        self.html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.css = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.js = (ROOT / "app.js").read_text(encoding="utf-8")
        self.parser = LandingPageParser()
        self.parser.feed(self.html)

    def test_both_language_variants_are_present(self):
        self.assertEqual(self.parser.languages, {"en", "ar"})
        self.assertIn('lang="ar"', self.html)
        self.assertIn('dir="rtl"', self.html)

    def test_semantic_landmarks_and_form_labels_exist(self):
        self.assertEqual(self.parser.main_landmarks, 1)
        self.assertGreaterEqual(self.parser.forms, 2)
        self.assertGreaterEqual(self.parser.email_inputs, 2)
        self.assertTrue(all(label for label in self.parser.labels))

    def test_language_toggle_updates_language_and_direction(self):
        self.assertIn("root.lang", self.js)
        self.assertIn('root.dir', self.js)
        self.assertIn("aria-pressed", self.html)

    def test_forms_are_demo_only_and_never_send_data(self):
        self.assertIn("preventDefault()", self.js)
        self.assertIn("Demo only", self.js)
        self.assertIn("<fieldset disabled>", self.html)
        self.assertIn("fieldset.disabled = false", self.js)
        self.assertNotRegex(self.js, r"\b(fetch|XMLHttpRequest|sendBeacon)\s*\(")

    def test_css_uses_logical_properties_not_left_right_layout_rules(self):
        self.assertNotRegex(self.css, r"\b(margin|padding|border|inset)-(left|right)\b")
        self.assertIn("margin-inline", self.css)
        self.assertIn("padding-inline", self.css)

    def test_mobile_breakpoint_and_reduced_motion_are_defined(self):
        self.assertRegex(self.css, r"@media\s*\(max-width:")
        self.assertIn("prefers-reduced-motion", self.css)

    def test_no_remote_assets_or_missing_local_files(self):
        self.assertEqual(self.parser.external_assets, [])
        self.assertTrue((ROOT / "styles.css").is_file())
        self.assertTrue((ROOT / "app.js").is_file())


if __name__ == "__main__":
    unittest.main()
