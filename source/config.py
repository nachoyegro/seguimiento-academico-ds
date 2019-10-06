from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['BACKEND_URL'] = 'http://127.0.0.1:8000/api'
app.config['API_V2_URL'] = app.config['BACKEND_URL'] + '/v2'
app.config['TOKEN_URL'] = app.config['BACKEND_URL'] + '/token/'
app.config['ALUMNOS_URL'] = app.config['API_V2_URL'] + '/alumnos/'
app.config['MATERIASCURSADAS_URL'] = app.config['API_V2_URL'] + '/materiascursadas/'


app.config['USERNAME'] = ''
app.config['PASSWORD'] = ''
