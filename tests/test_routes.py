import unittest
from app import app, SCHEMES_DATASET

class TestFlaskRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'GovScheme NLP', response.data)

    def test_check_eligibility_route(self):
        response = self.app.get('/check-eligibility')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Tell Us About Yourself', response.data)

    def test_process_profile_post_route(self):
        response = self.app.post('/process-profile', data={'user_text': 'I am a 22 year old student from Maharashtra.'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Analyzing Your Natural Language Input', response.data)

    def test_results_route(self):
        response = self.app.post('/results', data={'user_text': 'I am a 22 year old student from Maharashtra. My family income is 2.5 lakh. OBC category, education scholarship.'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Relevant Government Schemes', response.data)
        self.assertIn(b'Post-Matric Scholarship for OBC Students', response.data)

    def test_scheme_details_route(self):
        first_id = SCHEMES_DATASET[0]['id']
        response = self.app.get(f'/scheme/{first_id}')
        self.assertEqual(response.status_code, 200)

    def test_find_schemes_route(self):
        response = self.app.get('/find-schemes?query=scholarship&category=Education')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Search Results', response.data)

    def test_nlp_analysis_route(self):
        response = self.app.get('/nlp-analysis')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'How NLP Understands Your Input', response.data)

    def test_how_it_works_route(self):
        response = self.app.get('/how-it-works')
        self.assertEqual(response.status_code, 200)

    def test_about_route(self):
        response = self.app.get('/about')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
