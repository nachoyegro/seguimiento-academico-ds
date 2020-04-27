from manipulator import DataManipulator
from transformer import DataTransformer
import pandas as pd
import numpy as np
import unittest
import json


class MateriasPlanTest(unittest.TestCase):

    def setUp(self):
        self.manipulator = DataManipulator()
        transformer = DataTransformer()
        with open('source/tests/json/api_carreras_materiascursadas.json', 'r') as archivo_alumnos:
            data = json.loads(archivo_alumnos.read())
            df_materias = transformer.transform_materiascursadas_to_dataframe(data)
        with open('source/tests/json/plan_test.json', 'r') as archivo_plan:
            data = json.loads(archivo_plan.read())
            df_plan = transformer.transform_to_dataframe(data)
        self.dataframe = transformer.merge_materias_con_plan(
            df_materias, df_plan)

    def test_alumnos_faltan_aprobar_materia(self):
        """
            El listado de materias tiene 9 alumnos que faltan aprobar la materia 01051
        """
        alumnos = self.manipulator.alumnos_falta_aprobar_materia_series(
            self.dataframe, '01051')
        self.assertEqual(len(alumnos), 9)

    def test_alumnos_de_materia(self):
        """
            Quiero los alumnos de una materia, sin importar si aprobaron o no o si estan repetidos
        """
        alumnos = self.manipulator.filtrar_alumnos_de_materia(
            self.dataframe,  '90028')
        self.assertEqual(len(alumnos), 5)

    def test_alumnos_periodo_materia(self):
        """
            Quiero los alumnos de una materia, en un periodo determinado
        """
        alumnos = self.manipulator.filtrar_alumnos_de_materia_periodo(
            self.dataframe, '90028', '2012-01-01', '2014-10-10')
        self.assertEqual(len(alumnos), 3)

    def test_cantidad_alumnos_aprobados(self):
        """
            Quiero los alumnos de una materia que aprobaron en ese periodo
        """
        alumnos = self.manipulator.filtrar_alumnos_de_materia_periodo(
            self.dataframe, '90028', '2012-01-01', '2014-10-10')
        cantidad = self.manipulator.cantidad_alumnos_aprobados(
            alumnos, '90028')
        self.assertEqual(cantidad, 1)

    def test_cantidad_alumnos_desaprobados(self):
        """
            Quiero los alumnos de una materia que desaprobaron en ese periodo
        """
        alumnos = self.manipulator.filtrar_alumnos_de_materia_periodo(
            self.dataframe, '90028', '2012-01-01', '2014-10-10')
        cantidad = self.manipulator.cantidad_alumnos_desaprobados(
            alumnos, '90028')
        self.assertEqual(cantidad, 2)

    def test_cantidad_alumnos_ausentes(self):
        """
            Quiero los alumnos de una materia que estuvieron ausentes en ese periodo
        """
        alumnos = self.manipulator.filtrar_alumnos_de_materia_periodo(
            self.dataframe, '01033', '2001-01-01', '2015-10-10')
        cantidad = self.manipulator.cantidad_alumnos_ausentes(alumnos, '01033')
        self.assertEqual(cantidad, 1)

    def test_cantidad_alumnos_pendientes(self):
        """
            Quiero los alumnos de una materia pendientes en ese periodo
        """
        alumnos = self.manipulator.filtrar_alumnos_de_materia_periodo(
            self.dataframe, '01045', '2001-01-01', '2020-10-10')
        cantidad = self.manipulator.cantidad_alumnos_pendientes(
            alumnos, '01045')
        self.assertEqual(cantidad, 1)

    def test_cantidad_alumnos_falta_aprobar_periodo_grande(self):
        """
            Quiero los alumnos de una materia que faltan aprobar en ese periodo
            Hay que tener en cuenta que para saber quienes faltan aprobar en un periodo, 
            tengo que tener en cuenta el historial de aprobaciones. No me sirve el filtro del inicio
        """
        alumnos = self.manipulator.filtrar_periodo(
            self.dataframe, None, '2020-10-10')
        cantidad = self.manipulator.cantidad_alumnos_falta_aprobar(
            alumnos, '90028')
        self.assertEqual(cantidad, 9)

    def test_cantidad_alumnos_falta_aprobar_periodo_corto(self):
        """
            Quiero los alumnos de una materia que faltan aprobar en ese periodo
            Hay que tener en cuenta que para saber quienes faltan aprobar en un periodo, 
            tengo que tener en cuenta el historial de aprobaciones. No me sirve el filtro del inicio
        """
        alumnos = self.manipulator.filtrar_periodo(
            self.dataframe, None, '2013-12-12')
        cantidad = self.manipulator.cantidad_alumnos_falta_aprobar(
            alumnos, '90028')
        self.assertEqual(cantidad, 5)


    def test_periodo_solo_fecha_inicio(self):
        alumnos = self.manipulator.filtrar_periodo(
            self.dataframe, '2014-07-01', None)
        self.assertEqual(len(alumnos), 9)

    def test_periodo_solo_fecha_fin(self):
        alumnos = self.manipulator.filtrar_periodo(
            self.dataframe, None, '2018-01-01')
        self.assertEqual(len(alumnos), 12)

    def test_periodo_sin_fechas(self):
        """ 
            Test cuantas cursadas tengo filtrando sin fechas
            Deberia darme todas
        """
        alumnos = self.manipulator.filtrar_periodo(
            self.dataframe, None, None)
        self.assertEqual(len(alumnos), 20)


if __name__ == '__main__':
    unittest.main()
