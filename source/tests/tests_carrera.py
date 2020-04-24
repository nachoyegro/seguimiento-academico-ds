from manipulator import DataManipulator
from transformer import DataTransformer
import pandas as pd
import numpy as np
import unittest
import json


class CarreraTest(unittest.TestCase):

    def setUp(self):
        self.manipulator = DataManipulator()
        transformer = DataTransformer()
        with open('tests/alumnos_test.json', 'r') as archivo_alumnos:
            data = json.loads(archivo_alumnos.read())
            df_materias = transformer.transform_to_dataframe(data)
        with open('tests/plan_test.json', 'r') as archivo_plan:
            data = json.loads(archivo_plan.read())
            df_plan = transformer.transform_to_dataframe(data)
        self.dataframe = transformer.merge_materias_con_plan(
            df_materias, df_plan)