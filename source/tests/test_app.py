import unittest
import json
import requests
from provider import DataProvider
from mock_server import mock_app
from app import bp
from flask import Flask

test_app = Flask(__name__)
test_app.register_blueprint(bp)

class AppTest(unittest.TestCase):

    def setUp(self):
        self.provider = DataProvider()
        self.mock_app = mock_app
        self.mock_url = "0.0.0.0"
        self.mock_port = 8008

    def test_recursantes_unauthorized(self):
        """
            Hago un request sin el token, y deberia darme 401
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                response = client.get('/materias/90028/recursantes')
                self.assertEqual(response.status_code, 401)

    def test_recursantes(self):
        """
            Hago un request con token, deberia darme los recursantes
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/materias/90028/recursantes?carrera=TEST', headers={"Authorization": f"Bearer {token}"})
                self.assertEqual(response.status_code, 200)