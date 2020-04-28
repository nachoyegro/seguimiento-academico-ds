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
                response = client.get('/materias/90028/recursantes?carrera=TEST')
                self.assertEqual(response.status_code, 401)

    def test_recursantes(self):
        """
            Hago un request con token, deberia darme los recursantes
            Chequeo que el alumno con legajo 1 haya recursado 2 veces
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/materias/90028/recursantes?carrera=TEST', headers={"Authorization": f"Bearer {token}"})
                data = json.loads(response.get_data())
                self.assertEqual(data['1'], 2)

    def test_detalle_aprobados_unauthorized(self):
        """
            Hago un request sin token, deberia darme 401
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/materias/90028/detalle-aprobados?carrera=TEST')
                self.assertEqual(response.status_code, 401)

    def test_detalle_aprobados(self):
        """
            Hago un request con token
            Deberia darme un solo resultado, el alumno con legajo 10
            Que promociono en otra carrera
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/materias/90028/detalle-aprobados?carrera=TEST', headers={"Authorization": f"Bearer {token}"})
                data = json.loads(response.get_data())
                self.assertEqual(data[0]['Promocion en otra carrera'], 1)

    def test_basicos_unauthorized(self):
        """
            Hago un request sin token, deberia darme 401
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/materias/90028/basicos?carrera=TEST')
                self.assertEqual(response.status_code, 401)

    def test_basicos_aprobados(self):
        """
            Hago un request con token
            Segun los datos, hay un solo aprobado
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/materias/90028/basicos?carrera=TEST', headers={"Authorization": f"Bearer {token}"})
                data = json.loads(response.get_data())
                self.assertEqual(data[0]['Aprobados'], 1)

    def test_basicos_ausentes(self):
        """
            Hago un request con token
            Segun los datos, no hay ausentes
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/materias/90028/basicos?carrera=TEST', headers={"Authorization": f"Bearer {token}"})
                data = json.loads(response.get_data())
                self.assertEqual(data[0]['Ausentes'], 0)

    def test_basicos_desaprobados(self):
        """
            Hago un request con token
            Segun los datos, hay 4 desaprobados
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/materias/90028/basicos?carrera=TEST', headers={"Authorization": f"Bearer {token}"})
                data = json.loads(response.get_data())
                self.assertEqual(data[0]['Desaprobados'], 4)

    def test_basicos_faltantes(self):
        """
            Hago un request con token
            Segun los datos, hay 9 faltantes
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/materias/90028/basicos?carrera=TEST', headers={"Authorization": f"Bearer {token}"})
                data = json.loads(response.get_data())
                self.assertEqual(data[0]['Faltantes'], 9)


    def test_dispersion_notas_unauthorized(self):
        """
            Hago un request sin token, deberia darme 401
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/materias/90028/dispersion-notas?carrera=TEST')
                self.assertEqual(response.status_code, 401)

    def test_dispersion_notas(self):
        """
            Hago un request con token
            Devuelvo la primer nota, que deberia ser 2
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/materias/90028/dispersion-notas?carrera=TEST', headers={"Authorization": f"Bearer {token}"})
                data = json.loads(response.get_data())
                self.assertEqual(data[0]['Nota'], '2')

    def test_porcentajes_areas_unauthorized(self):
        """
            Hago un request sin token, deberia darme 401
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/alumnos/1/porcentajes-areas?carrera=TEST&plan=2019')
                self.assertEqual(response.status_code, 401)

    def test_porcentajes_areas(self):
        """
            Hago un request con token
            Deberia tener un 50 de ingles
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/alumnos/1/porcentajes-areas?carrera=TEST&plan=2019', headers={"Authorization": f"Bearer {token}"})
                data = json.loads(response.get_data())
                for materia in data:
                    if materia['nombre'] == 'Inglés':
                        self.assertEqual("%.2f" % materia['valor'], '50.00')

    def test_porcentajes_nucleos_unauthorized(self):
        """
            Hago un request sin token, deberia darme 401
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/alumnos/1/porcentajes-nucleos?carrera=TEST&plan=2019')
                self.assertEqual(response.status_code, 401)

    def test_porcentajes_nucleos(self):
        """
            Hago un request con token
            Deberia tener un 33.33 del ingreso
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/alumnos/1/porcentajes-nucleos?carrera=TEST&plan=2019', headers={"Authorization": f"Bearer {token}"})
                data = json.loads(response.get_data())
                for nucleo in data:
                    if nucleo['nombre'] == 'I':
                        self.assertEqual("%.2f" % nucleo['valor'], '33.33')

    def test_alumnos_carrera_unauthorized(self):
        """
            Hago un request sin token, deberia darme 401
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/carreras/TEST/alumnos?plan=2019')
                self.assertEqual(response.status_code, 401)

    def test_alumnos_carrera(self):
        """
            Hago un request con token
            Deberia darme 10 alumnos
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/carreras/TEST/alumnos?plan=2019', headers={"Authorization": f"Bearer {token}"})
                data = json.loads(response.get_data())
                self.assertEqual(data[0]['cantidad'], 10)

    def test_cantidades_alumnos_unauthorized(self):
        """
            Hago un request sin token, deberia darme 401
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/carreras/TEST/cantidades-alumnos?plan=2019')
                self.assertEqual(response.status_code, 401)

    def test_cantidades_alumnos_graduados(self):
        """
            Hago un request con token
            Deberia retornar [..., {'Cohorte': 2019, 'Graduados': 1, 'Cursantes': 10, 'Ingresantes': 2}]
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/carreras/TEST/cantidades-alumnos?plan=2019', headers={"Authorization": f"Bearer {token}"})
                data = json.loads(response.get_data())
                for cohorte in data:
                    if cohorte['Cohorte'] == 2019:
                        self.assertEqual(cohorte['Graduados'], 1)

    def test_cantidades_alumnos_ingresantes(self):
        """
            Hago un request con token
            Deberia retornar [..., {'Cohorte': 2019, 'Graduados': 1, 'Cursantes': 10, 'Ingresantes': 2}]
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/carreras/TEST/cantidades-alumnos', headers={"Authorization": f"Bearer {token}"})
                data = json.loads(response.get_data())
                for cohorte in data:
                    if cohorte['Cohorte'] == 2019:
                        self.assertEqual(cohorte['Ingresantes'], 2)

    def test_cantidades_alumnos_cursantes(self):
        """
            Hago un request con token
            Deberia retornar [..., {'Cohorte': 2019, 'Graduados': 1, 'Cursantes': 10, 'Ingresantes': 2}]
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/carreras/TEST/cantidades-alumnos', headers={"Authorization": f"Bearer {token}"})
                data = json.loads(response.get_data())
                for cohorte in data:
                    if cohorte['Cohorte'] == 2019:
                        self.assertEqual(cohorte['Cursantes'], 10)

    def test_cantidades_ingresantes_unauthorized(self):
        """
            Hago un request sin token, deberia darme 401
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/carreras/TEST/cantidades-ingresantes')
                self.assertEqual(response.status_code, 401)

    def test_cantidades_ingresantes(self):
        """
            Hago un request con token
            Deberia retornar [..., {'Cohorte': 2019, 'Alumnos ingresantes': 2}]
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/carreras/TEST/cantidades-ingresantes', headers={"Authorization": f"Bearer {token}"})
                data = json.loads(response.get_data())
                for cohorte in data:
                    if cohorte['Cohorte'] == 2019:
                        self.assertEqual(cohorte['Alumnos ingresantes'], 2)

    def test_cursantes_actual_unauthorized(self):
        """
            Hago un request sin token, deberia darme 401
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/carreras/TEST/cursantes-actual')
                self.assertEqual(response.status_code, 401)

    def test_cursantes_actual(self):
        """
            Hago un request con token
            Deberia retornar {'nombre': 'Cursantes del año actual', 'valor': 10}
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/carreras/TEST/cursantes-actual', headers={"Authorization": f"Bearer {token}"})
                data = json.loads(response.get_data())
                self.assertEqual(data['valor'], 10)

    def test_ingresantes_actual_unauthorized(self):
        """
            Hago un request sin token, deberia darme 401
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/carreras/TEST/ingresantes-actual')
                self.assertEqual(response.status_code, 401)

    def test_ingresantes_actual(self):
        """
            Hago un request con token
            Deberia retornar {'nombre': 'Ingresantes del año actual', 'valor': 2}
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/carreras/TEST/ingresantes-actual', headers={"Authorization": f"Bearer {token}"})
                data = json.loads(response.get_data())
                self.assertEqual(data['valor'], 2)


    def test_graduados_total_unauthorized(self):
        """
            Hago un request sin token, deberia darme 401
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/carreras/TEST/graduados-total')
                self.assertEqual(response.status_code, 401)

    def test_graduados_total(self):
        """
            Hago un request con token
            Deberia retornar {'nombre': 'Graduados', 'valor': 1}
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/carreras/TEST/graduados-total', headers={"Authorization": f"Bearer {token}"})
                data = json.loads(response.get_data())
                self.assertEqual(data['valor'], 1)

    def test_notas_unauthorized(self):
        """
            Hago un request sin token, deberia darme 401
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/alumnos/1/notas?carrera=TEST&plan=2019')
                self.assertEqual(response.status_code, 401)

    def test_notas(self):
        """
            Hago un request con token
            Deberia retornar [... {'Fecha': '2018-02-07', 'Materia': 'Inglés II', 'Plan': 2019, 'Nota': '3'}]
        """
        with self.mock_app.run(self.mock_url, self.mock_port):
            with test_app.test_client() as client:
                token = self.provider.retrieve_token()
                response = client.get('/alumnos/1/notas?carrera=TEST&plan=2019', headers={"Authorization": f"Bearer {token}"})
                data = json.loads(response.get_data())
                for materia in data:
                    if materia['Materia'] == 'Inglés II' and materia['Fecha'] == '2018-02-07':
                        self.assertEqual(materia['Nota'], '3')