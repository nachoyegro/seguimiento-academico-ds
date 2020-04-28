from http_server_mock import HttpServerMock
import json

mock_app = HttpServerMock(__name__)

@mock_app.route("/api/token/", methods=["POST"])
def token():
    """
        Devuelve un token que vence en el 2050
        Para la carrera TEST
        y el username test
    """
    return json.dumps({
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU4Nzk5MjIyNCwianRpIjoiN2EwMzdlNGYxOGFmNDVmOWE1YzcxZDRhYzhiMDg1ODEiLCJ1c2VyX2lkIjoxLCJjYXJyZXJhcyI6WyJBIiwiQiIsIkMiLCJEIiwiRSIsIkYiLCJHIiwiSCIsIkkiLCJKIiwiSjIiLCJLIiwiTCIsIk4yIiwiUCIsIlEiLCJPIiwiUiIsIlMiLCJOIiwiTSIsIlQiLCJBMSIsIkcxIiwiVSIsIlYiLCJWMSIsIlciLCJIMSJdLCJ1c2VybmFtZSI6ImFkbWluIn0.2QgqtOEsSreA-yp43qJsTyno_K6ptyB_WkbPUS1doCQ",
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoyNTM0OTc1OTk5LCJqdGkiOiJlNTAyNTYzZWE5MmI0MDYwOTczYTAxNDE5ODkxMDU4OSIsInVzZXJfaWQiOjEsImNhcnJlcmFzIjpbIlRFU1QiXSwidXNlcm5hbWUiOiJ0ZXN0In0.1pto6DgaLX_GetMuJNQ8pkL9jMStUDOWqkk8P3Y5PXM"
                        })

@mock_app.route("/api/carreras/TEST/alumnos/", methods=["GET"])
def carrera_alumnos():
    with open('source/tests/json/api_carreras_alumnos.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/TEST/planes/2019/cantidad-materias-necesarias/", methods=["GET"])
def carrera_plan_materias_necesarias():
    with open('source/tests/json/api_carrera_planes_anio_cantidad_materias_necesarias.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)
    
@mock_app.route("/api/carreras/TEST/planes/", methods=["GET"])
def carrera_planes():
    with open('source/tests/json/api_carreras_planes.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/TEST/planes/2019/", methods=["GET"])
def carrera_planes_anio():
    with open('source/tests/json/api_carreras_planes_anio.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/TEST/inscripciones/", methods=["GET"])
def carrera_inscripciones():
    with open('source/tests/json/api_carreras_inscripciones.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/TEST/cantidad-graduados/", methods=["GET"])
def carrera_cantidad_graduados():
    with open('source/tests/json/api_carreras_cantidad_graduados.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/TEST/cantidad-graduados/2019/", methods=["GET"])
def carrera_cantidad_graduados_anio():
    with open('source/tests/json/api_carreras_cantidad_graduados_anio.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/TEST/cantidad-postulantes/", methods=["GET"])
def carrera_cantidad_postulantes():
    with open('source/tests/json/api_carreras_cantidad_postulantes.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/TEST/cantidad-postulantes/2019/", methods=["GET"])
def carrera_cantidad_postulantes_anio():
    with open('source/tests/json/api_carreras_cantidad_postulantes_anio.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/TEST/cantidad-ingresantes/", methods=["GET"])
def carrera_cantidad_ingresantes():
    with open('source/tests/json/api_carreras_cantidad_ingresantes.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/TEST/cantidad-ingresantes/2019/", methods=["GET"])
def carrera_cantidad_ingresantes_anio():
    with open('source/tests/json/api_carreras_cantidad_ingresantes_anio.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/TEST/cantidad-cursantes/", methods=["GET"])
def carrera_cantidad_cursantes():
    with open('source/tests/json/api_carreras_cantidad_cursantes.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/TEST/cantidad-cursantes/2019/", methods=["GET"])
def carrera_cantidad_cursantes_anio():
    with open('source/tests/json/api_carreras_cantidad_cursantes_anio.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/TEST/materiascursadas/", methods=["GET"])
def carrera_materiascursadas():
    with open('source/tests/json/api_carreras_materiascursadas.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/TEST/cantidad-cursantes/<anio>/", methods=["GET"])
def cantidad_cursantes(anio):
    with open('source/tests/json/api_carreras_cantidad_cursantes_anio.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/TEST/cantidad-ingresantes/<anio>/", methods=["GET"])
def cantidad_ingresantes(anio):
    with open('source/tests/json/api_carreras_cantidad_ingresantes_anio.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/TEST/cantidad-graduados/<anio>/", methods=["GET"])
def cantidad_graduados(anio):
    with open('source/tests/json/api_carreras_cantidad_graduados_anio.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)