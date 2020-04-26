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

#with app.run("localhost", 8008):
#    r = requests.get("http://localhost:8008/")
    # r.status_code == 200
    # r.text == "Hello world"
