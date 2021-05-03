import requests
import json
from config import app, cache
import os
from transformer import DataTransformer


class DataProvider:

    def retrieve_token(self, **kwargs):
        """
            :kwargs tiene que tener username y password
        """
        token_url = app.config['TOKEN_URL']
        response = requests.post(token_url,
                                 data=kwargs)
        if response.status_code == 200:
            data = json.loads(response.text)
            return data['access']
        else:
            raise Exception

    def get_headers(self, token):
        return {'Authorization': 'Bearer ' + token}
        
    def retrieve_alumnos_de_carrera(self, token, carrera):
        headers = self.get_headers(token)
        response = requests.get(app.config['ALUMNOS_CARRERA_URL'].format(
            carrera), headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception

    def retrieve_cantidad_materias_necesarias(self, token, carrera, plan):
        headers = self.get_headers(token)
        response = requests.get(app.config['MATERIAS_NECESARIAS_URL'].format(
            carrera, plan), headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception

    def retrieve_plan(self, token, carrera, plan):
        """
            Trae el plan de estudios pedido desde el backend
        """
        headers = self.get_headers(token)
        response = requests.get(app.config['PLAN_URL'].format(
            carrera, plan), headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception

    def retrieve_inscriptos(self, token, carrera, anio=None, mes=None):
        """
            Trae las inscripciones desde el backend
        """
        headers = self.get_headers(token)
        url = app.config['INSCRIPCIONES_URL'].format(carrera)
        response = requests.get(url + str(anio) + '/' + str(mes) + '/' if anio else url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception

    def get_materiascursadas(self, token, carrera):
        if cache.get('materias_cursadas'):
            result = json.loads(cache.get('materias_cursadas'))
        else:
            data = self.retrieve_materiascursadas(token, carrera)
            cache.set('materias_cursadas', data)
            result = json.loads(data)
        return result

    def retrieve_materiascursadas(self, token, carrera):
        """
            Trae las materias cursadas desde el backend
        """
        headers = self.get_headers(token)
        response = requests.get(
            app.config['MATERIASCURSADAS_URL'].format(carrera), headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return []

    def retrieve_cursantes(self, token, carrera, anio=None):
        """
            Trae los cursantes de una carrera
        """
        headers = self.get_headers(token)
        url = app.config['CURSANTES_URL'].format(carrera) 
        response = requests.get(url + str(anio) + '/' if anio else url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return []

    def retrieve_ingresantes(self, token, carrera, anio=None):
        """
            Trae los ingresantes de una carrera
        """
        headers = self.get_headers(token)
        url = app.config['INGRESANTES_URL'].format(carrera) 
        response = requests.get(url + str(anio) + '/' if anio else url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return []

    def retrieve_postulantes(self, token, carrera, anio=None):
        """
            Trae los postulantes de una carrera
        """
        headers = self.get_headers(token)
        url = app.config['POSTULANTES_URL'].format(carrera) 
        response = requests.get(url + str(anio) + '/' if anio else url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return []

    def retrieve_graduados(self, token, carrera, anio=None):
        """
            Trae los graduados historicos de una carrera
        """
        headers = self.get_headers(token)
        url = app.config['GRADUADOS_URL'].format(carrera) 
        response = requests.get(url + str(anio) + '/' if anio else url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return []

    """
    def get_materiascursadas_con_plan(self, token, carrera, plan):
        
            Se encarga de mergear los datos de materias cursadas con los datos del plan
            Quedando un DataFrame con datos completos, incluyendo creditos, areas, etc
            return DataFrame
        
        materiascursadas_data = self.get_materiascursadas(token, carrera)
        materiascursadas_data.rename(
            columns={'materia': 'codigo'}, inplace=True)
        plan_data = self.retrieve_plan(token, carrera, plan)
        return pd.merge(materiascursadas_data, plan_data, on=['codigo'])
    """

    def get_cursantes(self, token, carrera, anio=None):
        data = self.retrieve_cursantes(token, carrera, anio)
        return json.loads(data)

    def get_ingresantes(self, token, carrera, anio=None):
        data = self.retrieve_ingresantes(token, carrera, anio)
        return json.loads(data)

    def get_postulantes(self, token, carrera, anio=None):
        data = self.retrieve_postulantes(token, carrera, anio)
        return json.loads(data)

    def get_graduados(self, token, carrera, anio=None):
        data = self.retrieve_graduados(token, carrera, anio)
        return json.loads(data)

    def get_inscriptos(self, token, carrera, anio=None, mes=None):
        data = self.retrieve_inscriptos(token, carrera, anio, mes)
        return json.loads(data)

    def get_plan(self, token, carrera, plan):
        data = self.retrieve_plan(token, carrera, plan)
        return json.loads(data)

    def get_alumnos_de_carrera(self, token, carrera):
        data = self.retrieve_alumnos_de_carrera(token, carrera)
        return json.loads(data)

    def get_cantidad_materias_necesarias(self, token, carrera, plan):
        data = self.retrieve_cantidad_materias_necesarias(token, carrera, plan)
        return json.loads(data)