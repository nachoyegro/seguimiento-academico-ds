from flask import Flask

app = Flask(__name__)
app.config['BACKEND_URL'] = 'http://127.0.0.1:8000/api'
app.config['API_V2_URL'] = app.config['BACKEND_URL'] + '/v2'
app.config['TOKEN_URL'] = app.config['BACKEND_URL'] + '/token/'
app.config['ALUMNOS_URL'] = app.config['API_V2_URL'] + '/alumnos/'