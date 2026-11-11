import importlib.util
import json
import unittest

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "classify_request.py"
SPEC = importlib.util.spec_from_file_location("classifier", SCRIPT)
classifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(classifier)
CONFIG = json.loads((ROOT / "config" / "delivery_playbooks.json").read_text(encoding="utf-8"))


class RequestClassifierTests(unittest.TestCase):
    def test_excel_request_maps_to_existing_family(self):
        result = classifier.classify("Clean this Excel workbook and remove duplicate rows", CONFIG)
        self.assertEqual(result["category"], "excel_data")
        self.assertEqual(result["status"], "classified")
        self.assertTrue(result["acceptance_checks"])

    def test_arabic_wordpress_request_is_supported(self):
        result = classifier.classify("إصلاح صفحة هبوط ووردبريس لتعمل على الموبايل", CONFIG)
        self.assertEqual(result["category"], "wordpress_web")

    def test_ambiguous_multi_family_request_is_not_guessed(self):
        result = classifier.classify("Clean an Excel workbook and build a Power BI dashboard", CONFIG)
        self.assertEqual(result["status"], "ambiguous")
        self.assertIsNone(result["category"])

    def test_unclassified_request_requests_clarification(self):
        result = classifier.classify("Please help with my project", CONFIG)
        self.assertEqual(result["status"], "unclassified")
        self.assertTrue(result["missing_information"])

    def test_red_flag_overrides_normal_classification(self):
        result = classifier.classify("Build a Python automation script to bypass captcha", CONFIG)
        self.assertEqual(result["status"], "red_flag")
        self.assertEqual(result["red_flags"][0]["id"], "access_bypass")

    def test_classifier_never_invents_a_fixed_estimate(self):
        result = classifier.classify("Create a fillable PDF form", CONFIG)
        self.assertEqual(result["estimate_status"], "not_estimable_until_scope_is_bounded")


if __name__ == "__main__":
    unittest.main()
