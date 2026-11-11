import copy
import importlib.util
import json
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_demand_snapshot.py"
SPEC = importlib.util.spec_from_file_location("validator", SCRIPT)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class DemandSnapshotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads(validator.DATA.read_text(encoding="utf-8"))

    def test_checked_in_snapshot_is_valid(self):
        self.assertEqual(validator.validate(self.payload), [])

    def test_duplicate_ids_are_rejected(self):
        payload = copy.deepcopy(self.payload)
        payload["jobs"][1]["id"] = payload["jobs"][0]["id"]
        self.assertIn("job IDs must be unique", validator.validate(payload))

    def test_non_upwork_urls_are_rejected(self):
        payload = copy.deepcopy(self.payload)
        payload["jobs"][0]["url"] = "https://example.com/jobs/123"
        self.assertTrue(any(".url must be an Upwork job URL" in e for e in validator.validate(payload)))

    def test_category_count_drift_is_rejected(self):
        payload = copy.deepcopy(self.payload)
        payload["category_counts"]["excel_data"] += 1
        self.assertIn("category_counts does not match actual job records", validator.validate(payload))

    def test_missing_delivery_notes_are_rejected(self):
        payload = copy.deepcopy(self.payload)
        del payload["jobs"][0]["delivery_notes"]
        self.assertTrue(any("delivery_notes" in e for e in validator.validate(payload)))


if __name__ == "__main__":
    unittest.main()
