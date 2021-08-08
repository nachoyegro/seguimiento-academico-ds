from transformer import DataTransformer
import pandas as pd
import numpy as np
import unittest
import json
from datetime import date, datetime


class TransformerTest(unittest.TestCase):

    def setUp(self):
        self.transformer = DataTransformer()

    def test_periodo_segundo_semestre(self):
        fecha = '2020-12-12'
        semestre_esperado = '2020-S2'
        semestre_resultado = self.transformer.periodo_semestre(fecha)
        self.assertEqual(semestre_esperado, semestre_resultado)

    def test_periodo_primer_semestre(self):
        fecha = '2020-05-12'
        semestre_esperado = '2020-S1'
        semestre_resultado = self.transformer.periodo_semestre(fecha)
        self.assertEqual(semestre_esperado, semestre_resultado)

    def test_forma_aprobacion_encontrada(self):
        forma_aprobacion = 'P'
        esperado = 'Promocion'
        resultado = self.transformer.get_forma_aprobacion(forma_aprobacion)
        self.assertEqual(esperado, resultado)

    def test_forma_aprobacion_no_encontrada(self):
        """
            Si la forma de aprobación no existe, devuelve la pedida
        """
        forma_aprobacion = 'Pw'
        esperado = 'Pw'
        resultado = self.transformer.get_forma_aprobacion(forma_aprobacion)
        self.assertEqual(esperado, resultado)

    def test_fecha_periodo_primer_semestre(self):
        """
            Si la fecha esta comprendida entre el mes 4 y el 9, pertenece al primer semestre
            Porque las notas del segundo semestre pueden llegar a cerrarse en el mes 3.
        """
        fecha = '2020-05-12'
        semestre_esperado = '2020-06-30'
        semestre_resultado = self.transformer.fecha_periodo(fecha)
        self.assertEqual(semestre_esperado, semestre_resultado)

    def test_fecha_periodo_segundo_semestre_anio_anterior(self):
        """
            Si la fecha esta comprendida entre el mes 1 y el 3, 
            pertenece al segundo semestre del año anterior
        """
        fecha = '2020-02-12'
        semestre_esperado = '2019-12-31'
        semestre_resultado = self.transformer.fecha_periodo(fecha)
        self.assertEqual(semestre_esperado, semestre_resultado)

    def test_fecha_periodo_segundo_semestre_mismo_anio(self):
        """
            Si la fecha esta comprendida entre el mes 10 y el 12, 
            pertenece al segundo semestre de ese mismo año
        """
        fecha = '2020-11-12'
        semestre_esperado = '2020-12-31'
        semestre_resultado = self.transformer.fecha_periodo(fecha)
        self.assertEqual(semestre_esperado, semestre_resultado)

    def test_timestamp_to_semester(self):
        timestamp = '2020-07-01 12:12:12'
        esperado = '2020-S2'
        resultado = self.transformer.transform_timestamp_to_semester(timestamp)
        self.assertEqual(esperado, resultado)

    def test_timestamp_to_semester_1st(self):
        timestamp = '2020-01-01 12:12:12'
        esperado = '2020-S1'
        resultado = self.transformer.transform_timestamp_to_semester(timestamp)
        self.assertEqual(esperado, resultado)

    def test_date_to_semester(self):
        fecha = date(2020, 7, 1)
        esperado = '2020-S2'
        resultado = self.transformer.transform_date_to_semester(fecha)
        self.assertEqual(esperado, resultado)

    def test_date_to_semester_1st(self):
        fecha = date(2020, 1, 1)
        esperado = '2020-S1'
        resultado = self.transformer.transform_date_to_semester(fecha)
        self.assertEqual(esperado, resultado)

    def test_timestamp_to_datetime(self):
        timestamp = '2020-01-01 12:12:12'
        esperado = datetime(2020, 1, 1, 12, 12, 12)
        resultado = self.transformer.transform_timestamp_to_datetime(timestamp)
        self.assertEqual(esperado, resultado)

    def test_merge_materias_con_promedio(self):
        pass

    def test_merge_materias_con_plan(self):
        pass

    def test_transform_scores_unicos(self):
        pass

    def test_materiascursadas_to_dataframe(self):
        pass

    def test_transform_to_dataframe(self):
        pass