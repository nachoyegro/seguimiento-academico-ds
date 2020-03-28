from pandas.io.json import json_normalize
import pandas as pd


class DataTransformer:

    def transform_to_dataframe(self, data):
        return json_normalize(data)

    def transform_materiascursadas_to_dataframe(self, data):
        materias = json_normalize(data)
        materias.rename(columns={'materia': 'codigo'}, inplace=True)
        return materias

    def merge_materias_con_plan(self, materias, plan):
        return pd.merge(materias, plan, on=['codigo'])