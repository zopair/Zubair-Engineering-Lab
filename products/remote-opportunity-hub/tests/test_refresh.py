import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from remote_hub.ingest import refresh, source_url


class RefreshSafetyTests(unittest.TestCase):
    def test_failed_source_does_not_mark_existing_jobs_inactive(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "sources.json"
            output = Path(tmp) / "jobs.json"
            config.write_text(json.dumps({"sources": [{"provider": "greenhouse", "board": "demo", "enabled": True}]}))
            output.write_text(json.dumps({"jobs": [{"id": "existing", "platform": "Greenhouse", "board": "demo", "status": "active"}]}))
            with patch("remote_hub.ingest.fetch_source", side_effect=OSError("network unavailable")):
                result = refresh(str(config), str(output))
            self.assertEqual(result["jobs"][0]["status"], "active")
            self.assertEqual(result["sources"][0]["status"], "error")

    def test_successful_empty_board_marks_missing_job_inactive(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "sources.json"
            output = Path(tmp) / "jobs.json"
            config.write_text(json.dumps({"sources": [{"provider": "greenhouse", "board": "demo", "enabled": True}]}))
            output.write_text(json.dumps({"jobs": [{"id": "existing", "platform": "Greenhouse", "board": "demo", "status": "active"}]}))
            with patch("remote_hub.ingest.fetch_source", return_value=[]):
                result = refresh(str(config), str(output))
            self.assertEqual(result["jobs"][0]["status"], "inactive")

    def test_board_identifier_rejects_path_injection(self):
        with self.assertRaises(ValueError):
            source_url({"provider": "greenhouse", "board": "../other"})


if __name__ == "__main__":
    unittest.main()
