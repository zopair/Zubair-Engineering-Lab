import unittest
from remote_hub.normalize import normalize_greenhouse, normalize_lever, normalize_ashby, is_explicitly_remote

class NormalizationTests(unittest.TestCase):
    def test_greenhouse_maps_platform_and_application_url(self):
        raw = {"id": 12, "title": "Data Analyst", "absolute_url": "https://jobs.example/12", "location": {"name": "Remote - Worldwide"}, "first_published": "2026-11-10T10:00:00Z"}
        job = normalize_greenhouse(raw, {"company": "Example", "board": "example"})
        self.assertEqual(job["platform"], "Greenhouse")
        self.assertEqual(job["application_url"], "https://jobs.example/12")
        self.assertEqual(job["remote_status"], "remote")

    def test_lever_maps_hosted_url_and_workplace(self):
        raw = {"id": "abc", "text": "Python Engineer", "hostedUrl": "https://jobs.lever.co/example/abc", "categories": {"location": "Remote, EMEA"}, "descriptionPlain": "Work remotely"}
        job = normalize_lever(raw, {"company": "Example", "board": "example"})
        self.assertEqual(job["platform"], "Lever")
        self.assertEqual(job["remote_status"], "remote")

    def test_ashby_rejects_hybrid_as_fully_remote(self):
        raw = {"title": "Engineer", "jobUrl": "https://jobs.ashbyhq.com/x", "workplaceType": "Hybrid", "location": "Remote / New York"}
        job = normalize_ashby(raw, {"company": "Example", "board": "example"})
        self.assertEqual(job["remote_status"], "hybrid")

    def test_unknown_location_is_not_promoted_to_remote(self):
        self.assertFalse(is_explicitly_remote("Cairo, Egypt", "Software Engineer", ""))
        
if __name__ == "__main__":
    unittest.main()
