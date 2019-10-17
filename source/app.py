# app.py - a minimal flask api using flask_restful
from flask import Flask, escape, request
from provider import DataProvider
from transformer import DataTransformer
from manipulator import DataManipulator
import json
from config import app
from unittest import TestLoader, runner
from argparse import ArgumentParser
from jwt_decorator import tiene_jwt

parser = ArgumentParser(prog='App',
                        description='App de Flask')

parser.add_argument(
    'mode', type=str, help='Modo de ejecucion (runserver|tests)'
)

args = parser.parse_args()

@app.route('/')
def home():
    """
        Token must come as part of the request
    """
    dp = DataProvider()
    #token = dp.retrieve_token(username=app.config['USERNAME'], password=app.config['PASSWORD'])
    data = dp.retrieve_materiascursadas()
    dataframe = DataTransformer(data).transform_to_dataframe()
    return dataframe

@app.route('/carreras/<cod_carrera>/materias/<cod_materia>/basicos')
@tiene_jwt
def datos_basicos_materia(cod_carrera, cod_materia):
    #TODO: falta token
    json_data = DataProvider().retrieve_materiascursadas()
    data = DataTransformer(json_data).transform_to_dataframe()
    manipulator = DataManipulator()
    fecha_inicio = request.args.get('inicio')
    fecha_fin = request.args.get('fin')
    if fecha_inicio and fecha_fin:
        df = manipulator.filtrar_alumnos_de_materia_periodo(data, cod_materia, fecha_inicio, fecha_fin)
    else:
        df = manipulator.filtrar_alumnos_de_materia(data, cod_materia)
    aprobados = manipulator.cantidad_alumnos_aprobados(df, cod_materia)
    desaprobados = manipulator.cantidad_alumnos_desaprobados(df, cod_materia)
    ausentes = manipulator.cantidad_alumnos_ausentes(df, cod_materia)
    faltantes = manipulator.cantidad_alumnos_falta_aprobar(df, cod_materia)
    return json.dumps([{'Materia': cod_materia, 
                        'Aprobados': aprobados, 
                        'Ausentes': ausentes, 
                        'Desaprobados': desaprobados,
                        'Faltantes': faltantes}])

@app.route('/carreras/<cod_carrera>/alumnos/<legajo>/porcentajes-areas')
def porcentajes_areas_alumno(cod_carrera, legajo):
    json_data = DataProvider().retrieve_materiascursadas()
    data = DataTransformer(json_data).transform_to_dataframe()
    manipulator = DataManipulator()
    return json.dumps([manipulator.porcentajes_aprobadas_por_area(data, legajo)])


def runserver():
    app.run(debug=True, host='0.0.0.0')

def tests():
    loader = TestLoader()
    tests = loader.discover('tests/')
    testRunner = runner.TextTestRunner()
    testRunner.run(tests)


modes = {
    'runserver': runserver,
    'tests': tests
}[args.mode]()
