import unittest
from services.eligibility import evaluate_scheme_eligibility, match_user_profile_with_schemes

class TestEligibilityMatching(unittest.TestCase):

    def setUp(self):
        self.sample_scheme = {
            "id": "SCH001",
            "name": "Post-Matric Scholarship for OBC Students",
            "category": "Education",
            "scope": "Central",
            "state_scope": [],
            "minimum_age": 15,
            "maximum_age": 30,
            "maximum_income": 250000,
            "eligible_categories": ["OBC"],
            "eligible_occupations": ["student"]
        }

    def test_matching_eligible_user(self):
        profile = {
            "age": 22,
            "income": 200000,
            "state": "Maharashtra",
            "category": "OBC",
            "occupation": "student",
            "need_category": "Education"
        }
        res = evaluate_scheme_eligibility(profile, self.sample_scheme)

        self.assertEqual(res["profile_match_score"], 100.0)
        self.assertEqual(res["criteria_breakdown"]["age"]["status"], "MATCHED")
        self.assertEqual(res["criteria_breakdown"]["income"]["status"], "MATCHED")
        self.assertEqual(res["criteria_breakdown"]["category"]["status"], "MATCHED")

    def test_unmatched_income_and_category(self):
        profile = {
            "age": 22,
            "income": 400000, # Exceeds 250000
            "state": "Maharashtra",
            "category": "General", # Not OBC
            "occupation": "student",
            "need_category": "Education"
        }
        res = evaluate_scheme_eligibility(profile, self.sample_scheme)

        self.assertLess(res["profile_match_score"], 100.0)
        self.assertEqual(res["criteria_breakdown"]["income"]["status"], "NOT_MATCHED")
        self.assertEqual(res["criteria_breakdown"]["category"]["status"], "NOT_MATCHED")

    def test_missing_attributes(self):
        profile = {
            "age": None,
            "income": None,
            "state": None,
            "category": None,
            "occupation": None,
            "need_category": None
        }
        res = evaluate_scheme_eligibility(profile, self.sample_scheme)
        self.assertEqual(res["criteria_breakdown"]["age"]["status"], "NOT_PROVIDED")
        self.assertEqual(res["criteria_breakdown"]["income"]["status"], "NOT_PROVIDED")

if __name__ == "__main__":
    unittest.main()
