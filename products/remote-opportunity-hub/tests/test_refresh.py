import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from datetime import datetime, timezone
from remote_hub.ingest import fetch_himalayas, refresh, source_url


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


    def test_himalayas_browse_fallback_shows_geographic_restrictions(self):
        source = {"provider": "himalayas", "board": "egypt-worldwide", "company": "Himalayas listings", "queries": [{"country": "EG"}], "max_pages": 1, "fallback_browse_pages": 1}
        worldwide = {"guid": "global-1", "title": "Remote Python Developer", "applicationLink": "https://himalayas.app/jobs/global-1", "locationRestrictions": []}
        us_only = {"guid": "us-1", "title": "Remote US Developer", "applicationLink": "https://himalayas.app/jobs/us-1", "locationRestrictions": [{"name": "United States", "alpha2": "US"}]}
        with patch("remote_hub.ingest.fetch_json", side_effect=[{"jobs": []}, {"jobs": [worldwide, us_only]}]):
            jobs = fetch_himalayas(source)
        self.assertEqual(len(jobs), 2)
        by_id = {job["external_id"]: job for job in jobs}
        self.assertEqual(by_id["global-1"]["eligibility_label"], "Worldwide")
        self.assertIn("United States", by_id["us-1"]["eligibility_label"])

    def test_himalayas_daily_cache_prevents_repeated_api_calls(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "sources.json"
            output = Path(tmp) / "jobs.json"
            config.write_text(json.dumps({"sources": [{"provider": "himalayas", "board": "egypt-worldwide", "enabled": True}]}))
            verified = datetime.now(timezone.utc).isoformat()
            output.write_text(json.dumps({"jobs": [], "sources": [{"source": "himalayas:egypt-worldwide", "status": "ok", "jobs": 4, "verified_at": verified}]}))
            with patch("remote_hub.ingest.fetch_source", side_effect=AssertionError("daily cache should skip fetch")):
                result = refresh(str(config), str(output))
            self.assertEqual(result["sources"][0]["status"], "cached")

    def test_board_identifier_rejects_path_injection(self):
        with self.assertRaises(ValueError):
            source_url({"provider": "greenhouse", "board": "../other"})


if __name__ == "__main__":
    unittest.main()
