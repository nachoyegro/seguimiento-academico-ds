import unittest
import json
import requests
from mock_server import mock_app
from provider import DataProvider

class ProviderTest(unittest.TestCase):

    def setUp(self):
        self.provider = DataProvider()
        self.mock_app = mock_app
        self.url = "localhost"
        self.port = 8008

    def test_get_alumnos_de_carrera(self):
        with self.mock_app.run(self.url, self.port):
            token = self.provider.retrieve_token()
            alumnos = self.provider.get_alumnos_de_carrera(token, 'W')
            self.assertEqual(len(alumnos), 10)

    def test_get_cantidad_materias_necesarias(self):
        with self.mock_app.run(self.url, self.port):
            token = self.provider.retrieve_token()
            materias_necesarias = self.provider.get_cantidad_materias_necesarias(token, 'W', 2015)
            self.assertEqual(materias_necesarias['cantidad'], 40)

    def test_get_plan(self):
        with self.mock_app.run(self.url, self.port):
            token = self.provider.retrieve_token()
            materias = self.provider.get_plan(token, 'W', 2015)
            self.assertEqual(len(materias), 59)

    def test_get_inscriptos(self):
        with self.mock_app.run(self.url, self.port):
            token = self.provider.retrieve_token()
            inscriptos = self.provider.get_inscriptos(token, 'W')
            self.assertEqual(len(inscriptos), 10)

    def test_get_graduados(self):
        with self.mock_app.run(self.url, self.port):
            token = self.provider.retrieve_token()
            graduados = self.provider.get_graduados(token, 'W')
            self.assertEqual(len(graduados), 10)

    def test_get_graduados_anio(self):
        with self.mock_app.run(self.url, self.port):
            token = self.provider.retrieve_token()
            graduados = self.provider.get_graduados(token, 'W', 2019)
            self.assertEqual(graduados['cantidad'], 1)

    def test_get_ingresantes(self):
        with self.mock_app.run(self.url, self.port):
            token = self.provider.retrieve_token()
            ingresantes = self.provider.get_ingresantes(token, 'W')
            self.assertEqual(len(ingresantes), 10)

    def test_get_ingresantes_anio(self):
        with self.mock_app.run(self.url, self.port):
            token = self.provider.retrieve_token()
            ingresantes = self.provider.get_ingresantes(token, 'W', 2019)
            self.assertEqual(ingresantes['cantidad'], 2)

    def test_get_cursantes(self):
        with self.mock_app.run(self.url, self.port):
            token = self.provider.retrieve_token()
            cursantes = self.provider.get_cursantes(token, 'W')
            self.assertEqual(len(cursantes), 10)

    def test_get_cursantes_anio(self):
        with self.mock_app.run(self.url, self.port):
            token = self.provider.retrieve_token()
            cursantes = self.provider.get_cursantes(token, 'W', 2019)
            self.assertEqual(cursantes['cantidad'], 10)

    def test_get_postulantes(self):
        with self.mock_app.run(self.url, self.port):
            token = self.provider.retrieve_token()
            postulantes = self.provider.get_postulantes(token, 'W')
            self.assertEqual(len(postulantes), 10)

    def test_get_postulantes_anio(self):
        with self.mock_app.run(self.url, self.port):
            token = self.provider.retrieve_token()
            postulantes = self.provider.get_postulantes(token, 'W', 2019)
            self.assertEqual(postulantes['cantidad'], 3)