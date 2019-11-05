from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['BACKEND_URL'] = 'http://seguimiento-academico:8000'
app.config['API_URL'] = app.config['BACKEND_URL'] + '/api'
app.config['TOKEN_URL'] = app.config['API_URL'] + '/token/'
app.config['ALUMNOS_URL'] = app.config['API_URL'] + '/alumnos/'
app.config['MATERIASCURSADAS_URL'] = app.config['API_URL'] + \
    '/materiascursadas/'
app.config['SECRET_KEY'] = 'super-secret'

app.config['USERNAME'] = ''
app.config['PASSWORD'] = ''
