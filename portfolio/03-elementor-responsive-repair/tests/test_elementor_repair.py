import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PreviewParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.section_classes = []
        self.main_count = 0
        self.css_links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "main":
            self.main_count += 1
        if tag == "section":
            self.section_classes.append(attrs.get("class", ""))
        if tag == "link" and attrs.get("rel") == "stylesheet":
            self.css_links.append(attrs.get("href"))


class ElementorRepairTests(unittest.TestCase):
    def setUp(self):
        self.plugin = (ROOT / "elementor-mobile-section-fix.php").read_text(encoding="utf-8")
        self.css = (ROOT / "assets" / "elementor-mobile-fix.css").read_text(encoding="utf-8")
        self.preview = (ROOT / "preview.html").read_text(encoding="utf-8")
        self.parser = PreviewParser()
        self.parser.feed(self.preview)

    def test_plugin_has_metadata_and_wordpress_direct_access_guard(self):
        self.assertIn("Plugin Name:", self.plugin)
        self.assertIn("defined('ABSPATH') || exit", self.plugin)

    def test_stylesheet_is_enqueued_only_when_elementor_is_loaded(self):
        self.assertIn("did_action('elementor/loaded')", self.plugin)
        self.assertIn("wp_enqueue_style", self.plugin)
        self.assertIn("wp_enqueue_scripts", self.plugin)

    def test_css_is_scoped_to_the_target_elementor_section(self):
        self.assertIn(".elementor-element-7f3a9c2", self.css)
        self.assertNotRegex(self.css, r"(?m)^\s*(?:body|html|h1|p|\.elementor-widget)\s*\{")

    def test_mobile_repair_and_logical_properties_are_present(self):
        self.assertIn("@media (max-width: 767px)", self.css)
        self.assertIn("padding-inline", self.css)
        self.assertIn("margin-inline", self.css)
        self.assertNotRegex(self.css, r"\b(margin|padding|inset)-(left|right)\b")

    def test_preview_contains_target_section_and_local_stylesheet(self):
        self.assertEqual(self.parser.main_count, 1)
        self.assertTrue(any("elementor-element-7f3a9c2" in value for value in self.parser.section_classes))
        self.assertIn("./assets/elementor-mobile-fix.css", self.parser.css_links)

    def test_plugin_and_preview_have_no_remote_runtime_dependencies(self):
        self.assertNotRegex(self.plugin, r"https?://")
        self.assertNotRegex(self.preview, r"https?://")
        self.assertTrue((ROOT / "assets" / "elementor-mobile-fix.css").is_file())


if __name__ == "__main__":
    unittest.main()
