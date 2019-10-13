from manipulator import DataManipulator
from transformer import DataTransformer
import pandas as pd
import numpy as np
import unittest
import json

class BaseTest(unittest.TestCase):

    def setUp(self):
        with open('../alumnos_test.json', 'r') as archivo_alumnos:
            data=json.loads(archivo_alumnos.read())
            self.dataframe = DataTransformer(data).transform_to_dataframe()
            self.manipulator = DataManipulator()

    def test_alumnos_faltan_aprobar_materia(self):
        """
            El listado de materias tiene 2 alumnos que faltan aprobar la materia COMPUTADORES
        """
        alumnos = self.manipulator.alumnos_falta_aprobar_materia_series(self.dataframe, '273')
        self.assertEqual(len(alumnos), 2)

    def test_alumnos_de_materia(self):
        alumnos = self.manipulator.filtrar_alumnos_de_materia(self.dataframe,  '628')
        self.assertEqual(len(alumnos), 7)

    def test_alumnos_periodo_materia(self):
        alumnos = self.manipulator.filtrar_alumnos_de_materia_periodo(self.dataframe, '628', '2001-01-01', '2010-10-10')
        self.assertEqual(len(alumnos), 7)

    def test_cantidad_alumnos_aprobados(self):
        alumnos = self.manipulator.filtrar_alumnos_de_materia_periodo(self.dataframe, '628', '2001-01-01', '2010-10-10')
        cantidad = self.manipulator.cantidad_alumnos_aprobados(self.dataframe, '628')
        self.assertEqual(cantidad, 3)

    def test_cantidad_alumnos_desaprobados(self):
        alumnos = self.manipulator.filtrar_alumnos_de_materia_periodo(self.dataframe, '628', '2001-01-01', '2010-10-10')
        cantidad = self.manipulator.cantidad_alumnos_desaprobados(self.dataframe, '628')
        self.assertEqual(cantidad, 1)

    def test_cantidad_alumnos_ausentes(self):
        alumnos = self.manipulator.filtrar_alumnos_de_materia_periodo(self.dataframe, '628', '2001-01-01', '2010-10-10')
        cantidad = self.manipulator.cantidad_alumnos_ausentes(self.dataframe, '628')
        self.assertEqual(cantidad, 2)

    def test_cantidad_alumnos_pendientes(self):
        alumnos = self.manipulator.filtrar_alumnos_de_materia_periodo(self.dataframe, '628', '2001-01-01', '2010-10-10')
        cantidad = self.manipulator.cantidad_alumnos_pendientes(self.dataframe, '628')
        self.assertEqual(cantidad, 1)

    def test_cantidad_alumnos_falta_aprobar(self):
        alumnos = self.manipulator.filtrar_alumnos_de_materia_periodo(self.dataframe, '628', '2001-01-01', '2010-10-10')
        cantidad = self.manipulator.cantidad_alumnos_falta_aprobar(self.dataframe, '628')
        self.assertEqual(cantidad, 0)

if __name__ == '__main__':
    unittest.main()
