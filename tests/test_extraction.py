import unittest
from nlp.entity_extraction import (
    extract_age,
    extract_income,
    extract_state,
    extract_user_profile
)

class TestAttributeExtraction(unittest.TestCase):

    def test_age_extraction(self):
        self.assertEqual(extract_age("I am 22 years old."), 22)
        self.assertEqual(extract_age("My age is 25."), 25)
        self.assertEqual(extract_age("I am a 20-year-old student."), 20)
        self.assertIsNone(extract_age("I like computer science."))

    def test_income_extraction(self):
        self.assertEqual(extract_income("My family income is ₹2.5 lakh per year."), 250000)
        self.assertEqual(extract_income("Income of 250000 rupees"), 250000)
        self.assertEqual(extract_income("Annual earning 1.8 lakhs"), 180000)
        self.assertEqual(extract_income("Income is 300000"), 300000)

    def test_state_extraction(self):
        self.assertEqual(extract_state("I live in Maharashtra."), "Maharashtra")
        self.assertEqual(extract_state("I belong to maharashtra state."), "Maharashtra")
        # Typo tolerance
        self.assertEqual(extract_state("I am from Mahrastra."), "Maharashtra")

    def test_full_user_profile_extraction(self):
        sample_text = "I am a 22 year old student from Maharashtra. My family income is ₹2.5 lakh per year. I belong to OBC category and I am looking for an education scholarship."
        profile = extract_user_profile(sample_text)

        self.assertEqual(profile["age"], 22)
        self.assertEqual(profile["income"], 250000)
        self.assertEqual(profile["state"], "Maharashtra")
        self.assertEqual(profile["occupation"], "student")
        self.assertEqual(profile["category"], "OBC")
        self.assertEqual(profile["need_category"], "Education")
        self.assertTrue(profile["student_status"])

if __name__ == "__main__":
    unittest.main()
