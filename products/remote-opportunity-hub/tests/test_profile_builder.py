import unittest
from remote_hub.profile_builder import build_profile

class ProfileBuilderTests(unittest.TestCase):
    def test_optional_answers_produce_truthful_copy(self):
        profile = build_profile({"target_role":"Data Analyst","skills":["Python","SQL"],"projects":[{"name":"Sales dashboard","description":"Built KPI dashboard"}],"experience_years":None})
        self.assertIn("Data Analyst", profile["headline"])
        self.assertIn("Python", profile["skills"])
        self.assertNotIn("years of experience", profile["about"].lower())

    def test_empty_profile_does_not_invent_qualifications(self):
        profile = build_profile({})
        self.assertIn("add your real", profile["about"].lower())
        self.assertEqual(profile["skills"], [])
        
if __name__ == "__main__":
    unittest.main()
