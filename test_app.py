from application import application
import unittest
import requests
url="http://127.0.0.1:5050"
class appTest(unittest.TestCase):

    def setUp(self):
        application.testing = True
        self.app = application.test_client()

    def test_getMethod(self):
        try:
            response = requests.get(url)
            self.assertEqual(response.status_code, 200, "Wrong Request\n")
        except Exception:
            self.assertTrue(response.ok, "Server Not Responding")

    def test_postMethod(self):
        try:
            response = requests.post(url, "jerusalem")
            self.assertEqual(response.status_code, 200, "Bad Request!")
        except Exception:
            self.assertTrue(response.ok, "Server Not Responding")
