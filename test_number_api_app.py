import unittest
from number_api_app import app

class NumberApiAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_welcome(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'HNG Backend Stage 1 Task')

    def test_classify_num_missing_parameter(self):
        response = self.app.get('/api/classify-number')
        self.assertEqual(response.status_code, 400)
        self.assertIn('missing', response.json['number'])
        self.assertTrue(response.json['error'])

    def test_classify_num_negative_number(self):
        response = self.app.get('/api/classify-number?number=-5')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['number'], 'negative')
        self.assertTrue(response.json['error'])

    def test_classify_num_alphabet_input(self):
        response = self.app.get('/api/classify-number?number=abc')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['number'], 'alphabet')
        self.assertTrue(response.json['error'])

    def test_classify_num_valid_input(self):
        response = self.app.get('/api/classify-number?number=5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['number'], 5)
        self.assertTrue(response.json['is_prime'])
        self.assertFalse(response.json['is_perfect'])
        self.assertIn('odd', response.json['properties'])
        self.assertEqual(response.json['digit_sum'], 5)

    def test_json_sort_keys(self):
        self.assertFalse(app.json.sort_keys)

if __name__ == '__main__':
    unittest.main()