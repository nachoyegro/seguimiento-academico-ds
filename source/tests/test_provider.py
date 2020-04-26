import unittest
import json
import requests
from mock_server import mock_app
from provider import DataProvider

class ProviderTest(unittest.TestCase):

    def setUp(self):
        self.provider = DataProvider()
        self.mock_app = mock_app
        self.mock_app.run("localhost", 8008)

    def test_retrieve_alumnos_de_carrera(self):
        token = self.provider.retrieve_token()
        data = self.provider.retrieve_alumnos_de_carrera(token, 'W')
        alumnos = json.loads(data)
        self.assertEqual(len(alumnos), 10)
