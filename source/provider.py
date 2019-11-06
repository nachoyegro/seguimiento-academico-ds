import requests
import json
from config import app
import os


class DataProvider:

    def retrieve_token(self, **kwargs):
        """
            Retrieve data from alumnos-backend
            Response from request is '{"access": <token>, "refresh": <token>}'
            :kwargs must have username and password
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
        """
            :url must be /alumnos, /materias, /carreras...
            :kwargs
        """
        #token = self.retrieve_token(**kwargs)
        headers = self.get_headers(token)
        response = requests.get(app.config['ALUMNOS_URL'], headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception

    def retrieve_plan(self, token, carrera, plan):
        headers = self.get_headers(token)
        response = requests.get(app.config['PLAN_URL'].format(
            carrera, plan), headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception

    def get_materiascursadas(self, token, carrera):
        # TODO: me falta chequear permisos
        path = 'data/materiascursadas_{}.json'.format(carrera)
        # Si ya lo traje en otro momento
        if os.path.isfile(path):
            with open(path, 'r') as archivo:
                return json.loads(archivo.read())
        else:
            # Si no lo tenia, lo traigo y lo guardo para la proxima
            data = self.retrieve_materiascursadas(token, carrera)
            with open(path, 'w+') as archivo:
                archivo.write(json.dumps(data))
                archivo.close()
            return json.loads(data)

    def retrieve_materiascursadas(self, token, carrera):
        headers = self.get_headers(token)
        response = requests.get(
            app.config['MATERIASCURSADAS_URL'].format(carrera), headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return []
