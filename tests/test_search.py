import unittest
from services.scheme_search import SchemeSearchService
from nlp.spell_correction import correct_word, correct_text

class TestSchemeSearch(unittest.TestCase):

    def setUp(self):
        self.sample_schemes = [
            {
                "id": "SCH001",
                "name": "Post-Matric Scholarship for OBC Students",
                "category": "Education",
                "scope": "Central",
                "description": "Financial assistance for education and tuition fees for college students.",
                "keywords": ["education", "scholarship", "obc", "student"],
                "target_groups": ["OBC Students"],
                "eligible_occupations": ["student"]
            },
            {
                "id": "SCH003",
                "name": "Pradhan Mantri Kisan Samman Nidhi",
                "category": "Agriculture",
                "scope": "Central",
                "description": "Financial benefit and income support for landholding farmers.",
                "keywords": ["farmer", "agriculture", "kisan", "crop"],
                "target_groups": ["Farmers"],
                "eligible_occupations": ["farmer"]
            }
        ]
        self.search_service = SchemeSearchService(self.sample_schemes)

    def test_tfidf_search_relevance(self):
        results = self.search_service.search_schemes(query="education scholarship")
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]["id"], "SCH001")

        farmer_results = self.search_service.search_schemes(query="farmer crop loan")
        self.assertTrue(len(farmer_results) > 0)
        self.assertEqual(farmer_results[0]["id"], "SCH003")

    def test_spelling_correction(self):
        self.assertEqual(correct_word("Mahrastra"), "Maharashtra")
        self.assertEqual(correct_word("studant"), "student")
        self.assertEqual(correct_word("agricultre"), "agriculture")

        res = correct_text("I am a studant from Mahrastra")
        self.assertIn("student", res["corrected_text"])
        self.assertIn("Maharashtra", res["corrected_text"])

if __name__ == "__main__":
    unittest.main()
