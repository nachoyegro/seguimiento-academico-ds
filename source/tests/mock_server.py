from http_server_mock import HttpServerMock
import json

mock_app = HttpServerMock(__name__)

@mock_app.route("/api/token/", methods=["POST"])
def token():
    return json.dumps({
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU4Nzk5MjIyNCwianRpIjoiN2EwMzdlNGYxOGFmNDVmOWE1YzcxZDRhYzhiMDg1ODEiLCJ1c2VyX2lkIjoxLCJjYXJyZXJhcyI6WyJBIiwiQiIsIkMiLCJEIiwiRSIsIkYiLCJHIiwiSCIsIkkiLCJKIiwiSjIiLCJLIiwiTCIsIk4yIiwiUCIsIlEiLCJPIiwiUiIsIlMiLCJOIiwiTSIsIlQiLCJBMSIsIkcxIiwiVSIsIlYiLCJWMSIsIlciLCJIMSJdLCJ1c2VybmFtZSI6ImFkbWluIn0.2QgqtOEsSreA-yp43qJsTyno_K6ptyB_WkbPUS1doCQ",
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTg3OTkyMjI0LCJqdGkiOiJlNTAyNTYzZWE5MmI0MDYwOTczYTAxNDE5ODkxMDU4OSIsInVzZXJfaWQiOjEsImNhcnJlcmFzIjpbIkEiLCJCIiwiQyIsIkQiLCJFIiwiRiIsIkciLCJIIiwiSSIsIkoiLCJKMiIsIksiLCJMIiwiTjIiLCJQIiwiUSIsIk8iLCJSIiwiUyIsIk4iLCJNIiwiVCIsIkExIiwiRzEiLCJVIiwiViIsIlYxIiwiVyIsIkgxIl0sInVzZXJuYW1lIjoiYWRtaW4ifQ.e9BquoAy_22-pzLKyxxBY6PEZmTJdCYX7-sYBJgZLCk"
                        })

@mock_app.route("/api/carreras/W/alumnos/", methods=["GET"])
def carrera_alumnos():
    with open('tests/json/api_carreras_alumnos.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/W/planes/2015/cantidad-materias-necesarias/", methods=["GET"])
def carrera_plan_materias_necesarias():
    with open('tests/json/api_carrera_planes_anio_cantidad_materias_necesarias.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)
    
@mock_app.route("/api/carreras/W/planes/", methods=["GET"])
def carrera_planes():
    with open('tests/json/api_carreras_planes.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/W/planes/2015/", methods=["GET"])
def carrera_planes_anio():
    with open('tests/json/api_carreras_planes_anio.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/W/inscripciones/", methods=["GET"])
def carrera_inscripciones():
    with open('tests/json/api_carreras_inscripciones.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/W/cantidad-graduados/", methods=["GET"])
def carrera_cantidad_graduados():
    with open('tests/json/api_carreras_cantidad_graduados.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/W/cantidad-graduados/2019/", methods=["GET"])
def carrera_cantidad_graduados_anio():
    with open('tests/json/api_carreras_cantidad_graduados_anio.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/W/cantidad-postulantes/", methods=["GET"])
def carrera_cantidad_postulantes():
    with open('tests/json/api_carreras_cantidad_postulantes.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/W/cantidad-postulantes/2019/", methods=["GET"])
def carrera_cantidad_postulantes_anio():
    with open('tests/json/api_carreras_cantidad_postulantes_anio.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/W/cantidad-ingresantes/", methods=["GET"])
def carrera_cantidad_ingresantes():
    with open('tests/json/api_carreras_cantidad_ingresantes.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/W/cantidad-ingresantes/2019/", methods=["GET"])
def carrera_cantidad_ingresantes_anio():
    with open('tests/json/api_carreras_cantidad_ingresantes_anio.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/W/cantidad-cursantes/", methods=["GET"])
def carrera_cantidad_cursantes():
    with open('tests/json/api_carreras_cantidad_cursantes.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)

@mock_app.route("/api/carreras/W/cantidad-cursantes/2019/", methods=["GET"])
def carrera_cantidad_cursantes_anio():
    with open('tests/json/api_carreras_cantidad_cursantes_anio.json', 'r') as archivo:
        data = json.loads(archivo.read())
    return json.dumps(data)