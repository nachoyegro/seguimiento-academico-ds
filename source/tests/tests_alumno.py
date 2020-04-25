from manipulator import DataManipulator
from transformer import DataTransformer
import pandas as pd
import numpy as np
import unittest
import json


class AlumnoTest(unittest.TestCase):

    def setUp(self):
        self.manipulator = DataManipulator()
        self.transformer = DataTransformer()
        with open('tests/json/api_carreras_materiascursadas.json', 'r') as archivo_alumnos:
            data = json.loads(archivo_alumnos.read())
            self.df_materiascursadas = self.transformer.transform_materiascursadas_to_dataframe(data)

        with open('tests/json/api_carreras_plan.json', 'r') as archivo_plan:
            data = json.loads(archivo_plan.read())
            self.df_plan = self.transformer.transform_to_dataframe(data)
        self.dataframe = self.transformer.merge_materias_con_plan(
            self.df_materiascursadas, self.df_plan)

    def test_porcentaje_nucleos(self):
        materias_alumno = self.manipulator.filtrar_materias_de_alumno(self.dataframe, "1")
        data = self.manipulator.porcentajes_aprobadas_areas(
        self.df_plan, materias_alumno)
        self.assertEqual(data['Inglés'], 50) # Tiene el 50% aprobado segun el mock

    def test_porcentaje_nucleos_dentro_periodo(self):
        materias_alumno = self.manipulator.filtrar_materias_de_alumno(self.dataframe, "1")
        filtradas_periodo = self.manipulator.filtrar_periodo(materias_alumno, '2018-02-10', '2020-02-10')
        data = self.manipulator.porcentajes_aprobadas_areas(self.df_plan, filtradas_periodo)
        self.assertEqual(data['Inglés'], 50) # Tiene el 50% aprobado segun el mock

    def test_porcentaje_nucleos_fuera_periodo(self):
        materias_alumno = self.manipulator.filtrar_materias_de_alumno(self.dataframe, "1")
        filtradas_periodo = self.manipulator.filtrar_periodo(materias_alumno, '2018-02-10', '2018-10-10')
        data = self.manipulator.porcentajes_aprobadas_areas(self.df_plan, filtradas_periodo)
        self.assertEqual(data['Inglés'], 0) # Tiene el 0% aprobado segun el mock

    def test_porcentaje_areas(self):
        materias_alumno = self.manipulator.filtrar_materias_de_alumno(self.dataframe, "1")
        data = self.manipulator.porcentajes_aprobadas_nucleos(
        self.df_plan, materias_alumno)
        self.assertEqual("%.2f" % data['I'], '33.33') # Segun el mock, tiene el 33.333333%, lo limito a 2 decimales

    def test_porcentaje_areas_dentro_periodo(self):
        materias_alumno = self.manipulator.filtrar_materias_de_alumno(self.dataframe, "1")
        filtradas_periodo = self.manipulator.filtrar_periodo(materias_alumno, '2018-02-10', '2020-10-10')
        data = self.manipulator.porcentajes_aprobadas_nucleos(
        self.df_plan, filtradas_periodo)
        self.assertEqual("%.2f" % data['I'], '33.33') # Segun el mock, tiene el 33.333333%, lo limito a 2 decimales

    def test_porcentaje_areas_fuera_periodo(self):
        materias_alumno = self.manipulator.filtrar_materias_de_alumno(self.dataframe, "1")
        filtradas_periodo = self.manipulator.filtrar_periodo(materias_alumno, '2018-02-10', '2018-10-10')
        data = self.manipulator.porcentajes_aprobadas_nucleos(
        self.df_plan, filtradas_periodo)
        self.assertEqual("%.2f" % data['I'], '0.00') # Segun el mock, tiene el 0%