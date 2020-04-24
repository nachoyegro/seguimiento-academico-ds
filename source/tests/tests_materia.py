from manipulator import DataManipulator
from transformer import DataTransformer
import pandas as pd
import numpy as np
import unittest
import json


class MateriaTest(unittest.TestCase):

    def setUp(self):
        self.manipulator = DataManipulator()
        self.transformer = DataTransformer()
        with open('tests/json/api_carreras_inscripciones.json', 'r') as archivo_alumnos:
            data = json.loads(archivo_alumnos.read())
            self.df_inscripciones = self.transformer.transform_materiascursadas_to_dataframe(data)

        with open('tests/json/api_carreras_materiascursadas.json', 'r') as archivo_alumnos:
            data = json.loads(archivo_alumnos.read())
            self.df_cursadas = self.transformer.transform_materiascursadas_to_dataframe(data)


    def test_recursante_repetido(self):
        """
            El alumno 1 va a recursar la materia 90028 por tercera vez
            El alumno 9 va a recursarla por 2da vez
            El alumno 10 ya la aprobo luego de recursarla
        """
        recursantes = self.manipulator.get_recursantes(self.df_cursadas, self.df_inscripciones, '90028')
        esperado = {"1": 2, "9": 1}
        self.assertEqual(recursantes, esperado)
