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

bp = Blueprint('rutas', __name__)


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


def get_plan(request, carrera=None):
    provider = DataProvider()
    transformer = DataTransformer()

    # Saco el token del request
    token = get_token(request)
    # Formateo los args
    fecha_inicio = request.args.get('inicio')
    fecha_fin = request.args.get('fin')
    # Tiene que ser una sola carrera y un solo plan para calcular creditos
    carrera = carrera or request.args.get('carrera')
    plan = request.args.get('plan')
    # Traigo el plan
    plan_json = provider.get_plan(token, carrera, plan)
    plan_data = transformer.transform_to_dataframe(plan_json)
    return plan_data


def get_materiascursadas_plan(request, carrera=None):
    transformer = DataTransformer()

    cursadas_data = get_materiascursadas(request, carrera)
    plan_data = get_plan(request, carrera)
    data = transformer.merge_materias_con_plan(cursadas_data, plan_data)
    return data, cursadas_data, plan_data


def get_materiascursadas_promedio(request, carrera, inicio=None, fin=None):
    cursadas_data = get_materiascursadas(request, carrera, inicio, fin)

    transformer = DataTransformer()

    # Obtengo los alumnos de la carrera
    token = get_token(request)  # Saco el token del request
    alumnos_carrera_json = DataProvider().get_alumnos_de_carrera(token, carrera)
    alumnos_carrera_df = transformer.transform_to_dataframe(
        alumnos_carrera_json)
    data = transformer.merge_materias_con_promedio(
        cursadas_data, alumnos_carrera_df)
    return data


@bp.route('/materias/<cod_materia>/recursantes')
@tiene_jwt
def recursantes_materia(cod_materia):
    token = get_token(request)

    cod_materia = cod_materia.zfill(5)
    carrera = request.args.get('carrera')
    fecha_fin = request.args.get('fecha')
    anio = fecha_fin.split('-')[0] if fecha_fin else None
    mes = fecha_fin.split('-')[1] if fecha_fin else None
    semestre = 1 if mes and int(mes) <= 6 else 2
    dm = DataManipulator()

    # Filtro los inscriptos de la carrera y materia
    inscriptos = DataProvider().get_inscriptos(token, carrera, anio, semestre)
    inscriptos_df = DataTransformer().transform_materiascursadas_to_dataframe(inscriptos)

    # Filtro las cursadas de la carrera y materia
    cursadas = DataProvider().get_materiascursadas(token, carrera)
    cursadas_df = DataTransformer().transform_materiascursadas_to_dataframe(cursadas)

    recursantes = dm.get_recursantes(cursadas_df, inscriptos_df, cod_materia)
    return json.dumps([{"Legajo": key , "Cantidad": value} for key, value in recursantes.items()])


@bp.route('/materias/<cod_materia>/detalle-aprobados')
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


@bp.route('/materias/<cod_materia>/basicos')
@tiene_jwt
def datos_basicos_materia(cod_materia):
    manipulator = DataManipulator()
    df = get_materiascursadas(request)
    aprobados = manipulator.cantidad_alumnos_aprobados(df, cod_materia)
    desaprobados = manipulator.cantidad_alumnos_desaprobados(df, cod_materia)
    ausentes = manipulator.cantidad_alumnos_ausentes(df, cod_materia)
    faltantes = manipulator.cantidad_alumnos_falta_aprobar(df, cod_materia)
    nombre = manipulator.get_nombre_materia(df, cod_materia)
    return json.dumps([{'Aprobados': aprobados,
                        'Ausentes': ausentes,
                        'Desaprobados': desaprobados,
                        'Faltantes': faltantes}])


@bp.route('/materias/<cod_materia>/dispersion-notas')
@tiene_jwt
def dispersion_notas(cod_materia):
    transformer = DataTransformer()
    provider = DataProvider()
    token = get_token(request)  # Saco el token del request
    df = get_alumnos_de_materia_periodo(request, cod_materia)

    alumnos_carrera_json = provider.get_alumnos_de_carrera(
        token, request.args.get('carrera'))
    alumnos_carrera_df = transformer.transform_to_dataframe(
        alumnos_carrera_json)
    data = transformer.merge_materias_con_promedio(df, alumnos_carrera_df)
    # Itero para generar el json final
    resultado = []
    for row in data.itertuples():
        nota = getattr(row, 'nota')
        if nota:
            resultado.append({"Promedio": getattr(row, 'promedio'), "Alumno": getattr(row, 'alumno'), "Nota": nota})
    return json.dumps(resultado)

@bp.route('/alumnos/<legajo>/porcentajes-areas')
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


@bp.route('/alumnos/<legajo>/porcentajes-nucleos')
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


@bp.route('/carreras/<carrera>/alumnos')
@tiene_jwt
def alumnos_carrera(carrera):
    token = get_token(request)
    transformer = DataTransformer()
    json_data = DataProvider().get_alumnos_de_carrera(token, carrera)
    data = transformer.transform_to_dataframe(json_data)
    inscriptos = DataManipulator().inscriptos_por_carrera(data)['alumno']
    return json.dumps([{"nombre": transformer.transform_timestamp_to_semester(key), "cantidad": value} for key, value in inscriptos.items()])


@bp.route('/carreras/<carrera>/cantidades-alumnos')
@tiene_jwt
def cantidades_alumnos_carrera(carrera):
    '''
        Deberia retornar una lista del tipo [{"Cohorte": 2015, "Graduados": 2, "Cursantes": 200, "Ingresantes": 100, "postulantes": 500}]
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


@bp.route('/carreras/<carrera>/cantidades-ingresantes')
@tiene_jwt
def cantidades_ingresantes_carrera(carrera):
    '''
        Deberia retornar una lista del tipo [{"anio": 2015, "Ingresantes": 100}]
    '''
    token = get_token(request)
    provider = DataProvider()
    ingresantes = provider.get_ingresantes(token, carrera)
    return json.dumps([{"Cohorte": dato["anio"], "Ingresantes": dato["cantidad"]} for dato in ingresantes])


@bp.route('/carreras/<carrera>/cursantes-actual')
@tiene_jwt
def cantidad_cursantes_actual(carrera):
    token = get_token(request)
    provider = DataProvider()
    anio = date.today().year
    cursantes = provider.get_cursantes(token, carrera, anio)
    return json.dumps({'nombre': 'Cursantes del año actual', 'valor': cursantes["cantidad"]})


@bp.route('/carreras/<carrera>/ingresantes-actual')
@tiene_jwt
def cantidad_ingresantes_actual(carrera):
    token = get_token(request)
    provider = DataProvider()
    anio = date.today().year
    cursantes = provider.get_ingresantes(token, carrera, anio)
    return json.dumps({'nombre': 'Ingresantes del año actual', 'valor': cursantes["cantidad"]})


@bp.route('/carreras/<carrera>/graduados-total')
@tiene_jwt
def cantidad_graduados(carrera):
    token = get_token(request)
    provider = DataProvider()
    anio = date.today().year
    cursantes = provider.get_graduados(token, carrera, anio)
    return json.dumps({'nombre': 'Graduados', 'valor': cursantes["cantidad"]})


@bp.route('/alumnos/<legajo>/notas')
@tiene_jwt
def notas_alumno(legajo):
    merged_data, _, plan_data = get_materiascursadas_plan(request)
    manipulator = DataManipulator()
    # Filtro las materias
    materias_alumno = manipulator.filtrar_materias_de_alumno(
        merged_data, legajo)
    return json.dumps([{'Fecha': row['fecha'], 'Materia': row['materia'], 'Plan': row['plan'], 'Nota': row['nota'], 'Resultado': row['resultado'], 'Acta Examen': row['acta_examen'] or '', 'Acta Promocion': row['acta_promocion'] or ''} for index, row in materias_alumno.iterrows()])


@bp.route('/alumnos/<legajo>/scores')
@tiene_jwt
def promedios_alumno(legajo):
    merged_data, _, plan_data = get_materiascursadas_plan(request)
    manipulator = DataManipulator()
    scores = manipulator.get_scores_alumno(merged_data, legajo)
    return json.dumps([{"nombre": row["periodo_semestre"], "valor": row["score_periodo"]} for index, row in DataTransformer().transform_scores_unicos(scores).iterrows()])


@bp.route('/alumnos/<legajo>/porcentaje-carrera')
@tiene_jwt
def alumno_porcentaje_carrera(legajo):
    merged_data, _, plan_data = get_materiascursadas_plan(request)
    manipulator = DataManipulator()
    # Filtro las materias
    materias_alumno = manipulator.filtrar_materias_de_alumno(
        merged_data, legajo)
    cantidad_aprobadas = manipulator.cantidad_aprobadas(materias_alumno)
    cantidad_materias_necesarias = get_cantidad_materias_necesarias(request)
    porcentaje = manipulator.porcentaje_aprobadas(
        cantidad_aprobadas, cantidad_materias_necesarias)
    return json.dumps({'nombre': 'Porcentaje de avance en carrera', 'valor': str(round(porcentaje, 2))})


@bp.route('/carreras/<carrera>/dispersion-score-promedio')
@tiene_jwt
def dispersion_score_avance(carrera):
    fin = date.today()
    inicio = fin - timedelta(days=int(request.args.get('dias')))

    data = get_materiascursadas_promedio(
        request, carrera, inicio.strftime('%Y-%m-%d'), fin.strftime('%Y-%m-%d'))
    scores = DataManipulator().get_scores_periodos(data)

    return json.dumps([{"Promedio": getattr(row, 'promedio'), "Alumno": getattr(row, 'alumno'), "Score": getattr(row, 'score_periodo')} for row in scores.itertuples()])


@bp.route('/carreras/<carrera>/materias-traba')
@tiene_jwt
def materias_traba(carrera):
    from utils import calcular_score_materia
    merged_data, _, plan_data = get_materiascursadas_plan(request, carrera)
    manipulator = DataManipulator()
    # Filtro las materias
    materias = manipulator.calcular_materias_traba(merged_data)
    return json.dumps([{'Materia': row['materia'], 'Promedio de Aprobación': "%.2f" % row['indice_aprobacion'], 'Obligatorias dependientes': row['cantidad_obligatoria_de'], 'Score': "%.2f" % calcular_score_materia(row['cantidad_obligatoria_de'], row['indice_aprobacion'])} for index, row in materias.iterrows()])


def runserver():
    app.register_blueprint(bp)
    app.run(debug=True, host='0.0.0.0')

def run_prod():
    app.register_blueprint(bp)
    app.run(host='0.0.0.0')


def tests():
    app.testing = True
    loader = TestLoader()
    tests = loader.discover('source/tests/')
    testRunner = runner.TextTestRunner()
    testRunner.run(tests)


modes = {
    'runserver': runserver,
    'prod':run_prod,
    'tests': tests
}[args.mode]()