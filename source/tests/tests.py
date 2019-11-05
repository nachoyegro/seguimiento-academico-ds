from manipulator import DataManipulator
from transformer import DataTransformer
import pandas as pd
import numpy as np
import unittest
import json


class BaseTest(unittest.TestCase):

    def setUp(self):
        with open('../alumnos_test.json', 'r') as archivo_alumnos:
            data = json.loads(archivo_alumnos.read())
            self.dataframe = DataTransformer().transform_to_dataframe(data)
            self.manipulator = DataManipulator()

    def test_alumnos_faltan_aprobar_materia(self):
        """
            El listado de materias tiene 2 alumnos que faltan aprobar la materia COMPUTADORES
        """
        alumnos = self.manipulator.alumnos_falta_aprobar_materia_series(
            self.dataframe, '273')
        self.assertEqual(len(alumnos), 2)

    def test_alumnos_de_materia(self):
        alumnos = self.manipulator.filtrar_alumnos_de_materia(
            self.dataframe,  '628')
        self.assertEqual(len(alumnos), 7)

    def test_alumnos_periodo_materia(self):
        alumnos = self.manipulator.filtrar_alumnos_de_materia_periodo(
            self.dataframe, '628', '2001-01-01', '2010-10-10')
        self.assertEqual(len(alumnos), 7)

    def test_cantidad_alumnos_aprobados(self):
        alumnos = self.manipulator.filtrar_alumnos_de_materia_periodo(
            self.dataframe, '628', '2001-01-01', '2010-10-10')
        cantidad = self.manipulator.cantidad_alumnos_aprobados(alumnos, '628')
        self.assertEqual(cantidad, 3)

    def test_cantidad_alumnos_desaprobados(self):
        alumnos = self.manipulator.filtrar_alumnos_de_materia_periodo(
            self.dataframe, '628', '2001-01-01', '2010-10-10')
        cantidad = self.manipulator.cantidad_alumnos_desaprobados(
            alumnos, '628')
        self.assertEqual(cantidad, 0)

    def test_cantidad_alumnos_ausentes(self):
        alumnos = self.manipulator.filtrar_alumnos_de_materia_periodo(
            self.dataframe, '628', '2001-01-01', '2010-10-10')
        cantidad = self.manipulator.cantidad_alumnos_ausentes(alumnos, '628')
        self.assertEqual(cantidad, 4)

    def test_cantidad_alumnos_pendientes(self):
        alumnos = self.manipulator.filtrar_alumnos_de_materia_periodo(
            self.dataframe, '628', '2001-01-01', '2010-10-10')
        cantidad = self.manipulator.cantidad_alumnos_pendientes(alumnos, '628')
        self.assertEqual(cantidad, 0)

    def test_cantidad_alumnos_falta_aprobar(self):
        alumnos = self.manipulator.filtrar_alumnos_de_materia_periodo(
            self.dataframe, '628', '2001-01-01', '2010-10-10')
        cantidad = self.manipulator.cantidad_alumnos_falta_aprobar(
            alumnos, '628')
        self.assertEqual(cantidad, 0)

    def test_periodo_solo_fecha_inicio(self):
        alumnos = self.manipulator.filtrar_periodo(
            self.dataframe, '2001-07-01', None)
        self.assertEqual(len(alumnos), 154)

    def test_periodo_solo_fecha_fin(self):
        alumnos = self.manipulator.filtrar_periodo(
            self.dataframe, None, '2010-01-01')
        self.assertEqual(len(alumnos), 97)

    def test_periodo_sin_fechas(self):
        alumnos = self.manipulator.filtrar_periodo(
            self.dataframe, None, None)
        self.assertEqual(len(alumnos), 154)


if __name__ == '__main__':
    unittest.main()
