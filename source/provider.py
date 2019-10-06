import requests
import json
from config import app

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

    def retrieve_materiascursadas(self, token):
        """
            :url must be /materiascursadas
            :kwargs
        """
        #token = self.retrieve_token(**kwargs)
        headers = self.get_headers(token)
        response = requests.get(app.config['MATERIASCURSADAS_URL'], headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception
        



