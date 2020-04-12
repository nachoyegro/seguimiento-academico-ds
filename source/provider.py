import requests
import json
from config import app
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

    def retrieve_alumnos(self, token):
        # token = self.retrieve_token(**kwargs)
        headers = self.get_headers(token)
        response = requests.get(app.config['ALUMNOS_URL'], headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception

    def retrieve_alumnos_de_carrera(self, token, carrera):
        headers = self.get_headers(token)
        response = requests.get(app.config['ALUMNOS_CARRERA_URL'].format(
            carrera), headers=headers)
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

    def retrieve_inscriptos(self, token, carrera):
        """
            Trae las inscripciones desde el backend
        """
        headers = self.get_headers(token)
        response = requests.get(app.config['INSCRIPCIONES_URL'].format(
            carrera), headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception

    def get_materiascursadas(self, token, carrera):
        """
            Se encarga de traer las materias cursadas
            Fijandose primero si ya las tengo localmente
            Caso contrario, las traigo desde el backend y las guardo local
            return JSON
        """
        path = 'data/materiascursadas_{}.json'.format(carrera)
        # Si ya lo traje en otro momento
        if os.path.isfile(path):
            with open(path, 'r') as archivo:
                result = json.loads(archivo.read())
        else:
            # Si no lo tenia, lo traigo y lo guardo para la proxima
            data = self.retrieve_materiascursadas(token, carrera)
            with open(path, 'w+', encoding='utf-8') as archivo:
                json.dump(json.loads(data), archivo,
                          ensure_ascii=False, indent=4)
            result = json.loads(data)
        return result

    def get_materiascursadas_multiples_carreras(self, token, carreras):
        """
            Concatena las materias cursadas de todas las carreras pedidas
            return JSON
        """
        result = []
        for carrera in carreras:
            result += self.get_materiascursadas(token, carrera)
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

    def retrieve_cursantes(self, token, carrera):
        """
            Trae los cursantes historicos de una carrera
        """
        headers = self.get_headers(token)
        response = requests.get(
            app.config['CURSANTES_URL'].format(carrera), headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return []

    def retrieve_ingresantes(self, token, carrera):
        """
            Trae los ingresantes historicos de una carrera
        """
        headers = self.get_headers(token)
        response = requests.get(
            app.config['INGRESANTES_URL'].format(carrera), headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return []

    def retrieve_graduados(self, token, carrera):
        """
            Trae los graduados historicos de una carrera
        """
        headers = self.get_headers(token)
        response = requests.get(
            app.config['GRADUADOS_URL'].format(carrera), headers=headers)
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

    def get_cursantes(self, token, carrera):
        data = self.retrieve_cursantes(token, carrera)
        return json.loads(data)

    def get_ingresantes(self, token, carrera):
        data = self.retrieve_ingresantes(token, carrera)
        return json.loads(data)

    def get_graduados(self, token, carrera):
        data = self.retrieve_graduados(token, carrera)
        return json.loads(data)

    def get_inscriptos(self, token, carrera):
        data = self.retrieve_inscriptos(token, carrera)
        return json.loads(data)

    def get_plan(self, token, carrera, plan):
        data = self.retrieve_plan(token, carrera, plan)
        return json.loads(data)

    def get_alumnos_de_carrera(self, token, carrera):
        data = self.retrieve_alumnos_de_carrera(token, carrera)
        return json.loads(data)