import unittest
from nlp.preprocessing import preprocess_text

class TestNLPPreprocessing(unittest.TestCase):

    def test_tokenization_and_cleaning(self):
        text = "I am a 22-year-old student from Maharashtra!"
        res = preprocess_text(text)
        
        self.assertEqual(res["raw_text"], text)
        self.assertIn("maharashtra", res["cleaned_text"])
        self.assertTrue(len(res["sentences"]) >= 1)
        self.assertIn("student", res["tokens"])

    def test_stopword_removal_and_lemmatization(self):
        text = "Students are studying in colleges for higher degrees."
        res = preprocess_text(text)
        
        # Stop-words 'are', 'in', 'for' should be removed
        self.assertNotIn("are", res["filtered_tokens"])
        self.assertNotIn("for", res["filtered_tokens"])
        
        # Lemmatizer or tokens should contain student/college
        self.assertTrue(len(res["lemmatized_words"]) > 0)

    def test_empty_input(self):
        res = preprocess_text("")
        self.assertEqual(res["tokens"], [])
        self.assertEqual(res["sentences"], [])

if __name__ == "__main__":
    unittest.main()
