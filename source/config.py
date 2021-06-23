from flask import Flask
from flask_cors import CORS
import os
from pymemcache.client.base import PooledClient

cache = PooledClient('memcached:11211', max_pool_size=10, encoding="utf-8")

app = Flask(__name__)
CORS(app)

if os.getenv('STAGE') == 'test':
    app.config['BACKEND_URL'] = 'http://localhost:8008'
else:
    app.config['BACKEND_URL'] = 'http://seguimiento-academico_1:8000'
app.config['API_URL'] = app.config['BACKEND_URL'] + '/api'
app.config['TOKEN_URL'] = app.config['API_URL'] + '/token/'
app.config['ALUMNOS_URL'] = app.config['API_URL'] + '/alumnos/'
app.config['CARRERAS_URL'] = app.config['API_URL'] + '/carreras/{}'
app.config['MATERIASCURSADAS_URL'] = app.config['CARRERAS_URL'] + \
    '/materiascursadas/'
app.config['INSCRIPCIONES_URL'] = app.config['CARRERAS_URL'] + \
    '/inscripciones/'
app.config['PLAN_URL'] = app.config['CARRERAS_URL'] + '/planes/{}/'
app.config['ALUMNOS_CARRERA_URL'] = app.config['CARRERAS_URL'] + '/alumnos/'
app.config['CURSANTES_URL'] = app.config['CARRERAS_URL'] + \
    '/cantidad-cursantes/'
app.config['INGRESANTES_URL'] = app.config['CARRERAS_URL'] + \
    '/cantidad-ingresantes/'
app.config['GRADUADOS_URL'] = app.config['CARRERAS_URL'] + \
    '/cantidad-graduados/'
app.config['POSTULANTES_URL'] = app.config['CARRERAS_URL'] + \
    '/cantidad-postulantes/'
app.config['MATERIAS_NECESARIAS_URL'] = app.config['PLAN_URL'] + \
    'cantidad-materias-necesarias/'
app.config['SECRET_KEY'] = 'super-secret'

app.config['USERNAME'] = ''
app.config['PASSWORD'] = ''
