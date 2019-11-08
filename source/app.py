# app.py - a minimal flask api using flask_restful
from flask import Flask, escape, request
from provider import DataProvider
from transformer import DataTransformer
from manipulator import DataManipulator
import json
from config import app
from unittest import TestLoader, runner
from argparse import ArgumentParser
from jwt_decorator import tiene_jwt, get_token
import pandas as pd

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
    token = dp.retrieve_token(
        username=app.config['USERNAME'], password=app.config['PASSWORD'])
    #data = dp.retrieve_plan(token, 'W', '2019')
    #data = dp.retrieve_materiascursadas(token, 'W')
    #data = dp.get_materiascursadas(token, 'W')
    data = dp.get_inscriptos(token, 'W')
    #dataframe = DataTransformer().transform_to_dataframe(data)
    return json.dumps(data)


@app.route('/materias/<cod_carrera>/<cod_materia>/recursantes')
@tiene_jwt
def recursantes_materia(cod_carrera, cod_materia):

    token = get_token(request)

    cod_materia = cod_materia.zfill(5)
    dm = DataManipulator()

    # Filtro los inscriptos de la carrera y materia
    inscriptos = DataProvider().get_inscriptos(token, cod_carrera)
    inscriptos_df = DataTransformer().transform_to_dataframe(inscriptos)
    inscriptos_df = dm.filtrar_alumnos_de_materia(inscriptos_df, cod_materia)

    # Filtro las cursadas de la carrera y materia
    cursadas = DataProvider().get_materiascursadas(token, cod_carrera)
    cursadas_df = DataTransformer().transform_to_dataframe(cursadas)
    cursadas_df = dm.filtrar_alumnos_de_materia(cursadas_df, cod_materia)

    merge_df = pd.merge(inscriptos_df, cursadas_df, on=['alumno', 'materia'])

    return merge_df['alumno'].value_counts()


@app.route('/materias/<cod_materia>/basicos')
@tiene_jwt
def datos_basicos_materia(cod_materia):
    # TODO: falta chequear permisos de token (fecha de expiracion y carreras)
    # Proceso los argumentos
    cod_materia = cod_materia.zfill(5)
    fecha_inicio = request.args.get('inicio')
    fecha_fin = request.args.get('fin')
    carreras_str = request.args.get('carreras')
    carreras = carreras_str.split(',') if carreras_str else []
    # Traigo las materias cursadas
    json_data = DataProvider().retrieve_materiascursadas()
    data = DataTransformer().transform_to_dataframe(json_data)
    manipulator = DataManipulator()
    df = manipulator.filtrar_carreras(data, carreras)
    df = manipulator.filtrar_alumnos_de_materia_periodo(
        df, cod_materia, fecha_inicio, fecha_fin)
    aprobados = manipulator.cantidad_alumnos_aprobados(df, cod_materia)
    desaprobados = manipulator.cantidad_alumnos_desaprobados(df, cod_materia)
    ausentes = manipulator.cantidad_alumnos_ausentes(df, cod_materia)
    faltantes = manipulator.cantidad_alumnos_falta_aprobar(df, cod_materia)
    nombre = manipulator.get_nombre_materia(df, cod_materia)
    return json.dumps([{'Materia': cod_materia,
                        'Nombre': nombre,
                        'Aprobados': aprobados,
                        'Ausentes': ausentes,
                        'Desaprobados': desaprobados,
                        'Faltantes': faltantes}])


@app.route('/alumnos/<legajo>/porcentajes-areas')
@tiene_jwt
def porcentajes_areas_alumno(legajo):
    token = get_token(request)
    fecha_inicio = request.args.get('inicio')
    fecha_fin = request.args.get('fin')
    plan = request.args.get('plan')

    manipulator = DataManipulator()
    carreras_str = request.args.get('carreras')

    carreras = carreras_str.split(',') if carreras_str else []
    df = DataProvider().get_materias_cursadas(token, carreras)
    # TODO: falta concatenarle los planes
    df = manipulator.filtrar_periodo(df, fecha_inicio, fecha_fin)
    porcentajes = manipulator.porcentajes_aprobadas_areas(df, legajo)
    return json.dumps([porcentajes])


@app.route('/alumnos/<legajo>/creditos')
@tiene_jwt
def creditos_alumno(legajo):
    # Saco el token del request
    token = get_token(request)
    # Formateo los args
    fecha_inicio = request.args.get('inicio')
    fecha_fin = request.args.get('fin')
    # Tiene que ser una sola carrera y un solo plan para calcular creditos
    carrera = request.args.get('carrera')
    plan = request.args.get('plan')

    # Inicializo los helpers
    manipulator = DataManipulator()
    provider = DataProvider()
    transformer = DataTransformer()
    # Traigo las cursadas
    cursadas_json = provider.get_materiascursadas(token, carrera)
    cursadas_data = transformer.transform_to_dataframe(cursadas_json)
    # Traigo el plan
    plan_json = provider.get_plan(token, carrera, plan)
    plan_data = transformer.transform_to_dataframe(plan_json)
    data = transformer.merge_materias_con_plan(cursadas_data, plan_data)

    # Filtro periodo
    #df = manipulator.filtrar_carreras(data, carrera)
    df = manipulator.filtrar_periodo(data, fecha_inicio, fecha_fin)

    # Filtro las materias
    materias_alumno = manipulator.filtrar_materias_de_alumno(df, legajo)
    aprobadas = manipulator.filtrar_aprobados(materias_alumno)

    # Filtro los nucleos
    basico = manipulator.filtrar_nucleo(aprobadas, 'B')
    avanzado = manipulator.filtrar_nucleo(aprobadas, 'A')
    introductorio = manipulator.filtrar_nucleo(aprobadas, 'I')
    complementario = manipulator.filtrar_nucleo(aprobadas, 'C')

    # Cuento la cantidad de creditos de los nucleos
    creditos_aprobadas = manipulator.cantidad_creditos(aprobadas)
    creditos_basico = manipulator.cantidad_creditos(basico)
    creditos_avanzado = manipulator.cantidad_creditos(avanzado)
    creditos_introductorio = manipulator.cantidad_creditos(introductorio)
    creditos_complementario = manipulator.cantidad_creditos(complementario)
    return json.dumps([{
        'Total': creditos_aprobadas,
        'Basico': creditos_basico,
        'Avanzado': creditos_avanzado,
        'Introductorio': creditos_introductorio,
        'Complementario': creditos_complementario}])


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
