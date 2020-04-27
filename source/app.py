# app.py - a minimal flask api using flask_restful
from flask import Flask, escape, request, Blueprint
from provider import DataProvider
from transformer import DataTransformer
from manipulator import DataManipulator
import json
from config import app
from unittest import TestLoader, runner
from argparse import ArgumentParser
from decorators import tiene_jwt, get_token
import pandas as pd
from datetime import date, timedelta

parser = ArgumentParser(prog='App',
                        description='App de Flask')

parser.add_argument(
    'mode', type=str, help='Modo de ejecucion (runserver|tests)'
)

args = parser.parse_args()

app = Blueprint('app', __name__)

def get_materiascursadas(request, cod_carrera=None, inicio=None, fin=None):

    provider = DataProvider()
    transformer = DataTransformer()
    manipulator = DataManipulator()

    # Saco el token del request
    token = get_token(request)
    # Formateo los args
    fecha_inicio = inicio or request.args.get('inicio')
    fecha_fin = fin or request.args.get('fin')
    # Tiene que ser una sola carrera y un solo plan para calcular creditos
    carrera = cod_carrera or request.args.get('carrera')
    plan = request.args.get('plan')
    # Traigo las cursadas
    cursadas_json = provider.get_materiascursadas(token, carrera)
    cursadas_data = transformer.transform_materiascursadas_to_dataframe(
        cursadas_json)

    # Filtro periodo
    df = manipulator.filtrar_periodo(cursadas_data, fecha_inicio, fecha_fin)
    return df


def get_alumnos_de_materia_periodo(request, cod_materia):
    manipulator = DataManipulator()
    df = get_materiascursadas(request)
    return manipulator.filtrar_alumnos_de_materia(df, cod_materia)

def get_cantidad_materias_necesarias(request):
    provider = DataProvider()
    # Saco el token del request
    token = get_token(request)
    carrera = request.args.get('carrera')
    plan = request.args.get('plan')
    return provider.get_cantidad_materias_necesarias(token, carrera, plan)["cantidad"]


def get_plan(request):
    provider = DataProvider()
    transformer = DataTransformer()

    # Saco el token del request
    token = get_token(request)
    # Formateo los args
    fecha_inicio = request.args.get('inicio')
    fecha_fin = request.args.get('fin')
    # Tiene que ser una sola carrera y un solo plan para calcular creditos
    carrera = request.args.get('carrera')
    plan = request.args.get('plan')
    # Traigo el plan
    plan_json = provider.get_plan(token, carrera, plan)
    plan_data = transformer.transform_to_dataframe(plan_json)
    return plan_data

def get_materiascursadas_plan(request):
    transformer = DataTransformer()

    cursadas_data = get_materiascursadas(request)
    plan_data = get_plan(request)
    data = transformer.merge_materias_con_plan(cursadas_data, plan_data)
    return data, cursadas_data, plan_data

def get_materiascursadas_promedio(request, carrera, inicio=None, fin=None):
    cursadas_data = get_materiascursadas(request, carrera, inicio, fin)

    transformer = DataTransformer()

    #Obtengo los alumnos de la carrera
    token = get_token(request) # Saco el token del request
    alumnos_carrera_json = DataProvider().get_alumnos_de_carrera(token, carrera)
    alumnos_carrera_df = transformer.transform_to_dataframe(alumnos_carrera_json)
    data = transformer.merge_materias_con_promedio(cursadas_data, alumnos_carrera_df)
    return data

@app.route('/')
def home():
    """
        Token must come as part of the request
    """
    dp = DataProvider()
    token = dp.retrieve_token(
        username=app.config['USERNAME'], password=app.config['PASSWORD'])
    # data = dp.retrieve_plan(token, 'W', '2019')
    # data = dp.retrieve_materiascursadas(token, 'W')
    # data = dp.get_materiascursadas(token, 'W')
    data = dp.get_inscriptos(token, 'W')
    # dataframe = DataTransformer().transform_to_dataframe(data)
    return json.dumps(data)


@app.route('/materias/<cod_materia>/recursantes')
@tiene_jwt
def recursantes_materia(cod_materia):
    token = get_token(request)

    cod_materia = cod_materia.zfill(5)
    carrera = request.args.get('carrera')
    dm = DataManipulator()

    # Filtro los inscriptos de la carrera y materia
    inscriptos = DataProvider().get_inscriptos(token, carrera)
    inscriptos_df = DataTransformer().transform_materiascursadas_to_dataframe(inscriptos)

    # Filtro las cursadas de la carrera y materia
    cursadas = DataProvider().get_materiascursadas(token, carrera)
    cursadas_df = DataTransformer().transform_materiascursadas_to_dataframe(cursadas)

    recursantes = dm.get_recursantes(cursadas_df, inscriptos_df, cod_materia)
    return recursantes


@app.route('/materias/<cod_materia>/detalle-aprobados')
@tiene_jwt
def detalle_aprobados(cod_materia):
    manipulator = DataManipulator()
    transformer = DataTransformer()
    df = get_alumnos_de_materia_periodo(request, cod_materia)
    df = manipulator.filtrar_aprobados(df)
    detalle_aprobados = manipulator.cantidades_formas_aprobacion(df)
    data = detalle_aprobados.to_dict()
    resultado = {}
    for nombre, valor in data.items():
        resultado[transformer.get_forma_aprobacion(nombre)] = valor
    return json.dumps([resultado])


@app.route('/materias/<cod_materia>/basicos')
@tiene_jwt
def datos_basicos_materia(cod_materia):
    manipulator = DataManipulator()
    df = get_materiascursadas(request)
    aprobados = manipulator.cantidad_alumnos_aprobados(df, cod_materia)
    desaprobados = manipulator.cantidad_alumnos_desaprobados(df, cod_materia)
    ausentes = manipulator.cantidad_alumnos_ausentes(df, cod_materia)
    faltantes = manipulator.cantidad_alumnos_falta_aprobar(df, cod_materia)
    nombre = manipulator.get_nombre_materia(df, cod_materia)
    return json.dumps([{'Materia': cod_materia,
                        'Aprobados': aprobados,
                        'Ausentes': ausentes,
                        'Desaprobados': desaprobados,
                        'Faltantes': faltantes}])




@app.route('/materias/<cod_materia>/dispersion-notas')
@tiene_jwt
def dispersion_notas(cod_materia):
    transformer = DataTransformer()
    provider = DataProvider()
    token = get_token(request) # Saco el token del request
    df = get_alumnos_de_materia_periodo(request, cod_materia)

    alumnos_carrera_json = provider.get_alumnos_de_carrera(token, request.args.get('carrera'))
    alumnos_carrera_df = transformer.transform_to_dataframe(alumnos_carrera_json)
    data = transformer.merge_materias_con_promedio(df, alumnos_carrera_df)
    return json.dumps([{"Promedio": getattr(row, 'promedio'), "Alumno": getattr(row, 'alumno'), "Nota": getattr(row, 'nota')} for row in data.itertuples()])


@app.route('/alumnos/<legajo>/porcentajes-areas')
@tiene_jwt
def porcentajes_areas_alumno(legajo):
    merged_data, _, plan_data = get_materiascursadas_plan(request)

    fecha_inicio = request.args.get('inicio')
    fecha_fin = request.args.get('fin')
    manipulator = DataManipulator()
    materias_alumno = manipulator.filtrar_materias_de_alumno(
        merged_data, legajo)
    materias_alumno = manipulator.filtrar_periodo(
        materias_alumno, fecha_inicio, fecha_fin)
    data = manipulator.porcentajes_aprobadas_areas(
        plan_data, materias_alumno)
    return json.dumps([{"nombre": nombre, "valor": valor} for nombre, valor in data.items()])


@app.route('/alumnos/<legajo>/porcentajes-nucleos')
@tiene_jwt
def porcentajes_nucleos_alumno(legajo):
    merged_data, _, plan_data = get_materiascursadas_plan(request)

    fecha_inicio = request.args.get('inicio')
    fecha_fin = request.args.get('fin')
    manipulator = DataManipulator()
    materias_alumno = manipulator.filtrar_materias_de_alumno(
        merged_data, legajo)
    materias_alumno = manipulator.filtrar_periodo(
        materias_alumno, fecha_inicio, fecha_fin)
    data = manipulator.porcentajes_aprobadas_nucleos(
        plan_data, materias_alumno)
    return json.dumps([{"nombre": nombre, "valor": valor} for nombre, valor in data.items()])


@app.route('/carreras/<carrera>/alumnos')
@tiene_jwt
def alumnos_carrera(carrera):
    token = get_token(request)
    transformer = DataTransformer()
    json_data = DataProvider().get_alumnos_de_carrera(token, carrera)
    data = transformer.transform_to_dataframe(json_data)
    inscriptos = DataManipulator().inscriptos_por_carrera(data)['alumno']
    return json.dumps([{"nombre": transformer.transform_timestamp_to_semester(key), "cantidad": value} for key, value in inscriptos.items()])

@app.route('/carreras/<carrera>/cantidades-alumnos')
@tiene_jwt
def cantidades_alumnos_carrera(carrera):
    '''
        Deberia retornar una lista del tipo [{"anio": 2015, "graduados": 2, "cursantes": 200, "ingresantes": 100, "postulantes": 500}]
    '''
    token = get_token(request)
    provider = DataProvider()
    graduados = provider.get_graduados(token, carrera)
    ingresantes = provider.get_ingresantes(token, carrera)
    cursantes = provider.get_cursantes(token, carrera)
    return json.dumps([{"Cohorte": cursantes[i]["anio"], 
                        "Graduados": graduados[i]["cantidad"], 
                        "Cursantes": cursantes[i]["cantidad"], 
                        "Ingresantes": ingresantes[i]["cantidad"]}
                        for i in range(0, len(cursantes))
                        ])

@app.route('/carreras/<carrera>/cantidades-ingresantes')
@tiene_jwt
def cantidades_ingresantes_carrera(carrera):
    '''
        Deberia retornar una lista del tipo [{"anio": 2015, "ingresantes": 100}]
    '''
    token = get_token(request)
    provider = DataProvider()
    ingresantes = provider.get_ingresantes(token, carrera)
    return json.dumps([{"Cohorte": dato["anio"], "Alumnos ingresantes": dato["cantidad"]} for dato in ingresantes ])



@app.route('/carreras/<carrera>/cursantes-actual')
@tiene_jwt
def cantidad_cursantes_actual(carrera):
    token = get_token(request)
    provider = DataProvider()
    anio = date.today().year
    cursantes = provider.get_cursantes(token, carrera, anio)
    return json.dumps({'nombre': 'Cursantes del año actual', 'valor': cursantes["cantidad"]})

@app.route('/carreras/<carrera>/ingresantes-actual')
@tiene_jwt
def cantidad_ingresantes_actual(carrera):
    token = get_token(request)
    provider = DataProvider()
    anio = date.today().year
    cursantes = provider.get_ingresantes(token, carrera, anio)
    return json.dumps({'nombre': 'Ingresantes del año actual', 'valor': cursantes["cantidad"]})

@app.route('/carreras/<carrera>/graduados-total')
@tiene_jwt
def cantidad_graduados(carrera):
    token = get_token(request)
    provider = DataProvider()
    anio = date.today().year
    cursantes = provider.get_graduados(token, carrera, anio)
    return json.dumps({'nombre': 'Graduados', 'valor': cursantes["cantidad"]})

@app.route('/widget')
def widget():
    return json.dumps({'nombre': 'Aprobados', 'valor': 55})

@app.route('/alumnos/<legajo>/porcentajes-creditos-nucleos')
@tiene_jwt
def porcentajes_creditos_alumno(legajo):
    merged_data, _, plan_data = get_materiascursadas_plan(request)

    manipulator = DataManipulator()
    # Filtro las materias
    materias_alumno = manipulator.filtrar_materias_de_alumno(
        merged_data, legajo)
    aprobadas = manipulator.filtrar_aprobados(materias_alumno)

    porcentajes = manipulator.porcentajes_creditos_nucleos(
        plan_data, aprobadas)
    return json.dumps([porcentajes])


@app.route('/alumnos/<legajo>/porcentajes-creditos-areas')
@tiene_jwt
def porcentajes_creditos_areas(legajo):
    merged_data, _, plan_data = get_materiascursadas_plan(request)

    manipulator = DataManipulator()
    # Filtro las materias
    materias_alumno = manipulator.filtrar_materias_de_alumno(
        merged_data, legajo)
    aprobadas = manipulator.filtrar_aprobados(materias_alumno)

    porcentajes = manipulator.porcentajes_creditos_areas(
        plan_data, aprobadas)
    return json.dumps([porcentajes])


@app.route('/alumnos/<legajo>/creditos-nucleos')
@tiene_jwt
def creditos_nucleos(legajo):
    merged_data, _, _ = get_materiascursadas_plan(request)

    manipulator = DataManipulator()
    # Filtro las materias
    materias_alumno = manipulator.filtrar_materias_de_alumno(
        merged_data, legajo)
    aprobadas = manipulator.filtrar_aprobados(materias_alumno)

    data = manipulator.cantidades_creditos_nucleos(
        aprobadas, ['B', 'A', 'I', 'C'])

    return json.dumps([data])


@app.route('/alumnos/<legajo>/creditos-areas')
@tiene_jwt
def creditos_areas(legajo):
    merged_data, _, plan_data = get_materiascursadas_plan(request)

    manipulator = DataManipulator()
    # Filtro las materias
    materias_alumno = manipulator.filtrar_materias_de_alumno(
        merged_data, legajo)
    aprobadas = manipulator.filtrar_aprobados(materias_alumno)

    areas = manipulator.areas_unicas(plan_data)

    data = manipulator.cantidades_creditos_areas(aprobadas, areas)

    return json.dumps([data])

@app.route('/alumnos/<legajo>/notas')
@tiene_jwt
def notas_alumno(legajo):
    merged_data, _, plan_data = get_materiascursadas_plan(request)
    manipulator = DataManipulator()
    # Filtro las materias
    materias_alumno = manipulator.filtrar_materias_de_alumno(
        merged_data, legajo)
    return json.dumps([{'Fecha': row['fecha'], 'Materia': row['materia'], 'Plan': row['plan'], 'Nota': row['nota']} for index, row in materias_alumno.iterrows()])

@app.route('/alumnos/<legajo>/scores')
@tiene_jwt
def promedios_alumno(legajo):
    merged_data, _, plan_data = get_materiascursadas_plan(request)
    manipulator = DataManipulator()
    scores = manipulator.get_scores_alumno(merged_data, legajo)
    return json.dumps([{"nombre": row["periodo_semestre"], "valor": row["score_periodo"]} for index,row in DataTransformer().transform_scores_unicos(scores).iterrows()])

@app.route('/alumnos/<legajo>/porcentaje-carrera')
@tiene_jwt
def alumno_porcentaje_carrera(legajo):
    merged_data, _, plan_data = get_materiascursadas_plan(request)
    manipulator = DataManipulator()
    # Filtro las materias
    materias_alumno = manipulator.filtrar_materias_de_alumno(
        merged_data, legajo)
    cantidad_aprobadas = manipulator.cantidad_aprobadas(materias_alumno)
    cantidad_materias_necesarias = get_cantidad_materias_necesarias(request)
    porcentaje = manipulator.porcentaje_aprobadas(cantidad_aprobadas, cantidad_materias_necesarias)
    return json.dumps({'nombre': 'Porcentaje de avance', 'valor': porcentaje})
    
@app.route('/carreras/<carrera>/dispersion-score-promedio')
@tiene_jwt
def dispersion_score_avance(carrera):
    fin = date.today()
    inicio = fin - timedelta(days=365)

    data = get_materiascursadas_promedio(request, carrera, inicio.strftime('%Y-%m-%d'), fin.strftime('%Y-%m-%d'))
    scores = DataManipulator().get_scores_periodos(data)

    return json.dumps([{"Promedio": getattr(row, 'promedio'), "Alumno": getattr(row, 'alumno'), "Score": getattr(row, 'score_periodo')} for row in scores.itertuples()])

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
