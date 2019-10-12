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
        alumnos = self.manipulator.filtrar_alumnos_de_materia_periodo(self.dataframe, '628', '2004-01-01', '2007-07-01')
        self.assertEqual(len(alumnos), 3)

if __name__ == '__main__':
    unittest.main()
